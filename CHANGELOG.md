# CHANGELOG

## nmt-engine v1.0.0 — 12/11/2026

Owner yêu cầu đóng gói nmt-engine (Ngang Một Tí) thành bản phát hành v1.0.0 và commit vào nhánh chính.

- **Có trong bản này:** `output/_engine/` (renderer `cute_engine`, CLI `nmt_engine.py`, cổng duyệt `gates`, khung an toàn `safe_frame`, xuất đa nền tảng `platform_export`, âm thanh `audio_engine`, thư viện `library_sync`, font Be Vietnam Pro (OFL), `NMT_ENGINE.md`, `IMPROVEMENT_LOG.md`, `VERSION`); lệnh `/nmt-engine` và alias `/couple-engine` trong `.claude/commands/`; phụ thuộc watermark `src/ai_video_factory/core/{branding,config}.py` và logo `output/branding/ngang-mot-ti/`.
- **Quy trình:** kịch bản → giọng/hình mẫu → video → xuất TikTok/YouTube Shorts/Facebook Reels, mỗi bước dừng chờ Owner duyệt; không tự đăng.
- **Mới trong đợt EP17–EP19:** tranh cảnh full-bleed 9:16 tạo bằng ChatGPT image_gen, kiểm vùng an toàn bằng lưới; nhạc CC0 Freesound khoá SHA; quy tắc "mọi video cuối thêm hình vào thư viện" — `--export-finish` tự gọi `library_sync.sync` gồm `sync_scene_art` (tranh cảnh `episode_scene_art`, `LIBRARY_ART`, contact sheet).
- **Đã kiểm thử:** EP17, EP18, EP19 dựng và xuất thật bằng engine này (EP19: 63,5 s, −14,8 LUFS, watermark, kiểm phụ đề 3 nền tảng đạt); `--library-sync` chạy lại cho kết quả `same` (không trùng mục).
- **Không có trong repo (cục bộ):** `character_library/` (ảnh nhân vật, 319 MB), các tập `output/epNN_*`, `videos-post/`, model VieNeu và venv (`workspace/`). Engine cần các thư mục này khi chạy.
- **Đã biết:** `tts_vieneu.py` chung còn trỏ đường dẫn máy ảo cũ; các tập dùng `render/tts_local.py`. Độ lệch thoại 0,35 s đầu cảnh vẫn là mặc định engine (EP19 tự đặt `FIRST_LEAD`).

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


Ghi lại thay đổi đáng chú ý theo từng phase. Định dạng dựa trên Keep a Changelog.

## [Unreleased]

### Couple-engine EP08 v2, phụ đề và cải tiến liên tục (2026-11-08)

- EP08 dựng lại bằng 15 sprite Codex ImageGen (Owner duyệt hình và video cuối); bản v1 lưu ở `output/ep08_ngay_dau_vs_nam_ba/_superseded_v1_2d/`.
- `cute_engine.py`: kiểm tra tự động phụ đề đè nhân vật và chạm watermark NMT (`--check-subs`), chặn ở `--mux` và `--export-finish`; dải phụ đề cho cảnh toàn khung; khung chia đôi tự thu theo vùng an toàn nền tảng.
- Quy tắc Owner: cải tiến liên tục mỗi ngày, sổ `output/_engine/IMPROVEMENT_LOG.md`.
- Bố cục khung couple-engine: nội dung 3/4 trên, phụ đề 1/4 dưới (tối đa 1/3, engine chặn); phụ đề tự né watermark NMT.

### Thư viện nhân vật Style C (2026-11-05)

- Audit ảnh trên hai nền, lưu bằng chứng theo ID, thêm 8 bản Mimi v2 và cập nhật hàng đợi duyệt trực quan.

- Khôi phục Python riêng của ComfyUI và xác minh phép thử PyTorch MPS.
- Lập chỉ mục 90 PNG gồm 66 ảnh thử local. Cổng chất lượng hình ảnh còn mở cho các tài sản cần sửa.

### Phase 1 – Bắt đầu bước 1.0 (2026-10-31)

#### Added

- `docs/operations/phase-reports/PHASE-01-PLAN.md`: kế hoạch Phase 1, Project Owner xác nhận 2026-10-31.
- `docs/testing/phase1-candidates.md`: dự thảo danh sách ứng viên và license, chờ Owner duyệt.

#### Changed (bản sửa sau Codex pre-approval review)

- `docs/testing/phase1-candidates.md` viết lại: phân loại A, B, C; hồ sơ từng ứng viên (nguồn, revision, quantization, voice ID, license, chuỗi quyền, tài nguyên, điểm chưa xác minh); tách bốn trạng thái phương pháp, kế hoạch, danh sách, quyền tải.
- Loại Piper `vais1000` (chuỗi quyền qua lessac/Blizzard 2013 chỉ cho nghiên cứu) và VieNeu-TTS 0.3B, 0.5B (dữ liệu CC BY-NC). Không còn TTS tiếng Việt nào đủ điều kiện nhóm B.
- `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`: đồng bộ; Codex re-review BLOCKED vì chưa có Scope Grant.

#### Changed

- D-013, D-017 `Approved`; Q-03 (có kiếm tiền), Q-06 (4 giờ) đã trả lời. Cập nhật `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`, `CURRENT_STATUS.md`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`.

#### Không có

- Cài đặt, tải model, code ứng dụng, commit, push. Bước 1.0 chỉ đọc tài liệu.

### Workflow mức B được nghiệm thu (2026-10-30)

Project Owner nghiệm thu tài liệu workflow mức B và đóng SG-001 sau khi Codex kết luận `APPROVED` tại RR-002. Đã dùng 1/3 vòng. Chỉ cập nhật dòng trạng thái trong workflow, không đổi quy tắc. Mức C chưa đạt. Không thay đổi phase.

Sau đó, theo cho phép của Project Owner: dọn trạng thái cũ trong `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`, và tạo một commit cục bộ trên `main`. Commit này chưa push.

### RR-002 vòng 1/3 (2026-10-30)

Codex kết luận `APPROVED`, đóng F-001 và F-002, không có finding mới. RR-002 chuyển `ANSWERED`. Workflow chưa được Project Owner nghiệm thu; SG-001 vẫn `ACTIVE`.

### SG-001 Amendment A01 (2026-10-30, chờ Codex vòng 1/3)

#### Changed

- `TASKS.md`: ghi Amendment A01 do Project Owner phê duyệt; RR-001 chuyển `ANSWERED`; đăng RR-002 tiếp nối, vòng 1/3, không đặt lại bộ đếm.
- `docs/operations/AI_REVIEW_WORKFLOW.md`: F-001, chia file thành nhóm A, B, C, thêm kiểm tra reviewer artifact theo số byte và SHA-256; F-002, quy định phản hồi finding, trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` và đường sau PASS.
- `AGENTS.md`, `CLAUDE.md`: làm rõ reviewer artifact, giới hạn của SHA-256 và điều kiện dừng.
- `REVIEW_RESPONSE.md`: phản hồi F-001, F-002.

#### Không có

- Code, script điều phối, cài đặt, commit, push, tạo nhánh, sửa báo cáo Codex, đóng finding, nghiệm thu workflow.

### Workflow Claude–Codex mức B (2026-10-30, chờ Codex review)

#### Added

- `docs/operations/AI_REVIEW_WORKFLOW.md`: Scope Grant, Review Request, kiểm tra đầu vào, quyền ghi, giới hạn 3 vòng, điều kiện dừng, mức A, B, C.
- `TASKS.md`: mục Scope Grants, Review Requests, SG-001, RR-001.

#### Changed

- `AGENTS.md`: lượt có thể đến từ Review Request hợp lệ trong Scope Grant; thêm kết luận `BLOCKED`; trỏ tới workflow.
- `CLAUDE.md`: nhánh phase chỉ dùng khi Chủ dự án cho phép; trỏ tới workflow.
- `docs/workflows/README.md`: thay mục quy trình lặp lại bằng liên kết; giữ quy tắc nhánh.
- `docs/operations/README.md`: thêm chỉ mục.

#### Không có

- Code ứng dụng, script điều phối, cài đặt, commit, push, tạo nhánh, thay đổi quyết định. Workflow chưa được kiểm chứng bằng một vòng thực tế.

### Phase 0 – Nghiệm thu

`2026-10-30 — Phase 0 accepted by Project Owner following Codex Final F-01 PASS.`

Nghiệm thu chỉ ở mức documentation/design. Không xác nhận application code đã triển khai, không xác nhận runtime test đã pass và không cho phép bắt đầu Phase 1.

Commit đầu tiên được tạo cục bộ trên `main` theo cho phép của Project Owner. Chưa push.

### Phase 0 – Sửa F-01 (2026-10-30)

#### Changed

- `PROJECT_MASTER.md`, `TECH_STACK.md`, `docs/requirements/README.md`: đồng bộ ba dòng hiện hành với D-023 `Approved — Option C` và Q-13 `Answered — Option C`. TikTok Direct Post vẫn `POLICY BLOCKED`; mục tiêu giữ trong roadmap.
- `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`: ghi R4-01 `CLOSED` theo Codex và F-01 chờ xác minh.

#### Không có

- Code, cài đặt, commit, push, thay đổi D-009 đến D-022, nghiệm thu Phase 0, bắt đầu Phase 1.

### Phase 0 – Ghi nhận D-023/Q-13 và khắc phục R4-01 (2026-10-30, chờ Codex kiểm tra lại)

#### Changed

- `DECISIONS.md`: D-023 chuyển sang `Approved` theo quyết định của Project Owner, phương án C. Bản ghi được chuyển sang mục "Đã duyệt", không tạo bản trùng. Tách Decision status và Direct Post integration status.
- `docs/deployment/platform-verification.md` mục 3: định nghĩa `POLICY BLOCKED` và năm điều kiện mở cổng G1–G5.
- `IMPLEMENTATION_PLAN.md`, `docs/architecture/publishing-reliability.md`: bỏ cách viết khiến quyết định D-023 có thể bị hiểu là điều kiện đủ để viết adapter.
- `CURRENT_STATUS.md`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`, báo cáo Phase 0: đồng bộ. Sửa dòng Git: đã có remote `origin`.

#### Không có

- Code ứng dụng, adapter TikTok, OAuth, gọi API, credentials, cài đặt, commit, push, thay đổi D-009 đến D-022, nghiệm thu Phase 0.

### Phase 0 – Bản sửa 3 theo Codex review vòng 3 (2026-10-30, chờ Chủ dự án quyết định)

#### Added

- `platform-verification.md` mục 3: xung đột TikTok Direct Post với mục đích dùng cá nhân, ba lựa chọn.
- D-023 ở trạng thái `Proposed`, Q-13, rủi ro R13.
- `queue-safety.md`: T11a–c, AC-Q18, AC-Q19, FI-44 đến FI-51.

#### Changed

- `queue-safety.md`: `pending_outcome` có hai loại `success`, `failure` với yêu cầu riêng; phát hiện đồng hồ lùi và dịch lịch khi Worker đang sống, kèm bước kẹp độc lập; FI-32 cấm khởi động lại.
- TikTok được đánh dấu bị chặn ở `publishing-reliability.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `docs/requirements`. Mục tiêu sản phẩm giữ nguyên chờ Chủ dự án quyết định.

#### Không có

- Code ứng dụng, phần mềm cài đặt, phê duyệt thay Chủ dự án, thay đổi mục tiêu sản phẩm.

### Phase 0 – Bản sửa 2 theo Codex review vòng 2 (2026-10-30, chờ Chủ dự án quyết định nghiệm thu)

#### Fixed

- `.gitignore`: bỏ `!tests/fixtures/**`, vốn làm secret, token, DB, model và media trong `tests/fixtures` không còn bị chặn. Thay bằng chặn mặc định, cho phép 7 định dạng văn bản, khối secret đặt cuối. Thêm `*.env`, `*.p8`, `*.jks`. Đã xác minh.
- `security-and-rights.md`: bỏ yêu cầu "cổng cố định" cho callback, không đúng với mọi nhà cung cấp.

#### Added

- `queue-safety.md`: `SQLITE_BUSY`, tiến trình mồ côi, `heavy.lock`, FI-22 đến FI-43, AC-Q10 đến AC-Q17, oracle OR1–OR6.
- `publishing-reliability.md`: ranh giới adapter, yêu cầu TikTok, YouTube, Facebook, AC-P12 đến AC-P17, PF-14 đến PF-22.
- `security-and-rights.md`: xác minh scope, `client_secret` desktop, token không tới dashboard, năm điều kiện tạo `queued`, `PublishGrant`, AC-S7 đến AC-S9, AC-R4 đến AC-R8.
- Ghi nhận chính sách ngày 2026-10-30 có nguồn.

#### Changed

- Thu hồi job chỉ xảy ra lúc Worker khởi động; `lease_expires_at` dùng để hiển thị `stalled`.
- Lược đồ khái niệm: thêm `packages`, `rights_reviews`, `publish_intents`; `approvals` gắn `package_sha256`.
- Phase 2, 3, 13, 15, 16: cập nhật tiêu chí nghiệm thu.
- D-018, D-019, D-021, D-022: mở rộng phạm vi, trạng thái vẫn `Proposed`.

#### Không có

- Code ứng dụng, phần mềm cài đặt, thay đổi bộ công nghệ, Agent mới, phê duyệt thay Chủ dự án, tuyên bố tuân thủ nền tảng.

### Phase 0 – Bản sửa 1 theo Codex review (2026-10-30, chờ review lần 2)

#### Added

- `REVIEW_RESPONSE.md`: phản hồi từng BLOCKER, WARNING, RECOMMENDATION.
- `HANDOFF_TO_CHATGPT.md`.
- `docs/architecture/queue-safety.md`: fencing, staging, phục hồi, tiêu chí nghiệm thu, fault injection.
- `docs/architecture/publishing-reliability.md`: máy trạng thái upload, đối soát, chống đăng trùng.
- `docs/architecture/security-and-rights.md`: mô hình đe dọa, OAuth, token, log, quyền nội dung, Rights Gate.
- `docs/deployment/platform-verification.md`: quy trình và ảnh chụp chính sách có nguồn.
- D-018 đến D-022, ở trạng thái `Proposed`.
- Spike TTS Việt–Anh trong Phase 1.
- `IMPLEMENTATION_PLAN.md` mục 6: cổng quyết định theo phase.

#### Changed

- `DECISIONS.md`: thêm rà soát D-009 đến D-017. Trạng thái giữ nguyên `Proposed`.
- `ARCHITECTURE.md`: gắn nhãn đề xuất; viết lại mục 5, 10, 11; thêm mục 15. Tập trạng thái job đổi thành `queued`, `running`, `succeeded`, `dead`, `cancelled`.
- `CURRENT_STATUS.md`: bỏ cách gom quyết định vào Q-01; không còn gọi Phase 0 là "triển khai xong".
- `TECH_STACK.md`: sửa ghi chú YouTube đã lỗi thời theo tài liệu chính thức.
- Bổ sung `docs/` về DB, Agent, kiểm thử, yêu cầu.

#### Không có

- Code ứng dụng, phần mềm cài đặt, thay đổi bộ công nghệ, Agent mới, phê duyệt thay Chủ dự án.

### Phase 0 – Hồ sơ dự án (2026-10-30, chờ nghiệm thu)

#### Added

- Tài liệu quản lý: `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`.
- Hướng dẫn AI: `AGENTS.md`, phần hướng dẫn mới trong `CLAUDE.md`.
- Tài liệu chi tiết trong `docs/`, mẫu báo cáo phase, báo cáo Phase 0.
- `.gitignore`.

#### Changed

- `CLAUDE.md`: thêm nội dung phía trên quy tắc bàn giao của Chủ dự án; quy tắc đó giữ nguyên.

#### Không có

- Code ứng dụng, phần mềm cài đặt, model AI, credentials, tích hợp mạng xã hội.

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
