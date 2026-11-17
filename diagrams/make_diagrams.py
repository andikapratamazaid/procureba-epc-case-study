#!/usr/bin/env python3
"""Generate all ProcureBA diagrams as PNG with matplotlib:
process maps (as-is, to-be), power-interest grid, use case diagram, ERD.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = "#16324f"
STEEL = "#4a6fa5"
LIGHT = "#dbe7f3"
ACCENT = "#c05621"
GREY = "#666666"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), dpi=150)
    plt.close(fig)
    print("diagram:", name)


def box(ax, x, y, w, h, text, fc=LIGHT, ec=NAVY, fs=8.2, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.1",
                                fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)


def arrow(ax, x1, y1, x2, y2, color=NAVY):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=11, color=color, lw=1.1))


LANES = ["Requester (Site)", "Project Manager", "Procurement", "Vendors", "Warehouse and Finance"]


def process_map(filename, title, steps, pain_note):
    n = len(steps)
    width = 2.55 + n * 2.02
    fig, ax = plt.subplots(figsize=(15.2, 6.6))
    ax.set_xlim(0, width)
    ax.set_ylim(-1.5, 5.7)
    ax.axis("off")
    for li, lane in enumerate(LANES):
        y = 4.6 - li * 1.05
        ax.add_patch(Rectangle((0, y - 0.46), width, 0.98,
                               fc="#f2f6fa" if li % 2 == 0 else "#ffffff", ec="#c9d6e4", lw=0.7))
        ax.text(0.1, y, lane, fontsize=8.8, fontweight="bold", color=NAVY, va="center")
    prev = None
    for i, (lane_idx, text, fc) in enumerate(steps):
        x = 2.55 + i * 2.02
        y = 4.6 - lane_idx * 1.05
        box(ax, x, y - 0.4, 1.86, 0.84, text, fc=fc, fs=7.7)
        if prev is not None:
            px, py = prev
            arrow(ax, px + 1.92, py, x - 0.04, y)
        prev = (x, y)
    ax.set_title(title, fontsize=12.5, color=NAVY, fontweight="bold", pad=10)
    ax.text(0.1, -0.72, pain_note, fontsize=8.6, color=ACCENT, va="top")
    save(fig, filename)


PAIN = "#fbd9c9"
OKC = "#cdeacd"

AS_IS = [
    (0, "1. Fill paper\nPR form", PAIN),
    (1, "2. PM signs paper form\n(avg 3.74 days)", PAIN),
    (2, "3. Log PR manually\nin spreadsheet", LIGHT),
    (2, "4. Review queue, file\nmoves by hand\n(avg 4.04 days)", PAIN),
    (2, "5. Prepare RFQ in Word,\nsend by email", LIGHT),
    (3, "6. Vendors reply by email\nwhen ready\n(avg 6.02 days)", PAIN),
    (2, "7. Compare quotations\nin spreadsheet", LIGHT),
    (2, "8. Type, print, sign, scan\nand email PO\n(eval + PO avg 2.59 days)", LIGHT),
    (4, "9. Paper delivery note\ncheck, manual 3-way\ninvoice match", LIGHT),
]

TO_BE = [
    (0, "1. Submit PR in system,\ncatalog based", OKC),
    (1, "2. PM approves in app,\nauto reminder\n(target 1 day)", OKC),
    (2, "3. Auto queue and digital\nvalidation (target 1 day)", OKC),
    (2, "4. System generates RFQ\nto vendor portal\n(target 0.5 day)", OKC),
    (3, "5. Quotations online with\ndeadline reminders\n(target 3 days)", OKC),
    (2, "6. System comparison\nmatrix and evaluation\n(target 1 day)", OKC),
    (2, "7. E-PO issued with\ne-signature\n(target 0.5 day)", OKC),
    (4, "8. Delivery tracked, GR in\nsystem, auto 3-way match", OKC),
]

process_map("process_as_is.png",
            "As-Is Process Map: Manual PR-to-PO (average 17.5 days, synthetic case data)",
            AS_IS,
            "Pain points (orange): the PM signature waits for one person, the paper review queue is invisible, and the vendor quotation wait\n"
            "has no deadline or reminder. Requesters have no status visibility at any stage, so urgent needs bypass the process entirely\n"
            "(12.2% of PRs are maverick purchases).")
process_map("process_to_be.png",
            "To-Be Process Map: Digital PR-to-PO (target average 7.0 days, simulation target)",
            TO_BE,
            "Design targets: every stage is time-boxed inside the system, requesters see live status, and a controlled fast-track lane\n"
            "handles genuine urgencies inside the system instead of maverick buying outside it.")

# ---------------- Power-interest grid ----------------
fig, ax = plt.subplots(figsize=(7.6, 6.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
for (x0, y0, c) in [(5, 5, "#fdeeda"), (0, 5, "#eef4ea"), (5, 0, "#eef2f7"), (0, 0, "#f7f7f7")]:
    ax.add_patch(Rectangle((x0, y0), 5, 5, fc=c, ec="none"))
ax.axhline(5, color=GREY, lw=0.9)
ax.axvline(5, color=GREY, lw=0.9)
ax.text(7.5, 9.6, "Manage closely", ha="center", fontsize=9, color=ACCENT, fontweight="bold")
ax.text(2.5, 9.6, "Keep satisfied", ha="center", fontsize=9, color=GREY, fontweight="bold")
ax.text(7.5, 0.35, "Keep informed", ha="center", fontsize=9, color=GREY, fontweight="bold")
ax.text(2.5, 0.35, "Monitor", ha="center", fontsize=9, color=GREY, fontweight="bold")
stakeholders = [
    ("Director of Operations", 8.4, 9.1),
    ("Procurement Manager", 7.4, 8.4),
    ("Project Managers (5 sites)", 8.3, 7.2),
    ("Finance Manager", 6.2, 8.3),
    ("Site Engineers (requesters)", 8.8, 5.7),
    ("IT Department", 4.0, 6.6),
    ("Vendors (18 active)", 5.9, 4.4),
    ("Warehouse Staff", 6.9, 3.2),
    ("QA/QC and HSE", 3.2, 3.6),
    ("External auditors", 2.0, 5.7),
]
for name, x, y in stakeholders:
    ax.plot(x, y, "o", color=NAVY, markersize=7)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(7, 4), fontsize=8.2)
ax.set_xlabel("Interest in the project (low to high)")
ax.set_ylabel("Power / influence (low to high)")
ax.set_title("Stakeholder Power-Interest Grid", fontsize=12, color=NAVY, fontweight="bold")
save(fig, "power_interest_grid.png")

# ---------------- Use case diagram ----------------
fig, ax = plt.subplots(figsize=(11.5, 7.2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")
ax.add_patch(Rectangle((4.2, 0.5), 6.4, 8.0, fc="#fbfcfe", ec=NAVY, lw=1.4))
ax.text(7.4, 8.15, "E-Procurement System (to-be)", ha="center", fontsize=10.5,
        color=NAVY, fontweight="bold")
use_cases = [
    "UC-01 Submit Purchase Requisition",
    "UC-02 Approve or Reject PR",
    "UC-03 Create and Send RFQ",
    "UC-04 Submit Quotation",
    "UC-05 Evaluate and Issue PO",
    "UC-06 Track Procurement Status",
    "UC-07 Record Goods Receipt",
    "UC-08 Match Invoice (3-way)",
    "UC-09 Manage Vendor Master Data",
    "UC-10 View KPI Dashboard",
    "UC-11 Manage Users and Catalog",
]
uc_left, uc_right = {}, {}
for i, uc in enumerate(use_cases):
    y = 7.55 - i * 0.62
    ax.add_patch(Ellipse((7.4, y), 5.4, 0.52, fc=LIGHT, ec=NAVY, lw=0.9))
    ax.text(7.4, y, uc, ha="center", va="center", fontsize=8.0)
    uc_left[uc] = (4.7, y)
    uc_right[uc] = (10.1, y)
actors_left = [("Site Engineer", [0]), ("Project Manager", [1]),
               ("Procurement Officer", [2, 4, 5, 8, 9]), ("Vendor", [3])]
actors_right = [("Warehouse Staff", [6]), ("Finance Staff", [7]),
                ("System Admin", [10]), ("Management", [9])]
for j, (name, idxs) in enumerate(actors_left):
    y = 6.9 - j * 1.7
    box(ax, 0.2, y - 0.3, 1.9, 0.6, name, fc="#eef4ea", fs=8.6)
    for ix in idxs:
        tx, ty = uc_left[use_cases[ix]]
        arrow(ax, 2.1, y, tx, ty, color=STEEL)
for j, (name, idxs) in enumerate(actors_right):
    y = 6.9 - j * 1.7
    box(ax, 11.9, y - 0.3, 1.9, 0.6, name, fc="#eef4ea", fs=8.6)
    for ix in idxs:
        tx, ty = uc_right[use_cases[ix]]
        arrow(ax, 11.9, y, tx, ty, color=STEEL)
ax.set_title("Use Case Diagram: Proposed E-Procurement System", fontsize=12.5,
             color=NAVY, fontweight="bold")
save(fig, "use_case_diagram.png")

# ---------------- ERD ----------------
TABLES = {
    "PURCHASE_REQUISITION": (0.3, 6.3, ["pr_id (PK)", "pr_date", "site", "requester_id", "category",
                                        "urgent_flag", "status"]),
    "APPROVAL": (4.9, 6.3, ["approval_id (PK)", "pr_id (FK)", "approver_id", "approval_level",
                            "decision", "decision_date", "remarks"]),
    "VENDOR": (9.5, 6.3, ["vendor_id (PK)", "vendor_name", "tier", "contact_email", "bank_account", "status"]),
    "PURCHASE_ORDER": (14.1, 6.3, ["po_id (PK)", "pr_id (FK)", "vendor_id (FK)", "po_date",
                                   "po_value", "promised_lead_time_days", "status"]),
    "PR_ITEM": (0.3, 2.0, ["pr_item_id (PK)", "pr_id (FK)", "item_id (FK)", "quantity", "unit",
                           "estimated_price", "line_total"]),
    "ITEM_CATALOG": (4.9, 2.0, ["item_id (PK)", "item_code", "item_name", "category", "unit",
                                "standard_price"]),
    "GOODS_RECEIPT": (14.1, 2.0, ["gr_id (PK)", "po_id (FK)", "receipt_date", "received_by",
                                  "qty_received", "condition_ok"]),
}
fig, ax = plt.subplots(figsize=(16.5, 8.6))
ax.set_xlim(0, 17.6)
ax.set_ylim(0, 10.2)
ax.axis("off")
geo = {}
for name, (x, y, fields) in TABLES.items():
    h = 0.62 + 0.33 * len(fields)
    ax.add_patch(Rectangle((x, y), 3.2, h, fc="white", ec=NAVY, lw=1.2))
    ax.add_patch(Rectangle((x, y + h - 0.44), 3.2, 0.44, fc=NAVY, ec=NAVY))
    ax.text(x + 1.6, y + h - 0.22, name, ha="center", va="center", fontsize=9.5,
            color="white", fontweight="bold")
    for i, f in enumerate(fields):
        ax.text(x + 0.12, y + h - 0.82 - i * 0.315, f, fontsize=8.6, va="center")
    geo[name] = {"cx": x + 1.6, "x": x, "y": y, "w": 3.2, "h": h,
                 "l": (x, y + h / 2), "r": (x + 3.2, y + h / 2),
                 "t": (x + 1.6, y + h), "b": (x + 1.6, y)}


def rel(a, side_a, b, side_b, label, label_dy=0.22):
    x1, y1 = geo[a][side_a]
    x2, y2 = geo[b][side_b]
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + label_dy, label, ha="center", fontsize=9, color=ACCENT)


rel("PURCHASE_REQUISITION", "r", "APPROVAL", "l", "1 : N")
rel("VENDOR", "r", "PURCHASE_ORDER", "l", "1 : N")
rel("PURCHASE_REQUISITION", "b", "PR_ITEM", "t", "1 : N", label_dy=0.0)
rel("ITEM_CATALOG", "l", "PR_ITEM", "r", "1 : N")
rel("PURCHASE_ORDER", "b", "GOODS_RECEIPT", "t", "1 : N", label_dy=0.0)
# PR to PO routed below the top row to avoid crossing tables
pr = geo["PURCHASE_REQUISITION"]
po = geo["PURCHASE_ORDER"]
route_y = 5.75
ax.plot([pr["cx"], pr["cx"], po["cx"]], [pr["y"], route_y, route_y], color=STEEL, lw=1.2)
ax.annotate("", xy=(po["cx"], po["y"]), xytext=(po["cx"], route_y),
            arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.2))
ax.text((pr["cx"] + po["cx"]) / 2, route_y + 0.18, "PURCHASE_REQUISITION 1 : 1..N PURCHASE_ORDER",
        ha="center", fontsize=9, color=ACCENT)
ax.set_title("Entity Relationship Diagram: Proposed E-Procurement System",
             fontsize=13.5, color=NAVY, fontweight="bold")
save(fig, "erd.png")
print("All diagrams done.")
