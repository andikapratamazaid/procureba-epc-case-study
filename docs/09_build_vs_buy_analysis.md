# Build vs Buy Analysis

**ProcureBA, EPC Procurement Digitalization Case Study**
Options assessed: (A) build a custom system in-house, (B) buy a cloud e-procurement SaaS, (C) activate the procurement module of a full ERP. Scores are 1 (poor) to 5 (excellent), assessed for a mid-size EPC contractor with about 120 users, 5 sites, and 1,200 PRs per year.

## 1. Weighted Scorecard

| Criterion | Weight | A. Build in-house | B. Buy SaaS | C. ERP module |
|---|---|---|---|---|
| Functional fit to the BRD | 25% | 5 | 4 | 3 |
| Time to implement | 20% | 2 | 5 | 3 |
| Total cost over 3 years | 20% | 2 | 4 | 3 |
| Scalability (sites, volume) | 15% | 3 | 4 | 4 |
| Vendor support and Indonesian localization | 10% | 2 | 4 | 3 |
| Integration with finance systems | 10% | 3 | 4 | 5 |
| **Weighted total** | **100%** | **3.00** | **4.20** | **3.35** |

Weighted calculation example (Option B): 4 x 0.25 + 5 x 0.20 + 4 x 0.20 + 4 x 0.15 + 4 x 0.10 + 4 x 0.10 = 1.00 + 1.00 + 0.80 + 0.60 + 0.40 + 0.40 = **4.20**.

## 2. Scoring Rationale

**Functional fit.** Build scores 5 because every requirement can be matched exactly, including the fast-track governance rule (FR-08). SaaS scores 4: mainstream e-procurement products cover FR-01 to FR-15, but the post-review flagging of fast-track purchases may need configuration workarounds. The ERP module scores 3: strong on PO and finance, weaker on vendor portal experience and requester tracking.

**Time to implement.** Build scores 2: a realistic 9 to 14 months for a small internal team, which misses the next peak season. SaaS scores 5: configuration-based rollout in the 3-phase, 9-month roadmap with Phase 1 live in month 3. ERP scores 3: module activation is fast, but the surrounding ERP program (chart of accounts, inventory, finance) usually expands the project well beyond procurement.

**Total cost over 3 years.** Build scores 2: development plus permanent maintenance headcount is the most expensive path at this scale, and the cost is the least predictable. SaaS scores 4: the Cost-Benefit Analysis models Rp 0.80 billion one-time plus Rp 0.54 billion per year, the lowest predictable total. ERP scores 3: licensing is moderate, but implementation consulting for a full ERP footprint typically exceeds the procurement-only scope.

**Scalability.** Build scores 3: scalable only as far as the internal team maintains it. SaaS scores 4: adding sites and vendors is configuration. ERP scores 4: equally scalable, with more overhead per change.

**Vendor support and localization.** Build scores 2: support is the internal team itself. SaaS scores 4: Indonesian e-procurement vendors offer Bahasa Indonesia interfaces, IDR handling, and local support hours. ERP scores 3: global products localize well but support is often regional and slower.

**Integration with finance.** ERP scores 5 by definition. SaaS scores 4 via standard APIs for invoice and payment data. Build scores 3 because every integration is custom work.

## 3. Recommendation

**Buy a cloud e-procurement SaaS (Option B, weighted score 4.20).** The deciding factors are time and risk: the business problem is losing about Rp 4.19 billion per year to maverick price premiums alone (analysis estimate), so every quarter of delay costs more than the price differences between options. The SaaS path also keeps the internal IT burden low, which matters for a company whose IT team is small (see Stakeholder Analysis, SH-09).

**Conditions attached to the recommendation**

1. The selected product must demonstrate FR-08 fast-track governance and FR-11 automatic scorecards in a scripted proof of concept using this case study's use cases (UC-01 to UC-11) before contract signing.
2. Data export in open formats must be contractual, to avoid lock-in and to keep the ERP module option (3.35) open as a later consolidation step.
3. The contract must include the NFR-04 low-bandwidth usability requirement as an acceptance item, tested from the most remote site.
