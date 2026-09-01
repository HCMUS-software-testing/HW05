# AI Critique - Phê Bình Phân Tích AI (HW05)

- **Họ và tên**: Lê Trung Kiên
- **MSSV**: 23127075
- **Thành viên**: 4

 Trong quá trình thực hiện bài tập kiểm thử hiệu năng HW05, công cụ AI (Gemini / ChatGPT) đã thể hiện khả năng vượt trội trong việc sinh nhanh cấu hình kịch bản JMeter (`.jmx`) và tổng hợp khung báo cáo Markdown. Tuy nhiên, khi đi sâu vào phân tích dữ liệu hiệu năng thực tế từ file log thô (`.jtl`), AI bộc lộ nhiều hạn chế nghiêm trọng. AI dễ bị ảo giác (hallucination) khi đọc các bảng dữ liệu phức tạp, thường xuyên nhầm lẫn giữa giá trị trung bình (Average Latency) và điểm bách phân thứ 95 (p95 Latency), đồng thời không phân biệt được lỗi hệ thống thật (HTTP 500) với các lỗi do dữ liệu đầu vào cố ý test sai (HTTP 401/404).

Nguyên nhân chính là do model AI xử lý dữ liệu dựa trên xác suất chuỗi văn bản thay vì thực sự chạy phép tính thống kê trên các log điểm thời gian thô. AI cũng thiếu ngữ cảnh về môi trường thực thi (chẳng hạn như việc EShop backend sử dụng SQLite đĩa đơn trên máy cá nhân), dẫn đến việc đưa ra các đề xuất tối ưu hóa xa rời thực tế như yêu cầu dựng cluster Redis phức tạp.

Bài học quan trọng nhất rút ra về nguyên tắc cộng tác với AI là: **AI chỉ đóng vai trò trợ lý tăng tốc (Accelerator), không thể thay thế tư duy phản biện và rà soát của con người (Human-in-the-loop)**. Kỹ sư kiểm thử luôn phải là người sở hữu dữ liệu thô, tự mình đối chiếu từng con số trong log `.jtl` và chịu trách nhiệm hoàn toàn về tính chính xác của kết quả báo cáo cuối cùng.
