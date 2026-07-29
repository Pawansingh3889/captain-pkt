# Technical Blueprint: Copernus Data Infrastructure Implementation

## For: Pawan Singh Kapkoti — Reference Guide

---

## Phase 0: Discovery (Before You Touch Anything)

### Questions to Ask IT Team

**Database:**
1. What is the SQL Server version? (2016/2019/2022?)
2. What is the server name? (si-sql — confirm full hostname)
3. What authentication does it use? Windows Auth or SQL Auth?
4. Can I get a read-only login? What approval process?
5. Is there a test/staging database or only production?
6. What is the backup schedule?

**Schema:**
7. How many databases are on the server? (Just SI or others?)
8. Is there a schema diagram or data dictionary?
9. Which tables hold batch codes?
10. Which tables hold use-by dates?
11. Which tables hold stock locations (coldstore, blast freezer, etc)?
12. Which tables hold yield/weight data?
13. Which tables hold product specifications (RSPCA, MSC, standard)?
14. Are there views already created for SSRS reports?

**SSRS:**
15. Can I see the SQL queries behind the SSRS reports? (Yield By Run Number V3)
16. Where are SSRS report definitions stored? (.rdl files)
17. Are there stored procedures or just inline SQL?

**OCM:**
18. Does OCM write directly to SQL Server or to a middleware?
19. Which tables does OCM update? (baskets, kg, units)
20. How frequently does OCM write? (Real-time per basket? Batch?)

**SI Integreater:**
21. Does SI have an API or only the web interface?
22. Which tables does SI write to for run management?
23. How is the run-to-batch migration structured in the database?

**Infrastructure:**
24. Is Power BI Desktop allowed on factory workstations?
25. Is there a Power BI Service licence (Pro/Premium)?
26. Is there a Power BI Gateway installed? (Needed for auto-refresh)
27. What Windows version are the factory PCs running?

### Questions to Ask Production Manager

28. Which Excel report takes the longest to compile?
29. What columns/metrics do you track for plan attainment?
30. How do you currently calculate yield? (Which SSRS report?)
31. What would save you the most time if automated?

### Questions to Ask Despatch Team

32. How do you currently decide which stock to ship first?
33. When the planned use-by date differs from actual — how often?
34. How many QA concessions per week on average?
35. What information would you need on a screen to make faster decisions?

### Questions to Ask QA Team

36. How do you track concessions? (Log, spreadsheet, system?)
37. What triggers a concession request?
38. How long does a concession approval take?

---

## Phase 1: Database Exploration

### Step 1.1: Connect to SQL Server

**Tool:** SQL Server Management Studio (SSMS) or Azure Data Studio

```
Server: si-sql (or full hostname from IT)
Authentication: Windows or SQL Auth (from IT)
Database: (whatever IT gives you access to)
```

If SSMS is not installed, download Azure Data Studio (free, lighter):
https://learn.microsoft.com/en-us/azure-data-studio/

### Step 1.2: Map the Database Schema

Run these queries first day:

```sql
-- 1. List all databases
SELECT name FROM sys.databases WHERE database_id > 4;

-- 2. List all tables in the production database
SELECT
    s.name AS schema_name,
    t.name AS table_name,
    p.rows AS row_count
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
JOIN sys.partitions p ON t.object_id = p.object_id AND p.index_id IN (0,1)
ORDER BY p.rows DESC;

-- 3. Find tables related to batches
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%batch%' OR column_name LIKE '%lot%'
ORDER BY table_name;

-- 4. Find tables related to use-by dates
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%use%by%'
   OR column_name LIKE '%expir%'
   OR column_name LIKE '%best%before%'
   OR column_name LIKE '%shelf%life%'
ORDER BY table_name;

-- 5. Find tables related to stock/inventory
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%stock%'
   OR column_name LIKE '%location%'
   OR column_name LIKE '%coldstore%'
   OR column_name LIKE '%area%'
ORDER BY table_name;

-- 6. Find tables related to yield/weight
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%yield%'
   OR column_name LIKE '%weight%'
   OR column_name LIKE '%input%'
   OR column_name LIKE '%output%'
ORDER BY table_name;

-- 7. Find tables related to species/certification
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%species%'
   OR column_name LIKE '%rspca%'
   OR column_name LIKE '%msc%'
   OR column_name LIKE '%cert%'
ORDER BY table_name;

-- 8. Find tables related to runs/production
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%run%'
   OR column_name LIKE '%production%'
   OR column_name LIKE '%line%'
ORDER BY table_name;

-- 9. List all views (SSRS probably uses these)
SELECT name FROM sys.views ORDER BY name;

-- 10. List all stored procedures
SELECT name FROM sys.procedures ORDER BY name;
```

### Step 1.3: Reverse-Engineer SSRS Queries

The fastest way to understand the database is to look at existing SSRS reports:

```sql
-- Find SSRS report definitions (if stored in ReportServer DB)
SELECT c.Name, c.Path, c.Type
FROM ReportServer.dbo.Catalog c
WHERE c.Type = 2  -- Type 2 = reports
ORDER BY c.Name;
```

Or ask IT for the `.rdl` files — they contain the SQL queries. Open in Notepad and search for `<CommandText>`.

### Step 1.4: Document Findings

Create a schema map:

```
Table: [BatchCodes] (or whatever you find)
  - batch_id (PK)
  - batch_code (varchar)
  - product_id (FK)
  - use_by_date (date)         ← THIS IS THE KEY FIELD
  - created_date (datetime)

Table: [StockMovement]
  - movement_id (PK)
  - batch_id (FK)
  - location_code (varchar)    ← coldstore, blast freezer, etc
  - quantity_kg (decimal)
  - movement_date (datetime)

Table: [ProductionRuns]
  - run_number (PK)
  - batch_id (FK)
  - input_weight_kg (decimal)
  - output_weight_kg (decimal)
  - species (varchar)
  - certification (varchar)    ← RSPCA, MSC, standard
  - run_date (datetime)
```

*(These are example names — actual names will differ. That's what discovery finds.)*

---

## Phase 2: Dashboard 1 — Despatch Priority (FEFO)

### Priority: HIGHEST (This is the proof of concept)

### Step 2.1: Write the Core Query

```sql
-- Despatch Priority Query
-- Shows all stock sorted by days until expiry
SELECT
    b.batch_code,
    p.product_name,
    p.species,
    s.location_name,
    b.use_by_date,
    DATEDIFF(day, GETDATE(), b.use_by_date) AS days_to_expiry,
    CASE
        WHEN DATEDIFF(day, GETDATE(), b.use_by_date) <= 3 THEN 'RED - Ship Immediately'
        WHEN DATEDIFF(day, GETDATE(), b.use_by_date) <= 7 THEN 'AMBER - Ship Soon'
        ELSE 'GREEN - OK'
    END AS urgency,
    SUM(sm.quantity_kg) AS stock_kg,
    SUM(sm.quantity_units) AS stock_units,
    a.customer_name AS allocated_to
FROM BatchCodes b
JOIN Products p ON b.product_id = p.product_id
JOIN StockMovement sm ON b.batch_id = sm.batch_id
JOIN StockLocations s ON sm.location_code = s.location_code
LEFT JOIN Allocations a ON b.batch_id = a.batch_id
WHERE sm.quantity_kg > 0  -- Only in-stock items
GROUP BY b.batch_code, p.product_name, p.species,
         s.location_name, b.use_by_date, a.customer_name
ORDER BY days_to_expiry ASC;
```

*(Table/column names will change based on discovery. The LOGIC stays the same.)*

### Step 2.2: Build in Power BI

1. Open Power BI Desktop
2. Get Data → SQL Server
3. Server: `si-sql`
4. Database: (from discovery)
5. Advanced: paste the SQL query above
6. Load

### Step 2.3: Design the Dashboard

**Page 1: Despatch Priority Overview**

```
┌──────────────────────────────────────────────────┐
│  DESPATCH PRIORITY DASHBOARD          [Refresh]  │
│                                                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │
│  │ RED: 5 │ │AMBER:12│ │GREEN:48│ │Total: 65 │  │
│  │ <3 days│ │ 3-7 day│ │ 7+ day │ │ batches  │  │
│  └────────┘ └────────┘ └────────┘ └──────────┘  │
│                                                  │
│  Filter: [Species ▼] [Area ▼] [Customer ▼]      │
│                                                  │
│  ┌──────────────────────────────────────────────┐│
│  │ Batch    Product    Use-By   Days  Area  Kg  ││
│  │ ─────    ───────    ──────   ────  ────  ─── ││
│  │ BC001    Salmon120  21/03    2  🔴 GX   450 ││
│  │ BC002    Haddock    22/03    3  🔴 CO   230 ││
│  │ BC003    SalmonFil  24/03    5  🟡 BL   890 ││
│  │ BC004    CodFillet  27/03    8  🟢 FG   340 ││
│  └──────────────────────────────────────────────┘│
│                                                  │
│  Last refreshed: 19/03/2026 14:00                │
└──────────────────────────────────────────────────┘
```

**Power BI visuals to use:**
- Card visuals for RED/AMBER/GREEN counts
- Table visual for the batch list (conditional formatting on urgency)
- Slicer visuals for Species, Area, Customer filters
- Bar chart: stock kg by expiry urgency

### Step 2.4: Validate

Before showing anyone:
1. Pick 5 batch codes from the dashboard
2. Check each one manually in SSRS (Yield By Run Number)
3. Do the use-by dates match?
4. Do the stock quantities match?
5. If all 5 match → prototype is ready to show

---

## Phase 3: Dashboard 2 — Factory Performance

### Priority: HIGH

### Step 3.1: Core Queries

```sql
-- Plan Attainment per Line
SELECT
    r.production_date,
    r.production_line,
    SUM(r.planned_packs) AS planned,
    SUM(r.actual_packs) AS actual,
    ROUND(SUM(r.actual_packs) * 100.0 / NULLIF(SUM(r.planned_packs), 0), 1)
        AS attainment_pct
FROM ProductionRuns r
WHERE r.production_date >= DATEADD(day, -30, GETDATE())
GROUP BY r.production_date, r.production_line
ORDER BY r.production_date DESC, r.production_line;
```

```sql
-- Yield by Department
SELECT
    r.department,  -- Primary, Retail
    r.production_date,
    SUM(r.input_weight_kg) AS input_kg,
    SUM(r.output_weight_kg) AS output_kg,
    ROUND(SUM(r.output_weight_kg) * 100.0 /
          NULLIF(SUM(r.input_weight_kg), 0), 1) AS yield_pct,
    SUM(r.input_weight_kg) - SUM(r.output_weight_kg) AS giveaway_kg
FROM ProductionRuns r
WHERE r.production_date >= DATEADD(day, -30, GETDATE())
GROUP BY r.department, r.production_date
ORDER BY r.production_date DESC;
```

```sql
-- Shelf Life Classification for FEFO
-- Superchilled products have +11/+12 day shelf life vs standard +7 days
-- This query helps despatch prioritise standard products over superchilled
-- when both are in stock, because standard expires sooner
SELECT
    b.batch_code,
    p.product_name,
    CASE WHEN p.shelf_life_days >= 11 THEN 'Superchilled'
         ELSE 'Standard' END AS shelf_life_type,
    b.use_by_date,
    DATEDIFF(day, GETDATE(), b.use_by_date) AS days_remaining,
    s.area_name AS stock_location
FROM Batches b
JOIN Products p ON b.product_id = p.product_id
JOIN StockLocations s ON b.location_id = s.location_id
WHERE b.use_by_date >= GETDATE()
ORDER BY days_remaining ASC;
-- Standard (+7 day) products will appear first = ship these first
```

### Step 3.2: Dashboard Layout

```
┌──────────────────────────────────────────────────┐
│  FACTORY PERFORMANCE                  [Date ▼]   │
│                                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │Yield    │ │Plan     │ │Giveaway │            │
│  │88.2%    │ │95.3%    │ │1,240 kg │            │
│  │(today)  │ │attain.  │ │(today)  │            │
│  └─────────┘ └─────────┘ └─────────┘            │
│                                                  │
│  ┌────────────────────┐ ┌────────────────────┐   │
│  │ Yield % Trend      │ │ Plan Attainment    │   │
│  │ (line chart 30d)   │ │ by Line (bar)      │   │
│  │ Primary vs Retail  │ │                    │   │
│  └────────────────────┘ └────────────────────┘   │
│                                                  │
│  ┌────────────────────┐ ┌────────────────────┐   │
│  │ Superchilled vs    │ │ Giveaway Trend     │   │
│  │ Standard Yield     │ │ (area chart)       │   │
│  │ (comparison)       │ │                    │   │
│  └────────────────────┘ └────────────────────┘   │
└──────────────────────────────────────────────────┘
```

---

## Phase 4: Dashboard 3 — RSPCA Allocation Tracker

### Priority: MEDIUM

### Step 4.1: Core Query

```sql
-- RSPCA Misallocation Detection
SELECT
    r.run_number,
    r.run_date,
    r.batch_code,
    input_mat.certification AS input_certification,
    output_prod.certification_required AS output_certification,
    CASE
        WHEN input_mat.certification = 'RSPCA'
         AND output_prod.certification_required != 'RSPCA'
        THEN 'MISALLOCATED'
        ELSE 'OK'
    END AS allocation_status,
    r.input_weight_kg,
    (input_mat.price_per_kg - standard_mat.price_per_kg) * r.input_weight_kg
        AS margin_lost
FROM ProductionRuns r
JOIN Materials input_mat ON r.material_id = input_mat.material_id
JOIN Products output_prod ON r.product_id = output_prod.product_id
LEFT JOIN Materials standard_mat ON standard_mat.species = input_mat.species
    AND standard_mat.certification = 'Standard'
WHERE input_mat.certification = 'RSPCA'
  AND output_prod.certification_required != 'RSPCA'
  AND r.run_date >= DATEADD(month, -3, GETDATE())
ORDER BY r.run_date DESC;
```

---

## Tools and Tech Stack

### What You Need Installed

| Tool | Purpose | Where to Get | Cost |
|---|---|---|---|
| Power BI Desktop | Build dashboards | microsoft.com/power-bi | Free |
| Azure Data Studio | Query SQL Server | microsoft.com | Free |
| SSMS (optional) | Full SQL Server management | microsoft.com | Free |
| Python 3.11+ | Automation scripts if needed | Already installed | Free |
| Git | Version control for queries | Already installed | Free |

### Power BI Connection Setup

```
Data Source: SQL Server
Server: si-sql
Database: [from discovery]
Data Connectivity: DirectQuery (for live data) or Import (for cached)

Recommendation: Start with Import mode (faster dashboard)
Switch to DirectQuery later if real-time is needed
```

### Refresh Strategy

| Option | How | Frequency | Requires |
|---|---|---|---|
| Manual refresh | Click refresh button in Power BI | On-demand | Nothing |
| Scheduled via Gateway | Power BI Gateway installed on server | Hourly/daily | IT installs Gateway |
| Python script | Script runs query, exports to Power BI | Scheduled via Task Scheduler | Python + pyodbc |

**Start with manual refresh.** Automate later once dashboards are validated.

### Python Backup (If Power BI Isn't Approved)

If IT blocks Power BI, use Python + Streamlit instead:

```python
import pyodbc
import pandas as pd
import streamlit as st

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=si-sql;'
    'DATABASE=production;'
    'Trusted_Connection=yes;'
)

df = pd.read_sql("""
    SELECT batch_code, use_by_date,
           DATEDIFF(day, GETDATE(), use_by_date) as days_to_expiry
    FROM BatchCodes
    WHERE use_by_date >= GETDATE()
    ORDER BY use_by_date
""", conn)

st.title("Despatch Priority")
st.dataframe(df.style.applymap(
    lambda v: 'background-color: red' if v <= 3
    else 'background-color: orange' if v <= 7
    else 'background-color: green',
    subset=['days_to_expiry']
))
```

---

## Priority Order (What to Do First)

```
Week 1:
├── Day 1-2: Ask all discovery questions. Get SQL Server access.
├── Day 3: Run schema exploration queries. Document tables.
├── Day 4: Find the SSRS query behind Yield By Run Number V3
└── Day 5: Write Despatch Priority query. Test in SSMS.

Week 2:
├── Day 6-7: Build Dashboard 1 in Power BI
├── Day 8: Validate 5 batch codes against SSRS
├── Day 9: Show despatch team. Get feedback.
└── Day 10: Present prototype to manager. Get Phase 2 approval.

Week 3-4:
├── Build Dashboard 2 (Factory Performance)
├── Build Dashboard 3 (RSPCA Allocation)
└── Set up refresh schedule

Week 5-8:
├── Monitor accuracy
├── Iterate based on feedback
├── Document everything
└── Present business impact
```

---

## Common SQL Server Patterns You'll Need

### Running Total
```sql
SELECT batch_code, quantity_kg,
    SUM(quantity_kg) OVER (ORDER BY movement_date) AS running_total
FROM StockMovement;
```

### Year-over-Year Comparison
```sql
SELECT
    MONTH(run_date) AS month,
    YEAR(run_date) AS year,
    AVG(yield_pct) AS avg_yield,
    LAG(AVG(yield_pct)) OVER (ORDER BY YEAR(run_date), MONTH(run_date)) AS prev_month
FROM MonthlyYield
GROUP BY YEAR(run_date), MONTH(run_date);
```

### Pivot for Cross-Department View
```sql
SELECT production_date,
    [Primary] AS primary_yield,
    [Retail] AS retail_yield
FROM (
    SELECT production_date, department, yield_pct
    FROM DepartmentYield
) src
PIVOT (AVG(yield_pct) FOR department IN ([Primary], [Retail])) pvt;
```

### FEFO Priority Ranking
```sql
SELECT *,
    ROW_NUMBER() OVER (
        PARTITION BY species, location
        ORDER BY use_by_date ASC
    ) AS despatch_priority
FROM CurrentStock
WHERE quantity_kg > 0;
```

---

## Files to Maintain

```
C:\Projects\copernus-analytics\
├── queries\
│   ├── 01_schema_exploration.sql
│   ├── 02_despatch_priority.sql
│   ├── 03_factory_performance.sql
│   ├── 04_rspca_allocation.sql
│   └── 05_yield_analysis.sql
├── dashboards\
│   ├── Despatch_Priority.pbix
│   ├── Factory_Performance.pbix
│   └── RSPCA_Allocation.pbix
├── documentation\
│   ├── schema_map.md
│   ├── data_dictionary.md
│   └── user_guide.md
├── validation\
│   ├── batch_check_log.xlsx
│   └── accuracy_report.md
└── README.md
```

---

## Red Flags to Watch For

1. **If use-by dates are not in the database** — they might be calculated from production date + shelf life. Ask QA how shelf life is determined.
2. **If stock location is not tracked per batch** — SI might only track by product, not by physical location. The dashboard would need a different approach.
3. **If RSPCA/MSC certification is not a field** — it might be embedded in the product code (e.g., prefix "RSPCA-"). Parse it out.
4. **If the database has no indexes on date columns** — your queries will be slow. Ask IT to add indexes.
5. **If there are multiple databases** — SI might use one DB, OCM another. You'll need cross-database joins.

---

## Success Criteria

The project succeeds if:

1. Despatch can check actual use-by dates in under 30 seconds
2. QA concessions for date mismatches drop by 50%
3. Production manager stops manually updating the Excel attainment sheet
4. Factory manager has one screen showing all departments
5. RSPCA misallocation is tracked for the first time
6. Management sees enough value to discuss a permanent data analyst role
