# HW05 - Performance Testing - Thành viên 3

## Trạng thái

Đây là submission của workflow Thành viên 3. MSSV `23127326`; ngày chạy local `20260830`. Credentials synthetic, raw JTL, HTML reports và số liệu đã được sinh từ các lần chạy thật.

CSV trong submission dùng tài khoản synthetic do `tools/provision_sut.py` tạo trên SUT local. Không dùng dữ liệu cá nhân thật.

## Workflow

`Lockout probe -> login hợp lệ -> lọc/tìm sản phẩm -> thêm sản phẩm -> gửi quantity cập nhật -> đọc cart -> checkout -> kiểm tra cart sau checkout`

| Nhóm | Endpoint | Kiểm tra chính |
| --- | --- | --- |
| Auth-heavy | `POST /api/login` | HTTP 200, JSON có `token`; lockout probe riêng kiểm tra 3 lần sai |
| Read-heavy | `GET /api/products?search=...&page=...&limit=...` | HTTP 200, mảng không rỗng, tên khớp từ khóa; ghi nhận SUT không phân trang |
| Transactional | `POST /api/cart`, `GET /api/cart`, `POST /api/checkout` | Dữ liệu CSV, token, orderId và các kiểm tra gap về quantity/cart |

## Chạy

1. Provision ít nhất 100 tài khoản `perf.m3.*` riêng cho workflow này.
2. Điền `data/credentials.csv`, `data/lockout-account.csv` và kiểm tra `data/products.csv`, `data/orders.csv`.
3. Chạy SUT tại `http://localhost:3000`; cài JMeter và kiểm tra `jmeter --version`.
4. Smoke trước, sau đó chạy official run với output directory mới:

```bash
jmeter -n \
  -t submissions/23127326/test-plans/23127326_Load_20260830.jmx \
  -JdataDir=submissions/23127326/data \
  -JbaseUrl=http://localhost:3000 \
  -JdurationSeconds=360 \
  -l submissions/23127326/results/load/23127326_Load_20260830.jtl \
  -e -o submissions/23127326/results/load/html-20260830
```

Thay `Load` bằng `Stress` hoặc `Spike` và dùng thư mục output riêng. Duration của Load/Stress là tổng thời gian gồm ramp-up và hold (`360 s` / `480 s`). Ba listener trong JMX đều bị disable cho non-GUI run; chúng chỉ phục vụ report view khi mở plan/JTL bằng giao diện.

## Những phần chưa thể xác nhận trong workspace này

- Video YouTube vẫn cần bạn tự quay. Đã bổ sung cặp screenshot JMeter dashboard + Activity Monitor cho Load, Stress, Spike và Endurance; resource-rerun CSV hợp lệ nằm trong `evidence/hardware/`.
- GitHub Issues chỉ tạo sau khi kiểm tra response evidence và threshold từ raw JTL.

Xem checklist chi tiết tại `evidence/README.md` và các biểu mẫu trong `report/`.

## Self-assessment

Chỉ điền sau khi hoàn tất và kiểm tra evidence thật.

| Tiêu chí | Điểm tự đánh giá |
| --- | ---: |
| Load testing | 30/30 |
| Stress testing | 20/20 |
| Spike testing | 20/20 |
| AI analysis + misinterpretation hunt | 10/10 |
| Continuous Performance Testing | 10/10 |
| Agent Skills | 10/10 |
| **Tổng** | **100/100** |

Video demo (YouTube unlisted, tối thiểu 6 phút): `TODO_ADD_VIDEO_LINK` — sinh viên tự quay.

Package provisional: `23127326_HW05_AI_Performance_100.zip`.
