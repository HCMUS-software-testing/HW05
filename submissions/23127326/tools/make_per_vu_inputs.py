#!/usr/bin/env python3
"""Create isolated repeated input files: one account per virtual user."""

import argparse
import csv
from pathlib import Path


def read_one(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return next(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=60)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    credentials = list(csv.DictReader((args.data_dir / "credentials.csv").open(newline="", encoding="utf-8-sig")))
    product = read_one(args.data_dir / "products.csv")
    order = read_one(args.data_dir / "orders.csv")
    if len(credentials) < args.count:
        raise RuntimeError(f"need {args.count} credential rows, found {len(credentials)}")
    output_dir = args.data_dir / "per-vu"
    output_dir.mkdir(exist_ok=True)
    fields = ["email", "password", "search", "page", "limit", "product_id", "product_name", "price", "quantity_initial", "quantity_updated", "shipping_address"]
    for index in range(1, args.count + 1):
        row = {**credentials[index - 1], **product, **order}
        path = output_dir / f"input-{index}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(row for _ in range(args.repeats))
    print(f"Wrote {args.count} per-VU files x {args.repeats} rows under {output_dir}")


if __name__ == "__main__":
    main()
