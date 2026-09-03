# AI Critique - Phê Bình Phân Tích AI (HW05)

- **Họ và tên**: Lê Trung Kiên
- **MSSV**: 23127075
- **Thành viên**: 4

AI giúp tạo nhanh cấu trúc JMeter, script chạy và khung báo cáo nhưng đầu ra ban đầu có sai sót. AI mô tả Gaussian Random Timer như khoảng chặn cứng 1-3 giây, trong khi JMeter cấu hình trung bình và độ lệch chuẩn. AI đặt ID sản phẩm trong sampler label, làm HTML report sinh hàng nghìn nhãn. Khi đọc kết quả, AI dùng response time trung bình để đại diện trải nghiệm người dùng nhưng bỏ qua p95, đồng thời gọi throughput trung bình của lượt chạy là throughput đỉnh.

AI không phát hiện vì chỉ suy luận từ bảng tóm tắt, không kiểm tra ngữ nghĩa JMeter hoặc đối chiếu raw JTL với `statistics.json`. Dữ liệu Spike từng bị nối thành 14.400 mẫu trong khi HTML chỉ có 1.800 mẫu; nhìn riêng từng artifact vẫn dễ dẫn đến kết luận sai. AI còn đề xuất Redis cluster và Nginx cho backend Node.js dùng SQLite, vượt quá phạm vi bài tập.

Tôi giữ đề xuất index `users(email)` và cân nhắc SQLite WAL, nhưng loại index cho `products(id)` vì cột này đã là khóa chính. Bài học là sinh viên phải sở hữu phép đo: dọn output trước mỗi run, kiểm tra tổng mẫu, phân biệt `elapsed` với `Latency`, tính percentile bằng script và chỉ báo cáo CPU/RSS từ dữ liệu thật. Human-in-the-loop là quá trình tái lập, phản biện và sửa bằng bằng chứng.
