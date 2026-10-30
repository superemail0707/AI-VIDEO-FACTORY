# Ghi chú kiến trúc

Thiết kế tổng thể nằm tại [ARCHITECTURE.md](../../ARCHITECTURE.md). Thư mục này chứa thiết kế chi tiết của từng phần khi đến phase tương ứng, ví dụ định dạng scene spec ở Phase 4 và API ở Phase 2.

Quy ước: mỗi ghi chú có mục tiêu, ràng buộc, thiết kế và phương án đã loại. Quyết định quan trọng vẫn ghi vào [DECISIONS.md](../../DECISIONS.md).

| Tài liệu | Nội dung | Trạng thái | Phải duyệt trước |
|---|---|---|---|
| [queue-safety.md](queue-safety.md) | Fencing, staging, phục hồi, fault injection | `Proposed` | Phase 2 |
| [publishing-reliability.md](publishing-reliability.md) | Máy trạng thái upload, đối soát | `Proposed` | Phase 15 |
| [security-and-rights.md](security-and-rights.md) | Bảo mật, OAuth, quyền nội dung | `Proposed` | Phase 2, 13, 15 |
