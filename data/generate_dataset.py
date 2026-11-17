#!/usr/bin/env python3
"""Synthetic EPC procurement dataset generator.

ProcureBA case study: generates 2,400 purchase requisition (PR) records
across 2 years (2024-2025) and 5 project sites for a fictional mid-size
EPC company. The data is fully synthetic and modeled on typical EPC
procurement process patterns (manual PR handling, approval queues,
RFQ cycles, vendor lead times, maverick urgent buying).

Reproducibility: a fixed seed (default 42) always produces the same
dataset. Run directly to write procurement_data.csv next to this file.
"""
import csv
import os
import random
from datetime import date, timedelta

SEED = 42
RECORD_COUNT = 2400
START_DATE = date(2024, 1, 2)
DAYS_SPAN = 729  # 2024-01-02 .. 2025-12-31

SITES = [
    "Site Alpha - Industrial Plant",
    "Site Beta - Infrastructure",
    "Site Gamma - Power Plant",
    "Site Delta - Mining Facility",
    "Site Epsilon - Water Treatment",
]

# site factor slows approvals slightly on remote sites
SITE_APPROVAL_FACTOR = {
    "Site Alpha - Industrial Plant": 1.00,
    "Site Beta - Infrastructure": 1.10,
    "Site Gamma - Power Plant": 1.05,
    "Site Delta - Mining Facility": 1.25,
    "Site Epsilon - Water Treatment": 1.15,
}

CATEGORIES = [
    "Mechanical Equipment",
    "Electrical Equipment",
    "Piping and Fittings",
    "Civil Materials",
    "Instrumentation",
    "Consumables and MRO",
    "Services and Subcontracting",
    "IT and Office Supplies",
]

CATEGORY_WEIGHTS = [0.16, 0.13, 0.16, 0.14, 0.09, 0.15, 0.10, 0.07]

# estimated value range per category (IDR)
CATEGORY_VALUE_RANGE = {
    "Mechanical Equipment": (150_000_000, 2_400_000_000),
    "Electrical Equipment": (60_000_000, 1_500_000_000),
    "Piping and Fittings": (25_000_000, 700_000_000),
    "Civil Materials": (15_000_000, 500_000_000),
    "Instrumentation": (40_000_000, 900_000_000),
    "Consumables and MRO": (2_000_000, 120_000_000),
    "Services and Subcontracting": (80_000_000, 1_800_000_000),
    "IT and Office Supplies": (3_000_000, 150_000_000),
}

# vendor pool: name, tier (lead time profile), price factor, on-time base rate
VENDORS = [
    ("PT Sumber Teknik Abadi", "A", 0.99, 0.94),
    ("PT Karya Pipe Nusantara", "A", 1.00, 0.92),
    ("CV Maju Bersama Steel", "B", 1.01, 0.85),
    ("PT Elektro Prima Indonesia", "A", 0.98, 0.93),
    ("PT Global Instrumentindo", "B", 1.02, 0.84),
    ("PT Bangun Cipta Material", "B", 1.00, 0.86),
    ("CV Sinar Logistik", "C", 1.04, 0.72),
    ("PT Delta Valve Sejahtera", "B", 1.01, 0.83),
    ("PT Omega Cable Works", "A", 0.99, 0.91),
    ("CV Berkah Consumables", "C", 1.03, 0.75),
    ("PT Triputra Engineering Supply", "B", 1.02, 0.82),
    ("PT Nusantara Crane Services", "B", 1.01, 0.85),
    ("CV Tunas Office Station", "C", 1.02, 0.78),
    ("PT Harapan Pipa Industrial", "A", 1.00, 0.90),
    ("PT Sentosa Control System", "B", 1.03, 0.81),
    ("CV Wira Consumable Parts", "C", 1.05, 0.70),
    ("PT Mega Structure Material", "B", 1.00, 0.84),
    ("PT Artha Jasa Kontraktor", "B", 1.01, 0.86),
]

TIER_LEAD_TIME = {  # (min days, max days) promised lead time
    "A": (5, 14),
    "B": (8, 21),
    "C": (10, 30),
}

REQUESTER_ROLES = ["Site Engineer", "Construction Supervisor", "QA/QC Inspector",
                   "Warehouse Staff", "Maintenance Technician", "Project Admin"]


def _stage_days(rng, mean, spread=0.55):
    """Positive stage duration in whole days, roughly lognormal around mean."""
    val = rng.lognormvariate(0.0, spread) * mean / 1.16
    return max(0, int(round(val)))


def generate(seed=SEED, count=RECORD_COUNT):
    rng = random.Random(seed)
    vendors_by_cat = {}
    for cat in CATEGORIES:
        vendors_by_cat[cat] = VENDORS  # all vendors can serve, weighted by tier below

    records = []
    for i in range(count):
        # seasonality: more PRs in project ramp-up months (Mar-Aug), fewer in Dec-Jan
        while True:
            day_offset = rng.randrange(DAYS_SPAN)
            d = START_DATE + timedelta(days=day_offset)
            month_weight = {1: 0.55, 2: 0.75, 3: 1.05, 4: 1.15, 5: 1.2, 6: 1.2,
                            7: 1.15, 8: 1.1, 9: 1.0, 10: 0.95, 11: 0.85, 12: 0.6}[d.month]
            if rng.random() < month_weight:
                break

        site = rng.choices(SITES, weights=[0.24, 0.22, 0.20, 0.18, 0.16])[0]
        category = rng.choices(CATEGORIES, weights=CATEGORY_WEIGHTS)[0]
        lo, hi = CATEGORY_VALUE_RANGE[category]
        est_value = int(rng.lognormvariate(0, 0.6) * ((lo * hi) ** 0.5))
        est_value = max(lo // 2, min(hi, est_value))

        urgent = rng.random() < 0.21
        maverick = urgent and rng.random() < 0.62  # most urgent buys bypass procedure

        # vendor choice: tier A slightly preferred for planned purchases
        tier_weights = {"A": 0.40, "B": 0.38, "C": 0.22} if not maverick else {"A": 0.25, "B": 0.35, "C": 0.40}
        pool = [v for v in vendors_by_cat[category]]
        weights = [tier_weights[v[1]] / sum(1 for x in pool if x[1] == v[1]) for v in pool]
        vendor = rng.choices(pool, weights=weights)[0]
        vname, tier, price_factor, ontime_base = vendor

        factor = SITE_APPROVAL_FACTOR[site]
        if maverick:
            d_pm = _stage_days(rng, 0.8)
            d_review = 0
            d_rfq = 0  # no RFQ stage: direct purchase
            d_quote = 0
            d_eval = _stage_days(rng, 0.7)
            premium = rng.uniform(1.06, 1.16)
        else:
            d_pm = _stage_days(rng, 3.8 * factor)
            d_review = _stage_days(rng, 4.6)          # procurement queue bottleneck
            d_rfq = _stage_days(rng, 1.2)
            d_quote = _stage_days(rng, 6.8)           # waiting for vendor quotations
            d_eval = _stage_days(rng, 2.9)
            premium = rng.uniform(0.99, 1.03)

        po_value = int(est_value * price_factor * premium)
        lt_lo, lt_hi = TIER_LEAD_TIME[tier]
        promised_lt = rng.randint(lt_lo, lt_hi)
        on_time = rng.random() < ontime_base
        if on_time:
            actual_lt = max(1, promised_lt - rng.randint(0, 3))
        else:
            actual_lt = promised_lt + rng.randint(1, 12)

        pr_date = d
        pm_date = pr_date + timedelta(days=d_pm)
        review_date = pm_date + timedelta(days=d_review)
        rfq_date = review_date + timedelta(days=d_rfq)
        quote_date = rfq_date + timedelta(days=d_quote)
        po_date = quote_date + timedelta(days=d_eval)
        gr_date = po_date + timedelta(days=actual_lt)

        records.append({
            "pr_id": f"PR-{i + 1:05d}",
            "pr_date": pr_date.isoformat(),
            "site": site,
            "requester_role": rng.choice(REQUESTER_ROLES),
            "category": category,
            "estimated_value_idr": est_value,
            "urgent": "Yes" if urgent else "No",
            "maverick": "Yes" if maverick else "No",
            "pm_approval_date": pm_date.isoformat(),
            "procurement_review_date": review_date.isoformat(),
            "rfq_sent_date": rfq_date.isoformat(),
            "quotation_received_date": quote_date.isoformat(),
            "po_date": po_date.isoformat(),
            "po_value_idr": po_value,
            "vendor": vname,
            "vendor_tier": tier,
            "promised_lead_time_days": promised_lt,
            "goods_receipt_date": gr_date.isoformat(),
            "actual_lead_time_days": actual_lt,
            "on_time": "Yes" if on_time else "No",
            "cycle_time_days": (po_date - pr_date).days,
        })

    records.sort(key=lambda r: r["pr_date"])
    for idx, r in enumerate(records, start=1):
        r["pr_id"] = f"PR-{idx:05d}"
    return records


def main():
    records = generate()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "procurement_data.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} records to {out}")


if __name__ == "__main__":
    main()
