# Resource-monitor status

Các lần chạy chính thức đầu tiên dùng `ps -o %cpu=,rss=,thcount=`. macOS không cung cấp `thcount`, vì vậy bốn CSV chính thức cũ chỉ có header và không phải evidence CPU/RSS hợp lệ.

`tools/monitor_backend.py` đã được sửa để đọc CPU/RSS và đếm thread bằng `ps -M`. Bản sửa được xác nhận riêng với tiến trình Node thật trước các lần chạy workload; các file kiểm tra tool đó không phải evidence workload và không dùng để kết luận CPU/RSS cho Load, Stress, Spike hoặc Endurance.

Đã rerun mỗi workload bằng monitor macOS đã sửa. CSV hợp lệ nằm tại `backend-*-resource-20260830.csv`; ảnh Activity Monitor/JMeter nằm trong `evidence/screenshots/`. Ảnh hardware-spec là `hardware-20260830.png`.

Thí nghiệm staircase 70/100/150/200 VU và soak 200 VU dùng cùng monitor đã sửa; mỗi CSV ghi backend PID `4341` và nằm trong `staircase-20260830/`. Soak ghi 709 mẫu monitor trong 720 giây lịch chạy (mỗi vòng gồm `ps` rồi mới đợi interval), CPU tối đa 17,7%, RSS đầu/đỉnh/cuối hold 118,8/119,3/109,3 MB. Ba ảnh combined same-screen ghi backend PID Stress/Spike/Endurance lần lượt `31159`/`35179`/`54267`; PID khớp giữa terminal và Activity Monitor. Ảnh Endurance được chụp khi JMeter hiển thị `Active: 200`.
