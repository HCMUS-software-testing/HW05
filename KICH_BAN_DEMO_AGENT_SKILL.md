# KỊCH BẢN THAO TÁC VÀ LỜI THOẠI DEMO AGENT SKILL (HW05)

- **Sinh viên**: Lê Trung Kiên — **MSSV**: `23127075`
- **Agent Skill**: `performance-testing-skills` (Vị trí: `.agents/skills/performance-testing-skills/`)
- **Mục tiêu**: Trình diễn từ đầu đến cuối cách AI Agent tự động áp dụng skill để phân tích SUT, tạo JMX plan, thực thi kiểm thử, phân tích `.jtl` và đóng gói nộp bài.
- **Thời lượng mục tiêu**: **3 - 5 phút**
- **Hình thức đăng**: YouTube Unlisted Video (Đính kèm trong báo cáo Skill)

---

## 🖥️ 1. CẤU HÌNH MÀN HÌNH DEMO SKILL

* **Khung hình**: Mở giao diện AI Assistant (Codex / Antigravity IDE / VS Code) bên trái và Terminal bên phải.
* **Chuẩn bị môi trường**: Thư mục `.agents/skills/performance-testing-skills/` đã sẵn có trong dự án.

---

## ⏱️ 2. KỊCH BẢN CHI TIẾT THEO THỜI GIAN & LỜI THOẠI

---

### 📌 BƯỚC 1: GIỚI THIỆU AGENT SKILL (0:00 - 0:45)

* **Thao tác màn hình**:
  * Mở file `.agents/skills/performance-testing-skills/SKILL.md`.
  * Cho thấy cấu trúc skill gồm 10 Phase: từ SUT Analysis, JMX Design, Script Runner, JTL Analyzer đến Submission Packaging.
* **Lời thoại**:
  > *"Xin chào thầy. Để tự động hóa và chuẩn hóa quy trình kiểm thử hiệu năng cho các dự án REST API, em đã đóng gói bộ Agent Skill tên là `performance-testing-skills` tại thư mục `.agents/skills/performance-testing-skills/`.*
  > *Bộ skill này chứa toàn bộ lý thuyết ISTQB Performance Testing, quy chuẩn đặt tên kịch bản, cấu hình Gaussian Random Timer, script đo tài nguyên và bộ công cụ tự động phân tích log raw JTL."*

---

### 📌 BƯỚC 2: KÍCH HOẠT SKILL & ĐỌC PHÂN TÍCH SUT (0:45 - 1:30)

* **Thao tác màn hình**:
  * Gõ prompt kích hoạt AI:
    ```text
    /using-superpowers /performance-testing-skills Hãy phân tích ứng dụng eshop-sut và thiết kế kịch bản kiểm thử hiệu năng cho luồng Admin.
    ```
  * Quay màn hình thấy AI tự động đọc `eshop-sut/backend/server.js`, trích xuất 6 API endpoints và tạo 2 file CSV `credentials.csv` và `products.csv` trong `src/data/`.
* **Lời thoại**:
  > *"Khi kích hoạt skill bằng lệnh `/performance-testing-skills`, AI Agent lập tức tự động quét mã nguồn SUT trong `eshop-sut/backend/server.js`, phân loại API thành 3 nhóm Auth-heavy, Read-heavy và Transactional.*
  > *Sau đó, AI tự động khởi tạo dữ liệu kiểm thử đầu vào tại `src/data/credentials.csv` và `src/data/products.csv` với định dạng UTF-8 chuẩn."*

---

### 📌 BƯỚC 3: SINH JMX TEST PLANS & SỬA LỖI ĐƯỜNG DẪN (1:30 - 2:30)

* **Thao tác màn hình**:
  * Hiển thị AI sinh 3 file `.jmx` trong `src/test-plans/` với quy ước tên `{StudentID}_{ScenarioType}_{YYYYMMDD}.jmx`.
  * Cho thấy AI thiết lập đường dẫn tương đối `data/products.csv` và sử dụng **3 loại Listener riêng biệt** (`Aggregate Report`, `Summary Report`, `View Results Tree`).
* **Lời thoại**:
  > *"Tiếp theo, theo quy trình trong SKILL.md, AI Agent tự động sinh 3 test plan Load, Stress, Spike. Skill bắt buộc AI phải tuân thủ:*
  > *1. Đặt tên file theo đúng chuẩn MSSV.*
  > *2. Sử dụng đường dẫn tương đối để bộ bài làm có tính di động (portable).*
  > *3. Sử dụng 3 loại Listener hoàn toàn khác nhau cho 3 kịch bản.*
  > *4. Cấu hình Gaussian Random Timer với thông số mean và sigma chuẩn xác thay vì khoảng chặn cứng."*

---

### 📌 BƯỚC 4: THỰC THI & PHÂN TÍCH LOG AUTOMATION (2:30 - 3:45)

* **Thao tác màn hình**:
  * AI thực thi script `./run_tests.sh` và câu lệnh phân tích JTL:
    ```bash
    python3 tools/analyze_jtl.py results/load/raw.jtl results/stress/raw.jtl results/spike/raw.jtl
    ```
  * Màn hình console in ra bảng tổng hợp Throughput, Average Latency, p95, p99 từ log `.jtl` thô.
* **Lời thoại**:
  > *"Sau khi test plan được thực thi, AI Agent kích hoạt công cụ phân tích log tích hợp trong skill `analyze_jtl.py`. Công cụ này đọc trực tiếp từng sample từ file `.jtl` thô, tính toán chính xác Percentile p95, p99 và Throughput toàn run, loại bỏ hoàn toàn hiện tượng AI bịa số hoặc nhầm lẫn giữa Average Response Time và p95 Tail-Latency."*

---

### 📌 BƯỚC 5: ĐÓNG GÓI & KIỂM ĐỊNH BÀI NỘP (3:45 - 4:30)

* **Thao tác màn hình**:
  * AI thực thi script kiểm định bài nộp:
    ```bash
    python3 tools/validate_submission.py
    ```
  * Hiển thị danh sách kết quả `PASS` cho toàn bộ tiêu chí bài làm.
* **Lời thoại**:
  > *"Cuối cùng, skill định hướng AI khởi chạy validator `validate_submission.py` để rà soát toàn bộ cấu trúc file, tính nhất quán giữa JTL và HTML report, đối chiếu sampler count và đảm bảo không có đường dẫn tuyệt đối.*
  > *Nhờ bộ Agent Skill này, toàn bộ quy trình kiểm thử hiệu năng có thể tái sử dụng 100% cho bất kỳ dự án REST API nào khác. Em xin kết thúc phần demo Agent Skill!"*

---

## 📤 3. HƯỚNG DẪN GẮN LINK DEMO AGENT SKILL

1. Upload video demo Agent Skill lên YouTube ở chế độ **Unlisted**.
2. Dán link video demo Skill vào 2 vị trí:
   - Mục Agent Skill trong [`src/README.md`](src/README.md)
   - Phần Báo cáo Skill tại [`GUIDE_PERFORMANCE_TESTING_SKILLS.md`](GUIDE_PERFORMANCE_TESTING_SKILLS.md)
