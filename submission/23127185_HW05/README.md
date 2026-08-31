# HW05 Kiểm thử hiệu năng có hỗ trợ AI - MSSV 23127185

Sinh viên: Mai Thị Kim Duyên. Vai trò: Thành viên 2. Workflow: đăng ký người dùng mới, đăng nhập, duyệt danh mục/sản phẩm, áp dụng mã giảm giá và checkout.

## Danh mục artifact

- Test plan: `jmeter/plans/`
- JTL thô: `jmeter/results/`
- Báo cáo HTML: `jmeter/reports/`
- Chỉ số: `report/metrics.md` và `report/metrics.json`
- Báo cáo chính: `report/main-report.md`
- Báo cáo kiểm toán AI: `report/ai-audit-report.md`
- Phản biện AI: `report/ai-critique.md`
- Agent Skill: `agent-skill/eshop-performance-testing/SKILL.md`

## Cách thực thi

```bash
node tools/run_workflow.js --scenario load
node tools/run_workflow.js --scenario stress
node tools/run_workflow.js --scenario spike
node tools/run_workflow.js --scenario soak --duration 600
node tools/analyze_results.js
```

Backend phải đang chạy tại `http://localhost:3000`. Các ảnh chụp thủ công và video cuối cùng chưa được bổ sung; danh sách được ghi trong `evidence/manual-evidence-needed.md`.

## Tự đánh giá

Đã có bằng chứng API có thể tái lập, log thô, báo cáo HTML, báo cáo kiểm toán AI và phần phản biện. Bài nộp cuối chưa hoàn tất cho đến khi Mai xác nhận tương quan token của JMeter, chụp ảnh thủ công, quay video tiếng Việt và bổ sung liên kết YouTube.
