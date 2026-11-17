#!/usr/bin/env python3
"""Automated tests for the ProcureBA case study.

Verifies:
1. Dataset generator reproducibility: the same seed produces the same
   record count, the same records, and the same key aggregates.
2. KPI calculations: cycle time, stage durations, maverick metrics,
   vendor scorecard, and spend totals on known inputs and on the full
   generated dataset.

Run: python3 -m unittest discover -s tests -v   (from the project root)
Standard library only.
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

import generate_dataset  # noqa: E402
from kpi import compute_kpis, stage_durations  # noqa: E402


class TestGeneratorReproducibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = generate_dataset.generate(seed=42, count=2400)
        cls.b = generate_dataset.generate(seed=42, count=2400)

    def test_record_count(self):
        self.assertEqual(len(self.a), 2400)
        self.assertEqual(len(self.b), 2400)

    def test_same_seed_same_records(self):
        self.assertEqual(self.a, self.b)

    def test_different_seed_differs(self):
        other = generate_dataset.generate(seed=7, count=2400)
        self.assertNotEqual(self.a, other)

    def test_key_aggregates_stable(self):
        total_a = sum(r["po_value_idr"] for r in self.a)
        total_b = sum(r["po_value_idr"] for r in self.b)
        self.assertEqual(total_a, total_b)
        self.assertEqual(total_a, 656098070818)

    def test_records_sorted_by_date(self):
        dates = [r["pr_date"] for r in self.a]
        self.assertEqual(dates, sorted(dates))

    def test_all_records_have_valid_stage_order(self):
        for r in self.a:
            self.assertLessEqual(r["pr_date"], r["pm_approval_date"])
            self.assertLessEqual(r["pm_approval_date"], r["procurement_review_date"])
            self.assertLessEqual(r["rfq_sent_date"], r["quotation_received_date"])
            self.assertLessEqual(r["quotation_received_date"], r["po_date"])
            self.assertLessEqual(r["po_date"], r["goods_receipt_date"])

    def test_maverick_records_skip_rfq(self):
        for r in self.a:
            if r["maverick"] == "Yes":
                self.assertEqual(r["rfq_sent_date"], r["quotation_received_date"])
                self.assertEqual(r["procurement_review_date"], r["pm_approval_date"])


def make_record(**overrides):
    base = {
        "pr_id": "PR-00001", "pr_date": "2024-01-01", "site": "Site Alpha - Industrial Plant",
        "requester_role": "Site Engineer", "category": "Piping and Fittings",
        "estimated_value_idr": 100_000_000, "urgent": "No", "maverick": "No",
        "pm_approval_date": "2024-01-05", "procurement_review_date": "2024-01-09",
        "rfq_sent_date": "2024-01-10", "quotation_received_date": "2024-01-17",
        "po_date": "2024-01-20", "po_value_idr": 101_000_000,
        "vendor": "Test Vendor", "vendor_tier": "A", "promised_lead_time_days": 10,
        "goods_receipt_date": "2024-01-29", "actual_lead_time_days": 9, "on_time": "Yes",
        "cycle_time_days": 19,
    }
    base.update(overrides)
    return base


class TestKpiCalculations(unittest.TestCase):
    def test_stage_durations_known_input(self):
        sd = stage_durations(make_record())
        self.assertEqual(sd["PM Approval"], 4)
        self.assertEqual(sd["Procurement Review Queue"], 4)
        self.assertEqual(sd["RFQ Preparation"], 1)
        self.assertEqual(sd["Vendor Quotation Wait"], 7)
        self.assertEqual(sd["Evaluation and PO Issuance"], 3)

    def test_stage_durations_sum_to_cycle(self):
        r = make_record()
        self.assertEqual(sum(stage_durations(r).values()), r["cycle_time_days"])

    def test_kpis_on_known_pair(self):
        planned = make_record()
        maverick = make_record(
            pr_id="PR-00002", maverick="Yes", urgent="Yes",
            pm_approval_date="2024-01-02", procurement_review_date="2024-01-02",
            rfq_sent_date="2024-01-02", quotation_received_date="2024-01-02",
            po_date="2024-01-03", cycle_time_days=2,
            po_value_idr=112_000_000, on_time="No", actual_lead_time_days=15,
            goods_receipt_date="2024-01-18")
        k = compute_kpis([planned, maverick])
        self.assertEqual(k["record_count"], 2)
        self.assertEqual(k["maverick_count"], 1)
        self.assertEqual(k["maverick_rate_pct"], 50.0)
        self.assertEqual(k["total_spend_idr"], 213_000_000)
        self.assertEqual(k["on_time_rate_pct"], 50.0)
        self.assertEqual(k["cycle_time_avg_days"], 10.5)
        self.assertGreater(k["maverick_price_premium_pct"], 0)

    def test_full_dataset_headline_kpis(self):
        records = generate_dataset.generate(seed=42, count=2400)
        k = compute_kpis(records)
        self.assertEqual(k["record_count"], 2400)
        self.assertEqual(k["cycle_time_avg_days"], 17.5)
        self.assertEqual(k["bottleneck_stage"], "Vendor Quotation Wait")
        self.assertEqual(k["maverick_rate_pct"], 12.2)
        self.assertEqual(k["maverick_count"], 294)
        self.assertEqual(k["on_time_rate_pct"], 85.7)
        self.assertEqual(k["total_spend_idr"], 656098070818)
        self.assertAlmostEqual(sum(k["stage_share_pct"].values()), 100.0, delta=0.6)
        self.assertEqual(len(k["vendor_scorecard"]), 18)
        scores = [v["score"] for v in k["vendor_scorecard"]]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
