# Stakeholder Analysis

**ProcureBA, EPC Procurement Digitalization Case Study**
Power-interest grid: `diagrams/power_interest_grid.png`.

> Fictional case study. Roles and people are illustrative, modeled on a typical mid-size EPC contractor with five project sites.

## 1. Stakeholder Register

| ID | Stakeholder | Role in the process | Key interests | Main concerns |
|---|---|---|---|---|
| SH-01 | Director of Operations | Sponsor; approves budget and policy change | Shorter material lead times, cost control, project delivery certainty | Disruption during implementation; benefit claims must be measurable |
| SH-02 | Procurement Manager | Process owner; runs the procurement team | Queue control, vendor performance data, less manual administration | Team workload during transition; being measured by new KPIs |
| SH-03 | Project Managers (5 sites) | Approvers of PRs for their sites | Fast approval turnaround, material arriving on schedule | Losing the informal fast path (phone calls and maverick buying) |
| SH-04 | Finance Manager | Budget control, invoice matching, payment | Clean audit trail, accurate PO values, no duplicate payments | Data quality of migrated records; three-way match discipline |
| SH-05 | Site Engineers and Supervisors | Requesters; raise most PRs | Knowing PR status without chasing; fast handling of genuine urgencies | Extra data entry effort; system usability on site connectivity |
| SH-06 | Warehouse Staff | Goods receipt and stock records | Delivery information in advance; simple receipt recording | Double recording during transition period |
| SH-07 | Procurement Officers | Daily operators of RFQ, evaluation, PO | Less retyping, clear priorities, fair workload distribution | Job security fears about automation; learning curve |
| SH-08 | Vendors (18 active in the dataset) | Quotation and delivery partners | Clear RFQ specifications, fair deadlines, faster payment | Portal learning effort, especially small Tier C vendors |
| SH-09 | IT Department | System selection, security, support | Security compliance, low support burden, clean integration | Shadow IT risk if business picks tools without IT review |
| SH-10 | QA/QC and HSE | Material specification and inspection requirements | Correct specifications on PRs and POs; inspection hold points | Catalog standardization must not weaken technical specifications |
| SH-11 | External Auditors | Annual audit of procurement controls | Complete, retrievable audit trail | Transition period gaps between paper and digital records |

## 2. Power-Interest Assessment

| Stakeholder | Power | Interest | Quadrant strategy |
|---|---|---|---|
| Director of Operations (SH-01) | High | High | Manage closely: steering committee chair, monthly progress review |
| Procurement Manager (SH-02) | High | High | Manage closely: co-designer of the to-be process and KPI definitions |
| Project Managers (SH-03) | High | High | Manage closely: approval workflow and fast-track rules designed with them |
| Finance Manager (SH-04) | High | High | Manage closely: three-way match and reporting requirements validated together |
| Site Engineers (SH-05) | Low (individual) / High (collective) | High | Keep informed and involved: pilot users, feedback channel, site champions |
| IT Department (SH-09) | Medium | Medium | Keep satisfied: involved from vendor selection, owns security review |
| Vendors (SH-08) | Medium | Medium | Keep informed: onboarding program, assisted first quotation, helpdesk |
| Warehouse Staff (SH-06) | Low | Medium | Keep informed: simple receipt screens, training at each site |
| QA/QC and HSE (SH-10) | Medium | Low to Medium | Keep satisfied: catalog specification review before go-live |
| External Auditors (SH-11) | Medium | Low | Monitor: informed of cutover plan and archive arrangements |

The grid image (`diagrams/power_interest_grid.png`) plots the same assessment visually.

## 3. RACI Matrix

R = Responsible (does the work), A = Accountable (owns the decision), C = Consulted, I = Informed.

| Activity | Director of Operations | Procurement Manager | Project Manager | Procurement Officer | Finance | IT | Site Engineer | Vendor |
|---|---|---|---|---|---|---|---|---|
| Raise PR | I | I | A | I | I | n/a | R | n/a |
| Approve PR | I | C | A/R | I | C (budget) | n/a | I | n/a |
| Validate PR and assign priority | I | A | C | R | I | n/a | I | n/a |
| Issue RFQ | n/a | A | I | R | n/a | n/a | I | I |
| Submit quotation | n/a | I | n/a | I | n/a | n/a | n/a | R |
| Evaluate and award | I (above threshold) | A | C | R | C | n/a | I | I |
| Issue PO | I | A | I | R | I | n/a | I | I (acknowledge) |
| Record goods receipt | n/a | I | I | I | I | n/a | C | I |
| Match invoice and pay | I | C | n/a | C | A/R | n/a | n/a | I |
| Maintain vendor master data | n/a | A | n/a | R | C | C | n/a | C |
| Maintain item catalog | n/a | A | C | R | n/a | C | C | n/a |
| Administer users and roles | n/a | C | n/a | n/a | n/a | A/R | n/a | n/a |
| Review KPI dashboard | A | R | C | C | C | I | I | n/a |

## 4. Engagement Notes

- The single most important engagement risk is SH-03 (Project Managers). They currently benefit from informal fast paths. The design answer is not to forbid urgency but to give it a legitimate fast-track lane with their names on the approval, which converts a control problem into an accountability feature they helped design.
- SH-07 (Procurement Officers) need an explicit message that the system removes retyping, not people: the same headcount shifts from data entry to vendor management and expediting.
- SH-08 (Vendors) includes small Tier C vendors with limited IT capability. The rollout plan includes assisted onboarding and keeps email notification as the trigger, with the portal used only for quotation entry.
