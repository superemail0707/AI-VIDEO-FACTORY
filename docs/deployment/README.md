# Triển khai cục bộ

Chưa có gì để triển khai. Tài liệu này được hoàn thiện ở Phase 1, 2 và 19.

Xác minh chính sách trước mỗi publishing adapter: [platform-verification.md](platform-verification.md).

**Mục tiêu:** một máy Mac, không cần Docker, không cần dịch vụ ngoài trong luồng sản xuất.

**Sẽ ghi lại khi phát sinh:**

- Danh sách phần mềm đã cài, phiên bản, lý do và cách gỡ.
- Cách khởi động và dừng API, Worker, Dashboard.
- Biến cấu hình. Dự án chỉ commit `.env.example`, không commit giá trị thật.
- Cách giữ máy thức khi Worker chạy.
- Quy trình nâng cấp và migration.
