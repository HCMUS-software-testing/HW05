#!/usr/bin/env python3
import csv, sys, statistics
from pathlib import Path
for name in sys.argv[1:] or ['results/load/raw.jtl','results/stress/raw.jtl','results/spike/raw.jtl']:
    rows=list(csv.DictReader(open(name, newline='')))
    times=[int(r['elapsed']) for r in rows]
    ok=[r['success'].lower()=='true' for r in rows]
    ordered=sorted(times)
    p95=ordered[max(0, int(len(ordered)*.95)-1)] if ordered else 0
    duration=(max(int(r['timeStamp']) for r in rows)-min(int(r['timeStamp']) for r in rows))/1000 if rows else 0
    print(f'{name}: samples={len(rows)} ok={sum(ok)} errors={len(rows)-sum(ok)} error_rate={(1-sum(ok)/len(rows))*100 if rows else 0:.2f}% avg_ms={statistics.mean(times) if times else 0:.1f} min_ms={min(times) if times else 0} max_ms={max(times) if times else 0} p95_ms={p95} throughput_rps={len(rows)/duration if duration else 0:.2f}')
