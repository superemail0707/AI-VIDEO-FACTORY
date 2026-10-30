# AI VIDEO FACTORY – CURRENT STATUS

Cập nhật lần cuối: 2026-10-30 (workflow mức B được nghiệm thu, SG-001 đã đóng)

| Mục | Trạng thái |
|---|---|
| Phase hiện tại | Phase 0 – Hồ sơ dự án, đã nghiệm thu |
| Tình trạng phase | **Phase 0: ACCEPTED** ở mức tài liệu và thiết kế |
| Ngày nghiệm thu | 2026-10-30 |
| Người nghiệm thu | Project Owner |
| Căn cứ nghiệm thu | Codex Final F-01 Verification: PASS ([báo cáo](docs/operations/reviews/PHASE-00-REVIEW.md)) |
| Application code | **NOT IMPLEMENTED** |
| Runtime testing | **NOT PERFORMED** |
| Git checkpoint | Commit `def8fdf` đã có trên `origin/main`. Commit workflow được Project Owner cho phép, chỉ ở cục bộ. **Mỗi lần commit hay push cần cho phép riêng** |
| Workflow Claude–Codex | **Mức B: Project Owner nghiệm thu** (2026-10-30). Mức C chưa đạt. Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) |
| Scope Grant | SG-001 **DONE**. Không có Scope Grant hay Review Request đang mở |
| Review gần nhất | Codex RR-002: **APPROVED**, F-001 và F-002 CLOSED ([báo cáo](docs/operations/reviews/PHASE-00-REVIEW.md)). Phản hồi tại [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md) |
| D-023 | **APPROVED** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Lượt làm việc | Chủ dự án (Claude đã dừng) |
| Git | Nhánh `main`. `origin/main` ở `def8fdf`; commit workflow chưa push. Chưa xác định repo từ xa riêng tư hay công khai |
| Phase tiếp theo | **Phase 1: NOT AUTHORIZED.** Cổng đầu vào vẫn hiệu lực: quyết định D-013, D-017; trả lời Q-03, Q-06; kế hoạch Phase 1 được xác nhận |

## Tình trạng tính năng

| Hạng mục | Tài liệu | Thiết kế | Chủ dự án duyệt | Triển khai | Kiểm thử |
|---|---|---|---|---|---|
| Tài liệu dự án | Xong | – | Đã nghiệm thu (Phase 0) | – | Kiểm tra tài liệu đã chạy |
| `.gitignore` | Xong | – | Đã nghiệm thu (Phase 0) | Xong | Đã xác minh |
| Queue: fencing, BUSY, orphan | Xong | `Proposed` | Chờ | Chưa làm | Chưa làm |
| Upload, adapter | Xong | `Proposed` | Chờ | Chưa làm | Chưa làm |
| TikTok Direct Post | Xong | **`POLICY BLOCKED`** | D-023 `Approved` chỉ cho đánh giá; chưa có quyết định triển khai | Không được triển khai | Chưa làm |
| Bảo mật cục bộ, OAuth | Xong | `Proposed` | Chờ | Chưa làm | Chưa làm |
| Rights Gate | Xong | `Proposed` | Chờ | Chưa làm | Chưa làm |
| Code ứng dụng | – | – | – | Chưa làm | Chưa làm |
| Phần mềm cài cho dự án, model AI | – | – | – | Chưa làm | – |
| API credentials, tích hợp mạng xã hội | – | – | – | Chưa làm | – |

**Chưa tuyên bố queue an toàn.** Điều đó chỉ đúng sau khi triển khai và các kiểm thử fault injection pass.

## Quyết định

D-001 đến D-007 và **D-023** đã được Chủ dự án duyệt. D-008 thuộc thẩm quyền Lead Developer. **D-009 đến D-022 vẫn là `Proposed`.** Khuyến nghị của Lead Developer không phải phê duyệt.

**D-023 `Approved` không có nghĩa Direct Post được triển khai.** Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. Điều kiện mở cổng G1–G5: [platform-verification.md](docs/deployment/platform-verification.md) mục 3. Bảng theo phase: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) mục 6.

## Việc đang mở

- **R3-01 (HIGH):** đã có quyết định D-023, nhưng rủi ro chính sách **chưa được giải quyết**: Direct Post vẫn `POLICY BLOCKED`.
- **R4-01 (LOW):** Codex đã đóng ở mức tài liệu.
- **F-01 (LOW):** Codex đã đóng.
- **Git push:** commit workflow chưa được phép push. Repo từ xa là riêng tư hay công khai vẫn chưa được xác nhận.
- R3-02, R3-03: Codex xác nhận PASS ở mức đặc tả; chưa kiểm thử.
- FI-43 chưa chứng minh tác vụ trong daemon Ollama đã kết thúc trước job mới.
- B3: Phase 2 bị chặn cho tới khi có quyết định về D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020.
- B4: quyền API và license chỉ đóng khi có bằng chứng cho từng tích hợp. Facebook chưa xác minh.
- W2: chưa có số đo thực trên máy.
- Repo không có tệp báo cáo gốc của vòng 2.
- `vi` (PID 3151) vẫn tạm dừng, giữ buffer trống của `HANDOFF_TO_CHATGPT.md`. **Không dùng `:w!` trong phiên đó.** Thoát bằng `:q!`.

## Câu hỏi chờ Chủ dự án

| Mã | Câu hỏi | Mặc định đề xuất | Cần trước |
|---|---|---|---|
| Q-01 | ~~Nghiệm thu Phase 0 và cho phép tạo commit đầu tiên?~~ | Đã trả lời: **ACCEPTED** (2026-10-30), commit đầu tiên được phép. Push cần cho phép riêng | – |
| Q-02 | Định dạng đầu ra: chỉ 16:9, hay cả 9:16 cho TikTok? 1080p 24 fps có phù hợp? | 16:9 trước, 9:16 sau | Phase 4 |
| Q-03 | Video có kiếm tiền hoặc dùng cho mục đích thương mại không? | Giả định có, chỉ chọn license cho phép thương mại | **Phase 1** (spike TTS) |
| Q-04 | Athena được truy cập internet, hay chỉ dùng nguồn do bạn cung cấp? | Chỉ dùng nguồn cung cấp ở MVP | Phase 8 |
| Q-05 | Đã có Facebook Page, kênh YouTube, tài khoản TikTok chưa? Có sẵn sàng làm thủ tục duyệt app không? | – | Phase 15 |
| Q-06 | Máy có thể cắm điện và chạy qua đêm không? Thời gian tối đa chấp nhận được cho một video? | Chạy qua đêm, tối đa 8 giờ | Phase 1 |
| Q-07 | Sao lưu ở đâu: Git remote riêng tư, ổ ngoài, hay cả hai? | Remote riêng tư cho code, ổ ngoài cho dữ liệu | Phase 2 |
| Q-08 | Đối tượng khán giả có trẻ em không? | Không | Phase 8 |
| Q-09 | ~~Điền `HANDOFF_TO_CHATGPT.md` sau khi đóng `vi`?~~ | Đã trả lời: Chủ dự án yêu cầu tạo ngay | – |
| Q-10 | Quyết định D-013, D-017 | Duyệt | Phase 1 |
| Q-11 | Quyết định D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020 | Xem cổng quyết định | Phase 2 |
| Q-12 | Có muốn cung cấp tệp báo cáo gốc vòng 2 để lưu vào repo không? | Có | Nghiệm thu |
| Q-13 | ~~TikTok (D-023): chọn A, B hay C?~~ | **ANSWERED — OPTION C** (2026-10-30). Tiếp tục đánh giá có kiểm soát; không cấp quyền triển khai | – |
