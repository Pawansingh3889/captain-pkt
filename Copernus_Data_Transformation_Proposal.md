# Copernus Fresh Fish — Data Infrastructure Improvement Proposal

**To:** Factory Manager / HR
**From:** Pawan Singh Kapkoti, Operational Team Leader
**Date:** March 2026

---

## Executive Summary

This proposal outlines a plan to improve Copernus Fresh Fish's data infrastructure by connecting existing systems (SI Integreater, SQL Server, OCM, Excel) into a unified reporting layer. The goal is to eliminate manual data gaps that currently cause incorrect despatch decisions, unnecessary QA concessions, and preventable stock waste.

The work uses tools already available in the company (SQL Server, Power BI via Microsoft licence). No new software purchases are required.

If successful, this could transition into a permanent data analyst position supporting factory operations.

---

## The Current State

### What Works Well

| System | Function | Status |
|---|---|---|
| SI Integreater | Production runs, stock tracking, batch management | Working — web and desktop |
| SQL Server | Central database | Working — SSRS reports functional |
| OCM | Live dashboard showing baskets processed, auto-updates kg/units to SI | Working — real-time on factory floor |
| SSRS | Yield by Run Number, batch traceability | Working — accessible via si-sql |
| Excel | Plan attainment tracking, pack counts vs planned | Working — production manager updates manually |

### What Does Not Work

| Gap | Impact | Current Workaround |
|---|---|---|
| **Despatch uses planned use-by dates, not actual batch use-by dates** | Wrong stock shipped first. QA concessions needed when dates don't match. | QA team reviews and approves concessions manually — adds delay and risk |
| **RSPCA vs non-RSPCA allocation not tracked** | Premium raw material used on standard orders = margin loss | No visibility until after production |
| **Superchilled vs standard shelf life not distinguished in despatch** | Superchilled products have +11/+12 day shelf life vs standard +7 days. Despatch cannot see which products have longer shelf life remaining, risking shipping superchilled before standard that expires sooner | No distinction in current stock reports |
| **Run-to-batch migration creates data gaps** | Historical trend analysis breaks between old run-centric and new batch-centric data | No bridge built yet |
| **Excel reports are accurate but disconnected from SQL Server** | Production manager compiles data that already exists in the database | Manual effort that could be automated |
| **No single view across departments** | Primary, retail, despatch, and factory manager all look at different reports | Decisions made in silos |

---

## Why Power BI (Not More Excel)

| Factor | Excel (Current) | Power BI (Proposed) |
|---|---|---|
| Data source | Manual entry or copy-paste from SSRS | Direct connection to SQL Server — always live |
| Refresh | Someone updates the spreadsheet | Scheduled auto-refresh (hourly, daily, or on-demand) |
| Access | One person has the file open — others wait | Web-based — everyone views simultaneously |
| Accuracy | Depends on who entered the data | Pulls directly from the database — no human error |
| Historical trends | Manual — someone has to maintain the sheet | Automatic — Power BI keeps history by design |
| Mobile access | Not practical | Power BI mobile app — factory manager checks from anywhere |
| Cost | Free (already have it) | Free (included in existing Microsoft licence) |
| Integration with SQL Server | Requires ODBC or manual export | Native connector — built for SQL Server |
| SSRS replacement? | No | No — Power BI adds a layer ON TOP. SSRS continues as-is |

**Key point:** Power BI does not replace Excel or SSRS. It sits between the database and the people who need answers. Excel stays for ad-hoc analysis. SSRS stays for batch-level detail reports. Power BI provides the factory-wide operational view that neither currently offers.

---

## Proposed Solution: 3 Dashboards

### Dashboard 1: Despatch Priority (FEFO + Actual Use-By Dates)

**Problem solved:** Despatch currently uses planned use-by dates. Actual batch use-by dates differ. This causes wrong shipment order and QA concessions.

**How it works:**
1. Query SQL Server for all batch codes currently in stock
2. Join batch code to ACTUAL use-by date (from packing data, not plan)
3. Join to stock location (coldstore, blast freezer, despatch staging)
4. Calculate days-to-expiry for every batch
5. Display in Power BI: sorted by expiry urgency, colour-coded (red = <3 days, amber = 3-7, green = 7+)
6. Filter by species, area, customer allocation

**Impact:**
- Despatch sees actual dates, not planned dates
- No more QA concessions for date mismatches
- FEFO compliance automated — oldest stock ships first
- Audit-ready: batch-to-date chain visible in seconds

**Query time improvement:**
- Current: someone walks the coldstore or calls QA → 15-30 minutes
- Proposed: open dashboard on any screen → 5 seconds
- Auto-refreshes every hour from SQL Server

---

### Dashboard 2: Factory Performance (Cross-Department View)

**Problem solved:** Factory manager oversees primary (portioning, bone removal, chopping), retail, and despatch — but each has separate reports. No single view exists.

**How it works:**
1. Connect to SQL Server: pull OCM data (baskets, kg, units) + SI data (runs, batches) + yield data
2. Calculate plan attainment per line (what production manager currently does in Excel — automated)
3. Show yield % by department: primary vs retail
4. Show giveaway trends over time
5. Superchilled vs standard yield tracked separately for first time

**Impact:**
- Production manager's Excel task automated — data pulls from SQL Server directly
- Factory manager sees all departments on one screen
- Superchilled yield visible as standalone metric — tracks the most profitable line
- Plan attainment auto-calculated — no manual pack counting vs planned

---

### Dashboard 3: Raw Material Allocation Tracker

**Problem solved:** RSPCA-certified fish is more expensive. When it gets allocated to non-RSPCA (generic) orders, the company pays premium price but sells at standard price. Currently no visibility on this.

**How it works:**
1. Query SQL Server for raw material intake: species, certification (RSPCA, MSC, standard)
2. Track allocation: which raw material went to which production run/batch
3. Flag mismatches: RSPCA input → non-RSPCA output
4. Calculate margin impact: price difference × kg misallocated

**Impact:**
- First time allocation accuracy is measured
- Production planners can see before allocating — prevents the problem at source
- Monthly report showing total margin lost to misallocation
- Data for negotiating with suppliers on certification premiums

---

## Implementation Plan

### Phase 1: Proof of Concept (Week 1-2)

| Task | Who | Output |
|---|---|---|
| Get read-only SQL Server access | IT / Manager approval | Credentials issued |
| Install Power BI Desktop on one workstation | IT | Software ready |
| Map database schema: identify tables for batches, use-by dates, stock, yields | Pawan | Schema documentation |
| Build Despatch Priority dashboard (Dashboard 1) prototype | Pawan | Working prototype with real data |
| Test with despatch team — does it show the right information? | Pawan + Despatch lead | Feedback collected |

**Decision point:** If the prototype is useful, proceed to Phase 2. If not, stop. No cost incurred.

### Phase 2: Full Build (Week 3-4)

| Task | Who | Output |
|---|---|---|
| Build Factory Performance dashboard (Dashboard 2) | Pawan | Working dashboard |
| Automate plan attainment calculation (replaces manual Excel) | Pawan | Auto-calculated from SQL Server |
| Build RSPCA Allocation Tracker (Dashboard 3) | Pawan | Working dashboard |
| Set up scheduled refresh (Power BI Gateway if available, or manual) | Pawan + IT | Auto-refreshing dashboards |
| User guide + training for team leads | Pawan | 1-page guide per dashboard |

### Phase 3: Monitoring & Handover (Week 5-8)

| Task | Who | Output |
|---|---|---|
| Monitor dashboard accuracy — do numbers match SSRS? | Pawan | Validation report |
| Collect user feedback — what's missing, what's wrong? | Pawan + all users | Improvement list |
| Iterate on dashboards based on feedback | Pawan | Updated dashboards |
| Document all SQL queries and Power BI connections | Pawan | Technical handover document |
| Present results to management: waste reduced, time saved, margin recovered | Pawan | Business impact report |

---

## What I Need

| Requirement | Why | Risk |
|---|---|---|
| Read-only SQL Server access | To query production data — cannot modify anything | Zero risk — read-only |
| Power BI Desktop on one PC | Free Microsoft download | Zero cost |
| 1-2 hours per day during quieter periods | Analysis and dashboard building | Minimal impact on operations |
| Support from IT for database access | One-time setup | 30-minute IT task |
| Feedback from despatch, production manager, factory manager | To build dashboards that people actually use | Requires their time (15 min/week) |

---

## What This Does NOT Change

- SI Integreater continues as-is — no modifications
- SQL Server continues as-is — read-only access, no changes to data
- SSRS reports continue as-is — Power BI adds on top, does not replace
- OCM continues as-is — Power BI reads the same data OCM writes
- Excel continues for ad-hoc work — Power BI automates the repetitive parts
- Existing workflows unchanged — dashboards add visibility, not process changes

---

## Expected Outcomes (Measurable)

| Outcome | How to Measure | Target |
|---|---|---|
| QA concessions for date mismatches | Count before/after dashboard | 50% reduction |
| Time to identify despatch priority | Stopwatch: manual walk vs dashboard | 15 min → 30 seconds |
| RSPCA misallocation incidents | Count per month | Track for first time, then reduce |
| Plan attainment report time | Time production manager spends on Excel | Automated (saves 30+ min/day) |
| Superchilled yield visibility | Currently zero visibility | Tracked weekly |
| Audit batch traceability time | Time to pull full chain for one batch | Minutes → seconds |

---

## Long-Term Value

If the initial 8-week project succeeds, the logical next steps would be:

1. **Power BI Service deployment** — dashboards on TV screens on the factory floor (live)
2. **Automated alerts** — email when stock is within 2 days of expiry
3. **Supplier performance tracking** — yield by supplier, quality by source
4. **Predictive yield modelling** — forecast tomorrow's output based on today's intake
5. **Integration with planning system** — auto-suggest production schedule based on stock levels and customer orders

These would require a dedicated data analyst role — someone who understands both the factory operations and the data systems. This proposal serves as a proof of capability for that role.

---

## About Me

| Qualification | Detail |
|---|---|
| MSc Data Analytics (2:1) | Aston University, 2024 |
| Microsoft PL-300 | Power BI Data Analyst Associate — Active, verifiable |
| Google Data Analytics Certificate | 8-course professional certificate |
| SI Integreater experience | 12 months daily operational use at Copernus |
| SQL Server experience | Queries, joins, aggregations, window functions |
| Python + Power BI portfolio | 10 public projects on github.com/Pawansingh3889 |
| Production knowledge | Primary, retail, despatch workflows. MSC/RSPCA certification chain of custody |

---

## Risk Assessment

**Overall risk: Low**

| Risk | Likelihood | Mitigation |
|---|---|---|
| Dashboard shows wrong numbers | Medium | Validate against SSRS reports before deploying |
| Staff don't use it | Medium | Build with their input — not in isolation |
| SQL Server performance impacted | Low | Read-only queries during off-peak. Power BI caches data locally |
| IT blocks access | Medium | Propose read-only access as first step. Escalate if needed |
| Project doesn't deliver value | Low | Phase 1 is a 2-week proof of concept. Stop if it doesn't work |

---

## Next Step

A 15-minute conversation to discuss:
1. Is read-only SQL Server access feasible?
2. Which dashboard would be most valuable to build first?
3. Can Power BI Desktop be installed on a factory workstation?

If all three are yes, the proof of concept can start within a week.
