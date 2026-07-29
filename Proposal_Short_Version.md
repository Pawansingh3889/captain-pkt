# Data Analytics Support for IT — Proposal

**To:** Factory Manager / IT Manager
**From:** Pawan Singh Kapkoti
**Date:** March 2026

---

## Context

IT is planning to implement Python for database queries and reporting. Currently one person handles all data infrastructure. The factory generates thousands of records daily through SI Integreater, OCM, and SQL Server — batch traceability, yield tracking, stock management, compliance reporting.

The workload is growing. The tools are changing. An extra pair of hands with the right skills would help.

## What I Can Contribute

I have an MSc in Data Analytics (Aston University) and work daily with the exact tools being considered:

| Factory Need | My Skill | Evidence |
|---|---|---|
| SQL Server query optimisation | SQL — window functions, CTEs, indexing, joins | 14 published SQL queries on GitHub |
| Python data scripts | pandas, NumPy, SQLAlchemy, pyodbc | 10 public Python projects |
| Data visualisation | matplotlib, seaborn, Plotly, Power BI (PL-300 certified) | Live Streamlit dashboard deployed |
| Data quality checks | dbt testing framework, automated validation | 94 automated tests in production pipeline |
| ML models for prediction | scikit-learn, XGBoost, Random Forest | Yield prediction model at 93% accuracy |
| Reporting automation | Scheduled scripts, CI/CD, GitHub Actions | 3 automated workflows running daily |

## Proposed Arrangement

### Phase 1: Training and Integration (Week 1-4)

Work alongside IT to understand the database and current pain points.

| Week | Training Goal | Deliverable |
|---|---|---|
| 1 | Get read-only SQL Server access. Map database schema — tables, relationships, key fields for batches, use-by dates, stock, yields | Schema documentation |
| 2 | Identify the 5 slowest SSRS queries. Understand how OCM writes to SQL Server. Study the run-to-batch migration structure | Query performance report |
| 3 | Rewrite 2-3 slow queries in optimised SQL. Build first Python script to replicate one SSRS report | Working Python scripts |
| 4 | Build Despatch Priority view — batch codes with actual use-by dates, days to expiry, stock location. Test with despatch team | Working prototype |

**Milestone check:** Does the prototype match SSRS data? Does despatch find it useful? If yes, continue. If no, stop.

### Phase 2: Production Dashboards (Week 5-8)

Build the tools the factory actually needs.

| Week | Goal | Deliverable |
|---|---|---|
| 5-6 | Despatch FEFO dashboard — actual use-by dates, expiry urgency, stock by area. Eliminates need for QA concessions on date mismatches | Live dashboard connected to SQL Server |
| 7 | Factory performance view — yield by department, plan attainment (automates the Excel report), shelf life distinction (superchilled +11/+12 days vs standard +7 days) for FEFO accuracy | Cross-department dashboard |
| 8 | RSPCA allocation tracker — flags when premium material goes to standard orders. Calculates margin impact | Allocation report |

### Phase 3: Ongoing Value (Month 3+)

| Capability | What It Does |
|---|---|
| Query optimisation | Reduce report load times from minutes to seconds |
| Automated daily reports | Python scripts replace manual Excel compilation |
| Predictive yield modelling | Forecast output from today's intake using ML |
| Stock expiry alerts | Automated email when batches approach use-by date |
| Supplier performance | Yield and quality tracking by raw material source |
| Audit automation | Pull full batch traceability chain in seconds |

## What I Need

| Requirement | Details | Risk |
|---|---|---|
| Read-only SQL Server access | Cannot modify any data | Zero — read only |
| Python already planned by IT | No new software approval needed | Zero — IT is already doing this |
| 1-2 hours per day alongside normal duties | During quieter production periods | Minimal operations impact |
| IT support for initial setup | One-time: access credentials, schema walkthrough | 1-2 hours of IT time |

## What Does NOT Change

- SI Integreater, OCM, SSRS — all continue as-is
- No changes to production systems or workflows
- No additional software cost (Python is free, Power BI included in Teams licence)
- Read-only access — nothing can be broken

## Why This Makes Sense

The IT department is one person handling database, ERP, network, and now Python migration. Adding someone who already knows Python, SQL, and data analysis — and who understands the factory floor from 12 months of operational experience — reduces the burden without adding headcount cost.

The factory generates the data. The systems store the data. What's missing is someone who can turn that data into decisions. That's the gap this fills.

---

## Next Step

A conversation with IT to discuss:
1. Which queries are causing the most pain right now?
2. What's the Python implementation timeline?
3. Where would an extra pair of hands help most?
