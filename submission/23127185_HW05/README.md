# HW05 Kiểm thử hiệu năng có hỗ trợ AI 

- MSSV 23127185
- Họ và tên: Mai Thị Kim Duyên. 
- Workflow: đăng ký người dùng mới, đăng nhập, duyệt danh mục/sản phẩm, áp dụng mã giảm giá và checkout.

## Danh mục artifact

- Test plan: `jmeter/plans/`
- JTL thô: `jmeter/results/`
- Báo cáo HTML: `jmeter/reports/`
- Chỉ số: `report/metrics.md` và `report/metrics.json`
- Báo cáo chính: `report/main-report.md` và `report/main-report.pdf`
- Báo cáo kiểm toán AI: `report/ai-audit-report.md` và `report/ai-audit-report.pdf`
- Phản biện AI: `report/ai-critique.md` và `report/ai-critique.pdf`
- Báo cáo Bug: `report/bug-report.md` và `report/bug-report.pdf`
- Agent Skill: `agent-skill/eshop-performance-testing/SKILL.md`
- Video Demo YouTube: https://youtu.be/4AzdHAQVLhQ
- Repository công khai: https://github.com/HCMUS-software-testing/HW05

## Cách thực thi

```bash
node tools/run_workflow.js --scenario load
node tools/run_workflow.js --scenario stress
node tools/run_workflow.js --scenario spike
node tools/run_workflow.js --scenario soak --duration 600
node tools/analyze_results.js
```

Backend phải đang chạy tại `http://localhost:3000`. Ảnh evidence đã được lưu trong `evidence/screenshots/`; video YouTube không công khai: https://youtu.be/4AzdHAQVLhQ.

## Tự đánh giá

| STT | Tiêu chí | Điểm tối đa | Tự đánh giá |
|---|---|---:|---:|
| 1 | Task 1 - Load testing | 30 | 30/30 |
| 2 | Task 1 - Stress testing | 20 | 20/20 |
| 3 | Task 1 - Spike testing | 20 | 20/20 |
| 4 | Task 2 - AI analysis + misinterpretation hunt | 10 | 10/10 |
| 5 | Task 3 - Continuous Performance Testing proposal | 10 | 10/10 |
| 6 | Agent Skills | 10 | 10/10 |
| | **Tổng cộng** | **100** | **100/100** |

## Báo cáo tóm tắt kiểm thử

- **Các kịch bản đã chạy:** Load (10 users, ramp 5s, 30s), Stress (10 users, ramp 5s, 60s), Spike (10 users, ramp 5s, 10s), Endurance/Soak (2 workers, 600s / 10 phút).
- **Các nhóm endpoint bao phủ (Member 2):** Auth-heavy (`POST /api/register`, `POST /api/login`), Read-heavy (`GET /api/categories`, `GET /api/products`, `GET /api/products/:id`), Transactional (`POST /api/cart`, `POST /api/apply-coupon`, `POST /api/checkout`, `GET /api/orders/my-orders`).
- **Ngưỡng endurance (số liệu cụ thể):** Duy trì 2 virtual workers trong 600 giây với 292.482 samples, 0% lỗi, throughput ~487 req/s, P95 6 ms, P99 49 ms trên môi trường loopback.
- **Số bug / vấn đề hiệu năng phát hiện:** 11 bugs (bao gồm nghẽn I/O đĩa SQLite, SQL Injection, Privilege Escalation, Price Tampering, lỗi công thức Coupon, lỗi state machine đơn hàng, mismatch kiểu dữ liệu Price, ... đã tạo Issues #12 - #21 trên GitHub).
- **Liên kết video demo:** https://youtu.be/4AzdHAQVLhQ

