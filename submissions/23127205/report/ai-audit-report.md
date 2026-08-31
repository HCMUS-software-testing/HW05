# Phụ lục: Báo cáo Kiểm toán Sử dụng AI (AI Audit Report)

**Sinh viên:** Lâm Hữu Khánh  
**MSSV:** 23127205  
**Mã bài tập:** HW05-AI - Kiểm thử Hiệu năng  
**Workflow:** `Login -> Search Product -> Product Detail -> Add to Cart -> Checkout`  
**SUT:** EShop RESTful API Backend (`http://localhost:3000`), Frontend Web (`http://localhost:5173`), Frontend Admin (`http://localhost:5174`)  
**Repository:** [`https://github.com/HCMUS-software-testing/HW05`](https://github.com/HCMUS-software-testing/HW05)  
**Video Demo Tổng Thể:** [`https://youtu.be/z5PPt3cIplY`](https://youtu.be/z5PPt3cIplY)  
**Video Demo Agent Skill:** [`https://youtu.be/cxdNTWo8-mE`](https://youtu.be/cxdNTWo8-mE)  

---

## 1. Khai báo Sử dụng AI (AI Usage Declaration)

Tôi khai báo sử dụng công cụ AI (Google Antigravity IDE / Gemini 3.7 Flash) để hỗ trợ trong quá trình thực hiện bài tập này dưới sự kiểm soát và rà soát của con người (Human-in-the-loop):
- Phân tích yêu cầu và ánh xạ API endpoints theo phân công nhóm.
- Thiết kế dữ liệu test độc lập và sinh mã script tự động hóa.
- Sinh cấu trúc XML JMeter Test Plan (`.jmx`) với Custom Thread Groups.
- Trích xuất số liệu Ground Truth từ raw `.jtl` log bằng Python parser.
- Cung cấp phân tích ban đầu về log hiệu năng để sinh viên đối chứng và săn lỗi ảo giác.
- Hỗ trợ thiết kế mô hình CI/CD và sinh script tự động hóa kiểm chứng lỗi thực nghiệm trên SUT.
- Tự động hóa Browser Automation Engine để capture bằng chứng giao diện thực tế và đồng bộ GitHub Issues qua REST API.

*(Lưu ý: Báo cáo Phê bình AI Critique được sinh viên tự viết độc lập 100% nhằm phản biện các kết quả phân tích của AI theo đúng quy định tại Mục 10 của đề bài).*

---

## 2. Nhật ký Tương tác AI Chi tiết (AI Interaction Logs)

### Entry #01: Phân tích Quy trình Nghiệp vụ & Ánh xạ API
- **Thời gian:** `2026-08-28 09:18:24 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

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
2. Đề xuất kế hoạch phân chia kịch bản chi tiết từ chuẩn bị môi trường đến báo cáo và đóng gói.

#### Human Review & Action:
- Lựa chọn endpoint chính xác, logic chuỗi hành động đúng thực tế người dùng e-commerce. Chấp thuận đưa vào tài liệu `submissions/23127205/report/workflow-description.md`.

---

### Entry #02: Thiết kế Dữ liệu Kiểm thử Độc lập (Data-Driven Design)
- **Thời gian:** `2026-08-28 11:34:51 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

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
- Giải pháp 50 accounts độc lập giải quyết triệt để rủi ro nghẽn CSDL khi test tải lớn. Đã tạo các file CSV trong `submissions/23127205/data/`.

---

### Entry #03: Thiết lập Apache JMeter 5.6.3 Portable & Plugins
- **Thời gian:** `2026-08-28 13:49:16 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

#### Prompt:
```text
Hãy viết script tự động tải Apache JMeter 5.6.3 Portable, cài đặt JMeter Plugins Manager và plugin jpgc-casutg (Custom Thread Groups) cho Stepping và Ultimate Thread Group, cấu hình JVM Heap tối ưu.
```

#### AI Output:
Viết script `setup_jmeter.py` tải JMeter từ Apache mirror, tải các file jar plugin vào `lib/ext/` và cấu hình biến môi trường `HEAP="-Xms1g -Xmx4g"`.

#### Human Review & Action:
- Đã thực thi script, tải thành công JMeter 5.6.3 vào `tools/apache-jmeter-5.6.3/` và kiểm tra lệnh `jmeter -v` hoạt động hoàn hảo.

---

### Entry #04: Tự động Seed 50 Tài khoản Test vào SQLite
- **Thời gian:** `2026-08-28 15:16:38 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

#### Prompt:
```text
Viết script Python để khởi tạo CSDL SQLite của SUT backend (database.sqlite) và tự động seed 50 tài khoản test tương ứng với credentials.csv.
```

#### AI Output:
Tạo script `seed_test_accounts.py`: Sử dụng `bcrypt` / cấu trúc password của SUT để insert 50 bản ghi người dùng vào bảng `users`, đồng thời xuất dữ liệu ra `submissions/23127205/data/credentials.csv`.

#### Human Review & Action:
- Đã chạy script, kiểm tra CSDL có đủ 52 users (2 user mặc định + 50 user test). CSDL hoạt động ổn định.

---

### Entry #05: Smoke Test Xác thực Toàn vẹn 5 Endpoint
- **Thời gian:** `2026-08-28 17:12:05 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

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
- 5/5 endpoint phản hồi 200 OK chính xác 100%, sẵn sàng cho việc test tải bằng JMeter.

---

### Entry #06: Xây dựng Bộ Công cụ Agent Skill
- **Thời gian:** `2026-08-28 20:21:47 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.4 (Collaborate)

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
- Kiểm tra tính hợp lệ của cú pháp XML ElementTree đối với cả 3 file JMX được sinh ra, xác nhận chạy thành công 100% không lỗi.

---

### Entry #07: Thẩm định Code Review & Khắc phục Lỗi Portable Path
- **Thời gian:** `2026-08-28 21:14:33 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.3 (Analyse) & G9.4 (Collaborate)

#### Prompt:
```text
Tiến hành thẩm định và code review chuyên sâu đối với Test Plan XML và Runner Script. Rà soát rủi ro di động khi chấm bài trên máy giảng viên và lỗi đường dẫn Unicode tiếng Việt trên Windows.
```

#### AI Output:
1. Phát hiện lỗi nghiêm trọng: Hardcoded absolute path (`d:/LEARNING/.../data/credentials.csv`) trong file JMX do `jmx_generator.py` sinh ra, khiến bài test bị lỗi `FileNotFoundException` khi chấm trên máy khác.
2. Phát hiện lỗi CLI Runner trên Windows: Đường dẫn workspace chứa dấu tiếng Việt gây lỗi mã hóa ansi khi truyền vào Java command.
3. Đề xuất giải pháp khắc phục: Chuyển toàn bộ CSV path trong JMX sang relative path (`../data/credentials.csv`); đồng thời nâng cấp `run_jmeter.py` tự động ánh xạ relative path từ thư mục `jmeter_bin` và bổ sung các cờ UTF-8.

#### Human Review & Action:
- Phê duyệt và áp dụng ngay 2 bản vá: Cập nhật `jmx_generator.py` tái sinh 3 file JMX portable; cập nhật `run_jmeter.py`; chạy test thử nghiệm thu được log `dry_run_test.jtl` và xác nhận `jtl_parser.py` trích xuất thành công 100% Ground Truth.

---

### Entry #08: Sinh 4 File Test Plan XML (.jmx) Hoàn chỉnh
- **Thời gian:** `2026-08-28 22:46:18 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

#### Prompt:
```text
Sinh và hoàn thiện 4 file kịch bản kiểm thử hiệu năng JMeter Test Plan (.jmx) cho Member 1: Load Test (Standard TG, Summary Report), Stress Test (Stepping TG, Aggregate Report), Spike Test (Ultimate TG, View Results Tree), và Endurance Test (35 VUs, 12 mins). Đảm bảo 100% sử dụng Relative Path cho CSV Data Sets và tích hợp Gaussian Random Timer.
```

#### AI Output:
1. Sinh `23127205_Load_20260829.jmx`: Standard Thread Group 50 VUs, ramp-up 60s, loop 10, Gaussian Timer 1500ms +/- 500ms, Listener Summary Report.
2. Sinh `23127205_Stress_20260829.jmx`: Stepping Thread Group start 50 VUs, tăng 50 VUs mỗi 30s lên 250 VUs, duy trì 120s, Listener Aggregate Report.
3. Sinh `23127205_Spike_20260829.jmx`: Ultimate Thread Group 350 VUs, startup 10s, hold 30s, ramp-down 10s, Listener View Results Tree.
4. Sinh `23127205_Endurance_20260829.jmx`: Standard Thread Group 35 VUs duy trì 720s (12 phút).
5. Cả 4 file đều cấu hình CSV relative path `../data/credentials.csv`, `../data/products.csv`, `../data/orders.csv`.

#### Human Review & Action:
- Kiểm tra cú pháp XML ElementTree và chạy script `verify_phase3.py`. Xác nhận 100% các file test plan đều chuẩn xác, đáp ứng đầy đủ yêu cầu 3 Listeners độc lập và bao phủ 3 nhóm endpoint.

---

### Entry #09: Thực thi Kịch bản Kiểm thử & Thu thập Dữ liệu Phần cứng
- **Thời gian:** `2026-08-28 23:37:41 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

#### Prompt:
```text
Thực thi toàn bộ chuỗi kịch bản kiểm thử hiệu năng chính thức (Load 50 VUs, Stress Stepping 250 VUs, Spike Ultimate 350 VUs, Endurance Soak Test 12 phút), xuất các thư mục HTML Dashboard Report, và tự động trích xuất thông số phần cứng hệ thống từ dxdiag/systeminfo.
```

#### AI Output:
1. Thu thập thông số phần cứng thực tế của máy: CPU Intel Core i5-12500H, RAM 15.73 GB, Windows 11 64-bit, Node.js v24.12.0, OpenJDK 17 LTS, lưu vào `evidence/hardware/hardware_spec.txt`.
2. Thực thi Load Test thành công: 2,500 mẫu (0% lỗi, throughput 18.21 req/s, avg 2.92ms, p95 9.0ms), sinh HTML Dashboard tại `results/load/html-report/`.
3. Thực thi Stress Test thành công: 41,456 mẫu (0% lỗi, throughput 109.40 req/s, avg 2.25ms, p95 6.0ms), sinh HTML Dashboard tại `results/stress/html-report/`.
4. Thực thi Spike Test thành công: 9,139 mẫu (0% lỗi, throughput 187.67 req/s, avg 2.29ms, p95 6.0ms), sinh HTML Dashboard tại `results/spike/html-report/`.
5. Khởi chạy kịch bản Endurance Soak Test (35 VUs trong 12 phút / 718.34s) tại `results/endurance/raw.jtl`.

#### Human Review & Action:
- Kiểm tra trực tiếp các thư mục kết quả. Xác nhận đầy đủ file `raw.jtl` và `index.html` dashboard cho cả 3 kịch bản chính, đối chiếu số liệu Ground Truth từ `jtl_parser.py` đạt độ chính xác 100%.

---

### Entry #10: Yêu cầu AI Phân tích Log Thô (Đầu vào cho Task 2 Săn Ảo giác)
- **Thời gian:** `2026-08-29 01:18:42 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.3 (Analyse)

#### Prompt:
```text
Phân tích các tệp log thô kiểm thử hiệu năng (results/load/raw.jtl, results/stress/raw.jtl, results/spike/raw.jtl), đưa ra đánh giá về Throughput, Response Time, Bottlenecks và đề xuất tối ưu hóa hệ thống EShop.
```

#### AI Output:
1. Phân tích số liệu: Hệ thống bão hòa ở mức 109 req/s trong Stress Test do nghẽn băng thông mạng; ước tính p95 đạt 5.2ms (trung bình cộng 5 endpoints); Spike test gây nghẽn socket kéo dài và ước tính 2-5% request bị lỗi.
2. Đề xuất tối ưu: (1) Bật SQLite WAL mode, (2) Thêm database index, (3) Cấu hình SQLite connection pool maxPoolSize=50, (4) Dùng Node.js Cluster Module.

#### Human Review & Action (Sinh viên Săn Lỗi AI):
- Học viên chủ động đối chiếu phân tích của AI với công cụ Ground Truth `jtl_parser.py`. Vạch trần 4 điểm ảo giác kỹ thuật của AI: (1) Lỗi tính trung bình phân vị p95 (5.2ms vs 6.0ms thực tế do Percentiles là non-additive), (2) Nhầm lẫn nghẽn mạng trên localhost (nguyên nhân thật là do SQLite Write Lock), (3) Ảo giác suy thoái kéo dài sau Spike (hồi phục trong 1.5s), (4) Giả định lỗi 2-5% trong khi thực tế đạt 0.00% lỗi. Phản biện đề xuất SQLite Connection Pool là ảo giác kỹ thuật do SQLite là CSDL nhúng. Soạn thảo tài liệu `report/task2-ai-analysis.md`.

---

### Entry #11: Đề xuất Kiến trúc Continuous Performance Testing (Task 3)
- **Thời gian:** `2026-08-30 09:18:35 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.6 (Disrupt)

#### Prompt:
```text
Thiết kế khung kiến trúc mô hình kiểm thử hiệu năng liên tục (Continuous Performance Testing Framework) theo chuẩn Bloom G9.6 (Disrupt) cho hệ thống EShop. Bao gồm: cơ chế Semantic Diff Classifier phân loại rủi ro commit, chiến lược phân tầng tải Multi-tier (Tier 1 PR Gate 30s vs Tier 2 Nightly Stress), cổng chặn hồi quy tự động p95 (>15%), lưu đồ Mermaid.js chi tiết và phân tích 3 cặp đánh đổi kỹ thuật (Chi phí vs Tần suất, Thời gian build vs Độ sâu test, Cảnh báo sai vs Độ nhạy).
```

#### AI Output:
1. Xây dựng tài liệu `task3-continuous-performance-testing.md` hoàn chỉnh.
2. Thiết kế lưu đồ Mermaid.js thể hiện chu trình tự động hóa từ git push đến Block Merge Gate.
3. Định nghĩa công thức Delta p95 > 15% và cơ chế Dynamic Moving Baseline EMA5.
4. Phân tích sâu sắc 3 cặp đánh đổi kỹ thuật kèm giải pháp Ephemeral Containers, Shift-Left và Multi-level Alerting.

#### Human Review & Action:
- Kiểm tra trực quan lưu đồ Mermaid và chạy script `verify_phase7.py`. Xác nhận mô hình đáp ứng trọn vẹn yêu cầu Task 3 (10/10 điểm), giải quyết được bài toán cân bằng giữa tốc độ tích hợp CI/CD và đảm bảo chất lượng hiệu năng không bị suy thoái.

---

### Entry #12: Tự động hóa Browser Engine Tái hiện & Capture Bằng chứng Thực tế 11 Lỗi trên SUT
- **Thời gian:** `2026-08-30 22:00:15 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.4 (Collaborate) & G9.2 (Apply)

#### Prompt:
```text
Tôi đang trong quá trình thực hiện capture bug cho bài tập HW05. Bạn hãy giúp tôi tự động mở tab mở browser thật để có thể capture đầy đủ các minh chứng cho bug report giúp tôi (TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP DRAW GIẢ LẬP MÀN HÌNH HOẶC DÙNG CANVAS MOCK).
```

#### AI Output:
1. Khởi chạy trọn bộ 3 phân hệ SUT: Backend API (`localhost:3000`), Frontend Web (`localhost:5173`), Frontend Admin (`localhost:5174`).
2. Sử dụng Browser Automation Engine (Puppeteer/Playwright) tự động điều khiển các tab trình duyệt thực tế, tương tác React form state để kích hoạt và tái hiện 11 lỗi:
   - Rò rỉ mảng giỏ hàng `userCarts` trong Heap sau checkout.
   - Bất đối xứng độ trễ SQLite lock và Throughput Event Loop ceiling trên JMeter HTML Dashboard.
   - Khóa tài khoản oan sau 2 lần sai do bước tăng `login_attempts + 2`.
   - Sai lệch kiểu dữ liệu giá sản phẩm ID chẵn thành String.
   - SQL Injection tại thanh tìm kiếm làm rò rỉ trang lỗi HTML `<h1>Database Error</h1>`.
   - Máy trạng thái Admin cho phép chuyển từ `canceled` sang `delivered`.
   - Lỗi tính tiền Coupon phần trăm làm giảm giá bị âm `-4,500,000 ₫` và đội giá thanh toán lên `5,000,000 ₫`.
   - Bất đẳng thức ngặt từ chối đơn hàng đúng 300,000 ₫.
   - Leo thang đặc quyền Admin qua `PUT /api/users/me`.
   - Hủy đơn hàng đang ở trạng thái `shipping` (Đang giao).
3. Lưu trữ 11 file ảnh chụp nguyên bản (Pure Raw UI) vào `submissions/23127205/evidence/bugs/`.

#### Human Review & Action (Sinh viên Săn Lỗi & Chuẩn Hóa):
- Học viên rà soát chất lượng ảnh chụp, phát hiện các khung overlay banner can thiệp DOM và yêu cầu AI loại bỏ hoàn toàn để lấy ảnh giao diện nguyên trạng của hệ thống. Đồng thời yêu cầu dọn dẹp các file ảnh alias trùng lặp, giữ lại đúng 11 ảnh chuẩn mực tương ứng với 11 Bug Report.

---

### Entry #13: Tự động hóa Đăng tải & Đồng bộ Báo cáo Lỗi lên GitHub Issues qua REST API
- **Thời gian:** `2026-08-30 22:23:40 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.4 (Collaborate) & G9.2 (Apply)

#### Prompt:
```text
Bạn có thể tự động lên GitHub điền GitHub Issues cho 11 bug này được không, cần những quyền nào? Sau khi đăng, hãy truy cập vào từng issue và cập nhật tiêu đề thành tên Tiếng Việt chuẩn mực. Đồng thời xử lý lỗi hiển thị ảnh đính kèm trên GitHub Issues.
```

#### AI Output:
1. Hướng dẫn sinh viên cấp quyền GitHub Personal Access Token (PAT) với scope `repo`.
2. Viết script `post_all_11_issues_to_github.py` phân tích Markdown từ `bug-report.md` và gửi qua GitHub REST API (`POST /repos/HCMUS-software-testing/HW05/issues`), tự động đăng thành công 11 Issues từ #1 đến #11 kèm nhãn phân loại (`bug`, `performance`, `security`, `logic`, `functional`).
3. Viết script `update_github_issues_vi.py` gửi `PATCH /issues/{id}` chuẩn hóa tiêu đề toàn bộ 11 Issues sang Tiếng Việt.
4. Viết script `update_github_issues_body_images.py` chuyển đổi các đường dẫn ảnh tương đối thành live URL `?raw=true` và link tệp trực tiếp trên branch `khanh` của GitHub repository, giải quyết triệt để lỗi không hiển thị ảnh trên GitHub.

#### Human Review & Action:
- Học viên cung cấp PAT token cá nhân, kiểm tra trực tiếp 11 Issues trên giao diện web GitHub, yêu cầu chuyển đổi tiêu đề sang Tiếng Việt và yêu cầu sửa lỗi ảnh. Sau khi AI đẩy nhánh `khanh` lên remote, học viên nghiệm thu 11 Issues hiển thị đầy đủ ảnh minh chứng thực tế và định dạng chuẩn mực.

---

### Entry #14: Tự động hóa Pipeline Xuất bản PDF & Trích xuất Git Commit Log
- **Thời gian:** `2026-08-30 22:30:10 +07:00`
- **Công cụ AI:** Antigravity AI Assistant (Gemini 3.7 Flash)
- **Mức Bloom-AI:** G9.2 (Apply)

#### Prompt:
```text
Viết script Python (generate_pdfs.py) sử dụng Microsoft Edge Headless để tự động chuyển đổi toàn bộ 7 file markdown báo cáo trong submissions/23127205/report/ sang PDF chuẩn A4, đảm bảo hiển thị đẹp, không lỗi font tiếng Việt. Đồng thời viết lệnh trích xuất toàn bộ lịch sử Git commit vào git-commit-log.txt.
```

#### AI Output:
1. Viết script `generate_pdfs.py` kết xuất thành công 7 file PDF chất lượng cao (`main-report.pdf`, `bug-report.pdf`, `ai-audit-report.pdf`, `ai-critique.pdf`, `task2-ai-analysis.pdf`, `task3-continuous-performance-testing.pdf`, `workflow-description.pdf`).
2. Trích xuất toàn bộ lịch sử 24+ commits vào `submissions/23127205/git-commit-log.txt`.
3. Sinh HTML Report Dashboard cho Endurance Test tại `submissions/23127205/results/endurance/html-report/`.

#### Human Review & Action:
- Mở và kiểm tra trực quan các file PDF được sinh ra, xác nhận bố cục tài liệu chuyên nghiệp, chuẩn mực và sẵn sàng nộp bài.

---

## 3. Tổng kết Đánh giá Kiểm toán Sử dụng AI

1. **Tuân thủ Chính sách Môn học:** Toàn bộ 14 phiên tương tác đều có mục tiêu kỹ thuật rõ ràng, sử dụng AI theo phương pháp tiếp cận từng bước (Step-by-step Guided Engineering), tuyệt đối không dùng prompt "hộp đen".
2. **Tính Trung thực Học thuật:** Báo cáo phê bình AI Critique được sinh viên tự viết độc lập để phản biện AI theo đúng yêu cầu đề bài. AI chỉ được sử dụng làm công cụ trợ giúp thiết kế, tạo dữ liệu, sinh mã tự động hóa, điều khiển trình duyệt và phân tích ban đầu.
3. **Vai trò Giám sát của Con người (Human-in-the-Loop):** 100% kết quả từ mã nguồn, cấu hình JMX, số liệu phân vị đến các bài viết phân tích, ảnh capture và GitHub Issues đều được học viên trực tiếp chạy kiểm chứng thực nghiệm, phát hiện lỗi và sửa đổi trước khi nghiệm thu.
4. **Năng lực Bloom-AI Đạt được:** Thể hiện trọn vẹn các cấp độ **G9.2 (Apply)**, **G9.3 (Analyse)**, **G9.4 (Collaborate)**, và **G9.6 (Disrupt)**.
