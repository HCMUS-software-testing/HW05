# HW05 - Kiểm thử hiệu năng

## 1. Thông tin chung

| Mục | Nội dung |
| --- | --- |
| Mã bài tập | HW05-AI |
| Thời lượng | 10 giờ |
| Hạn nộp | Xem liên kết nộp bài trên Moodle |
| Hình thức | Bài tập cá nhân |
| Nộp bài | Moodle, nộp báo cáo |
| Giảng viên và trợ giảng | TS. Lâm Quang Vũ / TS. Trần Duy Hoàng / ThS. Trần Thị Bích Hạnh / ThS. Trương Phước Lộc / ThS. Hồ Tuấn Thanh |
| Liên hệ | lqvu@fit.hcmus.edu.vn / tdhoang@fit.hcmus.edu.vn / ttbhanh@fit.hcmus.edu.vn / tploc@fit.hcmus.edu.vn / hthanh@fit.hcmus.edu.vn |
| Chính sách AI | Mở, nhưng bắt buộc phải khai báo và đính kèm Báo cáo kiểm toán AI |
| Mức Bloom-AI yêu cầu | G9.1 đến G9.6 tùy bài tập, xem phần ánh xạ CLO |

## 2. Nguyên tắc thực hiện

Các nguyên tắc này quy định cách bạn cần làm việc trong toàn bộ chuỗi bài tập của môn học. Hãy đọc kỹ trước khi bắt đầu vì bài nộp sẽ được đánh giá theo các nguyên tắc này.

- **Chiến lược AI-first:** Bạn bắt buộc áp dụng AI cho các kỹ thuật kiểm thử đã học trên lớp. Tuy nhiên, điều này không có nghĩa là chỉ đưa một prompt chung chung như "hãy chạy load test và cho biết hiệu năng có tốt không". Bạn phải dẫn dắt AI qua từng bước của kỹ thuật như đã học, dùng AI như một trợ lý có kỷ luật thay vì một hộp đen.
- **Rà soát của con người:** Mọi kết quả do AI tạo ra phải được sinh viên kiểm tra cẩn thận. Bạn hoàn toàn chịu trách nhiệm về tính đúng đắn của các kết quả đó. Bạn cần chỉnh sửa và tinh chỉnh khi cần; nộp nguyên kết quả thô từ AI mà không rà soát là không được chấp nhận.
- **Báo cáo kiểm toán AI:** Toàn bộ quá trình sử dụng AI phải được ghi lại đầy đủ. Bạn được khuyến khích xây dựng Agent Skill để tự động thực hiện các hoạt động tương tự cho các bài tập sau. Nếu không dùng AI, bạn vẫn phải khai báo rõ.
- **Tài liệu hóa:** Toàn bộ quá trình làm việc phải được ghi lại ở định dạng văn bản, ví dụ Markdown.
- **Chất lượng quan trọng hơn hoàn thành hình thức:** Điểm không chỉ dựa trên việc có đủ nội dung hay không, mà còn dựa trên số lượng và chất lượng của test plan, file dữ liệu, log thô, các dạng báo cáo, bằng chứng tài nguyên/phần cứng, video demo, phần phản biện phân tích của AI và các liên kết tham chiếu.

## 3. Kết quả học tập

Sau khi hoàn thành bài tập này, bạn có thể:

- Thiết kế và chạy kiểm thử hiệu năng Load, Stress và Spike trên backend API của SUT bằng JMeter hoặc k6.
- Thu thập và trình bày chỉ số hiệu năng kèm giám sát tài nguyên và nhiều dạng báo cáo; xác định ngưỡng chịu tải lâu dài trên phần cứng của bạn.
- Dùng AI phân tích kết quả, sau đó phản biện phân tích của AI bằng cách xác định nơi AI hiểu sai chỉ số và đề xuất tối ưu nào khả thi.
- Đề xuất pipeline kiểm thử hiệu năng liên tục.
- Thể hiện năng lực Bloom-AI ở các mức G9.2 (Apply), G9.3 (Analyse), G9.4 (Collaborate) và G9.6 (Disrupt).

## 4. Hệ thống được kiểm thử

- **SUT:** EShop, một ứng dụng thương mại điện tử demo tiếng Việt dùng cho thực hành kiểm thử.
- **Repository:** <https://github.com/ttbhanh/eshop-sut>

Các chức năng của ứng dụng được tổ chức thành các nhóm sau:

### Pool A - Xác thực, danh mục và sản phẩm

- FR-01: Đăng ký tài khoản
- FR-02: Đăng nhập và khóa tài khoản
- FR-03: Quên mật khẩu và đặt lại mật khẩu, gồm hai bước
- FR-04: Quản lý hồ sơ cá nhân
- FR-05: Danh sách và tìm kiếm sản phẩm
- FR-06: Xem chi tiết sản phẩm

### Pool B - Giỏ hàng và thanh toán

- FR-07: Giỏ hàng
- FR-08: Thanh toán
- FR-09: Mã giảm giá
- FR-10: Máy trạng thái đơn hàng
- FR-11: Xem lịch sử đơn hàng của người dùng

### Pool C - Web Admin

- FR-12: Kiểm soát truy cập
- FR-13: Dashboard
- FR-14: Quản lý danh mục, CRUD
- FR-15: Quản lý sản phẩm, CRUD
- FR-16: Nhập sản phẩm từ CSV
- FR-17: Quản lý mã giảm giá, CRUD
- FR-18: Quản lý đơn hàng ở trang admin
- FR-19: Quản lý người dùng ở trang admin

### Pool D - Mobile App

SUT cung cấp REST backend API được web frontend sử dụng. Hãy xem repository để biết endpoint và port chính xác.

## 5. Phạm vi - chọn endpoint

Chọn ba nhóm endpoint backend API và ánh xạ chúng với API của SUT:

- **Read-heavy:** Ví dụ danh sách/tìm kiếm sản phẩm và chi tiết sản phẩm.
- **Auth-heavy:** Ví dụ đăng nhập, có xét đến hành vi khóa tài khoản.
- **Transactional:** Ví dụ thêm vào giỏ hàng và thanh toán/tạo đơn hàng.

Như các bài tập trước, phải đảm bảo lựa chọn của bạn không trùng với thành viên khác trong nhóm: không có hai thành viên kiểm thử cùng một workflow.

## 6. Yêu cầu

Với từng nhiệm vụ sau, hãy tài liệu hóa quá trình trong báo cáo chính và đính kèm bằng chứng bắt buộc. Hãy ôn lại các bài giảng liên quan đến kiểm thử hiệu năng trước khi bắt đầu.

### Task 1 - Thiết kế và thực thi kiểm thử có AI hỗ trợ

Theo chiến lược AI-first, dùng một công cụ AI để thiết kế và sinh test plan, sau đó bạn tự rà soát, sửa lỗi và chịu trách nhiệm hoàn toàn với chúng.

- **Thiết kế và sinh bằng AI:** Dẫn dắt AI từng bước, không dùng một prompt chung chung, để thiết kế và sinh ba test plan: Load, Stress và Spike. Cả ba test plan phải chạy cùng một workflow end-to-end, bao phủ cả ba nhóm endpoint: auth-heavy, read-heavy và transactional. Ví dụ: một virtual user đăng nhập, duyệt hoặc tìm kiếm sản phẩm, thêm sản phẩm vào giỏ và hoàn tất thanh toán. Nhờ AI hỗ trợ chọn tham số thực tế như think-time, ramp-up, số thread/virtual user cho từng kịch bản, và giải thích ngắn gọn cách workflow bao phủ từng nhóm endpoint.
- **Làm workflow theo hướng data-driven:** Dùng dữ liệu CSV trong workflow end-to-end để tham số hóa request, ví dụ credentials, product IDs hoặc order payloads. Có thể dùng một hoặc nhiều file CSV tùy workflow.
- **Dùng ba dạng báo cáo khác nhau:** Trong ba test plan, dùng ba listener/report khác nhau, ví dụ View Results Tree, Summary Report, Aggregate Report; không lặp lại cùng loại. Với k6, cung cấp các output tương đương và khác nhau.
- **Quy tắc đặt tên test plan:** `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
- **Rà soát và sửa lỗi bởi con người:** Phản biện test plan do AI sinh ra và chỉnh sửa. Báo cáo AI đã sai hoặc thiếu gì, ví dụ ramp-up hoặc think-time không thực tế, số thread sai, assertion yếu, thiếu xử lý khóa tài khoản, và giải thích nguyên nhân như chất lượng prompt, giới hạn mô hình hoặc đặc điểm endpoint. Bạn chịu trách nhiệm hoàn toàn với test plan cuối cùng.
- **Chạy đầy đủ nhất có thể, có bằng chứng:** Thực thi cả ba kịch bản và chụp, cho mỗi lần chạy, ảnh màn hình công cụ kiểm thử cùng với tài nguyên backend process như htop, Task Manager hoặc Activity Monitor. Thêm báo cáo phần cứng gồm ảnh dxdiag/screenfetch và bảng thông số. Khi Stress/Spike kích hoạt khóa đăng nhập do 3 lần sai, hãy reset giữa các lần chạy và ghi lại các bước. Tạo log thô `.jtl` và thư mục báo cáo HTML.
- **Xác định ngưỡng endurance:** Chạy một bài endurance/soak ngắn khoảng 10-15 phút với tải duy trì để tìm ngưỡng phần cứng của bạn bằng thực nghiệm, báo cáo bằng số cụ thể như RPS ổn định tối đa và trần bộ nhớ.
- **Ghi video demo:** Video YouTube không công khai, tổng thời lượng ít nhất 6 phút, có thể chia thành một clip cho mỗi kịch bản, hiển thị công cụ kiểm thử và màn hình giám sát tài nguyên trong cùng khung hình, có lời thuyết minh tiếng Việt của bạn.
- **Báo cáo lỗi:** Ghi nhận bug hoặc vấn đề hiệu năng thật, như lỗi response, crash, hồi quy chức năng, trên GitHub Issues kèm ảnh chụp. Việc ghi nhận vấn đề hiệu năng như latency cao hoặc tỷ lệ lỗi tăng được khuyến khích nhưng không bị phạt nếu không có.

### Task 2 - Phân tích bằng AI và săn lỗi diễn giải sai

Theo chiến lược AI-first, dùng AI phân tích kết quả, sau đó phản biện kết quả AI tạo ra. Phần phân tích là output của AI, phần rà soát là của bạn.

- **Phân tích bằng AI:** Sau khi thu thập kết quả thô, prompt một công cụ AI phân tích log `.jtl` và đề xuất ngưỡng hiệu năng.
- **Rà soát và sửa bởi con người:** Phản biện phân tích của AI và chỉ ra nơi AI diễn giải hoặc đọc sai chỉ số. Với mỗi lỗi diễn giải, trích giá trị đúng từ log `.jtl` thô và giải thích lỗi.
- **Đánh giá khuyến nghị của AI:** Yêu cầu AI đề xuất tối ưu, ví dụ thêm database index, connection pool hoặc bật SQLite WAL, rồi phân loại từng đề xuất là khả thi hay bịa đặt/hallucinated, kèm lập luận.

### Task 3 - Đề xuất kiểm thử hiệu năng liên tục (Disrupt)

Trong phần kết luận, đề xuất mô hình kiểm thử hiệu năng liên tục có khả năng theo dõi commit của SUT, quyết định khi nào chạy kiểm thử hiệu năng và cảnh báo hồi quy p95. Bao gồm flow chart và thảo luận trade-off như chi phí và cảnh báo sai.

## 7. Agent Skill

Bạn được khuyến khích xây dựng một Agent Skill áp dụng workflow kiểm thử hiệu năng và phân tích log này để có thể tái sử dụng cho endpoint khác trong các bài kiểm thử sau.

Nộp skill kèm video demo YouTube cho thấy từ đầu đến cuối cách bạn dùng skill trên một nhóm endpoint hoàn chỉnh.

## 8. Công cụ được phép và mức Bloom-AI

Bạn có thể dùng các công cụ sau và phải khai báo trong Báo cáo kiểm toán AI:

- JMeter mặc định hoặc k6 nếu muốn lấy điểm bonus.
- Bất kỳ công cụ AI nào bạn chọn, ví dụ ChatGPT, Claude, Gemini, để phân tích log.
- Công cụ giám sát tài nguyên như htop, Task Manager hoặc Activity Monitor.

Mức Bloom-AI bắt buộc cho bài này là G9.2 (Apply), G9.3 (Analyse), G9.4 (Collaborate) và G9.6 (Disrupt).

## 9. Báo cáo kiểm toán AI, phụ lục bắt buộc

Đính kèm Báo cáo kiểm toán AI như một phụ lục. Có thể dùng nội dung trong AI Templates nếu cần.

- Nếu không dùng AI, khai báo: "I do not use any AI help in this exercise."
- Nếu có dùng AI, khai báo: "I use AI tools for the following tasks," và đưa thông tin sau cho từng lượt tương tác:
  - Tên công cụ AI
  - Ngày và giờ
  - Prompt của bạn
  - Output của AI

Để đơn giản hóa, bạn được khuyến khích tạo skill hoặc rule tự động trích xuất các thông tin trên sau một phiên làm việc với AI.

## 10. AI Critique, bắt buộc, 200-300 từ

Viết một đoạn 200-300 từ phản biện AI. Trả lời các câu hỏi: AI sai, thiên lệch hoặc thiếu ở đâu? Vì sao AI không phát hiện được vấn đề? Bạn học được nguyên tắc gì khi cộng tác với AI trong bài tập này?

Có thể dùng nội dung của AI Templates nếu cần.

## 11. Ràng buộc chống gian lận bằng AI

Bài tập này dựa trên bằng chứng thực thi thật và có thể truy vết. Các mục sau không được AI tạo giả hoặc bịa đặt, và trợ giảng sẽ kiểm tra khi chấm:

- Tên file test plan phải khớp `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
- File log `.jtl` thô, đính kèm đầy đủ, không chỉ nộp tóm tắt.
- Video demo phải hiển thị công cụ kiểm thử và resource monitor trong cùng khung hình, có giọng thuyết minh của chính bạn.
- Báo cáo phần cứng phải có hostname khớp với các lần triển khai ở bài tập trước.

## 12. Git commit log

Tạo một Git commit mới cho mỗi bước của quy trình, ví dụ mỗi test plan của từng kịch bản, phần phân tích AI và đề xuất kiểm thử liên tục.

Cung cấp Git commit log ở định dạng file văn bản.

## 13. Bảo vệ vấn đáp

30% sinh viên được chọn ngẫu nhiên có thể được mời bảo vệ vấn đáp 5-7 phút trong tuần sau hạn nộp để giải thích cách hoàn thành bài tập.

## 14. Quy định nộp bài

- **Định dạng tên file:** `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`
- **SelfAssessedGrade:** Số 3 chữ số trong khoảng `[000, 100]`.
- **Ví dụ:** `25127001_HW05_AI_Performance_090.zip`

Nội dung bắt buộc trong file `.zip`:

- Báo cáo chính, Markdown và PDF, bao gồm báo cáo kiểm thử hiệu năng và phần AI-analysis critique.
- Link GitHub repository công khai chứa test plan và data file.
- Ba test plan Load / Stress / Spike đúng quy tắc đặt tên.
- Ba file log `.jtl` thô và ba thư mục báo cáo HTML.
- Ảnh resource monitor và ảnh/bảng thông số phần cứng.
- Link video demo YouTube không công khai.
- AI Critique và AI Audit Report, Markdown và PDF.
- Git commit log dạng text.
- Bug report kèm ảnh trên GitHub Issues nếu có.
- `README.md` chứa bảng tự đánh giá và báo cáo tóm tắt kiểm thử: các kịch bản đã chạy, nhóm endpoint đã bao phủ, ngưỡng endurance với số liệu, số bug/vấn đề hiệu năng và link video demo.
- Các tài liệu hỗ trợ khác nếu có.

Nộp lên Moodle. Hạn nộp xem tại liên kết nộp bài.

## 15. Mẫu đánh giá

| STT | Tiêu chí | Điểm tối đa | Điểm tự đánh giá |
| --- | --- | ---: | --- |
| 1 | Task 1 - Load testing | 30 | |
| 2 | Task 1 - Stress testing | 20 | |
| 3 | Task 1 - Spike testing | 20 | |
| 4 | Task 2 - Phân tích AI và săn lỗi diễn giải sai, có giá trị đúng từ log thô | 10 | |
| 5 | Task 3 - Đề xuất Continuous Performance Testing, G9.6 | 10 | |
| 6 | Agent Skills | 10 | |
|  | **Tổng** | **100** | |

## 16. Tài liệu tham khảo

- ISTQB Foundation Level Syllabus, phiên bản mới nhất.
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Anthropic (2025). Building Reliable AI Test Agents, engineering blog.
- Tài liệu DeepEval và Promptfoo về framework kiểm thử LLM.

## 17. Quy định khác

- Không chấp nhận nộp trễ.
- Thiếu bất kỳ tài liệu bắt buộc nào sẽ bị 0 điểm.
- Sao chép giữa sinh viên, bao gồm cả prompt, sẽ khiến cả hai bên bị 0 điểm.
