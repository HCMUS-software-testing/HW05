# HW05 Kiểm thử hiệu năng có hỗ trợ AI - MSSV 23127185

Sinh viên: Mai Thị Kim Duyên. Vai trò: Thành viên 2. Workflow: đăng ký người dùng mới, đăng nhập, duyệt danh mục/sản phẩm, áp dụng mã giảm giá và checkout.

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
- Repository công khai: bổ sung URL GitHub của bài nộp trước khi đóng gói.

## Cách thực thi

```bash
node tools/run_workflow.js --scenario load
node tools/run_workflow.js --scenario stress
node tools/run_workflow.js --scenario spike
node tools/run_workflow.js --scenario soak --duration 600
node tools/analyze_results.js
```

Backend phải đang chạy tại `http://localhost:3000`. Ảnh evidence đã được lưu trong `evidence/screenshots/`; video YouTube không công khai vẫn cần bổ sung URL trước khi nộp.

## Tự đánh giá

| Tiêu chí | Tự đánh giá |
|---|---:|
| Load testing | Chưa chốt |
| Stress testing | Chưa chốt |
| Spike testing | Chưa chốt |
| AI analysis và critique | Chưa chốt |
| Continuous performance testing | Chưa chốt |
| Agent Skill | Chưa chốt |

Bài nộp đã có bằng chứng API có thể tái lập, log thô, báo cáo kiểm toán AI, phần phản biện và ảnh thủ công. Ba thư mục HTML report tại `jmeter/reports/load`, `jmeter/reports/stress`, `jmeter/reports/spike` đã được sinh mới thành công có đầy đủ header, hiển thị khớp chính xác 90 mẫu (samples) và 0% tỷ lệ lỗi. Còn chờ PDF, video YouTube, URL repository công khai và kiểm tra cuối trước khi nộp.
