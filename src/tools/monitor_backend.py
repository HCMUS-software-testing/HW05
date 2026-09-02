#!/usr/bin/env python3
"""Record CPU and RSS for the backend process during an endurance run."""
from __future__ import annotations

import argparse
import csv
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def discover_pid(pattern: str) -> int:
    result = subprocess.run(
        ["pgrep", "-fo", pattern], check=False, capture_output=True, text=True
    )
    if result.returncode or not result.stdout.strip():
        raise RuntimeError(f"No process matched: {pattern}")
    return int(result.stdout.strip())


def sample(pid: int) -> tuple[float, int]:
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "%cpu=,rss="],
        check=True,
        capture_output=True,
        text=True,
    )
    cpu, rss_kib = result.stdout.split()
    return float(cpu), int(rss_kib)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pid", type=int)
    parser.add_argument("--pattern", default="node .*server\\.js")
    parser.add_argument("--duration", type=int, default=610)
    parser.add_argument("--interval", type=float, default=5)
    args = parser.parse_args()
    pid = args.pid or discover_pid(args.pattern)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + args.duration
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["timestamp_utc", "pid", "cpu_pct", "rss_kib", "rss_mib"])
        while time.monotonic() < deadline:
            try:
                cpu, rss_kib = sample(pid)
            except (subprocess.CalledProcessError, ValueError):
                break
            writer.writerow([
                datetime.now(timezone.utc).isoformat(), pid, cpu, rss_kib,
                round(rss_kib / 1024, 3),
            ])
            stream.flush()
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
