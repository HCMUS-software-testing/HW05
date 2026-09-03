#!/usr/bin/env python3
"""Analyze JMeter CSV JTL files without external dependencies."""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter
from pathlib import Path


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[max(0, math.ceil(percentile / 100 * len(ordered)) - 1)]


def analyze_jtl(path: Path) -> dict[str, object]:
    """Return run-level metrics from a JMeter CSV result file."""
    elapsed: list[float] = []
    latency: list[float] = []
    starts: list[float] = []
    ends: list[float] = []
    successes = 0
    labels: Counter[str] = Counter()
    response_codes: Counter[str] = Counter()

    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        required = {"timeStamp", "elapsed", "success"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing JTL columns: {', '.join(sorted(missing))}")
        for row in reader:
            elapsed_ms = float(row["elapsed"])
            start_ms = float(row["timeStamp"])
            elapsed.append(elapsed_ms)
            starts.append(start_ms)
            ends.append(start_ms + elapsed_ms)
            if row.get("Latency") not in (None, ""):
                latency.append(float(row["Latency"]))
            successes += row.get("success", "").lower() == "true"
            labels[row.get("label", "<missing>")] += 1
            response_codes[row.get("responseCode", "<missing>")] += 1

    samples = len(elapsed)
    duration_s = (max(ends) - min(starts)) / 1000 if samples else 0.0
    return {
        "file": str(path),
        "samples": samples,
        "successes": successes,
        "errors": samples - successes,
        "error_rate_pct": round((samples - successes) * 100 / samples, 4) if samples else 0.0,
        "duration_s": round(duration_s, 3),
        "start_timestamp_ms": min(starts, default=None),
        "end_timestamp_ms": max(ends, default=None),
        "throughput_rps": round(samples / duration_s, 4) if duration_s else 0.0,
        "avg_elapsed_ms": round(statistics.mean(elapsed), 2) if elapsed else 0.0,
        "min_elapsed_ms": min(elapsed, default=0.0),
        "max_elapsed_ms": max(elapsed, default=0.0),
        "p95_elapsed_ms": _percentile(elapsed, 95),
        "p99_elapsed_ms": _percentile(elapsed, 99),
        "avg_latency_ms": round(statistics.mean(latency), 2) if latency else None,
        "labels": dict(sorted(labels.items())),
        "response_codes": dict(sorted(response_codes.items())),
    }


def html_total(path: Path) -> int | None:
    """Read the aggregate sample count from JMeter's HTML statistics file."""
    if not path.exists():
        return None
    statistics_data = json.loads(path.read_text(encoding="utf-8"))
    total = statistics_data.get("Total")
    return int(total["sampleCount"]) if isinstance(total, dict) and "sampleCount" in total else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jtl", nargs="+", type=Path, help="CSV JTL file(s) to analyze")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    results = [analyze_jtl(path) for path in args.jtl]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    print("file\tsamples\terrors\tduration_s\tthroughput_rps\tavg_elapsed_ms\tp95_elapsed_ms\tp99_elapsed_ms\tavg_latency_ms")
    for item in results:
        keys = ("file", "samples", "errors", "duration_s", "throughput_rps", "avg_elapsed_ms", "p95_elapsed_ms", "p99_elapsed_ms", "avg_latency_ms")
        print("\t".join(str(item[key]) for key in keys))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
