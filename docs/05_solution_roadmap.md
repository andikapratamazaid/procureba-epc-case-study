# Solution Roadmap

**ProcureBA, EPC Procurement Digitalization Case Study**
All benefit figures are case-study simulation targets derived from the synthetic data analysis. They are design targets to be validated with real operating data after go-live, not measured results.

## Phase 0: Policy and Preparation (Month 0 to 1)

- Issue the company decree (SK Direksi) recognizing electronic approvals and e-signatures.
- Approve the quotation deadline rule (standard 3 working days) and the fast-track governance rule (justification, elevated approval, post-review).
- Finalize vendor selection (Build vs Buy recommendation: SaaS), contract, and security review with IT.
- Clean and migrate vendor master data (18 active vendors) and build the item catalog for the top three spend categories (Mechanical Equipment, Electrical Equipment, Services and Subcontracting, together 76.1% of spend).
- Exit criteria: policies signed, vendor data loaded, catalog covers the top three categories.

## Phase 1: Core Flow (Months 1 to 3)

**Deliverables:** online PR submission (FR-01, FR-02), approval workflow with reminders and delegation (FR-03), procurement validation queue with SLA timers (FR-04), requester status tracking (FR-13), notifications (FR-15).

- Pilot at two sites (one large, one remote) for four weeks, then roll out to all five sites.
- Paper PR forms withdrawn site by site as each site goes live.
- Target at end of Phase 1 (simulation target): PM approval plus review queue time down from 7.78 days combined to 2.0 days; 100% of new PRs digital.

## Phase 2: Sourcing and Fulfillment (Months 4 to 6)

**Deliverables:** RFQ generation and vendor portal (FR-05), comparison matrix (FR-06), e-PO with e-signature (FR-07), fast-track lane (FR-08), goods receipt and delivery tracking (FR-09), three-way match (FR-10).

- Vendor onboarding program: assisted first quotation for all 18 active vendors, with extra support for Tier C vendors.
- Fast-track lane activated together with a management communication that off-system buying will no longer be reimbursed without a fast-track record.
- Target at end of Phase 2 (simulation target): average cycle time 7.0 days or less; quotation wait 3.0 days or less; maverick rate trending to 3% or less.

## Phase 3: Intelligence and Optimization (Months 7 to 9)

**Deliverables:** KPI dashboard and scheduled reports (FR-12), vendor scorecards (FR-11), master data administration maturity (FR-14), framework agreements for top catalog categories.

- First quarterly vendor review using scorecards; order allocation guidance issued for low-scoring vendors (baseline weakest score 55.4, on-time 71.1%).
- Seasonal capacity plan for the March to August peak built from dashboard data.
- Target at end of Phase 3 (simulation target): on-time delivery rate toward 93%; maverick rate at or below 3%; monthly management reporting fully automatic.

## Benefit Ramp (simulation targets)

| Measure | Baseline (analysis) | End Phase 1 | End Phase 2 | End Phase 3 |
|---|---|---|---|---|
| Average cycle time | 17.5 days | 12 days | 7.0 days | 7.0 days or less |
| Maverick rate | 12.2% of PRs | 10% | 5% | 3% or less |
| Quotation wait | 6.02 days | 6.02 days | 3.0 days | 3.0 days or less |
| On-time delivery | 85.7% | 85.7% | 88% | toward 93% |
| PRs processed digitally | 0% | 100% | 100% | 100% |

## Implementation Risks (summary, full detail in the Risk Register)

| Risk | Phase most exposed | Headline mitigation |
|---|---|---|
| Approvers resist losing wet signatures | Phase 1 | Sponsor decree, mobile approval design, delegation rule |
| Vendors do not adopt the portal | Phase 2 | Assisted onboarding, email-triggered simple quotation entry, helpdesk |
| Sites keep buying off-system | Phase 2 | Fast-track lane plus reimbursement rule, monthly maverick report to management |
| Low site bandwidth degrades usability | Phase 1 | NFR-04 lightweight design, form autosave, pilot includes a remote site |
| Data migration errors in vendor master data | Phase 0 | Dual verification with finance records before load |
| Scope creep toward full ERP | All | Phase gates with the steering committee; ERP integration parked as a future phase decision |
