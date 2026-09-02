#!/usr/bin/env python3
"""Static submission audit, JTL metrics check, and safe staging package builder."""
from __future__ import annotations
import argparse, csv, json, re, shutil, statistics, sys, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"Load": (10, 10, 5), "Stress": (50, 15, 10), "Spike": (100, 1, 3)}
EVIDENCE = ["evidence/hardware/fastfetch.png", "evidence/screenshots/htop_load.png",
            "evidence/screenshots/htop_stress.png", "evidence/screenshots/htop_spike.png"]

def jtl_metrics(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    elapsed = sorted(float(r["elapsed"]) for r in rows if r.get("elapsed"))
    ok = sum(r.get("success", "").lower() == "true" for r in rows)
    pct = lambda p: elapsed[min(len(elapsed)-1, max(0, int((p/100)*len(elapsed)+.999)-1))] if elapsed else 0
    return {"samples": len(rows), "success": ok, "errors": len(rows)-ok,
            "avg_ms": round(statistics.mean(elapsed), 2) if elapsed else 0,
            "p95_ms": pct(95), "p99_ms": pct(99), "max_ms": max(elapsed, default=0)}

def audit():
    findings, metrics = [], {}
    def check(condition, message): findings.append(("PASS" if condition else "FAIL", message))
    plans = list((ROOT / "test-plans").glob("*.jmx"))
    check(len(plans) == 3, f"JMX plans: {len(plans)}/3")
    for kind, expected in EXPECTED.items():
        plan = next((p for p in plans if kind.lower() in p.name.lower()), None)
        result = ROOT / "results" / kind.lower() / "raw.jtl"
        check(plan is not None, f"{kind} plan exists")
        check(result.exists(), f"{kind} raw JTL exists")
        if plan:
            text = plan.read_text(encoding="utf-8", errors="replace")
            try:
                root = ET.parse(plan).getroot()
                props = {x.attrib.get("name"): (x.text or "") for x in root.iter("stringProp")}
                check((props.get("ThreadGroup.num_threads"), props.get("ThreadGroup.ramp_time"),
                       props.get("LoopController.loops")) == tuple(map(str, expected)),
                      f"{kind} parameters = threads/ramp/loops {expected}")
                check("HTTPSamplerProxy" in text and "Assertion" in text, f"{kind} samplers and assertions present")
                check("CSVDataSet" in text, f"{kind} CSV data sources present")
                check("ResultCollector" in text, f"{kind} listener present")
            except ET.ParseError as e: check(False, f"{kind} JMX XML parses: {e}")
        if result.exists():
            metrics[kind] = jtl_metrics(result)
            check(metrics[kind]["errors"] == 0, f"{kind} JTL errors = {metrics[kind]['errors']}")
            check((ROOT / "results" / kind.lower() / "html-report" / "index.html").exists(), f"{kind} HTML report exists")
    for rel in ["README.md", "report/main-report.md", "report/ai-critique.md", "ai-audit/ai_audit_report.md", "run_tests.sh"]:
        check((ROOT / rel).exists(), f"required file: {rel}")
    for rel in EVIDENCE: check((ROOT / rel).is_file(), f"evidence: {rel}")
    docs = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in [ROOT/"README.md", ROOT/"report/main-report.md"])
    check("[TODO" not in docs, "README/main report contains no TODO placeholders")
    words = re.findall(r"\b[\w'-]+\b", (ROOT/"report/ai-critique.md").read_text(encoding="utf-8"))
    check(200 <= len(words) <= 300, f"AI critique word count = {len(words)} (required 200-300)")
    out = {"metrics": metrics, "findings": [{"status": s, "message": m} for s,m in findings]}
    (ROOT / "validation-report.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for status, msg in findings: print(f"[{status}] {msg}")
    print(f"\nValidation report: {ROOT/'validation-report.json'}")
    return not any(s == "FAIL" for s, _ in findings)

def package(destination: Path, passed: bool, allow_incomplete: bool = False):
    if not passed and not allow_incomplete:
        print("Package skipped: fix validation failures first (or use --allow-incomplete).")
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        staging = Path(td) / "23127075_HW05"
        shutil.copytree(ROOT, staging, ignore=shutil.ignore_patterns("*.zip", "__pycache__"))
        staging_report = staging / "validation-report.json"
        if staging_report.exists(): staging_report.unlink()
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as z:
            for file in staging.rglob("*"):
                if file.is_file(): z.write(file, file.relative_to(staging.parent))
    print(f"Package created: {destination}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, help="create ZIP from a temporary copied staging folder")
    parser.add_argument("--allow-incomplete", action="store_true", help="allow packaging despite validation failures")
    args = parser.parse_args()
    passed = audit()
    if args.package:
        # Run the package operation only after the same audit has passed.
        if not package(args.package, passed, args.allow_incomplete): passed = False
    sys.exit(0 if passed else 1)
