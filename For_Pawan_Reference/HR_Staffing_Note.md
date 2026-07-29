# Staffing Context — Internal Note

## Current Team Leader Structure

| Line | Team Leaders | Roles |
|---|---|---|
| Line 1 | 1 | Line control |
| Line 2 | 2 | 1 line control + 1 paperwork |
| Line 3 | 1 | Line control |
| Line 4 | 2 (when required) | 1 line control + 1 paperwork |
| **Total** | **5** | |

## Why 2 Team Leaders on Some Lines

- BRCGS A-level certification requires detailed paperwork at every stage
- One team leader manages the production line (operators, output, quality)
- Second team leader maintains paperwork (batch records, traceability, compliance documentation)
- Both roles are essential — dropping either risks audit failure

## Current Pressures

- Production manager Simon regularly steps onto the line to help when short-staffed
- If one team leader takes holiday, remaining team leaders cover multiple responsibilities
- BRCGS audit approximately 2 months away — standards cannot slip
- Company culture is collaborative — supervisors help across lines — but goodwill cannot replace staffing

## My Commitment

- Team leader duties on Line 2 are my first priority
- IT/data training will only begin once Line 2 has adequate team leader coverage
- If a new team leader is hired for Line 2, that frees capacity for data work
- Until then, any data work happens strictly outside production hours or during genuinely quiet periods

## How Data Improvements Reduce Staffing Pressure

The reason 2 team leaders are needed on some lines is largely the paperwork burden. The data improvements proposed would directly reduce this:

| Current Manual Task | Proposed Automation | Impact |
|---|---|---|
| Manual weight recording from Loma | Automated data capture to SQL Server | Removes one manual recording step |
| Manual basket counting and ticket printing (salmon) | OCM individual basket weighing | More accurate, less manual intervention |
| Manual plan attainment tracking in Excel | Auto-calculated from OCM/SI data | Saves Simon 30+ min daily |
| Walking coldstore to check use-by dates | FEFO dashboard on screen | Saves despatch 15+ min per check |
| Compiling traceability data for audits | One-click query from SQL Server | Audit prep time: hours to minutes |

**Long-term outcome:** If paperwork is automated, the second team leader role on lines that require 2 becomes less critical. This does not eliminate the role — it reduces the workload enough that 1 strong team leader with automated tools could potentially manage what currently requires 2.
