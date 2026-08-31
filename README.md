# HW05-AI: Performance Testing - EShop Backend API
## MÔN HỌC: KIỂM THỬ PHẦN MỀM (SOFTWARE TESTING) — HCMUS

| Thông tin | Chi tiết |
|---|---|
| **Sinh viên thực hiện** | **Lâm Hữu Khánh** |
| **Mã số sinh viên** | **23127205** |
| **Vai trò nhóm** | **Thành viên 1 (Member 1)** |
| **Workflow phân công** | `Login -> Search Product -> Product Detail -> Add to Cart -> Checkout` |
| **Hệ thống kiểm thử (SUT)** | EShop Backend REST API (`http://localhost:3000`) |
| **Public GitHub Repository** | [`https://github.com/HCMUS-software-testing/HW05`](https://github.com/HCMUS-software-testing/HW05) |
| **GitHub Issues Bug Reports** | [`https://github.com/HCMUS-software-testing/HW05/issues`](https://github.com/HCMUS-software-testing/HW05/issues) |
| **Điểm tự đánh giá** | **100 / 100** |

**Hồ sơ bài nộp chi tiết của Sinh viên:** [`submissions/23127205/README.md`](submissions/23127205/README.md)

---

## 1. Hướng dẫn Khởi chạy và Tái hiện (Quick Start)

### Bước 1: Khởi động Backend SUT (Node.js & SQLite)
Mở một cửa sổ Terminal:
```bash
cd eshop-sut/backend
npm install
node server.js
```
*(Server backend sẽ lắng nghe tại `http://localhost:3000`)*

---

### Bước 2: Nạp dữ liệu 50 tài khoản test độc lập (Test Setup Fixture)
Mở một cửa sổ Terminal thứ hai:
```bash
python .agents/skills/performance-testing-agent/scripts/seed_test_accounts.py
```

---

### Bước 3: Smoke test kiểm tra 5 API endpoints
```bash
python .agents/skills/performance-testing-agent/scripts/smoke_test_sut.py
```
*(Đảm bảo cả 5 API đều phản hồi `200 OK` trước khi test tải)*

---

### Bước 4: Chạy kiểm thử hiệu năng với Apache JMeter

#### Cách A: Chạy bằng giao diện đồ họa (JMeter GUI)
```powershell
.\tools\apache-jmeter-5.6.3\bin\jmeter.bat
```
* Mở file kịch bản tương ứng trong `submissions/23127205/test-plans/` và bấm nút **Start**.

#### Cách B: Chạy tự động qua CLI Runner (Non-GUI Headless)
```bash
# 1. Chạy Load Test (50 VUs - Summary Report)
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Load_20260829.jmx -l submissions/23127205/results/load/raw.jtl -e -o submissions/23127205/results/load/html-report

# 2. Chạy Stress Test (250 VUs - Aggregate Report)
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Stress_20260829.jmx -l submissions/23127205/results/stress/raw.jtl -e -o submissions/23127205/results/stress/html-report

# 3. Chạy Spike Test (350 VUs - View Results Tree)
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Spike_20260829.jmx -l submissions/23127205/results/spike/raw.jtl -e -o submissions/23127205/results/spike/html-report
```

---

## 2. Danh mục Báo cáo Hoàn chỉnh (Markdown & PDF)

1. [Báo cáo Tổng thể Kiểm thử Hiệu năng (Main Report)](submissions/23127205/report/main-report.pdf)
2. [Báo cáo Phê bình Năng lực AI (AI Critique - 286 từ)](submissions/23127205/report/ai-critique.pdf)
3. [Báo cáo Kiểm toán Sử dụng AI (AI Audit Report - 14 logs)](submissions/23127205/report/ai-audit-report.pdf)
4. [Task 2: Săn Lỗi Diễn Giải Sai & Ảo Giác AI](submissions/23127205/report/task2-ai-analysis.pdf)
5. [Task 3: Đề xuất Continuous Performance Testing (G9.6)](submissions/23127205/report/task3-continuous-performance-testing.pdf)
6. [Báo cáo Chi tiết 11 Bugs Phát Hiện trên SUT](submissions/23127205/report/bug-report.pdf)
7. [Đặc tả Workflow 5 APIs & Endpoint Mapping](submissions/23127205/report/workflow-description.pdf)

---

## 3. Liên Kết Video Demo YouTube (Unlisted)

- 🎥 **Video Demo Tổng Thể HW05 (>= 6 phút):** [https://youtu.be/z5PPt3cIplY](https://youtu.be/z5PPt3cIplY)
- 🤖 **Video Demo Agent Skill Tự Động Hóa:** [https://youtu.be/cxdNTWo8-mE](https://youtu.be/cxdNTWo8-mE)
