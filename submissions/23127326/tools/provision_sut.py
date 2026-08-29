#!/usr/bin/env python3
"""Provision synthetic Member 3 accounts through the local SUT register API."""

import argparse
import csv
import json
import urllib.error
import urllib.request
from pathlib import Path


def post(base_url, payload):
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/register",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).parents[1] / "data")
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    credential_path = args.data_dir / "credentials.csv"
    lockout_path = args.data_dir / "lockout-account.csv"
    credentials = []
    for index in range(1, args.count + 1):
        email = f"perf.m3.{index:03d}@example.test"
        password = f"PerfM3-2026!{index:03d}"
        status, body = post(args.base_url, {"name": f"Performance M3 {index:03d}", "email": email, "password": password})
        if status not in (200, 201):
            raise RuntimeError(f"register failed for {email}: HTTP {status} {body}")
        credentials.append((email, password))
    lockout_email = "perf.m3.lockout@example.test"
    lockout_password = "PerfM3-Lockout-2026!"
    status, body = post(args.base_url, {"name": "Performance M3 Lockout", "email": lockout_email, "password": lockout_password})
    if status not in (200, 201):
        raise RuntimeError(f"register failed for {lockout_email}: HTTP {status} {body}")
    with credential_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("email", "password"))
        writer.writerows(credentials)
    with lockout_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("email", "password", "wrong_password"))
        writer.writerow((lockout_email, lockout_password, "Wrong-Password-2026!"))
    print(f"Provisioned {len(credentials)} performance accounts and 1 lockout account")
    print(f"Wrote {credential_path} and {lockout_path}")


if __name__ == "__main__":
    main()
