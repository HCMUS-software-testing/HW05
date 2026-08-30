# Staircase và Endurance threshold 2026-08-30

Backend PID `4341`; cùng một SUT sạch và 200 tài khoản riêng cho toàn bộ chuỗi. Screening tăng 70 -> 100 -> 150 -> 200 VU; mỗi bậc giữ tải 90 giây. Mức 200 VU sau đó được soak với ramp 120 giây và giữ tải 600 giây.

| Run | HTTP RPS trong hold | p95 tổng | HTTP error | CPU hold tối đa | RSS tối đa |
| --- | ---: | ---: | ---: | ---: | ---: |
| 70 VU | 26.4667 | 7 ms | 0% | 6.1% | 76.1 MB |
| 100 VU | 38.0778 | 7 ms | 0% | 8.5% | 87.4 MB |
| 150 VU | 56.8778 | 7 ms | 0% | 11.8% | 101.3 MB |
| 200 VU screening | 76.5222 | 6 ms | 0% | 13.7% | 118.2 MB |
| **200 VU endurance** | **77.4400** | **5 ms** | **0%** | **17.7%** | **119.3 MB** |

Ba cửa sổ hold của soak đạt 77.8950, 77.3650 và 77.0600 HTTP RPS. RSS đầu/đỉnh/cuối hold là 118,8/119,3/109,3 MB. Assertion 7.226/65.859 là gap `POST_CHECKOUT_CART` đã biết, không phải HTTP error.

Nguồn tổng hợp: `../../report/metrics-staircase-20260830/staircase-summary.json`; raw JTL và HTML nằm trong các thư mục con; monitor nằm tại `../../evidence/hardware/staircase-20260830/`.
