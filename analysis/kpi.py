#!/usr/bin/env python3
"""KPI calculations for the ProcureBA case study.

All functions operate on the record dicts produced by
data/generate_dataset.py (or rows loaded from the generated CSV).
Pure standard library so the analysis and the tests run anywhere.
"""
from datetime import date
from statistics import mean, median


def _d(s):
    return date.fromisoformat(s)


def stage_durations(record):
    """Calendar days spent in each PR-to-PO stage for one record."""
    pr = _d(record["pr_date"])
    pm = _d(record["pm_approval_date"])
    rev = _d(record["procurement_review_date"])
    rfq = _d(record["rfq_sent_date"])
    quo = _d(record["quotation_received_date"])
    po = _d(record["po_date"])
    return {
        "PM Approval": (pm - pr).days,
        "Procurement Review Queue": (rev - pm).days,
        "RFQ Preparation": (rfq - rev).days,
        "Vendor Quotation Wait": (quo - rfq).days,
        "Evaluation and PO Issuance": (po - quo).days,
    }


STAGES = ["PM Approval", "Procurement Review Queue", "RFQ Preparation",
          "Vendor Quotation Wait", "Evaluation and PO Issuance"]


def compute_kpis(records):
    n = len(records)
    cycles = [int(r["cycle_time_days"]) for r in records]
    stage_totals = {s: [] for s in STAGES}
    for r in records:
        sd = stage_durations(r)
        for s in STAGES:
            stage_totals[s].append(sd[s])
    stage_avg = {s: round(mean(v), 2) for s, v in stage_totals.items()}
    total_stage_avg = round(sum(stage_avg.values()), 2)
    stage_share = {s: round(stage_avg[s] / total_stage_avg * 100, 1) for s in STAGES}
    bottleneck = max(stage_avg, key=stage_avg.get)

    maverick = [r for r in records if r["maverick"] == "Yes"]
    normal = [r for r in records if r["maverick"] == "No"]
    urgent = [r for r in records if r["urgent"] == "Yes"]

    def price_ratio(rs):
        return mean(int(r["po_value_idr"]) / int(r["estimated_value_idr"]) for r in rs)

    mav_ratio = price_ratio(maverick)
    norm_ratio = price_ratio(normal)
    premium_pct = round((mav_ratio / norm_ratio - 1) * 100, 1)
    excess_spend = int(sum(int(r["po_value_idr"]) - int(r["estimated_value_idr"]) * norm_ratio
                           for r in maverick))

    total_spend = sum(int(r["po_value_idr"]) for r in records)
    total_est = sum(int(r["estimated_value_idr"]) for r in records)

    spend_by_category = {}
    count_by_category = {}
    cycle_by_category = {}
    for r in records:
        c = r["category"]
        spend_by_category[c] = spend_by_category.get(c, 0) + int(r["po_value_idr"])
        count_by_category[c] = count_by_category.get(c, 0) + 1
        cycle_by_category.setdefault(c, []).append(int(r["cycle_time_days"]))
    cycle_by_category = {c: round(mean(v), 1) for c, v in cycle_by_category.items()}

    spend_by_site = {}
    cycle_by_site = {}
    for r in records:
        s = r["site"]
        spend_by_site[s] = spend_by_site.get(s, 0) + int(r["po_value_idr"])
        cycle_by_site.setdefault(s, []).append(int(r["cycle_time_days"]))
    cycle_by_site = {s: round(mean(v), 1) for s, v in cycle_by_site.items()}

    # vendor scorecard: transactions, spend, avg lead time, on-time rate, score
    vendors = {}
    for r in records:
        v = vendors.setdefault(r["vendor"], {"vendor": r["vendor"], "tier": r["vendor_tier"],
                                             "transactions": 0, "spend": 0, "lead": [], "on_time": 0})
        v["transactions"] += 1
        v["spend"] += int(r["po_value_idr"])
        v["lead"].append(int(r["actual_lead_time_days"]))
        if r["on_time"] == "Yes":
            v["on_time"] += 1
    scorecard = []
    for v in vendors.values():
        otr = v["on_time"] / v["transactions"]
        avg_lead = mean(v["lead"])
        # score: 60% on-time reliability, 40% lead time speed (30 days = 0 points)
        score = round(0.6 * otr * 100 + 0.4 * max(0.0, (30 - avg_lead) / 30) * 100, 1)
        scorecard.append({
            "vendor": v["vendor"], "tier": v["tier"], "transactions": v["transactions"],
            "spend_idr": v["spend"], "avg_lead_time_days": round(avg_lead, 1),
            "on_time_rate_pct": round(otr * 100, 1), "score": score,
        })
    scorecard.sort(key=lambda x: x["score"], reverse=True)

    on_time_all = round(sum(1 for r in records if r["on_time"] == "Yes") / n * 100, 1)
    avg_lead_all = round(mean(int(r["actual_lead_time_days"]) for r in records), 1)

    # seasonality: PR count and spend by calendar month (both years combined)
    monthly_count = {m: 0 for m in range(1, 13)}
    monthly_spend = {m: 0 for m in range(1, 13)}
    ym_count = {}
    ym_cycle = {}
    for r in records:
        d = _d(r["pr_date"])
        monthly_count[d.month] += 1
        monthly_spend[d.month] += int(r["po_value_idr"])
        key = f"{d.year:04d}-{d.month:02d}"
        ym_count[key] = ym_count.get(key, 0) + 1
        ym_cycle.setdefault(key, []).append(int(r["cycle_time_days"]))
    ym_cycle_avg = {k: round(mean(v), 1) for k, v in sorted(ym_cycle.items())}
    peak_month = max(monthly_count, key=monthly_count.get)
    low_month = min(monthly_count, key=monthly_count.get)

    return {
        "record_count": n,
        "date_range": [records[0]["pr_date"] if records else None,
                       max(r["pr_date"] for r in records) if records else None],
        "total_spend_idr": total_spend,
        "total_estimated_idr": total_est,
        "avg_po_value_idr": int(round(total_spend / n)) if n else 0,
        "cycle_time_avg_days": round(mean(cycles), 1),
        "cycle_time_median_days": round(median(cycles), 1),
        "cycle_time_max_days": max(cycles),
        "cycle_time_p90_days": sorted(cycles)[int(0.9 * n)],
        "stage_avg_days": stage_avg,
        "stage_share_pct": stage_share,
        "bottleneck_stage": bottleneck,
        "urgent_count": len(urgent),
        "urgent_rate_pct": round(len(urgent) / n * 100, 1),
        "maverick_count": len(maverick),
        "maverick_rate_pct": round(len(maverick) / n * 100, 1),
        "maverick_spend_idr": sum(int(r["po_value_idr"]) for r in maverick),
        "maverick_spend_share_pct": round(sum(int(r["po_value_idr"]) for r in maverick) / total_spend * 100, 1),
        "maverick_price_premium_pct": premium_pct,
        "maverick_excess_spend_idr": excess_spend,
        "maverick_avg_cycle_days": round(mean(int(r["cycle_time_days"]) for r in maverick), 1),
        "normal_avg_cycle_days": round(mean(int(r["cycle_time_days"]) for r in normal), 1),
        "on_time_rate_pct": on_time_all,
        "avg_actual_lead_time_days": avg_lead_all,
        "spend_by_category_idr": dict(sorted(spend_by_category.items(), key=lambda kv: -kv[1])),
        "count_by_category": count_by_category,
        "cycle_by_category_days": cycle_by_category,
        "spend_by_site_idr": spend_by_site,
        "cycle_by_site_days": cycle_by_site,
        "vendor_scorecard": scorecard,
        "monthly_pr_count": {str(m): monthly_count[m] for m in range(1, 13)},
        "monthly_spend_idr": {str(m): monthly_spend[m] for m in range(1, 13)},
        "year_month_cycle_avg_days": ym_cycle_avg,
        "peak_month": peak_month,
        "peak_month_count": monthly_count[peak_month],
        "low_month": low_month,
        "low_month_count": monthly_count[low_month],
    }
