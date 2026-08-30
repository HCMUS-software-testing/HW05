# Đề xuất kiểm thử hiệu năng liên tục

```mermaid
flowchart TD
    A[Commit / Pull Request] --> B{Có thay đổi file backend?}
    B -- Không --> C[Bỏ qua performance run; tiếp tục unit/integration test]
    B -- Có --> D[Khởi động SUT sạch và database test cô lập]
    D --> E[Smoke: 1 VU, 1 iteration]
    E --> F{Smoke đạt?}
    F -- Không --> G[Fail check và tải log]
    F -- Có --> H{Loại lần chạy}
    H -- PR --> I[Load ngắn]
    H -- Hàng đêm --> J[Load + Stress + Spike đầy đủ]
    H -- Hàng tuần --> K[Endurance 10-15 phút]
    I --> L[Phân tích JTL thô và so baseline]
    J --> L
    K --> L
    L --> M{p95 > baseline +20% và +100 ms, hoặc error rate +1 điểm %?}
    M -- Không --> N[Đăng báo cáo và artifacts]
    M -- Có --> O[Chạy lại tối đa 3 lần trong môi trường cô lập]
    O --> P{Regression lặp lại ít nhất 2/3 lần?}
    P -- Không --> Q[Đánh dấu flaky / điều tra; không chặn]
    P -- Có --> R[Đánh dấu regression và yêu cầu review]
```

## Mô hình vận hành

- Pull Request: smoke và Load ngắn để phản hồi nhanh.
- Hàng đêm: chạy đầy đủ Load, Stress và Spike với fixture mới.
- Hàng tuần: Endurance tại 70% mức concurrency cao nhất đã duy trì ổn định.
- Lưu cùng nhau JTL thô, báo cáo HTML, phiên bản JMeter, commit SUT, phiên bản fixture và bằng chứng monitor tài nguyên.
- So sánh theo label và kịch bản ổn định. Tách assertion lỗi nghiệp vụ đã biết khỏi lỗi transport/HTTP.

## Đánh đổi

Runner self-hosted tốn thêm thời gian khi chạy Stress, Spike và Endurance. Runner local giảm chi phí cloud nhưng chịu nhiễu CPU, memory, tiến trình nền và trạng thái database. Database SQLite sạch giúp lặp lại tốt hơn nhưng có thể khác dữ liệu production. Ngưỡng p95 có thể tạo cảnh báo sai khi số mẫu nhỏ, vì vậy pipeline chạy lại và yêu cầu tái hiện trong 2/3 lần. Lưu JTL và HTML giúp audit nhưng tốn dung lượng; giữ đầy đủ artifact khi fail và rút ngắn thời gian lưu khi nightly pass. Baseline phải được version cùng tham số tải, nếu không thay đổi workload có thể bị hiểu nhầm là regression.
