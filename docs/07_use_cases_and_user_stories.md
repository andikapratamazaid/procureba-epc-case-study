# Use Cases and User Stories

**ProcureBA, EPC Procurement Digitalization Case Study**
Use case diagram: `diagrams/use_case_diagram.png`. Requirements referenced are from `docs/03_business_requirements.md`.

## 1. Use Case Specifications (summary form)

### UC-01 Submit Purchase Requisition
- **Actor:** Site Engineer (requester). **Covers:** FR-01, FR-02.
- **Main flow:** 1) Requester opens the PR form and picks items from the catalog or describes a non-catalog item. 2) System validates mandatory fields and budget code. 3) Requester sets the required date and urgency (normal or fast-track request with justification). 4) System issues a PR number, timestamps the submission, and routes it to the approval chain. 5) Requester sees the PR on their tracking page.
- **Alternative flow:** Non-catalog item: requester adds a free-text specification and attachment; procurement validates the specification during review.
- **Exception flow:** Budget code invalid or budget exceeded: submission is blocked with a clear message and routed to the Project Manager for a budget decision.

### UC-02 Approve or Reject PR
- **Actor:** Project Manager. **Covers:** FR-03.
- **Main flow:** 1) Approver receives a notification. 2) Approver reviews PR details, value, and justification in the app. 3) Approver approves; the PR moves to the procurement queue with a full audit entry. 4) If no action within the configured period, the system sends reminders; after the escalation period, the delegation rule routes to the named delegate.
- **Alternative flow:** Approver requests clarification; the PR returns to the requester with a comment, and the stage timer pauses.
- **Exception flow:** Approver rejects with a mandatory reason; the requester is notified and the PR closes with the reason on record.

### UC-03 Create and Send RFQ
- **Actor:** Procurement Officer. **Covers:** FR-05.
- **Main flow:** 1) Officer selects an approved PR from the queue. 2) System generates the RFQ from PR data with a standard template. 3) Officer selects vendors (scorecard data shown) and sets the quotation deadline. 4) System publishes the RFQ to the vendor portal and emails notifications.
- **Alternative flow:** Officer combines several PRs of the same category into one RFQ.
- **Exception flow:** Fewer than the minimum number of vendors available for the category: the system flags a single-source justification requirement.

### UC-04 Submit Quotation
- **Actor:** Vendor. **Covers:** FR-05.
- **Main flow:** 1) Vendor opens the RFQ from the email link and signs in. 2) Vendor enters unit prices, delivery lead time, and validity per line. 3) Vendor submits before the deadline; the system confirms receipt and locks the quotation.
- **Alternative flow:** Vendor submits a partial quotation for some lines only; the system marks missing lines clearly.
- **Exception flow:** Submission after the deadline is blocked unless procurement reopens the RFQ; late interest is recorded for the scorecard context.

### UC-05 Evaluate and Issue PO
- **Actor:** Procurement Officer (award), Procurement Manager (approval above threshold). **Covers:** FR-06, FR-07.
- **Main flow:** 1) After the deadline, the system builds the comparison matrix. 2) Officer evaluates price, lead time, and vendor score, and records the rationale. 3) Award above the value threshold routes to the Procurement Manager for approval. 4) System generates the PO from the awarded quotation, applies e-signature, and notifies the vendor. 5) Vendor acknowledges the PO in the portal.
- **Alternative flow:** Split award across two vendors by line item; the system generates one PO per vendor.
- **Exception flow:** All quotations exceed the budget estimate by more than the tolerance: the award is blocked and returned for re-scoping or budget approval.

### UC-06 Track Procurement Status
- **Actor:** Site Engineer, Project Manager, Management. **Covers:** FR-13, FR-12.
- **Main flow:** 1) User opens the tracking page or dashboard. 2) System shows each PR with its current stage, stage owner, elapsed days in stage, and expected completion. 3) User filters by site, status, or required date.
- **Exception flow:** A PR exceeding its stage SLA is highlighted and its escalation state is shown.

### UC-07 Record Goods Receipt
- **Actor:** Warehouse Staff. **Covers:** FR-09.
- **Main flow:** 1) Staff open the PO from the delivery list. 2) They record received quantities and condition per line. 3) System updates delivery status and notifies the requester and procurement. 4) Full receipt closes the delivery step; partial receipt keeps it open with the remaining quantities shown.
- **Exception flow:** Quantity or specification mismatch: staff record the discrepancy, the system flags it to procurement and blocks the affected lines from invoice matching.

### UC-08 Match Invoice (Three-Way Match)
- **Actor:** System (automatic), Finance Staff (exceptions). **Covers:** FR-10.
- **Main flow:** 1) Vendor invoice is registered against a PO. 2) System compares PO value, goods receipt quantities, and invoice lines. 3) Matching invoices are marked ready for payment; finance is notified.
- **Exception flow:** Any mismatch creates an exception task for finance with the differing fields highlighted; payment is blocked until resolved.

### UC-09 Manage Vendor Master Data
- **Actor:** Procurement Officer. **Covers:** FR-11, FR-14.
- **Main flow:** 1) Officer creates or updates a vendor record (identity, bank data, categories, tier). 2) Changes to bank data require a second-person verification. 3) System recalculates the scorecard monthly from transaction data.
- **Exception flow:** Duplicate vendor detected by tax ID: the system blocks creation and offers a merge flow.

### UC-10 View KPI Dashboard
- **Actor:** Management, Procurement Manager. **Covers:** FR-12.
- **Main flow:** 1) User opens the dashboard. 2) System shows cycle time by stage, maverick rate, spend by category and vendor, on-time rate, and queue aging for the selected period and site. 3) User exports or schedules the report.
- **Exception flow:** Figures for the current incomplete month are labeled as partial.

### UC-11 Manage Users and Catalog
- **Actor:** System Admin. **Covers:** FR-14.
- **Main flow:** 1) Admin maintains users, roles, and the approval matrix. 2) Admin maintains catalog items and standard specifications with QA/QC review for technical items. 3) All changes are versioned and logged.
- **Exception flow:** A catalog change affecting open PRs applies only to new PRs; open PRs keep the version they were created with.

## 2. User Stories with Acceptance Criteria

| ID | Story | Acceptance criteria | Covers |
|---|---|---|---|
| US-01 | As a Site Engineer, I want to raise a PR from a catalog in under five minutes so that ordering does not eat my engineering time. | Form completable in 5 minutes for catalog items; mandatory fields validated inline; PR number issued immediately | FR-01, FR-02 |
| US-02 | As a Site Engineer, I want to see exactly where my PR is so that I stop calling procurement for updates. | Tracking page shows stage, owner, and elapsed time, updated in real time | FR-13 |
| US-03 | As a Site Engineer facing a breakdown, I want a fast-track lane with a justification so that urgent work proceeds without breaking procedure. | Fast-track requires justification and one-level-higher approval; record flagged for post-review | FR-08 |
| US-04 | As a Project Manager, I want to approve PRs from my phone with reminders so that approvals stop waiting for my desk time. | Approval completable on mobile; reminder at 24 hours; delegation after the configured period | FR-03 |
| US-05 | As a Procurement Officer, I want one prioritized queue so that I work on the most time-critical PRs first. | Queue sorted by required date and SLA risk; aging visible per PR | FR-04 |
| US-06 | As a Procurement Officer, I want RFQs generated from PR data so that I never retype specifications. | RFQ document generated without manual data entry; deadline set by default rule | FR-05 |
| US-07 | As a Vendor, I want to submit a quotation through one simple page so that responding takes minutes, not a document exercise. | Quotation entry per line with price, lead time, validity; confirmation receipt issued | FR-05 |
| US-08 | As a Procurement Officer, I want an automatic comparison matrix with vendor scores so that my award decision is defensible. | Matrix shows price, lead time, score; rationale field mandatory before award | FR-06, FR-11 |
| US-09 | As a Procurement Manager, I want POs generated and e-signed from the award so that issuance takes hours, not days. | PO generated from awarded quotation; e-signature applied; vendor notified automatically | FR-07 |
| US-10 | As Warehouse Staff, I want to record receipts against the PO on one screen so that delivery status is always current. | Receipt recorded per line with quantity and condition; partial delivery supported | FR-09 |
| US-11 | As a Finance Manager, I want invoices matched automatically so that my team handles only exceptions. | Match result per invoice; exceptions listed with differing fields; payment blocked on unresolved mismatch | FR-10 |
| US-12 | As a Director, I want a monthly dashboard of cycle time, maverick rate, and vendor performance so that I can see whether procurement is improving. | Dashboard refreshes automatically; figures reconcile with transaction data | FR-12 |

## 3. Story Map

| Backbone activity | Walking skeleton (Phase 1) | Phase 2 additions | Phase 3 additions |
|---|---|---|---|
| Request | US-01 catalog PR | US-03 fast-track lane | Framework agreement call-off |
| Approve | US-04 mobile approval with delegation | Value-threshold approval levels | Approval analytics |
| Source | US-05 prioritized queue, US-06 RFQ generation | US-07 vendor quotation portal, US-08 comparison and award | Scorecard-driven vendor shortlists |
| Order | Status visibility of awarded PRs | US-09 e-PO with e-signature | Auto PO for catalog call-offs |
| Receive and Pay | Delivery expected-date view | US-10 goods receipt, US-11 three-way match | Exception trend analysis |
| Monitor | US-02 requester tracking | US-12 management dashboard (basic) | US-12 full KPI suite and vendor reviews |
