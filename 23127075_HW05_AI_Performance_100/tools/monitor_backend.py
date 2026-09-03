#!/usr/bin/env python3
"""Record CPU and RSS for the backend process during an endurance run."""
from __future__ import annotations

import argparse
import csv
import os
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


def proc_snapshot(pid: int) -> tuple[int, int]:
    process_fields = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()
    process_jiffies = int(process_fields[13]) + int(process_fields[14])
    cpu_fields = Path("/proc/stat").read_text(encoding="utf-8").splitlines()[0].split()[1:]
    return process_jiffies, sum(int(value) for value in cpu_fields)


def cpu_percent(previous: tuple[int, int], current: tuple[int, int], cpu_count: int) -> float:
    process_delta = current[0] - previous[0]
    total_delta = current[1] - previous[1]
    return round(process_delta / total_delta * cpu_count * 100, 3) if total_delta > 0 else 0.0


def rss_kib(pid: int) -> int:
    for line in Path(f"/proc/{pid}/status").read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1])
    raise RuntimeError(f"VmRSS unavailable for PID {pid}")


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
    previous = proc_snapshot(pid)
    time.sleep(args.interval)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["timestamp_utc", "pid", "cpu_interval_pct", "rss_kib", "rss_mib"])
        while time.monotonic() < deadline:
            try:
                current = proc_snapshot(pid)
                cpu = cpu_percent(previous, current, os.cpu_count() or 1)
                current_rss_kib = rss_kib(pid)
                previous = current
            except (FileNotFoundError, RuntimeError, ValueError):
                break
            writer.writerow([
                datetime.now(timezone.utc).isoformat(), pid, cpu, current_rss_kib,
                round(current_rss_kib / 1024, 3),
            ])
            stream.flush()
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
