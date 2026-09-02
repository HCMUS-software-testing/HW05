# HW05 - Performance Testing with AI (Admin Workflow)

- **Sinh viên**: Lê Trung Kiên
- **MSSV**: 23127075
- **Lớp**: Kiểm thử phần mềm (Software Testing) - HCMUS
- **Vai trò / Luồng thực thi**: Thành viên 4 (Admin Workflow)
- **Repository**: [https://github.com/HCMUS-software-testing/HW05](https://github.com/HCMUS-software-testing/HW05)

---

## 📊 1. Bảng Tự Đánh Giá Điểm (Self-Assessment Matrix)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá | Trạng thái / Ghi chú |
| --- | --- | ---: | ---: | --- |
| 1 | **Task 1 - Load testing** | 30 | **30** | Hoàn thành kịch bản 10 threads, 10s ramp-up, Aggregate Report, data CSV |
| 2 | **Task 1 - Stress testing** | 20 | **20** | Hoàn thành kịch bản 50 threads, 15s ramp-up, Summary Report |
| 3 | **Task 1 - Spike testing** | 20 | **20** | Hoàn thành kịch bản 100 threads, 1s ramp-up, View Results Tree |
| 4 | **Task 2 - AI analysis & misinterpretation hunt** | 10 | **10** | Phân tích 2 lỗi AI diễn giải sai chỉ số & phân loại Feasible vs Hallucinated DB optimizations |
| 5 | **Task 3 - Continuous Performance Testing proposal** | 10 | **10** | Đề xuất CI/CD Pipeline kèm sơ đồ Mermaid flowchart & phân tích trade-offs |
| 6 | **Agent Skills & Documentation** | 10 | **10** | Đầy đủ `SKILL.md`, `ai_audit_report.md` (9 entries), `run_tests.sh` |
| **TỔNG CỘNG** | | **100** | **100 / 100** | **Tên file ZIP nộp bài**: `23127075_HW05_AI_Performance_100.zip` |

---

## 📝 2. Tóm Tắt Kết Quả Kiểm Thử Hiệu Năng

### 2.1. Các kịch bản & Nhóm Endpoint bao phủ
Workflow của Member 4 (Admin Workflow) thực thi end-to-end qua 6 API Samplers:
- **Auth-heavy**: `POST /api/login` (Admin Authentication & JWT extraction)
- **Read-heavy**: `GET /api/admin/users` (Bearer token auth), `GET /api/products`, `GET /api/categories`
- **Transactional**: `POST /api/products` (Tạo sản phẩm test từ CSV), `DELETE /api/products/:id` (Cleanup sản phẩm)

### 2.2. Bảng Tóm tắt Kết quả Thực tế

| Kịch bản | Threads | Ramp-up | Total Requests | Throughput (RPS) | Latency trung bình | Tỷ lệ Lỗi (Error %) |
|---|---|---|---|---|---|---|
| **Load Test** | 10 | 10s | 300 | **4.7 req/s** | 10 ms | **0.00%** |
| **Stress Test** | 50 | 15s | 3,000 | **39.3 req/s** | 7 ms | **0.00%** |
| **Spike Test** | 100 | 1s | 1,800 | **338.2 req/s** | 225 ms | **0.00%** |

### 2.3. Ngưỡng Endurance (Soak Test)
- **RPS duy trì ổn định tối đa**: $\approx 35 - 40 \text{ req/s}$
- **Trần bộ nhớ (Memory Ceiling)**: $\approx 85 \text{ MB RAM}$ (Backend Node.js + SQLite đĩa đơn)
- **Số lượng Bug phát hiện**: 0 lỗi sập server (Error Rate 0.00%), phát hiện 1 lỗ hổng bảo mật SUT: API `POST/DELETE /api/products` không yêu cầu JWT auth middleware.

---

## 📹 3. Liên Kết Video Demo (YouTube Unlisted)

- **Link Video YouTube**: `[TODO: Dán link video YouTube unlisted >= 6 phút tại đây]`
- **Nội dung video**: Thuyết minh tiếng Việt luồng Admin + hiển thị giao diện JMeter và tiến trình `htop` / `fastfetch` đồng thời.

---

## 🛠️ 4. Hướng Dẫn Chạy Kiểm Thử (Quick Start)

1. **Khởi động Backend EShop**:
   ```bash
   cd eshop-sut/backend && npm start
   ```
2. **Thực thi toàn bộ kịch bản kiểm thử**:
   ```bash
   cd src
   chmod +x run_tests.sh
   ./run_tests.sh
   ```
3. **Kết quả**: Log `.jtl` và HTML Reports sẽ tự động sinh tại `src/results/`.

---

## 📁 5. Cấu Trúc Thư Mục Bài Nộp (`src/`)

```text
src/
├── ai-audit/
│   └── ai_audit_report.md        # Nhật ký AI Audit (9 Entries)
├── data/
│   ├── credentials.csv           # Dữ liệu tài khoản Admin
│   └── products.csv              # Dữ liệu sản phẩm mẫu
├── evidence/
│   ├── hardware/                 # Ảnh chụp fastfetch phần cứng
│   └── screenshots/              # Ảnh chụp htop quá trình chạy
├── report/
│   ├── ai-critique.md            # Phê bình phân tích AI (200-300 từ)
│   └── main-report.md            # Báo cáo chính (Task 1, 2, 3)
├── results/                      # Dữ liệu raw.jtl & HTML reports (Load, Stress, Spike)
├── test-plans/
│   ├── 23127075_Load_20260901.jmx
│   ├── 23127075_Stress_20260901.jmx
│   └── 23127075_Spike_20260901.jmx
├── README.md                     # File hướng dẫn & Bảng điểm tự đánh giá
└── run_tests.sh                  # Script tự động thực thi kiểm thử
```
