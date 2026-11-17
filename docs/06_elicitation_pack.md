# Elicitation Pack

**ProcureBA, EPC Procurement Digitalization Case Study**
Contains interview guides per role, a simulated findings summary, and three user personas. The findings are simulated for this case study and are consistent with the quantitative analysis of the synthetic dataset (2,400 PR records).

## 1. Interview Guides

### 1.1 Project Team (Project Managers, Site Engineers, Supervisors)

1. Walk me through the last PR you raised, from the moment you knew you needed the material to the moment it arrived. Where did time go?
2. How do you find out where your PR currently is? Who do you call, and how long does an answer take?
3. When do you mark a PR urgent, and what actually happens differently when you do?
4. Tell me about a time material arrived late and affected the work schedule. What was the root cause?
5. What makes you buy directly outside the PR process? What would have to change for you to stay inside it?
6. Which PR information do you wish you could see at any time?
7. If approval could be done from a phone, what would still stop it from being fast?
8. What item descriptions cause the most back-and-forth with procurement?

### 1.2 Procurement (Procurement Manager, Procurement Officers)

1. Describe your day when PR files arrive. How do you decide what to work on first?
2. Where does a PR wait the longest in your area, and why?
3. How do you build an RFQ today, and what information is usually missing from the PR?
4. How do vendors submit quotations, and what makes comparison slow or error-prone?
5. How is the PO produced and approved today? Where are the rework loops?
6. How do you choose which vendors receive an RFQ? What role does past delivery performance play?
7. What records do you keep for audit, and how long does retrieval take?
8. Which reports does management ask for, and how long do they take to assemble?

### 1.3 Finance (Finance Manager, Payables Staff)

1. Walk me through an invoice from arrival to payment. Where do mismatches appear?
2. What are the most common causes of a failed three-way match today?
3. How do maverick purchases show up in your process, and what extra work do they create?
4. What PO and receipt information would you need to match invoices without manual checking?
5. Which procurement data do you need for accruals and project cost reporting?
6. What controls must the new process keep for audit purposes?

### 1.4 Warehouse (Warehouse Staff, Storekeepers)

1. How do you know a delivery is coming? What notice do you get today?
2. Walk me through receiving a delivery: documents, checks, and records you produce.
3. What happens when quantities or specifications do not match the PO?
4. How are partial deliveries handled and communicated?
5. What would make goods receipt recording faster without losing accuracy?

## 2. Simulated Findings Summary

The themes below are the simulated outcome of running these interviews. Each theme is cross-checked against the dataset analysis.

| ID | Theme (what stakeholders said) | Evidence from data analysis | Design response |
|---|---|---|---|
| EF-01 | "We never know where our PR is." Requesters call or email procurement several times per PR. | No tracking exists; queue stages average 4.04 days invisible in the review queue | FR-13 status tracking, FR-04 visible queue |
| EF-02 | "Approval waits for one person." PM signatures stall when the PM is on site rounds. | PM Approval averages 3.74 days, 21.4% of the cycle | FR-03 mobile approval, reminders, delegation |
| EF-03 | "Urgent means we buy it ourselves." Sites bypass the process when work would stop. | 21.0% of PRs flagged urgent; 12.2% maverick at a 10.8% premium; maverick cycle 1.4 days vs 19.7 planned | FR-08 fast-track lane with post-review |
| EF-04 | "Vendors answer when they answer." No RFQ deadline culture. | Vendor Quotation Wait 6.02 days, the largest stage at 34.4% | FR-05 portal with deadline and reminders |
| EF-05 | "Good and bad vendors are treated the same." Buyers rely on memory. | Scorecard spread 55.4 to 86.2; weakest vendor still gets 159 transactions | FR-11 automatic scorecard |
| EF-06 | "Reporting takes days and is still doubted." Manual spreadsheet assembly. | Spend and cycle figures require full re-extraction each time | FR-12 dashboard |
| EF-07 | "The form comes back because the spec was unclear." Free-text PR items cause rework. | Rework concentrated in high-volume categories; top 3 categories are 76.1% of spend | FR-01 catalog with standard specifications |
| EF-08 | "Peak season overwhelms the queue." March to August volume strains fixed capacity. | Peak month volume 2.07 times the low month | FR-04 priority by required date; seasonal capacity plan |

## 3. User Personas

### Persona 1: Site Engineer (Requester)

- **Name and role:** Rizky, 29, Site Engineer at a remote project site, 4 years with the Company.
- **Goals:** Get the right material on site before the work front needs it; spend time on engineering, not paperwork.
- **Daily reality:** Raises 6 to 10 PRs per month, mostly Mechanical Equipment and Consumables. Connectivity at site is intermittent. Currently fills paper forms, photographs them "just in case", and calls procurement twice a week for status.
- **Frustrations:** No visibility; urgent needs force him into maverick buying that finance later questions; PR forms returned days later for unclear specifications.
- **What success looks like:** Submit a PR from the catalog in five minutes, watch it move, and use a legitimate fast-track when a breakdown stops work.
- **Key requirements driven:** FR-01, FR-08, FR-13, NFR-04.

### Persona 2: Procurement Officer (Operator)

- **Name and role:** Sari, 34, Procurement Officer at head office, handles RFQs and POs for two sites.
- **Goals:** Clear her queue fairly, award to vendors who deliver, keep an audit-clean record.
- **Daily reality:** Maintains the master spreadsheet, retypes PR data into RFQ documents and POs, chases vendors by phone for quotations, and fields status calls from sites. Her queue priority is set by whoever calls loudest.
- **Frustrations:** Retyping the same data three times; no record of vendor reliability when she needs to justify an award; month-end reporting assembled by hand.
- **What success looks like:** A prioritized queue, one-click RFQ from PR data, automatic quotation comparison, and a scorecard that backs her award decisions.
- **Key requirements driven:** FR-04, FR-05, FR-06, FR-11, FR-12.

### Persona 3: Finance Manager (Control)

- **Name and role:** Dewi, 41, Finance Manager, accountable for payment accuracy and audit outcomes.
- **Goals:** Pay the right amount once, on time, with a complete audit trail; close project cost reports without surprises.
- **Daily reality:** Her team manually matches invoices against scanned POs and paper delivery notes. Maverick purchases arrive as invoices with no PO at all, forcing exception handling and awkward conversations with sites.
- **Frustrations:** Mismatches discovered at payment time; incomplete trails for audit; no reliable accrual data from procurement.
- **What success looks like:** Automatic three-way match with exceptions only, every purchase carrying a PO or a fast-track record, and procurement data flowing into cost reporting.
- **Key requirements driven:** FR-09, FR-10, BR-08, NFR-05.
