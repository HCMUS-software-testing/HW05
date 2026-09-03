# KỊCH BẢN THAO TÁC VÀ LỜI THOẠI QUAY VIDEO DEMO HW05

- **Sinh viên**: Lê Trung Kiên — **MSSV**: `23127075`
- **Bài tập**: HW05 - Performance Testing with AI
- **Workflow**: Member 4 — Admin Workflow (`EShop REST Backend`)
- **Thời lượng mục tiêu**: **7 phút 30 giây** (Đạt điều kiện $\ge$ 6 phút)
- **Hình thức đăng**: YouTube Unlisted Video (Không công khai)

---

## 🖥️ 1. HƯỚNG DẪN CHUẨN BỊ MÀN HÌNH QUAY (SPLIT-SCREEN SETUP)

> ⚠️ **QUY ĐỊNH BẮT BUỘC CỦA ĐỀ BÀI**: Màn hình phải hiển thị **JMeter CLI / Terminal** VÀ **Công cụ giám sát tài nguyên (`htop`) TRONG CÙNG MỘT KHUNG HÌNH** (không được chuyển tab hay ẩn `htop`).

### Bố cục 2 cửa sổ song song (50/50):
```text
+------------------------------------+------------------------------------+
|  CỬA SỔ TERMINAL TRÁI (50%)        |  CỬA SỔ TERMINAL PHẢI (50%)        |
|  - Nơi gõ lệnh thực thi test plan  |  - Chạy `htop`                     |
|  - Mở file Markdown báo cáo        |  - Lọc tiến trình: `node` & `java` |
|  - Mở fastfetch / code JMX         |  - Theo dõi CPU%, RAM RSS real-time|
+------------------------------------+------------------------------------+
```

### Các lệnh chuẩn bị trước khi bấm Record:
1. **Terminal 1 (Backend SUT)**: Đảm bảo SUT đang chạy tại root project:
   ```bash
   cd eshop-sut/backend && npm start
   ```
2. **Terminal 2 (Giám sát `htop`)**:
   ```bash
   htop -p $(pgrep -d, -f 'node|java')
   ```
3. **Terminal 3 (Thao tác bài làm chính - Nửa bên trái)**:
   ```bash
   cd src
   ```

### 💡 Bộ lệnh chạy các kịch bản kiểm thử trong bài:
- **Chạy Load / Stress / Spike**:
  ```bash
  ./run_tests.sh
  ```
- **Chạy Endurance Test (10 phút) + Giám sát RAM/CPU tự động**:
  ```bash
  BACKEND_PID="$(pgrep -fo 'node .*server\.js')" ./run_endurance.sh
  ```

---

## ⏱️ 2. KỊCH BẢN CHI TIẾT THEO THỜI GIAN & LỜI THOẠI

---

### 📌 PHẦN 1: GIỚI THIỆU & MÔI TRƯỜNG PHẦN CỨNG (0:00 - 1:00)

* **Thao tác màn hình**:
  * Ở cửa sổ trái, gõ lệnh `fastfetch` (hoặc mở ảnh [`src/evidence/hardware/fastfetch.png`](src/evidence/hardware/fastfetch.png)).
  * Cho thấy hostname `tkin@fedora`, CPU Intel Core Ultra 7 155H, 16GB RAM.
* **Lời thoại**:
  > *"Xin chào thầy và các bạn. Em tên là Lê Trung Kiên, MSSV 23127075. Trong bài tập HW05 Kiểm thử hiệu năng với sự hỗ trợ của AI, em đảm nhận vai trò Thành viên 4 phụ trách luồng Admin Workflow của hệ thống EShop REST Backend.*
  > *Trước tiên, em xin giới thiệu môi trường thực thi trên máy cá nhân: Máy sử dụng hệ điều hành Fedora Linux x86_64, vi xử lý Intel Core Ultra 7 155H, 16GB RAM. Backend SUT Node.js và SQLite đang hoạt động tại cổng 3000."*

---

### 📌 PHẦN 2: GIẢI THÍCH WORKFLOW 6 API & TEST DATA (1:00 - 2:00)

* **Thao tác màn hình**:
  * Ở cửa sổ trái, mở file kịch bản JMX [`src/test-plans/23127075_Load_20260901.jmx`](src/test-plans/23127075_Load_20260901.jmx) hoặc hiển thị nội dung 6 Samplers.
  * Mở 2 file CSV trong [`src/data/`](src/data) (`credentials.csv` và `products.csv`).
* **Lời thoại**:
  > *"Workflow end-to-end của em gồm 6 bước API bao phủ trọn vẹn 3 nhóm yêu cầu:*
  > *1. Auth-heavy: Đăng nhập Admin (`POST /api/login`) lấy JWT Token, sau đó gọi API đọc danh sách Admin Users (`GET /api/admin/users`).*
  > *2. Read-heavy: Lấy danh sách sản phẩm (`GET /api/products`) và danh mục (`GET /api/categories`).*
  > *3. Transactional: Tạo sản phẩm mới từ dữ liệu trong file `products.csv`, trích xuất ID động và ngay lập tức gọi API xóa sản phẩm đó để dọn sạch dữ liệu.*
  > *Tất cả các kịch bản đều dùng đường dẫn tương đối và có Response Assertion kiểm tra mã HTTP 200."*

---

### 📌 PHẦN 3: KỊCH BẢN LOAD TESTING (2:00 - 3:30)

* **Thao tác màn hình**:
  * Cửa sổ phải: `htop` đang chạy.
  * Cửa sổ trái: Chạy kịch bản Load test qua CLI:
    ```bash
    jmeter -n -t test-plans/23127075_Load_20260901.jmx -l results/load/raw.jtl -e -o results/load/html-report
    ```
  * Chỉ chuột sang cửa sổ `htop` cho thấy CPU/RAM tăng nhẹ.
* **Lời thoại**:
  > *"Tiếp theo là kịch bản 1: Load Testing. Cấu hình kịch bản gồm 10 Virtual Users (threads), ramp-up trong 10 giây, lặp 5 lần, tổng cộng 300 samples. Em cài đặt Gaussian Random Timer với mean 2000ms, sigma 333ms để giả lập think-time thực tế.*
  > *Nhìn sang cửa sổ htop bên phải, tài nguyên CPU tăng nhẹ khoảng 10-15%, bộ nhớ ổn định.*
  > *Kịch bản này sử dụng Listener Aggregate Report. Kết quả thực tế từ raw JTL: 300 samples thành công 100%, Throughput trung bình 4.48 RPS, thời gian phản hồi trung bình 9.76ms và p95 cực tốt ở mức 17ms."*

---

### 📌 PHẦN 4: KỊCH BẢN STRESS TESTING (3:30 - 5:00)

* **Thao tác màn hình**:
  * Cửa sổ trái: Chạy kịch bản Stress test qua CLI:
    ```bash
    jmeter -n -t test-plans/23127075_Stress_20260901.jmx -l results/stress/raw.jtl -e -o results/stress/html-report
    ```
  * Quan sát `htop` bên phải: Các thanh CPU sáng màu, tài nguyên hoạt động mạnh hơn.
* **Lời thoại**:
  > *"Chuyển sang kịch bản 2: Stress Testing nhằm đẩy hệ thống lên tải cao. Cấu hình dùng 50 Virtual Users, ramp-up 15 giây, 10 vòng lặp, tổng cộng 3,000 samples với think-time dồn dập hơn (mean 1000ms).*
  > *Trực quan trên htop cho thấy CPU nhảy lên 30-40%.*
  > *Kịch bản này sử dụng loại Listener thứ hai là Summary Report. Kết quả: 3,000 samples không có lỗi nào (Error 0.00%), Throughput trung bình tăng lên 40.19 RPS, thời gian phản hồi trung bình là 7.62ms và p95 duy trì ở mức 15ms. SUT đáp ứng rất tốt ở mức tải 50 user."*

---

### 📌 PHẦN 5: KỊCH BẢN SPIKE TESTING (5:00 - 6:30)

* **Thao tác màn hình**:
  * Cửa sổ trái: Chạy kịch bản Spike test qua CLI:
    ```bash
    jmeter -n -t test-plans/23127075_Spike_20260901.jmx -l results/spike/raw.jtl -e -o results/spike/html-report
    ```
  * Quan sát `htop`: CPU vọt đỉnh tức thì trong 5 giây.
* **Lời thoại**:
  > *"Kịch bản thứ 3 là Spike Testing: Đột biến 100 Virtual Users đổ dồn vào hệ thống chỉ trong 1 giây, lặp 3 lần (1,800 samples) và không có think-time.*
  > *Trên htop, toàn bộ các nhân CPU vọt đỉnh ngay lập tức.*
  > *Kịch bản này sử dụng Listener loại thứ 3 là View Results Tree. Kết quả từ log thô cho thấy Throughput trung bình đạt tới 352.73 RPS. Dù không có lỗi HTTP (0% error), nhưng độ trễ tail-latency p95 bị dội lên 476ms và max latency lên 569ms. Điều này minh chứng hiện tượng nghẽn khóa ghi SQLite khi bị dội tải đột biến."*

---

### 📌 PHẦN 6: ENDURANCE TEST & CÁC BUG PHÁT HIỆN (6:30 - 7:30)

* **Thao tác màn hình**:
  * Ở cửa sổ trái, hiển thị lệnh chạy Endurance Test hoặc file log tài nguyên:
    ```bash
    BACKEND_PID="$(pgrep -fo 'node .*server\.js')" ./run_endurance.sh
    ```
  * Mở file [`src/report/main-report.md`](src/report/main-report.md) mục 1.5 và file [`src/report/bug-report.md`](src/report/bug-report.md).
* **Lời thoại**:
  > *"Ngoài ra, để xác định ngưỡng vận hành bền vững, em đã thực thi kịch bản Endurance Test ngâm tải trong 10 phút (30 VU, 17,238 samples) bằng câu lệnh `./run_endurance.sh`. Lệnh này tự động kích hoạt script `monitor_backend.py` ghi nhận bộ nhớ RSS cứ 5 giây/lần. Kết quả xác lập điểm tải bền vững 28.80 RPS với RSS bộ nhớ Node.js duy trì trong khoảng 103-111 MiB, chứng minh hệ thống không bị rò rỉ bộ nhớ (memory leak).*
  > *Đồng thời, em đã phát hiện và ghi nhận 3 vấn đề trong Báo cáo lỗi (Bug Report):*
  > *1. Bug Bảo mật: Endpoint Product CRUD thiếu middleware `authenticateToken` cho phép người dùng vãng lai tạo/sửa/xóa sản phẩm.*
  > *2. Bug Bảo mật: Lỗi SQL Injection tại API tìm kiếm sản phẩm `GET /api/products?search=...`.*
  > *3. Bug Hiệu năng: Tail-latency tăng vọt 31 lần khi Spike 100 VU/s do nghẽn SQLite Write Lock.*
  > *Em xin kết thúc phần trình bày demo. Cảm ơn thầy và các bạn đã chú ý lắng nghe!"*

---

## 📤 3. CÁC BƯỚC UPLOAD & HOÀN THIỆN FILE NỘP BÀI

1. Sau khi quay xong, kiểm tra dung lượng file video và thời lượng đạt $\ge$ **6 phút 30 giây**.
2. Upload video lên [YouTube Studio](https://studio.youtube.com/).
3. Tại bước **Visibility (Quyền truy cập)**: Chọn **Unlisted (Không công khai)**.
4. Copy liên kết video (dạng `https://youtu.be/...`).
5. Dán link video vào 2 file:
   - [`src/README.md`](src/README.md#L96)
   - [`src/report/main-report.md`](src/report/main-report.md#L104)
