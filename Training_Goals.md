# Training Goals and Skill Application Map

## For: Pawan Singh Kapkoti — Personal Reference

---

## My MSc Skills vs Factory Needs

| MSc Skill | Library/Tool | How It Applies at Copernus |
|---|---|---|
| Data manipulation | pandas | Read SQL Server data, clean batch records, merge tables, aggregate yields |
| Numerical computing | NumPy | Weight calculations, yield percentages, statistical analysis on production data |
| Data visualisation | matplotlib, seaborn | Yield trend charts, giveaway analysis, department comparisons |
| Interactive dashboards | Plotly, Streamlit | Real-time despatch priority board, factory floor screens |
| Database connectivity | SQLAlchemy, pyodbc | Connect Python to SQL Server, run queries, extract data |
| Machine learning | scikit-learn, XGBoost | Predict tomorrow's yield from today's intake, anomaly detection on weight variances |
| Statistical testing | scipy.stats | Are yield differences between departments statistically significant? |
| Data quality | dbt, Great Expectations | Automated checks: are all batch codes present? Do weights balance? |
| Reporting automation | Jupyter, scheduled scripts | Replace manual Excel reports with automated Python notebooks |
| Version control | Git | Track all query changes, rollback if something breaks |
| BI tools | Power BI (PL-300) | Executive dashboards for factory manager, published to web/mobile |

---

## Week-by-Week Training Goals

### Week 1: Understand the Data

**Goal:** Know what data exists and where it lives.

**Tasks:**
1. Get read-only SQL Server access from IT
2. Install Azure Data Studio or use SSMS on factory PC
3. Run schema discovery queries:

```python
import pyodbc
import pandas as pd

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=si-sql;'
    'DATABASE=production;'  # confirm actual DB name with IT
    'Trusted_Connection=yes;'
)

# List all tables and row counts
tables = pd.read_sql("""
    SELECT s.name AS schema_name, t.name AS table_name, p.rows
    FROM sys.tables t
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
    ORDER BY p.rows DESC
""", conn)
print(tables.to_string())

# Find batch-related columns
batch_cols = pd.read_sql("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE column_name LIKE '%batch%'
       OR column_name LIKE '%use_by%'
       OR column_name LIKE '%expir%'
       OR column_name LIKE '%yield%'
       OR column_name LIKE '%weight%'
    ORDER BY table_name
""", conn)
print(batch_cols.to_string())
```

4. Document every table, its purpose, and key relationships
5. Find which tables SSRS reports query (ask IT for .rdl files or check sys.dm_exec_query_stats)

**Deliverable:** Schema documentation in Markdown or Excel

**Success criteria:** Can answer "which table holds batch use-by dates?" and "which table holds current stock levels?"

---

### Week 2: Understand the Pain Points

**Goal:** Know which queries are slow and why.

**Tasks:**
1. Identify 5 slowest queries:

```python
# Find slowest queries on SQL Server
slow = pd.read_sql("""
    SELECT TOP 10
        qs.total_elapsed_time / qs.execution_count / 1000 AS avg_ms,
        qs.execution_count,
        SUBSTRING(qt.text, 1, 200) AS query_text
    FROM sys.dm_exec_query_stats qs
    CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
    ORDER BY avg_ms DESC
""", conn)
print(slow.to_string())
```

2. Time each SSRS report — how long does Yield By Run Number take?
3. Check which tables have indexes:

```python
indexes = pd.read_sql("""
    SELECT t.name AS table_name, i.name AS index_name,
           STRING_AGG(c.name, ', ') AS columns
    FROM sys.indexes i
    JOIN sys.tables t ON i.object_id = t.object_id
    JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
    JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
    WHERE i.type > 0
    GROUP BY t.name, i.name
    ORDER BY t.name
""", conn)
print(indexes.to_string())
```

4. Document: which queries are slow, why (missing indexes, full table scans, bad joins)
5. Suggest index additions to IT

**Deliverable:** Performance report with specific recommendations

**Success criteria:** Can say "Yield report takes 45 seconds because the ProductionRuns table has no index on run_date. Adding one would cut it to 2 seconds."

---

### Week 3: Build First Python Scripts

**Goal:** Replicate one SSRS report in Python, faster.

**Tasks:**
1. Pick the Yield By Run Number report (you already understand it)
2. Write the Python version:

```python
import pandas as pd
import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=si-sql;DATABASE=production;Trusted_Connection=yes;'
)

def get_yield_by_run(run_number):
    """Replicate SSRS Yield By Run Number V3"""
    query = """
        SELECT
            trans_type,
            product_code,
            description,
            si_batch,
            trans_date,
            weight_kg,
            units,
            supplier,
            trace_id,
            batch_code
        FROM vw_YieldByRun  -- or whatever view SSRS uses
        WHERE run_number = ?
        ORDER BY trans_type, trans_date
    """
    df = pd.read_sql(query, conn, params=[run_number])

    input_kg = df[df['trans_type'] == 'Input']['weight_kg'].sum()
    output_kg = df[df['trans_type'] == 'Output']['weight_kg'].sum()
    yield_pct = (output_kg / input_kg * 100) if input_kg > 0 else 0
    giveaway_kg = input_kg - output_kg

    print(f"Run: {run_number}")
    print(f"Input:    {input_kg:,.2f} kg")
    print(f"Output:   {output_kg:,.2f} kg")
    print(f"Yield:    {yield_pct:.1f}%")
    print(f"Giveaway: {giveaway_kg:,.2f} kg ({100-yield_pct:.1f}%)")

    return df, yield_pct

# Test with a known run
df, yield_pct = get_yield_by_run(353086)
```

3. Compare output with SSRS — do numbers match exactly?
4. If they match, the Python version runs in seconds vs SSRS minutes
5. Show IT guy: "same result, 10x faster, and I can automate it"

**Deliverable:** Working Python script that matches SSRS output

**Success criteria:** IT guy says "that's useful, what else can you do?"

---

### Week 4: Despatch Priority Prototype

**Goal:** Build the dashboard that solves the use-by date problem.

**Tasks:**
1. Write the despatch priority query:

```python
def despatch_priority():
    """
    Show all stock sorted by days until expiry.
    Colour: RED <3 days, AMBER 3-7, GREEN 7+
    """
    query = """
        SELECT
            b.batch_code,
            p.product_name,
            p.species,
            s.location_name,
            b.use_by_date,
            DATEDIFF(day, GETDATE(), b.use_by_date) AS days_to_expiry,
            SUM(sm.quantity_kg) AS stock_kg,
            SUM(sm.quantity_units) AS stock_units
        FROM BatchCodes b
        JOIN Products p ON b.product_id = p.product_id
        JOIN StockMovement sm ON b.batch_id = sm.batch_id
        JOIN StockLocations s ON sm.location_code = s.location_code
        WHERE sm.quantity_kg > 0
        GROUP BY b.batch_code, p.product_name, p.species,
                 s.location_name, b.use_by_date
        ORDER BY days_to_expiry ASC
    """
    df = pd.read_sql(query, conn)

    # Add urgency flag
    df['urgency'] = df['days_to_expiry'].apply(
        lambda d: 'RED' if d <= 3 else 'AMBER' if d <= 7 else 'GREEN'
    )

    return df
```

2. Build interactive dashboard:

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Despatch Priority", layout="wide")
st.title("Despatch Priority — FEFO Dashboard")

df = despatch_priority()

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("RED (<3 days)", len(df[df['urgency']=='RED']))
col2.metric("AMBER (3-7 days)", len(df[df['urgency']=='AMBER']))
col3.metric("GREEN (7+ days)", len(df[df['urgency']=='GREEN']))
col4.metric("Total Batches", len(df))

# Filters
species = st.selectbox("Species", ["All"] + list(df['species'].unique()))
location = st.selectbox("Location", ["All"] + list(df['location_name'].unique()))

filtered = df.copy()
if species != "All":
    filtered = filtered[filtered['species'] == species]
if location != "All":
    filtered = filtered[filtered['location_name'] == location]

# Colour-coded table
def color_urgency(val):
    if val == 'RED': return 'background-color: #ff4444; color: white'
    if val == 'AMBER': return 'background-color: #ffaa00'
    return 'background-color: #44bb44; color: white'

st.dataframe(
    filtered.style.applymap(color_urgency, subset=['urgency']),
    use_container_width=True
)

# Chart
fig = px.bar(filtered.groupby('urgency')['stock_kg'].sum().reset_index(),
             x='urgency', y='stock_kg', color='urgency',
             color_discrete_map={'RED':'red','AMBER':'orange','GREEN':'green'})
st.plotly_chart(fig)
```

3. OR build in Power BI if the factory prefers Microsoft tools
4. Validate: pick 5 batches, check against SSRS and physical stock
5. Show to despatch team for feedback

**Deliverable:** Working despatch priority dashboard

**Success criteria:** Despatch team says "I can use this instead of walking the coldstore"

---

## Full Skill Application Timeline

### Month 1: Foundation

| Skill | Application | Tool |
|---|---|---|
| SQL | Schema exploration, query optimisation | SSMS / Azure Data Studio |
| pyodbc/SQLAlchemy | Connect Python to SQL Server | Python |
| pandas | Data extraction and manipulation | Python |
| Git | Version control all queries | Git |

### Month 2: Dashboards

| Skill | Application | Tool |
|---|---|---|
| Streamlit or Power BI | Despatch priority dashboard | Python or Power BI |
| matplotlib/seaborn | Yield trend analysis | Python |
| Plotly | Interactive factory performance view | Python |
| pandas | Automate plan attainment calculation | Python |

### Month 3: Advanced

| Skill | Application | Tool |
|---|---|---|
| scikit-learn | Predict yield from raw material specs | Python |
| XGBoost | Anomaly detection on weight variances | Python |
| scipy.stats | Statistical significance of yield differences | Python |
| Scheduling | Automated daily reports via Windows Task Scheduler | Python + cron |

---

## Specific Python Scripts to Build

### Script 1: Daily Yield Summary (replaces Excel)

```python
"""
Runs at 6am via Task Scheduler.
Pulls yesterday's yield data.
Generates HTML email to production manager.
"""
import pandas as pd
import pyodbc
from datetime import date, timedelta

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=si-sql;DATABASE=production;Trusted_Connection=yes;')

yesterday = date.today() - timedelta(days=1)

yield_data = pd.read_sql(f"""
    SELECT
        production_line,
        department,
        SUM(input_weight_kg) AS input_kg,
        SUM(output_weight_kg) AS output_kg,
        ROUND(SUM(output_weight_kg) * 100.0 / NULLIF(SUM(input_weight_kg), 0), 1) AS yield_pct,
        COUNT(DISTINCT run_number) AS total_runs
    FROM ProductionRuns
    WHERE CAST(run_date AS DATE) = '{yesterday}'
    GROUP BY production_line, department
    ORDER BY department, production_line
""", conn)

total_input = yield_data['input_kg'].sum()
total_output = yield_data['output_kg'].sum()
overall_yield = round(total_output / total_input * 100, 1) if total_input > 0 else 0

print(f"=== Daily Yield Report: {yesterday} ===")
print(f"Overall yield: {overall_yield}%")
print(f"Total input: {total_input:,.1f} kg")
print(f"Total output: {total_output:,.1f} kg")
print(f"Giveaway: {total_input - total_output:,.1f} kg")
print()
print(yield_data.to_string(index=False))

# Save to Excel for backup
yield_data.to_excel(f'daily_yield_{yesterday}.xlsx', index=False)
```

### Script 2: Stock Expiry Alert

```python
"""
Runs at 7am daily.
Finds batches expiring within 3 days.
Sends alert to despatch.
"""
import pandas as pd
import pyodbc
import smtplib
from email.mime.text import MIMEText

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=si-sql;DATABASE=production;Trusted_Connection=yes;')

expiring = pd.read_sql("""
    SELECT batch_code, product_name, use_by_date,
           DATEDIFF(day, GETDATE(), use_by_date) AS days_left,
           location_name, stock_kg
    FROM vw_CurrentStock
    WHERE DATEDIFF(day, GETDATE(), use_by_date) <= 3
      AND stock_kg > 0
    ORDER BY use_by_date ASC
""", conn)

if len(expiring) > 0:
    print(f"WARNING: {len(expiring)} batches expiring within 3 days")
    print(expiring.to_string(index=False))
else:
    print("No batches expiring within 3 days")
```

### Script 3: RSPCA Misallocation Check

```python
"""
Runs weekly.
Identifies cases where RSPCA material was used on non-RSPCA orders.
"""
import pandas as pd
import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=si-sql;DATABASE=production;Trusted_Connection=yes;')

misalloc = pd.read_sql("""
    SELECT
        r.run_number,
        r.run_date,
        r.batch_code,
        m.certification AS raw_material_cert,
        p.certification_required AS product_cert,
        r.input_weight_kg,
        CASE
            WHEN m.certification = 'RSPCA' AND p.certification_required != 'RSPCA'
            THEN 'MISALLOCATED'
            ELSE 'OK'
        END AS status
    FROM ProductionRuns r
    JOIN Materials m ON r.material_id = m.material_id
    JOIN Products p ON r.product_id = p.product_id
    WHERE m.certification = 'RSPCA'
      AND p.certification_required != 'RSPCA'
      AND r.run_date >= DATEADD(month, -1, GETDATE())
    ORDER BY r.run_date DESC
""", conn)

if len(misalloc) > 0:
    total_kg = misalloc['input_weight_kg'].sum()
    print(f"RSPCA Misallocation: {len(misalloc)} incidents, {total_kg:,.1f} kg")
    print(misalloc.to_string(index=False))
else:
    print("No RSPCA misallocations this month")
```

### Script 4: Yield Prediction Model

```python
"""
Train a model to predict yield % based on:
- Species
- Raw material source/supplier
- Day of week
- Production line
- Shift (AM/PM)
"""
import pandas as pd
import pyodbc
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=si-sql;DATABASE=production;Trusted_Connection=yes;')

# Pull 6 months of yield data
df = pd.read_sql("""
    SELECT
        r.species,
        r.supplier,
        DATEPART(dw, r.run_date) AS day_of_week,
        r.production_line,
        r.shift,
        r.input_weight_kg,
        ROUND(r.output_weight_kg * 100.0 / NULLIF(r.input_weight_kg, 0), 2) AS yield_pct
    FROM ProductionRuns r
    WHERE r.run_date >= DATEADD(month, -6, GETDATE())
      AND r.input_weight_kg > 10  -- filter out test runs
""", conn)

# Encode categoricals
df_encoded = pd.get_dummies(df, columns=['species', 'supplier', 'production_line', 'shift'])

X = df_encoded.drop('yield_pct', axis=1)
y = df_encoded['yield_pct']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance:")
print(f"  MAE: {mae:.2f}% (average prediction error)")
print(f"  R2:  {r2:.3f} (explains {r2*100:.1f}% of yield variance)")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False).head(10)

print(f"\nTop factors affecting yield:")
print(importance.to_string(index=False))
```

---

## What NOT to Do

1. **Don't write to the database.** Read only. Always. If you accidentally run an UPDATE or DELETE, you break production.
2. **Don't run heavy queries during production hours (6am-6pm).** Schedule scripts for overnight or early morning.
3. **Don't build dashboards nobody asked for.** Solve the problem they told you about first.
4. **Don't use IT guy's credentials.** Get your own read-only login.
5. **Don't promise timelines you can't keep.** "Two weeks for a prototype" is honest. "I'll fix everything in a month" is not.
6. **Don't bypass IT.** Everything goes through the IT guy. He's your gatekeeper and your ally.
7. **Don't install software on factory PCs without IT approval.** Ask first, always.
8. **Don't show half-finished work to management.** Only show when the numbers are validated.
