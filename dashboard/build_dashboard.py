#!/usr/bin/env python3
"""Build the self-contained KPI dashboard HTML from analysis_results.json.
Before figures come from the analysis; after figures are labeled simulation
targets from the BRD and roadmap. Charts are embedded as base64 so the file
opens standalone offline.
"""
import base64
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with open(os.path.join(ROOT, "output", "analysis_results.json"), encoding="utf-8") as f:
    K = json.load(f)


def img64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def rp(v):
    return "Rp " + f"{v:,}".replace(",", ".")


CH = {name: img64(os.path.join(ROOT, "analysis", "charts", name + ".png"))
      for name in ["cycle_time_by_stage", "spend_by_category", "vendor_ontime_top10", "maverick_analysis"]}

stage_rows = ""
targets = {"PM Approval": 1.0, "Procurement Review Queue": 1.0, "RFQ Preparation": 0.5,
           "Vendor Quotation Wait": 3.0, "Evaluation and PO Issuance": 1.5}
for s, v in K["stage_avg_days"].items():
    stage_rows += (f"<tr><td>{s}</td><td>{v:.2f} days</td><td>{K['stage_share_pct'][s]}%</td>"
                   f"<td class='target'>{targets[s]:.1f} days</td></tr>")

sc = K["vendor_scorecard"]
vendor_rows = ""
for v in sc[:5] + sc[-3:]:
    cls = "good" if v["score"] >= 80 else ("mid" if v["score"] >= 65 else "bad")
    vendor_rows += (f"<tr><td>{v['vendor']}</td><td>{v['tier']}</td><td>{v['transactions']}</td>"
                    f"<td>{rp(v['spend_idr'])}</td><td>{v['avg_lead_time_days']} days</td>"
                    f"<td>{v['on_time_rate_pct']}%</td><td><span class='badge {cls}'>{v['score']}</span></td></tr>")

cat_rows = ""
total = K["total_spend_idr"]
for c, v in K["spend_by_category_idr"].items():
    cat_rows += f"<tr><td>{c}</td><td>{K['count_by_category'][c]}</td><td>{rp(v)}</td><td>{round(v/total*100,1)}%</td><td>{K['cycle_by_category_days'][c]} days</td></tr>"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ProcureBA KPI Dashboard (Case Study Prototype)</title>
<style>
  body {{ font-family: "Segoe UI", Arial, sans-serif; margin: 0; background: #eef2f6; color: #1c2b39; }}
  header {{ background: #16324f; color: #fff; padding: 18px 28px; }}
  header h1 {{ margin: 0; font-size: 22px; }}
  header p {{ margin: 4px 0 0; font-size: 13px; opacity: .85; }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 20px; }}
  .note {{ background: #fff7e8; border: 1px solid #e3c98a; border-radius: 8px; padding: 10px 14px; font-size: 13px; }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin: 18px 0; }}
  .card {{ background: #fff; border-radius: 10px; padding: 14px 16px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .card .label {{ font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: #5a6b7a; }}
  .card .before {{ font-size: 26px; font-weight: 700; color: #16324f; }}
  .card .after {{ font-size: 14px; color: #2f855a; font-weight: 600; }}
  .panel {{ background: #fff; border-radius: 10px; padding: 18px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .panel h2 {{ margin-top: 0; font-size: 17px; color: #16324f; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
  th, td {{ padding: 7px 9px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
  th {{ background: #f2f6fa; color: #16324f; }}
  td.target {{ color: #2f855a; font-weight: 600; }}
  .badge {{ padding: 2px 9px; border-radius: 10px; color: #fff; font-weight: 600; }}
  .badge.good {{ background: #2f855a; }} .badge.mid {{ background: #b7791f; }} .badge.bad {{ background: #c53030; }}
  img.chart {{ width: 100%; border: 1px solid #e2e8f0; border-radius: 6px; }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  @media (max-width: 860px) {{ .grid2 {{ grid-template-columns: 1fr; }} }}
  footer {{ text-align: center; color: #718096; font-size: 12px; padding: 14px; }}
</style>
</head>
<body>
<header>
  <h1>ProcureBA: Procurement KPI Dashboard</h1>
  <p>Business Analysis Case Study Prototype | Baseline period: January 2024 to December 2025 | 2,400 PR records, 5 sites</p>
</header>
<div class="wrap">
  <div class="note"><strong>How to read this dashboard:</strong> "Before" figures are computed from the case study synthetic dataset (fixed seed, reproducible, see the analysis folder). "After" figures are <strong>simulation targets</strong> from the BRD and Solution Roadmap, not measured results. This company and its data are fictional.</div>

  <div class="cards">
    <div class="card"><div class="label">Avg PR-to-PO cycle time</div><div class="before">{K['cycle_time_avg_days']} days</div><div class="after">Target: 7.0 days or less</div></div>
    <div class="card"><div class="label">Median / P90 cycle time</div><div class="before">{K['cycle_time_median_days']} / {K['cycle_time_p90_days']} days</div><div class="after">Target P90: 12 days</div></div>
    <div class="card"><div class="label">Maverick purchase rate</div><div class="before">{K['maverick_rate_pct']}% of PRs</div><div class="after">Target: 3% or less</div></div>
    <div class="card"><div class="label">Maverick price premium</div><div class="before">+{K['maverick_price_premium_pct']}%</div><div class="after">Excess spend: {rp(K['maverick_excess_spend_idr'])} in 2 years</div></div>
    <div class="card"><div class="label">Vendor on-time delivery</div><div class="before">{K['on_time_rate_pct']}%</div><div class="after">Target: 93%</div></div>
    <div class="card"><div class="label">Total spend (2 years)</div><div class="before">{rp(K['total_spend_idr'])}</div><div class="after">Avg PO value: {rp(K['avg_po_value_idr'])}</div></div>
  </div>

  <div class="panel">
    <h2>Cycle Time by Stage: Before vs Target</h2>
    <table><tr><th>Stage</th><th>Before (avg)</th><th>Share</th><th>After (simulation target)</th></tr>
    {stage_rows}
    <tr><td><strong>Total</strong></td><td><strong>{K['cycle_time_avg_days']} days</strong></td><td><strong>100%</strong></td><td class="target"><strong>7.0 days</strong></td></tr></table>
    <p style="font-size:13px;color:#5a6b7a">Bottleneck stage: <strong>{K['bottleneck_stage']}</strong> at {K['stage_avg_days'][K['bottleneck_stage']]:.2f} days ({K['stage_share_pct'][K['bottleneck_stage']]}% of the cycle). RFQs are sent by email with no deadline or reminder.</p>
    <img class="chart" src="{CH['cycle_time_by_stage']}" alt="Cycle time by stage chart">
  </div>

  <div class="grid2">
    <div class="panel"><h2>Spend by Category</h2><img class="chart" src="{CH['spend_by_category']}" alt="Spend by category chart"></div>
    <div class="panel"><h2>Maverick Buying Analysis</h2><img class="chart" src="{CH['maverick_analysis']}" alt="Maverick analysis chart">
    <p style="font-size:13px;color:#5a6b7a">Maverick PRs finish in {K['maverick_avg_cycle_days']} days versus {K['normal_avg_cycle_days']} days for planned purchases, which is why sites bypass the process. The fix is a controlled fast-track lane, not a ban.</p></div>
  </div>

  <div class="panel">
    <h2>Spend Detail by Category</h2>
    <table><tr><th>Category</th><th>PR count</th><th>Spend</th><th>Share</th><th>Avg cycle</th></tr>{cat_rows}</table>
  </div>

  <div class="panel">
    <h2>Vendor Scorecard (top 5 and bottom 3 of 18 vendors)</h2>
    <img class="chart" src="{CH['vendor_ontime_top10']}" alt="Vendor on-time chart">
    <table style="margin-top:12px"><tr><th>Vendor</th><th>Tier</th><th>Transactions</th><th>Spend</th><th>Avg lead time</th><th>On-time</th><th>Score</th></tr>
    {vendor_rows}</table>
    <p style="font-size:13px;color:#5a6b7a">Score formula: 60% on-time reliability plus 40% lead time speed. In the as-is process this data is never recorded, so the weakest vendor (score {sc[-1]['score']}, on-time {sc[-1]['on_time_rate_pct']}%) receives the same treatment as the best (score {sc[0]['score']}, on-time {sc[0]['on_time_rate_pct']}%).</p>
  </div>
</div>
<footer>ProcureBA case study prototype. Fictional company, synthetic data, simulation targets labeled as such. Built with plain HTML, CSS, and embedded charts. No external dependencies.</footer>
</body>
</html>"""

out = os.path.join(HERE, "kpi_dashboard.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("Wrote", out, f"({len(html)//1024} KB)")
