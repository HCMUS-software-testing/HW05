#!/usr/bin/env python3
"""Render the complete Markdown deliverables to print-quality PDFs.

Pandoc handles GitHub-flavoured Markdown and Chrome supplies a stable Unicode
PDF engine on macOS. The script validates page counts and required text so a
condensed or stale one-page export cannot silently replace the full reports.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
CSS = Path(__file__).with_name("report-print.css")

REPORTS = (
    {
        "markdown": REPORT_DIR / "main-report.md",
        "pdf": REPORT_DIR / "main-report.pdf",
        "minimum_pages": 4,
        "required": (
            "Thiết lập kịch bản",
            "Task 2 - Phản biện kết luận của AI",
            "Lockout reset runbook",
            "Kiểm thử hiệu năng liên tục",
            "Phụ lục - AI Critique",
            "https://youtu.be/lAfLKjpHHRM",
        ),
    },
    {
        "markdown": REPORT_DIR / "ai-audit-report.md",
        "pdf": REPORT_DIR / "ai-audit-report.pdf",
        "minimum_pages": 2,
        "required": (
            "Tên công cụ AI",
            "Ngày và giờ",
            "Prompt của bạn",
            "Đầu ra của AI",
            "Codex",
            "2026-08-30",
            "Chi tiết prompt và output",
            "khôi phục từ nhật ký công việc",
        ),
    },
    {
        "markdown": REPORT_DIR / "ai-critique.md",
        "pdf": REPORT_DIR / "ai-critique.pdf",
        "minimum_pages": 1,
        "required": (
            "356/3.287",
            "1.780/16.433",
            "cần profiling",
            "ảo giác",
        ),
    },
)


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def page_count(pdf: Path) -> int:
    output = subprocess.check_output(("pdfinfo", str(pdf)), text=True)
    for line in output.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Cannot determine page count for {pdf}")


def extract_text(pdf: Path, target: Path) -> str:
    run("pdftotext", "-layout", str(pdf), str(target))
    return target.read_text(encoding="utf-8")


def render(report: dict[str, object], temp_dir: Path) -> None:
    markdown = Path(report["markdown"])
    destination = Path(report["pdf"])
    html = temp_dir / f"{markdown.stem}.html"
    staged_pdf = temp_dir / destination.name

    run(
        "pandoc",
        "--from=gfm",
        "--to=html5",
        "--standalone",
        "--embed-resources",
        f"--css={CSS}",
        "--metadata",
        f"pagetitle={markdown.stem}",
        "--output",
        str(html),
        str(markdown),
    )
    html_text = html.read_text(encoding="utf-8")
    html.write_text(
        html_text.replace("<body>", f'<body class="{markdown.stem}">', 1),
        encoding="utf-8",
    )
    chrome_args = (
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--user-data-dir={temp_dir / (markdown.stem + '-chrome')}",
        f"--print-to-pdf={staged_pdf}",
        html.as_uri(),
    )
    chrome = subprocess.Popen(chrome_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    previous_size = -1
    stable_checks = 0
    for _ in range(300):
        if staged_pdf.is_file():
            size = staged_pdf.stat().st_size
            stable_checks = stable_checks + 1 if size == previous_size and size > 0 else 0
            previous_size = size
            if stable_checks >= 5:
                break
        if chrome.poll() is not None and not staged_pdf.is_file():
            raise RuntimeError(f"Chrome exited before creating {staged_pdf}")
        time.sleep(0.1)
    else:
        raise RuntimeError(f"Timed out while rendering {staged_pdf}")
    if chrome.poll() is None:
        chrome.terminate()
        try:
            chrome.wait(timeout=3)
        except subprocess.TimeoutExpired:
            chrome.kill()
            chrome.wait(timeout=3)

    pages = page_count(staged_pdf)
    if pages < int(report["minimum_pages"]):
        raise RuntimeError(f"{destination.name}: expected at least {report['minimum_pages']} pages, got {pages}")
    text = extract_text(staged_pdf, temp_dir / f"{markdown.stem}.txt")
    missing = [item for item in report["required"] if item not in text]
    if missing:
        raise RuntimeError(f"{destination.name}: required text missing: {missing}")

    shutil.copy2(staged_pdf, destination)
    print(f"{destination}: {pages} page(s), full Markdown verified")


def main() -> None:
    if not CHROME.is_file():
        raise RuntimeError(f"Chrome PDF engine not found: {CHROME}")
    if not CSS.is_file():
        raise RuntimeError(f"Print stylesheet not found: {CSS}")
    with tempfile.TemporaryDirectory(prefix="hw05-pdf-") as temp:
        temp_dir = Path(temp)
        for report in REPORTS:
            render(report, temp_dir)


if __name__ == "__main__":
    main()
