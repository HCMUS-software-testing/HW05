# Report Templates Reference

Templates for generating the required deliverable documents. Replace placeholders (`{...}`) with actual values.

## Main Report Template (`src/report/main-report.md`)

```markdown
# Báo Cáo Kiểm Thử Hiệu Năng (HW05 Performance Testing Report)

- **Họ và tên**: {Student Name}
- **MSSV**: {StudentID}
- **Vai trò / Thành viên**: {Role}
- **Hệ thống kiểm thử (SUT)**: {SUT description}
- **Luồng nghiệp vụ (Workflow)**: {Workflow steps}

---

## 1. Task 1 - Kịch bản & Kết quả Thực thi Kiểm thử Hiệu năng

### 1.1. Phạm vi & Nhóm API Endpoint

Kịch bản end-to-end bao phủ đầy đủ 3 nhóm API theo yêu cầu đề bài:
1. **Auth-heavy**: {endpoints}
2. **Read-heavy**: {endpoints}
3. **Transactional**: {endpoints}

### 1.2. Tổng hợp Kết quả Thực thi (Real Test Metrics)

| Chỉ số / Metric | Load Test | Stress Test | Spike Test |
|---|---|---|---|
| **Số Threads (VU)** | 10 | 50 | 100 |
| **Ramp-up Period** | 10s | 15s | 1s |
| **Số Loops** | 5 | 10 | 3 |
| **Tổng số Samples** | {N} | {N} | {N} |
| **Tổng thời gian chạy** | {T}s | {T}s | {T}s |
| **Throughput (RPS)** | {X} req/s | {X} req/s | {X} req/s |
| **Average Latency** | {X}ms | {X}ms | {X}ms |
| **Min Latency** | {X}ms | {X}ms | {X}ms |
| **Max Latency** | {X}ms | {X}ms | {X}ms |
| **p95 Latency** | {X}ms | {X}ms | {X}ms |
| **Tỷ lệ Lỗi (Error Rate)** | {X}% | {X}% | {X}% |
| **Listener Sử dụng** | Aggregate Report | Summary Report | View Results Tree |
| **File Log Thô** | `results/load/raw.jtl` | `results/stress/raw.jtl` | `results/spike/raw.jtl` |

### 1.3. Phân tích Chi tiết từng Kịch bản

- **Load Test (Tải bình thường)**: {Analysis with real numbers}
- **Stress Test (Tải áp lực)**: {Analysis with real numbers}
- **Spike Test (Đột biến tải)**: {Analysis with real numbers}

### 1.4. Bằng chứng Thực thi

- **Screenshot htop**: `evidence/screenshots/htop_{type}.png`
- **Screenshot Hardware**: `evidence/hardware/fastfetch.png`
- **HTML Reports**: `results/{type}/html-report/index.html`

### 1.5. Ngưỡng Endurance

{Endurance test results: sustained RPS, memory ceiling, test duration}

---

## 2. Task 2 - Phân tích bằng AI & Săn lỗi Diễn giải Sai

### 2.1. Phân tích AI

{AI analysis of .jtl logs and suggested thresholds}

### 2.2. Các lỗi Diễn giải Sai của AI (Misinterpretation Hunt)

| # | AI Claim | Actual Value (from .jtl) | Error Type |
|---|----------|--------------------------|------------|
| 1 | {What AI said} | {Real value} | {Type} |
| 2 | {What AI said} | {Real value} | {Type} |

### 2.3. Đánh giá Khuyến nghị Tối ưu hóa

| # | AI Recommendation | Verdict | Reasoning |
|---|-------------------|---------|-----------|
| 1 | {Recommendation} | Feasible / Hallucination | {Why} |
| 2 | {Recommendation} | Feasible / Hallucination | {Why} |

---

## 3. Task 3 - Đề xuất Continuous Performance Testing

### 3.1. Pipeline CI/CD

{Mermaid flowchart}

### 3.2. Giải thích Pipeline

{Explanation of each stage}

### 3.3. Đánh đổi (Trade-offs)

{Cost, false positives, infrastructure discussion}
```

---

## README Template (`src/README.md`)

```markdown
# HW05 - Performance Testing Report

## Thông tin sinh viên

| Mục | Chi tiết |
|-----|---------|
| Họ tên | {Name} |
| MSSV | {StudentID} |
| Vai trò | {Role} |

## Bảng tự đánh giá

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá |
|-----|----------|:---:|:---:|
| 1 | Task 1 - Load Testing | 30 | {Score} |
| 2 | Task 1 - Stress Testing | 20 | {Score} |
| 3 | Task 1 - Spike Testing | 20 | {Score} |
| 4 | Task 2 - AI Analysis + Misinterpretation Hunt | 10 | {Score} |
| 5 | Task 3 - Continuous Performance Testing | 10 | {Score} |
| 6 | Agent Skills | 10 | {Score} |
| | **Tổng** | **100** | **{Total}** |

## Cấu trúc thư mục

{Directory tree}

## Hướng dẫn chạy

1. Clone repository và cài đặt SUT
2. Start SUT backend: `cd eshop-sut/backend && npm start`
3. Chạy kiểm thử: `cd src && chmod +x run_tests.sh && ./run_tests.sh`

## Tóm tắt kết quả

- **Kịch bản đã chạy**: Load, Stress, Spike
- **Nhóm endpoint**: {Groups}
- **Ngưỡng Endurance**: {RPS} RPS bền vững, {MEM} MB memory ceiling
- **Số bug / vấn đề**: {N}
- **Video demo**: {YouTube link}
```

---

## AI Critique Template (200-300 words, `src/report/ai-critique.md`)

```markdown
# AI Critique (Phê bình AI)

## AI đã sai ở đâu?

{Describe specific misinterpretations, wrong metric values, hallucinated recommendations}

## Vì sao AI không phát hiện được?

{Explain limitations: context window, inability to run code, statistical reasoning gaps}

## Nguyên tắc cộng tác với AI

{Lessons learned about AI collaboration in performance testing}
```
