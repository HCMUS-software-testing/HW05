# HW05 Kiểm thử hiệu năng - Phân công công việc nhóm

## Mục đích

Tài liệu này chia công việc HW05 cho nhóm 4 thành viên, đồng thời tuân thủ yêu cầu của đề bài rằng không hai thành viên nào được kiểm thử cùng một workflow. HW05 là bài tập cá nhân, vì vậy mỗi thành viên vẫn phải tự tạo test plans, logs, screenshots, video, AI audit report, critique, Git commits, README và gói nộp bài của riêng mình.

## Giả định

- SUT: EShop tại <https://github.com/ttbhanh/eshop-sut>.
- Công cụ chính: JMeter. Một thành viên có thể dùng k6 chỉ khi cung cấp được các đầu ra tương đương.
- Mỗi thành viên kiểm thử một workflow end-to-end riêng biệt.
- Mỗi workflow phải bao phủ đủ ba nhóm endpoint:
- Auth-heavy: đăng nhập, đăng ký, kiểm soát truy cập, khóa tài khoản, đặt lại mật khẩu hoặc xử lý phiên đăng nhập.
- Read-heavy: danh sách sản phẩm, tìm kiếm, danh sách danh mục, chi tiết sản phẩm, dashboard hoặc các màn hình lịch sử.
- Transactional: thay đổi giỏ hàng, checkout/tạo đơn hàng, dùng mã giảm giá, CRUD admin, import hoặc thay đổi trạng thái đơn hàng.
- Nhóm có thể thảo luận tài liệu chung, nhưng không được sao chép prompts, báo cáo, raw logs, screenshots hoặc phân tích cuối cùng giữa các thành viên.

## Phân công workflow cho từng thành viên

| Thành viên | Workflow đề xuất | Bao phủ Auth-heavy | Bao phủ Read-heavy | Bao phủ Transactional | Rủi ro chính cần xử lý |
| --- | --- | --- | --- | --- | --- |
| Thành viên 1 | Người dùng có sẵn đăng nhập -> tìm kiếm sản phẩm -> xem chi tiết sản phẩm -> thêm vào giỏ hàng -> checkout | Đăng nhập người dùng có sẵn và xử lý session token/cookie | Tìm kiếm sản phẩm và chi tiết sản phẩm | Thêm vào giỏ hàng và checkout/tạo đơn hàng | Think-time phải thực tế và tránh khóa tài khoản khi chạy Stress/Spike |
| Thành viên 2 | Người dùng mới đăng ký/đăng nhập -> duyệt danh mục -> xem chi tiết sản phẩm -> checkout bằng mã giảm giá | Đăng ký tài khoản và đăng nhập lần đầu | Danh sách sản phẩm theo danh mục và chi tiết sản phẩm | Kiểm tra mã giảm giá và checkout | Cô lập dữ liệu: email/user phải duy nhất và dữ liệu sản phẩm/coupon có thể tái dùng |
| Thành viên 3 | Đăng nhập có xét negative/positive path liên quan lockout -> phân trang/lọc danh sách sản phẩm -> cập nhật số lượng giỏ hàng -> checkout | Đăng nhập và tài liệu hóa quy trình reset khóa sau 3 lần sai | Phân trang/lọc danh sách sản phẩm | Cập nhật số lượng trong giỏ hàng và checkout | Reset đúng tài khoản bị khóa giữa các lần chạy Stress/Spike |
| Thành viên 4 | Admin đăng nhập -> dashboard/danh sách sản phẩm -> CRUD sản phẩm/danh mục hoặc import CSV | Admin login và kiểm soát truy cập | Dashboard admin/danh sách sản phẩm/danh mục | CRUD sản phẩm/danh mục hoặc import CSV | Tránh thay đổi dữ liệu thật; dùng bản ghi test-only và có bước cleanup |

## Công việc chung của nhóm

Các việc này có thể phối hợp một lần, sau đó mỗi thành viên tự điều chỉnh cho workflow riêng.

| Công việc | Người phụ trách | Đầu ra |
| --- | --- | --- |
| Xác nhận cách setup SUT, ports, lệnh seed database và tài khoản mặc định | Thành viên 1 | Ghi chú setup dùng chung trong nhóm hoặc bản nháp README chung |
| Xác định endpoint API chính xác cho cả 4 workflow | Tất cả thành viên | Bảng endpoint map cho từng workflow |
| Thống nhất cấu trúc thư mục JMeter và quy ước đặt tên | Thành viên 2 | Folder template và ví dụ tên file |
| Thống nhất quy ước đặt tên screenshot và checklist bằng chứng | Thành viên 3 | Evidence checklist |
| Chuẩn bị khung báo cáo chung | Thành viên 4 | Chỉ là outline Markdown; mỗi thành viên tự viết nội dung riêng |

## Công việc cá nhân bắt buộc của mỗi thành viên

Mỗi thành viên phải hoàn thành các phần sau cho workflow được phân công.

### 1. Mô tả workflow và mapping endpoint

Sản phẩm cần nộp:

- Mô tả ngắn workflow.
- Bảng endpoint gồm method, path, nhóm endpoint, request data, expected response và assertion.
- Giải thích workflow bao phủ auth-heavy, read-heavy và transactional như thế nào.

Commit đề xuất:

```bash
git commit -m "docs: document selected performance workflow"
```

### 2. Dữ liệu đầu vào dạng data-driven

Sản phẩm cần nộp:

- CSV cho credentials.
- CSV cho product/category/search/order/coupon data nếu cần.
- Giải thích JMeter CSV Data Set Config nào dùng file CSV nào.

Commit đề xuất:

```bash
git commit -m "test: add data-driven inputs"
```

### 3. Load Test Plan

Sản phẩm cần nộp:

- JMeter test plan tên `{StudentID}_Load_{YYYYMMDD}.jmx`.
- Một loại report/listener riêng chỉ dùng cho Load.
- Raw `.jtl` log.
- Thư mục HTML report.
- Screenshot thể hiện JMeter và backend resource monitor trong cùng ngữ cảnh chạy.
- Ghi chú human review giải thích AI đã sai hoặc bỏ sót gì trong Load plan được sinh ra.

Commit đề xuất:

```bash
git commit -m "test: add load performance plan"
```

### 4. Stress Test Plan

Sản phẩm cần nộp:

- JMeter test plan tên `{StudentID}_Stress_{YYYYMMDD}.jmx`.
- Một loại report/listener riêng chỉ dùng cho Stress.
- Raw `.jtl` log.
- Thư mục HTML report.
- Screenshot thể hiện JMeter và backend resource monitor.
- Các bước reset account-lockout nếu lần chạy kích hoạt khóa tài khoản.
- Ghi chú human review giải thích AI đã sai hoặc bỏ sót gì trong Stress plan được sinh ra.

Commit đề xuất:

```bash
git commit -m "test: add stress performance plan"
```

### 5. Spike Test Plan

Sản phẩm cần nộp:

- JMeter test plan tên `{StudentID}_Spike_{YYYYMMDD}.jmx`.
- Một loại report/listener riêng chỉ dùng cho Spike.
- Raw `.jtl` log.
- Thư mục HTML report.
- Screenshot thể hiện JMeter và backend resource monitor.
- Các bước reset account-lockout nếu lần chạy kích hoạt khóa tài khoản.
- Ghi chú human review giải thích AI đã sai hoặc bỏ sót gì trong Spike plan được sinh ra.

Commit đề xuất:

```bash
git commit -m "test: add spike performance plan"
```

### 6. Endurance / Soak Test

Sản phẩm cần nộp:

- Một lần chạy sustained-load trong 10-15 phút.
- Các số liệu ngưỡng endurance cụ thể, ví dụ maximum stable RPS, p95 latency, error rate, CPU usage và memory ceiling.
- Screenshot hoặc log evidence chứng minh ngưỡng đã báo cáo.

Commit đề xuất:

```bash
git commit -m "docs: record endurance threshold"
```

### 7. AI Analysis và Misinterpretation Hunt

Sản phẩm cần nộp:

- Prompt yêu cầu AI phân tích raw `.jtl` logs và đề xuất thresholds.
- AI output được lưu trong AI Audit Report.
- Human review chỉ ra các metric AI đọc sai hoặc diễn giải sai.
- Giá trị đúng được trích dẫn từ raw `.jtl` logs.
- Phân loại các đề xuất tối ưu của AI là feasible hoặc hallucinated.

Commit đề xuất:

```bash
git commit -m "docs: add AI analysis review"
```

### 8. Đề xuất Continuous Performance Testing

Sản phẩm cần nộp:

- Một mô hình kiểm thử hiệu năng liên tục.
- Flow chart thể hiện commit detection, test selection, execution, baseline comparison và p95 regression flagging.
- Thảo luận trade-off gồm chi phí, thời gian chạy, cảnh báo sai, nhiễu môi trường và chi phí bảo trì.

Commit đề xuất:

```bash
git commit -m "docs: add continuous performance testing proposal"
```

### 9. Agent Skill

Sản phẩm cần nộp:

- Một Agent Skill hoặc rule tái sử dụng được cho workflow kiểm thử hiệu năng và phân tích log.
- Link YouTube demo cho thấy skill được dùng end-to-end trên một nhóm endpoint hoàn chỉnh.

Commit đề xuất:

```bash
git commit -m "skill: add reusable performance testing workflow"
```

### 10. Đóng gói cuối cùng

Sản phẩm cần nộp:

- Báo cáo chính ở Markdown và PDF.
- AI Critique ở Markdown và PDF.
- AI Audit Report ở Markdown và PDF.
- Ba `.jmx` test plans.
- Ba raw `.jtl` logs.
- Ba thư mục HTML report.
- Resource-monitor screenshots và hardware-spec screenshots.
- Link video demo YouTube không công khai.
- Git commit log text file.
- Bug reports kèm screenshots trên GitHub Issues, nếu có.
- `README.md` có bảng self-assessment và test summary.
- File zip cuối cùng tên `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`.

Commit đề xuất:

```bash
git commit -m "docs: finalize HW05 submission package"
```

## Timeline đề xuất

| Giai đoạn | Time box | Hoạt động nhóm | Đầu ra cá nhân |
| --- | --- | --- | --- |
| Giai đoạn 1 | 1 giờ | Xác nhận setup SUT và endpoint map | Workflow đã chọn và bảng endpoint |
| Giai đoạn 2 | 1 giờ | Thống nhất naming, folders và cách dùng CSV | Các file CSV data-driven |
| Giai đoạn 3 | 3 giờ | Chạy Load, Stress và Spike plans | `.jmx`, `.jtl`, HTML reports, screenshots |
| Giai đoạn 4 | 1 giờ | So sánh các lỗi diễn giải metric phổ biến | Endurance threshold và AI analysis review |
| Giai đoạn 5 | 1 giờ | Thảo luận mô hình CI/performance-regression | Continuous testing proposal |
| Giai đoạn 6 | 2 giờ | Peer-check evidence checklist | Final report, audit, critique, video, README, zip |

## Evidence Checklist cho mỗi thành viên

| Bằng chứng | Bắt buộc |
| --- | --- |
| 3 workflow khác nhau trong nhóm? | Có; cả 4 workflow nên khác nhau |
| Load test plan | Có |
| Stress test plan | Có |
| Spike test plan | Có |
| CSV data-driven input | Có |
| 3 loại report/listener khác nhau | Có |
| 3 raw `.jtl` logs | Có |
| 3 thư mục HTML report | Có |
| Resource monitor screenshots | Có |
| Hardware report screenshot và spec table | Có |
| Endurance threshold có số liệu | Có |
| AI analysis prompt và output | Có |
| Human correction cho các lỗi AI diễn giải sai | Có |
| Continuous performance-testing flow chart | Có |
| AI Critique, 200-300 từ | Có |
| AI Audit Report appendix | Có |
| Git commit log text file | Có |
| Video YouTube không công khai, ít nhất 6 phút | Có |
| README có self-assessment và summary | Có |

## Quy tắc peer review

- Các thành viên có thể review checklist, screenshots và cấu trúc báo cáo của nhau.
- Các thành viên không được sao chép prompts, AI outputs, đoạn văn báo cáo, `.jtl` logs hoặc screenshots.
- Mỗi thành viên phải trích dẫn giá trị từ raw `.jtl` files của chính mình.
- Mỗi thành viên phải tự thu âm thuyết minh tiếng Việt trong video demo.
- Nếu hai workflow trở nên quá giống nhau, phải đổi một workflow trước khi chạy test chính thức.

## Cấu trúc thư mục đề xuất cho mỗi thành viên

```text
submissions/
  <StudentID>/
    README.md
    report/
      main-report.md
      main-report.pdf
      ai-critique.md
      ai-critique.pdf
      ai-audit-report.md
      ai-audit-report.pdf
    test-plans/
      <StudentID>_Load_<YYYYMMDD>.jmx
      <StudentID>_Stress_<YYYYMMDD>.jmx
      <StudentID>_Spike_<YYYYMMDD>.jmx
    data/
      credentials.csv
      products.csv
      orders.csv
    results/
      load/
        raw.jtl
        html-report/
      stress/
        raw.jtl
        html-report/
      spike/
        raw.jtl
        html-report/
    evidence/
      screenshots/
      hardware/
    git-commit-log.txt
```
