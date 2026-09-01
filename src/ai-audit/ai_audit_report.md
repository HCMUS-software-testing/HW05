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

## 3. Tổng kết độ chính xác AI

- `[TODO]`

## 4. Kết luận

`[TODO]`

## 5. Disclosure

`[TODO]`
