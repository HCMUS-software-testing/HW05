import os
import sys
import csv
import math
import json
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def calculate_percentile(sorted_data, percentile):
    if not sorted_data:
        return 0
    k = (len(sorted_data) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return d0 + d1

def parse_jtl(jtl_path):
    if not os.path.exists(jtl_path):
        raise FileNotFoundError(f"File not found: {jtl_path}")
        
    samplers = {}
    total_elapsed = []
    total_bytes = 0
    total_sent_bytes = 0
    start_time = None
    end_time = None
    
    with open(jtl_path, "r", encoding="utf-8", errors="replace") as f:
        first_line = f.readline()
        f.seek(0)
        delimiter = "\t" if "\t" in first_line else ","
        
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            if not row:
                continue
            label = (row.get("label") or "").strip()
            # Ignore corrupt rows or non-standard sampler labels
            if not label or label in ["timeStamp", "label"] or not (label.startswith("0") or "/" in label):
                continue
                
            try:
                elapsed = float(row.get("elapsed") or 0)
                ts = int(row.get("timeStamp") or 0)
                success_val = str(row.get("success") or "true").strip().lower()
                success = (success_val == "true")
                bytes_recv = int(row.get("bytes") or 0)
                bytes_sent = int(row.get("sentBytes") or 0)
            except (ValueError, TypeError):
                continue
                
            if ts > 1000000000: # Valid epoch timestamp
                if start_time is None or ts < start_time:
                    start_time = ts
                if end_time is None or (ts + elapsed) > end_time:
                    end_time = int(ts + elapsed)
                
            if label not in samplers:
                samplers[label] = {
                    "count": 0,
                    "errors": 0,
                    "elapsed_times": [],
                    "bytes": 0,
                    "sent_bytes": 0
                }
                
            samplers[label]["count"] += 1
            if not success:
                samplers[label]["errors"] += 1
            samplers[label]["elapsed_times"].append(elapsed)
            samplers[label]["bytes"] += bytes_recv
            samplers[label]["sent_bytes"] += bytes_sent
            
            total_elapsed.append(elapsed)
            total_bytes += bytes_recv
            total_sent_bytes += bytes_sent
            
    total_duration_sec = ((end_time - start_time) / 1000.0) if (start_time and end_time and end_time > start_time) else 1.0
    if total_duration_sec < 0.1:
        total_duration_sec = 1.0
        
    results = {
        "jtl_file": os.path.abspath(jtl_path),
        "total_duration_sec": round(total_duration_sec, 2),
        "total_samples": len(total_elapsed),
        "samplers": {},
        "overall": {}
    }
    
    for label, data in samplers.items():
        times = sorted(data["elapsed_times"])
        count = data["count"]
        errors = data["errors"]
        avg = sum(times) / count if count else 0
        min_val = times[0] if times else 0
        max_val = times[-1] if times else 0
        p50 = calculate_percentile(times, 50)
        p90 = calculate_percentile(times, 90)
        p95 = calculate_percentile(times, 95)
        p99 = calculate_percentile(times, 99)
        tps = count / total_duration_sec if total_duration_sec else 0
        
        results["samplers"][label] = {
            "samples": count,
            "errors": errors,
            "error_rate_pct": round((errors / count) * 100, 2) if count else 0,
            "avg_ms": round(avg, 2),
            "min_ms": round(min_val, 2),
            "max_ms": round(max_val, 2),
            "p50_ms": round(p50, 2),
            "p90_ms": round(p90, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "throughput_rps": round(tps, 2),
            "recv_kb_sec": round((data["bytes"] / 1024) / total_duration_sec, 2) if total_duration_sec else 0,
            "sent_kb_sec": round((data["sent_bytes"] / 1024) / total_duration_sec, 2) if total_duration_sec else 0
        }
        
    all_times = sorted(total_elapsed)
    all_count = len(all_times)
    total_errors = sum(d["errors"] for d in samplers.values())
    results["overall"] = {
        "samples": all_count,
        "errors": total_errors,
        "error_rate_pct": round((total_errors / all_count) * 100, 2) if all_count else 0,
        "avg_ms": round(sum(all_times) / all_count, 2) if all_count else 0,
        "min_ms": round(all_times[0], 2) if all_times else 0,
        "max_ms": round(all_times[-1], 2) if all_times else 0,
        "p50_ms": round(calculate_percentile(all_times, 50), 2) if all_times else 0,
        "p90_ms": round(calculate_percentile(all_times, 90), 2) if all_times else 0,
        "p95_ms": round(calculate_percentile(all_times, 95), 2) if all_times else 0,
        "p99_ms": round(calculate_percentile(all_times, 99), 2) if all_times else 0,
        "throughput_rps": round(all_count / total_duration_sec, 2) if total_duration_sec else 0,
        "recv_kb_sec": round((total_bytes / 1024) / total_duration_sec, 2) if total_duration_sec else 0,
        "sent_kb_sec": round((total_sent_bytes / 1024) / total_duration_sec, 2) if total_duration_sec else 0
    }
    
    return results

def format_markdown_table(metrics):
    md = []
    md.append(f"### Ground Truth Performance Metrics (`{os.path.basename(metrics['jtl_file'])}`)")
    md.append(f"- **Total Samples:** `{metrics['overall']['samples']:,}` requests")
    md.append(f"- **Total Test Duration:** `{metrics['total_duration_sec']} s`")
    md.append(f"- **Overall Throughput:** `{metrics['overall']['throughput_rps']} req/s`")
    md.append(f"- **Overall Error Rate:** `{metrics['overall']['error_rate_pct']}%` ({metrics['overall']['errors']} errors)\n")
    
    md.append("| Sampler / Label | # Samples | Error % | Average (ms) | Min (ms) | Max (ms) | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Throughput (req/s) |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    
    for label, s in sorted(metrics["samplers"].items()):
        md.append(f"| `{label}` | {s['samples']:,} | {s['error_rate_pct']}% | {s['avg_ms']} | {s['min_ms']} | {s['max_ms']} | {s['p50_ms']} | {s['p90_ms']} | {s['p95_ms']} | {s['p99_ms']} | {s['throughput_rps']} |")
        
    ov = metrics["overall"]
    md.append(f"| **TOTAL / OVERALL** | **{ov['samples']:,}** | **{ov['error_rate_pct']}%** | **{ov['avg_ms']}** | **{ov['min_ms']}** | **{ov['max_ms']}** | **{ov['p50_ms']}** | **{ov['p90_ms']}** | **{ov['p95_ms']}** | **{ov['p99_ms']}** | **{ov['throughput_rps']}** |")
    return "\n".join(md)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JMeter JTL Log Ground-Truth Parser")
    parser.add_argument("jtl_file", nargs="?", help="Path to raw .jtl log file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    if not args.jtl_file:
        print("[*] JTL Parser tool ready. Usage: python jtl_parser.py <path_to_raw.jtl>")
        sys.exit(0)
        
    res = parse_jtl(args.jtl_file)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(format_markdown_table(res))
