# Danh sách kiểm tra bằng chứng

Chỉ đặt bằng chứng sinh từ lần chạy thật vào các thư mục con; không dùng ảnh hoặc log của thành viên khác.

- `screenshots/`: ảnh kết hợp JMeter/terminal và Activity Monitor trong cùng khung hình cho Load, Stress, Spike, Endurance.
- `hardware/`: ảnh thông số phần cứng/hostname và bảng CPU/RAM/OS; CSV CPU/RSS/thread của backend.
- `issues/`: ảnh GitHub Issue và bằng chứng response cho lỗi đã tái hiện.
- Video YouTube không công khai, tối thiểu 6 phút, phải do sinh viên tự quay và thuyết minh tiếng Việt.

Đã thay ba ảnh combined Stress/Spike/Endurance bằng screenshot thật trong cùng phiên thực thi. Stress hiển thị backend PID `31159`; Spike hiển thị PID `35179`; Endurance hiển thị PID `54267` và tải `Active: 200`. PID đều khớp giữa terminal và Activity Monitor.

## Evidence còn phải bổ sung

- [ ] Chụp lại Load khi JMeter đang chạy, có `Active`, backend PID và Activity Monitor trong cùng khung hình.
- [ ] Sau khi chạy non-GUI, mở JTL bằng report view tương ứng và chụp ba ảnh: Load/View Results Tree, Stress/Summary Report, Spike/Aggregate Report.
- [ ] Quay video không công khai tối thiểu 6 phút, có thuyết minh tiếng Việt và phần minh họa Agent Skill end-to-end.

CSV resource hợp lệ của lần chạy lại nằm trong `hardware/backend-*-resource-20260830.csv`. Staircase/soak bổ sung ghi CSV theo từng mức tại `hardware/staircase-20260830/`.

Đã có 4 lỗi được tái hiện và ghi nhận trên GitHub Issues #1-#4; ảnh trang issue nằm trong thư mục `issues/`.

Ảnh hardware-spec: `hardware/hardware-20260830.png`; file text đã che serial/UUID nhạy cảm.

Tên gợi ý: `23127326_Load_YYYYMMDD_jmeter-activity-monitor.png`, tương tự Stress/Spike/Endurance.
