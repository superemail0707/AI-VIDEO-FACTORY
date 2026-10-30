# Quy trình

## 1. Quy trình phát triển Claude – Codex

```text
Claude trình bày kế hoạch → Chủ dự án xác nhận → Claude làm trên nhánh phase/NN-<tên>
→ Claude test, cập nhật tài liệu, viết báo cáo → Claude dừng
→ Chủ dự án chuyển lượt → Codex review (chỉ đọc)
→ Có phát hiện: Chủ dự án chuyển lượt lại cho Claude, sửa, lặp lại
→ Đạt: Chủ dự án nghiệm thu, merge vào main → phase tiếp theo
```

**Quy tắc lượt:** tại một thời điểm chỉ một AI có quyền ghi. Trường "Lượt làm việc" trong `CURRENT_STATUS.md` cho biết ai đang giữ lượt. Chỉ Chủ dự án chuyển lượt và merge vào `main`.

**Quy tắc nhánh:**

- `main`: chỉ chứa phase đã nghiệm thu.
- `phase/NN-<tên>`: nhánh của Claude.
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
