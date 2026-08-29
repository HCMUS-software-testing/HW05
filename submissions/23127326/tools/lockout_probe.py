#!/usr/bin/env python3
"""Run the isolated live lockout probe and write JSONL evidence."""

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def login(base_url, email, password):
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/login",
        data=json.dumps({"email": email, "password": password}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status, body = response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read().decode("utf-8")
    return {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "elapsed_ms": round((time.time() - started) * 1000, 3), "status": status, "body": body}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--wrong-password", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    events = []
    for _ in range(3):
        events.append(login(args.base_url, args.email, args.wrong_password))
    events.append(login(args.base_url, args.email, args.password))
    with args.output.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps(events, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
