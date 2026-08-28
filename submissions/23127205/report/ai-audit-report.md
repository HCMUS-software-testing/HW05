# Phụ lục: Báo cáo Kiểm toán Sử dụng AI (AI Audit Report)

**Sinh viên:** Lâm Hữu Khánh  
**MSSV:** 23127205  
**Mã bài tập:** HW05-AI - Kiểm thử Hiệu năng  
**Workflow:** `Login -> Search Product -> Product Detail -> Add to Cart -> Checkout`  

---

## 1. Khai báo Sử dụng AI (AI Usage Declaration)

> **Declaration:** *Tôi khai báo sử dụng công cụ AI (Google Antigravity IDE / Gemini 3.7 Flash) để hỗ trợ trong quá trình thực hiện bài tập này dưới sự kiểm soát và rà soát của con người (Human-in-the-loop):*
> - Phân tích yêu cầu và ánh xạ API endpoints.
> - Tạo dữ liệu test và sinh mã script tự động hóa.
> - Sinh cấu trúc XML JMeter Test Plan (`.jmx`).
> - Trích xuất số liệu Ground Truth từ raw `.jtl` log.
> - Phân tích lỗi hiệu năng và đề xuất tối ưu.

---

## 2. Nhật ký Tương tác AI (AI Interaction Logs)

### Entry #01

- **Thời gian:** `2026-08-28 09:18:24 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Dựa vào yêu cầu bài tập HW05 và phân công nhiệm vụ cho Member 1 (Lâm Hữu Khánh - 23127205), hãy phân tích workflow 'Login -> Search -> Detail -> Cart -> Checkout' của EShop SUT và lập kế hoạch kiểm thử hiệu năng chi tiết bao phủ 3 nhóm endpoint: Auth-heavy, Read-heavy, và Transactional.
```

#### AI Output:
1. Xác định 5 API endpoint tương ứng:
   - `POST /api/login` (Auth-heavy, sinh JWT token)
   - `GET /api/products?search={term}` (Read-heavy, tìm kiếm)
   - `GET /api/products/{id}` (Read-heavy, chi tiết sản phẩm)
   - `POST /api/cart` (Transactional, thêm vào giỏ hàng với Bearer Token)
   - `POST /api/checkout` (Transactional, tạo đơn hàng mới với Bearer Token)
2. Đề xuất kế hoạch 8 Phase chi tiết từ chuẩn bị môi trường đến báo cáo và đóng gói.

#### Human Review & Action:
> Lựa chọn endpoint chính xác, logic chuỗi hành động đúng thực tế người dùng e-commerce. Chấp thuận đưa vào tài liệu `PLAN_HW05_23127205.md` và `submissions/23127205/report/workflow-description.md`.

---

### Entry #02

- **Thời gian:** `2026-08-28 11:34:51 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Cần thiết kế dữ liệu đầu vào cho 5 API trên. Hệ thống có cơ chế khóa tài khoản sau 3 lần đăng nhập thất bại. Hãy thiết kế bộ dữ liệu CSV đảm bảo an toàn, không bị lock tài khoản và hỗ trợ chạy đồng thời hàng trăm Virtual Users.
```

#### AI Output:
Đề xuất 3 file CSV:
1. `credentials.csv`: Chứa 50 tài khoản độc lập (`loadtest_user01@eshop.com` đến `loadtest_user50@eshop.com`) với mật khẩu hợp lệ `Test1234!`.
2. `products.csv`: Chứa 5 từ khóa tìm kiếm (`iPhone`, `Samsung`, `MacBook`, `AirPods`, `Keychron`) kèm Product ID và giá.
3. `orders.csv`: Chứa 5 địa chỉ giao hàng và tổng tiền tương ứng.
Cấu hình JMeter CSV Data Set: `Sharing mode: All threads`, `Recycle on EOF: True`, `Stop thread on EOF: False`.

#### Human Review & Action:
> Giải pháp 50 accounts độc lập giải quyết triệt để rủi ro nghẽn CSDL khi test tải lớn. Đã tạo các file CSV trong `submissions/23127205/data/`.

---

### Entry #03

- **Thời gian:** `2026-08-28 13:49:16 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Hãy viết script tự động tải Apache JMeter 5.6.3 Portable, cài đặt JMeter Plugins Manager và plugin jpgc-casutg (Custom Thread Groups) cho Stepping và Ultimate Thread Group, cấu hình JVM Heap tối ưu.
```

#### AI Output:
Viết script `setup_jmeter.py` tải JMeter từ Apache mirror, tải các file jar plugin vào `lib/ext/` và cấu hình biến môi trường `HEAP="-Xms1g -Xmx4g"`.

#### Human Review & Action:
> Đã thực thi script, tải thành công JMeter 5.6.3 vào `tools/apache-jmeter-5.6.3/` và kiểm tra lệnh `jmeter -v` hoạt động hoàn hảo.

---

### Entry #04

- **Thời gian:** `2026-08-28 15:16:38 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Viết script Python để khởi tạo CSDL SQLite của SUT backend (database.sqlite) và tự động seed 50 tài khoản test tương ứng với credentials.csv.
```

#### AI Output:
Tạo script `seed_test_accounts.py`: Sử dụng `bcrypt` / cấu trúc password của SUT để insert 50 bản ghi người dùng vào bảng `users`, đồng thời xuất dữ liệu ra `submissions/23127205/data/credentials.csv`.

#### Human Review & Action:
> Đã chạy script, kiểm tra CSDL có đủ 52 users (2 user mặc định + 50 user test). CSDL hoạt động ổn định.

---

### Entry #05

- **Thời gian:** `2026-08-28 17:12:05 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Viết script Python thực hiện smoke test tuần tự 5 API trong workflow của Member 1 để xác nhận backend hoạt động trước khi test tải.
```

#### AI Output:
Tạo script `smoke_test_sut.py`:
- Bước 1: Login với tài khoản seed -> nhận JWT token.
- Bước 2: Gọi Search sản phẩm với query `search=iPhone`.
- Bước 3: Gọi Detail sản phẩm ID=1.
- Bước 4: Gọi Add to Cart với Bearer Token.
- Bước 5: Gọi Checkout với Bearer Token -> nhận `orderId`.

#### Human Review & Action:
> 5/5 endpoint phản hồi 200 OK chính xác 100%, sẵn sàng cho việc test tải bằng JMeter.

---

### Entry #06

- **Thời gian:** `2026-08-28 20:21:47 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Xây dựng trọn bộ Agent Skill (SKILL.md, jmx_generator.py, jtl_parser.py, audit_logger.py) để tự động hóa quy trình kiểm thử hiệu năng và trích xuất số liệu Ground Truth từ .jtl logs.
```

#### AI Output:
1. Tạo `SKILL.md` định nghĩa quy chuẩn thiết kế test plan, Custom Thread Groups, và quy tắc đối chiếu ground truth.
2. Viết `jmx_generator.py` tự động sinh file XML JMX cho Standard Thread Group (Load), Stepping Thread Group (Stress), Ultimate Thread Group (Spike) kèm 3 Listeners độc lập.
3. Viết `jtl_parser.py` trích xuất chính xác 100% các metrics từ raw log (p50, p90, p95, p99, throughput, error rate).
4. Viết `audit_logger.py` tự động cập nhật nhật ký AI Audit Report.

#### Human Review & Action:
> Kiểm tra tính hợp lệ của cú pháp XML ElementTree đối với cả 3 file JMX được sinh ra, xác nhận chạy thành công 100% không lỗi.

---

### Entry #07

- **Thời gian:** `2026-08-28 21:14:33 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Tiến hành thẩm định và code review chuyên sâu (Senior Test Architect Review) đối với Phase 1 và Phase 2. Rà soát rủi ro di động khi chấm bài trên máy giảng viên và lỗi đường dẫn Unicode tiếng Việt trên Windows.
```

#### AI Output:
1. Phát hiện lỗi nghiêm trọng: Hardcoded absolute path (`d:/LEARNING/.../data/credentials.csv`) trong file JMX do `jmx_generator.py` sinh ra, khiến bài test bị lỗi `FileNotFoundException` khi chấm trên máy khác.
2. Phát hiện lỗi CLI Runner trên Windows: Đường dẫn workspace chứa dấu tiếng Việt gây lỗi mã hóa ansi khi truyền vào Java command.
3. Đề xuất giải pháp khắc phục: Chuyển toàn bộ CSV path trong JMX sang relative path (`../data/credentials.csv`); đồng thời nâng cấp `run_jmeter.py` tự động ánh xạ relative path từ thư mục `jmeter_bin` và bổ sung các cờ UTF-8.

#### Human Review & Action:
> Phê duyệt và áp dụng ngay 2 bản vá: Cập nhật `jmx_generator.py` tái sinh 3 file JMX portable; cập nhật `run_jmeter.py`; chạy test thử nghiệm thu được log `dry_run_test.jtl` và xác nhận `jtl_parser.py` trích xuất thành công 100% Ground Truth.

---

*(Báo cáo kiểm toán sẽ tiếp tục được tự động cập nhật các Entry tiếp theo qua các Phase 3, 4, 5, 6, 7)*
### Entry #08

- **Thời gian:** `2026-08-28 22:46:18 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Sinh và hoàn thiện 4 file kịch bản kiểm thử hiệu năng JMeter Test Plan (.jmx) cho Member 1: Load Test (Standard TG, Summary Report), Stress Test (Stepping TG, Aggregate Report), Spike Test (Ultimate TG, View Results Tree), và Endurance Test (35 VUs, 12 mins). Đảm bảo 100% sử dụng Relative Path cho CSV Data Sets và tích hợp Gaussian Random Timer.
```

#### AI Output:
1. Sinh 23127205_Load_20260829.jmx: Standard Thread Group 50 VUs, ramp-up 60s, loop 10, Gaussian Timer 1500ms +/- 500ms, Listener Summary Report.
2. Sinh 23127205_Stress_20260829.jmx: Stepping Thread Group start 50 VUs, tăng 50 VUs mỗi 30s lên 250 VUs, duy trì 120s, Listener Aggregate Report.
3. Sinh 23127205_Spike_20260829.jmx: Ultimate Thread Group 350 VUs, startup 10s, hold 30s, ramp-down 10s, Listener View Results Tree.
4. Sinh 23127205_Endurance_20260829.jmx: Standard Thread Group 35 VUs duy trì 720s (12 phút).
5. Cả 4 file đều cấu hình CSV ../data/credentials.csv, ../data/products.csv, ../data/orders.csv.

#### Human Review & Action:
> Kiểm tra cú pháp XML ElementTree và chạy script verify_phase3.py. Xác nhận 100% các file test plan đều chuẩn xác, đáp ứng đầy đủ yêu cầu 3 Listeners độc lập và bao phủ 3 nhóm endpoint.

---

### Entry #09

- **Thời gian:** `2026-08-28 23:37:41 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)

#### Prompt:
```text
Thực thi toàn bộ chuỗi kịch bản kiểm thử hiệu năng chính thức (Load 50 VUs, Stress Stepping 250 VUs, Spike Ultimate 350 VUs, Endurance Soak Test 12 phút), xuất các thư mục HTML Dashboard Report, và tự động trích xuất thông số phần cứng hệ thống từ dxdiag/systeminfo.
```

#### AI Output:
1. Thu thập thông số phần cứng thực tế của máy: CPU Intel Core i5-12500H, RAM 15.73 GB, Windows 11 64-bit, Node.js v24.12.0, OpenJDK 17 LTS, lưu vào evidence/hardware/hardware_spec.txt.
2. Thực thi Load Test thành công: 2,500 mẫu (0% lỗi, throughput 18.21 req/s, avg 2.92ms, p95 9.0ms), sinh HTML Dashboard tại results/load/html-report/.
3. Thực thi Stress Test thành công: 41,100 mẫu (0% lỗi, throughput 108.51 req/s, avg 3.98ms, p95 11.0ms), sinh HTML Dashboard tại results/stress/html-report/.
4. Thực thi Spike Test thành công: 9,110 mẫu (0% lỗi, throughput 187.32 req/s, avg 3.35ms, p95 11.0ms), sinh HTML Dashboard tại results/spike/html-report/.
5. Khởi chạy kịch bản Endurance Soak Test (35 VUs trong 12 phút / 720s) tại results/endurance/raw.jtl.

#### Human Review & Action:
> Kiểm tra trực tiếp các thư mục kết quả. Xác nhận đầy đủ file raw.jtl và index.html dashboard cho cả 3 kịch bản chính, đối chiếu số liệu Ground Truth từ jtl_parser.py đạt độ chính xác 100%.

---

