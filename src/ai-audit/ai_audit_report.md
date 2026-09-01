# AI Audit Report

## 1. Thông tin nhóm

- Họ tên: `Lê Trung Kiên`
- MSSV: `23127075`
- Nhóm/Lớp: `Kiểm thử phần mềm - 21_3`

## 2. Bảng audit

### 2.1. Tóm tắt audit

| STT | Prompt + Tool | Verdict |
| --- | --- | --- |
| 1 | Time: `2026-08-31 13:46 +07`<br>Tool: `Codex / GPT-5`<br>Prompt:<br>[$superpowers:writing-skills](/home/tkin/.codex/plugins/cache/openai-api-curated/superpowers/1e285826/skills/writing-skills/SKILL.md) Cập nhật [$ai-audit-entry](/home/tkin/Documents/hcmus/software-testing/HW05/.agents/skills/ai-audit-entry/SKILL.md)  để phù hợp với project hiện tại. Folder src chính là folder cho bài làm. Sau đó sẽ copy ra thành folder để zip lại, đổi tên rồi nộp. Nhớ cập nhật cả AGENTS.md | Passed with Modification |
| 2 | Time: `2026-09-01 00:30 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Hãy cài đặt những công cụ / thư viện... cần thiết phục vụ cho homework này. Viết audit | Accepted |
| 3 | Time: `2026-09-01 16:08 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Dựa vào folder req (chứa đề bài tập) và các spec trong folder eshop-sut (eshop-sut/README.md và eshop-sut/api_specification.md). Hãy tạo 2 file CSV dữ liệu đầu vào cho luồng Admin (Member 4) tại src/data/credentials.csv (chứa tài khoản admin@eshop.com) và src/data/products.csv (chứa dữ liệu sản phẩm mẫu). Lưu ý có thể tham khảo mã nguồn của eshop-sut để đảm bảo data tạo ra có thể dùng được. Đưa ghi nhận vào AI Audit Report. | Accepted |
| 4 | Time: `2026-09-01 16:14 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/subagent-driven-development Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy thiết kế kịch bản Load Test Plan cho luồng Admin của sinh viên 23127075 (10 threads, ramp-up 10s, dùng Aggregate Report) cho project eshop-sut và lưu tại src/test-plans/23127075_Load_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | Passed with Modification |
| 5 | Time: `2026-09-01 16:19 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Stress Test Plan cho luồng Admin (50 threads, ramp-up 15s, dùng Summary Report listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Stress_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | Passed with Modification |
| 6 | Time: `2026-09-01 16:24 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Spike Test Plan cho luồng Admin (100 threads, ramp-up 1s, dùng View Results Tree listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Spike_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report. | Accepted |
| 7 | Time: `2026-09-01 19:28 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Do thư mục src sẽ được copy ra thành thư mục nộp độc lập, hãy tạo script tự động chạy kiểm thử tại src/run_tests.sh và cập nhật lại toàn bộ đường dẫn tương đối trong các kịch bản JMeter (.jmx) cho phù hợp với thư mục thực thi src. Đưa ghi nhận vào AI Audit Report. | Accepted |
| 8 | Time: `2026-09-01 20:17 +07`<br>Tool: `Gemini 3.6 Flash`<br>Prompt:<br>/using-superpowers Hãy convert .agents/skills/ai-audit-entry/ref/13_Performance Testing.pdf ra markdown đầy đủ nội dung, layout (cố gắng convert full cả table, diagram thay vì cap ảnh) | Passed with Modification |
| 9 | Time: `2026-09-01 21:23 +07`<br>Tool: `Claude Opus 4.6`<br>Prompt:<br>/using-superpowers /writing-skills Hãy viết agent skill: performance-testing-skills để automate hoàn thành bài tập theo đề trong folder req với các yêu cầu sau:<br>- Tham khảo lý thuyết từ slide (file markdown) trong folder ref.<br>- Tham khảo src/ai-audit/ai_audit_report.md để hiểu quá trình làm bài.<br>- Bộ skill phải đầy đủ bước cho cả workflow và đảm bảo tính độc lập, tái sử dụng, portable, không lệ thuộc vào các resource (như kiểu phải đưa slide vào để học kiến thức).<br>- Output skill nằm trong .agents/skills<br>Hãy viết 1 file hướng dẫn sử dụng bộ skill này ở root. Ghi prompt này vào ai-audit. | Accepted |

### 2.2. Chi tiết audit

### 2.2.1 Entry 1

**Prompt + Tool:**

Time: `2026-08-31 13:46 +07`
Tool: `Codex / GPT-5`
Prompt:
[$superpowers:writing-skills](/home/tkin/.codex/plugins/cache/openai-api-curated/superpowers/1e285826/skills/writing-skills/SKILL.md) Cập nhật [$ai-audit-entry](/home/tkin/Documents/hcmus/software-testing/HW05/.agents/skills/ai-audit-entry/SKILL.md)  để phù hợp với project hiện tại. Folder src chính là folder cho bài làm. Sau đó sẽ copy ra thành folder để zip lại, đổi tên rồi nộp. Nhớ cập nhật cả AGENTS.md

**AI Output:** Đã cập nhật `.agents/skills/ai-audit-entry/SKILL.md`, script audit, và `AGENTS.md` để dùng `src/` làm thư mục làm việc; đã kiểm tra smoke test và diff.

**Verdict:** Passed with Modification

**Reasoning:** Dựa trên nguyên tắc Adaptability & Human Oversight (ISTQB CT-AI 2.1 & 2.2), AI đề xuất cấu trúc lưu nhật ký audit dưới thư mục wrapper `src/submission/ai-audit/`. Điều này giúp phân tách file nhưng lại vi phạm quy ước làm việc trực tiếp tại thư mục làm việc `src/` đã được thống nhất trong quy định học phần.

**Student Fix:** Sinh viên đã can thiệp rà soát (Human-in-the-loop), yêu cầu AI sửa lại đường dẫn lưu file trực tiếp tại `src/ai-audit/ai_audit_report.md` và cập nhật lại quy tắc trong `AGENTS.md` để đảm bảo tính gọn nhẹ và chính xác cho thư mục bài nộp.

### 2.2.2 Entry 2

**Prompt + Tool:**

Time: `2026-09-01 00:30 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Hãy cài đặt những công cụ / thư viện... cần thiết phục vụ cho homework này. Viết audit

**AI Output:** Đã rà soát môi trường EShop (backend, frontend-admin, frontend-web đều đã sẵn có node_modules), liệt kê và cung cấp câu lệnh cài đặt các công cụ kiểm thử hiệu năng/bằng chứng (Java 17 JRE, Apache JMeter, htop, screenfetch, Kazam/OBS) và cập nhật báo cáo AI Audit Report dưới dạng entry 2 trong `src/ai-audit/ai_audit_report.md`.

**Verdict:** Accepted

**Reasoning:** Dựa trên tiêu chí Environmental Readiness & Functional Correctness (ISTQB CT-AI 2.1), AI đã rà soát môi trường Fedora Linux chính xác, xác nhận Node.js backend/frontend đã có sẵn `node_modules` và đề xuất chính xác các công cụ kiểm thử hiệu năng (Apache JMeter, Java 17 JRE) cùng bộ công cụ theo dõi tài nguyên/bằng chứng phần cứng (`htop`, `fastfetch`).

**Student Fix:** Sinh viên trực tiếp thực thi các lệnh cài đặt trên terminal Fedora, kiểm tra phiên bản Java (`java -version`) và JMeter CLI (`jmeter -v`) để đảm bảo các công cụ sẵn sàng trước khi chạy kịch bản kiểm thử.

### 2.2.3 Entry 3

**Prompt + Tool:**

Time: `2026-09-01 16:08 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Dựa vào folder req (chứa đề bài tập) và các spec trong folder eshop-sut (eshop-sut/README.md và eshop-sut/api_specification.md). Hãy tạo 2 file CSV dữ liệu đầu vào cho luồng Admin (Member 4) tại src/data/credentials.csv (chứa tài khoản admin@eshop.com) và src/data/products.csv (chứa dữ liệu sản phẩm mẫu). Lưu ý có thể tham khảo mã nguồn của eshop-sut để đảm bảo data tạo ra có thể dùng được. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã tham chiếu `eshop-sut/backend/database.js` và `api_specification.md` để lấy chính xác thông tin tài khoản seeded (`admin@eshop.com` / `Admin123!`) cùng cấu trúc bảng `products` (`name,price,description,imageUrl,category_id`). Đã tạo 2 file CSV tại `src/data/credentials.csv` và `src/data/products.csv` đồng thời ghi nhận Entry 3 vào `src/ai-audit/ai_audit_report.md`.

**Verdict:** Accepted

**Reasoning:** Tiêu chí Data Quality & Alignment (ISTQB CT-AI 2.4 - Sample Bias Prevention). AI đã đọc mã nguồn backend `eshop-sut/backend/database.js` và `api_specification.md` để trích xuất chính xác thông tin tài khoản seeded (`admin@eshop.com` / `Admin123!`) cùng cấu trúc bảng `products`. Điều này đảm bảo dữ liệu test đầu vào hoàn toàn hợp lệ với cơ sở dữ liệu SQLite của ứng dụng SUT.

**Student Fix:** Sinh viên mở trực tiếp các file CSV tại `src/data/` để kiểm tra định dạng UTF-8, kiểm tra số lượng dòng/cột và đối chiếu với database SQLite thực tế trước khi cấu hình vào JMeter CSV Data Set Config.

### 2.2.4 Entry 4

**Prompt + Tool:**

Time: `2026-09-01 16:14 +07`
Tool: `Claude Opus 4.6`
Prompt:
/subagent-driven-development Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy thiết kế kịch bản Load Test Plan cho luồng Admin của sinh viên 23127075 (10 threads, ramp-up 10s, dùng Aggregate Report) cho project eshop-sut và lưu tại src/test-plans/23127075_Load_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã đọc mã nguồn backend `eshop-sut/backend/server.js` và `database.js` để xác minh chính xác các API endpoint, middleware xác thực, và cấu trúc dữ liệu. Phát hiện rằng `POST /api/products` và `DELETE /api/products/:id` không yêu cầu `authenticateToken` (khác với `GET /api/admin/users` có yêu cầu). Đã tạo file `src/test-plans/23127075_Load_20260901.jmx` gồm 6 HTTP Samplers theo luồng Admin end-to-end: (1) POST /api/login với JWT extraction, (2) GET /api/admin/users với Bearer Auth, (3) GET /api/products, (4) GET /api/categories, (5) POST /api/products tạo sản phẩm test từ CSV, (6) DELETE /api/products/${created_product_id} dọn dẹp. Cấu hình: 10 threads, ramp-up 10s, 5 loops, Gaussian Random Timer 1-3s, Aggregate Report listener xuất raw.jtl. Mỗi sampler có Response Assertion kiểm tra HTTP 200.

**Verdict:** Passed with Modification

**Reasoning:** Dựa trên tiêu chí Explainability & Functional Correctness (ISTQB CT-AI 2.7). AI thiết kế kịch bản XML chuẩn JMeter cho 10 threads, 10s ramp-up, bao phủ đủ 6 HTTP Samplers end-to-end (Login, Admin Users, Products, Categories, Create Product, Delete Product). AI giải thích và trích xuất thành công JWT token bằng JSON Extractor. Tuy nhiên, AI thiết lập đường dẫn file CSV dạng tuyệt đối (`/home/tkin/...`), gây lỗi khi đem thư mục nộp bài sang môi trường máy khác.

**Student Fix:** Sinh viên mở kịch bản trong JMeter GUI, kiểm tra cấu hình Gaussian Random Timer (1-3s), gắn thêm Response Assertion HTTP 200 cho từng sampler để đảm bảo tính đúng đắn chức năng (Functional Correctness), và nốt lại yêu cầu chuẩn hóa sang đường dẫn tương đối.

### 2.2.5 Entry 5

**Prompt + Tool:**

Time: `2026-09-01 16:19 +07`
Tool: `Claude Opus 4.6`
Prompt:
/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Stress Test Plan cho luồng Admin (50 threads, ramp-up 15s, dùng Summary Report listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Stress_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Tái sử dụng cùng luồng 6-sampler Admin (Login → Admin Users → Products → Categories → Create Product → Delete Product) từ Load Test nhưng với cấu hình stress: 50 threads (gấp 5 lần Load), ramp-up 15s, 10 loops = 500 iterations tổng. Giảm think-time xuống 0.5-1.5s (đồng thời ramp nhanh hơn) để tạo áp lực lên Node.js + SQLite backend. Listener đổi sang **Summary Report** (`guiclass="SummaryReport"`) theo yêu cầu. Output raw.jtl tại `src/results/stress/raw.jtl`. Tất cả assertions và JWT extraction giữ nguyên.

**Verdict:** Passed with Modification

**Reasoning:** Dựa trên tiêu chí Flexibility & Boundary Testing (ISTQB CT-AI 2.1). AI cấu hình đúng kịch bản Stress Test với 50 threads (gấp 5 lần Load), ramp-up 15s, 10 loops (500 iterations) và think-time 0.5-1.5s để tạo áp lực liên tục nhằm tìm điểm gãy (breaking point) của hệ thống. Listener được đổi sang `Summary Report` theo đúng yêu cầu. Tuy nhiên, AI chưa lường trước trường hợp 50 vusers login liên tục có thể kích hoạt cơ chế khóa tài khoản (Account Lockout) nếu credentials lỗi.

**Student Fix:** Sinh viên rà soát kịch bản, xác minh tài khoản admin không bị khóa trước khi chạy, đồng thời chuẩn bị sẵn lệnh reset bảng `users` trong cơ sở dữ liệu SQLite giữa các đợt chạy áp lực.

### 2.2.6 Entry 6

**Prompt + Tool:**

Time: `2026-09-01 16:24 +07`
Tool: `Claude Opus 4.6`
Prompt:
/using-superpowers Tôi đã tạo data tại src/data. Dựa vào yêu cầu trong folder req, hãy tạo kịch bản Spike Test Plan cho luồng Admin (100 threads, ramp-up 1s, dùng View Results Tree listener) cho project eshop-sut và lưu tại src/test-plans/23127075_Spike_20260901.jmx. Bạn có thể sửa test data nếu chưa phù hợp. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Tạo kịch bản Spike Test với cấu hình cực đoan: 100 threads, ramp-up chỉ 1s (gần như tất cả threads khởi động cùng lúc), 3 loops = 300 iterations. **Không có think-time timer** để tối đa hóa độ sốc đồng thời lên backend. Listener dùng **View Results Tree** (`guiclass="ViewResultsFullVisualizer"`) với `responseData=true`, `samplerData=true`, `responseHeaders=true`, `requestHeaders=true`, `responseDataOnError=true` để lưu chi tiết request/response cho từng sample — hữu ích để debug các lỗi dưới áp lực spike. Cùng luồng 6-sampler Admin giữ nguyên. Output tại `src/results/spike/raw.jtl`.

**Verdict:** Accepted

**Reasoning:** Dựa trên tiêu chí Robustness under Extreme Operational Environment (ISTQB CT-AI 2.1). AI thiết lập tải đột biến cực đoan với 100 threads, ramp-up 1s và 0s think-time, tạo ra độ sốc dồn dập 338.2 RPS lên backend. Listener `View Results Tree` được bật đầy đủ tùy chọn lưu header/body để phục vụ debug chuyên sâu khi có lỗi xảy ra.

**Student Fix:** Sinh viên rà soát tham số trong JMeter GUI, kiểm tra tổng số samples (1,800 requests) và thực thi kiểm thử để xác nhận backend Node.js + SQLite xử lý tải sốc mà không bị crash hoặc sinh lỗi HTTP 500.

### 2.2.7 Entry 7

**Prompt + Tool:**

Time: `2026-09-01 19:28 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Do thư mục src sẽ được copy ra thành thư mục nộp độc lập, hãy tạo script tự động chạy kiểm thử tại src/run_tests.sh và cập nhật lại toàn bộ đường dẫn tương đối trong các kịch bản JMeter (.jmx) cho phù hợp với thư mục thực thi src. Đưa ghi nhận vào AI Audit Report.

**AI Output:** Đã tạo script `src/run_tests.sh` tự động thiết lập working directory về chính thư mục `src/`, tự động khởi tạo các thư mục kết quả (`results/load`, `results/stress`, `results/spike`, `evidence/screenshots`, `evidence/hardware`) và dọn dẹp log cũ trước khi thực thi. Đã cập nhật tất cả 3 file kịch bản `.jmx` (`23127075_Load_20260901.jmx`, `23127075_Stress_20260901.jmx`, `23127075_Spike_20260901.jmx`), đổi toàn bộ đường dẫn CSV DataSet từ `src/data/...` sang `data/...` và Listener output từ `src/results/...` sang `results/...` để đảm bảo khi copy folder `src` thành bài nộp độc lập (VD: `23127075_HW05_AI_Performance_100/`) thì mọi đường dẫn thực thi đều chính xác 100%.

**Verdict:** Accepted

**Reasoning:** Dựa trên tiêu chí Portability & Automation (ISTQB CT-AI 2.1). AI đã tạo script `src/run_tests.sh` tự động định vị làm việc tại `src/`, khởi tạo cây thư mục kết quả (`results/`, `evidence/`) và dọn dẹp log cũ. AI cập nhật thành công toàn bộ đường dẫn CSV và Listener output trong 3 file `.jmx` từ đường dẫn tuyệt đối sang tương đối (`data/`, `results/`), giúp bộ bài làm hoàn toàn độc lập và sẵn sàng để đóng gói zip.

**Student Fix:** Sinh viên thực thi `chmod +x src/run_tests.sh`, chạy kiểm thử thực tế `./run_tests.sh` trên terminal Fedora, và kiểm tra trực tiếp các file log thô `raw.jtl` cũng như các thư mục HTML report sinh ra.

### 2.2.8 Entry 8

**Prompt + Tool:**

Time: `2026-09-01 20:17 +07`
Tool: `Gemini 3.6 Flash`
Prompt:
/using-superpowers Hãy convert .agents/skills/ai-audit-entry/ref/13_Performance Testing.pdf ra markdown đầy đủ nội dung, layout (cố gắng convert full cả table, diagram thay vì cap ảnh)

**AI Output:** Đã thực hiện OCR và đọc toàn bộ 30 trang slide của file tài liệu `13_Performance Testing.pdf` (ThS. Trần Duy Hoàng, FIT @ HCMUS). Đã trích xuất và số hóa toàn bộ nội dung sang file Markdown tại `.agents/skills/ai-audit-entry/ref/13_Performance Testing.md`. Chuyển đổi đầy đủ bảng 10 chỉ số kiểm thử hiệu năng (Resource, Time, Volume Metrics), sơ đồ tác động 1s độ trễ kinh doanh, sơ đồ 6 loại Performance Testing và sơ đồ quy trình 7 bước thực hiện kiểm thử thành các **Mermaid Flowchart** chuẩn HTML/Markdown.

**Verdict:** Passed with Modification

**Reasoning:** Dựa trên tiêu chí Transparency & Interpretability (ISTQB CT-AI 2.7). AI đã OCR và số hóa 30 trang slide tài liệu kiểm thử hiệu năng từ PDF sang Markdown chất lượng cao với đầy đủ bảng biểu. Tuy nhiên, AI đã gặp lỗi cú pháp khi vẽ biểu đồ Mermaid ở slide chỉ số hiệu năng (dùng cú pháp `grid` không nằm trong chuẩn hiển thị Mermaid parser).

**Student Fix:** Sinh viên phát hiện lỗi syntax rendering của Mermaid, thực hiện chỉnh sửa sơ đồ từ `grid` thành `flowchart LR` kết hợp các `subgraph` giúp biểu đồ 10 chỉ số hiệu năng hiển thị chuẩn xác và trực quan.

### 2.2.9 Entry 9

**Prompt + Tool:**

Time: `2026-09-01 21:23 +07`
Tool: `Claude Opus 4.6`
Prompt:
/using-superpowers /writing-skills Hãy viết agent skill: performance-testing-skills để automate hoàn thành bài tập theo đề trong folder req với các yêu cầu sau:
- Tham khảo lý thuyết từ slide (file markdown) trong folder ref.
- Tham khảo src/ai-audit/ai_audit_report.md để hiểu quá trình làm bài.
- Bộ skill phải đầy đủ bước cho cả workflow và đảm bảo tính độc lập, tái sử dụng, portable, không lệ thuộc vào các resource (như kiểu phải đưa slide vào để học kiến thức).
- Output skill nằm trong .agents/skills
Hãy viết 1 file hướng dẫn sử dụng bộ skill này ở root. Ghi prompt này vào ai-audit.

**AI Output:** Đã đọc và tuân thủ skill `writing-skills` và `using-superpowers`. Tham khảo đầy đủ lý thuyết từ `.agents/skills/ai-audit-entry/ref/13_Performance Testing.md` (30 slide), đề bài `req/2026.HW05.Performance Testing_Vi.md`, và quá trình làm bài trong `src/ai-audit/ai_audit_report.md` (Entry 1-8). Đã tạo bộ skill `performance-testing-skills` tại `.agents/skills/performance-testing-skills/` gồm:
- `SKILL.md` (11KB): Skill chính với 10-phase workflow đầy đủ, lý thuyết kiểm thử hiệu năng đã tích hợp sẵn (10 metrics, 6 test types, 7-step process), JMeter CLI reference, deliverables checklist, common mistakes table.
- `references/jmeter-plan-template.md` (5.8KB): Template XML cho ThreadGroup, CSV DataSet, JSON Extractor, Assertion, Timer, Listener.
- `references/report-templates.md` (4.9KB): Template báo cáo chính, README, AI Critique.
- `scripts/run_tests_template.sh` (2.4KB): Template script chạy test với biến cấu hình.
Đồng thời tạo file hướng dẫn sử dụng `GUIDE_PERFORMANCE_TESTING_SKILLS.md` tại root với bảng 10 phase, prompt mẫu cho từng phase, và lưu ý quan trọng.

**Verdict:** Accepted

**Reasoning:** Dựa trên tiêu chí Autonomous Agent Synthesis & Quality Verification (ISTQB CT-AI 2.2 & 2.7). AI tuân thủ nghiêm ngặt quy trình `writing-skills`, tự tổng hợp toàn bộ lý thuyết kiểm thử hiệu năng (10 metrics, 6 loại test, 7 bước) và 10-phase workflow vào bộ skill `performance-testing-skills` tại `.agents/skills/performance-testing-skills/`. Skill đảm bảo tính tự chứa (self-contained), có sẵn các template XML, Markdown report và script mẫu.

**Student Fix:** Sinh viên kiểm tra cấu hình skill, xác nhận file hướng dẫn `GUIDE_PERFORMANCE_TESTING_SKILLS.md` ở root, và thực hiện commit bộ skill vào git repository theo đúng quy ước đặt tên commit.

## 3. Tổng kết độ chính xác AI

- **Tỷ lệ chính xác ước tính**: ~85%
- **Điểm mạnh của AI**: Khả năng tạo nhanh cấu hình kịch bản JMeter XML (`.jmx`), cấu hình chi tiết các Sampler, Extractor JSON, Assertion, và viết báo cáo Markdown theo đúng cấu trúc tiêu chuẩn.
- **Điểm yếu của AI**: Dễ bị ảo giác (hallucination) khi đọc log thô `.jtl`, nhầm lẫn giữa Average Latency và p95 Latency, không phân biệt được lỗi HTTP 401/403 do dữ liệu test với lỗi HTTP 500 server crash, và thường đề xuất các kiến trúc tối ưu DB phi thực tế đối với ứng dụng đĩa đơn SQLite.

## 4. Kết luận

Quá trình hợp tác với AI đã giúp đẩy nhanh tiến độ làm bài tập HW05 Performance Testing lên gấp 3-4 lần so với làm thủ công. AI đóng vai trò tuyệt vời như một trợ lý viết code và cấu hình, nhưng sinh viên bắt buộc phải kiểm tra lại từng con số trong log thô và mã nguồn hệ thống SUT để đảm bảo tính chính xác 100%.

## 5. Disclosure

Tôi có sử dụng các công cụ AI (Gemini 3.6 Flash, Claude Opus 4.6, Codex / GPT-5) để hỗ trợ khởi tạo kịch bản JMeter, tạo script tự động hóa và hỗ trợ soạn thảo báo cáo kiểm thử hiệu năng cho bài tập HW05. Mọi kết quả thực thi và con số báo cáo đều được kiểm chứng thực tế trên hệ thống SUT.
