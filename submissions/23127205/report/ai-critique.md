# Phê Bình Năng Lực AI trong Kiểm Thử Hiệu Năng (AI Critique)

**Học viên:** Lâm Hữu Khánh — **MSSV:** 23127205 (Thành viên 1)
**Bài tập:** HW05-AI — Performance Testing | EShop Backend SUT

---

### Bài viết Phê bình (200 – 300 từ)

Trong quá trình thực hiện bài tập kiểm thử hiệu năng HW05, mô hình AI (Claude 3.5 / Gemini 3.7) đã bộc lộ nhiều điểm sai lệch toán học, định kiến kỹ thuật và ảo giác nghiêm trọng. Cụ thể, khi phân tích tệp dữ liệu thô `.jtl`, AI đã phạm sai lầm sơ đẳng khi tính phân vị p95 tổng thể bằng trung bình cộng các phân vị thành phần (5.2 ms thay vì giá trị phân vị gộp chính xác là 6.0 ms), vi phạm nguyên lý phi cộng tính (non-additivity) của phân vị thống kê. Ngoài ra, AI liên tục võ đoán nguyên nhân nghẽn Throughput là do "băng thông mạng" trong khi hệ thống đang chạy cục bộ trên Loopback Interface (127.0.0.1), đồng thời bịa đặt hiện tượng rớt gói 2–5% dù số liệu thực nghiệm ghi nhận 0.00% lỗi. Thậm chí, AI còn đề xuất cấu hình "Connection Pool 50 connections" cho SQLite — một ảo giác phi thực tế đối với cơ sở dữ liệu tệp nhúng.

Nguyên nhân chính khiến AI thất bại bắt nguồn từ bản chất mô hình ngôn ngữ lớn: AI chỉ suy luận dựa trên xác suất văn bản từ dữ liệu huấn luyện phổ quát trên Internet thay vì hiểu được ngữ cảnh triển khai phần cứng thực tế và bản chất kiến trúc của SUT. Khi gặp các chỉ số tải cao, AI có xu hướng áp đặt thiên kiến tiêu cực thông thường mà không thực thi các phép tính thống kê nghiêm ngặt trên toàn bộ tập dữ liệu.

Bài học cốt lõi tôi rút ra khi cộng tác với AI là: **"Ground Truth là chân lý duy nhất trong Performance Testing"**. AI chỉ đóng vai trò là một trợ lý sinh dàn ý và tăng tốc viết script; mọi kết luận phân tích, quyết định kiến trúc và số liệu đo đạc bắt buộc phải do con người (Human-in-the-Loop) trực tiếp xác minh định lượng bằng các công cụ trích xuất dữ liệu toán học đáng tin cậy.
