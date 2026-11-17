# Gap Analysis

**ProcureBA, EPC Procurement Digitalization Case Study**
Each gap maps the current state (as-is, evidenced by the synthetic data analysis) to the target state (to-be) and to the BRD requirement IDs that close it.

| Gap ID | Area | Current state (as-is) | Target state (to-be) | Gap size | Closing requirements |
|---|---|---|---|---|---|
| GAP-01 | PR submission | Paper form, free-text items, incomplete forms discovered late | Online form with catalog, mandatory fields, attachments | Large: new channel for about 1,200 PRs per year | FR-01, FR-02, BR-06 |
| GAP-02 | Approval | Wet signature, single approver, no delegation, avg 3.74 days | In-app approval with reminders and delegation, target 1.0 day | Large: behavior and policy change (e-signature decree) | FR-03, BR-01 |
| GAP-03 | Procurement queue | Invisible paper queue, avg 4.04 days, no SLA | Visible digital queue with SLA timers and escalation, target 1.0 day | Medium: process redesign plus system | FR-04, BR-01, BR-02 |
| GAP-04 | RFQ and quotation | Email RFQ, no deadline, avg wait 6.02 days (34.4% of cycle) | Vendor portal, fixed deadline, automatic reminders, target 3.0 days | Large: vendor onboarding for 18 active vendors | FR-05, BR-04 |
| GAP-05 | Evaluation | Manual spreadsheet comparison, rationale unrecorded | Automatic comparison matrix, recorded rationale | Medium | FR-06, BR-08 |
| GAP-06 | PO issuance | Typed, printed, signed, scanned, emailed; stage avg 2.59 days with evaluation | Generated e-PO with e-signature, target 0.5 day issuance | Medium | FR-07, BR-06 |
| GAP-07 | Urgent buying | 12.2% of PRs bypass the process at a 10.8% price premium | Fast-track lane inside the system with justification and post-review; maverick target 3% or less | Large: governance change, not only tooling | FR-08, BR-03 |
| GAP-08 | Status visibility | None; updates by phone and email | Live tracking page per requester and management dashboard | Medium | FR-13, FR-12, BR-02, BR-07 |
| GAP-09 | Goods receipt | Paper delivery notes, mismatches found at payment time | GR recorded against PO, delivery tracked, mismatch flagged at receipt | Medium | FR-09, FR-10 |
| GAP-10 | Invoice processing | Manual three-way match by finance | Automatic match, finance handles exceptions only | Medium | FR-10, BR-08 |
| GAP-11 | Vendor performance | Not recorded; scores in the analysis range 55.4 to 86.2 with no consequence | Automatic scorecard feeding vendor selection and allocation | Medium: data exists once transactions are digital | FR-11, BR-05 |
| GAP-12 | Spend and catalog management | Free-text buying across all categories; top 3 categories hold 76.1% of spend | Item catalog and framework agreements for the top categories | Medium | FR-01, FR-14, BR-07 |
| GAP-13 | Audit trail | Paper forms and personal inboxes | System audit log of every action, 10-year retention | Large for historical records; small going forward | FR-02, FR-06, NFR-05, BR-08 |
| GAP-14 | Reporting | Manual, rare, spreadsheet based | Automated monthly KPI dashboard and scheduled reports | Small once data is digital | FR-12, BR-07 |
| GAP-15 | Seasonal capacity | PR volume peaks at 2.07 times the low month (April 236 vs January 114) with flat manual capacity | Queue prioritization by required date and SLA absorbs peaks; seasonal staffing plan for March to August | Medium | FR-04, BR-01 |

## Reading the gaps

- **Tooling gaps** (GAP-01, 03, 05, 06, 08, 09, 10, 14) close as soon as the system is live, because the digital process produces the data as a by-product.
- **Behavior and governance gaps** (GAP-02, 04, 07) are the real project risk. They need policy decisions (e-signature decree, quotation deadline rule, fast-track governance) and are sequenced early in the roadmap for that reason.
- **Data gaps** (GAP-11, 12, 13) close progressively: scorecards and catalogs become meaningful after the first full quarter of digital transactions, which is why they sit in Phase 3 of the roadmap.
