# Báo cáo nhật ký sử dụng AI

## Tuyên bố

I use AI tools for the following tasks: lập bản đồ endpoint, thiết kế workload/test plan, sinh XML JMeter, review correlation/assertion, thiết kế script phân tích JTL, đề xuất threshold, lập checklist human review và đề xuất kiểm thử hiệu năng liên tục.

## Nhật ký tương tác

| # | Công cụ | Ngày giờ (Asia/Ho_Chi_Minh) | Prompt / thao tác | Output và review của người |
| ---: | --- | --- | --- | --- |
| 1 | Codex | 2026-08-29 09:10 | Đọc `plan/plan.md` và đề tiếng Việt; lập danh sách deliverable và ràng buộc. | Xác định phạm vi; đối chiếu thủ công với đề. |
| 2 | Codex | 2026-08-29 10:05 | Review API specification và backend EShop cho workflow được chọn. | Phát hiện gap lockout, pagination, cart và checkout; giữ evidence thật riêng. |
| 3 | Codex | 2026-08-29 14:20 | Sinh ba JMeter plan có workflow dùng chung, CSV và report view riêng cho từng kịch bản. | Human review phát hiện lỗi dùng chung CSV làm sai lifecycle; chuyển sang CSV riêng từng VU. |
| 4 | Codex analyzer | 2026-08-30 09:40 | Phân tích từng JTL thô theo label, tự tính percentile và phân loại failure. | Tính lại 4 JTL chính thức: HTTP error `0%`; failure là assertion cart sau checkout. JSON nằm trong `report/metrics-20260830/`. |
| 5 | Codex + human review | 2026-08-30 11:15 | Đề xuất tối ưu và phân loại claim theo mức bằng chứng. | Chỉ chấp nhận hành động có căn cứ contract/implementation; loại monitor cũ, rerun đủ 4 workload với CPU/RSS/thread hợp lệ. |
| 6 | Codex + human review | 2026-08-30 13:05 | Kiểm tra package theo acceptance checklist và dịch tài liệu sang tiếng Việt. | Bổ sung summary, threshold, hardware screenshot, ảnh kết hợp, issue evidence và sửa tài liệu stale. |

## Checklist review của người

- [x] Không bịa JTL, ảnh, video, metric hoặc issue.
- [x] Mỗi VU dùng tài khoản riêng và lifecycle CSV riêng.
- [x] Lockout probe tách khỏi positive run và có hướng dẫn reset.
- [x] Listener không được dùng làm số đo non-GUI chính thức.
- [x] Tách lỗi transport/HTTP khỏi assertion lỗi nghiệp vụ.
- [x] Metric truy nguyên được về JTL thô.
- [x] Khuyến nghị tối ưu được phân loại theo bằng chứng implementation/profiling.
- [x] Có ảnh JMeter, Activity Monitor, hardware và GitHub Issue evidence.
- [ ] Video demo vẫn chờ sinh viên tự quay và thêm link.
