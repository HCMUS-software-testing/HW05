# Kịch bản Lời thoại Quay Video Demo HW05 (Voiceover Script)

- **Sinh viên:** Mai Thị Kim Duyên
- **MSSV:** 23127185
- **Thời lượng dự kiến:** 6 phút 30 giây (Đạt chuẩn >= 6 phút)
- **Mục tiêu:** Thuyết minh chi tiết quá trình kiểm thử hiệu năng, cấu hình JMeter, phân tích JTL, phát hiện lỗi SUT và tích hợp GitHub Issues.

---

## 🎬 Chuẩn bị Màn hình trước khi Quay

1. **Giao diện 1 (Nửa trái):** Terminal 1 chạy Backend EShop (`node server.js`), Terminal 2 chạy `htop` để theo dõi CPU/RAM.
2. **Giao diện 2 (Nửa phải):** Trình duyệt web mở file Báo cáo HTML Dashboard (`jmeter/reports/load/index.html`) và trang GitHub Issues của repo `HCMUS-software-testing/HW05`.
3. **Cửa sổ chuẩn bị sẵn:** Mở file `report/main-report.pdf` và `report/bug-report.pdf`.

---

## ⏱️ KỊCH BẢN CHI TIẾT (LỜI THOẠI ĐỌC TRỰC TIẾP)

### PHẦN 1: GIỚI THIỆU & PHẠM VI KIỂM THỬ (0:00 - 1:00)

**[Hành động trên màn hình]:** Mở file `report/main-report.pdf` trên màn hình.

> **[Lời thoại]:**
> *"Kính chào Thầy/Cô và các bạn. Em tên là Mai Thị Kim Duyên, MSSV 23127185. Sau đây em xin trình bày video demo cho Bài tập cá nhân HW05: Kiểm thử hiệu năng hệ thống EShop có sự hỗ trợ của công cụ AI.*
>
> *Hệ thống được kiểm thử là EShop Backend chạy cục bộ tại địa chỉ `http://localhost:3000`. Workflow kiểm thử của em đại diện cho một hành trình mua sắm thực tế của người dùng, bao gồm 9 bước liên hoàn:*
> 1. *Đăng ký tài khoản mới (`POST /api/register`)*
> 2. *Đăng nhập nhận JWT Token (`POST /api/login`)*
> 3. *Duyệt danh mục sản phẩm (`GET /api/categories`)*
> 4. *Tìm kiếm sản phẩm (`GET /api/products?search=i`)*
> 5. *Xem chi tiết sản phẩm (`GET /api/products/1`)*
> 6. *Thêm sản phẩm vào giỏ hàng (`POST /api/cart`)*
> 7. *Áp dụng mã giảm giá SAVE10 (`POST /api/apply-coupon`)*
> 8. *Thực hiện Checkout đặt hàng (`POST /api/checkout`)*
> 9. *Và xem lịch sử đơn hàng của tôi (`GET /api/orders/my-orders`)."*

---

### PHẦN 2: CẤU HÌNH JMETER TEST PLAN & KỊCH BẢN TẢI (1:00 - 2:30)

**[Hành động trên màn hình]:** Chuyển sang phần mềm JMeter GUI hoặc xem file `jmeter/plans/23127185_Load.jmx`. Chỉ chuột vào node `JSON Extractor` bên dưới `Login Request`.

> **[Lời thoại]:**
> *"Tiếp theo, em xin trình bày về cấu hình Test Plan trên JMeter. Để workflow chạy liên tục mà không bị lỗi 401 Unauthorized, em đã thêm một JSON Extractor bên dưới sampler Login để bóc tách trường token trong JSON phản hồi, lưu vào biến `token`, sau đó tự động truyền vào HTTP Header Manager dạng `Bearer Token` cho các request phía sau như Cart, Coupon và Checkout.*
>
> *Em đã thiết lập và thực thi 4 kịch bản kiểm thử hiệu năng:*
> - *Thứ nhất là **Load Test**: Chạy 10 người dùng đồng thời, ramp-up 5 giây trong thời gian 30 giây.*
> - *Thứ hai là **Stress Test**: Chạy 10 người dùng duy trì tải trong 600 giây.*
> - *Thứ ba là **Spike Test**: Chạy 10 người dùng tạo đột biến trong 10 giây.*
> - *Và thứ tư là **Soak Test**: Chạy 2 worker kiểm thử sức bền liên tục trong 600 giây (tương đương 10 phút).*
>
> *Mỗi lần chạy đều xuất ra file log JTL thô có đầy đủ header thông tin để phục vụ phân tích."*

---

### PHẦN 3: DEMO CHẠY TEST & TRÌNH DIỄN BÁO CÁO HTML (2:30 - 4:00)

**[Hành động trên màn hình]:** 
1. Mở cửa sổ Terminal hiển thị `htop` đang giám sát tài nguyên CPU/RAM.
2. Mở trình duyệt web hiển thị trang Dashboard Báo cáo HTML tại `jmeter/reports/load/index.html`.
3. Di chuột qua các biểu đồ **APDEX Summary**, **Response Times Over Time**, **Throughput**.

> **[Lời thoại]:**
> *"Bây giờ em xin mời Thầy/Cô quan sát quá trình thực thi và báo cáo kết quả. Khi runner thực thi, công cụ `htop` bên cửa sổ terminal cho thấy dung lượng RAM và CPU được duy trì rất ổn định, không có hiện tượng rò rỉ bộ nhớ.*
>
> *Đây là giao diện HTML Dashboard Report được sinh ra từ file JTL thô của Load Test. Báo cáo hiển thị tổng cộng 90 mẫu request, đạt chỉ số APDEX mức tuyệt đối 1.000 với **0% tỷ lệ lỗi**. Tất cả 90 request đều vượt qua các hàm kiểm thử Assertion status 200 OK và đúng cấu trúc dữ liệu JSON."*

---

### PHẦN 4: PHÂN TÍCH CHỈ SỐ & PHÁT HIỆN LỖI BACKEND (4:00 - 5:30)

**[Hành động trên màn hình]:** 
1. Mở file `report/bug-report.pdf` trên màn hình.
2. Chuyển sang trình duyệt hiển thị danh sách **GitHub Issues** trên repo `HCMUS-software-testing/HW05`.

> **[Lời thoại]:**
> *"Dựa trên dữ liệu JTL và rà soát trực tiếp source code Backend (`server.js`), em đã phân tích được các điểm nghẽn hiệu năng và 11 lỗi nghiêm trọng của hệ thống:*
>
> **1. Về Hiệu năng:**
> *Các API chỉ đọc (`GET Categories`, `GET Products`) có thời gian phản hồi siêu nhanh dưới 1.5 ms. Trong khi đó, hai API ghi dữ liệu là `Register` và `Checkout` có độ trễ trung bình cao nhất (lần lượt 41.5 ms và 34.7 ms). Nguyên nhân là do SQLite sử dụng cơ chế ghi đĩa đồng bộ. Em kiến nghị bật chế độ Write-Ahead Logging (WAL) để tối ưu I/O đĩa.*
>
> **2. Về Lỗi Logic & Bảo mật SUT:**
> *Rà soát mã nguồn giúp em phát hiện các lỗi nghiêm trọng:*
> - *Lỗi khóa tài khoản: Khi đăng nhập sai, code tự cộng `+2` số lần thử thay vì `+1` và khóa tài khoản 180 giây thay vì 30 giây.*
> - *Lỗi tính mã giảm giá: Công thức tính coupon phần trăm bị sai khiến mã 10% bị trừ tới 90% giá trị.*
> - *Lỗi so sánh ngưỡng tối thiểu mã giảm giá dùng dấu `>` thay vì `>=`.*
> - *Lỗi bảo mật nghiêm trọng: Route `POST /api/checkout` tin tưởng trực tiếp `total_amount` do Client gửi lên mà không tự tính lại từ cơ sở dữ liệu.*
> - *Lỗ hổng SQL Injection tại ô tìm kiếm sản phẩm và Lỗ hổng Leo thang đặc quyền Admin qua API cập nhật user profile.*
>
> *Toàn bộ các lỗi này em đã tạo các **GitHub Issues** chính thức từ #12 đến #19 trên repository của dự án với mô tả chi tiết cách tái lập và gợi ý sửa lỗi."*

---

### PHẦN 5: AI AUDIT, CRITIQUE & KẾT LUẬN (5:30 - 6:30+)

**[Hành động trên màn hình]:** Mở file `report/ai-audit-report.pdf` và `report/ai-critique.pdf`.

> **[Lời thoại]:**
> *"Cuối cùng, về quá trình tương tác với AI: Bản nháp Test Plan ban đầu do AI khởi tạo bị lỗi đặt sai phân cấp của Token Extractor, khiến các sampler phía sau bị trả về lỗi 401. Em đã tự kiểm toán (AI Audit), phản biện (AI Critique) và khắc phục lại cấu trúc cây JMX để đảm bảo bài test chạy đúng 100%.*
>
> *Tất cả các artifact bao gồm Test Plan `.jmx`, log thô `.jtl`, báo cáo HTML, các báo cáo PDF và mã nguồn tool runner đã được đóng gói đầy đủ và đồng bộ trong thư mục bài nộp `submission/23127185_HW05/`.*
>
> *Em xin chân thành cảm ơn Thầy/Cô đã dành thời gian theo dõi video trình bày của em. Em xin kết thúc phần demo tại đây!"*
