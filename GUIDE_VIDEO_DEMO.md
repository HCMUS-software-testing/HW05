# Hướng Dẫn Quay Video Demo (YouTube Unlisted Video Guide)

Tài liệu này hướng dẫn chi tiết cách quay video demo thuyết minh bài tập HW05 đáp ứng 100% quy định trong file đề bài (`req/2026.HW05.Performance Testing_Vi.md`).

---

## 📹 1. Yêu Cầu Bắt Buộc Từ Đề Bài (Requirements)

- **Thời lượng**: Tổng cộng **ít nhất 6 phút** ($\ge$ 6:00).
- **Khung hình (Same Frame)**: Phải hiển thị đồng thời cả **Cửa sổ chạy lệnh/JMeter** VÀ **Resource Monitor (`htop`)** trong CÙNG MỘT KHUNG HÌNH (không chuyển tab che mất htop).
- **Thuyết minh**: Giọng nói tiếng Việt của chính sinh viên (không dùng giọng AI đọc).
- **Chế độ đăng**: Upload lên YouTube ở chế độ **Unlisted** (KhÔNG công khai).

---

## 🎬 2. Bố Cục Khung Hình Màn Hình (Screen Layout Setup)

Trước khi bấm quay màn hình (dùng OBS Studio / Kazam / Vokoscreen), bạn hãy sắp xếp 2 cửa sổ song song:

```text
+-----------------------------------+-----------------------------------+
|   CỬA SỔ TERMINAL 1 (BÊN TRÁI)    |   CỬA SỔ TERMINAL 2 (BÊN PHẢI)    |
|                                   |                                   |
|   Chạy lệnh ./run_tests.sh        |   Đang chạy `htop` (Filter node)  |
|   hoặc giao diện JMeter           |   Hiển thị CPU%, RAM% real-time   |
|                                   |                                   |
+-----------------------------------+-----------------------------------+
```

---

## 🎙️ 3. Kịch Bản Thuyết Minh Chi Tiết (Script theo từng Phút)

### 📌 Phần 1: Giới thiệu chung & Môi trường phần cứng (Phút 0:00 - 1:15)
- **Hành động**: Mở terminal chạy `fastfetch` bên trái.
- **Lời nói mẫu**:
  > *"Xin chào thầy và các bạn. Em tên là Lê Trung Kiên, MSSV 23127075. Trong bài tập HW05 Performance Testing, em đảm nhận vị trí Thành viên 4 với luồng nghiệp vụ Web Admin của hệ thống EShop SUT. Môi trường kiểm thử của em chạy trên hệ điều hành Fedora Linux, vi xử lý [Tên CPU] với [Số RAM] GB RAM."*

---

### 📌 Phần 2: Giải thích Luồng Kịch bản & Dữ liệu CSV (Phút 1:15 - 2:30)
- **Hành động**: Mở file `src/data/credentials.csv`, `src/data/products.csv` và giải thích file `.jmx`.
- **Lời nói mẫu**:
  > *"Em thiết kế luồng kịch bản Admin bao phủ đầy đủ 3 nhóm API:
  > 1. Auth-heavy: Đăng nhập admin với tài khoản trong credentials.csv và trích xuất Bearer JWT token.
  > 2. Read-heavy: Gọi API lấy danh sách Admin Users kèm token xác thực, lấy danh sách Products và Categories.
  > 3. Transactional: Thêm sản phẩm mới sử dụng dữ liệu tham số hóa từ products.csv, sau đó gọi DELETE dọn dẹp sản phẩm vừa tạo để tránh rác cơ sở dữ liệu."*

---

### 📌 Phần 3: Chạy Thực tế 3 Kịch bản & Quan sát `htop` (Phút 2:30 - 5:00)
- **Hành động**: Gõ `cd src && ./run_tests.sh`. Chỉ chuột vào cửa sổ `htop` bên phải khi từng kịch bản chạy qua.
- **Lời nói mẫu**:
  > *- **Khi chạy Load Test (10 threads)**: "Đầu tiên là Load Test với 10 virtual users, ramp-up 10 giây. Nhìn sang cửa sổ htop bên phải, mức sử dụng CPU tăng nhẹ khoảng 15%, thời gian phản hồi trung bình chỉ 10ms, hệ thống xử lý rất ổn định."*
  > *- **Khi chạy Stress Test (50 threads)**: "Tiếp theo là Stress Test với 50 virtual users, ramp-up 15 giây. Quan sát htop, các nhân CPU nhảy lên mức 40-50%, throughput đạt 39.3 RPS, không có request nào bị lỗi."*
  > *- **Khi chạy Spike Test (100 threads)**: "Cuối cùng là Spike Test với 100 virtual users đổ ập vào trong 1 giây. CPU vọt đỉnh tức thì, throughput đạt đỉnh 338.2 RPS. Độ trễ trung bình tăng lên 225ms nhưng tỷ lệ lỗi vẫn là 0%."*

---

### 📌 Phần 4: Tổng kết, Phân tích AI & Đề xuất CI/CD Pipeline (Phút 5:00 - 6:30+)
- **Hành động**: Mở file `src/report/main-report.md`.
- **Lời nói mẫu**:
  > *"Em đã thu thập các file raw.jtl và sinh báo cáo HTML report. Về phần phân tích AI (Task 2), em phát hiện AI thường mắc lỗi nhầm lẫn giữa Average Latency và 95th Percentile Latency, cũng như đề xuất ảo giác việc dựng Redis Cluster cho SQLite đĩa đơn. Về Task 3, em đề xuất pipeline CI/CD kiểm thử hiệu năng tự động trên GitHub Actions với sơ đồ Mermaid. Em xin kết thúc phần demo. Em cảm ơn thầy đã theo dõi."*

---

## 📤 4. Hướng Dẫn Đăng Video Lên YouTube Unlisted

1. Truy cập [YouTube Studio](https://studio.youtube.com/).
2. Nhấp **Tải video lên (Upload Video)** và chọn file video vừa quay.
3. Tại bước **Quyền truy cập (Visibility)**, chọn **Không công khai (Unlisted)**.
4. Sao chép đường link video (dạng `https://youtu.be/...`).
5. Dán đường link video vào 2 file:
   - File `src/README.md` (mục 3)
   - File `src/report/main-report.md` (mục 1.4)
