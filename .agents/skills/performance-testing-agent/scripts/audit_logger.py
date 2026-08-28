import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

def log_ai_interaction(ai_tool, timestamp_str, prompt, ai_output, human_review_note=""):
    ws_root = get_workspace_root()
    report_dir = os.path.join(ws_root, "submissions", "23127205", "report")
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, "ai-audit-report.md")
    
    # Initialize header if not exists
    if not os.path.exists(report_file):
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Phụ lục: Báo cáo Kiểm toán Sử dụng AI (AI Audit Report)\n\n")
            f.write("**Sinh viên:** Lâm Hữu Khánh  \n")
            f.write("**MSSV:** 23127205  \n")
            f.write("**Mã bài tập:** HW05-AI - Kiểm thử Hiệu năng  \n")
            f.write("**Workflow:** `Login -> Search Product -> Product Detail -> Add to Cart -> Checkout`  \n\n")
            f.write("---\n\n")
            f.write("## 1. Khai báo Sử dụng AI (AI Usage Declaration)\n\n")
            f.write("> **Declaration:** *Tôi khai báo sử dụng công cụ AI (Google Antigravity IDE / Gemini 3.7 Flash) để hỗ trợ trong quá trình thực hiện bài tập này dưới sự kiểm soát và rà soát của con người (Human-in-the-loop):*\n")
            f.write("> - Phân tích yêu cầu và ánh xạ API endpoints.\n")
            f.write("> - Tạo dữ liệu test và sinh mã script tự động hóa.\n")
            f.write("> - Sinh cấu trúc XML JMeter Test Plan (`.jmx`).\n")
            f.write("> - Trích xuất số liệu Ground Truth từ raw `.jtl` log.\n")
            f.write("> - Phân tích lỗi hiệu năng và đề xuất tối ưu.\n\n")
            f.write("---\n\n")
            f.write("## 2. Nhật ký Tương tác AI (AI Interaction Logs)\n\n")
            
    # Count existing entries
    entry_count = 1
    if os.path.exists(report_file):
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r"### Entry #(\d+)", content)
            if matches:
                entry_count = max([int(m) for m in matches]) + 1

    # Append entry
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(f"### Entry #{entry_count:02d}\n\n")
        f.write(f"- **Thời gian:** `{timestamp_str}`\n")
        f.write(f"- **Công cụ AI:** {ai_tool}\n\n")
        f.write("#### Prompt:\n")
        f.write("```text\n")
        f.write(prompt.strip() + "\n")
        f.write("```\n\n")
        f.write("#### AI Output:\n")
        f.write(f"{ai_output.strip()}\n\n")
        if human_review_note:
            f.write("#### Human Review & Action:\n")
            f.write(f"> {human_review_note.strip()}\n\n")
        f.write("---\n\n")
        
    print(f"[+] Appended Entry #{entry_count:02d} to: {report_file}")

if __name__ == "__main__":
    print("[*] AI Audit Logger is ready.")
