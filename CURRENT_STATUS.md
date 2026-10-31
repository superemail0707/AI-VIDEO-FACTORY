# AI VIDEO FACTORY – CURRENT STATUS

Cập nhật lần cuối: 2026-10-31 (đồng bộ trạng thái theo Amendment A02 và A06 của SG-002: 2G, 4c, cài Ollama, tải Qwen3 4B và 8B, số đo thô 4B)

| Mục | Trạng thái |
|---|---|
| Phase hiện tại | **Phase 1 – Môi trường & đo đạc nền: bước 1.0 (chỉ đọc tài liệu); hồ sơ ứng viên đã qua Codex RR-005 `APPROVED` ở mức phân loại, danh sách model mới duyệt một phần (Qwen3 4B `q4_K_M`)** ([danh sách](docs/testing/phase1-candidates.md)) (kế hoạch được Project Owner xác nhận 2026-10-31). Phase 0 đã nghiệm thu |
| Tình trạng phase | **Phase 0: ACCEPTED** ở mức tài liệu và thiết kế |
| Ngày nghiệm thu | 2026-10-30 |
| Người nghiệm thu | Project Owner |
| Căn cứ nghiệm thu | Codex Final F-01 Verification: PASS ([báo cáo](docs/operations/reviews/PHASE-00-REVIEW.md)) |
| Application code | **NOT IMPLEMENTED** |
| Runtime testing | **Chỉ có số đo thô Qwen3 4B** (Amendment A04, A05, 2026-10-31, cắm điện): nạp nguội 2.56 s, 34.1–34.6 token/s, RSS đỉnh 3,277 MB; `format` JSON schema 9/9 hợp lệ, không `format` 2/9 đạt đủ. **8B (A07, không đo cô lập):** ~19 token/s, RSS đỉnh 5,796 MB, swap tăng ~740 MB, `format` 9/9 (không `format` 8/9). Chưa đo cô lập, chưa đo nhiệt. Chất lượng tiếng Việt do Owner chấm (điểm tham khảo của Claude: lời dẫn 3, tóm tắt 2, chia cảnh 2; **chưa phải điểm Owner**). Không có kiểm thử nào cho code vì chưa có code |
| Git checkpoint | Commit `def8fdf` và `fb3a19f` đã có trên `origin/main` (Project Owner cho phép commit và push; Claude xác minh hash khớp). **Mỗi lần commit hay push tiếp theo cần cho phép riêng** |
| Workflow Claude–Codex | **Mức B: Project Owner nghiệm thu** (2026-10-30). Mức C chưa đạt. Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) |
| Scope Grant | SG-001 **DONE**. **SG-002 ACTIVE** (Amendment A01: bốn file nhóm A chỉ đọc; Amendment A02, 2026-10-31: Claude ghi D-024 vào `DECISIONS.md` và đồng bộ `CURRENT_STATUS.md`, không gồm `CHANGELOG.md`). Đã dùng vòng 0, 1, 2; còn vòng 3/3. Không có Review Request đang mở. **Amendment A03–A06 (2026-10-31):** A03 cài Ollama và tải 4B; A04 benchmark 4B (3c giữ lại, sau đó A06 cho tải 8B); A05 đo `format`; A06 tải 8B và đồng bộ trạng thái này. Vòng review còn 3/3 chưa dùng |
| Review gần nhất | Codex RR-005 (SG-002 vòng 2/3): **APPROVED** phân loại; P1-001, P1-002 CLOSED ở RR-004 ([báo cáo](docs/operations/reviews/PHASE-01-REVIEW.md)). Phase 0: RR-002 APPROVED ([báo cáo](docs/operations/reviews/PHASE-00-REVIEW.md)). Phản hồi tại [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md). `CURRENT_STATUS.md` và `DECISIONS.md` đã đổi sau ảnh chụp RR-005 theo A02 |
| D-023 | **APPROVED** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Lượt làm việc | Chủ dự án (Claude đã dừng) |
| Git | Nhánh `main` ở `e83ecec`, trùng `origin/main`; **working tree có thay đổi chưa commit** (7 file đã sửa, 3 file mới; model và số đo thô nằm ngoài Git). Commit và push chưa được cho phép. **Repo từ xa là CÔNG KHAI** (Project Owner xác nhận) |
| Danh sách ứng viên Phase 1 | Mã 1B: Qwen3 4B `q4_K_M` được duyệt vào danh sách. **Qwen3 8B:** Owner cho phép **tải** (A06, 2026-10-31), đã tải, **chưa chạy, chưa đo**; rủi ro RAM với 16 GB còn nguyên. **Chưa có TTS tiếng Việt nào đủ điều kiện nhóm B** (R1); nghiên cứu tài liệu mã 2A không đổi kết luận. Bốn trạng thái (phương pháp, kế hoạch, danh sách, quyền) không tương đương |
| Phase 1 | **PLAN CONFIRMED.** Kế hoạch: [PHASE-01-PLAN.md](docs/operations/phase-reports/PHASE-01-PLAN.md). Owner đã xác nhận điều 1–8 và **bác điều 9** (2G, 4c). Bước 1.0 xong ở mức hồ sơ; **đã làm một phần bước 1.1 và 1.2** (cài Ollama, tải 2 model, đo thô 4B). Chưa cài FFmpeg và Python mới, chưa benchmark render, Whisper, TTS, chưa đo nhiệt. **Mỗi lệnh cài hay tải mới vẫn cần xác nhận riêng.** Commit, push cần cho phép riêng |

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
| Phần mềm cài cho dự án, model AI | – | – | Owner cho phép (A03, A06) | **Đã cài:** Ollama 0.40.13 (Homebrew 7.0.11, kèm 10 gói phụ thuộc, `python@3.15`); **đã tải:** `qwen3:4b-q4_K_M`, `qwen3:8b-q4_K_M` (digest khớp hồ sơ) | 4B và 8B đã đo thô |
| API credentials, tích hợp mạng xã hội | – | – | – | Chưa làm | – |

**Chưa tuyên bố queue an toàn.** Điều đó chỉ đúng sau khi triển khai và các kiểm thử fault injection pass.

## Quyết định

D-001 đến D-007, **D-013, D-017** (2026-10-31), **D-023** và **D-024** (tiêu chuẩn S2, 2026-10-31) đã được Chủ dự án duyệt. D-008 thuộc thẩm quyền Lead Developer. **D-009 đến D-012, D-014 đến D-016 và D-018 đến D-022 (12 mục) vẫn là `Proposed`.** D-013 chỉ duyệt phương pháp benchmark, chưa chọn thư viện. Khuyến nghị của Lead Developer không phải phê duyệt.

**D-023 `Approved` không có nghĩa Direct Post được triển khai.** Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. Điều kiện mở cổng G1–G5: [platform-verification.md](docs/deployment/platform-verification.md) mục 3. Bảng theo phase: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) mục 6.

## Việc đang mở

- **R3-01 (HIGH):** đã có quyết định D-023, nhưng rủi ro chính sách **chưa được giải quyết**: Direct Post vẫn `POLICY BLOCKED`.
- **R4-01 (LOW):** Codex đã đóng ở mức tài liệu.
- **F-01 (LOW):** Codex đã đóng.
- **Repo công khai:** mọi nội dung đã push ai cũng đọc được. Quét `HEAD` không thấy secret, tên máy, đường dẫn cá nhân hay email; chỉ có tên tài khoản GitHub. Không commit credentials, dữ liệu vận hành, model hay media; quét trước mỗi commit. Lịch sử Git không thể xóa sạch nếu lỡ đẩy nội dung nhạy cảm.
- **Chờ Owner (chưa trả lời):** 3e, 3f (Python mới, FFmpeg); benchmark 8B; chấm tiếng Việt chính thức; 4d (chuẩn hóa artifact reviewer vắng mặt); 4e (đóng SG-002); 4f (commit, push). Đã trả lời: 2G, 4c, 3a–3d (một phần), 3c.
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
| Q-03 | ~~Video có kiếm tiền hoặc dùng cho mục đích thương mại không?~~ | **ANSWERED: CÓ** (Project Owner, 2026-10-31). Mọi model, giọng, nhạc, font, asset phải có license cho phép thương mại; thiếu hoặc không rõ thì loại. Áp dụng cho spike TTS Phase 1 và Rights Gate | – |
| Q-04 | Athena được truy cập internet, hay chỉ dùng nguồn do bạn cung cấp? | Chỉ dùng nguồn cung cấp ở MVP | Phase 8 |
| Q-05 | Đã có Facebook Page, kênh YouTube, tài khoản TikTok chưa? Có sẵn sàng làm thủ tục duyệt app không? | – | Phase 15 |
| Q-06 | ~~Máy có chạy qua đêm không? Thời gian tối đa cho một video?~~ | **ANSWERED** (Project Owner, 2026-10-31): chạy qua đêm được, tối đa **4 giờ** cho một video (Owner ghi "4G" và đã **xác nhận là 4 giờ**). Chặt hơn mặc định cũ 8 giờ; dùng làm ngân sách thời gian cho benchmark Phase 1 và đánh giá mục tiêu một video mỗi ngày | – |
| Q-07 | Sao lưu ở đâu? Repo hiện **công khai**, nên không dùng được cho dữ liệu hay secret; cần nơi khác (remote riêng tư, ổ ngoài, hay cả hai)? | Remote riêng tư hoặc ổ ngoài cho dữ liệu; repo công khai chỉ cho tài liệu và code | Phase 2 |
| Q-08 | Đối tượng khán giả có trẻ em không? | Không | Phase 8 |
| Q-09 | ~~Điền `HANDOFF_TO_CHATGPT.md` sau khi đóng `vi`?~~ | Đã trả lời: Chủ dự án yêu cầu tạo ngay | – |
| Q-10 | ~~Quyết định D-013, D-017~~ | **ANSWERED: duyệt cả hai** (Project Owner, 2026-10-31) | – |
| Q-11 | Quyết định D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020 | Xem cổng quyết định | Phase 2 |
| Q-12 | Có muốn cung cấp tệp báo cáo gốc vòng 2 để lưu vào repo không? | Có | Nghiệm thu |
| Q-13 | ~~TikTok (D-023): chọn A, B hay C?~~ | **ANSWERED — OPTION C** (2026-10-30). Tiếp tục đánh giá có kiểm soát; không cấp quyền triển khai | – |
