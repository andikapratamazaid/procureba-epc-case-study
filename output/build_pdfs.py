#!/usr/bin/env python3
"""Build the two ProcureBA PDFs with reportlab:
1. Case_Study_Report.pdf (portrait, from the case study content)
2. Management_Deck.pdf (landscape slides)
All figures come from output/analysis_results.json.
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
with open(os.path.join(HERE, "analysis_results.json"), encoding="utf-8") as f:
    K = json.load(f)

NAVY = colors.HexColor("#16324f")
STEEL = colors.HexColor("#4a6fa5")
ACCENT = colors.HexColor("#c05621")
LIGHTBG = colors.HexColor("#eef2f6")


def rp(v):
    return "Rp " + f"{v:,}".replace(",", ".")


def rp_b(v):
    return f"Rp {v/1e9:.2f} billion"


ss = getSampleStyleSheet()
TITLE = ParagraphStyle("title2", parent=ss["Title"], fontSize=24, leading=30, textColor=NAVY)
SUB = ParagraphStyle("sub", parent=ss["Normal"], fontSize=13, leading=17, alignment=TA_CENTER, textColor=STEEL)
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, leading=19, textColor=NAVY, spaceBefore=14)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=10)
BODY = ParagraphStyle("body", parent=ss["Normal"], fontSize=10.5, leading=15, alignment=TA_JUSTIFY)
BULLET = ParagraphStyle("bullet", parent=BODY, leftIndent=14, bulletIndent=4, spaceAfter=4)
SMALL = ParagraphStyle("small", parent=ss["Normal"], fontSize=9, leading=12.5, textColor=colors.HexColor("#555555"))
CELL = ParagraphStyle("cell", parent=ss["Normal"], fontSize=9.5, leading=12.5)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)


def styled_table(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b9c6d2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), NAVY)]
    t.setStyle(TableStyle(style))
    return t


def hdr(cells):
    return [Paragraph(c, CELLB) for c in cells]


def row(cells):
    return [Paragraph(str(c), CELL) for c in cells]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(15 * mm, 10 * mm, "ProcureBA Case Study. Fictional company, synthetic data (seed 42), simulation targets labeled.")
    canvas.drawRightString(A4[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------- report
def build_report():
    path = os.path.join(HERE, "Case_Study_Report.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title="ProcureBA Case Study Report", author="Andika Pratama Zaid")
    E = []
    E.append(Spacer(1, 22 * mm))
    E.append(Paragraph("ProcureBA", ParagraphStyle("brand", parent=TITLE, fontSize=30, leading=34)))
    E.append(Paragraph("EPC Procurement Digitalization", TITLE))
    E.append(Paragraph("A Business Analysis Case Study", SUB))
    E.append(Spacer(1, 8 * mm))
    E.append(Paragraph("Case Study Report", ParagraphStyle("cs", parent=SUB, fontSize=15)))
    E.append(Spacer(1, 16 * mm))
    E.append(Paragraph(
        "Honest labeling: this is a fictional case study created for professional portfolio purposes. "
        "The company, people, and transactions are not real. The dataset is synthetic (2,400 purchase "
        "requisition records generated with a fixed random seed) and modeled on typical EPC procurement "
        "process patterns. All analysis figures are real outputs computed from that synthetic dataset "
        "by the Python code in the project repository, so every number in this report can be reproduced.",
        ParagraphStyle("note", parent=BODY, backColor=LIGHTBG, borderPadding=10)))
    E.append(Spacer(1, 10 * mm))
    E.append(Paragraph("Author: Andika Pratama Zaid, Business Analyst", SUB))
    E.append(PageBreak())

    E.append(Paragraph("1. Executive Summary", H1))
    E.append(Paragraph(
        f"A fictional mid-size EPC contractor runs procurement for five project sites through a fully manual "
        f"process: paper purchase requisition (PR) forms, wet signatures, email-based RFQs, and spreadsheet "
        f"tracking. The Company processes about 1,200 PRs per year, with a two-year procurement spend of "
        f"{rp_b(K['total_spend_idr'])} in the synthetic dataset.", BODY))
    E.append(Paragraph(
        f"Analysis of {K['record_count']:,} PR records from January 2024 to December 2025 shows three structural "
        f"problems. First, slow cycle time: the average PR-to-PO cycle is {K['cycle_time_avg_days']} days "
        f"(median {K['cycle_time_median_days']} days, 90th percentile {K['cycle_time_p90_days']} days). Second, "
        f"maverick buying: {K['maverick_count']} PRs ({K['maverick_rate_pct']}%), worth {rp_b(K['maverick_spend_idr'])}, "
        f"bypass the procedure and carry a {K['maverick_price_premium_pct']}% price premium, an estimated excess spend "
        f"of {rp_b(K['maverick_excess_spend_idr'])} over two years. Third, vendor performance is never recorded: "
        f"on-time delivery averages {K['on_time_rate_pct']}%, but per-vendor scores range from "
        f"{K['vendor_scorecard'][-1]['score']} to {K['vendor_scorecard'][0]['score']} with no consequence for order allocation.", BODY))
    E.append(Paragraph(
        "The recommendation is a cloud e-procurement system (buy, not build) covering online PR submission, digital "
        "approval with reminders, an RFQ vendor portal with deadlines, electronic PO issuance, goods receipt recording, "
        "automatic three-way matching, and a KPI dashboard. Design targets: average cycle time of 7.0 days or less and a "
        "maverick rate of 3% or less, with a controlled fast-track lane for genuine urgencies. The Cost-Benefit Analysis "
        "(case-study estimates) projects annual benefits of about Rp 4.85 billion at steady state against one-time costs "
        "of Rp 0.80 billion and recurring costs of Rp 0.54 billion per year, with payback in approximately 9 months and a "
        "three-year ROI of about 401%.", BODY))

    E.append(Paragraph("2. Problem Statement", H1))
    for b in [
        "<b>Unpredictable material availability.</b> An average cycle of 17.5 days before vendor lead time (average actual lead time 13.6 days) makes site planning unreliable.",
        "<b>No visibility.</b> Nobody can answer where a PR is without phone calls and email searches; the tracking spreadsheet is updated by hand.",
        "<b>Loss of price control.</b> 12.2% of purchases bypass competitive quotation at an estimated 10.8% premium, about Rp 4.19 billion per year of excess spend.",
        "<b>No learning loop.</b> Vendor performance, bottlenecks, and spend patterns exist only as scattered emails and paper.",
    ]:
        E.append(Paragraph(b, BULLET, bulletText="•"))

    E.append(Paragraph("3. Objectives", H1))
    data = [hdr(["ID", "Objective", "Baseline", "Target"])]
    for r in [
        ("OBJ-1", "Shorten the PR-to-PO cycle", "17.5 days average", "7.0 days or less"),
        ("OBJ-2", "Real-time status visibility", "None", "100% of PRs trackable"),
        ("OBJ-3", "Control off-procedure buying", "12.2% of PRs maverick", "3% or less, fast-track lane"),
        ("OBJ-4", "Use vendor performance", "85.7% on-time, unrecorded", "Monthly scorecard, toward 93%"),
        ("OBJ-5", "Remove manual administration", "Paper, spreadsheets, retyping", "Zero paper forms"),
        ("OBJ-6", "Decision-grade reporting", "Manual and rare", "Automatic monthly dashboard"),
    ]:
        data.append(row(r))
    E.append(styled_table(data, [30 * mm, 62 * mm, 42 * mm, 40 * mm]))

    E.append(Paragraph("4. Key Findings", H1))
    E.append(Paragraph("F1. Waiting dominates the cycle", H2))
    data = [hdr(["Stage", "Avg days", "Share of cycle"])]
    for s, v in K["stage_avg_days"].items():
        data.append(row([s, f"{v:.2f}", f"{K['stage_share_pct'][s]}%"]))
    data.append(row(["<b>Total cycle</b>", f"<b>{K['cycle_time_avg_days']}</b>", "<b>100%</b>"]))
    E.append(styled_table(data, [74 * mm, 40 * mm, 40 * mm]))
    E.append(Spacer(1, 3 * mm))
    E.append(Image(os.path.join(ROOT, "analysis", "charts", "cycle_time_by_stage.png"), width=160 * mm, height=82 * mm))
    E.append(Paragraph(
        "The bottleneck is the Vendor Quotation Wait at 6.02 days (34.4% of the cycle): RFQs go out by email with no "
        "deadline and no reminder. The two internal approval stages add 7.78 days (44.5%) of pure waiting. In total, "
        "65.6% of the cycle is internal process time a digital workflow can compress directly.", BODY))
    E.append(Paragraph("F2. Maverick buying is a symptom, and an expensive one", H2))
    E.append(Paragraph(
        f"{K['maverick_count']} PRs ({K['maverick_rate_pct']}%) bypass the process, worth {rp_b(K['maverick_spend_idr'])} "
        f"({K['maverick_spend_share_pct']}% of spend). They finish in {K['maverick_avg_cycle_days']} days against "
        f"{K['normal_avg_cycle_days']} days for planned purchases, which is why sites use them, but they cost a "
        f"{K['maverick_price_premium_pct']}% premium: {rp(K['maverick_excess_spend_idr'])} of excess spend in two years.", BODY))
    E.append(Image(os.path.join(ROOT, "analysis", "charts", "maverick_analysis.png"), width=155 * mm, height=72 * mm))
    E.append(Paragraph("F3. Vendor performance is unmanaged", H2))
    sc = K["vendor_scorecard"]
    data = [hdr(["Vendor", "Tier", "Transactions", "Avg lead", "On-time", "Score"])]
    for v in sc[:3] + sc[-2:]:
        data.append(row([v["vendor"], v["tier"], v["transactions"], f"{v['avg_lead_time_days']} d",
                         f"{v['on_time_rate_pct']}%", v["score"]]))
    E.append(styled_table(data, [58 * mm, 14 * mm, 28 * mm, 22 * mm, 22 * mm, 16 * mm]))
    E.append(Paragraph(
        "Tier A vendors deliver on time 91.1% to 96.1% of the time; Tier C only 71.1% to 79.2%, with lead times around "
        "20 days, roughly 2.4 times slower. Because no scorecard exists, allocation ignores performance.", BODY))
    E.append(Paragraph("F4. Spend is concentrated; F5. The process, not a site, is the problem", H2))
    top3 = list(K["spend_by_category_idr"].items())[:3]
    E.append(Paragraph(
        f"The top three categories ({', '.join(c for c, _ in top3)}) hold 76.1% of spend, so catalogs and framework "
        f"agreements for a short list cover most value. Average cycle time by site spans only "
        f"{min(K['cycle_by_site_days'].values())} to {max(K['cycle_by_site_days'].values())} days, showing every site "
        "suffers the same manual design. Demand is seasonal: peak month April with "
        f"{K['peak_month_count']} PRs versus {K['low_month_count']} in January (2.07 times).", BODY))
    E.append(Image(os.path.join(ROOT, "analysis", "charts", "spend_by_category.png"), width=160 * mm, height=82 * mm))

    E.append(Paragraph("5. Recommendation and Roadmap", H1))
    for b in [
        "<b>Phase 1 (months 1 to 3), core flow:</b> online PR with catalog, digital approval with reminders and delegation, validation queue with SLA timers, requester tracking.",
        "<b>Phase 2 (months 4 to 6), sourcing and fulfillment:</b> RFQ vendor portal with deadlines, comparison matrix, e-PO with e-signature, fast-track lane, goods receipt, three-way match.",
        "<b>Phase 3 (months 7 to 9), intelligence:</b> KPI dashboard, vendor scorecards, framework agreements for top categories.",
    ]:
        E.append(Paragraph(b, BULLET, bulletText="•"))
    E.append(Paragraph(
        "Build vs Buy weighted scores: Buy SaaS 4.20, ERP module 3.35, Build in-house 3.00. The deciding factor is time: "
        "at an estimated Rp 4.19 billion per year of maverick excess spend, every quarter of delay costs more than the "
        "price differences between options.", BODY))
    E.append(Paragraph("6. Economics (case-study estimates)", H1))
    data = [hdr(["", "Year 1", "Year 2", "Year 3", "Total"])]
    data.append(row(["Benefits", "Rp 2.43 B", "Rp 4.85 B", "Rp 4.85 B", "Rp 12.13 B"]))
    data.append(row(["Costs (one-time + recurring)", "Rp 1.34 B", "Rp 0.54 B", "Rp 0.54 B", "Rp 2.42 B"]))
    data.append(row(["Net", "Rp 1.09 B", "Rp 4.31 B", "Rp 4.31 B", "Rp 9.71 B"]))
    E.append(styled_table(data, [52 * mm, 30 * mm, 30 * mm, 30 * mm, 32 * mm]))
    E.append(Paragraph(
        "Three-year ROI is about 401% and payback is approximately 9 months from project start. The project stays net "
        "positive over three years even if only about 20% of projected benefits materialize. Full assumptions are in the "
        "Cost-Benefit Analysis document.", BODY))
    E.append(Paragraph(
        "Supporting documents: Process Maps, Stakeholder Analysis, Business Requirements Document, Gap Analysis, "
        "Elicitation Pack, Use Cases and User Stories, Data Model, Build vs Buy Analysis, Risk Register, UAT Plan and "
        "Traceability Matrix, Change Management and Training Plan. Prototypes: KPI dashboard and workflow simulation "
        "(HTML). Analysis code, synthetic dataset, and automated tests are included in the project repository.", SMALL))
    doc.build(E, onFirstPage=footer, onLaterPages=footer)
    print("Built", path)


# ---------------------------------------------------------------- deck
def build_deck():
    path = os.path.join(HERE, "Management_Deck.pdf")
    W, H = landscape(A4)
    doc = SimpleDocTemplate(path, pagesize=landscape(A4), leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=16 * mm, bottomMargin=14 * mm,
                            title="ProcureBA Management Deck", author="Andika Pratama Zaid")
    DT = ParagraphStyle("dt", parent=ss["Title"], fontSize=30, leading=36, textColor=NAVY, alignment=TA_LEFT)
    DH = ParagraphStyle("dh", parent=ss["Heading1"], fontSize=24, leading=29, textColor=NAVY)
    DB = ParagraphStyle("db", parent=ss["Normal"], fontSize=14.5, leading=20)
    DBB = ParagraphStyle("dbb", parent=DB, leftIndent=18, bulletIndent=6, spaceAfter=7)
    DSMALL = ParagraphStyle("dsmall", parent=ss["Normal"], fontSize=10.5, leading=14, textColor=colors.HexColor("#555555"))
    BIG = ParagraphStyle("big", parent=ss["Normal"], fontSize=34, leading=38, textColor=ACCENT, alignment=TA_CENTER)
    BIGL = ParagraphStyle("bigl", parent=ss["Normal"], fontSize=12, leading=15, alignment=TA_CENTER, textColor=NAVY)

    def slide(title, body_elems):
        return [Paragraph(title, DH), Spacer(1, 5 * mm)] + body_elems + [PageBreak()]

    E = []
    E.append(Spacer(1, 26 * mm))
    E.append(Paragraph("ProcureBA", ParagraphStyle("brandd", parent=DT, fontSize=38, leading=42)))
    E.append(Paragraph("EPC Procurement Digitalization", DT))
    E.append(Spacer(1, 6 * mm))
    E.append(Paragraph("Management briefing: findings and recommendation from a business analysis case study", ParagraphStyle("dsub", parent=DB, textColor=STEEL)))
    E.append(Spacer(1, 12 * mm))
    E.append(Paragraph("Fictional case study. Synthetic dataset of 2,400 PR records (2024 to 2025), fixed seed, fully reproducible. Targets shown are simulation targets.", DSMALL))
    E.append(PageBreak())

    nums = Table([
        [Paragraph(f"{K['cycle_time_avg_days']} days", BIG), Paragraph(f"{K['maverick_rate_pct']}%", BIG), Paragraph(f"+{K['maverick_price_premium_pct']}%", BIG)],
        [Paragraph("average PR-to-PO cycle time (target 7.0 days)", BIGL), Paragraph("of PRs bypass the process entirely", BIGL), Paragraph("price premium paid on maverick purchases", BIGL)],
    ], colWidths=[(W - 40 * mm) / 3] * 3)
    nums.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    E += slide("The problem in three numbers", [nums, Spacer(1, 8 * mm),
               Paragraph(f"Maverick purchases total {rp_b(K['maverick_spend_idr'])} over two years and an estimated {rp_b(K['maverick_excess_spend_idr'])} of excess spend, about Rp 4.19 billion per year.", DB)])

    stage_data = [hdr(["Stage", "Avg days", "Share"])]
    for s, v in K["stage_avg_days"].items():
        stage_data.append(row([s, f"{v:.2f}", f"{K['stage_share_pct'][s]}%"]))
    E += slide("Where the time goes", [
        styled_table(stage_data, [90 * mm, 40 * mm, 40 * mm]),
        Spacer(1, 4 * mm),
        Paragraph("The quotation wait (34.4%) has no deadline and no reminder. The two approval stages add 7.78 days of pure waiting. 65.6% of the cycle is internal process time.", DB)])

    E += slide("Why sites bypass the process", [
        Paragraph(f"Maverick purchases finish in {K['maverick_avg_cycle_days']} days. Planned purchases take {K['normal_avg_cycle_days']} days.", DBB, bulletText="•"),
        Paragraph(f"{K['urgent_rate_pct']}% of all PRs are flagged urgent. The process offers no legitimate fast path.", DBB, bulletText="•"),
        Paragraph("Conclusion: maverick buying is a rational response to a slow process. Banning it without fixing the process would stop site work.", DBB, bulletText="•"),
        Paragraph("Design answer: a controlled fast-track lane inside the system, with mandatory justification, elevated approval, and post-review.", DBB, bulletText="•"),
    ])

    sc = K["vendor_scorecard"]
    vdata = [hdr(["Vendor", "On-time", "Avg lead", "Score"])]
    for v in sc[:2] + sc[-2:]:
        vdata.append(row([v["vendor"], f"{v['on_time_rate_pct']}%", f"{v['avg_lead_time_days']} d", v["score"]]))
    E += slide("Vendor performance is invisible today", [
        styled_table(vdata, [95 * mm, 35 * mm, 35 * mm, 30 * mm]),
        Spacer(1, 4 * mm),
        Paragraph(f"Overall on-time delivery is {K['on_time_rate_pct']}%. The weakest vendor still received {sc[-1]['transactions']} transactions because nothing records performance. A monthly automatic scorecard fixes this at near-zero marginal cost once transactions are digital.", DB)])

    E += slide("The recommendation", [
        Paragraph("<b>Buy a cloud e-procurement SaaS</b> (weighted score 4.20, ahead of ERP module 3.35 and build in-house 3.00).", DBB, bulletText="•"),
        Paragraph("<b>Phase 1 (months 1 to 3):</b> online PR, digital approval, visible queue, requester tracking.", DBB, bulletText="•"),
        Paragraph("<b>Phase 2 (months 4 to 6):</b> vendor RFQ portal with deadlines, e-PO, fast-track lane, goods receipt, three-way match.", DBB, bulletText="•"),
        Paragraph("<b>Phase 3 (months 7 to 9):</b> KPI dashboard, vendor scorecards, framework agreements for the top 3 categories (76.1% of spend).", DBB, bulletText="•"),
        Paragraph("Targets: cycle time 7.0 days or less, maverick rate 3% or less, on-time delivery toward 93%.", DBB, bulletText="•"),
    ])

    edata = [hdr(["Case-study estimates", "Year 1", "Year 2", "Year 3"])]
    edata.append(row(["Benefits", "Rp 2.43 B", "Rp 4.85 B", "Rp 4.85 B"]))
    edata.append(row(["Costs", "Rp 1.34 B", "Rp 0.54 B", "Rp 0.54 B"]))
    edata.append(row(["Net", "Rp 1.09 B", "Rp 4.31 B", "Rp 4.31 B"]))
    E += slide("The economics", [
        styled_table(edata, [70 * mm, 40 * mm, 40 * mm, 40 * mm]),
        Spacer(1, 4 * mm),
        Paragraph("Three-year net benefit about Rp 9.71 billion, ROI about 401%, payback approximately 9 months. The case stays positive even at 20% benefit realization, and the largest benefit line (maverick premium avoided, Rp 2.93 billion per year) alone covers all three-year costs.", DB)])

    E += slide("What we ask from management", [
        Paragraph("Approve the SaaS direction and the Phase 0 policy package: e-signature decree, quotation deadline rule, fast-track governance.", DBB, bulletText="1."),
        Paragraph("Approve the budget envelope: Rp 0.80 billion one-time, Rp 0.54 billion per year (case-study estimates).", DBB, bulletText="2."),
        Paragraph("Chair the monthly steering review against three KPIs: cycle time, maverick rate, on-time delivery.", DBB, bulletText="3."),
        Paragraph("Main risks are behavioral, not technical: approver habits, vendor adoption, off-system buying. Mitigations are in the Risk Register and Change Management Plan.", DBB, bulletText="4."),
    ])
    if E and isinstance(E[-1], PageBreak):
        E.pop()
    doc.build(E)
    print("Built", path)


if __name__ == "__main__":
    build_report()
    build_deck()
