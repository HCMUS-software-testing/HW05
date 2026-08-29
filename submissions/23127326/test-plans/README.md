# JMeter test plans

Các file `.jmx` được sinh từ `generate_plans.py` để tránh ba scenario lệch workflow. Ngày chạy local hiện là `20260830`; đổi `23127326` theo MSSV trước khi nộp.

| Plan | Tải mặc định | Report view riêng |
| --- | --- | --- |
| `23127326_Load_20260830.jmx` | 20 VU, ramp 60 s, giữ 300 s (duration tổng 360 s) | View Results Tree |
| `23127326_Stress_20260830.jmx` | 100 VU, ramp 300 s, giữ 180 s (duration tổng 480 s) | Summary Report |
| `23127326_Spike_20260830.jmx` | nền 10 VU/420 s; spike 90 VU sau 120 s, ramp 5 s, giữ 120 s | Aggregate Report |

Override được bằng `-Jthreads`, `-JrampSeconds`, `-JdurationSeconds`, `-JbackgroundThreads`, `-JspikeThreads`, `-JspikeDelaySeconds`, `-JspikeDurationSeconds`, `-JbaseUrl`, `-JdataDir`, `-JthinkMinMs`, `-JthinkMaxMs`.

`LOCKOUT_PROBE` là thread group disabled mặc định. Chạy probe riêng sau khi reset account; không trộn kết quả probe vào official positive performance run.
