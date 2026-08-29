#!/usr/bin/env python3
"""Summarize a JMeter CSV JTL without inventing missing evidence."""

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def percentile(values, percentage):
    ordered = sorted(values)
    if not ordered:
        return None
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


def summarize(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get("label", "(unlabelled)")].append(row)
    output = {"source_rows": len(rows), "labels": {}}
    for label, samples in sorted(groups.items()):
        elapsed = [number(item.get("elapsed")) for item in samples]
        failed = [item for item in samples if item.get("success", "true").lower() != "true"]
        http_errors = [item for item in failed if is_http_error(item)]
        assertion_failures = [item for item in failed if item.get("failureMessage", "").strip() and not is_http_error(item)]
        timestamps = [number(item.get("timeStamp")) for item in samples if item.get("timeStamp")]
        span_seconds = (max(timestamps) - min(timestamps)) / 1000 if len(timestamps) > 1 else 0
        output["labels"][label] = {
            "samples": len(samples),
            "failed": len(failed),
            "http_errors": len(http_errors),
            "assertion_failures": len(assertion_failures),
            "failure_rate_percent": round(100 * len(failed) / len(samples), 4) if samples else 0,
            "throughput_samples_per_second": round(len(samples) / span_seconds, 4) if span_seconds > 0 else None,
            "mean_ms": round(mean(elapsed), 3) if elapsed else None,
            "median_ms": round(median(elapsed), 3) if elapsed else None,
            "p90_ms": percentile(elapsed, 90),
            "p95_ms": percentile(elapsed, 95),
            "p99_ms": percentile(elapsed, 99),
            "max_ms": max(elapsed) if elapsed else None,
        }
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jtl", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()
    if not args.jtl.is_file():
        parser.error(f"JTL does not exist: {args.jtl}")
    with args.jtl.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    result = summarize(rows)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    print(f"Source rows: {result['source_rows']}")
    print("| Label | Samples | Failed | HTTP errors | Assertion failures | p95 ms | Throughput/s |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for label, item in result["labels"].items():
        print(f"| {label} | {item['samples']} | {item['failed']} | {item['http_errors']} | {item['assertion_failures']} | {item['p95_ms']} | {item['throughput_samples_per_second']} |")


if __name__ == "__main__":
    main()
