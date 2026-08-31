#!/usr/bin/env bash
set -eo pipefail

submission_dir="$(cd "$(dirname "$0")/.." && pwd)"
archive_name="23127326_HW05_AI_Performance_100.zip"
archive_path="$submission_dir/$archive_name"
temp_dir="$(mktemp -d /tmp/hw05-package.XXXXXX)"
temp_archive="$temp_dir/$archive_name"

python3 -B "$submission_dir/tools/validate_canonical_metrics.py"

if rg -q 'TODO_ADD_(VIDEO_LINK|PERFORMANCE_VIDEO_LINK)' "$submission_dir/README.md" "$submission_dir/report/main-report.md"; then
  echo "Warning: video link is still pending manual replacement." >&2
fi

missing_pdf=0
for required_pdf in main-report.pdf ai-audit-report.pdf ai-critique.pdf; do
  if [[ ! -f "$submission_dir/report/$required_pdf" ]]; then
    echo "Error: report/$required_pdf has not been exported yet." >&2
    missing_pdf=1
  fi
done
if [[ "$missing_pdf" -ne 0 ]]; then
  echo "Export the three PDFs before creating the final ZIP." >&2
  exit 1
fi

(
  cd "$submission_dir"
  zip -r -q "$temp_archive" . \
    -x "./$archive_name" \
    -x "*/__pycache__/*" \
    -x "*.DS_Store" \
    -x "*/source-recordings/*"
)

unzip -tq "$temp_archive" >/dev/null
mv "$temp_archive" "$archive_path"
rmdir "$temp_dir"

printf 'Created and verified %s\n' "$archive_path"
