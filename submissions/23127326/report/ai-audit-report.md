# Báo cáo nhật ký sử dụng AI

## Tuyên bố

I use AI tools for the following tasks: lập bản đồ endpoint, thiết kế workload/test plan, sinh XML JMeter, review correlation/assertion, thiết kế script phân tích JTL, đề xuất threshold, lập checklist human review và đề xuất kiểm thử hiệu năng liên tục.

## Phạm vi và tính toàn vẹn của nhật ký

Nhật ký dưới đây ghi tên công cụ, thời gian, prompt và phần đầu ra AI đã được dùng để ra quyết định. Các phiên Codex ban đầu không còn transcript nguyên văn; vì vậy prompt trong mục 1-7 được **khôi phục từ nhật ký công việc và artifact đã commit**, không tuyên bố là bản chép nguyên văn. Không có metric, screenshot, video, GitHub Issue hoặc kết quả chạy nào được AI bịa thêm.

Phần output bên dưới lưu nội dung quan trọng đã được chấp nhận hoặc bị human review bác bỏ. Output dạng file hoàn chỉnh được truy nguyên bằng đường dẫn artifact thay vì chép lặp hàng nghìn dòng XML/JTL vào phụ lục.

## Bảng tóm tắt tương tác

| # | Công cụ | Ngày giờ (Asia/Ho_Chi_Minh) | Mục tiêu | Output/artifact chính |
| ---: | --- | --- | --- | --- |
| 1 | Codex | 2026-08-29 09:10 | Phân rã đề bài và lập checklist | Phạm vi, deliverable và ràng buộc evidence |
| 2 | Codex | 2026-08-29 10:05 | Review API/implementation EShop | Bốn gap lockout, pagination, cart và checkout |
| 3 | Codex | 2026-08-29 14:20 | Sinh và review ba JMeter plan | Ba JMX, CSV theo VU và ba report view riêng |
| 4 | Codex analyzer | 2026-08-30 09:40 | Phân tích JTL và đề xuất threshold | JSON canonical và phân loại HTTP/assertion |
| 5 | Codex + human review | 2026-08-30 11:15 | Đề xuất và thẩm định tối ưu | Bảng khả thi/cần profiling/ảo giác |
| 6 | Codex + human review | 2026-08-30 13:05 | Audit package và evidence | Checklist package, hardware/resource/issue evidence |
| 7 | Codex + human review | 2026-08-30 15:35 | Sửa metric canonical và tìm endurance threshold | Staircase 70/100/150/200 VU và soak 200 VU |
| 8 | Codex + Computer Use | 2026-08-30 18:04 | Chụp evidence same-screen | Ảnh Stress/Spike/Endurance có PID khớp |
| 9 | Codex + JMeter GUI | 2026-08-30 19:16 | Kiểm tra ba listener trong JMeter | Sửa metadata GUI và xác nhận ba JMX tải không lỗi |

## Chi tiết prompt và output

### Tương tác 1 - Phân rã yêu cầu

**Công cụ:** Codex
**Thời gian:** 2026-08-29 09:10 (Asia/Ho_Chi_Minh)
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Đọc `req/2026.HW05.Performance Testing_Vi.md` và `plan/plan.md`. Hãy phân rã toàn bộ deliverable bắt buộc cho MSSV 23127326, tách rõ ba kịch bản Load/Stress/Spike, workflow auth-heavy/read-heavy/transactional, CSV, JTL, HTML report, resource/hardware evidence, endurance, video, AI Audit, AI Critique, Git log và Agent Skill. Không tạo bằng chứng chạy giả.

**Output AI đã dùng:**

- Chọn một workflow E2E chung cho cả ba plan.
- Bắt buộc lưu ba JMX, ba JTL, ba HTML report và ba report view không trùng.
- Tách negative lockout probe khỏi positive performance run.
- Ghi thêm endurance 10-15 phút, resource monitor, hardware, video, AI audit/critique và commit log.
- Cảnh báo không được sinh JTL, screenshot, video hoặc issue evidence bằng AI.

**Human review:** đối chiếu lại checklist với đề tiếng Việt; giữ video và evidence thật là công việc thủ công.

### Tương tác 2 - Review contract và implementation

**Công cụ:** Codex
**Thời gian:** 2026-08-29 10:05
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Review API specification và mã backend EShop cho workflow thành viên 3: login có lockout, product listing có search/page/limit, cart add/update và checkout. Lập bảng method/path, correlation, assertion và chỉ ra khoảng cách giữa contract với implementation. Chỉ nêu bug khi có thể tái hiện.

**Output AI đã dùng:**

| Phạm vi | Kết quả review |
| --- | --- |
| Lockout | Implementation có khả năng cộng sai số lần và dùng 180 giây thay vì 30 giây; cần probe độc lập. |
| Pagination | Endpoint đọc `search` nhưng có thể bỏ qua `page`/`limit`; cần so sánh response nhiều trang. |
| Cart quantity | Lần POST thứ hai có thể `push` dòng mới thay vì update quantity. |
| Checkout | Server có thể tin `total_amount` từ client và không xóa cart sau checkout. |

**Artifact hoàn chỉnh:** `agent-skill/performance-test-workflow/references/eshop-contract.md`, `evidence/issues/*.jsonl` và GitHub Issues #1-#4.
**Human review:** chạy probe thật trước khi tạo issue; không coi review mã nguồn là execution evidence.

### Tương tác 3 - Sinh và sửa JMeter plans

**Công cụ:** Codex
**Thời gian:** 2026-08-29 14:20
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Sinh ba JMeter plan `23127326_Load_20260830.jmx`, `23127326_Stress_20260830.jmx`, `23127326_Spike_20260830.jmx`. Cả ba dùng cùng E2E flow login -> search products -> cart add -> cart update -> cart get -> checkout -> verify cart. Dùng CSV, correlate JWT/product/order, think-time thực tế, assertion có ý nghĩa và ba listener khác nhau. Tách lockout probe, tắt nó trong positive run và tắt GUI listener khi chạy non-GUI.

**Output AI ban đầu:**

- Load: 20 VU, ramp-up 60 giây, giữ 300 giây; View Results Tree.
- Stress: 100 VU, ramp-up 300 giây, giữ 180 giây; Summary Report.
- Spike: 10 VU nền + 90 VU spike, ramp 5 giây, delay 120 giây, giữ spike 120 giây; Aggregate Report.
- CSV ban đầu dùng chung cho nhiều thread.

**Human review và sửa:** CSV chung làm thread đầu tiên tiêu thụ lifecycle của thread khác. Thiết kế cuối chuyển sang `data/per-vu/input-${__threadNum}.csv`, `Recycle on EOF=false`, `Stop thread on EOF=true`; Spike offset nhóm spike sau 10 tài khoản nền. Duration được sửa để tính cả ramp-up và hold.

**Artifact hoàn chỉnh:** `test-plans/*.jmx`, `test-plans/generate_plans.py`, `data/per-vu/*.csv`.

### Tương tác 4 - Phân tích JTL và threshold

**Công cụ:** Codex analyzer
**Thời gian:** 2026-08-30 09:40
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Đọc các raw JTL chính thức. Tính sample count, elapsed window, throughput, HTTP RPS chỉ cho row có URL, mean, median, p90, p95, p99, max và error rate theo label. Phân biệt HTTP/network error với JMeter assertion failure. Đề xuất threshold có thể truy nguyên và không kết luận memory leak nếu thiếu chuỗi quan sát.

**Output AI ban đầu bị bác bỏ:**

> Khoảng 10-11% sample thất bại có thể là server error; nên xem xét DB index, connection pool hoặc SQLite WAL.

**Output sau khi human review tính lại raw JTL:**

| Run | Assertion failure | HTTP/network error | HTTP RPS |
| --- | ---: | ---: | ---: |
| Load | 356/3.287 | 0/3.287 | 7,1076 |
| Stress | 1.780/16.433 | 0/16.433 | 26,7113 |
| Spike | 751/7.171 | 0/7.171 | 13,2665 |
| Endurance 70 VU | 2.699/24.574 | 0/24.574 | 23,6465 |

Mọi failure canonical nằm ở assertion `POST_CHECKOUT_CART - expected empty`; không được gọi là HTTP/server error. JMeter sample throughput không đồng nhất với HTTP RPS vì hai JSR223 sampler nội bộ cũng sinh JTL row.

**Artifact hoàn chỉnh:** `agent-skill/performance-test-workflow/scripts/analyze_jtl.py` và `report/metrics-resource-rerun-20260830/*.json`.

### Tương tác 5 - Đề xuất tối ưu

**Công cụ:** Codex + human review
**Thời gian:** 2026-08-30 11:15
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Dựa trên JTL và gap implementation, đề xuất các hướng tối ưu. Phân loại từng đề xuất thành khả thi có bằng chứng, cần profiling, hoặc ảo giác. Không suy nguyên nhân từ p95/error rate nếu JTL không chứng minh.

**Output AI và quyết định của người:**

- Sửa checkout tự tính total và xóa cart: **khả thi**, có contract, implementation và assertion.
- Bổ sung pagination và cart quantity semantics: **khả thi**, có probe/issue.
- Thêm DB index: **cần profiling**, chưa có query plan hay slow-query log.
- Điều chỉnh connection pool/bật SQLite WAL: **cần profiling**, chưa có bằng chứng contention.
- Tăng Node worker để sửa fail 10-11%: **ảo giác**, vì fail là assertion nghiệp vụ.

### Tương tác 6 - Audit package

**Công cụ:** Codex + human review
**Thời gian:** 2026-08-30 13:05
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Kiểm tra package theo acceptance checklist của HW05: tên file, JMX/JTL/HTML, data, report Markdown/PDF, resource/hardware screenshot, video link, AI Audit, AI Critique, Git log, issues và Agent Skill. Chỉ ra file stale, evidence không hợp lệ và mâu thuẫn giữa report với raw log.

**Output AI đã dùng:**

- Bổ sung README summary, endpoint map, threshold và hardware table.
- Loại CSV monitor cũ dùng `thcount` không tồn tại trên macOS.
- Yêu cầu rerun resource monitor bằng CPU/RSS/thread hợp lệ.
- Bổ sung issue evidence và phân biệt artifact canonical/invalid.
- Giữ video ở trạng thái chưa hoàn tất thay vì tạo evidence giả.

### Tương tác 7 - Staircase và endurance threshold

**Công cụ:** Codex + human review
**Thời gian:** 2026-08-30 15:35
**Trạng thái prompt:** khôi phục từ nhật ký công việc.

**Prompt:**

> Đối chiếu metric canonical với JTL, loại run có login 401 hoặc duration sai. Thiết kế staircase 70/100/150/200 VU, sau đó soak 10 phút ở mức cao nhất đạt SLO. Báo HTTP RPS trong hold, p95, HTTP error, assertion, CPU, RSS và xu hướng theo cửa sổ. Chỉ gọi là maximum stable observed trong dải đã thử.

**Output AI sau khi đọc evidence thật:**

- 70/100/150/200 VU đều đạt SLO screening.
- Soak 200 VU giữ đủ 600 giây: 77,4400 HTTP RPS, p95 5 ms, HTTP error 0%, CPU tối đa 17,7%, RSS tối đa 119,3 MB.
- Ba cửa sổ 200 giây: 77,8950; 77,3650; 77,0600 HTTP RPS; cửa sổ cuối thấp hơn đầu 1,072%.
- Kết luận giới hạn: `maximum stable observed = 77,4400 HTTP RPS at 200 VU`, không tuyên bố trần tuyệt đối.

**Artifact hoàn chỉnh:** `results/staircase-20260830/`, `evidence/hardware/staircase-20260830/` và `report/metrics-staircase-20260830/`.

### Tương tác 8 - Evidence same-screen

**Công cụ:** Codex + Computer Use
**Thời gian:** 2026-08-30 18:04
**Prompt:**

> Chạy lại kịch bản trên host và chụp screenshot tĩnh cùng màn hình với terminal/JMeter và Activity Monitor. Backend PID phải khớp ở hai cửa sổ; không ghép evidence từ hai thời điểm. Không quay hoặc giả lập video của sinh viên.

**Output AI/công cụ:**

- Stress: backend PID `31159` khớp terminal và Activity Monitor.
- Spike: backend PID `35179` khớp terminal và Activity Monitor.
- Endurance: backend PID `54267` khớp; JMeter hiển thị `Active: 200`.
- Load cũ chưa có bằng chứng PID rõ tương đương và được giữ là mục cần chụp lại, không đánh dấu hoàn tất.
- Không record video; video phải do sinh viên tự quay và thuyết minh.

### Tương tác 9 - Kiểm tra listener bằng JMeter GUI

**Công cụ:** Codex + Apache JMeter GUI 5.6.3
**Thời gian:** 2026-08-30 19:16

**Prompt:**

> Kiểm tra ba listener riêng của Load/Stress/Spike và sửa phần evidence liên quan. Không dùng HTML dashboard chung để thay cho View Results Tree, Summary Report và Aggregate Report; không tạo ảnh evidence giả.

**Output AI/công cụ ban đầu:**

- JMeter báo lỗi khi mở JMX vì metadata XML đặt sai vai trò của `guiclass` và `testclass` cho `ResultCollector`.
- `UniformRandomTimer` và `JSONPostProcessor` cũng đang dùng `TestBeanGUI`, không phải GUI class tương ứng.

**Output sau khi sửa và kiểm tra lại:**

- Generator dùng `testclass="ResultCollector"` và ba `guiclass` chuẩn: `ViewResultsFullVisualizer`, `SummaryReport`, `StatVisualizer`.
- Timer dùng `UniformRandomTimerGui`; JSON extractor dùng `JSONPostProcessorGui`.
- Cả ba file Load/Stress/Spike được JMeter 5.6.3 tải thành công; log không có `ERROR` hoặc exception khi parse plan.
- Listener vẫn để `enabled="false"` cho execution non-GUI. Sinh viên cần mở JTL bằng listener tương ứng và tự chụp ba ảnh evidence trước khi nộp.

**Artifact hoàn chỉnh:** `test-plans/generate_plans.py` và ba file `test-plans/23127326_*_20260830.jmx`.

## Checklist review của người

- [x] Không bịa JTL, metric, issue hoặc output AI không còn transcript.
- [x] Prompt khôi phục được gắn nhãn rõ, không tuyên bố là nguyên văn.
- [x] Mỗi VU dùng tài khoản riêng và lifecycle CSV riêng.
- [x] Lockout probe tách khỏi positive run và có hướng dẫn reset.
- [x] Listener không được dùng làm số đo non-GUI chính thức.
- [x] Tách lỗi transport/HTTP khỏi assertion lỗi nghiệp vụ.
- [x] Metric truy nguyên được về JTL thô.
- [x] Khuyến nghị tối ưu được phân loại theo bằng chứng implementation/profiling.
- [x] Có hardware evidence và GitHub Issue evidence.
- [x] Stress/Spike/Endurance có screenshot same-screen, PID khớp.
- [ ] Chụp lại Load same-screen, hiển thị backend PID và JMeter `Active`.
- [ ] Mở mỗi JTL bằng listener tương ứng và chụp View Results Tree/Summary Report/Aggregate Report.
- [ ] Video demo tối thiểu 6 phút vẫn chờ sinh viên tự quay và thêm link.
