# AI VIDEO FACTORY – TASKS

Trạng thái: `[ ]` chưa làm, `[~]` đang làm, `[x]` xong và có kiểm chứng, `[!]` bị chặn. Người phụ trách mặc định là Claude; việc của người khác ghi `(Codex)` hoặc `(Owner)` ở đầu dòng.

## Phase 0 – Hồ sơ dự án

- [x] Kiểm tra thư mục, không xóa dữ liệu
- [x] Viết `PROJECT_MASTER.md`
- [x] Viết `ARCHITECTURE.md`
- [x] Viết `IMPLEMENTATION_PLAN.md`
- [x] Viết `TECH_STACK.md`
- [x] Viết `AGENTS.md`
- [x] Viết `CLAUDE.md`, giữ nguyên quy tắc của Chủ dự án
- [x] Viết `DECISIONS.md`
- [x] Viết `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`
- [x] Tạo tài liệu trong `docs/`
- [x] Tạo `.gitignore`
- [x] Viết báo cáo Phase 0
- [x] Tạo `HANDOFF_TO_CHATGPT.md`
- [x] Codex review lần 1: NEEDS REVISION
- [x] Bản sửa 1: queue safety, rà soát D-009–D-017, spike TTS, độ tin cậy xuất bản, bảo mật và quyền nội dung
- [x] Viết `REVIEW_RESPONSE.md`
- [x] Nhận phát hiện review vòng 2 từ Chủ dự án
- [x] Bản sửa 2: `.gitignore`, `SQLITE_BUSY`, orphan, fault injection, OAuth, TikTok, Rights Gate, YouTube, Facebook
- [x] Xác minh `.gitignore` bằng `git check-ignore --no-index` và repo thử
- [x] Codex review vòng 3: CHANGES REQUESTED
- [x] Bản sửa 3: R3-01 ghi nhận và chặn TikTok, R3-02, R3-03 đặc tả
- [x] Codex review vòng 4: APPROVED WITH CHANGES cho hồ sơ Phase 0
- [x] Ghi nhận D-023 `Approved`, Q-13 phương án C (Project Owner, 2026-10-30)
- [x] Khắc phục R4-01 trong tài liệu: cổng G1–G5, tách Decision status và integration status
- [x] Codex kiểm tra lại R4-01: CLOSED
- [x] Sửa F-01; Codex Final F-01 Verification: PASS, F-01 CLOSED
- [x] Project Owner nghiệm thu Phase 0 (2026-10-30), mức tài liệu và thiết kế

## Git checkpoint

- [x] Chuẩn bị chỉ đọc: kiểm tra Git, file nhạy cảm, `.gitignore`, danh sách staging
- [x] Project Owner cho phép commit và chọn danh tính Git
- [x] Commit đầu tiên trên `main`, thực hiện cục bộ
- [x] Push commit đầu tiên `def8fdf` lên `origin/main`, do Project Owner thực hiện; Claude xác minh hash khớp
- [x] Commit workflow mức B trên `main`, thực hiện cục bộ theo cho phép của Project Owner
- [ ] (Owner) Quyết định có push commit workflow không

## Cổng trước Phase 1

- [ ] Chủ dự án quyết định D-013, D-017
- [ ] Trả lời Q-03, Q-06

## Phase 1 – Môi trường & đo đạc nền (chưa được phép bắt đầu)

- [ ] Trình bày kế hoạch chi tiết, chờ xác nhận
- [ ] Cài công cụ theo xác nhận từng bước
- [ ] Chạy benchmark LLM, rasterize, mã hóa, Whisper
- [ ] Chạy thử bền 30 phút
- [ ] Trình kết quả benchmark D-013
- [ ] Rà soát license ứng viên TTS trước khi tải
- [ ] Chạy spike TTS Việt–Anh, tạo mẫu nghe
- [ ] Chủ dự án nghe mù và chấm điểm
- [ ] Viết báo cáo số đo và `docs/testing/baseline-tts.md`

## Cổng trước Phase 2

- [ ] Chủ dự án quyết định D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020
- [ ] Trước khi tuyên bố không chồng tải: bổ sung bằng chứng tác vụ trong daemon Ollama đã kết thúc (mở rộng FI-43)

## TikTok Direct Post (`POLICY BLOCKED`)

- [ ] G1: hồ sơ đánh giá chính sách cập nhật, có dẫn nguồn
- [ ] G2: xác minh phương án sử dụng cụ thể đáp ứng Intended Use
- [ ] G3: bằng chứng về quyền truy cập, OAuth, scope, điều kiện nền tảng
- [ ] G4: Rights Gate, Human Approval, bảo mật, publishing reliability đáp ứng theo Phase
- [ ] G5: quyết định triển khai riêng của Project Owner

## Các phase sau

Xem [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Công việc chi tiết được thêm khi phase được duyệt.

## Scope Grants

Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) mục 3.

### SG-001 – Tài liệu workflow Claude–Codex mức B
- Cấp bởi / ngày: Project Owner / 2026-10-30
- Lời Owner: "Project Owner cho phép triển khai tài liệu quy trình phối hợp Claude–Codex ở mức B: file-based handoff, manual tool invocation. Đây là phê duyệt có điều kiện, chỉ dành cho việc hoàn thiện tài liệu workflow. Không phải quyền tự động điều phối công cụ, commit, push hoặc bắt đầu Phase 1."
- Mục tiêu: hoàn thiện tài liệu workflow mức B và bàn giao Codex review
- Được sửa: `docs/operations/AI_REVIEW_WORKFLOW.md`, `AGENTS.md`, `CLAUDE.md`, `TASKS.md`, `docs/workflows/README.md`, `docs/operations/README.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`
- Không được sửa: `DECISIONS.md`, `PROJECT_MASTER.md`, tài liệu kiến trúc, và mọi file không nêu ở dòng trên, gồm `REVIEW_RESPONSE.md`, `CURRENT_STATUS.md`
- Tiêu chí xong: đủ 12 yêu cầu của Owner, kiểm tra mục 6 của yêu cầu đạt, Codex review
- Giới hạn vòng: 3
- Trạng thái: DONE
- Đóng bởi / ngày: Project Owner / 2026-10-30. Lời Owner: "Nghiệm thu, đóng SG". Đã dùng 1/3 vòng; Codex `APPROVED` tại RR-002

#### SG-001 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-30
- Lời Owner: "Project Owner đã phê duyệt SG-001 Amendment A01 để khắc phục hai phát hiện từ Codex" và "Amendment A01 là phần bổ sung quyền cho SG-001, không phải một Scope Grant mới."
- Purpose: Resolve F-001 and F-002
- Original Scope Grant: SG-001, retained
- Original review: RR-001, round 0/3
- Next review: round 1/3
- Round counter: NOT RESET
- Claude được ghi thêm: `REVIEW_RESPONSE.md`, chỉ để phản hồi finding và tạo Review Request liên quan đến SG-001. Các file Claude khác giữ nguyên như dòng "Được sửa" của SG-001
- Codex được ghi: `docs/operations/reviews/PHASE-00-REVIEW.md`, chỉ cho báo cáo review
- Không mở rộng quyền sang file khác. Dòng "Không được sửa" của SG-001 vẫn áp dụng, trừ `REVIEW_RESPONSE.md` trong giới hạn trên
- Không cấp quyền commit, push, tạo nhánh, sửa quyết định `Proposed` hay mở Phase 1

## Review Requests

Mục này luôn ở cuối file. Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) mục 6.

### RR-001
- Trạng thái: ANSWERED
- Scope Grant: SG-001
- Vòng: 0/3
- Thay thế RR: không có
- Baseline Git: def8fdf0b7871abada7dad228e31c1ee96dae7b3
- Phiên bản review: SHA-256 bên dưới
- SHA-256:
  - `AGENTS.md` d45cc7d12cf886e7bc093938ddf6174e966668ce52e16636acd65a53257a837b
  - `CHANGELOG.md` 88c9773433145eef58b66bf060b58d30ff2f7e0f3d5234fbb35a83a7eb804471
  - `CLAUDE.md` ca0c761d52eb40b4c757e06de3962715800741dd42bd5c647ffc50ca8f02191b
  - `HANDOFF_TO_CHATGPT.md` 0c8a2806cf1f004976f4e17ee823add1d7aa1859da3116fe64611310a9694102
  - `docs/operations/AI_REVIEW_WORKFLOW.md` 153cffdc5de75fda20ac9f868d362ae830e20fd4c77ed6ec623dde5b9f32c5a6
  - `docs/operations/README.md` 039a53b45de3b87bbe82d60f96d1af338180015e326c9f15b42d98314f7564cd
  - `docs/workflows/README.md` 75b3b3ec997b2acba1000bdee8d90497c3adac7d546aebd68180b6a384013e0f
  - `TASKS.md` (phần trước `## Review Requests`) 2d304d4419dc4cfaa4e18f2712ccd42f3973c10a94562752e28127fd46c3c655
- Lệnh đã chạy và kết quả thật: `git status --porcelain` có 8 mục, đều trong allowlist; `shasum -a 256` cho các file trên; `grep` xác nhận đủ 12 yêu cầu của Owner và hai lệnh cố định; kiểm tra liên kết tương đối không có lỗi; D-009 đến D-022 là `Proposed`, 14/14; Phase 0 `ACCEPTED`, Phase 1 `NOT AUTHORIZED`, TikTok Direct Post `POLICY BLOCKED` trong `CURRENT_STATUS.md`
- Chưa kiểm tra được: chưa có vòng thực tế nào theo workflow; RR-001 là lần đầu dùng mẫu này; không có runtime test vì không có code
- Finding cần xem lại: không có
- Phạm vi hồi quy: `AGENTS.md`, `CLAUDE.md`, `docs/workflows/README.md`
- Yêu cầu review cụ thể: (1) Có quyền tự phê duyệt, commit, push, tạo nhánh hay đường vượt Phase Gate nào phát sinh không? (2) Có xung đột quyền ghi không? (3) Có đường đặt lại giới hạn 3 vòng ngoài Owner không? (4) Hợp đồng RR, kiểm tra đầu vào và lệnh hash có khả thi với công cụ của Codex không? (5) `AGENTS.md`, `CLAUDE.md` và workflow có thống nhất không? (6) `REVIEW_RESPONSE.md` và `CURRENT_STATUS.md` nằm ngoài SG-001: đánh giá ảnh hưởng tới vòng sửa. (7) Xác nhận không có tuyên bố đã kiểm chứng mức B hay đạt mức C
- END-OF-REVIEW-REQUEST

### RR-002
- Trạng thái: ANSWERED
- Scope Grant: SG-001
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-001 (vòng 0/3, CHANGES REQUESTED)
- Amendment: A01
- Baseline Git: def8fdf0b7871abada7dad228e31c1ee96dae7b3
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A):
  - `AGENTS.md` 599da96de01f938e589341f529ef891fecf6a17e11c6c11dc6928ee7e27d351a
  - `CHANGELOG.md` d614efc545bcc0aa7e2e5da279470c7a47cfeed57dc122d165902ddbf0a0186e
  - `CLAUDE.md` dfabb9407e1e4e6e8e131170709800035df0a465c56826b601422f5922d083e4
  - `HANDOFF_TO_CHATGPT.md` bf528c532f3356ffa3b1fb160e844273c9841f593b202b993f4420480fc1a2b2
  - `REVIEW_RESPONSE.md` fc7c026ba8230ec4e73a4606a63b18eb67826af5cc977485a7db8f40a5d708e4
  - `docs/operations/AI_REVIEW_WORKFLOW.md` 90305710bd3cedda08534e6d99db8283dea9388fab2f42c350cba2c310b394fc
  - `docs/operations/README.md` 039a53b45de3b87bbe82d60f96d1af338180015e326c9f15b42d98314f7564cd
  - `docs/workflows/README.md` 75b3b3ec997b2acba1000bdee8d90497c3adac7d546aebd68180b6a384013e0f
  - `TASKS.md` (phần trước `## Review Requests`) b7b81a64b8164557c503fa9677a8aec4ef7f566711afb79838983d3b2d109a7e
- Reviewer artifact (nhóm B) lúc bàn giao:
  - `docs/operations/reviews/PHASE-00-REVIEW.md` 51118 b89b19418301f1ebe577e5928d19ec0a1795ad2fc9096eec55937e204cc10944
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-002` mới ở đầu file; toàn bộ nội dung cũ giữ nguyên
- Lệnh đã chạy và kết quả thật: xem `REVIEW_RESPONSE.md`, mục "Bằng chứng đã chạy" của phần SG-001. Kiểm tra sau khi đăng RR-002 được Claude báo cáo riêng cho Owner trong chat
- Chưa kiểm tra được: xem `REVIEW_RESPONSE.md`, mục "Chưa thể kiểm chứng" của phần SG-001. Không có runtime test vì không có code
- Finding cần xem lại: F-001, F-002
- Phạm vi hồi quy: quyền ghi, kiểm tra toàn vẹn, bộ đếm vòng, không có quyền commit, push, nghiệm thu; `AGENTS.md`, `CLAUDE.md`; bảng A, B, C trong workflow
- Yêu cầu review cụ thể: (1) F-001: nhóm A, B, C có giải quyết bế tắc mà không tạo đường bỏ qua integrity không? Kiểm tra lệnh `tail -c` với số byte và hash ở trên. (2) F-002: quyền ghi `REVIEW_RESPONSE.md` có đúng giới hạn A01 không? (3) RR-002 tiếp nối RR-001 có giữ đúng bộ đếm vòng không? (4) Bản đối chiếu trong `REVIEW_RESPONSE.md` có tạo hai yêu cầu đang mở không? (5) Có quyền mới nào phát sinh không? (6) Chỉ Codex đóng finding; kết luận thuộc về Codex
- END-OF-REVIEW-REQUEST
