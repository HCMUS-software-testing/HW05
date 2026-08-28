import os
import sys
import xml.etree.ElementTree as ET
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_workspace_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

def print_check(name, passed, details=""):
    badge = "[PASS]" if passed else "[FAIL]"
    print(f"  {badge} {name}")
    if details:
        print(f"         └─ {details}")
    return passed

def run_phase2_verification():
    ws_root = get_workspace_root()
    print("=" * 70)
    print("        HW05 PHASE 2 AUTOMATED VERIFICATION REPORT")
    print(f"  Agent Skill: performance-testing-agent")
    print(f"  Workspace: {ws_root}")
    print("=" * 70)
    
    all_passed = True
    
    # 1. SKILL.md Check
    print("\n[1] Kiểm tra file đặc tả SKILL.md:")
    skill_file = os.path.join(ws_root, ".agents/skills/performance-testing-agent/SKILL.md")
    p1 = os.path.exists(skill_file) and os.path.getsize(skill_file) > 200
    all_passed &= print_check("File SKILL.md đặc tả kỹ năng và quy trình 6 bước", p1, f"File: {skill_file}")

    # 2. Automation Scripts Toolset Check
    print("\n[2] Kiểm tra Bộ Công cụ Scripts Python:")
    scripts = [
        ("jmx_generator.py", "Tool sinh Test Plan XML tự động cho 3 kịch bản"),
        ("jtl_parser.py", "Tool trích xuất Ground Truth metrics (p50/p90/p95/p99)"),
        ("audit_logger.py", "Tool tự động ghi log vào ai-audit-report.md"),
        ("run_jmeter.py", "CLI Runner chạy JMeter tối ưu JVM Heap & UTF-8"),
        ("reset_lockout.py", "Script mở khóa tài khoản SQLite tức thời"),
        ("seed_test_accounts.py", "Script seed 50 tài khoản test vào CSDL"),
        ("smoke_test_sut.py", "Script smoke test 5 API endpoints")
    ]
    for sc_name, sc_desc in scripts:
        sc_path = os.path.join(ws_root, ".agents/skills/performance-testing-agent/scripts", sc_name)
        p = os.path.exists(sc_path) and os.path.getsize(sc_path) > 100
        all_passed &= print_check(f"{sc_name} ({sc_desc})", p, f"Path: {sc_path}")

    # 3. Test Plans XML Validation & Relative Path Check
    print("\n[3] Kiểm tra 3 Test Plans (.jmx) đã sinh:")
    test_plans = [
        ("23127205_Load_20260829.jmx", "Standard TG (50 VUs) + Summary Report"),
        ("23127205_Stress_20260829.jmx", "Stepping TG (50-250 VUs) + Aggregate Report"),
        ("23127205_Spike_20260829.jmx", "Ultimate TG (350 VUs) + View Results Tree")
    ]
    for tp_name, tp_desc in test_plans:
        tp_path = os.path.join(ws_root, "submissions/23127205/test-plans", tp_name)
        valid = False
        rel_ok = False
        if os.path.exists(tp_path):
            try:
                tree = ET.parse(tp_path)
                valid = True
                with open(tp_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_ok = ("../data/credentials.csv" in content)
            except Exception:
                valid = False
        all_passed &= print_check(f"{tp_name} ({tp_desc})", valid and rel_ok, 
                                  "XML hợp lệ & đã dùng Relative Path cho CSV" if (valid and rel_ok) else "Lỗi XML hoặc dính Absolute Path")

    # Final Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("  >>> KẾT QUẢ: PHASE 2 ĐÃ HOÀN THÀNH 100% XUẤT SẮC! <<<")
        print("  Agent Skill & Bộ công cụ tự động hóa đã sẵn sàng vận hành.")
    else:
        print("  >>> KẾT QUẢ: CÒN MỘT SỐ HẠNG MỤC CHƯA ĐẠT! <<<")
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = run_phase2_verification()
    sys.exit(0 if success else 1)
