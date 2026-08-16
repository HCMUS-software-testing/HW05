# HW05 Performance Testing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thành HW05 bằng cách thiết kế, chạy, phân tích và nộp bộ kiểm thử hiệu năng Load/Stress/Spike cho EShop SUT, kèm bằng chứng thực thi thật, báo cáo AI Audit, AI Critique, video demo và gói nộp Moodle.

**Architecture:** Dùng JMeter làm công cụ chính vì đề bài mặc định theo JMeter và yêu cầu `.jtl`, listener/report rõ ràng. Workflow end-to-end thống nhất cho cả ba kịch bản: đăng nhập, đọc/tìm kiếm sản phẩm, xem chi tiết, thêm giỏ hàng, checkout/tạo đơn hàng; dữ liệu request được cấp qua CSV. Mọi kết quả sinh bởi AI phải có bước rà soát của người làm và đối chiếu với log thô.

**Tech Stack:** EShop SUT từ `https://github.com/ttbhanh/eshop-sut`, JMeter, CSV test data, htop hoặc Task Manager hoặc Activity Monitor, screenfetch hoặc dxdiag, Git/GitHub Issues, Markdown/PDF, YouTube unlisted.

---

## Cấu trúc file nên tạo trong bài làm

- `README.md`: bảng tự đánh giá, tóm tắt test summary, endpoint groups, endurance threshold, số bug/performance issues, link video.
- `report/main_report.md`: báo cáo chính bằng Markdown.
- `report/main_report.pdf`: bản PDF xuất từ báo cáo chính.
- `report/ai_audit_report.md`: nhật ký AI đầy đủ.
- `report/ai_audit_report.pdf`: bản PDF của AI Audit Report.
- `report/ai_critique.md`: đoạn critique 200-300 từ.
- `report/git_commit_log.txt`: log commit Git.
- `jmeter/plans/{StudentID}_Load_{YYYYMMDD}.jmx`: test plan Load.
- `jmeter/plans/{StudentID}_Stress_{YYYYMMDD}.jmx`: test plan Stress.
- `jmeter/plans/{StudentID}_Spike_{YYYYMMDD}.jmx`: test plan Spike.
- `jmeter/data/users.csv`: tài khoản đăng nhập hợp lệ dùng cho workflow.
- `jmeter/data/products.csv`: product IDs/search terms dùng cho read-heavy step.
- `jmeter/data/orders.csv`: dữ liệu checkout/order payload nếu endpoint cần.
- `jmeter/results/load/{StudentID}_Load_{YYYYMMDD}.jtl`: log thô Load.
- `jmeter/results/stress/{StudentID}_Stress_{YYYYMMDD}.jtl`: log thô Stress.
- `jmeter/results/spike/{StudentID}_Spike_{YYYYMMDD}.jtl`: log thô Spike.
- `jmeter/reports/load/`: HTML report Load.
- `jmeter/reports/stress/`: HTML report Stress.
- `jmeter/reports/spike/`: HTML report Spike.
- `evidence/screenshots/`: ảnh JMeter + resource monitor cho từng run, ảnh hardware report, ảnh bug/performance issue.
- `evidence/videos/video_links.md`: link YouTube unlisted và mô tả clip.
- `issues/bug_reports.md`: danh sách GitHub Issues đã tạo nếu có.
- `agent-skill/`: thư mục Agent Skill nếu làm phần 10 điểm này.

## Quy ước cần chốt trước khi chạy

- Thay `{StudentID}` bằng MSSV thật của bạn trong tất cả tên file nộp.
- Thay `{YYYYMMDD}` bằng ngày chạy test thực tế, ví dụ ngày 16/08/2026 viết là `20260816`.
- Nếu nhóm đã phân công workflow, ghi rõ workflow của bạn để tránh trùng với thành viên khác.
- Với Git, tạo commit nhỏ sau mỗi mốc: setup SUT, test data, Load plan, Stress plan, Spike plan, run logs, AI analysis, continuous testing proposal, final packaging.

## Task 1: Chuẩn bị SUT và môi trường

**Files:**
- Create: `report/main_report.md`
- Create: `report/ai_audit_report.md`
- Create: `evidence/screenshots/`
- Modify: `README.md`

- [ ] **Step 1: Clone và chạy EShop SUT**

  ```bash
  git clone https://github.com/ttbhanh/eshop-sut
  cd eshop-sut
  ```

  Đọc README của SUT để xác định lệnh chạy backend, frontend, database và port API thật. Ghi port backend vào `report/main_report.md`.

- [ ] **Step 2: Xác nhận endpoint thật**

  Dùng browser DevTools, Swagger nếu có, README hoặc source backend để xác định endpoint cho workflow:

  | Nhóm | Endpoint cần chọn | Bằng chứng cần ghi |
  | --- | --- | --- |
  | Auth-heavy | Login endpoint và behavior khóa tài khoản | URL, method, request body, response thành công/thất bại |
  | Read-heavy | Product listing/search và product detail | URL, query/path param, response có product ID |
  | Transactional | Add-to-cart và checkout/order creation | URL, method, body, token/session requirement |

- [ ] **Step 3: Ghi baseline phần cứng**

  Chạy một công cụ như `screenfetch`, `neofetch`, `lscpu`, `free -h`, hoặc `dxdiag` trên Windows. Chụp ảnh có hostname và ghi bảng cấu hình vào báo cáo:

  | Thuộc tính | Giá trị |
  | --- | --- |
  | Hostname | Ghi hostname thật |
  | CPU | Ghi model và số core/thread |
  | RAM | Ghi dung lượng |
  | OS | Ghi hệ điều hành |
  | Backend runtime | Ghi Node/Python/Java/.NET version tùy SUT |

- [ ] **Step 4: Commit môi trường ban đầu**

  ```bash
  git add README.md report/main_report.md report/ai_audit_report.md evidence/screenshots
  git commit -m "docs: initialize hw05 performance evidence"
  ```

## Task 2: Thiết kế workflow end-to-end và dữ liệu CSV

**Files:**
- Create: `jmeter/data/users.csv`
- Create: `jmeter/data/products.csv`
- Create: `jmeter/data/orders.csv`
- Modify: `report/main_report.md`
- Modify: `report/ai_audit_report.md`

- [ ] **Step 1: Viết prompt AI theo từng bước**

  Ghi vào `report/ai_audit_report.md` mỗi lượt gồm tên AI, ngày giờ, prompt, output. Prompt đầu nên yêu cầu AI không sinh ngay file cuối, mà trước tiên đề xuất workflow:

  ```text
  Tôi cần làm HW05 Performance Testing cho EShop SUT. Hãy giúp tôi thiết kế một workflow end-to-end duy nhất cho JMeter, bao phủ auth-heavy, read-heavy và transactional endpoint. Không viết test plan ngay. Trước tiên hãy liệt kê các API cần xác minh, dữ liệu CSV cần có, assertion nên dùng và rủi ro khóa tài khoản sau 3 lần login fail.
  ```

- [ ] **Step 2: Rà soát output AI**

  Trong `report/main_report.md`, tạo bảng:

  | Nội dung AI đề xuất | Giữ/Sửa/Bỏ | Lý do |
  | --- | --- | --- |
  | Ví dụ: login mỗi iteration | Sửa | Có thể tạo tải auth quá cao hoặc kích hoạt lockout nếu credentials sai |
  | Ví dụ: không kiểm tra token | Sửa | Các request transactional cần token/session hợp lệ |
  | Ví dụ: assertion chỉ check HTTP 200 | Sửa | Cần check field nghiệp vụ như product id/order id |

- [ ] **Step 3: Tạo CSV người dùng**

  `jmeter/data/users.csv` nên có header và tối thiểu vài tài khoản hợp lệ:

  ```csv
  username,password
  user01@example.com,Password123!
  user02@example.com,Password123!
  user03@example.com,Password123!
  ```

  Dùng tài khoản thật đã seed/tạo trong SUT. Không dùng tài khoản sai trong run chính để tránh lockout ngoài ý muốn.

- [ ] **Step 4: Tạo CSV sản phẩm**

  `jmeter/data/products.csv`:

  ```csv
  searchTerm,productId,quantity
  shirt,1,1
  phone,2,1
  book,3,2
  ```

  Thay `productId` bằng ID thật lấy từ API hoặc database seed.

- [ ] **Step 5: Tạo CSV order payload**

  `jmeter/data/orders.csv`:

  ```csv
  fullName,address,phone,couponCode,paymentMethod
  Nguyen Van A,227 Nguyen Van Cu Q5,0900000001,,COD
  Tran Thi B,227 Nguyen Van Cu Q5,0900000002,SALE10,COD
  Le Van C,227 Nguyen Van Cu Q5,0900000003,,COD
  ```

  Điều chỉnh cột đúng với API checkout thật.

- [ ] **Step 6: Commit dữ liệu test**

  ```bash
  git add jmeter/data report/main_report.md report/ai_audit_report.md
  git commit -m "test: add data driven performance workflow inputs"
  ```

## Task 3: Tạo Load Test Plan

**Files:**
- Create: `jmeter/plans/{StudentID}_Load_{YYYYMMDD}.jmx`
- Create: `jmeter/results/load/`
- Create: `jmeter/reports/load/`
- Modify: `report/main_report.md`
- Modify: `report/ai_audit_report.md`

- [ ] **Step 1: Dùng AI sinh bản nháp Load plan**

  Prompt nên cụ thể:

  ```text
  Dựa trên workflow đã xác minh, hãy đề xuất cấu hình JMeter Load Test mức tải bình thường cho máy cá nhân. Workflow gồm login -> search/list products -> product detail -> add cart -> checkout. Dữ liệu lấy từ users.csv, products.csv, orders.csv. Hãy đề xuất threads, ramp-up, loop/duration, think-time, assertion, listener duy nhất cho scenario này là Summary Report. Giải thích vì sao tham số hợp lý.
  ```

- [ ] **Step 2: Cấu hình JMeter Load**

  Mức khởi đầu an toàn cho máy cá nhân:

  | Tham số | Giá trị khởi đầu |
  | --- | --- |
  | Threads/users | 10 |
  | Ramp-up | 60 giây |
  | Duration | 5 phút |
  | Think-time | 1-3 giây giữa các request |
  | Listener/report view | Summary Report |
  | Assertion | HTTP status, response contains token/product/order id |

- [ ] **Step 3: Chạy Load và tạo report**

  ```bash
  jmeter -n -t jmeter/plans/{StudentID}_Load_{YYYYMMDD}.jmx -l jmeter/results/load/{StudentID}_Load_{YYYYMMDD}.jtl -e -o jmeter/reports/load
  ```

  Trong lúc chạy, mở resource monitor cạnh JMeter hoặc terminal để chụp chung một khung hình.

- [ ] **Step 4: Ghi kết quả Load vào báo cáo**

  Ghi các chỉ số tối thiểu:

  | Metric | Giá trị |
  | --- | --- |
  | Samples | Lấy từ Summary Report |
  | Error % | Lấy từ `.jtl`/report |
  | Average response time | Lấy từ report |
  | p95 | Lấy từ report |
  | Throughput/RPS | Lấy từ report |
  | CPU/RAM backend | Lấy từ ảnh resource monitor |

- [ ] **Step 5: Commit Load**

  ```bash
  git add jmeter/plans jmeter/results/load jmeter/reports/load report/main_report.md report/ai_audit_report.md evidence/screenshots
  git commit -m "test: add load performance scenario"
  ```

## Task 4: Tạo Stress Test Plan

**Files:**
- Create: `jmeter/plans/{StudentID}_Stress_{YYYYMMDD}.jmx`
- Create: `jmeter/results/stress/`
- Create: `jmeter/reports/stress/`
- Modify: `report/main_report.md`
- Modify: `report/ai_audit_report.md`

- [ ] **Step 1: Dùng AI đề xuất Stress plan**

  ```text
  Hãy đề xuất JMeter Stress Test cho cùng workflow Load Test, nhưng tăng tải theo bậc để tìm điểm suy giảm. Không dùng listener trùng với Load; scenario này dùng Aggregate Report. Cần tránh login lockout do 3 lần fail. Đề xuất threads theo bậc, ramp-up, duration mỗi bậc, stop condition, assertion và cách reset lockout nếu xảy ra.
  ```

- [ ] **Step 2: Cấu hình Stress theo bậc**

  Mức khởi đầu:

  | Giai đoạn | Threads | Ramp-up | Duration |
  | --- | ---: | ---: | ---: |
  | Warm-up | 10 | 60 giây | 2 phút |
  | Stress 1 | 25 | 90 giây | 3 phút |
  | Stress 2 | 50 | 120 giây | 3 phút |
  | Stress 3 | 75 | 180 giây | 3 phút |

  Nếu máy yếu hoặc backend lỗi sớm, giảm threads nhưng phải ghi lý do và số thực tế.

- [ ] **Step 3: Chạy Stress và tạo report**

  ```bash
  jmeter -n -t jmeter/plans/{StudentID}_Stress_{YYYYMMDD}.jmx -l jmeter/results/stress/{StudentID}_Stress_{YYYYMMDD}.jtl -e -o jmeter/reports/stress
  ```

- [ ] **Step 4: Xác định điểm gãy**

  Ghi điểm đầu tiên mà một trong các dấu hiệu xuất hiện:

  | Dấu hiệu | Ngưỡng ghi nhận |
  | --- | --- |
  | Error rate | Tăng rõ, ví dụ > 5% |
  | p95 | Tăng mạnh so với Load |
  | CPU | Gần 90-100% duy trì |
  | RAM | Tăng liên tục hoặc swap |
  | Functional issue | Checkout fail, login lockout, crash |

- [ ] **Step 5: Nếu bị lockout, reset và ghi lại**

  Ghi rõ tài khoản nào bị lock, thời điểm, cách reset qua admin/database/API, ảnh trước và sau reset.

- [ ] **Step 6: Commit Stress**

  ```bash
  git add jmeter/plans jmeter/results/stress jmeter/reports/stress report/main_report.md report/ai_audit_report.md evidence/screenshots
  git commit -m "test: add stress performance scenario"
  ```

## Task 5: Tạo Spike Test Plan

**Files:**
- Create: `jmeter/plans/{StudentID}_Spike_{YYYYMMDD}.jmx`
- Create: `jmeter/results/spike/`
- Create: `jmeter/reports/spike/`
- Modify: `report/main_report.md`
- Modify: `report/ai_audit_report.md`

- [ ] **Step 1: Dùng AI đề xuất Spike plan**

  ```text
  Hãy đề xuất JMeter Spike Test cho cùng workflow end-to-end. Không dùng listener trùng Load hoặc Stress; scenario này dùng View Results Tree trong quá trình debug và HTML report sau run. Cần mô phỏng tải nền thấp, spike tăng nhanh, giữ ngắn, rồi giảm. Nêu assertion và rủi ro lockout.
  ```

- [ ] **Step 2: Cấu hình Spike**

  Mức khởi đầu:

  | Giai đoạn | Threads | Ramp-up | Duration |
  | --- | ---: | ---: | ---: |
  | Baseline | 5 | 30 giây | 2 phút |
  | Spike | 60 | 15 giây | 1 phút |
  | Recovery | 5 | 30 giây | 2 phút |

  Nếu cần, dùng Ultimate Thread Group hoặc plugin tương đương; nếu không có plugin, mô phỏng bằng nhiều Thread Group liên tiếp.

- [ ] **Step 3: Chạy Spike và tạo report**

  ```bash
  jmeter -n -t jmeter/plans/{StudentID}_Spike_{YYYYMMDD}.jmx -l jmeter/results/spike/{StudentID}_Spike_{YYYYMMDD}.jtl -e -o jmeter/reports/spike
  ```

- [ ] **Step 4: Đánh giá recovery**

  Ghi thời gian hệ thống trở về gần baseline sau spike:

  | Metric | Trong spike | Sau recovery |
  | --- | --- | --- |
  | Error % | Ghi giá trị | Ghi giá trị |
  | p95 | Ghi giá trị | Ghi giá trị |
  | Throughput | Ghi giá trị | Ghi giá trị |
  | CPU/RAM | Ghi giá trị | Ghi giá trị |

- [ ] **Step 5: Commit Spike**

  ```bash
  git add jmeter/plans jmeter/results/spike jmeter/reports/spike report/main_report.md report/ai_audit_report.md evidence/screenshots
  git commit -m "test: add spike performance scenario"
  ```

## Task 6: Chạy Endurance/Soak Test 10-15 phút

**Files:**
- Create: `jmeter/results/endurance/`
- Create: `jmeter/reports/endurance/`
- Modify: `report/main_report.md`

- [ ] **Step 1: Chọn tải duy trì**

  Chọn mức thấp hơn điểm gãy của Stress. Ví dụ nếu Stress bắt đầu lỗi ở 50 users, chạy endurance ở 25-35 users.

- [ ] **Step 2: Chạy 10-15 phút**

  ```bash
  jmeter -n -t jmeter/plans/{StudentID}_Load_{YYYYMMDD}.jmx -l jmeter/results/endurance/{StudentID}_Endurance_{YYYYMMDD}.jtl -e -o jmeter/reports/endurance
  ```

  Nếu tái dùng Load plan, chỉnh duration trong bản copy hoặc trong JMeter property để đạt 10-15 phút.

- [ ] **Step 3: Báo cáo ngưỡng phần cứng**

  Ghi bằng số cụ thể:

  | Kết luận | Giá trị |
  | --- | --- |
  | Maximum stable RPS | Giá trị RPS ổn định cao nhất |
  | p95 tại ngưỡng | Giá trị ms |
  | Error rate tại ngưỡng | Giá trị % |
  | CPU ceiling | Giá trị % |
  | Memory ceiling | Giá trị MB/GB |

- [ ] **Step 4: Commit endurance**

  ```bash
  git add jmeter/results/endurance jmeter/reports/endurance report/main_report.md evidence/screenshots
  git commit -m "test: record endurance threshold"
  ```

## Task 7: Phân tích bằng AI và săn lỗi diễn giải sai

**Files:**
- Modify: `report/main_report.md`
- Modify: `report/ai_audit_report.md`
- Modify: `report/ai_critique.md`

- [ ] **Step 1: Cho AI phân tích log**

  Prompt:

  ```text
  Tôi có các file JMeter .jtl cho Load, Stress và Spike. Hãy phân tích throughput, average, p90, p95, p99, error rate và đề xuất performance thresholds. Chỉ kết luận dựa trên số liệu trong log. Nếu thiếu dữ liệu, hãy nói rõ thiếu gì.
  ```

- [ ] **Step 2: Tự đối chiếu với log thô**

  Mở `.jtl` hoặc HTML report, kiểm tra lại từng giá trị AI nêu. Tạo bảng:

  | Nhận định của AI | Giá trị AI nêu | Giá trị đúng từ `.jtl` | Đánh giá |
  | --- | --- | --- | --- |
  | Ví dụ: p95 Load là 300ms | 300ms | Ghi giá trị thật | Đúng/Sai và lý do |

- [ ] **Step 3: Đánh giá khuyến nghị tối ưu**

  Tạo bảng:

  | Khuyến nghị AI | Feasible/Hallucinated | Lý do |
  | --- | --- | --- |
  | Thêm database index | Feasible nếu query search/filter chậm và DB có cột phù hợp | Cần chứng cứ query/schema |
  | Bật SQLite WAL | Chỉ feasible nếu SUT dùng SQLite | Nếu SUT không dùng SQLite thì hallucinated |
  | Thêm connection pool | Feasible nếu backend dùng DB client hỗ trợ pool và lỗi do kết nối | Cần đối chiếu stack thật |

- [ ] **Step 4: Viết AI Critique 200-300 từ**

  Nội dung phải trả lời đủ:

  - AI sai, thiên lệch hoặc thiếu ở đâu?
  - Vì sao AI không tự phát hiện vấn đề?
  - Bạn học được nguyên tắc gì khi cộng tác với AI?

- [ ] **Step 5: Commit phân tích AI**

  ```bash
  git add report/main_report.md report/ai_audit_report.md report/ai_critique.md
  git commit -m "docs: add ai performance analysis critique"
  ```

## Task 8: Đề xuất Continuous Performance Testing

**Files:**
- Modify: `report/main_report.md`

- [ ] **Step 1: Viết mô hình pipeline**

  Đề xuất tối thiểu gồm:

  | Thành phần | Vai trò |
  | --- | --- |
  | GitHub webhook/CI trigger | Theo dõi commit hoặc pull request |
  | Change detector | Chỉ chạy performance test khi đổi backend/API/database |
  | Smoke perf test | Chạy nhanh để lọc lỗi lớn |
  | Nightly full perf test | Chạy Load/Stress/Spike hoặc subset |
  | Baseline store | Lưu p95/throughput/error rate theo commit |
  | Regression gate | Cảnh báo nếu p95 tăng quá ngưỡng |

- [ ] **Step 2: Thêm flow chart**

  Dùng Mermaid trong Markdown:

  ```mermaid
  flowchart TD
    A[Commit/PR to SUT] --> B{Backend/API/DB changed?}
    B -- No --> C[Skip performance suite]
    B -- Yes --> D[Run smoke performance test]
    D --> E{Error rate acceptable?}
    E -- No --> F[Flag build and open issue]
    E -- Yes --> G[Compare p95 with baseline]
    G --> H{p95 regression > threshold?}
    H -- Yes --> F
    H -- No --> I[Store metrics and pass]
    J[Nightly schedule] --> K[Run full Load/Stress/Spike suite]
    K --> G
  ```

- [ ] **Step 3: Thảo luận trade-off**

  Viết rõ:

  | Trade-off | Nội dung cần nêu |
  | --- | --- |
  | Cost | Full suite tốn thời gian và tài nguyên nên nên chạy nightly, không chạy mọi commit |
  | False alarms | Máy CI chia sẻ có nhiễu, cần baseline nhiều lần hoặc tolerance |
  | Coverage | Smoke perf nhanh nhưng không thay thế stress/spike |
  | Data stability | Test data phải reset được để checkout không làm bẩn DB |

- [ ] **Step 4: Commit proposal**

  ```bash
  git add report/main_report.md
  git commit -m "docs: propose continuous performance testing pipeline"
  ```

## Task 9: Agent Skill, phần 10 điểm

**Files:**
- Create: `agent-skill/SKILL.md`
- Create: `agent-skill/README.md`
- Modify: `report/main_report.md`
- Modify: `evidence/videos/video_links.md`

- [ ] **Step 1: Xác định phạm vi skill**

  Skill nên làm được:

  - Nhận endpoint group và workflow.
  - Sinh checklist test data.
  - Gợi ý tham số Load/Stress/Spike.
  - Nhắc người dùng chụp resource monitor và giữ log `.jtl`.
  - Hướng dẫn AI log analysis và misinterpretation hunt.

- [ ] **Step 2: Tạo `agent-skill/SKILL.md`**

  Nội dung tối thiểu:

  ```markdown
  ---
  name: performance-testing-workflow
  description: Guide an AI-first performance testing workflow for EShop endpoints using JMeter logs and human review.
  ---

  # Performance Testing Workflow

  Use this skill to plan Load, Stress, Spike, and endurance tests for one EShop endpoint workflow.

  ## Inputs

  - Student ID
  - API base URL
  - Auth-heavy endpoint
  - Read-heavy endpoint
  - Transactional endpoint
  - CSV data files

  ## Procedure

  1. Confirm endpoint methods, request bodies, auth/session handling, and lockout behavior.
  2. Produce a data-driven JMeter workflow using CSV input.
  3. Generate Load, Stress, and Spike parameters with distinct report views.
  4. Require human review for ramp-up, think-time, assertions, and lockout handling.
  5. Run tests, preserve `.jtl` logs, HTML reports, resource screenshots, and hardware evidence.
  6. Ask AI to analyze logs, then force manual verification against raw `.jtl` values.
  7. Classify AI optimization recommendations as feasible or hallucinated.
  ```

- [ ] **Step 3: Quay video demo skill**

  Video cần thể hiện cách dùng skill cho một endpoint group hoàn chỉnh, từ input đến kết quả hướng dẫn. Link đặt trong `evidence/videos/video_links.md`.

- [ ] **Step 4: Commit skill**

  ```bash
  git add agent-skill report/main_report.md evidence/videos/video_links.md
  git commit -m "docs: add reusable performance testing agent skill"
  ```

## Task 10: Video demo chính

**Files:**
- Create: `evidence/videos/video_links.md`
- Modify: `report/main_report.md`
- Modify: `README.md`

- [ ] **Step 1: Chuẩn bị kịch bản nói tiếng Việt**

  Video tổng ít nhất 6 phút, có thể chia 3 phần:

  | Phần | Nội dung |
  | --- | --- |
  | Load | Giới thiệu workflow, JMeter run, Summary Report, resource monitor |
  | Stress | Tăng tải, Aggregate Report, điểm gãy hoặc dấu hiệu suy giảm |
  | Spike | Spike nhanh, View Results Tree/debug evidence, recovery |

- [ ] **Step 2: Ghi hình đúng yêu cầu**

  Trong cùng khung hình phải thấy:

  - JMeter hoặc terminal chạy JMeter.
  - Resource monitor của backend process.
  - Bạn thuyết minh bằng tiếng Việt.

- [ ] **Step 3: Upload YouTube unlisted và ghi link**

  `evidence/videos/video_links.md`:

  ```markdown
  # Video Links

  - Main demo: <YouTube unlisted URL>
  - Agent Skill demo: <YouTube unlisted URL>
  ```

- [ ] **Step 4: Commit video link**

  ```bash
  git add evidence/videos/video_links.md report/main_report.md README.md
  git commit -m "docs: add performance demo video links"
  ```

## Task 11: Bug report và GitHub Issues

**Files:**
- Create: `issues/bug_reports.md`
- Modify: `report/main_report.md`

- [ ] **Step 1: Tạo issue nếu có lỗi thật**

  Với mỗi lỗi, GitHub Issue nên có:

  ```markdown
  ## Description
  Mô tả lỗi hoặc vấn đề hiệu năng.

  ## Environment
  SUT commit:
  OS:
  Hardware:
  Test scenario:

  ## Steps to reproduce
  1. Start backend.
  2. Run JMeter plan ...
  3. Observe ...

  ## Expected
  Kết quả mong đợi.

  ## Actual
  Kết quả thực tế.

  ## Evidence
  Screenshot/log/report link.
  ```

- [ ] **Step 2: Nếu không có bug, ghi rõ**

  Trong `issues/bug_reports.md`, ghi:

  ```markdown
  # Bug Reports

  No confirmed functional bugs were found during HW05 runs.

  Performance observations are documented in `report/main_report.md`.
  ```

- [ ] **Step 3: Commit bug report**

  ```bash
  git add issues/bug_reports.md report/main_report.md
  git commit -m "docs: record performance issue reports"
  ```

## Task 12: Hoàn thiện README, commit log và gói nộp

**Files:**
- Modify: `README.md`
- Create: `report/git_commit_log.txt`
- Create: `{StudentID}_HW05_AI_Performance_{SelfAssessedGrade}.zip`

- [ ] **Step 1: Xuất Git commit log**

  ```bash
  git log --oneline --decorate > report/git_commit_log.txt
  ```

- [ ] **Step 2: Hoàn thiện README**

  README cần có:

  | Mục | Nội dung |
  | --- | --- |
  | Self-assessment table | 6 tiêu chí, tổng 100 |
  | Scenarios run | Load, Stress, Spike, Endurance |
  | Endpoint groups covered | Auth-heavy, Read-heavy, Transactional |
  | Endurance threshold | RPS, p95, error rate, CPU/RAM |
  | Bugs/issues | Số issue và link |
  | Demo video | YouTube unlisted URL |
  | GitHub repo | Public repo URL |

- [ ] **Step 3: Xuất PDF**

  Có thể dùng một trong các cách:

  ```bash
  pandoc report/main_report.md -o report/main_report.pdf
  pandoc report/ai_audit_report.md -o report/ai_audit_report.pdf
  ```

  Nếu không có `pandoc`, mở Markdown bằng VS Code/Typora/Markdown Preview và export PDF.

- [ ] **Step 4: Kiểm tra checklist file bắt buộc**

  Trước khi zip, xác nhận có đủ:

  - Main report Markdown + PDF.
  - Public GitHub repository link.
  - 3 JMeter plans Load/Stress/Spike đúng tên.
  - 3 raw `.jtl` logs.
  - 3 HTML report folders.
  - Resource-monitor screenshots.
  - Hardware-spec screenshot/table.
  - YouTube unlisted demo link.
  - AI Critique.
  - AI Audit Report Markdown + PDF.
  - Git commit log text file.
  - GitHub Issues hoặc ghi rõ không có confirmed bugs.
  - README summary và self-assessment.
  - Agent Skill và video demo skill nếu làm phần này.

- [ ] **Step 5: Tạo zip đúng tên**

  ```bash
  zip -r {StudentID}_HW05_AI_Performance_{SelfAssessedGrade}.zip README.md report jmeter evidence issues agent-skill
  ```

  Ví dụ nếu MSSV là `25127001`, tự đánh giá `090`:

  ```bash
  zip -r 25127001_HW05_AI_Performance_090.zip README.md report jmeter evidence issues agent-skill
  ```

- [ ] **Step 6: Commit lần cuối**

  ```bash
  git add README.md report evidence issues agent-skill
  git commit -m "docs: finalize hw05 submission package"
  ```

## Self-Review

- **Spec coverage:** Kế hoạch bao phủ Task 1 Load/Stress/Spike, CSV data-driven workflow, 3 report views khác nhau, evidence/resource/hardware, endurance threshold, demo video, bug reports, Task 2 AI analysis và misinterpretation hunt, Task 3 continuous performance testing, Agent Skill, AI Audit, AI Critique, Git commit log và zip nộp Moodle.
- **Placeholder scan:** Những chuỗi `{StudentID}`, `{YYYYMMDD}` và `{SelfAssessedGrade}` là quy ước bắt buộc từ đề; phải thay bằng giá trị thật khi thực hiện. Các giá trị metric không thể điền trước vì phải lấy từ log thực tế.
- **Consistency:** Workflow, tên file, thư mục log/report và thứ tự commit được giữ thống nhất giữa các task.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-16-hw05-performance-testing.md`. Two execution options:

1. **Subagent-Driven (recommended)** - Dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
