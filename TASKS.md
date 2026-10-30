# AI VIDEO FACTORY – TASKS

Trạng thái: `[ ]` chưa làm, `[~]` đang làm, `[x]` xong và có kiểm chứng, `[!]` bị chặn.

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
- [ ] Push, sau khi được cho phép riêng

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
