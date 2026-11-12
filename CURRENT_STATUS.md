# AI VIDEO FACTORY – CURRENT STATUS

## Lần đăng thật đầu tiên qua pipeline tự động — ep08, 08/11/2026

- Owner chạy `approve-episode ngay-dau-yeu-vs-nam-thu-3` (lần đầu bị từ chối đúng thiết kế vì dòng xác nhận trống; sau đó sửa hiển thị tiếng Việt đọc được và in câu xác nhận riêng dòng).
- **Facebook:** `PUBLISHED_VERIFIED` — https://www.facebook.com/reel/2075754759737101 (đọc lại từ Meta: đúng Trang, đã công khai).
- **YouTube:** lần 1 Postiz `ERROR` ("Blocked IP" + không có gì nghe ở cổng 4007 trong container) → sửa theo D-028 (socat `postiz-loopback`, `DISABLE_SSRF_PROTECTION=true`) → Owner `resubmit` → `PUBLISHED_VERIFIED` riêng tư https://www.youtube.com/watch?v=sGOFpsIBa-M, xác minh bằng YouTube Data API đúng kênh; `youtube_contract.json` đã ghi → các tập sau YouTube tự `public`.
- **TikTok:** cùng lỗi, sau `resubmit` → `MANUAL_COMPLETION_REQUIRED` (đã vào hộp nháp TikTok; Owner bấm Đăng trong app).
- Unit test: 225/225 OK. `doctor`: facebook `DIRECT_READY`, youtube `PUBLIC_READY`, tiktok `INBOX_UPLOAD_ONLY`. Worker LaunchAgent đang chạy.
- Còn lại: Owner hoàn tất TikTok trong app; app Facebook bật Live; TikTok Production review; Codex review D-026/D-027/D-028; chưa commit.

## Tự động hoá đăng 3 nền tảng (D-027) — 08/11/2026

Owner: "Tôi muốn tất cả tự động hoá"; chọn 1 lần duyệt/tập, TikTok inbox + xin Direct Post, YouTube công bố AI trong mô tả, worker chạy nền launchd. Codex chưa review.

- **Đã triển khai:** `publishing/episode.py` (Tesla soạn nội dung từ `caption.txt`/`post.json`, lọc câu engagement bait, thêm câu hỏi bình luận, dòng công bố AI; chặn gói có nhạc bên thứ ba nếu không có `rights.json` của Owner); CLI `prepare-episode`, `approve-episode` (một cụm xác nhận cho cả tập), `episode-status`, `service install|uninstall|status`; cổng LIVE mới trong worker (TikTok chỉ `UPLOAD`; YouTube bắt buộc bộ xác minh, lần đầu `private`, ghi `youtube_contract.json` khi xác minh đúng kênh; Facebook qua adapter D-026, có chờ lịch); `verifiers.py` (YouTube Data API bằng token Postiz, dự phòng oEmbed); `doctor` báo trạng thái LIVE từng nền tảng. Website chính sách: https://superemail0707.github.io/ngangmotti/ (repo `superemail0707/ngangmotti`, có file xác minh TikTok). TikTok Sandbox đã kết nối trong Postiz.
- **Đã kiểm thử:** `PYTHONPATH=src python3 -m unittest discover -s tests/unit` → 219/219 OK (29 test mới trong `tests/unit/test_automation.py`). Chạy Tesla trên gói thật `ngay-dau-yeu-vs-nam-thu-3` → 3 manifest hợp lệ; gói `vi-anh-qua-dep-trai` bị chặn `POLICY_BLOCKED` vì dùng bài hát "Vì anh quá đẹp trai" (Trúc Nhân ft. Wren Evans) chưa có bằng chứng license. `doctor`, `service status` chạy thật.
- **Chưa kiểm chứng:** chưa chạy `prepare-episode`/`approve-episode`/`work` trên dữ liệu thật (thiếu API key Postiz trong Keychain và `init`); chưa cài LaunchAgent; chưa có lần đăng thật nào lên YouTube/TikTok qua pipeline; bộ xác minh YouTube mới chỉ unit test.
- **Phát hiện:** bản YouTube Shorts và Facebook Reels của ep08 trùng byte (đúng thiết kế bố cục v2, cột "vùng phụ đề" trong README `videos-post` đã cũ).
- **Owner cần làm:** tạo API key Postiz → Keychain; `init`; `prepare-episode videos-post/<slug>`; `approve-episode <slug>`; `service install`. App Facebook bật Live (URL chính sách mới). TikTok: nộp Production theo `docs/postiz/TIKTOK_PRODUCTION_REVIEW.md`.

## Facebook Reels đăng trực tiếp (D-026) — 08/11/2026

Owner giao trực tiếp: "fix để đăng video tự động lên Facebook", duyệt phương án A ("Approve option A"). Codex chưa review.

- **Lỗi đã sửa:** (1) `FACEBOOK_APP_ID`/`SECRET` trống trong env riêng của Postiz → điền App ID, Owner tự điền secret; Meta xác thực cặp ID/secret `CREDENTIALS_OK`. (2) Postiz gửi Meta `file_url=http://localhost:4007/uploads/...`, Meta không tải được → đăng video Facebook qua Postiz chắc chắn lỗi. Thay bằng adapter `src/ai_video_factory/publishing/facebook_reels.py` upload thẳng byte MP4 (Graph API `video_reels` + `rupload.facebook.com`).
- **Đã triển khai:** adapter; worker định tuyến Facebook qua adapter (`facebook=`), ranh giới bền trước bước `finish` không lặp lại, đọc lại từ Meta làm xác minh `PUBLISHED_VERIFIED`; lệnh `facebook-draft-test MANIFEST` (cứng `DRAFT`); `work` nạp `facebook_contract.json`. Manifest ep08: `output/ep08_ngay_dau_vs_nam_ba/publish/facebook.dryrun.json` và `facebook.draft.json`.
- **Đã kiểm thử:** `PYTHONPATH=src python3 -m unittest discover -s tests/unit` → 190/190 OK (20 test mới trong `tests/unit/test_facebook_reels.py`). Test DRAFT thật: video `1124038717286057` trên Trang "Ngang Một Tí" (Page ID `1474012595784934`, hồ sơ `61596370679676`): upload/processing `complete`, `published=false`, Trang khớp → `PASS_DRAFT_ONLY`, ghi `~/Library/Application Support/AI Video Factory/publishing/facebook_contract.json`.
- **Chưa làm / chưa kiểm chứng:** chưa đăng công khai lần nào; chưa kiểm chứng nhánh `PUBLISHED` và đối soát `PUBLISHED_VERIFIED` với Meta thật (chỉ unit test). App Facebook có thể còn **Development mode** (bài chỉ hiện với người có vai trò) → Owner cần đăng Chính sách quyền riêng tư (bản nháp `docs/postiz/FACEBOOK_PRIVACY_POLICY_DRAFT.md`) và bật Live. Adapter chưa `init` (`owner.json`) nên chưa chạy được `enqueue/approve/work`. Mục `rights` của manifest ep08 là DRAFT chờ Owner xác nhận (giọng VieNeu v3 Turbo, P1-004). Page mới 0 người theo dõi, chưa đủ điều kiện kiếm tiền.
- **Bước tiếp:** Owner xóa hoặc giữ bản nháp reel trong Meta Business Suite; bật Live; chạy `init` trong terminal; `enqueue` manifest `LIVE` → `approve` → `work --once`. Codex review D-026 (đặc biệt: chấp nhận công bố AI trong caption cho hoạt hình 2D, đọc token từ Postgres của Postiz).

## NMT-engine — tên chính từ 08/11/2026

Owner giao trực tiếp đổi tên `couple-engine` thành **NMT-engine — Ngang Một Tí** và bổ sung mô tả/tài liệu. Đã thực hiện trong phạm vi engine nội dung, không đổi kiến trúc Factory Manager + 7 Agent hoặc trạng thái phase.

- Lệnh chính Claude Code: `/nmt-engine <chủ đề hoặc brief>`, tại `.claude/commands/nmt-engine.md`.
- CLI: `python3 output/_engine/nmt_engine.py list|status` và `new "<chủ đề>"`.
- Tài liệu chính: `output/_engine/NMT_ENGINE.md`; prompt dùng với AI/app khác: `output/_engine/NMT_ENGINE_PROMPT.md`.
- Mô tả đã bổ sung: dựng hoạt hình 2D Tí–Ngang–Mimi (thú cưng của Ngang), brief/kịch bản → storyboard → sprite/key pose → thoại/nhạc → phụ đề/outro → MP4 NMT. Dùng phong cách/mẫu đã duyệt, cổng duyệt kịch bản/hình/video, kiểm chất lượng và xuất `videos-post/`. Mức rig/lip-sync không được suy ra từ ảnh hoặc key pose.
- Tên cũ giữ alias CLI/slash command và redirect tài liệu. Renderer kỹ thuật vẫn `cute_engine.py`. Tập cũ, ID, workflow/hash và MP4 không bị đổi tên hay dựng lại; đọc `CURRENT_PREVIEW.json` khi tiếp tục một revision.
- Đã kiểm chứng 8 smoke checks: CLI help, list/status, alias cũ, bộ khung mới với chủ đề tiếng Việt trong thư mục tạm, brand NMT, template biên dịch được, syntax các module liên quan và SHA-256 của ba MP4 EP10 không đổi. Frontmatter YAML của hai slash command hợp lệ. Chưa thử thực thi slash command trong phiên UI Claude Code; chưa cài/đổi một skill độc lập trong Claude Desktop.
- Báo cáo đổi tên: `output/_engine/NMT_RENAME_REPORT.json`. Không cài dependency, tải model, tạo tập thật, render video, commit/push hay đăng bài trong nhiệm vụ này.


Cập nhật lần cuối: 2026-10-31 (Owner cho phép sửa file này sau khi đóng SG-002: đồng bộ SG-002 DONE, RR-006, Git `7115591`)

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
| Scope Grant | SG-001 **DONE**. **SG-002 DONE** (Project Owner đóng 2026-10-31, lời "đóng"). Đã dùng đủ vòng 0–3. Không có Scope Grant ACTIVE và không có Review Request đang mở. Các chỉ đạo trực tiếp A02–A07 (nhãn do Claude đặt, ghi trong `TASKS.md`) đã thực hiện: ghi D-024, cài Ollama, tải Qwen3 4B và 8B, đo thô 4B và 8B. Đóng SG **không** hợp thức hóa các thao tác đó và không cấp quyền mới |
| Review gần nhất | Codex **RR-006** (SG-002 vòng 3/3, cuối): **CHANGES REQUESTED** — P1-003 (MEDIUM, đồng bộ trạng thái) và P1-004 (LOW, lập luận VieNeu) đã sửa theo "Cho sửa, không review"; `FIX IMPLEMENTED — NOT RE-REVIEWED`, **chưa CLOSED**. RR-004, RR-005 APPROVED ([báo cáo](docs/operations/reviews/PHASE-01-REVIEW.md)). Phase 0: RR-002 APPROVED ([báo cáo](docs/operations/reviews/PHASE-00-REVIEW.md)). Phản hồi tại [REVIEW_RESPONSE.md](REVIEW_RESPONSE.md). Codex không đánh giá quyền của cài đặt, tải, đo, commit/push |
| D-023 | **APPROVED** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Lượt làm việc | Chủ dự án (Claude đã dừng) |
| Git | Nhánh `main` ở `7115591`, trùng `origin/main` (đã push; Project Owner nói "Cho commit" và "Cho push" trong chat; **chưa có bản ghi trong file repo trước khi thực hiện**). Thay đổi của file này chưa commit. **Repo từ xa là CÔNG KHAI** (Project Owner xác nhận) |
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
- **Chờ Owner (chưa trả lời):** việc kế tiếp của Phase 1 và quyền cho từng lệnh cài (FFmpeg, Python mới, thư viện rasterize, faster-whisper); đo nhiệt; chấm tiếng Việt chính thức; 4d (chuẩn hóa artifact reviewer vắng mặt); dọn mục D-013/D-017 lặp trong `DECISIONS.md`; xác nhận bằng văn bản quyền commit/push; hướng cho TTS tiếng Việt (R1, chưa có ứng viên nhóm B).
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

## Thư viện nhân vật — 2026-11-05

ComfyUI Python RECOVERED, PyTorch MPS tensor PASS. Thư viện có 90 PNG lập chỉ mục, 24 Draft, 27 In Review và 39 Needs Revision. Chờ Owner xem contact sheets. Xem [báo cáo thư viện](character_library/CHARACTER_ASSET_REPORT.md).

### Visual Quality Gate — 2026-11-05

Giữ 90 PNG nguồn, thêm 8 bản sửa Mimi. 98 PNG qua kiểm tra kỹ thuật cơ bản. 29 In Review, 68 Needs Revision, 1 Draft, 0 Approved. Cổng hiện tại là Owner duyệt contact sheets trong [báo cáo](character_library/CHARACTER_ASSET_REPORT.md). Chưa xác minh rig, lip-sync hoặc chuỗi chuyển động.

### Phê duyệt hình ảnh — 2026-11-05

Owner duyệt 29 ảnh trong hàng đợi In Review dưới dạng sprite tĩnh. Trạng thái hiện tại gồm 29 Approved, 68 Needs Revision và 1 Draft. Phê duyệt hình ảnh không xác nhận rig, lip-sync hoặc hồ sơ quyền.

### Phê duyệt toàn bộ hình ảnh — 2026-11-05

Project Owner duyệt toàn bộ 98 PNG dưới dạng sprite tĩnh, gồm 90 ảnh nguồn và 8 bản Mimi v2. Chỉ mục hiện có 98 Approved. Các phát hiện QA và trạng thái trước duyệt được lưu để tra cứu. Rig, lip-sync và hồ sơ quyền vẫn có cổng riêng.

### Duyệt Bộ diễn xuất 01 — 2026-11-05

Project Owner duyệt 60 PNG của Bộ diễn xuất 01 dưới dạng sprite tĩnh. Chỉ mục hiện có 158 Approved, gồm 50 Tí, 50 Ngang và 58 Mimi.

### Duyệt trang phục và cảnh cặp — 2026-11-06

Project Owner duyệt 20 sprite trang phục Tí và Ngang. Chỉ mục nhân vật có 187 Approved (63 Tí, 63 Ngang, 61 Mimi). Hai PNG cảnh cặp Cổ tích và Dạ hội được lưu riêng trong chỉ mục cảnh của character_library, tra theo scene_id, character_ids hoặc coordination_id. sprite_ids liên kết đến ảnh riêng trong asset_index.json. Số ảnh cảnh được thống kê riêng. Phạm vi duyệt là hình ảnh tĩnh.

### Duyệt cảnh nhóm — 2026-11-07

Project Owner duyệt bốn cảnh nhóm gồm sofa ở nhà, phố mưa, dạ tiệc và thể thao công viên. Thư viện hiện có 211 sprite Approved và 6 cảnh Approved trong scene_index.json. Cảnh có nền liền ảnh, phạm vi duyệt là hình ảnh tĩnh.

## Couple-engine EP08 — 2026-11-07

Bộ hình visual_rebuild_v01 (15 sprite Codex ImageGen) **Owner duyệt**, đã vào thư viện (asset_index 251 mục). EP08 v2 (31,28 s) thay bản v1. 08/11: Owner báo phụ đề đè nhân vật → đã sửa engine (tự chặn phụ đề đè nhân vật/chạm watermark), Owner duyệt lại video cuối, xuất lại 3 nền tảng có watermark NMT vào `videos-post/ngay-dau-yeu-vs-nam-thu-3/`, chưa đăng. Lần xuất cuối 08/11 12:42 với bố cục mới: nội dung 3/4 trên, phụ đề 1/4 dưới (tối đa 1/3, engine chặn). Quy tắc mới: cải tiến liên tục (`output/_engine/IMPROVEMENT_LOG.md`). Bản v1 sao lưu ở `output/ep08_ngay_dau_vs_nam_ba/_superseded_v1_2d/`. Chi tiết trong `HANDOFF_TO_CHATGPT.md`.

### Hình ảnh mặc định và EP10 — 2026-11-08

Owner chốt comic Nhật theo video Ngày đầu yêu vs năm thứ 3 làm mặc định; Mimi là thú cưng của Ngang. EP10 cập nhật bối cảnh bám lời hát. Bảng font Be Vietnam Pro có ba độ đậm, đã kiểm tra glyph và render, chờ Owner chọn. Kịch bản EP10 đang chờ duyệt, mốc nhạc chưa xác minh.

### EP10 — phạm vi nhạc và hình bản 02, 2026-11-08

Owner chọn Itim cho EP10 và chỉ định đoạn từ phần xin số điện thoại đến hết post-chorus đầu. Độ dài theo bản thu, không áp mốc 25–35 giây cũ. Kịch bản mới gồm 13 nhịp, 12 khung, trang phục xanh phấn/vàng bơ và cú lật tuyển người chăm Mimi. Bộ mới ở output/ep10_vi_anh_qua_dep_trai/visual_rebuild_v02/. Chờ duyệt kịch bản/hình bản mới. Mốc cắt âm thanh vẫn chưa xác minh.


### EP10 — Bản video xem trước và Whisper local, 2026-11-08

Thay thế trạng thái chờ duyệt kịch bản/hình v02 ở ghi chú trước: Owner đã duyệt v02 và cho phép tải Whisper Small. Đã chạy faster-whisper Small MIT tại máy (CPU int8; 23,776 s), xử lý lỗi PyAV bằng FFmpeg ndarray. Mốc cắt ASR 31,10–86,35 s. Đã dựng `output/ep10_vi_anh_qua_dep_trai/final_video.mp4`: 55,25 s, 1080×1920/60 fps, 13 cảnh, Itim, twist Con sen mới. Full decode PASS; 514 mẫu phụ đề không đè nhân vật. Lưới trích MP4 `render/video_contact_sheet.jpg`; báo cáo `PRODUCTION_REPORT.md`, `render/video_qa.json`. Animation sprite, chưa rig/lip-sync. Cutout mới vẫn In Review. Âm thanh preview cuối −14,33 LUFS/−3,12 dBTP sau bổ sung headroom AAC; đạt giới hạn đỉnh. **Chờ Owner nghe/xem duyệt video cuối**, chưa xuất videos-post và chưa đăng.


### EP10 v03 — sửa phản hồi chuyển động/nhạc, 2026-11-08

Bản mới để duyệt: `output/ep10_vi_anh_qua_dep_trai/revisions/v03/final_video.mp4` (60,25 s, 1080×1920/60 fps); xem `CURRENT_PREVIEW.json` trong tập, không xuất nhầm MP4 55,25 s cũ. Tăng diễn xuất bằng 19 key pose mới (18 dùng trong video), Mimi 8 dáng, cảnh hôn dùng hình cặp đôi khớp môi, bỏ tim ở vùng mặt và bỏ dissolve gây ghost. Căn lại đúng văn bản theo từng từ, chỉ hiện từ tới mốc, highlight/icon. Twist chờ lần hát cuối và chữ đời kết thúc; thêm 1,8 s phản ứng và 3,2 s outro hồng/ba nhân vật/CTA/logo NMT. 7 test đạt; 464 mẫu phụ đề không đè; 40 mẫu MP4 trước/sau 20 mốc câu đạt theo alignment; full decode đạt; outro không chồng chữ/nhân vật. Nhạc xử lý local; key pose do built-in ImageGen, không phải SDXL. Chưa rig/lip-sync. **In Review**, cần Owner nghe/xem lại; chưa Approved, chưa xuất videos-post/chưa đăng. Bản cũ giữ nguyên và đánh dấu Needs Revision; mọi cutout mới giữ In Review. Chi tiết `revisions/v03/REVISION_NOTES.md`, `render/video_qa.json`, `assets/manifest.json`.


### EP10 v04 — Owner yêu cầu sửa continuity và xuất cuối, 2026-11-08

Đã bỏ hình Mimi trong lồng ở S03 (khoảng giây 08) và S10 hồ bơi, thay hình Ngang không mang lồng, Mimi ở ngoài. Lồng rỗng ở cú twist giữ nguyên. Owner nói “Và xuất video cuối cùng”, đã ghi approval theo phạm vi sửa cụ thể và xuất. Bản cuối v04 dài 60,25 s, 1080×1920/60fps. Đã xuất TikTok, YouTube Shorts, Facebook Reels có NMT vào `videos-post/vi-anh-qua-dep-trai/`; ba bản đã decode, kiểm watermark, phụ đề và mức âm thực. Có cover/caption/manifest. Không đăng. Bản sạch ở `output/ep10_vi_anh_qua_dep_trai/revisions/v04/`; báo cáo `EXPORT_REPORT.md` và `videos-post/vi-anh-qua-dep-trai/export_report.json`. Các phiên bản cũ giữ nguyên; `CURRENT_PREVIEW.json` trỏ v04 đã duyệt theo yêu cầu xuất, không dùng nhầm v03. Không tự thay approval thư viện PNG.


### Khung an toàn 9:16 (NMT-SAFE-916 v1) + EP10 v05, 2026-11-08

Owner báo TikTok/YouTube Shorts phóng to và mất 4 góc, phần trên tràn lên tab. File không lỗi (1080×1920, SAR 1:1); nguyên nhân là bố cục đặt sát mép, trong khi app lấp đầy màn dài hơn 9:16 nên cắt ~108 px mỗi bên và đè đỉnh/đáy. Đã thêm `output/_engine/safe_frame.py`, mục 3.2 `NMT_ENGINE.md`, `cute_engine.SAFE916` + `safe_post()`, chặn trong `check_subs`, watermark `margin_x ≥ 120`. Test `tests/unit/test_subtitle_layout.py` 15/15 OK. EP10 v05 (`output/ep10_vi_anh_qua_dep_trai/revisions/v05/`) đã render, decode, kiểm khung an toàn đạt; **In Review**, chưa xuất videos-post (bản v04 vẫn ở đó), chưa đăng, chưa thử trên điện thoại. Còn mở: mặc định watermark trong `src/` (cần Scope Grant), EP08 chưa dựng lại.


### EP10 v06 (sửa theo góp ý v05), 2026-11-08

Owner chê v05: nền mờ, Mimi nhảy rời rạc, chữ "Bình Quới", vị trí icon, Tí ngồi cao hơn Ngang. Đã sửa ở v06:
- tranh là khung bo góc gọn trong vùng an toàn, nền trơn (engine cũng đã bỏ nền mờ);
- Mimi nằm lim dim dưới chân Ngang ở S01–S10, dùng hình thư viện MIMI_ACTING_008;
- icon nằm trong viên phụ đề, sóng nhạc đặt trên tranh;
- ở ghế, hai người cùng mặt ghế và Ngang ôm Mimi.

Video đã render, giải mã toàn bộ, kiểm tra khung an toàn đều đạt. Trạng thái **In Review**: chưa xuất videos-post (vẫn là v04), chưa đăng, chưa xem trên điện thoại. v05 chuyển sang Needs Revision.


### EP10 v06 — Owner duyệt, đã xuất cuối, 2026-11-08

Owner duyệt bằng câu "Duyệt, xuất v06". Đã xuất 3 bản TikTok, YouTube Shorts và Facebook Reels vào `videos-post/vi-anh-qua-dep-trai/`. Thông số: 1080×1920, 60 fps, 60,25 s, theo khung an toàn NMT-SAFE-916 v1, watermark NMT `margin_x` 120.

Kiểm tra từng bản:
- watermark PASS;
- giải mã toàn bộ đạt;
- âm lượng -14,08 LUFS, đỉnh -2,74 dBTP.

Bản v04 được dời sang `_superseded_v04/`, không xoá. `CURRENT_PREVIEW.json` đã trỏ sang v06. Chưa đăng, chưa xem trên điện thoại. Báo cáo: `output/ep10_vi_anh_qua_dep_trai/revisions/v06/EXPORT_REPORT.md`.

Còn mở:
- mặc định watermark trong `src/` (cần Scope Grant);
- EP08 chưa dựng lại theo khung an toàn.


### Quy tắc mới: viền phụ đề luôn canh giữa màn hình, 2026-11-08

Owner phát hiện viền phụ đề EP10 v06 lệch tâm (x=510). Đã đổi `safe_frame.SUB_X_CENTER` thành 540, thêm kiểm tra tự chặn khi lệch quá 2 px, và engine không còn dời phụ đề sang ngang để né watermark. Test 17/17 đạt. Theo yêu cầu Owner, video đã xuất không làm lại; quy tắc áp dụng từ các video tiếp theo.
