# Hướng Dẫn Chụp Ảnh Màn Hình Bằng Chứng (Screenshot Guide)

Tài liệu này hướng dẫn chi tiết cách chụp ảnh màn hình đáp ứng 100% yêu cầu trong file đề bài (`req/2026.HW05.Performance Testing_Vi.md`).

---

## 📸 1. Danh Sách & Số Lượng Ảnh Cần Chụp

Bạn cần chụp tổng cộng **4 tấm ảnh** và lưu vào đúng các thư mục chỉ định trong `src/evidence/`:

| STT | Tên file ảnh | Vị trí lưu | Nội dung cần chụp | Thời điểm chụp |
|---|---|---|---|---|
| 1 | `fastfetch.png` | `src/evidence/hardware/` | Màn hình Terminal chạy lệnh `fastfetch` | Trước khi chạy test (Bất kỳ lúc nào) |
| 2 | `htop_load.png` | `src/evidence/screenshots/` | Màn hình Terminal chạy `htop` | Khi chạy **Load Test** (10 threads) |
| 3 | `htop_stress.png` | `src/evidence/screenshots/` | Màn hình Terminal chạy `htop` | Khi chạy **Stress Test** (50 threads) |
| 4 | `htop_spike.png` | `src/evidence/screenshots/` | Màn hình Terminal chạy `htop` | Khi chạy **Spike Test** (100 threads) |

---

## 🔍 2. Hướng Dẫn Chi Tiết Cho Từng Loại Ảnh

### 🔹 Ảnh 1: Thông số phần cứng (`src/evidence/hardware/fastfetch.png`)
- **Cách thực hiện**:
  1. Mở Terminal gõ lệnh:
     ```bash
     fastfetch
     ```
     *(Nếu máy chưa có `fastfetch`, dùng `screenfetch` hoặc `neofetch`)*.
  2. Chụp toàn bộ cửa sổ Terminal đó.
- **Thông số cần chú ý trong ảnh**:
  - **OS**: Fedora
  - **Host / CPU**: Số nhân/luồng CPU
  - **Memory**: Dung lượng RAM tổng

---

### 🔹 Ảnh 2, 3, 4: Giám sát tài nguyên `htop` (`src/evidence/screenshots/`)

Vì `htop` là giao diện CLI (dòng lệnh) như trong ảnh màn hình của bạn, hãy làm theo các bước sau để ảnh chụp trực quan nhất:

#### 💡 Mẹo chuẩn bị `htop` trước khi bấm chạy test:
1. Mở một cửa sổ Terminal riêng dành cho `htop`.
2. Gõ lệnh: `htop`
3. Nhấn phím **`F4`** (Filter), gõ từ khóa `node` (hoặc `jmeter`). `htop` sẽ tự động lọc hiển thị đúng tiến trình Node.js Backend đang xử lý API.
4. Mở cửa sổ Terminal thứ 2 bên cạnh để sẵn sàng gõ `./run_tests.sh`.

---

#### ⏱️ Thời điểm & Thông số cần chụp cho từng kịch bản:

#### 1. Kịch bản Load Test (`htop_load.png`)
- **Thời điểm chụp**: Khoảng giây thứ 15–30 khi script đang ở bước `🚀 1/3 Running Load Test`.
- **Thông số cần chú ý trong ảnh `htop`**:
  - Thanh **CPU [0..15]**: Sử dụng mức thấp-trung bình ($\approx 10\% - 25\%$).
  - **Mem**: Tăng nhẹ ($\approx 1.5GB - 2GB$).
  - Tiến trình `node /usr/.../server.js`: Đang chạy mượt mà.

#### 2. Kịch bản Stress Test (`htop_stress.png`)
- **Thời điểm chụp**: Khoảng giây thứ 20–40 khi script đang ở bước `🚀 2/3 Running Stress Test` (50 threads đồng thời).
- **Thông số cần chú ý trong ảnh `htop`**:
  - Thanh **CPU [0..15]**: Nhiều nhân nhảy lên màu đỏ/xanh lá cao hơn ($\approx 30\% - 60\%$).
  - **Load average**: Giá trị 1 min tăng lên (ví dụ: `2.43 1.83 1.38` như ảnh mẫu của bạn).
  - **MEM%** của tiến trình `node`: Nhích lên.

#### 3. Kịch bản Spike Test (`htop_spike.png`)
- **Thời điểm chụp**: Ngay lập tức trong 3-5 giây đầu tiên khi script ở bước `🚀 3/3 Running Spike Test` (100 threads dồn dập trong 1s).
- **Thông số cần chú ý trong ảnh `htop`**:
  - Thanh **CPU**: Bị đẩy vọt đỉnh tức thì (Spike) trên nhiều nhân.
  - **Tasks / threads**: Số lượng threads hoạt động đạt cực đại.

---

## 🛠️ 3. Thao Tác Chụp Ảnh Trên Fedora Linux

- **Chụp 1 cửa sổ Terminal**: Nhấn `Alt + PrintScreen` (hoặc mở phần mềm **Take Screenshot** / **Gnome Screenshot**).
- **Chụp vùng chọn**: Nhấn `Shift + PrintScreen`.
- Lưu đúng định dạng `.png` vào các đường dẫn:
  - `src/evidence/hardware/fastfetch.png`
  - `src/evidence/screenshots/htop_load.png`
  - `src/evidence/screenshots/htop_stress.png`
  - `src/evidence/screenshots/htop_spike.png`
