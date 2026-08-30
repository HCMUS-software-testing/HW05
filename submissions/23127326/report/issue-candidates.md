# Các issue và candidate lỗi

Kho GitHub công khai: `https://github.com/HB4305/23127326-HW05-AI-Performance`

Đã tạo 4 GitHub Issue cho các lỗi có bằng chứng tái hiện. Mỗi issue có response evidence và ảnh trang GitHub trong `evidence/issues/`.

| Candidate | Kỳ vọng | Thực tế | Bằng chứng |
| --- | --- | --- | --- |
| Lockout counter/window | Mỗi login sai tăng +1; khóa sau 3 lần; 30 s | **Đã tái hiện**: status `401, 401, 403, 403`; DB attempts `4`; thời gian khóa `180 s` | `evidence/issues/lockout-probe-20260830.jsonl`, `lockout-state-after-probe-20260830.txt`, GitHub Issue #1, `github-issue-1.png` |
| Checkout cleanup/total | Server tự tính total và làm rỗng cart | **Đã tái hiện**: assertion `POST_CHECKOUT_CART` fail ở cả 4 workload; HTTP error `0%` | JTL thô, `report/metrics-20260830/*.json`, GitHub Issue #2, `github-issue-2.png` |
| Product pagination | `page`/`limit` phải thay đổi phần tử trả về | Đã probe độc lập; SUT chỉ lọc `search`, chưa phân trang | `evidence/issues/pagination-probe-20260830.jsonl`, GitHub Issue #3, `github-issue-3.png` |
| Cart quantity update | Một sản phẩm giữ một dòng với quantity mới | Đã probe độc lập; request POST lần hai tạo dòng sản phẩm trùng | `evidence/issues/cart-update-probe-20260830.jsonl`, GitHub Issue #4, `github-issue-4.png` |

Các lỗi HTTP/network được phân biệt với assertion nghiệp vụ. Không sửa SUT để làm kết quả đẹp.
