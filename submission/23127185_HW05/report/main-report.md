# Báo cáo kiểm thử hiệu năng HW05

## Sinh viên và phạm vi

- Sinh viên: Mai Thị Kim Duyên
- MSSV: 23127185
- Vai trò: Thành viên 2
- SUT: backend EShop cục bộ tại `http://localhost:3000`
- Workflow: đăng ký người dùng mới -> đăng nhập -> duyệt danh mục -> xem/tìm kiếm sản phẩm -> xem chi tiết -> thêm vào giỏ hàng -> áp dụng `SAVE10` -> checkout -> xem lịch sử đơn hàng.

Cùng một workflow được thực thi bằng ba JMeter plan chính thức; Agent Skill runner được dùng thêm để kiểm tra khả năng tái sử dụng và phân tích. Lần chạy đầu phát hiện lỗi đặt token extractor, sau đó cây JMX được sửa và chạy lại thành công.

## Ánh xạ API

| Nhóm | Endpoint | Assertion |
|---|---|---|
| Auth-heavy | `POST /api/register`, `POST /api/login` | 200, phản hồi đăng ký, JWT token |
| Read-heavy | `GET /api/categories`, `GET /api/products?search=i`, `GET /api/products/1` | 200 và dữ liệu JSON |
| Transactional | `POST /api/cart`, `POST /api/apply-coupon`, `POST /api/checkout`, `GET /api/orders/my-orders` | 200 và phản hồi giỏ hàng/mã giảm giá/đơn hàng |

## Mô hình tải

| Kịch bản | Cấu hình sử dụng | Samples |
|---|---|---:|
| Load | JMeter: 10 người dùng, ramp-up 5 giây, duration 30 giây | 90 |
| Stress | JMeter: 10 người dùng, ramp-up 5 giây, duration 60 giây | 90 |
| Spike | JMeter: 10 người dùng, ramp-up 5 giây, duration 10 giây | 90 |
| Soak | 2 worker đồng thời trong 600 giây | 278.460 |

Runner sử dụng email đăng ký duy nhất cùng dữ liệu sản phẩm/mã giảm giá từ CSV. Runner ghi lại samples thô và không sửa dữ liệu sau khi thực thi.

## Kết quả từ JTL thô

| Kịch bản | Samples | Tỷ lệ lỗi | Trung bình (ms) | Trung vị (ms) | P95 (ms) | P99 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| Load | 90 | 0% | 9.34 | 1 | 51 | 59 |
| Stress | 90 | 0% | 2.00 | 1 | 12 | 13 |
| Spike | 90 | 0% | 2.51 | 1 | 13 | 14 |
| Soak | 278,460 | 0% | 4.05 | 2 | 7 | 49 |

Đây là kết quả trên kết nối loopback cục bộ, không phải năng lực production. Không được suy rộng kết quả này cho môi trường mạng hoặc triển khai nhiều node.

## Phát hiện khi rà soát thủ công

Bản nháp JMeter do AI sinh cần được sửa. Ban đầu extractor nằm ngoài hash tree của sampler Login nên các request cần xác thực nhận 401. Sau khi sửa cây JMX và chạy khi backend đang hoạt động, ba JTL chính thức đều có 90 mẫu và 0% lỗi. Ba thư mục báo cáo HTML chính thức tại `jmeter/reports/load`, `jmeter/reports/stress` và `jmeter/reports/spike` đã được sinh thành công từ các file `.jtl` có đầy đủ header. Cả ba báo cáo đều hiển thị chính xác 90 mẫu (samples) và 0% lỗi, khớp 100% giữa log `.jtl` thô, file `statistics.json` và giao diện Dashboard Report.

Rà soát source cũng phát hiện lỗi trong SUT: đăng nhập thất bại tăng số lần thử thêm 2 thay vì 1 và khóa 180 giây thay vì 30 giây; kiểm tra ngưỡng mã giảm giá dùng `>` thay vì `>=`; công thức giảm phần trăm sai; `apply-coupon` không có middleware xác thực; checkout chấp nhận `total_amount` từ client mà không tính lại tổng giỏ hàng. Đây là phát hiện về triển khai, không phải lỗi hiệu năng được bịa ra.

## Ngưỡng endurance

Trong lần chạy MVP cục bộ này, mức ổn định quan sát được là 2 worker đồng thời trong 599,935 giây: 278.460 samples, 0% lỗi, P95 7 ms và P99 49 ms. Đây là ngưỡng quan sát trên máy kiểm thử, không phải cam kết cấp dịch vụ. Bằng chứng CPU/RAM phải đi kèm các ảnh chụp thủ công được liệt kê trong `evidence/manual-evidence-needed.md`.

Ba JMeter plan hiện đều dùng 10 user; khác biệt chính là thời lượng 30/60/10 giây. Vì vậy kết quả hiện tại chỉ là baseline/MVP cho workflow, chưa đủ để kết luận ngưỡng chịu tải hay spike capacity. Muốn báo cáo stress/spike đúng nghĩa cần tăng số user theo từng nấc và chạy lại JTL, HTML report cùng evidence.

## Đề xuất kiểm thử hiệu năng liên tục

Sau mỗi commit: phát hiện route backend thay đổi -> chạy smoke workflow trong 1 phút -> so sánh tỷ lệ lỗi và P95 với baseline -> chạy Load trên pull request -> chạy Stress/Spike hằng đêm -> cảnh báo khi P95 tăng trên 20% hoặc xuất hiện lỗi chức năng. Lưu JTL làm artifact và rà soát nhiễu môi trường trước khi tạo issue hiệu năng.
