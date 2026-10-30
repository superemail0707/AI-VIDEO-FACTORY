# Yêu cầu

Tất cả ở trạng thái **Chưa làm**. Mỗi test nghiệm thu nên tham chiếu mã yêu cầu.

## Chức năng

| Mã | Yêu cầu | Phase |
|---|---|---|
| FR-01 | Tạo video hoạt hình 2D từ văn bản | 9 |
| FR-02 | Hỗ trợ tiếng Việt và tiếng Anh | 6–9 |
| FR-03 | Video dài tối đa 10 phút | 14 |
| FR-04 | Nhiều nhân vật | 12 |
| FR-05 | Nhiều giọng đọc | 6, 12 |
| FR-06 | Lip-sync cơ bản | 12 |
| FR-07 | Stickman animation | 5 |
| FR-08 | Whiteboard animation | 11 |
| FR-09 | Educational explainer | 11 |
| FR-10 | Storytelling nhiều nhân vật | 12 |
| FR-11 | Phụ đề | 9 |
| FR-12 | Thumbnail | 13 |
| FR-13 | Metadata | 13 |
| FR-14 | Xuất MP4 | 4 |
| FR-15 | Đăng YouTube qua API chính thức | 15 |
| FR-16 | Đăng TikTok qua API chính thức; mục tiêu giữ trong roadmap. **`POLICY BLOCKED`:** D-023 `Approved — Option C` (2026-10-30, Project Owner), Q-13 `Answered — Option C` chỉ cho phép tiếp tục nghiên cứu, đánh giá. G1–G5 vẫn bắt buộc trước khi đề xuất triển khai, và phải có quyết định triển khai riêng của Project Owner | 16 |
| FR-17 | Đăng Facebook qua API chính thức | 16 |
| FR-18 | Dashboard quản lý toàn bộ quy trình | 10 |
| FR-19 | Phân tích hiệu suất | 17 |
| FR-20 | Phê duyệt của con người trước khi xuất bản | 3, 10 |

## Phi chức năng

| Mã | Yêu cầu | Đo bằng |
|---|---|---|
| NFR-01 | Chạy trên MacBook Air M4 16GB | Benchmark Phase 1, 14 |
| NFR-02 | Hướng đến một video mỗi ngày | Phase 14; ngưỡng thời gian chờ Q-06 |
| NFR-03 | Local-first; chỉ dùng mạng khi cần thiết (ví dụ xuất bản) | Rà soát |
| NFR-04 | Retry từng tác vụ, từng cảnh | Test lỗi giả lập |
| NFR-05 | Phục hồi sau gián đoạn | Kill tiến trình, ngủ máy |
| NFR-06 | Không secret trong source | Quét repo |
| NFR-07 | Không tự xóa dữ liệu quan trọng | Rà soát code, test |
| NFR-08 | Có manifest license cho mọi asset | QG5 |
| NFR-09 | Có khả năng mở rộng thành website hoặc ứng dụng | Ranh giới API |
| NFR-10 | Worker cũ không ghi đè kết quả mới | FI-01 đến FI-06, FI-22, FI-23 |
| NFR-14 | Không chồng tác vụ nặng, kể cả khi có tiến trình mồ côi | FI-33 đến FI-42 |
| NFR-15 | Tranh chấp DB không bị tính là lỗi job và không tạo thành công giả | FI-18, FI-26 đến FI-31, FI-44 đến FI-49 |
| NFR-11 | Không có đăng trùng tự động | AC-P1 đến AC-P11, PF-01 đến PF-13 |
| NFR-12 | Không xuất bản khi quyền nội dung thiếu hoặc không rõ | AC-R1 đến AC-R3 |
| NFR-13 | API cục bộ chống yêu cầu từ trình duyệt ngoài ý muốn | AC-S1, AC-S2 |
