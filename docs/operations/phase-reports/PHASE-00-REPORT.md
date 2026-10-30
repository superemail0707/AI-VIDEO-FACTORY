# Báo cáo Phase 0 – Hồ sơ dự án

- Ngày: 2026-10-30
- Nhánh / commit: `main`, chưa có commit
- Trạng thái: đã nghiệm thu ngày 2026-10-30, xem mục "Nghiệm thu chính thức" ở cuối báo cáo

## Tóm tắt

Đã tạo bộ tài liệu quản lý dự án. Không có code ứng dụng, không cài phần mềm, không tải model, không tạo credentials, không tích hợp mạng xã hội.

Brief ghi thư mục "hoàn toàn trống", nhưng thực tế khi làm việc đã có khung file rỗng, `.git/` do Chủ dự án khởi tạo, quy tắc bàn giao trong `CLAUDE.md`, và `HANDOFF_TO_CHATGPT.md` đang mở trong `vi` (chưa lưu xuống đĩa). Không có dữ liệu nào bị xóa hoặc ghi đè.

## File đã tạo hoặc sửa

**Tệp gốc (ghi vào tệp rỗng có sẵn):** `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`, `AGENTS.md`, `.gitignore`.

**Sửa:** `CLAUDE.md` – thêm phần hướng dẫn phía trên; quy tắc của Chủ dự án giữ nguyên.

**Tạo mới:** `docs/README.md`, `README.md` trong tám thư mục con của `docs/`, `docs/operations/phase-report-template.md`, báo cáo này.

**Không động đến:** `HANDOFF_TO_CHATGPT.md`, `.HANDOFF_TO_CHATGPT.md.swp`, `.git/`.

## Lệnh đã chạy

Tất cả chỉ đọc; thay đổi tệp được thực hiện qua công cụ ghi tệp, không qua shell.

- Kiểm tra thư mục: `pwd`, `ls -la`, `find`, `wc -c`.
- Kiểm tra máy: `sw_vers`, `sysctl`, `df -h`, `command -v`, `xcode-select -p`.
- Kiểm tra Git: `git status`, `git log`, `git remote -v`, `git ls-files --others`, `git check-ignore`.
- Kiểm tra tiến trình giữ tệp: `lsof`, `ps`, `file`, `stat`.
- Kiểm tra nội dung: `grep`, `sed`, `tail`.

## Kết quả kiểm tra

Phase này không có test tự động vì chưa có code. Các kiểm tra sau đã chạy thật:

| Kiểm tra | Kết quả |
|---|---|
| `.gitignore` bỏ qua secret, DB, model, media, tệp swap (9 mẫu) | Đạt |
| `.gitignore` không bỏ qua nhầm `.env.example`, thư mục code `models/`, `data/`, fixture test, `HANDOFF_TO_CHATGPT.md` (5 mẫu) | Đạt, sau khi sửa lỗi neo đường dẫn |
| Chỉ có `.md` và `.gitignore` được thêm | Đạt |
| Quét chuỗi giống secret | Không có |
| Quy tắc của Chủ dự án còn trong `CLAUDE.md` | Đạt |
| FFmpeg, Ollama, uv vẫn chưa có | Đạt |
| Liên kết tương đối trong tài liệu | Đạt, kiểm tra lại sau khi tạo báo cáo này |

Các ước tính về RAM, dung lượng, tốc độ trong tài liệu là **giả định chưa đo**, được đánh dấu rõ. Thông tin chính sách API và license chưa được đối chiếu với nguồn chính thức trong phase này.

## Tình trạng tính năng

| Thành phần | Trạng thái |
|---|---|
| Tài liệu Phase 0 | Đã triển khai & kiểm thử ở mức trên, chờ nghiệm thu |
| Cập nhật `HANDOFF_TO_CHATGPT.md` | Chưa làm, bị chặn vì tệp đang mở |
| Mọi tính năng sản phẩm | Chưa làm |

## Quyết định mới

- `Approved` (ghi lại từ brief): D-001 đến D-007.
- `Accepted (Lead)`: D-008.
- `Proposed`, chờ duyệt: D-009 đến D-017.

## Vấn đề chưa giải quyết

1. Máy là MacBook Air không quạt: thông lượng render khi chạy lâu có thể thấp hơn nhiều so với lúc chạy ngắn. Mục tiêu một video mỗi ngày chưa được chứng minh.
2. Chưa xác định được giọng tiếng Việt miễn phí, chất lượng tốt, đúng license.
3. Chính sách API có thể chặn đăng công khai cho tới khi app được duyệt.
4. `HANDOFF_TO_CHATGPT.md` chưa tồn tại trên đĩa.
5. Các câu hỏi Q-01 đến Q-09 trong `CURRENT_STATUS.md`.

## Yêu cầu review cho Codex

1. Đối chiếu `ARCHITECTURE.md` với `PROJECT_MASTER.md`: có thay đổi kiến trúc chưa được duyệt không? Mục `[Đề xuất]` nào thực chất là thay đổi cốt lõi?
2. Thiết kế lease và heartbeat của Job Queue có kẽ hở khi máy ngủ, nhất là tình huống hai lần chạy cùng một job?
3. Thứ tự phase có đẩy rủi ro lớn nhất (R1, R2) ra đủ sớm không?
4. Mục 10 của `ARCHITECTURE.md` có thiếu rủi ro bảo mật nào, đặc biệt prompt injection qua Athena?
5. Thiếu sót của `.gitignore` đối với secret.
6. Quy tắc lượt làm việc Claude–Codex có khả thi và đủ chặt không?
7. Đối chiếu ràng buộc API và license ở `TECH_STACK.md` với tài liệu chính thức hiện hành.

## Bước tiếp theo đề xuất

Chủ dự án nghiệm thu và trả lời Q-01, Q-06, Q-09. Sau đó Claude trình bày kế hoạch chi tiết Phase 1 và chờ xác nhận. **Claude không tự bắt đầu Phase 1.**

---

## Phụ lục: Bản sửa 1 (2026-10-30)

Phần trên giữ nguyên làm lịch sử. Một số nội dung đã được thay thế: danh sách câu hỏi, bước tiếp theo, trạng thái tệp handoff.

**Bối cảnh:** Codex kết luận NEEDS REVISION ([REVIEW_REPORT.md](../../../REVIEW_REPORT.md)). Chủ dự án yêu cầu sửa tài liệu, không code. Phản hồi: [REVIEW_RESPONSE.md](../../../REVIEW_RESPONSE.md). Danh sách thay đổi: [CHANGELOG.md](../../../CHANGELOG.md).

**Lệnh đã chạy (chỉ đọc):** `ls`, `find`, `git status`, `git log`, `git branch`, `git remote`, `git check-ignore`, `git ls-files`, `ps`, `strings`, `tail`, `grep`, `sed`, `wc`, `tr`, `command -v`. Đọc ba trang tài liệu chính thức của YouTube, TikTok, Facebook.

**Kết quả kiểm tra:** không có test tự động vì không có code. Các kiểm tra tài liệu đã chạy thật:

| Kiểm tra | Kết quả |
|---|---|
| Chỉ có tệp `.md` và `.gitignore`, không có code | Đạt |
| Liên kết tương đối trong tài liệu | Không có liên kết hỏng |
| D-009 đến D-022 đều `Proposed`; không nơi nào ghi đã duyệt | Đạt |
| Không nơi nào ghi Phase 0 đã nghiệm thu | Đạt |
| 24 mục BLOCKER, WARNING, RECOMMENDATION đều có phản hồi | Đạt |
| Đặc tả đủ 9 AC-Q, 21 FI, 3 MT, 11 AC-P, 13 PF | Đạt |
| `.gitignore`: 7 mẫu bị bỏ qua, 3 mẫu vẫn theo dõi | Đạt (tự kiểm tra) |
| Quét chuỗi giống secret | Không có |
| `CLAUDE.md`, `.gitignore`, `REVIEW_REPORT.md` không đổi (theo thời gian sửa) | Đạt |
| FFmpeg, Ollama, uv vẫn chưa có | Đạt |

Các đặc tả là thiết kế, **chưa được kiểm chứng bằng code**. Tính đúng đắn của fencing chỉ mới được lập luận và chờ Codex review.

**Kết luận:** Phase 0 vẫn chưa được nghiệm thu. Bước tiếp theo đề xuất là Codex review lần 2.

---

## Phụ lục 2: Bản sửa 2 (2026-10-30)

Phát hiện vòng 2 do Chủ dự án chuyển; repo không có tệp báo cáo gốc. Phản hồi từng mục: [REVIEW_RESPONSE.md](../../../REVIEW_RESPONSE.md).

**Đính chính:** các dòng về `.gitignore` ở báo cáo gốc và Phụ lục 1 ghi "Đạt" là **không đủ căn cứ**. Các kiểm tra đó không thử secret bên trong `tests/fixtures`, và quy tắc `!tests/fixtures/**` thực tế đã làm lộ các tệp này.

### Xác minh `.gitignore`

Môi trường: repo dự án, nhánh `main`. `tests/` chưa tồn tại, nên kiểm tra A–C đánh giá đường dẫn giả định; kiểm tra D dùng tệp thật trong repo thử ở thư mục tạm của phiên.

**Tái hiện lỗi trước khi sửa:**

```bash
git check-ignore --no-index -q tests/fixtures/secret.env; echo "exit=$?"
```

Vòng lặp dùng lệnh này cho 7 đường dẫn: `secret.env`, `token.json`, `voice.mp3`, `model.gguf`, `test.db`, `x.pem`, `secrets/a.json` trong `tests/fixtures/`. Kết quả: **cả 7 đều không bị bỏ qua.**

**A. Phải bị bỏ qua** (`exit=0`):

```bash
git check-ignore --no-index -q "$p"; echo "exit=$? $p"
```

| Đường dẫn | Kết quả |
|---|---|
| `tests/fixtures/secret.env` | exit=0 |
| `tests/fixtures/token.json` | exit=0 |
| `tests/fixtures/voice.mp3` | exit=0 |
| `tests/fixtures/model.gguf` | exit=0 |
| `tests/fixtures/test.db` | exit=0 |
| `tests/fixtures/.env`, `.env.local` | exit=0 |
| `tests/fixtures/x.pem`, `x.key` | exit=0 |
| `tests/fixtures/client_secret_1.json`, `credentials.json`, `oauth_state.json`, `service-account.json` | exit=0 |
| `tests/fixtures/my_token.txt`, `password.txt` | exit=0 |
| `tests/fixtures/secrets/a.json`, `sub/token.json`, `sub/clip.mp4` | exit=0 |
| `tests/fixtures/a.wav`, `a.sqlite3`, `m.safetensors`, `run.log`, `image.png`, `script.sh` | exit=0 |
| `.env`, `secret.env`, `token.json`, `db.sqlite3`, `workspace/spikes/tts/a.wav`, `models/m.gguf` | exit=0 |

Tổng: 30/30 đạt.

**B. Phải theo dõi được** (`exit=1`), cùng lệnh:

| Đường dẫn | Kết quả |
|---|---|
| `tests/fixtures/scene_spec.json`, `sub/storyboard.json` | exit=1 |
| `tests/fixtures/script_vi.txt`, `notes.md`, `data.csv`, `character.svg`, `subs.srt`, `subs.vtt` | exit=1 |
| `.env.example`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md` | exit=1 |
| `src/ai_video_factory/models/x.py`, `src/ai_video_factory/data/x.py` | exit=1 |

Tổng: 13/13 đạt.

**C. Quy tắc quyết định:**

```bash
git check-ignore --no-index -v -n tests/fixtures/secret.env tests/fixtures/token.json tests/fixtures/voice.mp3 tests/fixtures/model.gguf tests/fixtures/test.db tests/fixtures/scene_spec.json
```

```text
.gitignore:122:/tests/fixtures/**/*.env	tests/fixtures/secret.env
.gitignore:118:/tests/fixtures/**/*token*	tests/fixtures/token.json
.gitignore:52:*.mp3	tests/fixtures/voice.mp3
.gitignore:37:*.gguf	tests/fixtures/model.gguf
.gitignore:31:*.db	tests/fixtures/test.db
.gitignore:9:!/tests/fixtures/**/*.json	tests/fixtures/scene_spec.json
```

**D. Tệp thật trong repo thử:** tạo 19 tệp trong `tests/fixtures/` và `.env.example`, chép `.gitignore` sang, rồi chạy:

```bash
git add -A --dry-run
```

Chỉ 10 tệp được nhận: `.env.example`, `.gitignore`, `character.svg`, `data.csv`, `notes.md`, `scene_spec.json`, `script_vi.txt`, `sub/storyboard.json`, `subs.srt`, `subs.vtt`. Mọi tệp secret, token, media, model, DB, ảnh đều bị loại.

**Giới hạn:** `.gitignore` lọc theo tên, không theo nội dung. Quét secret vẫn cần trước mỗi commit.

### Lệnh khác đã chạy

Chỉ đọc trên repo: `ls`, `find`, `ps`, `git status`, `git log`, `git config --get`, `grep`, `sed`, `wc`, `stat`. Trong repo thử ở thư mục tạm: `git init`, `cp`, `mkdir`, `git add -A --dry-run`. Đọc tài liệu chính thức của TikTok, Google, Facebook.

### Kết quả kiểm tra tài liệu

Không có test tự động vì chưa có code. Mọi FI, MT, PF, AC đều **chưa chạy**. Các kiểm tra tài liệu đã chạy thật:

| Kiểm tra | Kết quả |
|---|---|
| Chỉ có tệp `.md` và `.gitignore`; `src/`, `tests/` chưa tồn tại | Đạt |
| Liên kết tương đối | Không có liên kết hỏng |
| D-009 đến D-022 đều `Proposed` | Đạt, 14/14 |
| Không ghi Phase 0 đã nghiệm thu, queue đã an toàn, hay đã tuân thủ nền tảng | Đạt |
| Bảng FI và MT: 46 dòng, đủ cột, không trùng mã | Đạt |
| Bảng T: 10 dòng; PF: 22; AC-P: 17; AC-S và AC-R: 17 | Đạt |
| Quét chuỗi giống secret | Không có |
| `CLAUDE.md`, `REVIEW_REPORT.md` không đổi (theo thời gian sửa) | Đạt |
| FFmpeg, Ollama, uv vẫn chưa có | Đạt |

### Kết luận

Phase 0 **chưa được nghiệm thu**. Queue **chưa được chứng minh an toàn**. Không có quyết định `Proposed` nào được duyệt.

---

## Phụ lục 3: Bản sửa 3 (2026-10-30)

**Bối cảnh:** Codex review vòng 3 ([PHASE-00-REVIEW.md](../reviews/PHASE-00-REVIEW.md)) kết luận CHANGES REQUESTED. Chủ dự án yêu cầu xử lý R3-01, R3-02, R3-03 trong tài liệu. Codex đã chạy lại độc lập kiểm tra `.gitignore` của Phụ lục 2: 30/30 và 13/13 khớp. Phản hồi: [REVIEW_RESPONSE.md](../../../REVIEW_RESPONSE.md).

| Mã | Mức | Kết quả |
|---|---|---|
| R3-01 | HIGH | Đã ghi nhận và chặn TikTok trong tài liệu. **Chưa giải quyết:** chờ Chủ dự án quyết định D-023, Q-13 |
| R3-02 | MEDIUM | Đã đặc tả, chưa triển khai, chưa kiểm thử |
| R3-03 | LOW | Đã đặc tả, chưa triển khai, chưa kiểm thử |

**Lệnh đã chạy (chỉ đọc):** `grep`, `find`, `ls`, `sed`, `awk`, `stat`, `ps`, `git status`, `git log`, `git ls-files`, `git check-ignore --no-index`, `command -v`. Đọc hai trang tài liệu TikTok.

**Kết quả kiểm tra tài liệu.** Không có test tự động vì chưa có code. Mọi FI, MT, PF, AC đều **chưa chạy**.

| Kiểm tra | Kết quả |
|---|---|
| Chỉ có tệp `.md` và `.gitignore`; `src/`, `tests/` chưa tồn tại | Đạt |
| Liên kết tương đối | Không có liên kết hỏng |
| D-009 đến D-023 đều `Proposed` | Đạt, 15/15 |
| Bảng FI và MT: 54 dòng, đủ cột, không trùng mã | Đạt |
| AC-Q: 19; bảng T: 13 dòng | Đạt |
| Không ghi queue đã an toàn hay R3-01 đã giải quyết | Đạt |
| `.gitignore` không đổi; 5 đường dẫn bắt buộc vẫn bị bỏ qua | Đạt |
| `CLAUDE.md`, `REVIEW_REPORT.md`, báo cáo Codex không đổi | Đạt |
| Quét chuỗi giống secret | Không có |
| FFmpeg, Ollama, uv vẫn chưa có | Đạt |

**Chưa thể xác minh:** chưa có review lại Bản sửa 3. TikTok chưa nhận hồ sơ audit nào, nên chưa có quyết định thực tế từ TikTok. Luồng Upload vào inbox chưa xác minh.

**Kết luận:** Phase 0 **chưa được nghiệm thu**. Không có quyết định `Proposed` nào được duyệt.

---

## Phụ lục 4: Ghi nhận D-023 và khắc phục R4-01 (2026-10-30)

Phần trên giữ nguyên làm lịch sử. Dòng "D-009 đến D-023 đều `Proposed`" ở Phụ lục 3 đúng tại thời điểm đó; hiện D-023 là `Approved`, D-009 đến D-022 vẫn `Proposed`.

**Quyết định:** Project Owner phê duyệt D-023/Q-13, phương án C, ngày 2026-10-30, trong cuộc trao đổi với ChatGPT Architecture Advisor, và chuyển quyết định cho Claude. Repo không lưu biên bản cuộc trao đổi đó.

**R4-01:** đã sửa trong tài liệu, chờ Codex kiểm tra lại. Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. Cổng G1–G5 ở `docs/deployment/platform-verification.md` mục 3.

**Kết quả kiểm tra.** Chỉ đọc tài liệu và trạng thái repo; không có runtime test.

| Mã | Kiểm tra | Kết quả |
|---|---|---|
| TC-01 | D-023 có đúng một bản ghi, `Approved`, nằm ở mục "Đã duyệt" | PASS |
| TC-02 | `POLICY BLOCKED` có ở 7 tài liệu đồng bộ | PASS |
| TC-03 | Không tài liệu nào khẳng định D-023 tự động cho phép triển khai; mọi dòng khớp đều là câu phủ định | PASS |
| TC-04 | Factory Manager và 7 Agent không đổi | PASS |
| TC-05 | Không ghi Phase 0 đã nghiệm thu; Phase 1 chưa được phép | PASS |
| TC-06 | D-009 đến D-022 đều `Proposed`, 14/14 | PASS |
| TC-07 | Không có mâu thuẫn trong các file thuộc phạm vi; ba dòng lỗi thời ngoài phạm vi được ghi tại `REVIEW_RESPONSE.md` | PASS, có ghi chú |
| TC-08 | Chỉ có `.md` và `.gitignore`; không có `src/`, `tests/`, commit hay nhánh mới | PASS |

**Kết luận:** Phase 0 **NOT ACCEPTED**. Phase 1 **NOT AUTHORIZED**. TikTok Direct Post **POLICY BLOCKED**.

---

## Nghiệm thu chính thức

Các kết luận "chưa nghiệm thu" ở trên đúng tại thời điểm viết và được giữ làm lịch sử.

| Mục | Nội dung |
|---|---|
| Kết quả | **PHASE 0 — ACCEPTED** |
| Ngày nghiệm thu | 2026-10-30 |
| Người nghiệm thu | Project Owner |
| Căn cứ | Codex Final F-01 Verification: `PASS — READY FOR OWNER ACCEPTANCE`; F-01 CLOSED; R4-01 CLOSED; các phát hiện Review 3 đã được giải quyết ở mức hồ sơ và đặc tả; Project Owner trực tiếp xác nhận |

**Phạm vi được chấp nhận:** hồ sơ nền tảng dự án; mục tiêu và phạm vi sản phẩm; kiến trúc tổng thể; Factory Manager và 7 Agent; tech stack định hướng; Implementation Plan; Decision Log; các đặc tả kỹ thuật và kế hoạch kiểm thử; quy tắc bảo mật, bản quyền và publishing; quy trình phối hợp Claude, Codex và Project Owner.

**Không xác nhận:** application code đã được triển khai, runtime test đã pass, hay toàn bộ AI Video Factory đã hoàn thành. Nghiệm thu không cho phép bắt đầu Phase 1.

**Giới hạn chưa được kiểm chứng bằng runtime:**

- Toàn bộ FI, MT, PF và AC đều chưa chạy; tính an toàn của queue chưa được chứng minh.
- `flock` qua FFmpeg, độ bền `F_FULLFSYNC`, cách ly Keychain giữa các tiến trình.
- Việc tác vụ trong daemon Ollama đã kết thúc trước job mới (FI-43 chưa chứng minh).
- OAuth, Rights Gate và publishing chưa được triển khai.
- Hiệu năng, nhiệt, RAM, chất lượng TTS tiếng Việt và mục tiêu một video mỗi ngày chưa có số đo.

**Rủi ro và cổng quyết định chuyển sang phase tiếp theo:**

| Mục | Nội dung |
|---|---|
| Vào Phase 1 | Quyết định D-013, D-017; trả lời Q-03, Q-06; kế hoạch Phase 1 được xác nhận. Trạng thái: **NOT AUTHORIZED** |
| Vào Phase 2 | Quyết định D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020 |
| Sau đó | D-012, D-014 trước Phase 4; D-022 trước Phase 13; D-019, D-021, D-015 (Keychain) trước Phase 15 |
| D-009 đến D-022 | Vẫn `Proposed`; nghiệm thu Phase 0 không phê duyệt các quyết định này |
| TikTok Direct Post | D-023 `Approved — Option C`, Q-13 `Answered — Option C`; tích hợp vẫn `POLICY BLOCKED`, cần G1–G5 |
| R3-01 | Rủi ro chính sách chưa được giải quyết |
| Facebook, Upload inbox | Chưa xác minh |
| Rủi ro lớn nhất cần đo | R1 (TTS tiếng Việt), R2 (render, nhiệt) |

---

## Chuẩn bị Git checkpoint (chỉ đọc, 2026-10-30)

**Git checkpoint: PENDING PREPARATION / OWNER AUTHORIZATION.** Không chạy `git add` trên index thật, không commit, không tag, không fetch, không push, không sửa remote. `.gitignore` không đổi.

**Trạng thái thực tế:**

| Mục | Kết quả |
|---|---|
| Nhánh, HEAD | `main`, chưa có HEAD, chưa có `.git/index`, 0 file được theo dõi, 0 tag |
| File chưa theo dõi | 30 (29 `.md` và `.gitignore`), đều là văn bản, tổng 292 KB |
| File bị bỏ qua | 1: `.HANDOFF_TO_CHATGPT.md.swp` |
| Remote | `origin`, không có userinfo hay token trong URL, không có `pushurl` riêng |
| `user.name`, `user.email` | **Đều chưa cấu hình.** Commit sẽ thất bại cho tới khi có danh tính |
| Hook đang hoạt động | Không có |
| Object trong `.git` | 103 blob, 68 tree, 0 commit, từ `refs/codex/turn-diffs/...` do Codex tạo. Không do Claude tạo |
| `FETCH_HEAD` | Rỗng, tạo lúc 22:38:57, không do Claude tạo; không có remote ref nào được lưu |

**`.gitignore`:** chạy lại `git check-ignore --no-index -q` trên bộ 43 mẫu: 30/30 phải bỏ qua, 13/13 được phép. PASS.

**Quét nội dung 30 file:** không có API key, token, private key, JWT, bearer, cặp khóa–giá trị bí mật, hay URL chứa thông tin đăng nhập. Một dòng khớp mẫu chuỗi dài (`PHASE-00-REVIEW.md:244`) là đường dẫn URL tài liệu Google, không phải secret. Không có email cá nhân, đường dẫn home hay tên tài khoản macOS. 103 blob trong `.git` được quét theo các mẫu khóa chính: 0 trúng. Đây là quét theo mẫu, không chứng minh tuyệt đối.

**Mô phỏng staging** trong bản sao ở thư mục tạm: đúng 30 mục, khớp kế hoạch, tệp swap bị loại.

**Phân loại:**

| Nhóm | File |
|---|---|
| **SAFE TO COMMIT** (29) | 14 tệp gốc: `.gitignore`, `AGENTS.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `CLAUDE.md`, `CURRENT_STATUS.md`, `DECISIONS.md`, `HANDOFF_TO_CHATGPT.md`, `IMPLEMENTATION_PLAN.md`, `PROJECT_MASTER.md`, `REVIEW_REPORT.md`, `REVIEW_RESPONSE.md`, `TASKS.md`, `TECH_STACK.md`. 15 tệp trong `docs/`, gồm mọi tệp trừ tệp ở nhóm dưới |
| **REQUIRES REVIEW** (1) | `docs/operations/reviews/PHASE-00-REVIEW.md`: tệp của Codex, có tên tài khoản GitHub trong URL remote ở dòng 41 |
| **MUST NOT COMMIT** (1) | `.HANDOFF_TO_CHATGPT.md.swp`; hiện đã bị bỏ qua |

**Cần Project Owner quyết định trước checkpoint:**

1. Cho phép tạo commit đầu tiên, và cung cấp danh tính Git.
2. Xác nhận URL `origin` là đúng repository dự kiến. Repo không có giá trị tham chiếu nào để đối chiếu.
3. Xác nhận repository từ xa là riêng tư hay công khai. Chưa kiểm tra vì không được fetch.

`PROJECT_MASTER.md:8, 44` đã được sửa theo chỉ đạo của Project Owner: dòng 8 ghi Phase 0 `ACCEPTED` và Phase 1 `NOT AUTHORIZED`, dòng 44 bỏ tên máy.

**Cập nhật:** Codex Acceptance & Git Checkpoint Review kết luận `PASS — READY FOR OWNER CHECKPOINT AUTHORIZATION`. Project Owner sau đó cho phép commit và chọn danh tính cho commit đầu tiên. Commit được tạo cục bộ trên `main`, thêm 30 file theo danh sách tường minh. Danh tính được truyền riêng cho commit đó, không ghi vào cấu hình Git. **Chưa push;** mục 2 và 3 ở trên còn mở.

**Lưu ý khi thực hiện sau này:** thêm file theo danh sách tường minh, không dùng `git add .`. Chỉ push nhánh `main`; không dùng `git push --mirror`, vì lệnh đó sẽ đẩy cả `refs/codex/...`.
