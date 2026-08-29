# Kế hoạch HW05 cho Thành viên 3

## 1. Mục tiêu và chiến lược

Thực hiện độc lập workflow:

`Lockout probe → đăng nhập hợp lệ → lọc/tìm sản phẩm → thêm và cập nhật số lượng giỏ hàng → checkout`

Workflow bao phủ:

- Auth-heavy: `POST /api/login`, gồm cả positive path và kiểm tra khóa tài khoản sau ba lần sai.
- Read-heavy: `GET /api/products?search=...&page=...&limit=...`.
- Transactional: `POST /api/cart`, `GET /api/cart`, `POST /api/checkout`.

Không sửa SUT để làm test “chạy đẹp”. Các khác biệt giữa đặc tả và implementation phải được giữ lại làm assertion, bằng chứng và GitHub Issue:

- SUT chỉ hỗ trợ `search`, chưa thực hiện phân trang.
- Không có `PUT/PATCH` cập nhật giỏ hàng; gọi `POST /api/cart` lần hai đang thêm dòng mới.
- Login thực tế tăng `login_attempts` thêm 2 và khóa 180 giây, khác yêu cầu tăng 1 và khóa 30 giây.
- Checkout không xóa giỏ hàng.

Các endpoint và payload lấy từ [API specification của EShop](https://github.com/ttbhanh/eshop-sut/blob/main/api_specification.md); hành vi thực tế phải được đối chiếu thêm với [backend/server.js](https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js).

## 2. Chuẩn bị và giao diện dữ liệu

### Cấu trúc sản phẩm bàn giao

Dùng `submissions/<StudentID>/` với:

- `test-plans/`: ba file `.jmx`.
- `data/`: credentials, sản phẩm và địa chỉ checkout.
- `results/{load,stress,spike,endurance}/`: raw `.jtl` và HTML report.
- `evidence/{screenshots,hardware,issues}/`.
- `report/`: báo cáo chính, AI critique và AI audit ở Markdown/PDF.
- `README.md`, `git-commit-log.txt`.

Tên plan dùng ngày chạy thật:

- `<StudentID>_Load_<YYYYMMDD>.jmx`
- `<StudentID>_Stress_<YYYYMMDD>.jmx`
- `<StudentID>_Spike_<YYYYMMDD>.jmx`

### Môi trường và fixtures

- Cài JMeter vì máy hiện chưa có lệnh `jmeter`; xác nhận bằng `jmeter --version`.
- SUT chạy riêng tại `http://localhost:3000`; máy đo là MacBook Pro M1 Pro, 10 cores, RAM 32 GB.
- Tạo tối thiểu 100 tài khoản `perf.m3.*` chỉ dùng cho thành viên 3. Việc tạo fixture không đưa vào thời gian đo và không được xem là workflow đăng ký của thành viên 2.
- Mỗi virtual user dùng một tài khoản riêng. CSV Data Set Config đặt `Recycle on EOF=false`, `Stop thread on EOF=true`, sharing mode toàn test plan.
- Dùng một tài khoản riêng `perf.m3.lockout.*` cho negative path.

Các CSV:

- `credentials.csv`: `email,password`
- `lockout-account.csv`: `email,password,wrong_password`
- `products.csv`: `search,page,limit,product_id,product_name,price,quantity_initial,quantity_updated`
- `orders.csv`: `shipping_address`

Các thuộc tính JMeter có thể override từ CLI: `baseUrl`, `threads`, `rampSeconds`, `durationSeconds`, `thinkMinMs`, `thinkMaxMs`.

## 3. Thiết kế và thực thi

### Luồng sampler dùng chung

1. `POST /api/login` với credentials hợp lệ.
2. Assert HTTP 200 và JSON có `token`; dùng JSON Extractor lưu `${token}`.
3. Gắn `Authorization: Bearer ${token}` cho các request được bảo vệ.
4. `GET /api/products?search=${search}&page=${page}&limit=${limit}`.
5. Assert HTTP 200, JSON array không rỗng và sản phẩm khớp từ khóa.
6. Extract `id`, `name`, `price` từ kết quả thay vì tin hoàn toàn vào giá trị hard-code.
7. `POST /api/cart` với `quantity_initial`.
8. Gọi lại `POST /api/cart` cùng sản phẩm với `quantity_updated`, sau đó `GET /api/cart`.
9. Kiểm tra kỳ vọng nghiệp vụ: một dòng sản phẩm duy nhất với số lượng mới. Nếu SUT tạo hai dòng, lưu response làm bug evidence nhưng vẫn cho workflow tiếp tục.
10. `POST /api/checkout` với `shipping_address`; assert HTTP 200 và có `orderId`.
11. `GET /api/cart` sau checkout; kỳ vọng giỏ rỗng. Ghi riêng lỗi nghiệp vụ để không nhầm với lỗi transport.
12. Chèn Uniform Random Timer 1–3 giây giữa các hành động người dùng.

Tách label rõ ràng thành `AUTH`, `READ`, `CART_UPDATE`, `CHECKOUT`, `POST_CHECKOUT_CART` để phân tích p95 và error rate theo endpoint. Các assertion kiểm tra đặc tả bị lỗi phải được báo cáo riêng với HTTP/network errors.

### Lockout probe và reset

Trước mỗi lần chạy chính thức:

1. Dùng một thread, gửi ba login sai liên tiếp.
2. Ghi status code, response body, `login_attempts` và thời gian khóa.
3. Thử positive login khi đang khóa.
4. Đối chiếu kỳ vọng: mỗi lần sai tăng 1, khóa sau lần thứ ba trong 30 giây.
5. Chụp bằng chứng nếu implementation khóa từ lần thứ hai hoặc giữ khóa 180 giây.
6. Reset đúng tài khoản test bằng cập nhật có điều kiện:
   `UPDATE users SET login_attempts=0, locked_until=NULL WHERE email='<lockout-test-email>';`
7. Chạy `SELECT` xác nhận đã reset trước khi bắt đầu đo.
8. Không chạy lại toàn bộ `database.js` giữa các scenario vì sẽ xóa dữ liệu không liên quan.

Negative probe nằm trong JMX nhưng tắt ở official performance run; kết quả của probe được lưu riêng để không làm sai error rate và latency của positive workflow.

### Hồ sơ tải mặc định

| Scenario  | Cấu hình                                                                       | Report view riêng                               |
| --------- | ------------------------------------------------------------------------------ | ----------------------------------------------- |
| Smoke     | 1 VU, 1 iteration                                                              | Dùng để xác nhận correlation/assertion          |
| Load      | 20 VU, ramp-up 60 giây, giữ tải 5 phút                                         | View Results Tree chỉ cho smoke/đọc JTL sau run |
| Stress    | 100 VU, ramp-up tuyến tính 300 giây, giữ tải thêm 3 phút                       | Summary Report                                  |
| Spike     | 10 VU nền trong 7 phút; thêm 90 VU sau 120 giây, ramp 5 giây, giữ spike 2 phút | Aggregate Report                                |
| Endurance | 70% mức concurrency cao nhất còn ổn định, chạy 10–15 phút                      | Tái dùng Load plan bằng CLI properties          |

Ba listener phải tồn tại đúng plan nhưng bị disable trong official non-GUI run để không làm méo kết quả. Sau run, mở raw JTL bằng report view tương ứng để chụp bằng chứng. Mỗi official run dùng:

```bash
jmeter -n -t <plan>.jmx -l <raw.jtl> -e -o <html-report>
```

Trước mỗi run phải:

- Restart backend để xóa in-memory cart.
- Reset lockout account và kiểm tra fixtures.
- Xóa hoặc chọn thư mục HTML output mới, không ghi đè bằng chứng cũ.
- Đặt terminal JMeter và Activity Monitor cạnh nhau; theo dõi đúng tiến trình Node backend.
- Ghi CPU, memory, throughput, p95, error rate và thời điểm tải đạt đỉnh.

Ngưỡng ổn định mặc định: error transport/HTTP dưới 1%, p95 dưới 1.000 ms, CPU backend dưới 85%, memory không tăng liên tục, throughput không suy giảm qua ba cửa sổ đo liên tiếp. Endurance chạy tại 70% mức VU cuối cùng thỏa toàn bộ điều kiện; báo cáo maximum stable RPS, p95, error rate, CPU và memory ceiling bằng số thật.

## 4. Phân tích, báo cáo và CI proposal

### AI-first và human review

- Lưu từng prompt, output, công cụ, ngày giờ vào `ai-audit-report.md`, gồm cả phiên lập kế hoạch này nếu được sử dụng cho bài nộp.
- Prompt AI theo từng bước: endpoint mapping, thiết kế workload, tạo JMX, review correlation/assertion, phân tích từng JTL, đề xuất threshold và tối ưu.
- Không dùng chung prompt, output hoặc prose với thành viên khác.
- Human review phải chỉ rõ các lỗi AI như bỏ qua lockout, dùng một account cho mọi thread, chạy listener GUI khi đo tải, tin `total_amount` client gửi lên hoặc nhầm assertion failure với server error.
- Tự tính lại từ raw JTL: sample count, throughput, error %, mean, median, p90, p95, p99 và max theo label; trích giá trị/dòng dữ liệu thật khi bác bỏ phân tích AI.
- Phân loại từng tối ưu AI là khả thi, cần thêm bằng chứng hoặc hallucinated. Không khẳng định database index/connection pool/WAL là nguyên nhân nếu chưa có profiling.

Các GitHub Issue chỉ tạo khi tái hiện được, gồm expected/actual, bước tái hiện, môi trường, response hoặc screenshot. Ưu tiên bốn ứng viên: lockout sai, pagination bị bỏ qua, cập nhật quantity tạo dòng trùng và checkout không xóa cart.

### Continuous Performance Testing

Đề xuất GitHub Actions với self-hosted runner cố định:

`Commit → kiểm tra file backend thay đổi → khởi động SUT sạch → smoke → PR load test → so baseline → chạy lại tối đa 3 lần khi nghi regression → đánh dấu p95/error regression → lưu JTL/HTML`

- PR: smoke và Load ngắn.
- Nightly: Load đầy đủ, Stress và Spike.
- Hàng tuần: Endurance.
- Flag regression khi p95 tăng trên 20% và tối thiểu 100 ms so với baseline, hoặc error rate tăng quá 1 điểm phần trăm; chỉ chặn sau khi tái hiện ít nhất 2/3 lần.
- Báo cáo trade-off: thời gian runner, nhiễu máy local, database state, false positive, chi phí lưu artifacts và bảo trì baseline.

### Video và đóng gói

- Video YouTube không công khai tối thiểu 6 phút, có giọng thuyết minh tiếng Việt.
- Hiển thị JMeter/terminal và Activity Monitor trong cùng khung hình.
- Trình bày ít nhất Load, Stress, Spike, lockout/reset, raw JTL/HTML report và một lần dùng Agent Skill.
- AI Critique dài 200–300 từ.
- README có self-assessment, workflow, endpoint coverage, endurance threshold, số issue và link video.
- Xuất Markdown sang PDF, kiểm tra PDF và toàn bộ link trước khi zip.
- File cuối: `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`.

## 5. Kiểm thử chấp nhận và tiến độ

### Acceptance checklist

- Ba JMX đúng tên, cùng workflow và ba report view không trùng.
- CSV được dùng thật; không hard-code JWT, product hoặc địa chỉ trong sampler.
- Positive login, token extraction và toàn bộ protected requests hoạt động.
- Negative lockout được tái hiện, reset và tài liệu hóa.
- Có ba raw JTL, ba HTML report và endurance evidence riêng.
- Screenshot chứa công cụ chạy và resource monitor; hardware evidence khớp hostname.
- Phân biệt HTTP errors, assertion failures và khác biệt đặc tả.
- Mọi số liệu trong báo cáo truy ngược được về raw JTL.
- Có flowchart CI, AI Audit, AI Critique, video, issue evidence và git log.
- Chạy `git diff --check` và kiểm tra zip trước khi nộp.

### Time box 10 giờ

1. Setup, fixtures, endpoint probe: 1 giờ.
2. CSV và JMeter skeleton: 1 giờ.
3. Load/Stress/Spike, debug và evidence: 3 giờ.
4. Endurance và resource analysis: 1,5 giờ.
5. AI analysis, human corrections và issues: 1 giờ.
6. CI proposal, Agent Skill và critique: 1 giờ.
7. Video, PDF, README, audit và đóng gói: 1,5 giờ.

Commit riêng cho workflow mapping, data, từng scenario, endurance, AI review, CI proposal, Agent Skill và final package; cuối cùng xuất `git log` ra `git-commit-log.txt`.

## Giả định đã khóa

- Dùng JMeter, không chuyển sang k6.
- Giữ `<StudentID>` và `<YYYYMMDD>` cho đến khi biết MSSV và ngày chạy thật.
- Giữ nguyên workflow thành viên 3 dù SUT thiếu pagination và API update quantity; các khoảng cách này trở thành assertion/bug evidence.
- Chỉ dùng dữ liệu và tài khoản test riêng; không dùng raw logs, prompts hoặc screenshots của thành viên khác.
- Không bịa số liệu hoặc issue: mọi metric, screenshot, video và bug report phải sinh từ lần chạy thật.
