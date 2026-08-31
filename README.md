# HW05 - Performance Testing

- **Họ và tên**: Lê Trung Kiên
- **Mã số sinh viên**: 23127075
- **Thành viên**: 4

## Workflow được phân công (Thành viên 4)
- **Quy trình**: Admin đăng nhập -> Dashboard / Danh sách sản phẩm -> CRUD Sản phẩm / Danh mục hoặc Import CSV.
- **Bao phủ**:
  - **Auth-heavy**: Admin login & kiểm soát truy cập (Access Control).
  - **Read-heavy**: Dashboard Admin, danh sách sản phẩm / danh mục.
  - **Transactional**: CRUD sản phẩm/danh mục hoặc Import CSV.
- **Tên file quy chuẩn**: `23127075_Load_<YYYYMMDD>.jmx`, `23127075_Stress_<YYYYMMDD>.jmx`, `23127075_Spike_<YYYYMMDD>.jmx`
