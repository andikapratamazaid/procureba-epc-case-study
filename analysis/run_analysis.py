#!/usr/bin/env python3
"""Run the ProcureBA analysis: generate (if needed) the synthetic dataset,
compute KPIs, save analysis_results.json, and render all charts as PNG.

Usage: python3 run_analysis.py
Outputs:
  ../data/procurement_data.csv      (generated if missing)
  output/analysis_results.json
  charts/*.png
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "data"))
sys.path.insert(0, HERE)

import generate_dataset  # noqa: E402
from kpi import compute_kpis, STAGES  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY = "#16324f"
STEEL = "#4a6fa5"
LIGHT = "#9db6cf"
ACCENT = "#c05621"
GREEN = "#2f855a"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_records():
    csv_path = os.path.join(ROOT, "data", "procurement_data.csv")
    if not os.path.exists(csv_path):
        generate_dataset.main()
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_chart(fig, name):
    out = os.path.join(HERE, "charts", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print("chart:", out)


def main():
    records = load_records()
    kpis = compute_kpis(records)

    out_json = os.path.join(ROOT, "output", "analysis_results.json")
    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(kpis, f, indent=2, ensure_ascii=False)
    print("results:", out_json)

    # 1. Average days per stage
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    vals = [kpis["stage_avg_days"][s] for s in STAGES]
    colors = [ACCENT if s == kpis["bottleneck_stage"] else STEEL for s in STAGES]
    ax.barh(STAGES[::-1], vals[::-1], color=colors[::-1])
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.15, i, f"{v:.2f} days", va="center", fontsize=9)
    ax.set_xlabel("Average calendar days per PR")
    ax.set_title("Average PR-to-PO Cycle Time by Stage (synthetic data, n=2,400)")
    ax.set_xlim(0, max(vals) * 1.25)
    save_chart(fig, "cycle_time_by_stage.png")

    # 2. Monthly cycle time trend (year-month)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    keys = list(kpis["year_month_cycle_avg_days"].keys())
    ax.plot(keys, [kpis["year_month_cycle_avg_days"][k] for k in keys],
            color=NAVY, marker="o", markersize=3.5, linewidth=1.6)
    ax.axhline(kpis["cycle_time_avg_days"], color=ACCENT, linestyle="--",
               label=f"Overall average {kpis['cycle_time_avg_days']} days")
    ax.set_ylabel("Average cycle time (days)")
    ax.set_title("Average PR-to-PO Cycle Time by Month, 2024-2025")
    plt.setp(ax.get_xticklabels(), rotation=60, ha="left", fontsize=8)
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    save_chart(fig, "cycle_time_trend.png")

    # 3. Spend by category
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    cats = list(kpis["spend_by_category_idr"].keys())
    vals = [kpis["spend_by_category_idr"][c] / 1e12 for c in cats]
    ax.barh(cats[::-1], vals[::-1], color=STEEL)
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 0.06, i, f"Rp {v:.2f} T", va="center", fontsize=9)
    ax.set_xlabel("Total PO value 2024-2025 (Rp trillion)")
    ax.set_title("Procurement Spend by Category (synthetic data)")
    ax.set_xlim(0, max(vals) * 1.22)
    save_chart(fig, "spend_by_category.png")

    # 4. Seasonality: PR count by calendar month
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    counts = [kpis["monthly_pr_count"][str(m)] for m in range(1, 13)]
    ax.bar(MONTH_NAMES, counts, color=LIGHT, edgecolor=NAVY)
    ax.set_ylabel("PR count (2024 + 2025 combined)")
    ax.set_title("Seasonality: Purchase Requisitions by Calendar Month")
    save_chart(fig, "seasonality_pr_by_month.png")

    # 5. Vendor scorecard: on-time rate of top 10 vendors by transactions
    top = sorted(kpis["vendor_scorecard"], key=lambda v: -v["transactions"])[:10]
    top = sorted(top, key=lambda v: v["on_time_rate_pct"])
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.barh([v["vendor"] for v in top], [v["on_time_rate_pct"] for v in top], color=GREEN)
    for i, v in enumerate(top):
        ax.text(v["on_time_rate_pct"] + 1, i, f"{v['on_time_rate_pct']:.1f}%", va="center", fontsize=8.5)
    ax.set_xlabel("On-time delivery rate (%)")
    ax.set_title("Vendor On-Time Delivery Rate, Top 10 Vendors by Transaction Count")
    ax.set_xlim(0, 112)
    save_chart(fig, "vendor_ontime_top10.png")

    # 6. Maverick vs normal: cycle time and price premium
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0))
    axes[0].bar(["Planned", "Maverick"], [kpis["normal_avg_cycle_days"], kpis["maverick_avg_cycle_days"]],
                color=[STEEL, ACCENT])
    axes[0].set_ylabel("Average cycle time (days)")
    axes[0].set_title("Cycle time: planned vs maverick")
    axes[1].bar(["Share of PRs", "Share of spend"],
                [kpis["maverick_rate_pct"], kpis["maverick_spend_share_pct"]], color=[ACCENT, ACCENT])
    axes[1].set_ylabel("%")
    axes[1].set_title("Maverick buying share")
    save_chart(fig, "maverick_analysis.png")

    print(json.dumps({k: kpis[k] for k in [
        "record_count", "cycle_time_avg_days", "cycle_time_median_days", "cycle_time_p90_days",
        "bottleneck_stage", "maverick_rate_pct", "maverick_price_premium_pct",
        "on_time_rate_pct", "total_spend_idr"]}, indent=2))


if __name__ == "__main__":
    main()
