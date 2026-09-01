# HW05 AI Performance Testing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thành bài HW05 bằng một workflow admin duy nhất, ba kịch bản JMeter, bằng chứng chạy thật, phân tích AI có kiểm chứng, đề xuất continuous performance testing và gói nộp được tạo từ `src/`.

**Architecture:** Mọi deliverable nằm trực tiếp dưới `src/`, được tổ chức theo workflow, scenario và evidence; không tạo `src/submission/`. Ba test plan dùng cùng một workflow end-to-end nhưng cấu hình tải khác nhau, còn báo cáo Markdown liên kết tới raw logs, HTML reports, screenshots và video. AI hỗ trợ thiết kế, sinh khung, phân tích và review; sinh viên xác minh endpoint, chạy thử, sửa plan và ghi nhận giá trị thực tế.

**Tech Stack:** Apache JMeter, JMeter HTML dashboard, CSV Data Set Config, htop/Task Manager/Activity Monitor, Markdown/PDF, Git, công cụ AI đã khai báo trong `src/ai-audit/ai_audit_report.md`.

**Spec:** `req/2026.HW05.Performance Testing_Vi.md`, `req/2026.HW05.Performance Testing_En.md`, `docs/team-task-division.vi.md`

## Global Constraints

- SUT là EShop; workflow cá nhân là admin login → dashboard/danh sách sản phẩm → CRUD sản phẩm/danh mục hoặc import CSV.
- Mỗi test plan phải bao phủ auth-heavy, read-heavy và transactional trong cùng workflow end-to-end.
- Tên plan phải theo `{StudentID}_{ScenarioType}_{YYYYMMDD}`; StudentID là `23127075`, ngày chạy dùng ngày thực tế.
- Dữ liệu test phải dùng CSV và chỉ dùng tài khoản/bản ghi test-only; không commit secrets.
- Load, Stress và Spike phải dùng ba listener/report khác nhau.
- Raw `.jtl`, HTML reports, screenshots, hardware evidence, báo cáo và audit phải nằm trực tiếp hoặc trong thư mục con hợp lý của `src/`.
- Endurance phải chạy khoảng 10–15 phút và báo cáo RPS ổn định, p95, error rate, CPU và memory bằng số đo thật.
- Không bịa raw logs, screenshot, video, hostname, GitHub Issue hoặc số liệu hiệu năng.
- Ghi một Git commit cho mỗi bước deliverable chính; không commit thay đổi nếu chưa được yêu cầu.

---

### Task 1: Xác nhận SUT và workflow admin

**Files:**
- Create: `src/docs/workflow-endpoint-map.md`
- Create: `src/docs/test-environment.md`

**Interfaces:**
- Consumes: endpoint và port thực tế từ repository EShop, phân công trong `docs/team-task-division.vi.md`.
- Produces: bảng method/path/request/response/assertion và quy trình reset/cleanup để các test plan dùng thống nhất.

- [ ] **Step 1:** Checkout/chạy EShop theo README của SUT, ghi base URL, port, seed command, tài khoản admin test-only và cách reset dữ liệu vào `src/docs/test-environment.md`.
- [ ] **Step 2:** Dùng browser/API inspection để xác định endpoint admin login, dashboard/list, và transactional mutation (ưu tiên CRUD sản phẩm hoặc import CSV); ghi method, path, headers, body, biến động dữ liệu và response mẫu vào `src/docs/workflow-endpoint-map.md`.
- [ ] **Step 3:** Đánh dấu rõ auth-heavy, read-heavy và transactional; thêm assertion dự kiến cho status code, response field và quyền admin.
- [ ] **Step 4:** Chạy từng request thủ công một lần, lưu các giá trị ID cần thiết vào dữ liệu test-only và xác nhận cleanup không phá dữ liệu thật.
- [ ] **Step 5:** Commit bằng `git add src/docs && git commit -m "docs: document selected performance workflow"`.

### Task 2: Chuẩn bị CSV và khung báo cáo

**Files:**
- Create: `src/data/admin_credentials.csv`
- Create: `src/data/admin_workflow.csv`
- Create: `src/docs/ai-human-review.md`
- Create: `src/README.md`

**Interfaces:**
- Consumes: contract trong `src/docs/workflow-endpoint-map.md`.
- Produces: CSV headers ổn định (`username,password,product_id,category_id,product_name,price`) và checklist evidence/report để test plans và báo cáo tham chiếu.

- [ ] **Step 1:** Tạo CSV chỉ với dữ liệu test-only; không ghi mật khẩu thật vào Git nếu repository có thể công khai, thay bằng biến môi trường và mô tả cách inject.
- [ ] **Step 2:** Viết `src/README.md` với workflow, quy ước tên file, lệnh JMeter, bảng output bắt buộc và mục sẽ điền bằng kết quả chạy thật.
- [ ] **Step 3:** Tạo `src/docs/ai-human-review.md` gồm các cột: AI suggestion, evidence, student decision, reason; để ghi các lỗi về ramp-up, threads, think-time, assertion, lockout và dữ liệu.
- [ ] **Step 4:** Commit bằng `git add src/data src/docs/ai-human-review.md src/README.md && git commit -m "test: add data-driven inputs"`.

### Task 3: Sinh và sửa ba JMeter plans

**Files:**
- Create: `src/jmeter/23127075_Load_20260831.jmx`
- Create: `src/jmeter/23127075_Stress_20260831.jmx`
- Create: `src/jmeter/23127075_Spike_20260831.jmx`

**Interfaces:**
- Consumes: endpoint map và CSV từ Task 1–2.
- Produces: ba plan cùng workflow, khác tải và listener/report: Load dùng Summary Report, Stress dùng Aggregate Report, Spike dùng View Results Tree (hoặc listener tương đương không lặp).

- [ ] **Step 1:** Prompt AI theo từng lượt để thiết kế workflow, map endpoint, chọn tham số và sinh từng plan; lưu prompt/output vào audit report theo skill hiện hành.
- [ ] **Step 2:** Mở mỗi `.jmx`, cấu hình CSV Data Set Config, HTTP defaults, cookie/cache/session handling, admin login, dashboard/list read, mutation transaction, assertions và cleanup.
- [ ] **Step 3:** Đặt tham số Load ở mức baseline hợp lý; Stress tăng dần đến khi đạt lỗi/ngưỡng; Spike chuyển nhanh từ tải thấp sang cao rồi về thấp. Ghi lý do tham số trong `src/docs/ai-human-review.md`.
- [ ] **Step 4:** Kiểm tra bằng một thread/ít request và sửa mọi lỗi functional trước khi chạy tải lớn.
- [ ] **Step 5:** Commit từng plan bằng `test: add load performance plan`, `test: add stress performance plan`, và `test: add spike performance plan`.

### Task 4: Chạy Load, Stress, Spike và thu bằng chứng

**Files:**
- Create: `src/results/load/23127075_Load_20260831.jtl` và HTML report
- Create: `src/results/stress/23127075_Stress_20260831.jtl` và HTML report
- Create: `src/results/spike/23127075_Spike_20260831.jtl` và HTML report
- Create: `src/evidence/` screenshots và hardware report
- Modify: `src/docs/test-environment.md`

**Interfaces:**
- Consumes: ba plans đã smoke-test.
- Produces: raw logs, HTML reports, screenshot JMeter cùng resource monitor, hardware specs và quy trình reset lockout.

- [ ] **Step 1:** Chụp hardware evidence có hostname, CPU, RAM, OS; ghi bảng thông số và thời điểm chạy.
- [ ] **Step 2:** Chạy từng plan non-GUI bằng `jmeter -n -t <plan> -l <jtl> -e -o <html-dir>` trong khi resource monitor hiển thị cùng phiên bằng chứng.
- [ ] **Step 3:** Nếu Stress/Spike kích hoạt lockout, reset đúng tài khoản, ghi từng bước và xác nhận login lại trước lần chạy tiếp theo.
- [ ] **Step 4:** Kiểm tra log không bị rỗng, HTML report mở được, screenshot có đủ context; ghi số request, error, throughput, p95 và CPU/RAM vào `src/README.md`.
- [ ] **Step 5:** Commit artifacts bằng các commit scenario tương ứng.

### Task 5: Endurance threshold và AI analysis

**Files:**
- Create: `src/results/endurance/` raw log/report/evidence
- Create: `src/docs/ai-analysis-review.md`

**Interfaces:**
- Consumes: raw `.jtl` của ba scenario và resource evidence.
- Produces: threshold có số liệu thật, AI analysis, bảng đối chiếu metric và phân loại recommendation feasible/hallucinated.

- [ ] **Step 1:** Chạy sustained load 10–15 phút ở mức ổn định, lưu raw log và resource measurements.
- [ ] **Step 2:** Tính từ raw log maximum stable RPS, p95, error rate, CPU peak/average và memory ceiling; ghi công thức và dòng/nguồn dữ liệu.
- [ ] **Step 3:** Prompt AI phân tích `.jtl` và đề xuất thresholds/optimizations; lưu output vào audit report.
- [ ] **Step 4:** Đối chiếu từng kết luận AI với raw log, sửa metric sai, giải thích nguyên nhân và đánh dấu recommendation khả thi hay hallucinated trong `src/docs/ai-analysis-review.md`.
- [ ] **Step 5:** Viết AI Critique 200–300 từ, rồi commit bằng `git commit -m "docs: add AI analysis review"`.

### Task 6: Continuous Performance Testing proposal

**Files:**
- Create: `src/docs/continuous-performance-testing.md`

**Interfaces:**
- Consumes: test plans, baseline metrics và threshold từ Task 4–5.
- Produces: flow chart commit detection → test selection → execution → baseline comparison → p95 regression flag, cùng trade-offs.

- [ ] **Step 1:** Vẽ flow chart bằng Mermaid trong Markdown và mô tả trigger theo commit, smoke gate, scheduled full test, artifact retention và failure notification.
- [ ] **Step 2:** Định nghĩa p95 regression rule bằng baseline + tolerance, đồng thời nêu chi phí, thời gian, false positives, môi trường nhiễu và maintenance.
- [ ] **Step 3:** Commit bằng `git commit -m "docs: add continuous performance testing proposal"`.

### Task 7: Agent Skill, PDF, commit log và đóng gói

**Files:**
- Modify/Create: `src/.agents/skills/<skill-name>/SKILL.md` nếu cần nộp skill tái sử dụng
- Create: `src/docs/git-commit-log.txt`
- Create: `src/docs/main-report.md`, `src/docs/ai-critique.md`, các PDF tương ứng
- Modify: `src/README.md`
- Create outside source of truth: staging copy và `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`

**Interfaces:**
- Consumes: mọi artifact và số liệu đã xác minh từ Task 1–6.
- Produces: `src/` hoàn chỉnh và ZIP từ bản copy đổi tên, không thay đổi `src/`.

- [ ] **Step 1:** Nếu xây skill, mô tả input endpoint/CSV, trình tự tạo plan/chạy/phân tích/audit và giới hạn không được bịa evidence; quay video demo tối thiểu 6 phút với công cụ và resource monitor cùng khung hình, giọng Việt của sinh viên.
- [ ] **Step 2:** Viết main report gồm workflow map, setup, ba scenario, evidence, endurance, AI review, bug/issues, continuous proposal và links; xuất Markdown + PDF.
- [ ] **Step 3:** Xuất AI Audit Report Markdown + PDF, bảo đảm có toàn bộ prompt/output, disclosure và AI critique; cập nhật audit cho các phiên được user cho phép.
- [ ] **Step 4:** Tạo commit log bằng `git log --oneline --all > src/docs/git-commit-log.txt`; kiểm tra không có secrets, `__pycache__`, `.jtl` ngoài ý muốn hoặc file thừa.
- [ ] **Step 5:** Hoàn thiện self-assessment và test summary trong `src/README.md`, chọn điểm tự đánh giá `[000,100]` dựa trên evidence thực tế.
- [ ] **Step 6:** Copy nguyên `src/` sang staging, đổi tên folder theo quy ước, inspect ZIP contents, rồi tạo `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`; giữ nguyên `src/` làm source of truth.

## Mức độ có thể tự động hóa

Có thể tự động hóa gần như toàn bộ phần lặp lại và kiểm tra tính nhất quán:

- Sinh khung `.jmx`, CSV, thư mục results/evidence, lệnh chạy ba scenario và HTML dashboard.
- Chạy JMeter headless, parse `.jtl`, tính throughput/p95/error rate và tạo bảng/biểu đồ báo cáo.
- Thu thập CPU/RAM định kỳ, kiểm tra naming/path, phát hiện thiếu artifact, secrets và file thừa.
- Gọi AI theo từng bước để sinh plan hoặc phân tích log, lưu prompt/output vào audit report.
- Tạo commit log, export Markdown/PDF nếu công cụ có sẵn, copy staging và tạo ZIP.

Không thể tự động hóa đáng tin cậy nếu không có quyền truy cập SUT và thiết bị của sinh viên:

- Xác nhận endpoint/port/seed thực tế, tài khoản admin và reset lockout.
- Tạo dữ liệu hiệu năng thật, quyết định human review, xác minh recommendation của AI và viết critique chịu trách nhiệm cá nhân.
- Chụp hardware/resource screenshots, quay video có giọng sinh viên, tạo GitHub Issues và cung cấp link YouTube.
- Bịa hoặc thay thế raw logs, hostname, screenshot, video hay kết quả benchmark là không được phép theo đề.

## Self-review against the specification

- Task 1: Tasks 1–4 cover AI-assisted plans, CSV, three reports, review, execution, evidence and lockout reset.
- Task 2: Task 5 covers raw-log analysis, thresholds, metric correction and feasible/hallucinated recommendations.
- Task 3: Task 6 covers flow chart, p95 regression and trade-offs.
- Agent Skill, AI Audit, 200–300 word critique, commit log and packaging: Task 7 covers all explicitly.
- No placeholder instructions such as “TBD” or invented runtime values are used; values requiring execution are explicitly sourced from real evidence.
