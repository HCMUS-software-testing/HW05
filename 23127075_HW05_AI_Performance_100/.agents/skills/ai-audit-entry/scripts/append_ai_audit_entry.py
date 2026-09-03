#!/usr/bin/env python3
"""Append an AI audit entry to the submission report."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_AUDIT_FILE = Path("src/ai-audit/ai_audit_report.md")
DEFAULT_TOOL_MODEL = "Codex / GPT-5"
MANUAL_PLACEHOLDER = "[Manual by user]"
SUMMARY_TABLE_HEADER = (
    "| STT | Prompt + Tool | Verdict |\n"
    "| --- | --- | --- |"
)
LEGACY_TABLE_HEADER = (
    "| STT | Prompt + Tool | AI Output | Verdict | Reasoning | Student Fix |\n"
    "| --- | --- | --- | --- | --- | --- |"
)
SECTION_HEADINGS = {
    "group": "## 1. Thông tin nhóm",
    "audit": "## 2. Bảng audit",
    "accuracy": "## 3. Tổng kết độ chính xác AI",
    "conclusion": "## 4. Kết luận",
    "disclosure": "## 5. Disclosure",
}
AUDIT_SUBHEADINGS = {
    "summary": "### 2.1. Tóm tắt audit",
    "details": "### 2.2. Chi tiết audit",
}


@dataclass
class AuditEntry:
    prompt_tool: str
    ai_output: str
    verdict: str = MANUAL_PLACEHOLDER
    reasoning: str = MANUAL_PLACEHOLDER
    student_fix: str = MANUAL_PLACEHOLDER
    original_index: int | None = None
    full_output: bool = False


def table_cell(value: str) -> str:
    """Format arbitrary text for a single Markdown table cell."""
    stripped = value.strip()
    if not stripped:
        return ""
    return (
        stripped.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "<br>")
    )


def detail_value(value: str) -> str:
    """Keep detail fields readable and single-line for predictable parsing."""
    return table_cell(summarize_cell(value)).strip()


def detail_block(value: str) -> str:
    """Preserve a contiguous generated artifact exactly in the detail log."""
    return value.strip()


def fenced_block(value: str, language: str = "markdown") -> str:
    """Fence full artifact output so its headings do not affect audit sections."""
    stripped = value.strip()
    longest_backticks = max((len(match) for match in re.findall(r"`+", stripped)), default=0)
    fence = "`" * max(3, longest_backticks + 1)
    return f"{fence}{language}\n{stripped}\n{fence}"


def unfence_block(value: str) -> tuple[str, bool]:
    """Return the content inside a full-output fence if present."""
    stripped = value.strip()
    match = re.match(
        r"^(?P<fence>`{3,})[A-Za-z0-9_-]*\n(?P<body>.*)\n(?P=fence)$",
        stripped,
        flags=re.DOTALL,
    )
    if not match:
        return stripped, False
    return match.group("body").strip(), True


def detail_field(label: str, value: str) -> list[str]:
    stripped = value.strip()
    if "\n" in stripped:
        return [f"**{label}:**", "", stripped]
    return [f"**{label}:** {stripped}"]


def ai_output_field(entry: AuditEntry) -> list[str]:
    if entry.full_output:
        return ["**AI Output:**", "", fenced_block(entry.ai_output)]
    return detail_field("AI Output", entry.ai_output)


def prompt_tool_value(timestamp: str, tool_model: str, prompt: str) -> str:
    """Keep the user's prompt complete for audit traceability."""
    return f"Time: `{timestamp}`\nTool: `{tool_model}`\nPrompt:\n{prompt.strip()}"


def summarize_cell(value: str, max_chars: int = 220) -> str:
    """Keep audit fields concise while preserving readable evidence."""
    normalized = re.sub(r"\s+", " ", value.strip())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + "..."


def split_markdown_row(line: str) -> list[str]:
    parts = re.split(r"(?<!\\)\|", line.strip())
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [part.strip() for part in parts]


def initial_report() -> str:
    return f"""# AI Audit Report

{SECTION_HEADINGS["group"]}

- Họ tên: `Lê Trung Kiên`
- MSSV: `23127075`
- Nhóm/Lớp: `[TODO]`

{build_audit_section([])}

{SECTION_HEADINGS["accuracy"]}

- Các nội dung AI tạo đã được rà soát với yêu cầu bài làm: `[TODO]`
- Mức độ chính xác/độ hữu ích tổng quan: `[TODO]`
- Giới hạn hoặc rủi ro còn lại: `[TODO]`

{SECTION_HEADINGS["conclusion"]}

`[TODO]`

{SECTION_HEADINGS["disclosure"]}

`[TODO]`
"""


def build_audit_section(entries: list[AuditEntry]) -> str:
    summary_lines = [SECTION_HEADINGS["audit"], "", AUDIT_SUBHEADINGS["summary"], "", SUMMARY_TABLE_HEADER]
    for index, entry in enumerate(entries, start=1):
        summary_lines.append(
            f"| {index} | {table_cell(entry.prompt_tool)} | {table_cell(entry.verdict)} |"
        )

    detail_lines = ["", AUDIT_SUBHEADINGS["details"]]
    for index, entry in enumerate(entries, start=1):
        detail_lines.extend(
            [
                "",
                f"### 2.2.{index} Entry {index}",
                "",
                *detail_field("Prompt + Tool", entry.prompt_tool),
                "",
                *ai_output_field(entry),
                "",
                *detail_field("Verdict", entry.verdict),
                "",
                *detail_field("Reasoning", entry.reasoning),
                "",
                *detail_field("Student Fix", entry.student_fix),
            ]
        )

    return "\n".join(summary_lines + detail_lines)


def append_entry(
    audit_file: Path,
    purpose: str,
    prompt: str,
    output: str,
    tool_model: str,
    full_output: bool = False,
) -> None:
    del purpose
    audit_file.parent.mkdir(parents=True, exist_ok=True)
    text = audit_file.read_text(encoding="utf-8") if audit_file.exists() else initial_report()
    text = normalize_report_sections(text)
    entries = extract_audit_entries(text)

    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%Y-%m-%d %H:%M %Z")
    prompt_tool = prompt_tool_value(now, tool_model, prompt)
    entries.append(
        AuditEntry(
            prompt_tool=prompt_tool,
            ai_output=detail_block(output) if full_output else detail_value(output),
            full_output=full_output,
        )
    )

    text = replace_audit_section(text, entries)
    audit_file.write_text(text.rstrip() + "\n", encoding="utf-8")


def normalize_report_sections(text: str) -> str:
    """Ensure the report follows the teacher-provided section structure."""
    text = remove_legacy_sections(text)
    text = normalize_numbered_headings(text)

    if SECTION_HEADINGS["audit"] not in text:
        text = initial_report().rstrip() + "\n\n" + text.strip() + "\n"

    entries = extract_audit_entries(text)
    text = replace_audit_section(text, entries)

    required_sections = [
        (SECTION_HEADINGS["accuracy"], "- `[TODO]`"),
        (SECTION_HEADINGS["conclusion"], "`[TODO]`"),
        (SECTION_HEADINGS["disclosure"], "`[TODO]`"),
    ]
    for heading, placeholder in required_sections:
        if heading not in text:
            text = text.rstrip() + f"\n\n{heading}\n\n{placeholder}\n"
    return text


def normalize_numbered_headings(text: str) -> str:
    replacements = {
        r"^## (?:\d+\.\s*)?Thông tin nhóm\s*$": SECTION_HEADINGS["group"],
        r"^## (?:\d+\.\s*)?Bảng audit\s*$": SECTION_HEADINGS["audit"],
        r"^## (?:\d+\.\s*)?Tổng kết độ chính xác AI\s*$": SECTION_HEADINGS["accuracy"],
        r"^## (?:\d+\.\s*)?Kết luận\s*$": SECTION_HEADINGS["conclusion"],
        r"^## (?:\d+\.\s*)?Disclosure\s*$": SECTION_HEADINGS["disclosure"],
        r"^### (?:2\.1\.\s*)?(?:Tóm tắt audit|Bảng tóm tắt)\s*$": AUDIT_SUBHEADINGS["summary"],
        r"^### (?:2\.2\.\s*)?(?:Chi tiết audit|Danh sách entry|Audit entries)\s*$": AUDIT_SUBHEADINGS["details"],
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


def remove_legacy_sections(text: str) -> str:
    """Remove sections generated by the previous audit format."""
    legacy_headings = [
        "## AI Tool Usage Summary",
        "## Prompt and Output Log",
        "## Integrity Notes",
    ]
    for heading in legacy_headings:
        pattern = rf"\n?{re.escape(heading)}\n.*?(?=\n## |\Z)"
        text = re.sub(pattern, "\n", text, flags=re.DOTALL)
    return text.strip() + "\n"


def extract_audit_entries(text: str) -> list[AuditEntry]:
    detail_entries = extract_detail_entries(text)
    if detail_entries:
        return reconcile_summary_and_detail_entries(text, detail_entries)
    return extract_legacy_table_entries(text)


def reconcile_summary_and_detail_entries(
    text: str, detail_entries: list[AuditEntry]
) -> list[AuditEntry]:
    """Preserve only entries still present in both audit subsections.

    Users may delete an entry from either the summary table or the detailed
    section. Treat either deletion as intentional, then rebuild both sections
    from the surviving details so numbering is normalized on every write.
    """
    summary_indices = extract_summary_entry_indices(text)
    if summary_indices is None:
        return detail_entries

    surviving_indices = set(summary_indices)
    return [
        entry
        for entry in detail_entries
        if entry.original_index is not None and entry.original_index in surviving_indices
    ]


def extract_summary_entry_indices(text: str) -> list[int] | None:
    summary_heading = AUDIT_SUBHEADINGS["summary"]
    start = text.find(summary_heading)
    if start == -1:
        return None

    end = text.find(f"\n{AUDIT_SUBHEADINGS['details']}", start)
    if end == -1:
        end = text.find(f"\n{SECTION_HEADINGS['accuracy']}", start)
    if end == -1:
        end = len(text)

    indices: list[int] = []
    for line in text[start:end].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        if not cells or cells[0] in {"STT", "---"}:
            continue
        try:
            indices.append(int(cells[0]))
        except ValueError:
            continue
    return indices


def extract_detail_entries(text: str) -> list[AuditEntry]:
    detail_heading = AUDIT_SUBHEADINGS["details"]
    start = text.find(detail_heading)
    if start == -1:
        return []

    end = text.find(f"\n{SECTION_HEADINGS['accuracy']}", start)
    if end == -1:
        end = len(text)
    detail_text = text[start:end]

    pattern = re.compile(
        r"^### 2\.2\.(?P<index>\d+) Entry \d+\n"
        r"\n\*\*Prompt \+ Tool:\*\*\s*(?P<prompt>.+?)\n"
        r"\n\*\*AI Output:\*\*\s*(?P<output>.+?)\n"
        r"\n\*\*Verdict:\*\*\s*(?P<verdict>.+?)\n"
        r"\n\*\*Reasoning:\*\*\s*(?P<reasoning>.+?)\n"
        r"\n\*\*Student Fix:\*\*\s*(?P<student_fix>.+?)"
        r"(?=\n### 2\.2\.|\n## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    entries: list[AuditEntry] = []
    for match in pattern.finditer(detail_text):
        output, output_was_fenced = unfence_block(match.group("output"))
        entries.append(
            AuditEntry(
                prompt_tool=match.group("prompt").strip(),
                ai_output=output,
                verdict=match.group("verdict").strip(),
                reasoning=match.group("reasoning").strip(),
                student_fix=match.group("student_fix").strip(),
                original_index=int(match.group("index")),
                full_output=output_was_fenced or "\n" in output,
            )
        )
    return entries


def extract_legacy_table_entries(text: str) -> list[AuditEntry]:
    if LEGACY_TABLE_HEADER not in text:
        return []

    start = text.find(LEGACY_TABLE_HEADER) + len(LEGACY_TABLE_HEADER)
    end = text.find("\n## ", start)
    if end == -1:
        end = len(text)

    rows = []
    for line in text[start:end].splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = split_markdown_row(line)
        if len(cells) != 6:
            continue
        rows.append(cells)

    entries: list[AuditEntry] = []
    for cells in rows:
        entries.append(
            AuditEntry(
                prompt_tool=cells[1],
                ai_output=cells[2],
                verdict=cells[3],
                reasoning=cells[4],
                student_fix=cells[5],
            )
        )
    return entries


def replace_audit_section(text: str, entries: list[AuditEntry]) -> str:
    audit_start = text.find(SECTION_HEADINGS["audit"])
    if audit_start == -1:
        return text.rstrip() + "\n\n" + build_audit_section(entries) + "\n"

    after_audit = text.find(f"\n{SECTION_HEADINGS['accuracy']}", audit_start)
    if after_audit == -1:
        after_audit = len(text)

    before = text[:audit_start].rstrip()
    after = text[after_audit:].lstrip("\n")
    rebuilt = build_audit_section(entries)
    if before:
        rebuilt_text = before + "\n\n" + rebuilt
    else:
        rebuilt_text = rebuilt
    if after:
        rebuilt_text += "\n\n" + after
    return rebuilt_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-file", type=Path, default=DEFAULT_AUDIT_FILE)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--prompt", required=True)
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument("--output")
    output_group.add_argument(
        "--output-file",
        type=Path,
        help=(
            "Path to a single AI-created artifact. The file content is used "
            "verbatim as the detailed AI Output when the artifact is contiguous."
        ),
    )
    output_group.add_argument(
        "--output-summary",
        dest="output",
        help="Backward-compatible alias for --output.",
    )
    parser.add_argument(
        "--tool-model",
        default=DEFAULT_TOOL_MODEL,
        help=(
            "AI tool and model/version used, for example "
            "'Codex / GPT-5' or 'Claude Sonnet'."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = (
        args.output_file.read_text(encoding="utf-8")
        if args.output_file is not None
        else args.output
    )
    append_entry(
        audit_file=args.audit_file,
        purpose=args.purpose,
        prompt=args.prompt,
        output=output,
        tool_model=args.tool_model,
        full_output=args.output_file is not None,
    )


if __name__ == "__main__":
    main()
