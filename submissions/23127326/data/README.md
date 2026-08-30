# Dữ liệu kiểm thử

`credentials.csv` chứa 100 dòng tài khoản kiểm thử khác nhau, được tạo trên SUT local ngoài thời gian đo. Mật khẩu chỉ dùng cho kiểm thử; không thay bằng mật khẩu cá nhân.

`products.csv` và `orders.csv` chứa dữ liệu đầu vào kiểm thử. JMX lấy `search`, `page`, `limit`, số lượng và địa chỉ từ CSV, nhưng trích xuất `id`, `name`, `price` của sản phẩm từ response thật trước khi tạo request cart/checkout. Các cột `product_id`, `product_name`, `price` chỉ là dữ liệu fixture để review, không phải giá trị correlation đáng tin cậy.

`lockout-account.csv` chỉ được dùng bởi thread group negative-path đang tắt. Reset tài khoản giữa các kịch bản bằng SQL trong `../report/main-report.md`.
