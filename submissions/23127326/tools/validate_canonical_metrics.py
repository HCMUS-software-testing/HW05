#!/usr/bin/env python3
"""Fail when canonical JTL metrics drift across the submission narrative."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "report" / "metrics-resource-rerun-20260830"

EXPECTED = {
    "load": (3287, 356),
    "stress": (16433, 1780),
    "spike": (7171, 751),
    "endurance": (24574, 2699),
}

DOCUMENTS = (
    ROOT / "README.md",
    ROOT / "report" / "main-report.md",
    ROOT / "report" / "ai-critique.md",
    ROOT / "report" / "issue-candidates.md",
)

STALE_TOKENS = ("3.314", "16.519", "7.175", "24.608", "359/", "1.789/", "753/", "2.700/")


def main():
    for scenario, (rows, assertions) in EXPECTED.items():
        payload = json.loads((METRICS / f"{scenario}.json").read_text(encoding="utf-8"))
        assert payload["source_rows"] == rows, (scenario, payload["source_rows"], rows)
        observed_http = sum(label["http_errors"] for label in payload["labels"].values())
        observed_assertions = sum(label["assertion_failures"] for label in payload["labels"].values())
        assert observed_http == 0, (scenario, "HTTP errors", observed_http)
        assert observed_assertions == assertions, (scenario, observed_assertions, assertions)

    for document in DOCUMENTS:
        text = document.read_text(encoding="utf-8")
        stale = [token for token in STALE_TOKENS if token in text]
        assert not stale, (document, "stale canonical values", stale)

    staircase = json.loads(
        (ROOT / "report" / "metrics-staircase-20260830" / "staircase-summary.json").read_text(encoding="utf-8")
    )
    endurance = next(run for run in staircase["runs"] if run["run"] == "Endurance 200 VU")
    assert endurance["samples"] == 65859
    assert endurance["http_errors"] == 0
    assert endurance["assertion_failures"] == 7226
    assert endurance["hold_http_requests_per_second"] == 77.44
    assert endurance["p95_ms"] == 5.0
    assert endurance["hold_cpu_percent_max"] == 17.7
    assert endurance["rss_mb_max"] == 119.328

    report_text = (ROOT / "report" / "main-report.md").read_text(encoding="utf-8")
    for token in ("77.4400", "65,859", "17,7%", "119.3 MB"):
        assert token in report_text, ("main-report.md", "missing threshold token", token)

    print("Canonical and staircase metrics validated: JTL-derived JSON and narratives agree.")


if __name__ == "__main__":
    main()
