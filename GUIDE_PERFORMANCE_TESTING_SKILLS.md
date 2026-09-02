# Hướng Dẫn Sử Dụng Bộ Skill: performance-testing-skills

## Tổng quan

Bộ skill `performance-testing-skills` tự động hóa toàn bộ quy trình làm bài tập kiểm thử hiệu năng (HW05 Performance Testing) từ đầu đến cuối. Skill hoạt động độc lập, không phụ thuộc vào slide hay tài liệu bên ngoài — toàn bộ lý thuyết kiểm thử hiệu năng đã được tích hợp sẵn bên trong.

## Cấu trúc Skill

```
.agents/skills/performance-testing-skills/
├── SKILL.md                              # Hướng dẫn chính (10 phase workflow)
├── references/
│   ├── jmeter-plan-template.md           # Template XML cho JMeter .jmx
│   └── report-templates.md               # Template báo cáo Markdown
├── scripts/
│   ├── analyze_jtl.py                    # Phân tích elapsed, latency, percentile, RPS
│   ├── monitor_backend.py                # Lấy CPU theo interval và RSS đúng PID backend
│   ├── run_endurance_template.sh         # Chạy soak test và monitor backend
│   └── run_tests_template.sh             # Template script chạy ba test chính
└── tests/
    └── test_skill_artifacts.py           # Kiểm tra hồi quy cho skill
```

## Workflow 10 Bước

| Phase | Mô tả | Output |
|-------|--------|--------|
| 1. SUT Analysis | Đọc mã nguồn SUT, xác định endpoints, auth, DB | Danh sách endpoint phân nhóm |
| 2. Endpoint Selection | Chọn 3 nhóm (Auth/Read/Transactional), thiết kế workflow | Workflow end-to-end |
| 3. Test Data Creation | Tạo CSV data files (credentials, products...) | `src/data/*.csv` |
| 4. Test Plan Design | Tạo 3 file `.jmx` (Load/Stress/Spike) | `src/test-plans/*.jmx` |
| 5. Runner Script | Tạo script tự động chạy 3 test | `src/run_tests.sh` |
| 6. Execution & Evidence | Chạy test, soak 10-15 phút, chụp htop/fastfetch | `src/results/`, `src/evidence/` |
| 7. Report Generation | Viết báo cáo Task 1+2+3 | `src/report/main-report.md` |
| 8. README & Self-Assessment | Tạo README với bảng tự đánh giá | `src/README.md` |
| 9. Video Demo | Quay video YouTube ≥ 6 phút | Link YouTube unlisted |
| 10. Submission Packaging | Copy, đổi tên, ZIP | File `.zip` nộp bài |

## Cách Kích Hoạt Skill

### Cách 1: Tự động (Recommended)

Skill sẽ tự động kích hoạt khi bạn đề cập đến bất kỳ từ khóa nào liên quan đến performance testing, JMeter, load/stress/spike test trong prompt.

### Cách 2: Từng bước thủ công

Bạn có thể gọi từng phase riêng lẻ bằng các prompt mẫu dưới đây:

#### Phase 1-2: Phân tích SUT & Chọn endpoint
```
Phân tích mã nguồn eshop-sut và thiết kế workflow end-to-end cho luồng [tên luồng].
Xác định các endpoint Auth-heavy, Read-heavy, và Transactional.
```

#### Phase 3: Tạo test data
```
Tạo file CSV dữ liệu đầu vào cho luồng [tên luồng] tại src/data/.
Tham khảo database schema của SUT để đảm bảo dữ liệu hợp lệ.
```

#### Phase 4: Thiết kế test plan
```
Thiết kế kịch bản [Load/Stress/Spike] Test Plan cho sinh viên [MSSV]
với [N] threads, ramp-up [X]s, dùng [Listener Type].
Lưu tại src/test-plans/[MSSV]_[Type]_[YYYYMMDD].jmx
```

#### Phase 5: Tạo runner script
```
Tạo script tự động chạy kiểm thử tại src/run_tests.sh
với đường dẫn tương đối cho thư mục nộp bài độc lập.
```

#### Phase 6: Chạy test & thu thập bằng chứng
```
Chạy ./run_tests.sh và hướng dẫn tôi chụp htop, fastfetch.
```

#### Phase 7: Tạo báo cáo
```
Phân tích kết quả từ file .jtl và tạo báo cáo chính tại src/report/main-report.md
bao gồm Task 1 (metrics), Task 2 (AI misinterpretation hunt), Task 3 (CI/CD proposal).
```

#### Phase 8-10: README, Video, Đóng gói
```
Tạo README.md với bảng tự đánh giá và đóng gói bài nộp.
```

## Lý Thuyết Tích Hợp Sẵn

Skill đã tích hợp đầy đủ kiến thức từ bài giảng "Performance Testing" (ThS. Trần Duy Hoàng, FIT @ HCMUS):

- ✅ **Định nghĩa & Mục tiêu**: Speed, Scalability, Stability
- ✅ **10 Chỉ số Kiểm thử**: CPU, Memory, Response times, Throughput, Latency, Bandwidth, RPS, Error rate, Transactions
- ✅ **6 Loại Test**: Load, Endurance, Stress, Volume, Spike, Scalability
- ✅ **Quy trình 7 Bước**: Identify → Criteria → Plan → Configure → Implement → Run → Analyze

## Tính Năng Nổi Bật

| Đặc điểm | Mô tả |
|-----------|--------|
| **Độc lập** | Không phụ thuộc slide, PDF, hay tài liệu bên ngoài |
| **Tái sử dụng** | Áp dụng được cho mọi endpoint/workflow khác nhau |
| **Portable** | Folder `src/` hoạt động như bài nộp độc lập |
| **Template-driven** | Có sẵn template JMeter XML, báo cáo, runner script |
| **Checklist đầy đủ** | Danh sách deliverables giúp không bỏ sót |

## Kết Hợp Với Skill Khác

- **ai-audit-entry**: Tự động ghi nhật ký AI audit sau mỗi phase
- **brainstorming**: Dùng trước khi bắt đầu Phase 1-2 để brainstorm workflow

## Lưu Ý Quan Trọng

1. **Đường dẫn tương đối**: Mọi path trong `.jmx` và `run_tests.sh` phải relative tới `src/`
2. **3 listener khác nhau**: Không được dùng cùng loại listener cho 2 plan
3. **Kiểm chứng số liệu**: Luôn đối chiếu kết quả AI phân tích với raw `.jtl` log
4. **Hostname**: Hardware screenshot phải khớp hostname với các bài tập trước
5. **Không sửa/xóa `src/`**: Copy ra folder mới trước khi đổi tên và ZIP
6. **Gaussian không bị chặn cứng**: Cấu hình theo mean và standard deviation; khoảng `+/- 3 sigma` chỉ là xấp xỉ 99,7%
7. **Đối chiếu artifact**: Tổng mẫu trong raw JTL phải bằng `Total.sampleCount` của HTML report
8. **Đóng gói skill**: Copy `.agents/skills/performance-testing-skills/` vào `agent-skill/` trong bản staging
9. **Không nói quá endurance**: Một mức tải chỉ chứng minh điểm vận hành bền vững, chưa phải ngưỡng tối đa
