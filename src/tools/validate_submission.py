#!/usr/bin/env python3
"""Static submission audit, JTL metrics check, and safe staging package builder."""
from __future__ import annotations
import argparse, csv, json, re, shutil, sys, tempfile, zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from analyze_jtl import analyze_jtl, html_total

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"Load": (10, 10, 5), "Stress": (50, 15, 10), "Spike": (100, 1, 3)}
EVIDENCE = ["evidence/hardware/fastfetch.png", "evidence/screenshots/htop_load.png",
            "evidence/screenshots/htop_stress.png", "evidence/screenshots/htop_spike.png"]
SKILL = ROOT.parent / ".agents" / "skills" / "performance-testing-skills"

def jtl_metrics(path: Path):
    """Backward-compatible alias used by older validation reports."""
    return analyze_jtl(path)


def result_consistency(jtl: Path, statistics_path: Path, expected_samples: int | None = None) -> list[str]:
    """Return concrete result-integrity problems for one run."""
    metrics = analyze_jtl(jtl)
    findings = []
    if expected_samples is not None and metrics["samples"] != expected_samples:
        findings.append(f"JTL samples = {metrics['samples']}, expected {expected_samples}")
    report_samples = html_total(statistics_path)
    if report_samples is None:
        findings.append("HTML statistics.json has no Total sample count")
    elif report_samples != metrics["samples"]:
        findings.append(f"JTL samples = {metrics['samples']}, HTML samples = {report_samples}")
    return findings


def plan_assertions_valid(root: ET.Element) -> bool:
    """Require every HTTP sampler's adjacent subtree to assert HTTP 200."""
    for parent in root.iter():
        children = list(parent)
        for index, child in enumerate(children):
            if child.tag != "HTTPSamplerProxy":
                continue
            if index + 1 >= len(children) or children[index + 1].tag != "hashTree":
                return False
            assertions = [
                node for node in children[index + 1].iter("ResponseAssertion")
                if node.attrib.get("enabled", "true") == "true"
            ]
            valid = False
            for assertion in assertions:
                props = {node.attrib.get("name"): (node.text or "") for node in assertion.iter("stringProp")}
                values = [(node.text or "") for node in assertion.findall("./collectionProp/stringProp")]
                if props.get("Assertion.test_field") == "Assertion.response_code" and "200" in values:
                    valid = True
            if not valid:
                return False
    return True


def workflow_cleanup_findings(metrics: dict[str, object], cleanup: dict[str, object] | None) -> list[str]:
    labels = metrics.get("labels", {})
    creates = sum(count for label, count in labels.items() if "Create Product" in label)
    deletes = sum(count for label, count in labels.items() if "Delete Product Cleanup" in label)
    orphans = max(0, creates - deletes)
    if not orphans:
        return []
    if not cleanup:
        return [f"transactional imbalance: {creates} creates, {deletes} deletes"]
    deleted_ids = cleanup.get("deleted_ids", [])
    if cleanup.get("orphan_count") != orphans or len(deleted_ids) != orphans or cleanup.get("all_deleted") is not True:
        return [f"cleanup evidence does not account for {orphans} orphan products"]
    return []


def resource_log_findings(
    rows: list[dict[str, str]], minimum_span_s: float = 590,
    run_start_ms: float | None = None, run_end_ms: float | None = None,
) -> list[str]:
    if len(rows) < 2:
        return ["resource log has fewer than two samples"]
    try:
        timestamps = [datetime.fromisoformat(row["timestamp_utc"]) for row in rows]
        pids = {int(row["pid"]) for row in rows}
        rss = [float(row["rss_mib"]) for row in rows]
    except (KeyError, TypeError, ValueError):
        return ["resource log has invalid timestamp, PID, or RSS values"]
    findings = []
    if len(pids) != 1:
        findings.append("resource log contains multiple PIDs")
    span = (max(timestamps) - min(timestamps)).total_seconds()
    if span < minimum_span_s:
        findings.append(f"resource log span = {span:.3f}s, expected >= {minimum_span_s}s")
    if run_start_ms is not None and run_end_ms is not None:
        resource_start_ms = min(timestamp.timestamp() for timestamp in timestamps) * 1000
        resource_end_ms = max(timestamp.timestamp() for timestamp in timestamps) * 1000
        # The monitor samples every 5 seconds; allow one sampling interval at
        # either edge instead of requiring an artificial sample at test start/end.
        sampling_tolerance_ms = 5000
        if resource_start_ms > run_start_ms + sampling_tolerance_ms or resource_end_ms < run_end_ms - sampling_tolerance_ms:
            findings.append("resource log does not cover the JTL run window")
    if any(value <= 0 for value in rss):
        findings.append("resource log contains non-positive RSS")
    return findings


def package_root_name(destination: Path) -> str:
    match = re.fullmatch(r"(\d+_HW05_AI_Performance_(?:100|0\d{2}))\.zip", destination.name)
    if not match:
        raise ValueError("package name must be <StudentID>_HW05_AI_Performance_<000-100>.zip")
    return match.group(1)

def audit():
    findings, metrics = [], {}
    def check(condition, message): findings.append(("PASS" if condition else "FAIL", message))
    plans = list((ROOT / "test-plans").glob("*.jmx"))
    required_plans = [p for p in plans if any(f"_{kind}_" in p.name for kind in EXPECTED)]
    check(len(required_plans) == 3, f"required Load/Stress/Spike JMX plans: {len(required_plans)}/3")
    listener_types = []
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
                samplers = list(root.iter("HTTPSamplerProxy"))
                collectors = list(root.iter("ResultCollector"))
                check(len(samplers) == 6, f"{kind} sampler count = {len(samplers)}/6")
                check(plan_assertions_valid(root), f"{kind} has enabled HTTP 200 assertion per sampler")
                check("CSVDataSet" in text, f"{kind} CSV data sources present")
                check(len(collectors) == 1, f"{kind} has exactly one listener")
                if collectors: listener_types.append(collectors[0].attrib.get("guiclass"))
                labels = [sampler.attrib.get("testname", "") for sampler in samplers]
                check(not any("${" in label for label in labels), f"{kind} sampler labels are stable")
                check("/home/" not in text, f"{kind} uses no absolute home path")
            except ET.ParseError as e: check(False, f"{kind} JMX XML parses: {e}")
        if result.exists():
            metrics[kind] = jtl_metrics(result)
            check(metrics[kind]["errors"] == 0, f"{kind} JTL errors = {metrics[kind]['errors']}")
            html_dir = ROOT / "results" / kind.lower() / "html-report"
            check((html_dir / "index.html").exists(), f"{kind} HTML report exists")
            consistency = result_consistency(result, html_dir / "statistics.json", expected[0] * expected[2] * 6)
            check(not consistency, f"{kind} result consistency" + (f": {'; '.join(consistency)}" if consistency else ""))
    check(len(listener_types) == 3 and len(set(listener_types)) == 3,
          f"three distinct listeners: {', '.join(x or '<missing>' for x in listener_types)}")

    endurance_plan = next((p for p in plans if "_Endurance_" in p.name), None)
    endurance_jtl = ROOT / "results" / "endurance" / "raw.jtl"
    endurance_html = ROOT / "results" / "endurance" / "html-report"
    resource_log = ROOT / "results" / "endurance" / "backend-resources.csv"
    cleanup_log = ROOT / "results" / "endurance" / "cleanup-evidence.json"
    check(endurance_plan is not None, "Endurance JMX plan exists")
    check(endurance_jtl.exists(), "Endurance raw JTL exists")
    check((endurance_html / "index.html").exists(), "Endurance HTML report exists")
    check(resource_log.exists(), "Endurance backend resource log exists")
    if endurance_jtl.exists():
        metrics["Endurance"] = analyze_jtl(endurance_jtl)
        if resource_log.exists():
            with resource_log.open(newline="", encoding="utf-8") as stream:
                resource_problems = resource_log_findings(
                    list(csv.DictReader(stream)),
                    run_start_ms=metrics["Endurance"]["start_timestamp_ms"],
                    run_end_ms=metrics["Endurance"]["end_timestamp_ms"],
                )
            check(not resource_problems, "Endurance resource log integrity" + (f": {'; '.join(resource_problems)}" if resource_problems else ""))
        check(metrics["Endurance"]["duration_s"] >= 590, f"Endurance duration = {metrics['Endurance']['duration_s']}s (target >= 590s)")
        check(metrics["Endurance"]["errors"] == 0, f"Endurance JTL errors = {metrics['Endurance']['errors']}")
        problems = result_consistency(endurance_jtl, endurance_html / "statistics.json")
        check(not problems, "Endurance JTL/HTML consistency" + (f": {'; '.join(problems)}" if problems else ""))
        cleanup = json.loads(cleanup_log.read_text(encoding="utf-8")) if cleanup_log.exists() else None
        cleanup_problems = workflow_cleanup_findings(metrics["Endurance"], cleanup)
        check(not cleanup_problems, "Endurance transactional cleanup" + (f": {'; '.join(cleanup_problems)}" if cleanup_problems else ""))
    for rel in ["README.md", "report/main-report.md", "report/ai-critique.md", "ai-audit/ai_audit_report.md", "run_tests.sh"]:
        check((ROOT / rel).exists(), f"required file: {rel}")
    for rel in EVIDENCE: check((ROOT / rel).is_file(), f"evidence: {rel}")
    docs = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in [ROOT/"README.md", ROOT/"report/main-report.md"])
    check("[TODO" not in docs, "README/main report contains no TODO placeholders")
    youtube = re.search(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/\S+", docs)
    check(youtube is not None, "YouTube demo link exists")
    check((ROOT / "report" / "main-report.pdf").exists(), "main report PDF exists")
    check((ROOT / "ai-audit" / "ai_audit_report.pdf").exists(), "AI audit PDF exists")
    check(any((ROOT / "evidence" / "issues").glob("*.png")), "GitHub issue screenshot exists for documented SUT bug")
    check((SKILL / "SKILL.md").exists(), "performance-testing skill exists outside src")
    check((SKILL / "scripts" / "analyze_jtl.py").exists(), "skill includes reusable JTL analyzer")
    check((ROOT / "git-commit-log.txt").stat().st_size > 0, "git commit log is non-empty")
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
    try:
        root_name = package_root_name(destination)
    except ValueError as error:
        print(f"Package skipped: {error}")
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        staging = Path(td) / root_name
        shutil.copytree(ROOT, staging, ignore=shutil.ignore_patterns("*.zip", "__pycache__"))
        if SKILL.exists():
            shutil.copytree(SKILL, staging / "agent-skill" / "performance-testing-skills")
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
