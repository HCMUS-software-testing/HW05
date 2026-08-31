# Báo cáo nhật ký sử dụng AI

## Tuyên bố

I use AI tools for the following tasks: lập bản đồ endpoint, thiết kế workload/test plan, sinh XML JMeter, review correlation/assertion, thiết kế script phân tích JTL, đề xuất threshold, kiểm tra package và đề xuất kiểm thử hiệu năng liên tục.

Các phiên Codex ban đầu không còn transcript nguyên văn; vì vậy prompt trong tương tác 1-7 được khôi phục từ nhật ký công việc và artifact đã commit, không tuyên bố là bản chép nguyên văn. Không có metric, screenshot, video, GitHub Issue hoặc kết quả chạy nào được AI bịa thêm.

## Chi tiết prompt và output

### Tương tác 1 - Phân rã yêu cầu

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-29 09:10 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Đọc `req/2026.HW05.Performance Testing_Vi.md` và `plan/plan.md`. Hãy phân rã toàn bộ deliverable bắt buộc cho MSSV 23127326, tách rõ ba kịch bản Load/Stress/Spike, workflow auth-heavy/read-heavy/transactional, CSV, JTL, HTML report, resource/hardware evidence, endurance, video, AI Audit, AI Critique, Git log và Agent Skill. Không tạo bằng chứng chạy giả.

**Đầu ra của AI:**

- Chọn một workflow E2E chung cho cả ba plan.
- Bắt buộc lưu ba JMX, ba JTL, ba HTML report và ba report view không trùng.
- Tách negative lockout probe khỏi positive performance run.
- Ghi thêm endurance 10-15 phút, resource monitor, hardware, video, AI audit/critique và commit log.
- Cảnh báo không được sinh JTL, screenshot, video hoặc issue evidence bằng AI.

### Tương tác 2 - Review contract và implementation

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-29 10:05 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Review API specification và mã backend EShop cho workflow thành viên 3: login có lockout, product listing có search/page/limit, cart add/update và checkout. Lập bảng method/path, correlation, assertion và chỉ ra khoảng cách giữa contract với implementation. Chỉ nêu bug khi có thể tái hiện.

**Đầu ra của AI:**

| Phạm vi | Kết quả review |
| --- | --- |
| Lockout | Implementation có khả năng cộng sai số lần và dùng 180 giây thay vì 30 giây; cần probe độc lập. |
| Pagination | Endpoint đọc `search` nhưng có thể bỏ qua `page`/`limit`; cần so sánh response nhiều trang. |
| Cart quantity | Lần POST thứ hai có thể `push` dòng mới thay vì update quantity. |
| Checkout | Server có thể tin `total_amount` từ client và không xóa cart sau checkout. |

### Tương tác 3 - Sinh và sửa JMeter plans

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-29 14:20 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Sinh ba JMeter plan `23127326_Load_20260830.jmx`, `23127326_Stress_20260830.jmx`, `23127326_Spike_20260830.jmx`. Cả ba dùng cùng E2E flow login -> search products -> cart add -> cart update -> cart get -> checkout -> verify cart. Dùng CSV, correlate JWT/product/order, think-time thực tế, assertion có ý nghĩa và ba listener khác nhau. Tách lockout probe, tắt nó trong positive run và tắt GUI listener khi chạy non-GUI.

**Đầu ra của AI:**

- Load: 20 VU, ramp-up 60 giây, giữ 300 giây; View Results Tree.
- Stress: 100 VU, ramp-up 300 giây, giữ 180 giây; Summary Report.
- Spike: 10 VU nền + 90 VU spike, ramp 5 giây, delay 120 giây, giữ spike 120 giây; Aggregate Report.
- CSV ban đầu dùng chung cho nhiều thread.

- Sau phản hồi review, thiết kế được sửa sang `data/per-vu/input-${__threadNum}.csv`, `Recycle on EOF=false`, `Stop thread on EOF=true`; Spike offset nhóm spike sau 10 tài khoản nền và duration tính cả ramp-up lẫn hold.

### Tương tác 4 - Phân tích JTL và threshold

**Tên công cụ AI:** Codex analyzer

**Ngày và giờ:** 2026-08-30 09:40 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Đọc các raw JTL chính thức. Tính sample count, elapsed window, throughput, HTTP RPS chỉ cho row có URL, mean, median, p90, p95, p99, max và error rate theo label. Phân biệt HTTP/network error với JMeter assertion failure. Đề xuất threshold có thể truy nguyên và không kết luận memory leak nếu thiếu chuỗi quan sát.

**Đầu ra của AI:**

> Khoảng 10-11% sample thất bại có thể là server error; nên xem xét DB index, connection pool hoặc SQLite WAL.

Sau khi được yêu cầu tính lại raw JTL, AI trả về:

| Run | Assertion failure | HTTP/network error | HTTP RPS |
| --- | ---: | ---: | ---: |
| Load | 356/3.287 | 0/3.287 | 7,1076 |
| Stress | 1.780/16.433 | 0/16.433 | 26,7113 |
| Spike | 751/7.171 | 0/7.171 | 13,2665 |
| Endurance 70 VU | 2.699/24.574 | 0/24.574 | 23,6465 |

Mọi failure canonical nằm ở assertion `POST_CHECKOUT_CART - expected empty`; không được gọi là HTTP/server error. JMeter sample throughput không đồng nhất với HTTP RPS vì hai JSR223 sampler nội bộ cũng sinh JTL row.

### Tương tác 5 - Đề xuất tối ưu

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-30 11:15 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Dựa trên JTL và gap implementation, đề xuất các hướng tối ưu. Phân loại từng đề xuất thành khả thi có bằng chứng, cần profiling, hoặc ảo giác. Không suy nguyên nhân từ p95/error rate nếu JTL không chứng minh.

**Đầu ra của AI:**

- Sửa checkout tự tính total và xóa cart: **khả thi**, có contract, implementation và assertion.
- Bổ sung pagination và cart quantity semantics: **khả thi**, có probe/issue.
- Thêm DB index: **cần profiling**, chưa có query plan hay slow-query log.
- Điều chỉnh connection pool/bật SQLite WAL: **cần profiling**, chưa có bằng chứng contention.
- Tăng Node worker để sửa fail 10-11%: **ảo giác**, vì fail là assertion nghiệp vụ.

### Tương tác 6 - Audit package

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-30 13:05 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Kiểm tra package theo acceptance checklist của HW05: tên file, JMX/JTL/HTML, data, report Markdown/PDF, resource/hardware screenshot, video link, AI Audit, AI Critique, Git log, issues và Agent Skill. Chỉ ra file stale, evidence không hợp lệ và mâu thuẫn giữa report với raw log.

**Đầu ra của AI:**

- Bổ sung README summary, endpoint map, threshold và hardware table.
- Loại CSV monitor cũ dùng `thcount` không tồn tại trên macOS.
- Yêu cầu rerun resource monitor bằng CPU/RSS/thread hợp lệ.
- Bổ sung issue evidence và phân biệt artifact canonical/invalid.
- Giữ video ở trạng thái chưa hoàn tất thay vì tạo evidence giả.

### Tương tác 7 - Staircase và endurance threshold

**Tên công cụ AI:** Codex

**Ngày và giờ:** 2026-08-30 15:35 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Đối chiếu metric canonical với JTL, loại run có login 401 hoặc duration sai. Thiết kế staircase 70/100/150/200 VU, sau đó soak 10 phút ở mức cao nhất đạt SLO. Báo HTTP RPS trong hold, p95, HTTP error, assertion, CPU, RSS và xu hướng theo cửa sổ. Chỉ gọi là maximum stable observed trong dải đã thử.

**Đầu ra của AI:**

- 70/100/150/200 VU đều đạt SLO screening.
- Soak 200 VU giữ đủ 600 giây: 77,4400 HTTP RPS, p95 5 ms, HTTP error 0%, CPU tối đa 17,7%, RSS tối đa 119,3 MB.
- Ba cửa sổ 200 giây: 77,8950; 77,3650; 77,0600 HTTP RPS; cửa sổ cuối thấp hơn đầu 1,072%.
- Kết luận giới hạn: `maximum stable observed = 77,4400 HTTP RPS at 200 VU`, không tuyên bố trần tuyệt đối.

### Tương tác 8 - Evidence same-screen

**Tên công cụ AI:** Codex + Computer Use

**Ngày và giờ:** 2026-08-30 18:04 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Chạy lại kịch bản trên host và chụp screenshot tĩnh cùng màn hình với terminal/JMeter và Activity Monitor. Backend PID phải khớp ở hai cửa sổ; không ghép evidence từ hai thời điểm. Không quay hoặc giả lập video của sinh viên.

**Đầu ra của AI:**

- Stress: backend PID `31159` khớp terminal và Activity Monitor.
- Spike: backend PID `35179` khớp terminal và Activity Monitor.
- Endurance: backend PID `54267` khớp; JMeter hiển thị `Active: 200`.
- Load cũ chưa có bằng chứng PID rõ tương đương và được giữ là mục cần chụp lại, không đánh dấu hoàn tất.
- Không record video; video phải do sinh viên tự quay và thuyết minh.

### Tương tác 9 - Kiểm tra listener bằng JMeter GUI

**Tên công cụ AI:** Codex + Apache JMeter GUI 5.6.3

**Ngày và giờ:** 2026-08-30 19:16 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Kiểm tra ba listener riêng của Load/Stress/Spike và sửa phần evidence liên quan. Không dùng HTML dashboard chung để thay cho View Results Tree, Summary Report và Aggregate Report; không tạo ảnh evidence giả.

**Đầu ra của AI:**

- JMeter báo lỗi khi mở JMX vì metadata XML đặt sai vai trò của `guiclass` và `testclass` cho `ResultCollector`.
- `UniformRandomTimer` và `JSONPostProcessor` cũng đang dùng `TestBeanGUI`, không phải GUI class tương ứng.

Sau khi sửa và kiểm tra lại, AI trả về:

- Generator dùng `testclass="ResultCollector"` và ba `guiclass` chuẩn: `ViewResultsFullVisualizer`, `SummaryReport`, `StatVisualizer`.
- Timer dùng `UniformRandomTimerGui`; JSON extractor dùng `JSONPostProcessorGui`.
- Cả ba file Load/Stress/Spike được JMeter 5.6.3 tải thành công; log không có `ERROR` hoặc exception khi parse plan.
- Listener vẫn để `enabled="false"` cho execution non-GUI. Việc nạp JTL và chụp evidence sau chạy được ghi ở tương tác 10.

### Tương tác 10 - Hoàn thiện Load và listener evidence

**Tên công cụ AI:** Codex + Computer Use + Apache JMeter 5.6.3 + Activity Monitor

**Ngày và giờ:** 2026-08-30 21:27 (Asia/Ho_Chi_Minh)

**Prompt của bạn:**

> Chụp lại Load với JMeter `Active`, backend PID và Activity Monitor trong cùng màn hình. Mở ba JTL bằng View Results Tree, Summary Report và Aggregate Report rồi chụp ảnh. Chỉ dùng lần chạy và raw JTL thật.

**Đầu ra của AI:**

- Khởi động EShop cô lập với process title `HW05_LOAD_BE`, PID `97107`; Activity Monitor được lọc đúng process và hiển thị cùng PID.
- Chạy Load 20 VU; raw JTL đang ghi xác nhận `allThreads=20`. Frame evidence cùng màn hình hiển thị `Active=20`, backend PID `97107` ở terminal và Activity Monitor.
- Nạp bộ JTL canonical `results/resource-rerun/` bằng chính component JMeter 5.6.3 và render ba listener: Load/View Results Tree, Stress/Summary Report, Spike/Aggregate Report.
- Không dùng HTML dashboard chung để thay cho ba listener; không nhập tay sample count hoặc metric vào ảnh listener.
