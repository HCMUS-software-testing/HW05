---
name: ai-audit-entry
description: Offer to append an AI audit entry for software-testing homework work in `src/`. Use for every prompt session before finishing, especially when Codex plans, edits, reviews, generates, or executes work for the submission; ask before writing the audit report.
---
# AI Audit Entry

## Workflow

Ask the user whether they want to append an audit entry before writing to:

`src/ai-audit/ai_audit_report.md`

`src/` is the student's submission folder. Keep all coursework artifacts and the audit report directly under `src/`; do not add a `submission/` wrapper folder. The final submission is a copied, renamed, zipped version of `src/`.

If the user says no, do not run the append script. If the user says yes, run the bundled script before the final response whenever meaningful work was performed:

```bash
rtk python3 .agents/skills/ai-audit-entry/scripts/append_ai_audit_entry.py \
  --audit-file "src/ai-audit/ai_audit_report.md" \
  --purpose "Short purpose of the session" \
  --prompt "Copy the user's prompt exactly, with no paraphrase or correction" \
  --output "Short factual summary of the AI output for the audit table" \
  --tool-model "Codex / GPT-5"
```

When the AI output is a single generated file, report, template, code file, Markdown artifact, or other contiguous artifact, use `--output-file path/to/artifact` instead of `--output`. In this case, the script must copy the artifact content verbatim into `2.2` `AI Output` because the AI-created result is continuous and can be fully quoted without reconstructing it from scattered conversation turns. The full output must be wrapped in a fenced code block so headings, tables, and lists inside the generated artifact do not become audit report sections. Keep using `--output` for fragmented outputs, multi-file work, command results, conclusions, or cases where a concise factual summary is clearer than a full artifact.

The `2.1` summary table stays short. Full generated artifacts belong only in `2.2` detail entries, inside fenced code blocks.

Follow the teacher-provided report sections exactly and number every top-level audit section:

- `1. Thông tin nhóm`
- `2. Bảng audit`
- `3. Tổng kết độ chính xác AI`
- `4. Kết luận`
- `5. Disclosure`

Inside `## 2. Bảng audit`, always maintain two numbered subsections:

- `### 2.1. Tóm tắt audit`
- `### 2.2. Chi tiết audit`

Each prompt session is one new numbered entry in both subsections. Before appending, the script must treat both subsections as authoritative deletion surfaces: if an existing entry was removed from either the summary table or the detailed entry list, do not recreate it from the other subsection. Keep only entries still present in both subsections, then rebuild both subsections from scratch with sequential numbering.

`2.1` is only a short summary table with these columns:

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |

`2.2` is the full audit log. Each entry must use its own heading:

- `### 2.2.1 Entry 1`
- `### 2.2.2 Entry 2`
- ...

Under each `2.2.x` entry, write these fields in order:

- `Prompt + Tool`
- `AI Output`
- `Verdict`
- `Reasoning`
- `Student Fix`

Fill `STT` with the next sequential number. Before appending a new entry, renumber all surviving summary rows and detailed entries from `1` in their current order because the user may manually delete any entry in the middle. Fill `Prompt + Tool` with the timestamp, AI tool/model, and the user's full prompt exactly as provided; never summarize, truncate, paraphrase, or correct the prompt text. Fill `AI Output` with a concise summary for ordinary sessions; for a single contiguous generated artifact supplied through `--output-file`, fill `AI Output` with the full artifact content fenced as Markdown/code. Keep these fields as manual placeholders because the student will complete them:

- `Verdict`: `[Manual by user]`
- `Reasoning`: `[Manual by user]`
- `Student Fix`: `[Manual by user]`

Do not create or maintain legacy sections such as `AI Tool Usage Summary`, `Prompt and Output Log`, or `Integrity Notes`.

## Language and Encoding

Use Vietnamese with full accents for new audit metadata that the AI writes itself, such as `Purpose`, brief factual notes, or non-verbatim summaries, unless the user explicitly requests another language.

For each audit entry, keep prompts and output summaries in their original language. Do not remove accents, add accents, or correct character encoding. The prompt is always copied in full. For `--output`, the script escapes Markdown table pipes, converts line breaks to `<br>`, and shortens long output text so ordinary entries remain concise. For `--output-file`, the script preserves the UTF-8 file content verbatim in the `2.2` detail entry and wraps it in a fenced code block.

Write and read the audit report as UTF-8. If using `--output-file`, the script copies that file as UTF-8 verbatim into the `Output` field.

## Entry Guidance

Use concise, factual text. Do not include private chain-of-thought, hidden policy, or long command outputs. Mention files changed or artifacts created when relevant.

`Prompt + Tool` must include the user's full prompt for that session. Do not translate, summarize, truncate, normalize spelling, add missing accents, or correct typos.

`AI Output` should be short and factual for ordinary sessions. Mention the changed files, generated artifacts, or conclusion rather than pasting a full report/code block into the report unless the AI output is one contiguous generated artifact. If the artifact is continuous and available as a single file, include the full content with `--output-file`.

Always record the clearest available tool and model/version in `Tool/Model`. Use `--tool-model` when known, for example `GPT-5.4`, `GPT-5.5`, or `Claude Sonnet`. If the exact version is not visible, use the tool family plus the most specific known model name instead of a generic value.

If the report file does not exist, create its parent directories under `src/` and initialize a minimal audit report structure with the required Vietnamese headings before appending.

## Project Submission Layout

- Work only in `src/` for the deliverable: JMeter plans, inputs, raw `.jtl` logs, HTML reports, screenshots, results, documentation, and `ai-audit/`.
- Do not put generated submission artifacts in the repository root, `req/`, or `docs/`.
- Before submission, copy `src/` to a separate staging folder, rename the copy according to the teacher's naming convention, inspect it for secrets and unwanted files, then zip that copied folder. Keep the working `src/` folder unchanged as the source of truth.
- Record the final copied-folder and ZIP names in the student's submission notes when known; never change or delete `src/` as part of packaging.

The script removes legacy audit sections before saving, rewrites `2. Bảng audit` into the new `2.1` + `2.2` structure, upgrades the older single-table format, reconciles deletions between summary/detail subsections, and renumbers surviving audit entries before appending the next entry.

Do not commit changes unless the user explicitly asks.
