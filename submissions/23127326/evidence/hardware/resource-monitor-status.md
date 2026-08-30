# Resource-monitor status

Các lần chạy chính thức đầu tiên dùng `ps -o %cpu=,rss=,thcount=`. macOS không cung cấp `thcount`, vì vậy bốn CSV chính thức cũ chỉ có header và không phải evidence CPU/RSS hợp lệ.

`tools/monitor_backend.py` đã được sửa để đọc CPU/RSS và đếm thread bằng `ps -M`. Bản sửa được xác nhận với tiến trình Node thật trong `monitor-pid-check-20260830-v6.csv`. Đây chỉ là kiểm tra tool, không phải kết quả workload; không dùng file cũ để kết luận CPU/RSS cho Load, Stress, Spike hoặc Endurance.

Đã rerun mỗi workload bằng monitor macOS đã sửa. CSV hợp lệ nằm tại `backend-*-resource-20260830.csv`; ảnh Activity Monitor/JMeter nằm trong `evidence/screenshots/`. Ảnh hardware-spec là `hardware-20260830.png`.
