# Chiến lược kiểm thử

Chưa có test vì chưa có code.

| Tầng | Phạm vi | Khi chạy |
|---|---|---|
| Unit | Logic thuần, schema, chuyển trạng thái | Mỗi thay đổi |
| Integration | Queue + SQLite, API, FFmpeg với đầu vào nhỏ | Trước khi kết thúc phase |
| E2E | Pipeline hoàn chỉnh với video ngắn | Từ Phase 9 |
| Soak | Video 10 phút, chạy nhiều ngày | Phase 14 |
| Fault injection | Kill tiến trình, lỗi đĩa, lỗi mạng, ngủ máy | Từ Phase 2 |
| Manual | Chất lượng giọng, hình, nội dung | Chủ dự án, theo phase |

**Quy tắc:**

- Test mặc định không gọi mạng, không cần LLM thật và không cần credentials.
- Dùng adapter giả cho LLM, TTS, nền tảng; test thật được đánh dấu riêng.
- Không dùng API thật hay tài khoản thật cho test tự động.
- Báo cáo ghi kết quả thực tế; test bị bỏ qua phải nêu rõ lý do.

**Báo cáo số đo:** đặt tại `docs/testing/baseline-<chủ-đề>.md`, ghi cấu hình máy, phiên bản phần mềm, lệnh và kết quả thô.

**Bộ kiểm thử đã đặc tả, chưa triển khai:**

| Mã | Chủ đề | Vị trí |
|---|---|---|
| FI-xx, MT-xx | Fault injection queue, `SQLITE_BUSY`, orphan, ngủ máy thật | [queue-safety.md](../architecture/queue-safety.md) mục 13 |
| PF-xx | Lỗi xuất bản, chống đăng trùng | [publishing-reliability.md](../architecture/publishing-reliability.md) mục 9 |
| AC-S, AC-R | Bảo mật và quyền nội dung | [security-and-rights.md](../architecture/security-and-rights.md) mục 10 |
| Spike TTS | So sánh giọng Việt–Anh | `baseline-tts.md`, Phase 1 |

Kiểm thử thủ công phải báo cáo riêng, không được thay bằng mô phỏng rồi ghi là đã kiểm tra.
