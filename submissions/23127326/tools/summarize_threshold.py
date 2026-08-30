#!/usr/bin/env python3
"""Create an auditable aggregate summary for the staircase and soak runs."""

import csv
import json
import math
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = ROOT / "results" / "staircase-20260830"
MONITOR_ROOT = ROOT / "evidence" / "hardware" / "staircase-20260830"
OUTPUT = ROOT / "report" / "metrics-staircase-20260830" / "staircase-summary.json"

RUNS = (
    ("70 VU", 30, 120, RESULT_ROOT / "70vu" / "23127326_Staircase_70VU_20260830.jtl", MONITOR_ROOT / "backend-staircase-70vu-20260830.csv"),
    ("100 VU", 30, 120, RESULT_ROOT / "100vu" / "23127326_Staircase_100VU_20260830.jtl", MONITOR_ROOT / "backend-staircase-100vu-20260830.csv"),
    ("150 VU", 45, 135, RESULT_ROOT / "150vu" / "23127326_Staircase_150VU_20260830.jtl", MONITOR_ROOT / "backend-staircase-150vu-20260830.csv"),
    ("200 VU", 60, 150, RESULT_ROOT / "200vu" / "23127326_Staircase_200VU_20260830.jtl", MONITOR_ROOT / "backend-staircase-200vu-20260830.csv"),
    ("Endurance 200 VU", 120, 720, RESULT_ROOT / "endurance-200vu" / "23127326_Endurance_200VU_20260830.jtl", MONITOR_ROOT / "backend-endurance-200vu-20260830.csv"),
)


def percentile(values, percentage):
    ordered = sorted(values)
    rank = max(1, math.ceil((percentage / 100) * len(ordered)))
    return ordered[rank - 1]


def is_http_error(row):
    code = (row.get("responseCode") or "").strip()
    if code.lower().startswith("non http"):
        return True
    try:
        return int(code) >= 400
    except ValueError:
        return False


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def summarize(name, ramp_seconds, scheduled_duration_seconds, jtl, monitor):
    rows = read_csv(jtl)
    resources = read_csv(monitor)
    elapsed = [float(row["elapsed"]) for row in rows]
    started = [float(row["timeStamp"]) for row in rows]
    finished = [float(row["timeStamp"]) + float(row["elapsed"]) for row in rows]
    duration = (max(finished) - min(started)) / 1000
    hold_start = min(started) + ramp_seconds * 1000
    hold_end = min(started) + scheduled_duration_seconds * 1000
    hold_seconds = scheduled_duration_seconds - ramp_seconds
    hold_rows = [row for row in rows if hold_start <= float(row["timeStamp"]) < hold_end]
    http_rows = [row for row in rows if (row.get("URL") or "").strip().lower() not in ("", "null")]
    hold_http_rows = [row for row in hold_rows if (row.get("URL") or "").strip().lower() not in ("", "null")]
    window_seconds = hold_seconds / 3
    hold_window_rps = []
    hold_http_rps = []
    for window in range(3):
        window_start = hold_start + window * window_seconds * 1000
        window_end = window_start + window_seconds * 1000
        count = sum(window_start <= float(row["timeStamp"]) < window_end for row in rows)
        http_count = sum(
            window_start <= float(row["timeStamp"]) < window_end
            and (row.get("URL") or "").strip().lower() not in ("", "null")
            for row in rows
        )
        hold_window_rps.append(round(count / window_seconds, 4))
        hold_http_rps.append(round(http_count / window_seconds, 4))
    failed = [row for row in rows if row.get("success", "true").lower() != "true"]
    http_errors = [row for row in failed if is_http_error(row)]
    assertions = [row for row in failed if row.get("failureMessage", "").strip() and not is_http_error(row)]
    cpu = [float(row["cpu_percent"]) for row in resources]
    rss = [float(row["rss_kb"]) / 1024 for row in resources]
    hold_cpu = cpu[min(ramp_seconds, len(cpu) - 1):min(scheduled_duration_seconds, len(cpu))]
    hold_rss = rss[min(ramp_seconds, len(rss) - 1):min(scheduled_duration_seconds, len(rss))]
    return {
        "run": name,
        "jtl": str(jtl.relative_to(ROOT)),
        "monitor": str(monitor.relative_to(ROOT)),
        "samples": len(rows),
        "ramp_seconds": ramp_seconds,
        "scheduled_duration_seconds": scheduled_duration_seconds,
        "duration_seconds": round(duration, 3),
        "throughput_samples_per_second": round(len(rows) / duration, 4),
        "http_requests": len(http_rows),
        "http_requests_per_second": round(len(http_rows) / duration, 4),
        "hold_samples": len(hold_rows),
        "hold_throughput_samples_per_second": round(len(hold_rows) / hold_seconds, 4),
        "hold_http_requests": len(hold_http_rows),
        "hold_http_requests_per_second": round(len(hold_http_rows) / hold_seconds, 4),
        "hold_window_rps": hold_window_rps,
        "hold_window_http_rps": hold_http_rps,
        "hold_first_to_last_percent": round(100 * (hold_window_rps[-1] - hold_window_rps[0]) / hold_window_rps[0], 3),
        "hold_http_first_to_last_percent": round(100 * (hold_http_rps[-1] - hold_http_rps[0]) / hold_http_rps[0], 3),
        "mean_ms": round(mean(elapsed), 3),
        "median_ms": round(median(elapsed), 3),
        "p95_ms": percentile(elapsed, 95),
        "p99_ms": percentile(elapsed, 99),
        "max_ms": max(elapsed),
        "failed": len(failed),
        "http_errors": len(http_errors),
        "http_error_rate_percent": round(100 * len(http_errors) / len(rows), 4),
        "assertion_failures": len(assertions),
        "assertion_failure_rate_percent": round(100 * len(assertions) / len(rows), 4),
        "cpu_percent_max": max(cpu),
        "hold_cpu_percent_max": max(hold_cpu),
        "rss_mb_min": round(min(rss), 3),
        "rss_mb_max": round(max(rss), 3),
        "rss_mb_start": round(rss[0], 3),
        "rss_mb_end": round(rss[-1], 3),
        "hold_rss_mb_start": round(hold_rss[0], 3),
        "hold_rss_mb_end": round(hold_rss[-1], 3),
        "hold_rss_growth_percent": round(100 * (hold_rss[-1] - hold_rss[0]) / hold_rss[0], 3),
        "monitor_samples": len(resources),
        "backend_pid": int(resources[0]["pid"]),
    }


def main():
    missing = [str(path) for _, _, _, jtl, monitor in RUNS for path in (jtl, monitor) if not path.is_file()]
    if missing:
        raise SystemExit("Missing completed-run evidence:\n" + "\n".join(missing))
    output = {
        "acceptance_criteria": {
            "http_error_rate_percent_lt": 1,
            "p95_ms_lt": 1000,
            "cpu_percent_lt": 85,
            "memory": "no sustained monotonic growth across the hold period",
        },
        "runs": [summarize(*run) for run in RUNS],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
