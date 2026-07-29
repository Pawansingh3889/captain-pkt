# Data Analytics Training Programme — Proposal

**To:** Factory Manager, Copernus Fresh Fish
**From:** Pawan Singh Kapkoti, Operational Team Leader
**Date:** March 2026
**Duration:** 4 weeks (alongside normal duties)

---

## Summary

I'm proposing a 4-week programme to build analytics dashboards using our existing SI Integreater data and SQL Server. No new software purchases needed — Power BI is free with our Microsoft licence, and the data already exists in the system. The goal is to answer questions the current SSRS reports can't.

---

## The Problem

Our current reporting shows **what happened** on each run. It does not show:

- Which batch codes are expiring soonest and need despatch priority
- Whether RSPCA-certified raw material is being used on non-RSPCA orders (margin loss)
- Shelf life distinction in despatch: superchilled (+11/+12 days) vs standard (+7 days) — ensuring standard ships before superchilled when both are in stock
- How the run-to-batch migration affects historical trend analysis

These gaps mean decisions are made manually or too late. Data exists in SQL Server to answer all of them — it just needs extracting and visualising.

---

## What I'll Build

### Week 1: Data Access & Understanding

| Day | Task | Output |
|---|---|---|
| Mon | Get read-only access to SI SQL Server | Access confirmed |
| Tue | Map the database schema — which tables hold runs, batches, products, yields, stock movements | Schema diagram |
| Wed | Identify key tables: production runs, batch codes, use-by dates, stock locations, product allocations | Table list with row counts |
| Thu | Write test queries — pull one day's yield data, one batch's traceability chain | Verified SQL queries |
| Fri | Document data dictionary — what each column means in business terms | Data dictionary document |

**Deliverable:** Database schema map + data dictionary. Manager can review and confirm understanding is correct.

---

### Week 2: FEFO Dashboard (First Expired First Out)

| Day | Task | Output |
|---|---|---|
| Mon | Query batch codes with use-by dates from SQL Server | Raw dataset |
| Tue | Join batch codes to current stock locations (coldstore, blast freezer, despatch) | Combined dataset |
| Wed | Calculate days-to-expiry for every batch currently in stock | Expiry priority list |
| Thu | Build Power BI dashboard: stock by location, sorted by use-by date, colour-coded by urgency | Dashboard v1 |
| Fri | Add filters: by species, by area, by customer allocation. Test with despatch team | Dashboard reviewed |

**Deliverable:** FEFO dashboard showing exactly which batches need shipping first. Despatch can check this instead of walking the coldstore.

**Business value:** Reduces waste from expired stock. Ensures oldest stock ships first.

---

### Week 3: Yield Analytics & RSPCA Allocation Tracker

| Day | Task | Output |
|---|---|---|
| Mon | Query yield data: input weight, output weight, giveaway by batch code | Yield dataset |
| Tue | Distinguish superchilled (+11/+12 day shelf life) vs standard (+7 day) in stock data. Ensure FEFO dashboard prioritises standard over superchilled when both in stock | Shelf life classification |
| Wed | Track RSPCA vs non-RSPCA raw material allocation. Flag mismatches | Allocation mismatch report |
| Thu | Build Power BI page: yield trend by product type, RSPCA allocation accuracy | Dashboard page 2 |
| Fri | Calculate estimated margin loss from RSPCA misallocation over past 3 months | Financial impact number |

**Deliverable:** Yield dashboard broken out by product type + RSPCA allocation tracker.

**Business value:** Shows exactly how much margin is lost when premium fish goes to standard orders. Gives production planners data to allocate correctly.

---

### Week 4: Automation & Handover

| Day | Task | Output |
|---|---|---|
| Mon | Set up Power BI auto-refresh from SQL Server (scheduled daily) | Auto-refreshing dashboard |
| Tue | Build batch traceability lookup — enter a batch code, see full chain from input to despatch | Traceability tool |
| Wed | Write user guide for the dashboards — how to read them, how to filter | 1-page user guide |
| Thu | Present to factory manager and team leads. Collect feedback | Presentation done |
| Fri | Make final adjustments. Document all SQL queries for handover | Handover complete |

**Deliverable:** 3 working dashboards + documentation + handover so anyone can maintain them.

---

## What I Need

| Requirement | Detail |
|---|---|
| Read-only SQL Server access | To query production data. No write access needed |
| Power BI Desktop installed | Free download from Microsoft. May need IT to install |
| 1-2 hours per day during quieter periods | Analysis work during low-production times |
| Feedback from despatch and planning teams | To make dashboards useful for actual users |

---

## What This Does NOT Change

- No changes to SI Integreater
- No changes to the production database
- No changes to SSRS reports
- No changes to existing workflows
- Read-only access only — cannot modify any data

This adds a reporting layer on top of what already exists. If it doesn't work, nothing is affected.

---

## Expected Outcomes

| Outcome | Measure |
|---|---|
| Reduced expired stock waste | Track before/after dashboard implementation |
| Fewer RSPCA misallocations | Count of RSPCA fish used on non-RSPCA orders |
| Faster despatch decisions | Time to identify priority batches: manual walk vs dashboard check |
| Superchilled yield visibility | First time this data is tracked separately |
| Audit readiness | Batch traceability available in seconds, not minutes |

---

## About Me

- MSc Data Analytics (Aston University, 2:1)
- Microsoft Certified: Power BI Data Analyst Associate (PL-300) — Active
- 12 months operating SI Integreater daily
- Built 10 data analytics projects using Python, SQL, Power BI (portfolio: github.com/Pawansingh3889)
- Currently studying for AWS Data Engineer Associate certification

---

## Risk

**Low.** Read-only access means nothing can break. Power BI is a Microsoft product already compatible with SQL Server. If the dashboards aren't useful, we simply stop using them. No downtime, no cost, no disruption to production.

---

*I'm happy to discuss this further or demonstrate a prototype using sample data before accessing the live system.*
