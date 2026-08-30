# HW05 - Kiểm thử hiệu năng - Thành viên 3

## Trạng thái

Đây là bài nộp workflow của Thành viên 3. MSSV `23127326`; ngày chạy local `2026-08-30`. Tài khoản kiểm thử, JTL thô, báo cáo HTML và số liệu đều được sinh từ các lần chạy thật.

Các CSV dùng tài khoản kiểm thử do `tools/provision_sut.py` tạo trên SUT local. Không dùng dữ liệu cá nhân thật.

Kho GitHub công khai: `https://github.com/HB4305/23127326-HW05-AI-Performance`

## Quy trình

`Lockout probe -> login hợp lệ -> lọc/tìm sản phẩm -> thêm sản phẩm -> gửi quantity cập nhật -> đọc cart -> checkout -> kiểm tra cart sau checkout`

| Nhóm | Endpoint | Kiểm tra chính |
| --- | --- | --- |
| Auth-heavy | `POST /api/login` | HTTP 200, JSON có `token`; lockout probe riêng kiểm tra 3 lần sai |
| Read-heavy | `GET /api/products?search=...&page=...&limit=...` | HTTP 200, mảng không rỗng, tên khớp từ khóa; ghi nhận SUT không phân trang |
| Transactional | `POST /api/cart`, `GET /api/cart`, `POST /api/checkout` | Dữ liệu CSV, token, orderId và các kiểm tra gap về quantity/cart |

## Cách chạy

1. Tạo ít nhất 100 tài khoản `perf.m3.*` riêng cho workflow này.
2. Điền `data/credentials.csv`, `data/lockout-account.csv` và kiểm tra `data/products.csv`, `data/orders.csv`.
3. Chạy SUT tại `http://localhost:3000`; cài JMeter và kiểm tra `jmeter --version`.
4. Chạy smoke trước, sau đó chạy lần đo chính thức với thư mục output mới:

```bash
jmeter -n \
  -t submissions/23127326/test-plans/23127326_Load_20260830.jmx \
  -JdataDir=submissions/23127326/data \
  -JbaseUrl=http://localhost:3000 \
  -JdurationSeconds=360 \
  -l submissions/23127326/results/load/23127326_Load_20260830.jtl \
  -e -o submissions/23127326/results/load/html-20260830
```

Thay `Load` bằng `Stress` hoặc `Spike` và dùng thư mục output riêng. Duration của Load/Stress là tổng thời gian gồm ramp-up và hold (`360 s` / `480 s`). Ba listener trong JMX được tắt khi chạy non-GUI; chúng chỉ dùng làm các dạng báo cáo khi mở plan/JTL bằng giao diện.

## Tóm tắt kết quả và ngưỡng endurance

| Kịch bản | VU | Thông lượng | p95 | HTTP/network | CPU backend tối đa | RSS tối đa |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Load | 20 | 9.1583 RPS | 6 ms | 0% | 16.4% | 75.8 MB |
| Stress | 100 | 34.4137 RPS | 5 ms | 0% | 17.4% | 120.8 MB |
| Spike | 10 + 90 | 17.1228 RPS | 5 ms | 0% | 25.5% | 90.5 MB |
| Endurance | 70 | 30.4315 RPS | 6 ms | 0% | 19.6% | 85.6 MB |

Điểm duy trì bền vững quan sát được: **70 VU, 30.4315 RPS trong 600 giây giữ tải**, p95 6 ms, CPU tối đa 19.6%, RSS tối đa 85.6 MB. Đây là điểm duy trì đã đo được, không khẳng định là giới hạn tối đa của phần cứng. Có 2 lỗi nghiệp vụ đã tái hiện và tạo GitHub Issue; 2 candidate khác được ghi riêng trong `report/issue-candidates.md`.

## Ghi chú bàn giao

- Video YouTube vẫn cần bạn tự quay và thêm link bên dưới.
- Mỗi kịch bản có ảnh JMeter và Activity Monitor; ảnh kết hợp cùng khung hình được lưu trong `evidence/screenshots/`.
- Evidence resource hợp lệ nằm trong `evidence/hardware/`; thông số phần cứng nằm trong `evidence/hardware/hardware-20260830.png` và file văn bản đi kèm.

Xem checklist chi tiết tại `evidence/README.md` và các biểu mẫu trong `report/`.

## Self-assessment

Chỉ điền sau khi hoàn tất và kiểm tra evidence thật.

| Tiêu chí | Điểm tự đánh giá |
| --- | ---: |
| Kiểm thử Load | 30/30 |
| Kiểm thử Stress | 20/20 |
| Kiểm thử Spike | 20/20 |
| Phân tích AI và săn lỗi diễn giải | 10/10 |
| Kiểm thử hiệu năng liên tục | 10/10 |
| Agent Skill | 10/10 |
| **Tổng** | **100/100** |

Video demo YouTube không công khai, tối thiểu 6 phút: `TODO_ADD_VIDEO_LINK` — sinh viên tự quay.

Gói nộp: `23127326_HW05_AI_Performance_100.zip`.
