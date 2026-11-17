# Process Maps: As-Is and To-Be

**ProcureBA, EPC Procurement Digitalization Case Study**
Diagrams: `diagrams/process_as_is.png` and `diagrams/process_to_be.png` (BPMN-style swimlane maps, drawn programmatically by `diagrams/make_diagrams.py`).

> Fictional case study with synthetic data. Stage times quoted below are computed from the synthetic dataset of 2,400 PR records (see `analysis/findings.md`).

## As-Is Process (manual, average cycle time 17.5 days)

| Step | Lane | Activity | Avg days in stage | Pain points |
|---|---|---|---|---|
| 1 | Requester (Site) | Fill paper PR form | n/a | Free-text item descriptions, no catalog, frequent incomplete forms returned later; no copy retained at site |
| 2 | Project Manager | Sign paper form | 3.74 (PM Approval) | Single-person dependency; form waits when PM is on site rounds or leave; no delegation rule; no reminder |
| 3 | Procurement | Log PR manually in spreadsheet | part of queue | Double data entry; typos in values and vendor names; spreadsheet is the only tracking tool and is often out of date |
| 4 | Procurement | Review queue, paper file moves by hand | 4.04 (Procurement Review Queue) | Queue is invisible; no priority rule except shouting; no SLA; files wait over weekends unnoticed |
| 5 | Procurement | Prepare RFQ in Word, send by email | 1.09 (RFQ Preparation) | RFQ format differs per officer; specification attachments get lost between email threads |
| 6 | Vendors | Reply by email when ready | 6.02 (Vendor Quotation Wait) | No quotation deadline and no reminder; this is the single largest stage at 34.4% of the cycle; late quotations hold up everything downstream |
| 7 | Procurement | Compare quotations in spreadsheet | part of evaluation | Manual retyping of prices; comparison errors; no record of why a vendor was chosen |
| 8 | Procurement | Type, print, sign, scan, email PO | 2.59 (Evaluation and PO Issuance) | PO typed from scratch; wet signature repeats the PM bottleneck pattern; scanned copies are hard to search later |
| 9 | Warehouse and Finance | Paper delivery note check, manual 3-way invoice match | outside PR-to-PO cycle | Mismatches between PO, delivery note, and invoice are found at payment time, causing rework and late payment to vendors |

**Cross-cutting pain points**

- No status visibility at any stage: requesters phone procurement for updates, which consumes the same staff time needed to clear the queue.
- No audit trail: decisions and approvals live on paper and in personal email inboxes.
- Urgent needs have no legitimate fast path, so 21.0% of PRs are marked urgent and 12.2% bypass the process entirely (maverick), at a 10.8% price premium.
- Vendor delivery performance (overall on-time rate 85.7%, ranging from 71.1% to 96.1% per vendor) is never recorded, so it cannot influence vendor selection.

## To-Be Process (digital, design target average cycle time 7.0 days)

| Step | Lane | Activity | Target days | How the pain point is removed |
|---|---|---|---|---|
| 1 | Requester (Site) | Submit PR in system, catalog based | same day | Catalog items with standard specifications; mandatory fields prevent incomplete PRs; requester keeps a live tracking view |
| 2 | Project Manager | Approve in app, auto reminder | 1.0 | Mobile approval, automatic reminders, delegation rule when PM is unavailable |
| 3 | Procurement | Auto queue and digital validation | 1.0 | Queue is visible and prioritized by required date; SLA timer escalates stalled PRs |
| 4 | Procurement | System generates RFQ to vendor portal | 0.5 | Standard RFQ template generated from PR data; no retyping |
| 5 | Vendors | Submit quotations online with deadline reminders | 3.0 | Fixed quotation deadline, automatic reminders at midpoint and one day before closing |
| 6 | Procurement | System comparison matrix and evaluation | 1.0 | Prices captured once by vendors; comparison matrix is automatic; evaluation rationale is recorded |
| 7 | Procurement | E-PO issued with e-signature | 0.5 | PO generated from the awarded quotation; no printing or scanning; vendor notified instantly |
| 8 | Warehouse and Finance | Delivery tracked, goods receipt in system, auto 3-way match | outside PR-to-PO cycle | Mismatches flagged at receipt time, not payment time; finance receives only matched invoices |

**Design principles behind the to-be process**

1. Every stage has an owner, a time target, and a visible queue.
2. Data is captured once, at the source (requester enters the PR, vendor enters the quotation), and reused downstream.
3. Genuine urgencies get a controlled fast-track lane inside the system (mandatory justification, higher approval level, post-review) instead of an uncontrolled path outside it.
4. Every action writes to an audit trail automatically.
