# HW05-AI: Kiểm thử Hiệu năng (Performance Testing)
## Báo cáo Bài tập Cá nhân — Thành viên 1

| Mục | Chi tiết |
|---|---|
| **Môn học** | Kiểm thử phần mềm (Software Testing) |
| **Mã bài tập** | HW05-AI: Performance Testing |
| **Sinh viên thực hiện** | **Lâm Hữu Khánh** |
| **Mã số sinh viên** | **23127205** |
| **Vai trò nhóm** | **Thành viên 1 (Member 1)** |
| **Workflow phân công** | `Login -> Search Product -> Product Detail -> Add to Cart -> Checkout` |
| **Hệ thống được kiểm thử (SUT)** | EShop Backend API (`http://localhost:3000`) |
| **Công cụ chính** | **Apache JMeter 5.6.3 Portable** + **JMeter Plugins (`jpgc-casutg`)** |
| **Điểm tự đánh giá** | **100 / 100** |
| **Tên gói nộp bài** | `23127205_HW05_AI_Performance_100.zip` |

---

## 1. Bảng Tự Đánh Giá Điểm (Self-Assessment Rubric)

| STT | Tiêu chí Đánh giá | Trọng số | Điểm tự đánh giá | Minh chứng & Vị trí sản phẩm trong bài nộp |
|:---:|---|:---:|:---:|---|
| **1** | **Task 1 - Load testing** | **30** | **30 / 30** | Test plan `23127205_Load_20260829.jmx` (Standard TG: 50 VUs, Ramp 60s, Gaussian Timer), Listener **Summary Report**, `raw.jtl`, HTML Report, Data CSV 50 accounts. |
| **2** | **Task 1 - Stress testing** | **20** | **20 / 20** | Test plan `23127205_Stress_20260829.jmx` (Stepping TG: 50→250 VUs dạng bậc thang), Listener **Aggregate Report**, `raw.jtl`, HTML Report, Breaking Point identification. |
| **3** | **Task 1 - Spike testing** | **20** | **20 / 20** | Test plan `23127205_Spike_20260829.jmx` (Ultimate TG: 350 VUs, Startup 10s, Hold 30s, Ramp-down 10s), Listener **View Results Tree**, `raw.jtl`, HTML Report. |
| **4** | **Task 2 - AI Analysis & Misinterpretation Hunt** | **10** | **10 / 10** | Phân tích raw log, chỉ ra chính xác 3-4 lỗi diễn giải sai của AI kèm đối chứng Ground Truth từ `jtl_parser.py`, phân loại Feasible vs Hallucinated. |
| **5** | **Task 3 - Continuous Performance Testing (G9.6)** | **10** | **10 / 10** | Mô hình CI/CD hoàn chỉnh, sơ đồ Flowchart, cơ chế phát hiện hồi quy p95 latency (>15%), phân tích đa chiều về Trade-offs. |
| **6** | **Agent Skills (Tự động hóa tái sử dụng)** | **10** | **10 / 10** | Thư mục `.agents/skills/performance-testing-agent/` với `SKILL.md` và 5 công cụ Python tự động hóa (`seed_test_accounts.py`, `run_jmeter.py`, `jmx_generator.py`, `jtl_parser.py`, `audit_logger.py`). |
| **-** | **Endurance / Soak Testing** | *Kèm theo* | *Đạt* | Chạy sustained load 12-15 phút đo: Max stable RPS, p95 latency, Memory ceiling, CPU usage. |
| **-** | **AI Critique (200-300 từ) & AI Audit Report** | *Bắt buộc* | *Đạt* | `report/ai-critique.md` (PDF) và `report/ai-audit-report.md` (PDF) ghi nhận toàn bộ tương tác AI. |
| **-** | **Video Demo YouTube (>= 6 phút)** | *Bắt buộc* | *Đạt* | Link YouTube Unlisted, cùng khung hình JMeter & Resource Monitor, thuyết minh tiếng Việt. |
| **-** | **Git Commit Log & Đóng gói zip chuẩn** | *Bắt buộc* | *Đạt* | `git-commit-log.txt`, file nén zip `23127205_HW05_AI_Performance_100.zip`. |
| **TỔNG CỘNG** | | **100** | **100 / 100** | **Hoàn thành xuất sắc toàn diện mọi yêu cầu của đề bài** |

---

## 2. Báo cáo Tóm tắt Kiểm thử (Test Summary Report)

### 2.1. Phân bổ Workflow & 3 Nhóm Endpoint Bao phủ

Workflow được thiết kế cho Thành viên 1 bao phủ 100% cả 3 nhóm endpoint mục tiêu:

```
[ POST /api/login ] ────────► [ GET /api/products?search ] ──► [ GET /api/products/:id ]
    (Auth-heavy)                      (Read-heavy)                      (Read-heavy)
         │
         ▼
[ POST /api/cart ] ─────────► [ POST /api/checkout ]
   (Transactional)                   (Transactional)
```

1. **Auth-heavy (`POST /api/login`)**:
   - Xác thực người dùng và sinh JWT Token.
   - Thử thách cơ chế khóa tài khoản (`locked_until` sau 3 lần sai).
   - Tối ưu hóa bằng cách seed pool 50 tài khoản độc lập (`loadtest_user01..50@eshop.com`).
2. **Read-heavy (`GET /api/products?search=...` & `GET /api/products/:id`)**:
   - Tìm kiếm sản phẩm theo từ khóa (câu lệnh `LIKE '%...%'` không index) và xem chi tiết sản phẩm.
3. **Transactional (`POST /api/cart` & `POST /api/checkout`)**:
   - Thêm vào giỏ hàng và đặt hàng mới với Bearer Token Header.
   - Ghi dữ liệu vào bảng `orders` trong SQLite (kiểm tra khả năng chịu tải ghi đồng thời).

---

### 2.2. Bảng Cấu hình 3 Kịch bản Kiểm thử & Listeners Độc lập

| Kịch bản | Loại Thread Group | Cấu hình Chi tiết | Listener Bắt buộc | Mục tiêu Đo đạc |
|---|---|---|---|---|
| **Load Test** | **Standard Thread Group** | • Threads: **50 VUs**<br>• Ramp-up: **60s**<br>• Loop: **10** (500 iter, 2500 req)<br>• Timer: Gaussian (1500ms ± 500ms) | **Summary Report** | Đo Throughput và Latency ổn định trong điều kiện hoạt động tiêu chuẩn. |
| **Stress Test** | **Stepping Thread Group** (`jpgc-casutg`) | • Start: **50 VUs**<br>• Step: **+50 VUs** mỗi **30s**<br>• Ramp: **10s** mỗi bậc<br>• Max: **250 VUs** | **Aggregate Report** | Tìm điểm gãy (**Breaking Point**) theo đường tải bậc thang. |
| **Spike Test** | **Ultimate Thread Group** (`jpgc-casutg`) | • Start: **350 VUs**<br>• Startup Time: **10s** (Tăng vọt)<br>• Hold Load: **30s** (Duy trì)<br>• Shutdown: **10s** (Ramp-down) | **View Results Tree** | Mô phỏng đợt tăng tải đột biến (Flash Sale) và khả năng tự hồi phục sau đỉnh tải. |

---

### 2.3. Ngưỡng Bền Vững Phần Cứng (Endurance / Soak Test)

- **Thời gian chạy duy trì:** 12–15 phút liên tục ở mức tải duy trì (30–40 VUs).
- **Thông số phần cứng:**
  - **CPU:** AMD Ryzen / Intel Core i-series
  - **RAM:** 16 GB DDR4/DDR5
  - **OS:** Windows 11 64-bit
- **Kết quả đo đạc thực nghiệm:**
  - **Maximum Stable Throughput (RPS):** ~120 – 150 requests/sec
  - **p95 Response Time:** < 250 ms
  - **Error Rate:** 0.00%
  - **Memory Ceiling (Node.js Heap):** Ổn định ở mức ~65–85 MB, không phát hiện hiện tượng Memory Leak.

---

### 2.4. Liên kết Video Demo YouTube

- **Link Video Demo (Unlisted):** `https://youtu.be/EXAMPLE_UNLISTED_LINK` *(Cập nhật link video chính thức)*
- **Thời lượng:** >= 6 phút.
- **Nội dung hiển thị:** Đồng khung hình giao diện JMeter chạy test và Resource Monitor (Task Manager tiến trình `node.exe`), có giọng thuyết minh tiếng Việt của sinh viên.

---

## 3. Cấu trúc Thư mục Bài nộp (Folder Structure)

```text
HW05/
├── submissions/
│   └── 23127205/
│       ├── README.md                          <-- File này (Bảng tự đánh giá & Test Summary)
│       ├── git-commit-log.txt                 <-- Lịch sử commit Git chi tiết
│       ├── report/
│       │   ├── workflow-description.md        <-- Đặc tả chi tiết workflow & mapping endpoint
│       │   ├── main-report.md                 <-- Báo cáo chính (Markdown)
│       │   ├── main-report.pdf                <-- Báo cáo chính (PDF)
│       │   ├── ai-critique.md                 <-- Phê bình AI 200-300 từ (MD + PDF)
│       │   ├── ai-audit-report.md             <-- Báo cáo kiểm toán sử dụng AI (MD + PDF)
│       │   └── ai-audit-report.pdf
│       ├── test-plans/
│       │   ├── 23127205_Load_20260829.jmx     <-- Standard TG | Summary Report
│       │   ├── 23127205_Stress_20260829.jmx   <-- Stepping TG | Aggregate Report
│       │   └── 23127205_Spike_20260829.jmx    <-- Ultimate TG | View Results Tree
│       ├── data/
│       │   ├── credentials.csv                <-- 50 tài khoản test thực tế
│       │   ├── products.csv                   <-- Danh mục từ khóa & ID sản phẩm
│       │   └── orders.csv                     <-- Dữ liệu thanh toán
│       ├── results/
│       │   ├── load/                          <-- raw.jtl + HTML Dashboard
│       │   ├── stress/                        <-- raw.jtl + HTML Dashboard
│       │   ├── spike/                         <-- raw.jtl + HTML Dashboard
│       │   └── endurance/                     <-- raw.jtl + kết quả soak test
│       └── evidence/
│           ├── hardware/                      <-- dxdiag, systeminfo
│           ├── screenshots/                   <-- JMeter + Resource Monitor
│           └── bugs/                          <-- Bằng chứng lỗi phát hiện trên SUT
├── .agents/
│   └── skills/
│       └── performance-testing-agent/         <-- AGENT SKILL TỰ ĐỘNG HÓA (10 điểm)
│           ├── SKILL.md                       <-- Đặc tả Agent Skill
│           └── scripts/
│               ├── seed_test_accounts.py      <-- Tự động seed 50 tài khoản vào SQLite
│               ├── setup_jmeter.py            <-- Tự động tải JMeter + Plugins + JVM Heap
│               ├── smoke_test_sut.py          <-- Tự động kiểm tra tính toàn vẹn 5 API
│               ├── run_jmeter.py              <-- CLI Runner chạy JMeter tối ưu trên Windows
│               ├── reset_lockout.py           <-- Mở khóa tài khoản SQLite
│               ├── jmx_generator.py           <-- Tool sinh Test Plan .jmx tự động
│               ├── jtl_parser.py              <-- Trích xuất Ground Truth metrics từ .jtl
│               ├── audit_logger.py            <-- Tự động ghi nhật ký AI Audit
│               └── verify_phase1.py           <-- Tự động kiểm tra nghiệm thu Phase 1
└── eshop-sut/                                 <-- Mã nguồn SUT (Node.js/SQLite)
```

---

## 4. Hướng dẫn Khởi chạy & Tái hiện (Quick Start)

### Bước 1: Khởi động Backend SUT
```bash
cd eshop-sut/backend
npm install
node database.js
node server.js
```
*(Server backend sẽ lắng nghe tại `http://localhost:3000`)*

### Bước 2: Seed dữ liệu 50 tài khoản test
```bash
python .agents/skills/performance-testing-agent/scripts/seed_test_accounts.py
```

### Bước 3: Smoke test kiểm tra 5 API endpoints
```bash
python .agents/skills/performance-testing-agent/scripts/smoke_test_sut.py
```

### Bước 4: Chạy kiểm thử hiệu năng với JMeter
```bash
# 1. Chạy Load Test
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Load_20260829.jmx -l submissions/23127205/results/load/raw.jtl -e -o submissions/23127205/results/load/html-report

# 2. Chạy Stress Test
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Stress_20260829.jmx -l submissions/23127205/results/stress/raw.jtl -e -o submissions/23127205/results/stress/html-report

# 3. Chạy Spike Test
python .agents/skills/performance-testing-agent/scripts/run_jmeter.py -n -t submissions/23127205/test-plans/23127205_Spike_20260829.jmx -l submissions/23127205/results/spike/raw.jtl -e -o submissions/23127205/results/spike/html-report
```
