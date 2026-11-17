# Case Study Report

# ProcureBA: EPC Procurement Digitalization
## A Business Analysis Case Study

**Author:** Andika Pratama Zaid, Business Analyst
**Document type:** Case study report (portfolio project)
**Status:** Final

> **Honest labeling.** This is a fictional case study created for professional portfolio purposes. The company, people, and transactions are not real. The dataset is synthetic (2,400 purchase requisition records generated with a fixed random seed) and modeled on typical EPC procurement process patterns: manual paper forms, email-based RFQs, spreadsheet tracking, and maverick urgent buying. All analysis figures are real outputs computed from that synthetic dataset by the Python code in this repository, so every number in this report can be reproduced by running the analysis.

---

## 1. Executive Summary

A fictional mid-size EPC contractor, referred to in this case study as "the Company", runs procurement for five project sites through a fully manual process: paper purchase requisition (PR) forms, wet signatures, email-based requests for quotation (RFQ), and spreadsheet tracking. The Company processes about 1,200 PRs per year with a two-year procurement spend of Rp 656.10 billion (synthetic data).

Analysis of 2,400 PR records from January 2024 to December 2025 shows three structural problems:

1. **Slow cycle time.** The average PR-to-PO cycle time is 17.5 days (median 18.0 days, 90th percentile 27 days). The largest single stage is the vendor quotation wait at 6.02 days (34.4% of the cycle), followed by the procurement review queue at 4.04 days (23.1%) and PM approval at 3.74 days (21.4%). About 65.6% of the cycle is internal process time.
2. **Maverick buying.** 294 PRs (12.2%), worth Rp 89.44 billion or 13.6% of spend, bypass the procedure entirely because the official process is too slow for urgent site needs (maverick cycle time 1.4 days versus 19.7 days for planned purchases). Maverick purchases carry a 10.8% price premium, an estimated excess spend of Rp 8.37 billion over two years, about Rp 4.19 billion per year.
3. **Unused vendor performance data.** On-time delivery across all vendors is 85.7%, but the spread is wide: the best vendor scores 86.2 on the case study scorecard (95.5% on-time), while the weakest scores 55.4 (71.1% on-time) and still receives 159 transactions. Nothing in the manual process records or uses this performance.

The recommendation is to implement a cloud e-procurement system (buy, not build, based on the weighted scorecard in the Build vs Buy Analysis) covering online PR submission, digital approval with reminders, an RFQ vendor portal with deadlines, electronic PO issuance, goods receipt recording, automatic three-way matching, and a KPI dashboard. The design target is an average cycle time of 7.0 days or less and a maverick rate of 3% or less, achieved partly by giving genuine urgencies a controlled fast-track lane inside the system.

The Cost-Benefit Analysis (all figures are case-study estimates) projects annual quantified benefits of about Rp 4.85 billion at steady state against one-time implementation costs of Rp 0.80 billion and recurring costs of Rp 0.54 billion per year, with payback in approximately 9 months from project start and a three-year ROI of about 401%.

## 2. Background and Problem Statement

### 2.1 Situation

The Company executes EPC projects at five sites. Site teams raise PRs for equipment, materials, consumables, and services. The procurement function sits at head office. Every step of the PR-to-PO process is manual:

- Requesters fill in a paper PR form and obtain a wet signature from the Project Manager.
- Procurement logs each PR into a shared spreadsheet by hand.
- RFQs are prepared in Word and sent to vendors by email, with no deadline and no reminder mechanism.
- Quotations return by email at whatever pace vendors choose, and are compared in a spreadsheet.
- POs are typed in Word, printed, signed, scanned, and emailed.
- Goods receipts are recorded on paper delivery notes, and finance matches invoices to PO and delivery note manually.

### 2.2 Problem statement

The manual process creates four business problems:

1. **Unpredictable material availability.** With an average cycle time of 17.5 days and a 90th percentile of 27 days before vendor lead time even starts (average actual lead time 13.6 days), site teams cannot plan work reliably around material arrival.
2. **No visibility.** Nobody, requester, Project Manager, or management, can answer "where is my PR?" without phone calls and email searches. The spreadsheet log is updated by hand and is frequently out of date.
3. **Loss of price control.** 12.2% of purchases bypass competitive quotation entirely and cost an estimated 10.8% premium, about Rp 4.19 billion per year in excess spend.
4. **No learning loop.** Vendor delivery performance, stage bottlenecks, and spend patterns exist only as scattered emails and paper. Management reporting is assembled manually and rarely produced.

### 2.3 Why now

PR volume is seasonal (peak month April with 236 PRs across two years versus 114 in January, a 2.07 times ratio), and the high season from March to August coincides with project ramp-ups, exactly when delays hurt most. Monthly cycle time has stayed between 16.5 and 18.9 days for 24 consecutive months, showing the process will not improve without structural change.

## 3. Objectives

| ID | Objective | Measure (baseline from analysis) |
|---|---|---|
| OBJ-1 | Shorten the PR-to-PO cycle | Average cycle time from 17.5 days to 7.0 days or less |
| OBJ-2 | Make procurement status visible | 100% of PRs trackable by requester in real time |
| OBJ-3 | Bring urgent buying under control | Maverick rate from 12.2% of PRs to 3% or less, with a controlled fast-track lane |
| OBJ-4 | Use vendor performance in decisions | Scorecard published monthly; on-time rate from 85.7% toward a 93% target |
| OBJ-5 | Reduce manual administration | Paper forms, spreadsheet logging, and manual PO typing eliminated |
| OBJ-6 | Give management decision-grade reporting | Monthly spend, cycle time, and compliance dashboard without manual assembly |

## 4. Scope

**In scope**

- PR submission, approval workflow, procurement validation, RFQ and quotation management, PO issuance, goods receipt, and invoice three-way matching for all five sites.
- Vendor master data and vendor performance scorecards.
- KPI dashboard and management reporting.
- Item catalog for the three largest spend categories (Mechanical Equipment 40.3% of spend, Electrical Equipment 18.3%, Services and Subcontracting 17.5%).
- Training and change management for about 120 users.

**Out of scope (this phase)**

- Full ERP replacement or deep ERP integration (kept as a later phase option).
- Inventory optimization and warehouse automation.
- Contract lifecycle management for subcontract agreements.
- Payment execution (finance keeps its existing banking process; the system hands over matched invoices).

## 5. Approach

The analysis followed a standard business analysis flow:

1. **Elicitation.** Interview guides were prepared for the project team, procurement, finance, and warehouse roles (see Elicitation Pack), producing simulated findings and three user personas.
2. **Process analysis.** The current process was mapped in BPMN-style swimlanes (see Process Maps document) and each stage was timed using the dataset.
3. **Data analysis.** A reproducible synthetic dataset of 2,400 PR records was generated (fixed seed 42) and analyzed with Python: stage cycle times, bottlenecks, vendor scorecards, spend concentration, seasonality, and maverick buying (see Analysis Findings Summary).
4. **Requirements.** Findings were converted into numbered business, functional, and non-functional requirements with MoSCoW priorities and acceptance criteria (see Business Requirements Document), and traced through use cases to UAT scenarios (see UAT Plan and Traceability Matrix).
5. **Solution assessment.** Build, buy, and ERP module options were scored on a weighted scorecard (see Build vs Buy Analysis), followed by a Cost-Benefit Analysis, Risk Register, Solution Roadmap, and Change Management and Training Plan.

## 6. Key Findings

All figures are computed from the synthetic dataset; full detail is in `analysis/findings.md`.

**F1. Waiting dominates the cycle.** Vendor Quotation Wait averages 6.02 days (34.4% of the cycle) because RFQs go out by email with no deadline or reminder. The procurement review queue adds 4.04 days (23.1%) and PM approval 3.74 days (21.4%). Both are single-person or invisible-queue waits.

**F2. Maverick buying is a symptom, and an expensive one.** 294 PRs (12.2%) bypass the process. They finish in 1.4 days against 19.7 days for planned purchases, which is why sites use them, but they cost a 10.8% price premium and about Rp 8.37 billion of excess spend over two years.

**F3. Vendor performance is unmanaged.** Scorecard scores range from 86.2 (PT Karya Pipe Nusantara, 95.5% on-time, 8.3 day average lead time) down to 55.4 (CV Wira Consumable Parts, 71.1% on-time, 20.4 day average lead time). Tier C vendors are roughly 2.4 times slower than Tier A, yet order allocation ignores performance entirely.

**F4. Spend is concentrated.** The top three categories hold 76.1% of the Rp 656.10 billion two-year spend, so catalogs and framework agreements for a short list of categories cover most of the value.

**F5. The problem is the process design, not a site.** Average cycle time by site spans only 16.8 to 18.1 days. Every site suffers the same manual design.

## 7. Recommendation

Implement a cloud e-procurement SaaS covering the full PR-to-PO flow, in three phases (detail in the Solution Roadmap):

- **Phase 1 (months 1 to 3): core flow.** Online PR with catalog, digital approval with reminders and delegation, procurement validation queue with SLA timers, status tracking for requesters.
- **Phase 2 (months 4 to 6): sourcing and fulfillment.** RFQ vendor portal with deadlines, quotation comparison matrix, e-PO with e-signature, goods receipt recording, controlled fast-track lane for urgencies.
- **Phase 3 (months 7 to 9): intelligence.** KPI dashboard, vendor scorecards, automatic three-way invoice matching, framework agreement support for the top spend categories.

Design targets (simulation targets, to be validated after go-live): average cycle time 7.0 days or less (stage targets: PM approval 1.0, review queue 1.0, RFQ preparation 0.5, quotation wait 3.0, evaluation and PO issuance 1.5), maverick rate 3% or less, on-time delivery 93%.

## 8. Risks and Constraints (summary)

The largest implementation risks are approver resistance to losing paper signatures, vendor reluctance to use the portal, and low-bandwidth connectivity at remote sites. Mitigations are detailed in the Risk Register, including mobile-friendly approval, a vendor onboarding program with assisted first quotations, and an offline-tolerant design requirement (NFR-04).

## 9. Deliverable Index

| # | Deliverable | Location |
|---|---|---|
| 1 | This case study report | docs/01_case_study_report.md and output/Case_Study_Report.pdf |
| 2 | Process maps and pain points | diagrams/process_as_is.png, diagrams/process_to_be.png, docs/00_process_maps.md |
| 3 | Stakeholder analysis | docs/02_stakeholder_analysis.md |
| 4 | Business Requirements Document | docs/03_business_requirements.md |
| 5 | Data analysis and findings | analysis/run_analysis.py, analysis/findings.md, analysis/charts/ |
| 6 | Gap analysis | docs/04_gap_analysis.md |
| 7 | KPI dashboard prototype | dashboard/kpi_dashboard.html |
| 8 | Workflow prototype | prototype/workflow_prototype.html |
| 9 | Solution roadmap | docs/05_solution_roadmap.md |
| 10 | Elicitation pack | docs/06_elicitation_pack.md |
| 11 | Use cases and user stories | docs/07_use_cases_and_user_stories.md, diagrams/use_case_diagram.png |
| 12 | Data model and data dictionary | docs/08_data_model.md, diagrams/erd.png |
| 13 | Wireframes | wireframes/wireframes.html |
| 14 | Build vs buy analysis | docs/09_build_vs_buy_analysis.md |
| 15 | Cost-benefit analysis | docs/10_cost_benefit_analysis.md |
| 16 | Risk register | docs/11_risk_register.md |
| 17 | UAT plan and traceability matrix | docs/12_uat_plan_and_traceability.md |
| 18 | Change management and training plan | docs/13_change_management_and_training.md |
| 19 | Management deck | output/Management_Deck.pdf |
| 20 | README | README.md |
| 21 | Automated tests | tests/test_dataset_and_kpi.py |
