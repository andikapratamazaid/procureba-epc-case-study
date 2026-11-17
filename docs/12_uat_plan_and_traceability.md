# UAT Plan and Traceability Matrix

**ProcureBA, EPC Procurement Digitalization Case Study**

## 1. UAT Approach

- **Participants:** two Site Engineers, one Project Manager, two Procurement Officers, the Procurement Manager, one Warehouse Staff, one Finance Staff, and two vendor representatives (one Tier A, one Tier C), facilitated by the Business Analyst.
- **Environment:** vendor sandbox loaded with the case study master data (18 vendors, top-three-category catalog) and 50 scripted test PRs covering normal, urgent, high-value, and mismatch scenarios.
- **Entry criteria:** system configuration complete per the BRD; NFR-04 connectivity test passed from the most remote site; test data loaded and verified.
- **Exit criteria:** all Must-priority scenarios (UAT-01 to UAT-11) pass; no open severity-1 or severity-2 defects; business sign-off by the Procurement Manager and Finance Manager.
- **Defect severity:** S1 blocks a core flow, S2 major workaround exists, S3 cosmetic or minor.

## 2. UAT Scenarios

| ID | Scenario | Key steps | Expected result | Priority |
|---|---|---|---|---|
| UAT-01 | Submit a catalog PR end to end | Site Engineer submits a PR with 3 catalog lines and an attachment | PR number issued, routed to the correct approver, visible on the tracking page | Must |
| UAT-02 | Approval with reminder and delegation | PM takes no action for the reminder period, then the delegate approves | Reminder sent; delegation activates per rule; audit log shows the delegate acted for the PM | Must |
| UAT-03 | Rejection with mandatory reason | PM attempts rejection without a reason, then with a reason | System blocks the reasonless rejection; requester notified with the reason | Must |
| UAT-04 | RFQ generation and on-time quotation | Officer generates an RFQ from an approved PR; vendor submits before the deadline | RFQ created without retyping; quotation recorded and locked; receipt confirmed to the vendor | Must |
| UAT-05 | Late quotation blocked | Vendor attempts submission after the deadline | Submission blocked; attempt logged; officer can reopen the RFQ explicitly | Must |
| UAT-06 | Comparison matrix and award | Officer opens the matrix for a closed RFQ and awards with a rationale | Matrix shows price, lead time, and vendor score; award blocked until the rationale is entered | Must |
| UAT-07 | E-PO issuance and acknowledgment | Award approved above threshold; PO generated and sent; vendor acknowledges | E-signed PO issued from the awarded quotation; acknowledgment recorded; no printing step exists | Must |
| UAT-08 | Fast-track urgent PR | Requester submits an urgent PR with justification; elevated approver approves | PR follows the fast-track SLA; record flagged for post-review; appears in the maverick and fast-track report | Must |
| UAT-09 | Requester tracking accuracy | Requester checks a PR at three different stages | Stage, owner, and elapsed time match the workflow state each time | Must |
| UAT-10 | Goods receipt: partial delivery and mismatch | Warehouse records a partial receipt, then a quantity mismatch on a second delivery | Partial status shown with remaining quantities; mismatch flags the lines and blocks invoice matching for them | Must |
| UAT-11 | Three-way match and exception | Finance registers a matching invoice, then an invoice with a wrong amount | Matching invoice marked ready to pay; wrong invoice creates an exception task with differing fields highlighted | Must |
| UAT-12 | Vendor scorecard calculation | BA recomputes on-time rate and lead time for 3 vendors from raw transactions and compares with the system scorecard | Figures match exactly; tier assignment follows the documented formula | Should |
| UAT-13 | Dashboard reconciliation | BA compares dashboard stage averages and spend totals with transaction data for the test period | All figures reconcile; partial month labeled as partial | Should |
| UAT-14 | Role-based access control | Vendor account attempts to open another vendor's RFQ; requester attempts an approval action | Both attempts denied and logged | Must |

## 3. Traceability Matrix

Every business requirement traces to at least one functional requirement, one use case, and one UAT scenario. Rows marked with an asterisk are also covered by the automated KPI tests in `tests/`.

| BR | Business requirement (short) | FR | Use case | UAT |
|---|---|---|---|---|
| BR-01 | Cycle time 17.5 to 7.0 days | FR-03, FR-04, FR-05, FR-07, FR-15 | UC-02, UC-03, UC-05 | UAT-02, UAT-04, UAT-07 |
| BR-02 | Real-time status visibility | FR-04, FR-13 | UC-06 | UAT-09 |
| BR-03 | Maverick control with fast-track | FR-08 | UC-01 (fast-track path), UC-05 | UAT-08 |
| BR-04 | Standard quotation process with deadlines | FR-05, FR-06 | UC-03, UC-04, UC-05 | UAT-04, UAT-05, UAT-06 |
| BR-05 | Vendor performance used in selection | FR-11 | UC-09, UC-05 | UAT-12 * |
| BR-06 | Eliminate manual administration | FR-01, FR-02, FR-07, FR-14 | UC-01, UC-05, UC-11 | UAT-01, UAT-07 |
| BR-07 | Management reporting without manual assembly | FR-12 | UC-10 | UAT-13 * |
| BR-08 | Complete audit trail | FR-02, FR-06, FR-10 | UC-05, UC-08 | UAT-06, UAT-11, UAT-14 |

| FR | Requirement (short) | Use case | UAT |
|---|---|---|---|
| FR-01 | Online PR submission with catalog | UC-01 | UAT-01 |
| FR-02 | Automatic numbering and routing | UC-01 | UAT-01 |
| FR-03 | Approval workflow, reminders, delegation | UC-02 | UAT-02, UAT-03 |
| FR-04 | Validation queue with SLA timers | UC-03 (queue entry) | UAT-04, UAT-09 |
| FR-05 | RFQ generation and vendor portal | UC-03, UC-04 | UAT-04, UAT-05 |
| FR-06 | Comparison matrix with rationale | UC-05 | UAT-06 |
| FR-07 | E-PO with e-signature | UC-05 | UAT-07 |
| FR-08 | Fast-track lane | UC-01, UC-02 | UAT-08 |
| FR-09 | Goods receipt recording | UC-07 | UAT-10 |
| FR-10 | Automatic three-way match | UC-08 | UAT-11 |
| FR-11 | Vendor master data and scorecard | UC-09 | UAT-12 |
| FR-12 | KPI dashboard and scheduled reports | UC-10 | UAT-13 |
| FR-13 | Requester status tracking | UC-06 | UAT-09 |
| FR-14 | Master data administration | UC-11 | UAT-14 |
| FR-15 | Notification engine | UC-02, UC-03 | UAT-02, UAT-04 |

Non-functional coverage: NFR-03 is exercised by UAT-14; NFR-04 is an entry criterion tested from the most remote site; NFR-01 and NFR-02 are verified by vendor load testing evidence reviewed at the Phase 1 gate; NFR-05 and NFR-06 are verified by configuration and backup-restore inspection; NFR-07 is verified during configuration review.
