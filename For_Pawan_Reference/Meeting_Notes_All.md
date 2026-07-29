# Meeting Notes — Captain PKT Cheat Sheet

Memorise the key points for each person. Read this before each meeting.

---

## For Megan (HR) — Email + Brief Chat

### Key Points:
1. NOT asking to leave production. NOT asking for a new role right now.
2. Proposing to help IT with Python migration AFTER finishing team leader duties.
3. Aware that timing is sensitive — BRCGS audit is coming in a couple of months.
4. Will not start training until Line 2 has adequate team leader coverage.
5. The data improvements (reducing paperwork) actually support the BRCGS audit preparation.

### What to say:
> "I have a proposal to help IT with some data improvements on the factory floor. I understand the timing needs to work around production — I am not asking to step away from my team leader role. I would like to discuss it with Danny first. Could you help arrange a meeting on Monday?"

### What NOT to say:
- Do not mention visa, sponsorship, or CoS
- Do not mention leaving the company
- Do not attach your CV
- Do not mention wanting a different job title

### Megan already knows:
- She interviewed you for Supply Chain Junior in February
- She said the interviewer commended your professionalism
- She retained your CV
- She has applied for a Certificate of Sponsorship (discuss LATER, not now)

---

## For Danny (Factory Manager) — Monday Meeting (15-20 min)

### Open with (60 seconds):
> "Danny, you remember when we discussed the despatch use-by date problem in my interview. I have been thinking about it since. The data to fix it already exists in SQL Server. I have put together a proposal showing how I can build a dashboard that connects batch codes to actual use-by dates. Despatch would see which stock to ship first without needing QA concessions. It would take about two weeks for a working prototype."

### Key Points to Hit:
1. **The despatch problem is real** — he already acknowledged it
2. **Nobody was hired for the IT vacancy** — the problem is still unsolved
3. **Paul (IT) is already planning Python** — this is not a new initiative, it is support for an existing plan
4. **PL-300 certification** — earned this week, directly relevant
5. **Zero risk** — read-only database access, cannot break anything, stop in 2 weeks if it does not work

### Numbers Danny cares about:
- Loma giveaway: 14.4g per pack over target = 26kg free product per batch = £260-390 lost
- 17% rejection rate on Salmon Fillet Joint batch — needs investigation
- QA concessions for date mismatches — each one costs time and audit risk
- RSPCA fish on GG orders — premium cost, standard revenue

### What Danny will ask and your answers:

**"When would you do this?"**
> "After my team leader duties. I am aware we have 5 team leaders across 4 lines, and 2 lines need 2 leaders each — one for the line and one for paperwork. I would not start any IT training until Line 2 has adequate coverage. Production comes first."

**"What about BRCGS?"**
> "The audit is a couple of months away. The dashboards I am proposing would actually help with audit preparation — batch traceability in seconds instead of hours. But the timing has to work for you and Simon. I am not in a rush."

**"Can Paul not do this himself?"**
> "Paul is one person managing all IT infrastructure. He is already planning the Python migration. I am offering to help him, not replace him. Two people can move faster than one."

**"What do you need from me?"**
> "Just approval to get read-only SQL Server access from Paul, and your feedback on which dashboard would be most useful first. The software is free."

### Show Danny:
1. Proposal_Short_Version.docx (he reads this)
2. Copernus_Future_Goals.docx (flip through to show 10 initiatives — shows long-term thinking)
3. PL-300 certificate on your phone (only if he asks about qualifications)

### What NOT to say to Danny:
- Do not mention visa or sponsorship
- Do not mention wanting to leave production
- Do not criticise current systems or people
- Do not say "the data is wrong" — say "there is an opportunity to add visibility"

---

## For Simon (Production Manager) — Separate Chat

### Context:
Simon oversees all department from primary (portioning, bone removing, chopping), retail, and despatch. He currently does the plan attainment Excel report manually. Your proposal automates this for him.

### Key Points:
1. **You are not leaving his team** — you are adding a skill that helps the team
2. **His Excel report gets automated** — this saves him 30+ minutes daily
3. **Team leader coverage is your priority** — you will not start training until Line 2 is covered
4. **BRCGS preparation** — the dashboards help with audit readiness

### What to say:
> "Simon, I have been looking at how we can use the data we already have in SQL Server more effectively. One thing I noticed is that the plan attainment tracking you do in Excel could be automated — the data is already in OCM and SI. Would it help if I built something that pulls it automatically? I would do this after finishing my team leader duties, not during production time."

### What NOT to say:
- Do not say "your Excel is inefficient"
- Do not imply he is doing it wrong
- Frame it as "making your job easier" not "replacing your work"

---

## For the Director — Personal Conversation

### Key Points:
1. **Company growth requires data infrastructure** — the current setup works but will not scale
2. **This is an investment in the company** — not a personal project
3. **The tools are already paid for** — SQL Server, Microsoft licence (Power BI)
4. **Zero risk approach** — 2-week proof of concept, stop if it does not deliver

### What to say:
> "We have a strong production setup with SI and SQL Server. What we are missing is an analytics layer on top — something that turns the data we already collect into decisions. The despatch team makes shipping decisions on planned use-by dates, but actual batch dates are different. That costs us QA concessions and audit risk. I can build a prototype in two weeks using Power BI, which is already included in our Microsoft licence."

### Show the Director:
1. Proposal_Short_Version.docx (1 page — quick read)
2. Copernus_Future_Goals.docx (shows 10 long-term initiatives — shows vision)
3. The Loma giveaway number: "14.4g per pack over target = 26kg free product per batch"

---

## The Staffing Situation — Note for HR/Danny/Director

### Current State:
- 4 production lines
- 5 team leaders / line leaders
- 2 lines require 2 team leaders each (1 for line control, 1 for paperwork)
- Paperwork is critical for BRCGS A-level certification maintenance
- Production manager (Simon) regularly comes to the line to help
- Good team culture — supervisors help across lines

### The Problem:
- If one team leader is on holiday, remaining lines are stretched
- Simon gets pulled from management duties to cover production
- BRCGS audit is coming — paperwork standards cannot slip

### My Position:
- I will NOT start IT training until Line 2 has a new team leader
- Production duties come first
- IT/data work happens AFTER team leader responsibilities
- Timeline depends on when adequate coverage is in place

### How My Proposal Helps This Problem:
- Reducing paperwork through automated data capture means fewer team leaders needed per line
- Loma checkweigher integration = automated weight records (currently manual)
- Automated plan attainment = less Excel work for Simon
- Digital batch traceability = faster audit preparation
- Long term: 2 team leaders per line could become 1 if paperwork is digitised

### What to Say:
> "I understand we are stretched on team leaders and BRCGS is coming. I am not asking to step away from production. The data improvements I am proposing would actually reduce the paperwork burden — that is one of the reasons we need 2 team leaders on some lines. If we automate the weight recording and traceability, the paperwork load drops. But I will not start until the staffing situation allows it."

---

## Quick Memory Card — Read 5 Minutes Before Each Meeting

```
NUMBERS:
- 14.4g giveaway per pack (Loma data)
- 26kg free product per batch
- £260-390 lost per batch
- 17% rejection rate on Salmon Fillet Joint
- 5 team leaders, 4 lines, 2 lines need 2 leaders
- BRCGS audit: couple of months away
- PL-300 certified: March 18, 2026
- Power BI: free with Microsoft licence
- Proof of concept: 2 weeks

PHRASES TO USE:
- "Read-only access — cannot break anything"
- "The data already exists — it just needs connecting"
- "Two-week proof of concept — stop if it does not work"
- "After my team leader duties — production comes first"
- "This actually reduces paperwork long term"

PHRASES TO AVOID:
- "I want a different role"
- "The current system is bad"
- "I need visa sponsorship"
- "My visa expires soon"
- "I want to leave production"
```
