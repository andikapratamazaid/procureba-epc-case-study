# Business Requirements Document (BRD)

**Project:** ProcureBA, EPC Procurement Digitalization
**Version:** 1.0 (case study)
**Author:** Business Analyst

> Fictional case study. Baselines quoted below are computed from the synthetic dataset in this repository (2,400 PR records, 2024 to 2025). Targets are design targets for the proposed solution, labeled as simulation targets where they project future performance.

## 1. Purpose

This document defines the business, functional, and non-functional requirements for digitalizing the PR-to-PO procurement process of a mid-size EPC contractor operating five project sites. It is the controlling document for solution selection, prototyping, and user acceptance testing. Every requirement is numbered and traced to use cases and UAT scenarios in `docs/12_uat_plan_and_traceability.md`.

## 2. Business Requirements

| ID | Requirement | Baseline (analysis) | Target | Priority |
|---|---|---|---|---|
| BR-01 | Reduce the average PR-to-PO cycle time | 17.5 days average, 27 days at P90 | 7.0 days or less average within 6 months of go-live | Must |
| BR-02 | Provide real-time visibility of PR and PO status to requesters, procurement, and management | No visibility; status by phone and email | 100% of PRs trackable online at every stage | Must |
| BR-03 | Bring off-procedure buying under control while keeping a legitimate path for genuine urgencies | Maverick rate 12.2% of PRs, 13.6% of spend, 10.8% price premium | Maverick rate 3% or less; 100% of urgent PRs processed through the fast-track lane | Must |
| BR-04 | Standardize the vendor quotation process with deadlines and comparable data | Quotation wait 6.02 days average, no deadline | Quotation wait 3.0 days or less; every RFQ carries a deadline | Must |
| BR-05 | Record vendor delivery performance and use it in vendor selection | On-time rate 85.7% overall, never recorded per vendor | Monthly vendor scorecard; on-time rate toward 93% | Should |
| BR-06 | Eliminate manual administration in the PR-to-PO flow | Paper forms, spreadsheet logging, manual PO typing | Zero paper forms and zero retyping of PR or quotation data | Must |
| BR-07 | Provide management reporting on spend, cycle time, and compliance without manual assembly | Reporting assembled by hand, rarely produced | Monthly dashboard refreshed automatically | Should |
| BR-08 | Create a complete audit trail for every PR, approval, quotation, and PO | Paper and personal email records | 100% of actions logged with user, timestamp, and before/after values | Must |

## 3. Functional Requirements

| ID | Requirement | Priority (MoSCoW) | Related BR |
|---|---|---|---|
| FR-01 | Online PR submission using an item catalog with standard specifications, mandatory fields, and attachment support | Must | BR-01, BR-06 |
| FR-02 | Automatic PR numbering, timestamping, and routing to the correct approval chain based on site, category, and value | Must | BR-06, BR-08 |
| FR-03 | Multi-level approval workflow with in-app and email approval, automatic reminders, and a delegation rule when an approver is unavailable | Must | BR-01 |
| FR-04 | Procurement validation queue showing all pending PRs with age, priority, required date, and SLA timers with escalation | Must | BR-01, BR-02 |
| FR-05 | RFQ generation from PR data and a vendor portal for quotation submission with a fixed deadline and automatic reminders | Must | BR-04 |
| FR-06 | Quotation comparison matrix generated automatically from submitted quotations, with a recorded evaluation rationale | Must | BR-04, BR-08 |
| FR-07 | PO generation from the awarded quotation with e-signature and automatic notification to the vendor | Must | BR-01, BR-06 |
| FR-08 | Fast-track lane for urgent PRs requiring a written justification, one-level-higher approval, and automatic post-review flagging | Must | BR-03 |
| FR-09 | Goods receipt recording against a PO, with quantity and condition checks and delivery status updates | Must | BR-02 |
| FR-10 | Automatic three-way match of PO, goods receipt, and vendor invoice, with mismatch flagging for finance | Must | BR-08 |
| FR-11 | Vendor master data management and an automatic vendor performance scorecard (on-time rate, lead time, transaction volume) | Should | BR-05 |
| FR-12 | KPI dashboard (cycle time by stage, maverick rate, spend by category and vendor, on-time rate) with scheduled report distribution | Should | BR-07 |
| FR-13 | Requester status tracking page showing the current stage, stage owner, and elapsed time for each of their PRs | Must | BR-02 |
| FR-14 | Master data administration for item catalog, users, roles, and the approval matrix | Should | BR-06 |
| FR-15 | Notification engine for approvals, deadlines, escalations, and status changes by email and in-app alerts | Must | BR-01 |

**Could have (future phase):** predictive delivery risk alerts based on vendor history; automatic framework agreement call-off for catalog items; spend forecasting by project schedule.

**Won't have (this phase):** full ERP integration; inventory optimization; subcontract contract lifecycle management; payment execution.

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Performance | Page loads under 3 seconds and approval actions under 2 seconds at 120 concurrent users |
| NFR-02 | Availability | 99.5% availability during business hours (06:00 to 22:00, Monday to Saturday) |
| NFR-03 | Security and access control | Role-based access per the RACI matrix; single sign-on ready; complete audit log; vendor accounts see only their own RFQs and POs |
| NFR-04 | Usability and connectivity | Fully usable on low-bandwidth site connections; approval workflow completable on a mobile phone browser; forms tolerate connection drops without data loss |
| NFR-05 | Data retention and backup | Daily backup; transaction records retained 10 years for audit; paper archive of pre-cutover records remains retrievable |
| NFR-06 | Scalability | Supports up to 10 sites, 250 users, and 3,000 PRs per year without redesign (current volume 2,400 PRs over two years across 5 sites) |
| NFR-07 | Language and localization | Interface in Bahasa Indonesia and English; currency in IDR; Indonesian tax document fields (faktur pajak reference) supported on invoice records |

## 5. Acceptance Criteria (business level)

The solution is accepted when all of the following are demonstrated in UAT (see `docs/12_uat_plan_and_traceability.md`) and measured after go-live:

1. A standard PR can be submitted, approved, quoted, and converted to a PO entirely inside the system with no paper and no retyping (FR-01 to FR-07).
2. An urgent PR processed through the fast-track lane shows its justification, elevated approval, and post-review flag (FR-08, BR-03).
3. A requester can see the live stage and elapsed time of any of their PRs without contacting procurement (FR-13, BR-02).
4. The vendor scorecard for the pilot period reproduces on-time and lead time figures consistent with the underlying transaction records (FR-11).
5. The KPI dashboard stage averages reconcile with the transaction data for the same period (FR-12).
6. Three months after go-live, the measured average cycle time is on the glide path to 7.0 days or less and the maverick rate is 3% or less (BR-01, BR-03). These are simulation targets set at design time and must be validated with real operating data.

## 6. Assumptions and Constraints

- Approvers are willing to replace wet signatures with e-signature, supported by a company decree (SK Direksi) on electronic approvals.
- Vendors can access email reliably; portal use is limited to quotation entry and PO acknowledgment to keep the vendor learning curve low.
- Site connectivity is sufficient for web forms; no offline native app is built in this phase (NFR-04 mitigates).
- Budget envelope follows the Cost-Benefit Analysis: one-time Rp 0.80 billion, recurring Rp 0.54 billion per year (case-study estimates).
