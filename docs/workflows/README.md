# Quy trình

## 1. Quy trình phát triển Claude – Codex

Quy trình chuẩn nằm tại [AI_REVIEW_WORKFLOW.md](../operations/AI_REVIEW_WORKFLOW.md): Scope Grant, Review Request, quyền ghi, xác định lượt, giới hạn vòng và điều kiện dừng. Mục này không lặp lại các quy tắc đó.

**Quy tắc nhánh:**

- `main`: chỉ chứa phase đã nghiệm thu. Chỉ Chủ dự án quyết định merge vào `main`.
- `phase/NN-<tên>`: nhánh của Claude, chỉ dùng khi Chủ dự án cho phép.
- `review/phase-NN-<chủ-đề>`: chỉ khi Chủ dự án giao Codex sửa.

## 2. Quy trình sản xuất một video

Dự kiến, chưa triển khai:

1. Chủ dự án tạo run trên dashboard: chủ đề, ngôn ngữ, phong cách, độ dài.
2. Worker chạy Athena → Leonardo. Tùy chọn dừng duyệt kịch bản.
3. Edison → Pixar → Spielberg, chạy theo từng cảnh, qua Quality Gate.
4. Lỗi cảnh nào retry cảnh đó. Hết lượt thì run chuyển `BLOCKED` và hiển thị trên dashboard.
5. Chủ dự án xem video, thumbnail, metadata; duyệt hoặc yêu cầu làm lại.
6. Rights Gate chạy lại trên đúng checksum. Tesla đăng bài. Timeout hoặc crash khi upload chuyển `unknown`, chỉ đối soát; không xác định được thì chờ người. Newton thu thập số liệu.

## 3. Lịch dự kiến hằng ngày

Phụ thuộc số đo Phase 14 và Q-06: duyệt chủ đề buổi tối, máy chạy qua đêm khi cắm điện, duyệt và đăng buổi sáng.
