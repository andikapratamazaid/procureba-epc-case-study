# Analysis Findings Summary

**ProcureBA, EPC Procurement Digitalization Case Study**
Data: synthetic dataset of 2,400 purchase requisitions, 2 January 2024 to 30 December 2025, 5 project sites, 18 vendors. Generated with fixed seed 42 by `data/generate_dataset.py`. All figures below are computed by `analysis/run_analysis.py` and stored in `output/analysis_results.json`. Every number quoted in the case study documents comes from this file.

> Important: this is a fictional case study. The data is synthetic and modeled on typical EPC procurement process patterns. It does not describe any real company.

## Headline figures

| Metric | Value |
|---|---|
| PR records analyzed | 2,400 |
| Period | 2024-01-02 to 2025-12-30 |
| Total PO spend (2 years) | Rp 656,098,070,818 (Rp 656.10 billion) |
| Total estimated value (2 years) | Rp 635,495,232,327 (Rp 635.50 billion) |
| Average PO value | Rp 273,374,196 |
| Average PR-to-PO cycle time | 17.5 days |
| Median cycle time | 18.0 days |
| 90th percentile cycle time | 27 days |
| Maximum cycle time | 57 days |
| Overall on-time delivery rate | 85.7% |
| Average actual vendor lead time | 13.6 days |

## Finding 1: The cycle time problem is mostly waiting, and the biggest wait is vendor quotations

| Stage | Avg days | Share of cycle |
|---|---|---|
| Vendor Quotation Wait | 6.02 | 34.4% |
| Procurement Review Queue | 4.04 | 23.1% |
| PM Approval | 3.74 | 21.4% |
| Evaluation and PO Issuance | 2.59 | 14.8% |
| RFQ Preparation | 1.09 | 6.2% |

The bottleneck stage is Vendor Quotation Wait at 6.02 days (34.4% of the total cycle). RFQs are sent by email with no deadline and no reminder, so quotations arrive whenever vendors are ready. The two internal approval stages (PM Approval and Procurement Review Queue) add 7.78 days together (44.5% of the cycle) and are pure waiting time: the paper file sits with one approver or in an invisible queue. In total, 65.6% of the cycle is internal process time that a digital workflow can compress directly.

## Finding 2: Maverick buying is a rational response to a slow process, and it is expensive

- Urgent PRs: 504 of 2,400 (21.0%).
- Maverick (off-procedure) PRs: 294 of 2,400 (12.2%), worth Rp 89,442,194,613, which is 13.6% of total spend.
- Maverick purchases complete in 1.4 days on average versus 19.7 days for planned purchases, which explains why requesters bypass the process.
- Maverick purchases carry a 10.8% price premium over planned purchasing patterns, producing an estimated excess spend of Rp 8,374,710,381 over two years, about Rp 4.19 billion per year.

## Finding 3: Vendor performance varies widely and is not used in selection

- Best vendor score: PT Karya Pipe Nusantara, 86.2 (on-time 95.5%, average lead time 8.3 days, 176 transactions).
- Largest vendor by spend: PT Sumber Teknik Abadi, Rp 58,659,062,400, score 85.9 (on-time 96.1%).
- Weakest vendor score: CV Wira Consumable Parts, 55.4 (on-time 71.1%, average lead time 20.4 days, 159 transactions), yet it still receives a large transaction volume.
- Tier A vendors deliver on time 91.1% to 96.1% of the time. Tier C vendors deliver on time only 71.1% to 79.2% of the time, with average lead times around 20 days, roughly 2.4 times slower than Tier A.
- Because there is no scorecard, low-performing vendors keep receiving orders at the same rate as high performers.

## Finding 4: Spend is concentrated, which makes standardization valuable

| Category | Spend (Rp) | Share |
|---|---|---|
| Mechanical Equipment | 264,532,306,157 | 40.3% |
| Electrical Equipment | 120,019,899,420 | 18.3% |
| Services and Subcontracting | 114,954,073,498 | 17.5% |
| Piping and Fittings | 58,112,039,945 | 8.9% |
| Instrumentation | 52,673,649,675 | 8.0% |
| Civil Materials | 34,438,196,396 | 5.3% |
| Consumables and MRO | 6,816,452,394 | 1.0% |
| IT and Office Supplies | 4,551,453,333 | 0.7% |

The top three categories hold 76.1% of spend. Catalog standardization and framework agreements for these categories would cover most of the value flowing through the process.

## Finding 5: Demand is seasonal, but staffing of the review queue is flat

- Peak month: April, 236 PRs across the two years. Low month: January, 114 PRs. Peak demand is 2.07 times low demand.
- The high season runs from March to August, matching project ramp-up periods.
- Monthly average cycle time ranged only between 16.5 and 18.9 days across 24 months: the process does not improve over time, and it does not collapse in peak season either, because requesters route around it through maverick buying.

## Finding 6: Cycle time is consistent across sites, so the problem is the process, not one site

Average cycle time by site ranges from 16.8 days (Site Delta, Mining Facility) to 18.1 days (Site Beta, Infrastructure). The narrow spread shows the delay is built into the shared manual process design, not caused by a single underperforming site.

## Charts

- `charts/cycle_time_by_stage.png`: average days per stage, bottleneck highlighted.
- `charts/cycle_time_trend.png`: monthly average cycle time, 2024 to 2025.
- `charts/spend_by_category.png`: spend by category.
- `charts/seasonality_pr_by_month.png`: PR volume by calendar month.
- `charts/vendor_ontime_top10.png`: on-time rate of the 10 busiest vendors.
- `charts/maverick_analysis.png`: planned versus maverick cycle time and maverick share.
