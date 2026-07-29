# Copernus Fresh Fish — Data-Driven Operations: Future Goals

**Prepared by:** Pawan Singh Kapkoti, Operational Team Leader
**Date:** March 2026

---

## Current Initiatives (Completed / In Progress)

| Initiative | Status | Impact |
|---|---|---|
| Run-centric to batch-centric migration | In Progress | Each batch independently traceable — audit compliant |
| Despatch FEFO with actual use-by dates | Proposed | Correct shipping priority, fewer QA concessions |
| Python migration support (with IT) | Proposed | Reduce SQL Server query times, replace slow reports |

---

## Short-Term Goals (Next 3 Months)

### 1. Loma Checkweigher Data Capture and Giveaway Tracking

**Current state:** Loma checkweigher captures pack-level data (accepted/rejected counts, mean weight, standard deviation, metal rejects) but this data stays on the machine screen. OCM captures basket-level kg data and feeds into SI. Pack-level detail from Loma is not connected to any reporting system.

**The problem in numbers:** On a recent Salmon Fillet Joint batch, the Loma screen showed mean weight of 514.4g against a 500g target — 14.4g giveaway per pack. Over 1806 accepted packs, that is 26kg of free product in a single batch. At salmon fillet pricing, that is approximately £260-390 lost per batch with no visibility or trending.

**Goal:** Capture Loma end-of-batch statistics into SQL Server so giveaway per run can be tracked and trended over time.

**How:**
- Identify Loma's data export capability (USB, network, serial port)
- Build Python script to capture end-of-batch statistics and write to SQL Server staging table
- Dashboard shows giveaway trend by product, line, and shift
- Alert when mean weight drifts more than 10g above target

**Business impact:**
- First-time visibility on pack-level giveaway — currently invisible
- Rejection rate tracking: 371 rejected out of 2177 total (17%) on the Salmon Fillet Joint batch needs investigation
- Standard deviation tracking (19.16g) indicates cutting consistency — high SD means inconsistent portioning
- Audit trail: every batch statistic linked to product, date, line

**Measurable outcome:** Giveaway trend visible per product/line/shift. Target: reduce mean weight overshoot from 14.4g to under 5g per pack.

---

### 2. Chopper Output Tracking and Supplier Yield Analysis

**Current state:** The chopper cuts whole fish into multiple products:
- **Cod:** Loins (260g, belly, highest value) → Fillets (250g, sides) → Simply (2-10 pieces, tail/trim, lowest value). Primary manager manually switches the cutter weight from 260g to 250g once the loins target is met.
- **Salmon:** 140g → 120g → 110g portions → Simply (leftover). Two types: GG (Global Gap) and RSPCA (premium).

The chopper has a screen (like Loma) but this data is not captured in any database. Output goes into baskets (36 packs per basket, 2.25kg tare), then onto pallets (16 baskets per pallet). OCM weighs baskets and feeds kg to SI.

**Data quality issue discovered:** Basket counting is currently done manually. Some staff calculate 20 baskets x 2.5kg tare = 50kg, but actual is 16 baskets x 2.25kg tare = 36kg. This 14kg error per pallet means yield data calculated from OCM is biased. All downstream analysis built on this data is unreliable until the tare weight input is corrected.

**Goal (Phase 1 — Fix the data):** Verify and correct basket tare weights in OCM. Ensure basket count per pallet is accurate. This must happen before any analysis is trustworthy.

**Goal (Phase 2 — Supplier yield tracking):** Track which supplier's fish produces the best loin-to-fillet-to-simply ratio. Currently all cod goes into one run — there is no visibility on whether supplier A's fish produces more loins (high value) than supplier B's fish.

**How:**
- Phase 1: Audit OCM tare weight settings against actual basket weights. Correct any discrepancies. Document the impact on historical yield data.
- Phase 2: Link supplier batch code at intake through to chopper output by product type. Record: loins count/weight, fillets count/weight, simply count/weight per batch code.
- Phase 3: Analyse — which supplier's fish produces the highest revenue per kg input? (Revenue = loins_kg x loin_price + fillets_kg x fillet_price + simply_kg x simply_price)
- Pilot programme: Run controlled data collection on 2-3 suppliers over 4 weeks using different measurement methods.

**Business impact:**
- Fixing tare weight error immediately corrects yield reporting — management sees real performance for the first time
- Supplier yield data enables procurement negotiations: "Supplier A produces 15% more loins per fish than Supplier B — justify your price"
- Optimal loin-to-fillet switch point identified from data, not guesswork
- RSPCA salmon allocation accuracy: track whether premium GG fish is going to standard orders

**Measurable outcome:** Phase 1: tare weight corrected within 1 week. Phase 2: supplier yield comparison after 4-week pilot.

---

### 3. Seabream New Product: Weight Baseline and Giveaway Analysis

**Current state:** Seabream is a new product line. Target weights and acceptable giveaway percentages are not yet established from production data.

**Goal:** Establish statistical baseline for seabream weights and giveaway from first 4 weeks of production data.

**How:**
- Collect seabream production data from SI: input weight, output weight, giveaway, batch code
- Python analysis:
  - Mean, median, standard deviation of finished product weight
  - Giveaway % distribution — what's normal, what's an outlier
  - Comparison to salmon and cod baselines
- Set control limits: upper and lower acceptable giveaway thresholds
- Flag batches outside control limits automatically

**Business impact:**
- Data-driven pricing: actual yield determines cost per unit, not estimates
- Giveaway targets set from evidence, not assumption
- New product launches in future follow the same data-driven baseline process
- QA has documented acceptable ranges for seabream

**Measurable outcome:** Documented giveaway baseline within 4 weeks of production start. Pricing accuracy improved.

---

### 4. Cod Product Mix Optimisation

**Current state:** Whole cod is cut into loins (highest value, 260g belly), fillets (mid value, 250g sides), and simply (lowest value, 2-10 pieces tail/trim). Primary manager manually switches the chopper weight once the loins target is met. Daily output: approximately 100 baskets loins, 100 baskets fillets, 40 baskets simply (36 packs per basket). No data exists on whether the current switch point maximises revenue.

**Goal:** Find the optimal loin-to-fillet switch point that maximises total revenue per fish using production data.

**How:**
- Record exact switch point for every batch over 4 weeks: loins count/weight, fillets count/weight, simply count/weight
- Calculate revenue per fish at different switch points: (loins_kg x price) + (fillets_kg x price) + (simply_kg x price)
- Link supplier batch code to product output — identify which supplier produces more loins per fish
- Factor in the recent simply spec change (2-6 to 2-10 pieces)

**Business impact:**
- Data-driven switch point vs experience-based guesswork
- Supplier negotiations: "Supplier A produces 15% more loins per fish"
- Revenue increase per fish without changing volume

**Measurable outcome:** Top 3 factors identified. Process recommendation documented. Before/after yield comparison over 8 weeks.

---

## Medium-Term Goals (3-6 Months)

### 5. RSPCA vs Standard Allocation Tracker

**Current state:** RSPCA-certified fish is more expensive. Occasionally allocated to non-RSPCA (generic) production orders. No tracking of how often this happens or the cost impact.

**Goal:** Track every allocation of RSPCA fish to production orders and flag mismatches.

**How:**
- Query SQL Server: raw material intake with certification type (RSPCA, MSC, standard)
- Join to production run allocation
- Flag: RSPCA input → non-RSPCA output order
- Calculate margin impact: (RSPCA price - standard price) × kg misallocated
- Weekly report: total misallocation cost

**Business impact:**
- First-time visibility on allocation accuracy
- Production planners see mismatches before they happen
- Annual margin recovery: even small improvements = significant savings on premium raw material

---

### 6. Despatch Priority Dashboard (FEFO with Actual Use-By Dates)

**Current state:** Despatch uses planned use-by dates from production plan. Actual batch use-by dates differ. QA concessions required when dates don't match.

**Goal:** Dashboard showing every batch in stock with actual use-by date, sorted by expiry urgency.

**How:**
- Query SQL Server: batch codes in stock + actual use-by date + location (coldstore, blast freezer, despatch)
- Calculate days-to-expiry
- Dashboard: colour-coded (red = expires in 3 days, amber = 3-7, green = 7+)
- Filter by species, area, customer allocation
- Auto-refresh hourly

**Business impact:**
- Despatch makes decisions on correct dates
- QA concessions for date mismatches eliminated
- FEFO compliance automated
- Stock waste reduced: oldest stock ships first, nothing expires in coldstore

---

### 7. Supplier Performance Scorecard

**Goal:** Rate each fish supplier on yield, quality, and consistency using production data.

**Metrics per supplier:**
- Average yield %
- Yield variance (consistency)
- Rejection rate
- Delivery reliability
- Price per kg vs yield per kg (true cost)

**Business impact:** Data-driven supplier negotiations. Poor suppliers identified and replaced. Procurement team has evidence, not opinions.

---

## Long-Term Goals (6-12 Months)

### 8. Predictive Yield Model

**Goal:** Forecast tomorrow's yield based on today's inputs using machine learning.

**Inputs:** Supplier, species, fish size, temperature, shift, operator, day of week, season
**Output:** Predicted yield % with confidence interval

**Method:** Train XGBoost or Random Forest on 6+ months of historical yield data. Deploy as internal tool.

**Business impact:** Production planning uses predicted yield to set accurate targets. Over/under-estimation of output reduced.

---

### 9. Factory Floor Live Dashboard (TV Screens)

**Goal:** Power BI or Streamlit dashboards on large screens across the factory floor.

**Dashboard per area:**
- Primary: chopper performance, yield by line, giveaway alerts
- Retail: pack count vs plan, attainment %, downtime
- Despatch: FEFO priority, stock levels, use-by date alerts
- Management: cross-department overview, daily/weekly trends

**How:** Power BI Service (if licence available) or Streamlit deployed on local server. Auto-refresh every 15 minutes. Display on existing TV hardware.

---

### 10. Automated Compliance Reporting

**Goal:** One-click audit reports for Lidl, Iceland, Tesco, RSPCA, MSC.

**Current state:** Audit preparation takes hours of pulling SSRS reports and compiling data.

**Goal:** Pre-built report templates that pull live data from SQL Server. Auditor asks a question → report generated in seconds.

---

## Skills I Bring to These Goals

| Skill | Evidence |
|---|---|
| Python (pandas, numpy, matplotlib, seaborn, scikit-learn) | MSc Data Analytics, 10 GitHub projects |
| SQL (window functions, CTEs, aggregations, joins) | SQL crime analytics project — 14 production queries |
| Power BI (DAX, Power Query, dashboards) | Microsoft PL-300 certified — March 2026 |
| Machine Learning (Random Forest, XGBoost, Isolation Forest) | Apex Data Migration project — 93% accuracy model |
| dbt (transformations, testing, documentation) | UK Crime Pipeline — 53 automated tests |
| SI Integreater | 12 months daily operational use at Copernus |
| Production knowledge | Primary, retail, despatch workflows. MSC/RSPCA chain of custody |
| CI/CD and automation | GitHub Actions — 3 automated workflows |

---

## What This Needs

| Requirement | Who | Time |
|---|---|---|
| Read-only SQL Server access | IT approval | One-time setup |
| Python already planned by IT | IT lead | Collaboration |
| Power BI Desktop (free download) | IT install or self-install | 10 minutes |
| 1-2 hours per day for analysis | Manager approval | During quieter periods |
| Feedback from department leads | Despatch, primary, retail leads | 15 min/week |

---

## Summary

These 10 goals transform Copernus from a factory that **records data** into a factory that **uses data to make decisions.** The infrastructure (SQL Server, SI, SSRS) already exists. The data already exists. What's missing is the analytics layer that turns raw numbers into actionable insight.

Every goal is designed to:
1. Use existing systems — no new software purchases
2. Start small — prove value in 2 weeks before scaling
3. Deliver measurable outcomes — not reports, but reduced waste, fewer concessions, better yield
4. Be maintained by anyone with basic SQL/Python skills — not dependent on one person
