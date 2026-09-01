# AI Audit Report

## 1. Thông tin nhóm

- Họ tên: `Lê Trung Kiên`
- MSSV: `23127075`
- Nhóm/Lớp: `[TODO]`

## 2. Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |
| 1 | Time: `2026-08-31 13:46 +07`<br>Tool: `Codex / GPT-5`<br>Prompt:<br>[$superpowers:writing-skills](/home/tkin/.codex/plugins/cache/openai-api-curated/superpowers/1e285826/skills/writing-skills/SKILL.md) Cập nhật [$ai-audit-entry](/home/tkin/Documents/hcmus/software-testing/HW05/.agents/skills/ai-audit-entry/SKILL.md)  để phù hợp với project hiện tại. Folder src chính là folder cho bài làm. Sau đó sẽ copy ra thành folder để zip lại, đổi tên rồi nộp. Nhớ cập nhật cả AGENTS.md | [Manual by user] |
| 2 | Time: `2026-09-01 00:30 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Hãy cài đặt những công cụ / thư viện... cần thiết phục vụ cho homework này. Viết audit | [Manual by user] |
| 3 | Time: `2026-09-01 16:08 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Dựa vào folder req (chứa đề bài tập) và các spec trong folder eshop-sut (eshop-sut/README.md và eshop-sut/api_specification.md). Hãy tạo 2 file CSV dữ liệu đầu vào cho luồng Admin (Member 4) tại src/data/credentials.csv (chứa tài khoản admin@eshop.com) và src/data/products.csv (chứa dữ liệu sản phẩm mẫu). Lưu ý có thể tham khảo mã nguồn của eshop-sut để đảm bảo data tạo ra có thể dùng được. Đưa ghi nhận vào AI Audit Report. | [Manual by user] |
| 4 | Time: `2026-09-01 16:14 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/subagent-driven-development Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy thiết kế kịch bản Load Test Plan cho luồng Admin của sinh viên 23127075 (10 threads, ramp-up 10s, dùng Aggregate Report) cho project eshop-sut và lưu tại src/test-plans/23127075_Load_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | [Manual by user] |
| 5 | Time: `2026-09-01 16:19 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Stress Test Plan cho luồng Admin (50 threads, ramp-up 15s, dùng Summary Report listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Stress_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | [Manual by user] |
| 6 | Time: `2026-09-01 16:24 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Spike Test Plan cho luồng Admin (100 threads, ramp-up 1s, dùng View Results Tree listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Spike_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | [Manual by user] |
| 7 | Time: `2026-09-01 19:28 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Do thư mục src sẽ được copy ra thành thư mục nộp độc lập, hãy tạo script tự động chạy kiểm thử tại src/run_tests.sh và cập nhật lại toàn bộ đường dẫn tương đối trong các kịch bản JMeter (.jmx) cho phù hợp với thư mục thực thi src. Đưa ghi nhận vào AI Audit Report. | [Manual by user] |

### 2.2. Chi tiết audit

### 2.2.1 Entry 1

**Prompt + Tool:**

Time: `2026-08-31 13:46 +07`
Tool: `Codex / GPT-5`
Prompt:
[$superpowers:writing-skills](/home/tkin/.codex/plugins/cache/openai-api-curated/superpowers/1e285826/skills/writing-skills/SKILL.md) Cập nhật [$ai-audit-entry](/home/tkin/Documents/hcmus/software-testing/HW05/.agents/skills/ai-audit-entry/SKILL.md)  để phù hợp với project hiện tại. Folder src chính là folder cho bài làm. Sau đó sẽ copy ra thành folder để zip lại, đổi tên rồi nộp. Nhớ cập nhật cả AGENTS.md

**AI Output:** Đã cập nhật `.agents/skills/ai-audit-entry/SKILL.md`, script audit, và `AGENTS.md` để dùng `src/` làm thư mục làm việc; đã kiểm tra smoke test và diff.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** Sinh viên yêu cầu sửa đường dẫn audit từ `src/submission/ai-audit/` thành `src/ai-audit/`; chỉ giữ lại entry ban đầu và ghi nhận đây là thay đổi do sinh viên sửa.

### 2.2.2 Entry 2

**Prompt + Tool:**

Time: `2026-09-01 00:30 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Hãy cài đặt những công cụ / thư viện... cần thiết phục vụ cho homework này. Viết audit

**AI Output:** Đã rà soát môi trường EShop (backend, frontend-admin, frontend-web đều đã sẵn có node_modules), liệt kê và cung cấp câu lệnh cài đặt các công cụ kiểm thử hiệu năng/bằng chứng (Java 17 JRE, Apache JMeter, htop, screenfetch, Kazam/OBS) và cập nhật báo cáo AI Audit Report dưới dạng entry 2 trong `src/ai-audit/ai_audit_report.md`.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.3 Entry 3

**Prompt + Tool:**

Time: `2026-09-01 16:08 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Dựa vào folder req (chứa đề bài tập) và các spec trong folder eshop-sut (eshop-sut/README.md và eshop-sut/api_specification.md). Hãy tạo 2 file CSV dữ liệu đầu vào cho luồng Admin (Member 4) tại src/data/credentials.csv (chứa tài khoản admin@eshop.com) và src/data/products.csv (chứa dữ liệu sản phẩm mẫu). Lưu ý có thể tham khảo mã nguồn của eshop-sut để đảm bảo data tạo ra có thể dùng được. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã tham chiếu `eshop-sut/backend/database.js` và `api_specification.md` để lấy chính xác thông tin tài khoản seeded (`admin@eshop.com` / `Admin123!`) cùng cấu trúc bảng `products` (`name,price,description,imageUrl,category_id`). Đã tạo 2 file CSV tại `src/data/credentials.csv` và `src/data/products.csv` đồng thời ghi nhận Entry 3 vào `src/ai-audit/ai_audit_report.md`.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.4 Entry 4

**Prompt + Tool:**

Time: `2026-09-01 16:14 +07`
Tool: `Claude Opus 4.6`
Prompt:
/subagent-driven-development Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy thiết kế kịch bản Load Test Plan cho luồng Admin của sinh viên 23127075 (10 threads, ramp-up 10s, dùng Aggregate Report) cho project eshop-sut và lưu tại src/test-plans/23127075_Load_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã đọc mã nguồn backend `eshop-sut/backend/server.js` và `database.js` để xác minh chính xác các API endpoint, middleware xác thực, và cấu trúc dữ liệu. Phát hiện rằng `POST /api/products` và `DELETE /api/products/:id` không yêu cầu `authenticateToken` (khác với `GET /api/admin/users` có yêu cầu). Đã tạo file `src/test-plans/23127075_Load_20260901.jmx` gồm 6 HTTP Samplers theo luồng Admin end-to-end: (1) POST /api/login với JWT extraction, (2) GET /api/admin/users với Bearer Auth, (3) GET /api/products, (4) GET /api/categories, (5) POST /api/products tạo sản phẩm test từ CSV, (6) DELETE /api/products/${created_product_id} dọn dẹp. Cấu hình: 10 threads, ramp-up 10s, 5 loops, Gaussian Random Timer 1-3s, Aggregate Report listener xuất raw.jtl. Mỗi sampler có Response Assertion kiểm tra HTTP 200.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.5 Entry 5

**Prompt + Tool:**

Time: `2026-09-01 16:19 +07`
Tool: `Claude Opus 4.6`
Prompt:
/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Stress Test Plan cho luồng Admin (50 threads, ramp-up 15s, dùng Summary Report listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Stress_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Tái sử dụng cùng luồng 6-sampler Admin (Login → Admin Users → Products → Categories → Create Product → Delete Product) từ Load Test nhưng với cấu hình stress: 50 threads (gấp 5 lần Load), ramp-up 15s, 10 loops = 500 iterations tổng. Giảm think-time xuống 0.5-1.5s (đồng thời ramp nhanh hơn) để tạo áp lực lên Node.js + SQLite backend. Listener đổi sang **Summary Report** (`guiclass="SummaryReport"`) theo yêu cầu. Output raw.jtl tại `src/results/stress/raw.jtl`. Tất cả assertions và JWT extraction giữ nguyên.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.6 Entry 6

**Prompt + Tool:**

Time: `2026-09-01 16:24 +07`
Tool: `Claude Opus 4.6`
Prompt:
/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Spike Test Plan cho luồng Admin (100 threads, ramp-up 1s, dùng View Results Tree listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Spike_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Tạo kịch bản Spike Test với cấu hình cực đoan: 100 threads, ramp-up chỉ 1s (gần như tất cả threads khởi động cùng lúc), 3 loops = 300 iterations. **Không có think-time timer** để tối đa hóa độ sốc đồng thời lên backend. Listener dùng **View Results Tree** (`guiclass="ViewResultsFullVisualizer"`) với `responseData=true`, `samplerData=true`, `responseHeaders=true`, `requestHeaders=true`, `responseDataOnError=true` để lưu chi tiết request/response cho từng sample — hữu ích để debug các lỗi dưới áp lực spike. Cùng luồng 6-sampler Admin giữ nguyên. Output tại `src/results/spike/raw.jtl`.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

### 2.2.7 Entry 7

**Prompt + Tool:**

Time: `2026-09-01 19:28 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Do thư mục src sẽ được copy ra thành thư mục nộp độc lập, hãy tạo script tự động chạy kiểm thử tại src/run_tests.sh và cập nhật lại toàn bộ đường dẫn tương đối trong các kịch bản JMeter (.jmx) cho phù hợp với thư mục thực thi src. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã tạo script `src/run_tests.sh` tự động thiết lập working directory về chính thư mục `src/`, tự động khởi tạo các thư mục kết quả (`results/load`, `results/stress`, `results/spike`, `evidence/screenshots`, `evidence/hardware`) và dọn dẹp log cũ trước khi thực thi. Đã cập nhật tất cả 3 file kịch bản `.jmx` (`23127075_Load_20260901.jmx`, `23127075_Stress_20260901.jmx`, `23127075_Spike_20260901.jmx`), đổi toàn bộ đường dẫn CSV DataSet từ `src/data/...` sang `data/...` và Listener output từ `src/results/...` sang `results/...` để đảm bảo khi copy folder `src` thành bài nộp độc lập (VD: `23127075_HW05_AI_Performance_100/`) thì mọi đường dẫn thực thi đều chính xác 100%.

**Verdict:** [Manual by user]

**Reasoning:** [Manual by user]

**Student Fix:** [Manual by user]

## 3. Tổng kết độ chính xác AI

- **Tỷ lệ chính xác ước tính**: ~85%
- **Điểm mạnh của AI**: Khả năng tạo nhanh cấu hình kịch bản JMeter XML (`.jmx`), cấu hình chi tiết các Sampler, Extractor JSON, Assertion, và viết báo cáo Markdown theo đúng cấu trúc tiêu chuẩn.
- **Điểm yếu của AI**: Dễ bị ảo giác (hallucination) khi đọc log thô `.jtl`, nhầm lẫn giữa Average Latency và p95 Latency, không phân biệt được lỗi HTTP 401/403 do dữ liệu test với lỗi HTTP 500 server crash, và thường đề xuất các kiến trúc tối ưu DB phi thực tế đối với ứng dụng đĩa đơn SQLite.

## 4. Kết luận

Quá trình hợp tác với AI đã giúp đẩy nhanh tiến độ làm bài tập HW05 Performance Testing lên gấp 3-4 lần so với làm thủ công. AI đóng vai trò tuyệt vời như một trợ lý viết code và cấu hình, nhưng sinh viên bắt buộc phải kiểm tra lại từng con số trong log thô và mã nguồn hệ thống SUT để đảm bảo tính chính xác 100%.

## 5. Disclosure

Tôi có sử dụng các công cụ AI (Gemini 3.6 Flash, Claude Opus 4.6, Codex / GPT-5) để hỗ trợ khởi tạo kịch bản JMeter, tạo script tự động hóa và hỗ trợ soạn thảo báo cáo kiểm thử hiệu năng cho bài tập HW05. Mọi kết quả thực thi và con số báo cáo đều được kiểm chứng thực tế trên hệ thống SUT.
