# Resource-monitor status

The first official runs used `ps -o %cpu=,rss=,thcount=`. macOS does not provide `thcount`, so the four official CSV files contain headers only and are not valid CPU/RSS evidence.

`tools/monitor_backend.py` is fixed to read CPU/RSS and count threads with `ps -M`. The fix was validated with a real Node process in `monitor-pid-check-20260830-v6.csv`. That check is tool validation only, not a workload result; no CPU/RSS conclusion is assigned to Load, Stress, Spike or Endurance.

Đã rerun mỗi workload bằng monitor macOS đã sửa. CSV hợp lệ nằm tại `backend-*-resource-20260830.csv`; ảnh Activity Monitor/JMeter nằm trong `evidence/screenshots/`. Ảnh hardware-spec là `hardware-20260830.png`.
