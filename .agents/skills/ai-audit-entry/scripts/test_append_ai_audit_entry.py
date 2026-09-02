#!/usr/bin/env python3
"""Regression tests for append_ai_audit_entry.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("append_ai_audit_entry.py")
DEFAULT_AUDIT_FILE = Path("src/ai-audit/ai_audit_report.md")
SUMMARY_HEADER = "| STT | Prompt + Tool | Verdict |"
DETAIL_ENTRY_HEADING = "### 2.2.1 Entry 1"


def test_default_output_path_is_submission_ai_audit(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--purpose",
            "record default path",
            "--prompt",
            "append default audit",
            "--output",
            "default output",
            "--tool-model",
            "Codex / GPT-5",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_file = tmp_path / DEFAULT_AUDIT_FILE
    assert audit_file.exists()
    audit_text = audit_file.read_text(encoding="utf-8")
    assert SUMMARY_HEADER in audit_text
    assert "## 1. Thông tin nhóm" in audit_text
    assert "## 2. Bảng audit" in audit_text
    assert "### 2.1. Tóm tắt audit" in audit_text
    assert "### 2.2. Chi tiết audit" in audit_text
    assert "## 3. Tổng kết độ chính xác AI" in audit_text
    assert "## 4. Kết luận" in audit_text
    assert "## 5. Disclosure" in audit_text
    assert "| 1 |" in audit_text
    assert "append default audit" in audit_text
    assert DETAIL_ENTRY_HEADING in audit_text
    assert "**AI Output:**" in audit_text


def test_output_file_records_full_contiguous_artifact(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    artifact = tmp_path / "artifact.md"
    artifact_content = "# Generated Artifact\n\nLine 1\nLine 2\n"
    artifact.write_text(artifact_content, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "record generated artifact",
            "--prompt",
            "make an artifact",
            "--output-file",
            str(artifact),
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert "## 2. Bảng audit" in audit_text
    assert SUMMARY_HEADER in audit_text
    assert "**AI Output:** # Generated Artifact Line 1 Line 2" in audit_text


def test_unicode_prompt_and_output_are_preserved_verbatim(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    prompt = "Cập nhật báo cáo đăng ký tài khoản, giữ nguyên tiếng Việt có dấu."
    output = "Đã tạo: Điều kiện, Kết quả mong đợi, Cần rà soát thủ công."

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "cập nhật skill tiếng Việt",
            "--prompt",
            prompt,
            "--output",
            output,
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert prompt in audit_text
    assert output in audit_text


def test_report_does_not_create_ai_tool_usage_summary(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "record one entry",
            "--prompt",
            "make an entry",
            "--output",
            "entry output",
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert "## AI Tool Usage Summary" not in audit_text
    assert "| Date/Time | Tool/Model | Purpose |" not in audit_text
    assert "## Prompt and Output Log" not in audit_text
    assert "## 1. Thông tin nhóm" in audit_text
    assert "## 2. Bảng audit" in audit_text
    assert "### 2.1. Tóm tắt audit" in audit_text
    assert "### 2.2. Chi tiết audit" in audit_text
    assert "## 3. Tổng kết độ chính xác AI" in audit_text
    assert "## 4. Kết luận" in audit_text
    assert "## 5. Disclosure" in audit_text


def test_legacy_unnumbered_sections_are_renumbered(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    audit_file.write_text(
        """# AI Audit Report

## Thông tin nhóm

- Họ tên: `Lê Trung Kiên`

## Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |

### 2.2. Chi tiết audit

## Tổng kết độ chính xác AI

- `[TODO]`

## Kết luận

`[TODO]`

## Disclosure

`[TODO]`
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "migrate numbered sections",
            "--prompt",
            "append after migration",
            "--output",
            "migration output",
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert "## 1. Thông tin nhóm" in audit_text
    assert "## 2. Bảng audit" in audit_text
    assert "### 2.1. Tóm tắt audit" in audit_text
    assert "### 2.2. Chi tiết audit" in audit_text
    assert "## 3. Tổng kết độ chính xác AI" in audit_text
    assert "## 4. Kết luận" in audit_text
    assert "## 5. Disclosure" in audit_text
    assert "## Thông tin nhóm" not in audit_text


def test_entries_are_numbered_sequentially(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"

    for prompt in ["first prompt", "second prompt"]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--audit-file",
                str(audit_file),
                "--purpose",
                "record numbered entry",
                "--prompt",
                prompt,
                "--output",
                f"output for {prompt}",
                "--tool-model",
                "Codex / GPT-5",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr

    audit_text = audit_file.read_text(encoding="utf-8")
    assert "| 1 |" in audit_text
    assert "| 2 |" in audit_text
    assert "### 2.2.1 Entry 1" in audit_text
    assert "### 2.2.2 Entry 2" in audit_text


def test_existing_entries_are_renumbered_after_middle_deletion(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    audit_file.write_text(
        """# AI Audit Report

## 1. Thông tin nhóm

- Họ tên: `Lê Trung Kiên`

## 2. Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |
| 1 | Prompt one | [Manual by user] |
| 3 | Prompt three | [Manual by user] |

### 2.2. Chi tiết audit

### 2.2.1 Entry 1

**Prompt + Tool:** Prompt one

**AI Output:** Output one

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.3 Entry 3

**Prompt + Tool:** Prompt three

**AI Output:** Output three

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

## 3. Tổng kết độ chính xác AI

- `[TODO]`

## 4. Kết luận

`[TODO]`

## 5. Disclosure

`[TODO]`
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "renumber deleted entry gap",
            "--prompt",
            "append after deleting middle entry",
            "--output",
            "new output",
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    summary_rows = [
        line
        for line in audit_text.splitlines()
        if line.startswith("| ") and not line.startswith("| STT") and not line.startswith("| ---")
    ]
    assert [row.split("|")[1].strip() for row in summary_rows] == ["1", "2", "3"]
    assert "### 2.2.1 Entry 1" in audit_text
    assert "### 2.2.2 Entry 2" in audit_text
    assert "### 2.2.3 Entry 3" in audit_text
    assert "**Prompt + Tool:** Time:" in audit_text


def test_deleted_summary_row_removes_matching_detail_entry(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    audit_file.write_text(
        """# AI Audit Report

## 1. Thông tin nhóm

- Họ tên: `Lê Trung Kiên`

## 2. Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |
| 1 | Prompt one | [Manual by user] |
| 3 | Prompt three | [Manual by user] |

### 2.2. Chi tiết audit

### 2.2.1 Entry 1

**Prompt + Tool:** Prompt one

**AI Output:** Output one

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.2 Entry 2

**Prompt + Tool:** Prompt two

**AI Output:** Output two

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.3 Entry 3

**Prompt + Tool:** Prompt three

**AI Output:** Output three

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

## 3. Tổng kết độ chính xác AI

- `[TODO]`

## 4. Kết luận

`[TODO]`

## 5. Disclosure

`[TODO]`
""",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "renumber after summary row deletion",
            "--prompt",
            "append after deleting a summary row",
            "--output",
            "new output",
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert "Prompt one" in audit_text
    assert "Prompt two" not in audit_text
    assert "Prompt three" in audit_text
    assert "### 2.2.1 Entry 1" in audit_text
    assert "### 2.2.2 Entry 2" in audit_text
    assert "### 2.2.3 Entry 3" in audit_text


def test_long_output_is_summarized_for_table(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"
    long_output = " ".join(["generated-content"] * 40)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "record concise summary",
            "--prompt",
            "summarize long output",
            "--output",
            long_output,
            "--tool-model",
            "Codex / GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    summary_row = next(line for line in audit_text.splitlines() if line.startswith("| 1 |"))
    assert len(summary_row) < 500
    detail_line = next(line for line in audit_text.splitlines() if line.startswith("**AI Output:**"))
    assert len(detail_line) < 300
    assert "..." in detail_line


def test_table_cells_escape_pipes_and_newlines(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    audit_file = tmp_path / "audit.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-file",
            str(audit_file),
            "--purpose",
            "record table-safe entry",
            "--prompt",
            "make A | B",
            "--output",
            "line 1\nline | 2",
            "--tool-model",
            "Codex | GPT-5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    audit_text = audit_file.read_text(encoding="utf-8")
    assert "Codex \\| GPT-5" in audit_text
    assert "make A \\| B" in audit_text
    assert "line 1 line \\| 2" in audit_text


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_output_file_records_full_contiguous_artifact(temp_path / "output-file")
        test_default_output_path_is_submission_ai_audit(temp_path / "default-path")
        test_unicode_prompt_and_output_are_preserved_verbatim(temp_path / "unicode")
        test_report_does_not_create_ai_tool_usage_summary(temp_path / "no-summary")
        test_legacy_unnumbered_sections_are_renumbered(temp_path / "section-numbering")
        test_entries_are_numbered_sequentially(temp_path / "numbered")
        test_existing_entries_are_renumbered_after_middle_deletion(temp_path / "renumber-gap")
        test_deleted_summary_row_removes_matching_detail_entry(temp_path / "summary-row-deleted")
        test_long_output_is_summarized_for_table(temp_path / "concise")
        test_table_cells_escape_pipes_and_newlines(temp_path / "table-safe")
