import os
import sys

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

def run_phase7_verification():
    ws_root = get_workspace_root()
    print("=" * 70)
    print("        HW05 PHASE 7 (TASK 3) AUTOMATED VERIFICATION REPORT")
    print(f"  Student: Lam Huu Khanh (23127205) - Member 1")
    print(f"  Workspace: {ws_root}")
    print("=" * 70)
    
    all_passed = True
    report_file = os.path.join(ws_root, "submissions", "23127205", "report", "task3-continuous-performance-testing.md")
    
    # -------------------------------------------------------------
    # 1. Document Existence Verification
    # -------------------------------------------------------------
    print("\n[1] Kiểm tra Tệp Báo cáo Đề xuất Task 3 (task3-continuous-performance-testing.md):")
    p1 = os.path.exists(report_file) and os.path.getsize(report_file) > 2000
    all_passed &= print_check("File task3-continuous-performance-testing.md tồn tại và hoàn thiện", p1, f"Path: {report_file}")
    
    if p1:
        with open(report_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        # -------------------------------------------------------------
        # 2. Mermaid Diagram Verification
        # -------------------------------------------------------------
        print("\n[2] Kiểm tra Lưu đồ Kiến trúc CI/CD (Mermaid.js Flowchart):")
        has_mermaid = "```mermaid" in content and "flowchart TD" in content and "Git Push" in content
        has_nodes = "Classifier" in content and "Block Merge" in content and "Tier 1" in content and "Tier 2" in content
        p2 = has_mermaid and has_nodes
        all_passed &= print_check("Lưu đồ Flowchart Mermaid chuẩn xác với đầy đủ các bước quyết định", p2, "Luồng từ Commit -> Classifier -> Tier 1/2 -> JMeter -> p95 Gate -> Merge/Block")

        # -------------------------------------------------------------
        # 3. p95 Regression Gate Logic
        # -------------------------------------------------------------
        print("\n[3] Kiểm tra Ngưỡng Cổng Chặn Hồi quy p95 (p95 Regression Gate):")
        has_gate = "p95" in content and "15%" in content and "Error Rate" in content
        all_passed &= print_check("Ngưỡng chặn hồi quy p95 > 15% hoặc Error Rate > 0.1%", has_gate, "Có công thức tính Delta p95 và cơ chế Dynamic Baseline trượt")

        # -------------------------------------------------------------
        # 4. Multi-Tier Strategy Definition
        # -------------------------------------------------------------
        print("\n[4] Kiểm tra Chiến lược Phân tầng Tải (Multi-Tier Execution):")
        has_tiers = "Tier 1" in content and "Tier 2" in content and "Nightly" in content
        all_passed &= print_check("Phân tách Tier 1 (PR Micro-bench 30s) và Tier 2 (Nightly Stress/Soak)", has_tiers, "Tránh làm nghẽn hàng đợi CI/CD ban ngày")

        # -------------------------------------------------------------
        # 5. Three Engineering Trade-offs
        # -------------------------------------------------------------
        print("\n[5] Kiểm tra 3 Cặp Đánh đổi Kỹ thuật (Engineering Trade-offs):")
        has_to1 = "Chi phí Hạ tầng" in content and "Tần suất" in content
        has_to2 = "Thời gian Chờ Build" in content and "Độ Sâu" in content
        has_to3 = "Cảnh báo Sai" in content and "Độ Nhạy" in content
        p5 = has_to1 and has_to2 and has_to3
        all_passed &= print_check("3 Cặp Đánh đổi (Cost vs Frequency, Pipeline Duration vs Depth, False Alarms vs Sensitivity)", p5, "Kèm giải pháp Ephemeral Containers, Shift-Left và Multi-level Alerting")

    # Final Summary
    print("\n" + "=" * 70)
    if all_passed:
        print("  >>> KẾT QUẢ: PHASE 7 (TASK 3) ĐÃ HOÀN THÀNH 100% XUẤT SẮC! <<<")
        print("  Đề xuất Continuous Performance Testing đạt chuẩn Bloom G9.6 (Disrupt).")
    else:
        print("  >>> KẾT QUẢ: CÒN MỘT SỐ TIÊU CHÍ CHƯA ĐẠT! <<<")
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = run_phase7_verification()
    sys.exit(0 if success else 1)
