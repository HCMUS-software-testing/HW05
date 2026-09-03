# HW05 - Performance Testing with AI

- **Sinh viên**: Lê Trung Kiên
- **MSSV**: 23127075
- **Workflow**: Member 4 - Admin Workflow
- **Repository**: <https://github.com/HCMUS-software-testing/HW05>

## 1. Tự đánh giá

| STT | Tiêu chí | Tối đa | Tự đánh giá | Bằng chứng chính |
| --- | --- | ---: | ---: | --- |
| 1 | Task 1 - Load testing | 30 | 28 | 300 samples, 0 lỗi, JTL + HTML + screenshot |
| 2 | Task 1 - Stress testing | 20 | 18 | 3.000 samples, 0 lỗi, JTL + HTML + screenshot |
| 3 | Task 1 - Spike testing | 20 | 18 | 1.800 samples, 0 lỗi, JTL + HTML + screenshot |
| 4 | Task 2 - AI analysis + misinterpretation | 10 | 10 | Giá trị đúng từ raw JTL và phản biện recommendation |
| 5 | Task 3 - Continuous testing | 10 | 10 | Pipeline Mermaid, p95 gate và trade-offs |
| 6 | Agent Skills | 10 | 10 | Skill, analyzer, endurance runner và regression tests |
| **Tổng nội dung kỹ thuật** | | **100** | **94 / 100** | Chưa phải trạng thái sẵn sàng nộp |

Các mục còn cần hoàn tất thủ công: export PDF của báo cáo chính và AI Audit, cập nhật git commit log sau các thay đổi cuối, và kiểm tra video ở chế độ unlisted, thời lượng tối thiểu 6 phút cùng nội dung hiển thị theo đề.

## 2. Phạm vi và kết quả

Workflow sáu request bao phủ:

- **Auth-heavy**: `POST /api/login`, `GET /api/admin/users` với JWT.
- **Read-heavy**: `GET /api/products`, `GET /api/categories`.
- **Transactional**: tạo sản phẩm từ CSV rồi xóa đúng ID vừa tạo.

| Scenario | Threads / Ramp / Loops | Samples | Avg throughput | Avg / p95 response time | Errors |
| --- | --- | ---: | ---: | ---: | ---: |
| Load | 10 / 10 s / 5 | 300 | 4,4834 RPS | 9,76 / 17 ms | 0 |
| Stress | 50 / 15 s / 10 | 3.000 | 40,1924 RPS | 7,62 / 15 ms | 0 |
| Spike | 100 / 1 s / 3 | 1.800 | 352,7337 RPS | 238,47 / 476 ms | 0 |
| Endurance | 30 / 30 s / duration 600 s | 17.238 | 28,8012 RPS | 15,46 / 16 ms | 0 |

Điểm tải endurance đã chứng minh: **30 VU đạt trung bình 28,80 RPS trong 10 phút**, backend RSS **103,676-111,680 MiB**, không có xu hướng tăng bộ nhớ trong 121 mẫu giám sát. Đây không phải tải tối đa vì chưa chạy nhiều bậc tải. Xem [`report/main-report.md`](report/main-report.md) để biết p99, outlier, cleanup và phương pháp tính.

Các bug và vấn đề đã được ghi nhận tại GitHub Issues: #22 và #23 là lỗi bảo mật, #24 là vấn đề hiệu năng. Báo cáo chi tiết nằm tại [`report/bug-report.md`](report/bug-report.md).

## 3. Chạy lại

Khởi động SUT từ root repository:

```bash
cd eshop-sut/backend
npm start
```

Chạy sạch ba scenario chính:

```bash
cd src
./run_tests.sh
python3 tools/analyze_jtl.py \
  results/load/raw.jtl results/stress/raw.jtl results/spike/raw.jtl
```

Chạy Endurance với PID backend thực:

```bash
BACKEND_PID="$(pgrep -fo 'node .*server\.js')" ./run_endurance.sh
```

Nếu login bị khóa do credentials sai, chạy từ root repository:

```bash
sqlite3 eshop-sut/backend/database.sqlite \
  "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = 'admin@eshop.com';"
```

Kiểm tra bài nộp:

```bash
cd src
./tools/validate_submission.sh
```

## 4. Cấu trúc artifact

```text
src/
├── ai-audit/                 # AI Audit Markdown; PDF còn thiếu
├── data/                     # CSV credentials và products
├── evidence/                 # fastfetch và htop cho ba scenario
├── report/                   # main report, AI critique, bug report
├── results/                  # Load, Stress, Spike, Endurance JTL/HTML/resource log
├── test-plans/               # Ba plan bắt buộc và plan Endurance hỗ trợ
├── tools/                    # analyzer, monitor, validator và regression tests
├── run_tests.sh
└── run_endurance.sh
```

Skill nguồn nằm ngoài `src/` tại `.agents/skills/performance-testing-skills/`. Validator chỉ copy skill vào `agent-skill/` của bản staging; không tạo wrapper và không sửa tên thư mục `src/` đang làm việc.

## 5. Trạng thái trước khi nộp

Lần kiểm tra gần nhất bằng `tools/validate_submission.sh` còn các lỗi sau:

- `Endurance resource log integrity`: resource log chưa bao phủ toàn bộ cửa sổ JTL.
- `Endurance transactional cleanup`: còn chênh lệch 4 sản phẩm create/delete trong bằng chứng cleanup.
- Thiếu PDF của `report/main-report.md` và `ai-audit/ai_audit_report.md`.
- GitHub Issues đã tạo: [#22 BUG-SEC-23127075](https://github.com/HCMUS-software-testing/HW05/issues/22), [#23 BUG-SEC-23127075](https://github.com/HCMUS-software-testing/HW05/issues/23), [#24 BUG-PERF-23127075](https://github.com/HCMUS-software-testing/HW05/issues/24).
- Screenshot Issue: `evidence/screenshots/github_issue_bug.png`.

## 6. Video

- **Flow demo**: <https://youtu.be/iJPhKGJS6jM>
- **Agent demo**: <https://youtu.be/JUV8j6AjZdQ>

Hai video cần được đặt ở chế độ YouTube unlisted, dài tối thiểu 6 phút cho video bài nộp, có thuyết minh tiếng Việt và hiển thị JMeter cùng resource monitor trong một khung hình.
