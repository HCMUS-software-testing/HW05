#!/usr/bin/env python3
"""Sample the local backend process for resource evidence."""

import argparse
import csv
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pid", type=int)
    parser.add_argument("output", type=Path)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("timestamp_utc", "pid", "cpu_percent", "rss_kb", "threads"))
        while True:
            try:
                os.kill(args.pid, 0)
            except ProcessLookupError:
                break
            result = subprocess.run(["ps", "-p", str(args.pid), "-o", "%cpu=,rss="], capture_output=True, text=True, check=False)
            values = result.stdout.strip().split()
            threads = subprocess.run(
                ["ps", "-M", "-p", str(args.pid)],
                capture_output=True,
                text=True,
                check=False,
            )
            thread_count = max(0, len(threads.stdout.strip().splitlines()) - 1)
            if len(values) >= 2:
                writer.writerow((datetime.now(timezone.utc).isoformat(), args.pid, values[0], values[1], thread_count))
                handle.flush()
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
