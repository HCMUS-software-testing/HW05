#!/usr/bin/env python3
"""Regression tests for the HW05 result analyzer and submission validator."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_jtl import analyze_jtl, html_total
from monitor_backend import cpu_percent
from validate_submission import (
    package_root_name,
    plan_assertions_valid,
    resource_log_findings,
    result_consistency,
    workflow_cleanup_findings,
)


class JtlAnalyzerTests(unittest.TestCase):
    def test_cpu_percent_uses_interval_jiffy_deltas(self):
        self.assertEqual(cpu_percent((10, 100), (30, 200), cpu_count=4), 80.0)

    def test_reports_elapsed_and_latency_as_distinct_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "raw.jtl"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(
                    stream,
                    fieldnames=["timeStamp", "elapsed", "Latency", "success", "label"],
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"timeStamp": "1000", "elapsed": "100", "Latency": "40", "success": "true", "label": "A"},
                        {"timeStamp": "1200", "elapsed": "300", "Latency": "60", "success": "false", "label": "B"},
                    ]
                )

            metrics = analyze_jtl(path)

            self.assertEqual(metrics["samples"], 2)
            self.assertEqual(metrics["errors"], 1)
            self.assertEqual(metrics["avg_elapsed_ms"], 200.0)
            self.assertEqual(metrics["avg_latency_ms"], 50.0)
            self.assertEqual(metrics["duration_s"], 0.5)
            self.assertEqual(metrics["throughput_rps"], 4.0)

    def test_reads_total_sample_count_from_html_statistics(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "statistics.json"
            path.write_text(
                json.dumps({"Login": {"sampleCount": 2}, "Total": {"sampleCount": 6}}),
                encoding="utf-8",
            )
            self.assertEqual(html_total(path), 6)

    def test_detects_expected_count_and_html_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            jtl = root / "raw.jtl"
            with jtl.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=["timeStamp", "elapsed", "success"])
                writer.writeheader()
                writer.writerow({"timeStamp": "1000", "elapsed": "10", "success": "true"})
                writer.writerow({"timeStamp": "1020", "elapsed": "10", "success": "true"})
            statistics_path = root / "statistics.json"
            statistics_path.write_text(json.dumps({"Total": {"sampleCount": 1}}), encoding="utf-8")

            findings = result_consistency(jtl, statistics_path, expected_samples=3)

            self.assertIn("JTL samples = 2, expected 3", findings)
            self.assertIn("JTL samples = 2, HTML samples = 1", findings)

    def test_requires_cleanup_evidence_for_unbalanced_transactional_samples(self):
        metrics = {"labels": {"Create Product": 4, "Delete Product Cleanup": 2}}
        self.assertTrue(workflow_cleanup_findings(metrics, None))
        cleanup = {"orphan_count": 2, "deleted_ids": [11, 12], "all_deleted": True}
        self.assertEqual(workflow_cleanup_findings(metrics, cleanup), [])

    def test_resource_log_must_cover_endurance_window_with_one_pid(self):
        rows = [
            {"timestamp_utc": "2026-09-02T17:10:50+00:00", "pid": "7", "rss_mib": "100"},
            {"timestamp_utc": "2026-09-02T17:20:55+00:00", "pid": "7", "rss_mib": "110"},
        ]
        self.assertEqual(
            resource_log_findings(
                rows, minimum_span_s=590,
                run_start_ms=1788369052343, run_end_ms=1788369650860,
            ),
            [],
        )
        rows[1]["pid"] = "8"
        self.assertIn("resource log contains multiple PIDs", resource_log_findings(rows, 590))

    def test_resource_log_rejects_non_overlapping_run(self):
        rows = [
            {"timestamp_utc": "2026-09-01T00:00:00+00:00", "pid": "7", "rss_mib": "100"},
            {"timestamp_utc": "2026-09-01T00:10:00+00:00", "pid": "7", "rss_mib": "110"},
        ]
        findings = resource_log_findings(
            rows, 590, run_start_ms=1788369052343, run_end_ms=1788369650860
        )
        self.assertIn("resource log does not cover the JTL run window", findings)

    def test_package_name_controls_zip_and_internal_root(self):
        self.assertEqual(
            package_root_name(Path("23127075_HW05_AI_Performance_094.zip")),
            "23127075_HW05_AI_Performance_094",
        )
        with self.assertRaises(ValueError):
            package_root_name(Path("23127075_HW05.zip"))


class PlanRegressionTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[1]

    def test_delete_sampler_labels_are_stable(self):
        for plan in sorted((self.ROOT / "test-plans").glob("*_[LSS]*_*.jmx")):
            root = ET.parse(plan).getroot()
            labels = [node.attrib.get("testname", "") for node in root.iter("HTTPSamplerProxy")]
            self.assertFalse(any("${created_product_id}" in label for label in labels), plan.name)

    def test_gaussian_timer_targets_are_documented_as_distribution(self):
        expected = {"Load": ("2000", "333"), "Stress": ("1000", "167")}
        for kind, values in expected.items():
            plan = next((self.ROOT / "test-plans").glob(f"*_{kind}_*.jmx"))
            root = ET.parse(plan).getroot()
            timer = next(root.iter("GaussianRandomTimer"))
            props = {node.attrib.get("name"): node.text for node in timer.iter("stringProp")}
            self.assertEqual((props["ConstantTimer.delay"], props["RandomTimer.range"]), values)
            self.assertIn("99.7%", timer.attrib.get("testname", ""))

    def test_each_sampler_has_enabled_http_code_assertion(self):
        for plan in sorted((self.ROOT / "test-plans").glob("*.jmx")):
            self.assertTrue(plan_assertions_valid(ET.parse(plan).getroot()), plan.name)

    def test_endurance_plan_runs_sustained_load_for_ten_minutes(self):
        plans = list((self.ROOT / "test-plans").glob("*_Endurance_*.jmx"))
        self.assertEqual(len(plans), 1)
        root = ET.parse(plans[0]).getroot()
        props = {node.attrib.get("name"): node.text for node in root.iter("stringProp")}
        bools = {node.attrib.get("name"): node.text for node in root.iter("boolProp")}
        self.assertEqual(props["ThreadGroup.num_threads"], "30")
        self.assertEqual(props["ThreadGroup.duration"], "600")
        self.assertEqual(props["LoopController.loops"], "-1")
        self.assertEqual(bools["ThreadGroup.scheduler"], "true")
        self.assertTrue((self.ROOT / "tools" / "monitor_backend.py").exists())
        runner = (self.ROOT / "run_endurance.sh").read_text(encoding="utf-8")
        self.assertIn("rm -f results/endurance/raw.jtl", runner)
        self.assertIn("23127075_Endurance_20260902.jmx", runner)
        self.assertIn("backend-resources.csv", runner)


if __name__ == "__main__":
    unittest.main()
