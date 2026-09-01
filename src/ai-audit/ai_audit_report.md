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

## 3. Tổng kết độ chính xác AI

- `[TODO]`

## 4. Kết luận

`[TODO]`

## 5. Disclosure

`[TODO]`
