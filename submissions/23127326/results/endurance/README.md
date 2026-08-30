# Kết quả Endurance

Lần chạy canonical cũ: `../resource-rerun/endurance/23127326_Endurance_resource_20260830.jtl` + `../resource-rerun/endurance/html-20260830/`. 70 VU; ramp 210 s; giữ tải 600 s; tổng 810 s. Có 24.574 mẫu; lỗi HTTP 0%; 2.699 assertion lỗi nghiệp vụ sau checkout. Thông lượng 30.4315 mẫu/s, tương đương 23.6465 HTTP RPS; p95 6 ms; CPU tối đa 19,6%; RSS tối đa 85,6 MB; tối đa 11 thread.

Ngưỡng thay thế nằm tại `../staircase-20260830/endurance-200vu/`: 200 VU, ramp 120 s, giữ tải 600 s, 77.4400 HTTP RPS trong hold, p95 5 ms, HTTP error 0%, CPU tối đa 17,7%, RSS tối đa 119,3 MB. JTL và HTML trong thư mục hiện tại chỉ giữ để audit.
