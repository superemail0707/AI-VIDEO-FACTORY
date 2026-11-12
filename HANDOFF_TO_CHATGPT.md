# HANDOFF TO CHATGPT – AI VIDEO FACTORY

## nmt-engine v1.0.0 — 12/11/2026

Owner yêu cầu đóng gói nmt-engine (Ngang Một Tí) thành bản phát hành v1.0.0 và commit vào nhánh chính.

- **Có trong bản này:** `output/_engine/` (renderer `cute_engine`, CLI `nmt_engine.py`, cổng duyệt `gates`, khung an toàn `safe_frame`, xuất đa nền tảng `platform_export`, âm thanh `audio_engine`, thư viện `library_sync`, font Be Vietnam Pro (OFL), `NMT_ENGINE.md`, `IMPROVEMENT_LOG.md`, `VERSION`); lệnh `/nmt-engine` và alias `/couple-engine` trong `.claude/commands/`; phụ thuộc watermark `src/ai_video_factory/core/{branding,config}.py` và logo `output/branding/ngang-mot-ti/`.
- **Quy trình:** kịch bản → giọng/hình mẫu → video → xuất TikTok/YouTube Shorts/Facebook Reels, mỗi bước dừng chờ Owner duyệt; không tự đăng.
- **Mới trong đợt EP17–EP19:** tranh cảnh full-bleed 9:16 tạo bằng ChatGPT image_gen, kiểm vùng an toàn bằng lưới; nhạc CC0 Freesound khoá SHA; quy tắc "mọi video cuối thêm hình vào thư viện" — `--export-finish` tự gọi `library_sync.sync` gồm `sync_scene_art` (tranh cảnh `episode_scene_art`, `LIBRARY_ART`, contact sheet).
- **Đã kiểm thử:** EP17, EP18, EP19 dựng và xuất thật bằng engine này (EP19: 63,5 s, −14,8 LUFS, watermark, kiểm phụ đề 3 nền tảng đạt); `--library-sync` chạy lại cho kết quả `same` (không trùng mục).
- **Không có trong repo (cục bộ):** `character_library/` (ảnh nhân vật, 319 MB), các tập `output/epNN_*`, `videos-post/`, model VieNeu và venv (`workspace/`). Engine cần các thư mục này khi chạy.
- **Đã biết:** `tts_vieneu.py` chung còn trỏ đường dẫn máy ảo cũ; các tập dùng `render/tts_local.py`. Độ lệch thoại 0,35 s đầu cảnh vẫn là mặc định engine (EP19 tự đặt `FIRST_LEAD`).

## 1001 Ngang — master ImageGen và sửa màu lông Mimi, 12/11/2026

- **Đã làm, đã kiểm:** Owner cho phép Claude điều khiển ChatGPT trong trình duyệt tích hợp. 10 master sheet (S1/S2/S3 × Ngang, Tí, Mimi; Tí S1 có 2 phương án) đã tải nguyên byte về `character_library/inbox/imagegen-downloads/` và import `in_review` (`.superpowers/sdd/EXECUTION_PLAN/import_imagegen_masters.py`). Sao lưu DB trước khi import. Trang duyệt: `docs/1001-ngang/review/MASTERS_REVIEW.html` (cấu hình `ngang-owner-review`, cổng 8765). Toàn bộ unit test: 282 OK.
- **Sửa màu lông Mimi (Owner 12/11):** Mimi là mướp nâu xám như ảnh master gốc, không phải xám xanh. Bible Mimi bản sửa là DB version 2, `in_review`; version 1 đã duyệt vẫn ghi xám xanh. Style profile S2 đã duyệt còn chữ "xám xanh", chưa sửa vì sửa sẽ cần Owner duyệt lại.
- **Owner duyệt master 12/11** ("Duyệt tất cả, Tí S1 chọn A"): 9 ảnh `approved` và gán master (`approve_imagegen_masters.py`); `approved_context` sẵn sàng cho S1/S2/S3 × Ngang, Tí, Mimi. Tí S1 B vẫn `in_review`. Unit 282 OK.
- **Bible Mimi version 2 đã duyệt 12/11** ("Duyệt Bible Mimi v2"), khớp master Mimi.
- **Còn chờ Owner:** có sửa chữ "xám xanh" trong style profile S2 hay không; license VieNeu; duyệt nội dung 5 pilot; lệnh "Làm Task 7".
- **Ghi chú:** `character_library/asset_index.json` bị đổi lúc 10:23 ngày 12/11, ngoài phạm vi engine. `imagegen-bridge` (script `.superpowers/sdd/EXECUTION_PLAN/imagegen_bridge.py`, cấu hình trong `.claude/launch.json`) chỉ là công cụ tạm, chỉ bind 127.0.0.1. Chưa commit.

## 1001 Ngang Engine — thư viện ảnh, reference, nhân vật/style, series/script/storyboard (Task 1–6), 11/11/2026

- Nhánh `review/phase-02-1001-ngang-engine`; chưa commit. Thiết kế `docs/1001-ngang/CURRENT_ARCHITECTURE.md`, kế hoạch 11 task `docs/1001-ngang/EXECUTION_PLAN.md` (Owner duyệt 10/11). Tiến độ/báo cáo/review từng task: `.superpowers/sdd/EXECUTION_PLAN/`.
- **Đã triển khai và có test:** `src/ai_video_factory/shared/` — Task 1 `store.py`/`migrations.py` (SQLite schema v1, transaction, backup/restore); Task 2 `legacy.py`/`library.py` (đọc hợp nhất 3 index cũ, search/pin/resolve theo SHA-256, không ghi index); Task 3 `import_image`/`reconcile` (byte gốc giữ nguyên, địa chỉ nội dung trong `character_library/inbox/generated-images/`, thumbnail, chống trùng, mặc định `in_review`); Task 4 `approvals.py`, `collections.py`, `new_version` (chỉ Owner duyệt, cần evidence + checksum, lịch sử chỉ thêm, override legacy chỉ trong SQLite, version bất biến, master/rollback bằng event).
- **Test:** `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_shared_*.py'` → 27 OK; `-p 'test_ngang_*.py'` → 11 OK; toàn bộ `tests/unit` → 280 OK (trước Task 1: 241).
- **Database migration:** chỉ schema v1 trong code; **chưa tạo DB thật** (`workspace/shared_library/library.sqlite3` chưa có). Chưa ghi gì vào `character_library/` thật.
- **Reference library:** đọc thật ngày 10/11: 299 ảnh (270 approved, 23 in_review, 6 archived). `generated_references/index.json` đổi lúc 11/11 07:18 (42 → 52 bản ghi, không do engine) nên số liệu này đã cũ. 0 ảnh approved trong store mới; 0 collection; chưa có master đa style.
- **Task 5:** `src/ai_video_factory/ngang/profiles.py` — identity/Bible/style tách lớp; seed 3 nhân vật (không bịa ngoại hình, Mimi là mèo rig feline, pet_of ngang) và 6 style §7 (chỉ tên, chưa duyệt); master theo style do Owner chọn qua collection; ảnh nhiều nhân vật cần `character_mapping`; `approved_context`/`require_context` trả `DEPENDENCY_REQUIRED`. Docs `CHARACTER_LIBRARY.md`, `VISUAL_STYLE_SYSTEM.md`.
- **Task 6:** `ngang/catalog.py` (literal Owner, test so với OWNER_REQUIREMENTS.md), `series.py` (series/30 topic, tập đánh số an toàn đa tiến trình, script/storyboard version + Owner review, storyboard `stale` khi script đổi, `production_readiness`), `storyboard.py` (đủ 24 trường §12, camera grammar, 8–20 s, NaN/∞ bị chặn, mixed style cần cờ), `pilots.py` + `docs/1001-ngang/PILOT_DRAFTS.md` (5 pilot nháp, style đề xuất anime-slice-of-life, chưa duyệt, mỗi pilot liệt kê dependency). Doc `1001_NGANG_ENGINE.md`.
- **Chưa làm:** Task 7 (ImageGen thủ công), 8 (NMT adapter/render/QC), 9 (CLI + dashboard), 10 (analytics), 11 (pilot, docs, regression).
- **Vấn đề đã biết:** một bản ghi index cũ hỏng làm cả thư viện báo lỗi (fail-closed); chưa test import/review đồng thời nhiều tiến trình; duyệt ảnh tĩnh ≠ quyền sử dụng/rig/video, chưa có cơ chế bắt buộc. `tests/unit/test_automation.py` bị sửa 11/11 10:52 ngoài phạm vi engine.
- **Gói duyệt Owner (11/11):** `docs/1001-ngang/review/OWNER_REVIEW.html`, một trang local tự chứa với ảnh thật. Nội dung: 3 hướng style có ảnh (S1 comic Nhật pastel là khuyến nghị, S2 Style C, S3 chibi; 4 style §7 còn lại chưa có ảnh); ứng viên master (Style C đủ 3 ảnh approved; pastel thiếu ảnh đứng một mình); Character Bible nháp ×3 (`review/bible_drafts/*.json`, mỗi chi tiết có nguồn, đúng schema, chưa duyệt); giọng Trúc Ly/Hải Đăng với mẫu EP03 (VieNeu chưa có license thương mại); bảng 30 topic đã phân loại vào 10 nhóm (`catalog.TOPIC_CATEGORIES`, Claude phân loại theo yêu cầu Owner, `initialize` chỉ điền chỗ còn trống). Toàn bộ unit 281 OK.
- **Quyết định Owner 11/11 đã áp dụng** (`docs/1001-ngang/OWNER_DECISIONS.md`):
  - Duyệt S1 `anime-slice-of-life`, S2 `style-c`, S3 `chibi`. Mỗi tập chọn style theo topic; scene được đổi style vì biểu cảm, kèm lý do.
  - Giọng Trúc Ly/Hải Đăng và nhóm topic đã duyệt.
  - Bible v2 đã sửa theo góp ý: trang phục đa dạng, góc máy phim, tỷ lệ 7–7,5 đầu với khung toàn thân/2/3/1/2, Mimi mướp xám xanh. Owner duyệt ngày 12/11 ("Duyệt Bible v2"); trong DB là version 1, approved, có backup.
  - 9 gói prompt ImageGen tạo master ở `docs/1001-ngang/imagegen/MASTER_PROMPTS.md`.
  - **DB thật đã tạo:** `workspace/shared_library/library.sqlite3` (gitignored, có backup) qua `ngang/bootstrap.py`. Trong DB: 3 style approved, 3 Bible (nội dung v2) đã approved ngày 12/11, 5 pilot nháp, 2 ảnh chibi ImageGen của Owner trong inbox (`in_review`).
  - Toàn bộ unit 282 OK.
- **Owner cần quyết (dependency):** nội dung Character Bible cho Ngang/Tí/Mimi; style nào dùng cho pilot; có tạo profile riêng cho Style C hay không; style cho 5 pilot; xác nhận hoặc sửa nhóm nội dung đã phân loại; duyệt nội dung 5 pilot nháp; tỷ lệ cơ thể chuẩn; nguồn của 2 ảnh chibi chưa index (18:14 ngày 11/11). Chưa có gì được duyệt nên mọi context sản xuất đang báo dependency.
- **Bước tiếp theo:** Owner tạo master bằng ImageGen theo MASTER_PROMPTS.md rồi đưa thư mục ảnh để import và duyệt. Task 7 (tự động hóa gói prompt và import) chờ Owner cho phép. Không tự tạo master, không tự duyệt Character Bible.

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


Cập nhật lần cuối: 2026-10-31, sau khi Owner trả lời "1B, 2A, 4a, 4b" (Amendment A02 của SG-002). Tệp này được duy trì sau mọi phase và giữ lại lịch sử còn liên quan.

## 1. Trạng thái hiện tại

| Mục | Giá trị |
|---|---|
| Phase hiện tại | **Phase 1 – Môi trường & đo đạc nền, bước 1.0.** Phase 0 đã nghiệm thu |
| Tình trạng | **Phase 0: ACCEPTED** (Project Owner, 2026-10-30), mức tài liệu và thiết kế. **Phase 1: PLAN CONFIRMED — step 1.0 only** (Owner xác nhận kế hoạch 2026-10-31; `docs/operations/phase-reports/PHASE-01-PLAN.md`). Chưa được phép cài đặt hay tải model; mỗi lệnh cần xác nhận riêng |
| Cổng đầu vào Phase 1 | Q-03 (video **có** kiếm tiền, license phải cho phép thương mại) và Q-06 (chạy qua đêm, tối đa **4 giờ** cho một video, Owner đã xác nhận) đã trả lời 2026-10-31. D-013 và D-017 đã duyệt 2026-10-31. **Kế hoạch chi tiết Phase 1 đã được Owner xác nhận** (2026-10-31). Không còn cổng đầu vào Phase 1 nào chờ; Owner đã chọn tiêu chuẩn nhóm B là S2 (2026-10-31, nguyên văn "Chọn S2"); Codex đã APPROVED phân loại theo S2 tại RR-005; việc đang chờ là: Owner chọn hướng TTS tiếng Việt, Owner duyệt danh sách model, và quyền tải, cài, chạy từng bước |
| D-023 | **APPROVED — OPTION C** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Git checkpoint | Commit `def8fdf`, `fb3a19f`, `e83ecec` đã có trên `origin/main` (Project Owner cho phép; Claude xác minh hash khớp). Mỗi lần commit hay push tiếp theo cần cho phép riêng |
| Kết luận Codex mới nhất | **Phase 1.0 hồ sơ nghiên cứu: APPROVED tại RR-004** (vòng 1/3) **và phân loại theo S2 APPROVED tại RR-005** (vòng 2/3). Không phải PASS về license thương mại cuối cùng, danh sách benchmark hay quyền thực thi. **Chọn tiêu chuẩn S2 không thay việc Owner duyệt từng ứng viên và rủi ro dư kèm theo.** (Phase 0: PASS — READY FOR OWNER ACCEPTANCE tại Final F-01 Verification, đã nghiệm thu.) |
| Kết luận Codex vòng 4 | **APPROVED WITH CHANGES**, chỉ cho hồ sơ Phase 0 (`docs/operations/reviews/PHASE-00-REVIEW.md`) |
| Kết luận Codex vòng 3 | CHANGES REQUESTED |
| Kết luận Codex vòng 1 | NEEDS REVISION |
| Vòng 2 | Phát hiện do Chủ dự án chuyển; repo không có tệp báo cáo gốc |
| Quy tắc D-023 | Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. Mở cổng cần G1–G5 (`docs/deployment/platform-verification.md` mục 3) |
| Workflow Claude–Codex | Mức B theo phê duyệt có điều kiện; tài liệu ở `docs/operations/AI_REVIEW_WORKFLOW.md`; Codex **APPROVED** tại RR-002; **Project Owner nghiệm thu** ngày 2026-10-30; mức C chưa đạt |
| SG-001 | **DONE** (Project Owner đóng, 2026-10-30); Amendment A01 đã áp dụng; đã dùng 1/3 vòng |
| RR-001 | Vòng 0/3: CHANGES REQUESTED, finding F-001, F-002 |
| RR-002 | Vòng 1/3: **APPROVED**, trạng thái `ANSWERED` |
| F-001, F-002 | **CLOSED** (Codex, RR-002) |
| SG-002 | **DONE** (Project Owner đóng 2026-10-31, lời "đóng"). Đã dùng đủ 4 lần review (vòng 0–3). RR-006 CHANGES REQUESTED: P1-003, P1-004 đã sửa nhưng **chưa CLOSED**, chưa review lại (Owner chấp nhận). Đóng SG không hợp thức hóa cài đặt, tải, đo, commit/push, nhãn A02–A07 và không cấp quyền mới |
| SG-002 Amendment A01 | **APPROVED** (Owner, 2026-10-31): bốn file (`CHANGELOG.md`, `CURRENT_STATUS.md`, `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`) là nhóm A **chỉ đọc**; không đặt lại bộ đếm |
| SG-002 Amendment A02 | **APPROVED** (Owner, 2026-10-31, lời "1B, 2A, 4a, 4b"): Claude được ghi D-024 (tiêu chuẩn S2) vào `DECISIONS.md` và đồng bộ `CURRENT_STATUS.md`; `CHANGELOG.md` vẫn chỉ đọc; không đặt lại bộ đếm. Hai file đó đổi hash so với ảnh chụp RR-005 (thay đổi hợp lệ theo A02) |
| Mã 1B | Danh sách model: **chỉ Qwen3 4B `q4_K_M`**, kèm rủi ro dư; 8B chưa duyệt. Không phải quyền tải, cài, chạy |
| Mã 2A | Nghiên cứu TTS bằng tài liệu: VieNeu v3 Turbo **không có tệp LICENSE trong kho Hugging Face** (chỉ metadata và README), giữ nhóm A; ViZipVoice nhóm A; VietTTS, viXTTS nhóm C. **Vẫn không có TTS tiếng Việt nhóm B (R1)**. Các thay đổi này chưa được Codex review |
| D-024 | **APPROVED** (Owner, S2). **Mã 2G và 4c (Owner, 2026-10-31, nguyên văn "2G, 4C- xác nhận 1-8"):** điều 9 của PHASE-01-PLAN.md **bị bác**; điều 1–8 **được xác nhận**. R1 vẫn mở (báo Owner trước Phase 4 và 5). Mã 3a–3g, 4d, 4e, 4f **chưa trả lời**; chưa có quyền tải, cài, chạy. `CURRENT_STATUS.md` chưa phản ánh 2G/4c (ngoài phạm vi A02) |
| RR-003 | Vòng 0/3: **CHANGES REQUESTED** (Codex), `ANSWERED` |
| RR-004 | Vòng 1/3: **APPROVED** (Codex), `ANSWERED`. Reviewer artifact `docs/operations/reviews/PHASE-01-REVIEW.md` |
| P1-001, P1-002 | **CLOSED** (Codex, RR-004) |
| Quyết định S2 | **Owner chọn S2 ngày 2026-10-31** (nguyên văn "Chọn S2"). Dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận, chỉ cho ứng viên thỏa ba điều kiện, chỉ cho phân loại. Không phải kết luận pháp lý, duyệt danh sách hay quyền tải, cài, chạy. Đã ghi thành D-024 trong `DECISIONS.md` (Amendment A02) |
| RR-005 | Vòng 2/3: **APPROVED** (Codex), `ANSWERED`. Phân loại Qwen3 4B, 8B lên nhóm B theo S2 được chấp nhận để **trình Owner**, không phải "đã duyệt" hay "sẵn sàng chạy" |
| RR-006 | Vòng 3/3 (cuối): **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-003 (MEDIUM, trạng thái hiện hành chưa đồng bộ với 1B, 2A, D-024) và P1-004 (LOW, lập luận thiếu LICENSE riêng của VieNeu mạnh hơn bằng chứng): Claude xác minh **đúng cả hai**, `FIX NOT IMPLEMENTED — AWAITING OWNER`; chưa CLOSED. Owner chỉ đạo "Cho sửa, không review": Claude đã sửa cả hai, trạng thái `FIX IMPLEMENTED — NOT RE-REVIEWED`, không CLOSED. Codex không đánh giá quyền của cài đặt, tải, đo, commit/push |
| SG-003 | **ACTIVE** (Project Owner, 2026-10-31, lời "Nghiên cứu trước"): nghiên cứu tài liệu license FFmpeg, resvg, CairoSVG, faster-whisper. Allowlist do Claude đề xuất, Owner chưa xác nhận từng dòng. Kết quả: [phase1-tools-candidates.md](docs/testing/phase1-tools-candidates.md) (đã đọc tiếp, mục 8): **FFmpeg 9.0.2 đề xuất nhóm B kèm rủi ro dư GPL-3.0-or-later (bản Homebrew) và sáng chế H.264 mà Owner phải chấp nhận riêng**; resvg vẫn A (Homebrew ghi MPL-2.0, upstream MIT/Apache-2.0, chưa giải thích); CairoSVG vẫn A (cần Python ≥ 3.10, phụ thuộc chưa đọc); faster-whisper vẫn A (PyAV/FFmpeg đi kèm chưa rõ, mô hình Systran MIT so với Whisper Apache-2.0). Chưa Codex review, chưa cài gì |
| SG-003 Amendment A01 | **APPROVED** (Owner, 2026-10-31, lời "Duyệt Amendment A01"): `CURRENT_STATUS.md` là nhóm A **chỉ đọc**, hash `962096ec…b961`; thay đổi có từ trước SG-003; không đặt lại bộ đếm |
| RR-007 | SG-003 vòng 0/3: **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-005 (MEDIUM, nhãn "B có điều kiện" chưa tách khỏi "B đã đủ bằng chứng") và P1-006 (LOW, thiếu cổng Codex PASS trước khi xin cài): Claude xác minh đúng cả hai, đã sửa, `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`; chưa CLOSED |
| RR-008 | SG-003 vòng 1/3: **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-006 **CLOSED** (Codex). P1-005 (MEDIUM) còn mở sau sửa một phần; P1-007 mới (MEDIUM, danh sách điều kiện trộn tầng và tạo vòng phụ thuộc). Claude xác minh đúng cả hai, đã sửa, `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |
| RR-009 | SG-003 vòng 2/3: **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-007 **CLOSED** (Codex); P1-006 vẫn CLOSED; P1-005 còn mở một điểm: tầng 1.1 (đọc toàn văn license phụ thuộc runtime). Claude đã đọc tệp license upstream của 11 phụ thuộc (mục 8.2 của hồ sơ), có giới hạn nêu rõ; `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |
| RR-010 | SG-003 vòng 3/3 (cuối): **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-005 **còn mở**: license chưa gắn đúng tag/commit của 11 phụ thuộc; LAME chưa có nguồn chính thức; lệch SVT-AV1 chưa đối chiếu v4.2.0. P1-006, P1-007 CLOSED. Hết vòng SG-003; Claude không sửa tiếp |
| SG-004 | **ACTIVE** (Owner, 2026-10-31, lời "Xác nhận allowlist"): xử lý P1-005 sau RR-010; 3 vòng mới độc lập với SG-003; allowlist và Amendment A01 (`CURRENT_STATUS.md` chỉ đọc, hash `962096ec…`). SG-003 vẫn ghi ACTIVE (Owner chưa quyết định) |
| RR-011 | SG-004 vòng 0/3: **CHANGES REQUESTED** (Codex), `ANSWERED`. P1-005 còn mở (sửa một phần): LAME, x265, mirror dav1d/x264, xz. P1-006, P1-007 vẫn CLOSED. Claude đã bổ sung: LAME tag RELEASE__4_0 (SVN chính thức), x265 tag 4.3 (kho Multicoreware), x264 COPYING tại commit, xz COPYING.0BSD/LGPLv2.1/GPLv2; mirror dav1d và x264 vẫn chưa xác nhận nguồn gốc |
| RR-012 | SG-004 vòng 1/3: **APPROVED WITH CHANGES — không phải PASS** (Codex), `ANSWERED`. P1-005 còn mở (Codex không đọc được vài URL; quan hệ mirror x264 chưa xác minh). P1-006, P1-007 CLOSED. Claude bổ sung URL thay thế (mục 8.4 của hồ sơ); phần còn lại là quyết định của Owner. Chưa đăng RR-013 |
| SG-005 (MVP video) | **ACTIVE** (Owner, 2026-10-31, "Duyệt SG-005+FFmpeg"). **Đã triển khai MVP cấp B, chờ Owner xem video:** `src/ai_video_factory/**` (Manager + 7 agent; Tesla và Newton là STUB), 29 unit test và 9 e2e test đạt. Video v1: `owner-1` (35.5 s). **Sau góp ý của Owner (giọng, minh họa, chuyển động, chữ lớn, keyword) đã làm lại: video v2 `workspace/runs/owner-3/spielberg/final.mp4` (49.2 s, 1080p24, H.264+AAC); 38 unit test, 14 e2e test đạt.** Giọng vẫn là macOS Linh (tổng hợp), minh họa là vector tự vẽ. **Vòng "MVP QUALITY UPGRADE" (2026-10-31): xong bước A–C** (audit hai video, bộ nhân vật gốc Mi và Bốp, prototype 15 giây, 3 mẫu giọng, đều ở `workspace/prototypes/` và `workspace/audit/`); **chờ Owner xem và chọn giọng/phong cách trước bước D** (video cải tiến). 50 unit test đạt. Giọng Linh (A–F) bị Owner từ chối (chưa tự nhiên). **Owner chọn giọng VieNeu Ngọc Huyền (2026-11-01); đã làm bước D: video v3 `workspace/runs/v3-2/spielberg/final.mp4` (58.7 s), pipeline có hook→kết, Mi và Bốp, nét vẽ dần, bong bóng thoại; chờ Owner xem.** Đã thử **VieNeu v3 Turbo** (Python 3.12, expat, venv `workspace/venv-vieneu`, chạy CPU nội bộ; mẫu G/H/I ở `workspace/prototypes/voice/m4a/`); chờ Owner nghe. FFmpeg 9.0.2_1 đã cài. **Chưa Human Approval, chưa Codex review, chưa commit.** Không phải cấp C. Stub và thay thế ghi ở `src/ai_video_factory/README.md` và `render_report.json` |
| SG-005 Amendment A04 | **Hoàn tất, chờ Owner xem mẫu** (Owner duyệt kế hoạch 2026-11-01, lời "Duyệt kế hoạch"): tỉ lệ khung `--aspect youtube/vertical/feed/square` (+ lệnh `rerender`), kịch bản viết từng cảnh với ý riêng và đo trùng lặp (`core/text_quality.py`), cổng Owner `--claims-gate`/`--script-gate`, nhân vật Lu và Giáo sư Tí, cử chỉ nhún vai/giới thiệu/nhảy/vỗ tay, biểu cảm hào hứng/lo lắng/tự đắc, đạo diễn theo nội dung (`core/direction.py`), 39 hình minh họa chọn theo nội dung (`core/props.py`). **Đã kiểm:** 70 unit test đạt; e2e 15/15 đạt (806 s); 7 video mẫu thật ở `workspace/deliver/a04/` (ffprobe: đúng kích thước, H.264+AAC, 24 fps). **Giới hạn thật:** nội dung LLM 8B vẫn có câu vô nghĩa/sai ý (kiểm tra chỉ theo quy tắc, không kiểm chứng sự thật), khung tham số hóa chưa xuất hiện trong video mẫu, một bản có 33% gần tĩnh, khung vuông có vùng minh họa nhỏ, Claude không nghe/đánh giá nghệ thuật. Chi tiết ở TASKS.md (SG-005 A04). Chưa commit |
| SG-005 Amendment A07 | **Hoàn tất, chờ Owner xem mẫu** (Owner, 2026-11-01, "Chỉnh theo góp ý"): một khung hình mỗi video; giáo sư là người giải thích; chữ phụ đề, từ khóa và nhãn sơ đồ hiện đúng lúc từ được nói (thời điểm từ ước lượng từ âm thanh); chữ minh họa là `board` ý chính + sơ đồ nhãn lấy từ lời giảng; `--lang vi|en`; `--voice` và danh mục 25+1 giọng vi, 18 giọng en. Video: `workspace/deliver/a07/`. 70 unit test đạt, e2e chưa chạy lại. **Chưa áp dụng tên agent mới** (không thấy trong PROJECT_MASTER.md; README MVP có 4 tên lạ thay tên cũ). Chi tiết và giới hạn: TASKS.md (SG-005 A07). Chưa commit |
| SG-005 Amendment A08 | **Hoàn tất, chờ Owner xem mẫu**: tên agent hiển thị mới (Hương Giang, Chớt, Thí Di, Hủ, Tứng, Mĩ Diên, Hoằng; mã định danh giữ ASCII, `core/names.py`); 4 phong cách (stickman, whiteboard, explainer, story) cho cùng một kịch bản và giọng, `manager.run styles`; xưng "bạn"; lời văn lôi cuốn; giọng nhấn âm lượng và nhiệt độ VieNeu 1.0; `--fast`. Video: `workspace/deliver/a08/`. Giới hạn: nội dung LLM 8B còn câu sai ý, không điều khiển được ngữ điệu, chưa chạy lại test sau A08, `PROJECT_MASTER.md` ngoài allowlist chưa đổi tên. Chưa commit |
| SG-005 Amendment A09 | **Sửa xong, chờ Owner xem mẫu và xác nhận kế hoạch tiếp theo:** whiteboard giữ màu và có bàn tay vẽ theo lời (`agents/spielberg/hand.py`); bỏ chữ Giáo sư ở explainer; bong bóng không đè chữ; `core/options.py` và `manager.run options` cho app sau này (4 phong cách, 2 ngôn ngữ, 26+18 giọng, 4 tỉ lệ); `run --styles all`. E2E phát hiện và đã sửa: kịch bản quá dài (131 s), `say` im lặng nhận giọng lạ, e2e trước đây chưa từng chạy VieNeu thật. 77 unit test đạt; e2e 14/15 rồi test hỏng và test_02 đạt sau sửa, 13 test còn lại chưa chạy lại. Video `workspace/deliver/a09/` dùng kịch bản Claude biên tập tay, không phải đầu ra LLM. Chưa commit: toàn bộ `src/`, `tests/` vẫn chưa nằm trong Git |
| Benchmark 12 giây (2026-11-01) | **Đã triển khai, chờ Owner xem và nghe:** chỉ đạo trực tiếp, không có Scope Grant riêng. `manager.run locked` (lời dẫn khóa, mốc theo âm thanh thật, rig Que, SFX tổng hợp, 30 FPS). Đầu ra `benchmarks/procrastination_12s/output/ai_factory_sample_12s.mp4`: ffprobe đạt 1080x1920, 30 FPS, 12.000 s, H.264 + AAC. 89 unit test đạt; e2e cũ chưa chạy lại sau khi sửa `draw_character`, Edison, `concat_with_gaps`. **Giới hạn:** biên đạo trong `agents/spielberg/stage.py` viết tay cho câu chuyện này; âm thanh chưa ai nghe; lời đọc chưa kiểm bằng ASR; VieNeu nhóm A, chỉ nội bộ; chưa commit. Việc tiếp theo: Owner xem, nghe, so sánh độc lập; dừng trước video 45 giây |
| Lượt làm việc | **Project Owner.** Không có RR đang mở. SG-004 còn 2 vòng (chưa dùng). Chờ Owner chọn: (a) đăng RR-013 để Codex xác nhận URL mới, (b) chấp nhận giới hạn mirror dav1d và x264, (c) cho tải chỉ để kiểm tra, hoặc (d) dừng. FFmpeg giữ trạng thái chờ, không cài, không commit/push. SG-003 vẫn ghi ACTIVE |
| Code ứng dụng | **NOT IMPLEMENTED** |
| Runtime testing | **NOT PERFORMED** |
| Phần mềm cài cho dự án, model AI, credentials | **Đã có (2026-10-31, Amendment A03):** Ollama 0.40.13 (Homebrew, kèm 10 gói phụ thuộc gồm `python@3.15`, `mlx`; Homebrew nâng lên 7.0.11) và model `qwen3:4b-q4_K_M` (digest khớp hồ sơ, SHA-256 blob tự tính). Đã tải thêm `qwen3:8b-q4_K_M` (A06, digest khớp, chưa chạy). **Đã đo thô Qwen3 4B** (A04, A05): nạp nguội 2.56 s, 34 token/s, RSS đỉnh 3,277 MB, `format` JSON schema 9/9 hợp lệ so với 2/9 không `format`; **Đo thô 8B (A07, không cô lập):** nạp 3.6 s, ~19 token/s, RSS đỉnh 5,796 MB, swap tăng ~740 MB; `format` giúp chia cảnh nhưng 8B ít lỗi hơn 4B khi không `format` (8/9 so với 2/9). Không bật dịch vụ nền. Credentials: chưa có |
| Git | Nhánh `main` ở `9838f0a`, trùng `origin/main` (Project Owner nói "Cho commit" và "Cho push" trong chat; **chưa ghi trong file repo**, xem RR-006). Working tree sạch lúc kiểm tra, trước khi đăng RR-006. **Repo từ xa CÔNG KHAI**: không đẩy secret, credentials, dữ liệu vận hành, model hay media |

## 2. Phân biệt trạng thái

| Hạng mục | Tài liệu | Thiết kế | Chủ dự án duyệt | Triển khai | Kiểm thử |
|---|---|---|---|---|---|
| Bộ tài liệu Phase 0 | Xong | – | Đã nghiệm thu | – | Kiểm tra tài liệu đã chạy |
| `.gitignore` | Xong | – | Đã nghiệm thu | **Xong** | **Đã xác minh** bằng lệnh |
| Queue: fencing, staging, BUSY, orphan | Xong | `Proposed` | Chờ, trước Phase 2 | Chưa làm | Chưa làm |
| Máy trạng thái upload, adapter | Xong | `Proposed` | Chờ, trước Phase 15 | Chưa làm | Chưa làm |
| TikTok Direct Post | Xong | **`POLICY BLOCKED`** | D-023 `Approved` chỉ cho đánh giá; chưa có quyết định triển khai | Không được triển khai | Chưa làm |
| Truy cập cục bộ | Xong | `Proposed` | Chờ, trước Phase 2 | Chưa làm | Chưa làm |
| OAuth, token | Xong | `Proposed` | Chờ, trước Phase 15 | Chưa làm | Chưa làm |
| Rights Gate, gói xuất bản | Xong | `Proposed` | Chờ, trước Phase 13 | Chưa làm | Chưa làm |
| Spike TTS | Xong | Đã lên kế hoạch | Theo Phase 1 | Chưa làm | Chưa làm |
| Mọi tính năng sản phẩm | – | – | – | Chưa làm | Chưa làm |

**Không tuyên bố queue an toàn.** Thiết kế chỉ mới được lập luận. Chỉ có `.gitignore` là cấu hình đã có hiệu lực và đã xác minh.

## 3. Blueprint đã duyệt

Factory Manager + bảy Agent (Athena, Leonardo, Edison, Pixar, Spielberg, Tesla, Newton). Local-first, sequential-first, scene-based rendering, SQLite, Quality Gate, phê duyệt của con người trước khi xuất bản, adapter module hóa. Máy mục tiêu: MacBook Air M4 không quạt (`Mac16,12`), 16GB, macOS 26. Xem `PROJECT_MASTER.md`.

## 4. Phát hiện review

### Vòng 4

| Mã | Mức | Vấn đề | Tình trạng |
|---|---|---|---|
| R4-01 | LOW | Lựa chọn C có thể bị hiểu là được triển khai Direct Post | **CLOSED** ở mức tài liệu (Codex) |
| F-01 | LOW | Ba dòng hiện hành chưa đồng bộ D-023 | **CLOSED** (Codex Final F-01 Verification) |

### Vòng 3 (chi tiết ở `REVIEW_RESPONSE.md`)

| Mã | Mức | Vấn đề | Tình trạng |
|---|---|---|---|
| R3-01 | HIGH | TikTok Direct Post xung đột với mục đích dùng cá nhân; audit không đủ để mở khóa | Đã có quyết định D-023. **Rủi ro chính sách chưa giải quyết**, giữ `POLICY BLOCKED` |
| R3-02 | MEDIUM | `pending_outcome` chưa tách thành công và lỗi | Codex: PASS ở mức đặc tả; chưa kiểm thử |
| R3-03 | LOW | Đồng hồ lùi khi Worker đang sống | Codex: PASS ở mức đặc tả; chưa kiểm thử |

### Vòng 2 (chi tiết ở `REVIEW_RESPONSE.md`)

| Mục | Vấn đề | Tình trạng |
|---|---|---|
| B | `.gitignore` phủ định quá rộng, làm lộ secret trong fixtures | **Đã sửa và xác minh** |
| C | `SQLITE_BUSY` chưa có hành vi khi hết ngân sách | Đã đặc tả |
| D | Tiến trình con mồ côi | Đã đặc tả |
| E | Thiếu kịch bản fault injection | Đã đặc tả, nay là FI-01 đến FI-51 |
| F | OAuth, TikTok | Đã đặc tả |
| G | Rights Gate chưa có ranh giới bắt buộc | Đã đặc tả |
| H | YouTube, Facebook | Đã đặc tả; **Facebook vẫn chưa xác minh** |

### Vòng 1

| Mã | Vấn đề | Tình trạng |
|---|---|---|
| B1 | Thiếu fencing | Đã đặc tả, chờ duyệt D-011, D-018 |
| B2 | Kết quả upload không rõ | Đã đặc tả, chờ duyệt D-019 |
| B3 | Quyết định chưa được duyệt trước Phase 2 | **Mở, chờ Chủ dự án** |
| B4 | Chưa xác minh quyền API và license | **Mở có kiểm soát**, đóng theo từng tích hợp |
| W2 | Chưa có bằng chứng khả thi | **Mở**, cần số đo Phase 1, 14 |
| W8 | Chính sách API | Ảnh chụp đã cập nhật; xác minh lại trước mỗi adapter |
| W9 | `.gitignore` | **Đã đóng ở vòng 2** |
| W1, W3–W7, W10, R1–R10 | Xem `REVIEW_RESPONSE.md` | Đã xử lý hoặc ghi nhận |

## 5. Quyết định chờ Chủ dự án

Tất cả là `Proposed`. Không có mục nào được duyệt thay cho Chủ dự án.

| Trước phase | Quyết định | Khuyến nghị |
|---|---|---|
| 1 | ~~D-013, D-017~~ | **Đã duyệt 2026-10-31** (D-013 chỉ duyệt phương pháp benchmark) |
| 2 | D-010, D-016, D-018, D-020 | Duyệt |
| 2 | D-009, D-011 (cùng D-018), D-015 (`.env`) | Duyệt có điều kiện |
| 4 | D-012 | Duyệt có điều kiện, sau số đo Phase 1 |
| 4 | D-014 | Hoãn tới Q-02 và số đo Phase 1 |
| 13 | D-022 | Duyệt |
| 15 | D-019, D-021, D-015 (Keychain) | Duyệt |

Đã duyệt: D-001 đến D-007, D-013, D-017, D-023 (chỉ cho đánh giá, không cấp quyền triển khai), D-024 (tiêu chuẩn S2, chỉ phân loại). Lead Developer: D-008.

## 6. Lịch sử thay đổi

**Bản sửa 1:** tạo `REVIEW_RESPONSE.md`, `HANDOFF_TO_CHATGPT.md`, ba đặc tả trong `docs/architecture/`, `docs/deployment/platform-verification.md`. Thêm D-018 đến D-022, spike TTS, cổng quyết định.

**Bản sửa 2:**

- `.gitignore`: chặn mặc định trong `tests/fixtures`, khối secret đặt cuối.
- `queue-safety.md`: viết lại; thêm `SQLITE_BUSY`, tiến trình mồ côi, `heavy.lock`, 43 kịch bản có đủ cột, oracle OR1–OR6. Thu hồi job chỉ lúc Worker khởi động.
- `publishing-reliability.md`: ranh giới adapter, TikTok, YouTube, Facebook, tiêu chí bổ sung.
- `security-and-rights.md`: `client_secret`, xác minh scope, token không tới dashboard, năm điều kiện tạo `queued`, `PublishGrant`.
- Cập nhật `platform-verification.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `DECISIONS.md`, `TECH_STACK.md`, các README trong `docs/`.

**Bản sửa 3:**

- R3-01: `platform-verification.md` mục 3, chặn TikTok ở `publishing-reliability.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `docs/requirements`; thêm rủi ro R13, D-023, Q-13.
- R3-02: `pending_outcome` hai loại `success`, `failure`; T11a–c; AC-Q18; FI-44 đến FI-49.
- R3-03: phát hiện và dịch lịch khi Worker đang sống, bước kẹp độc lập; AC-Q19; FI-32 sửa lại; FI-50, FI-51.

**Ghi nhận D-023 và R4-01:**

- D-023 `Approved`, phương án C; hai trạng thái độc lập; cổng G1–G5 ở `platform-verification.md` mục 3.
- `IMPLEMENTATION_PLAN.md`, `publishing-reliability.md`: bỏ cách viết khiến quyết định có thể bị hiểu là điều kiện đủ.

**Workflow mức B:** thêm `docs/operations/AI_REVIEW_WORKFLOW.md`; cập nhật `AGENTS.md`, `CLAUDE.md`, `TASKS.md`, `docs/workflows/README.md`, `docs/operations/README.md`. SG-001 và RR-001 nằm trong `TASKS.md`.

**Amendment A01:** Project Owner cấp thêm `REVIEW_RESPONSE.md` cho Claude và xác nhận reviewer artifact của Codex. Workflow chia file thành nhóm A, B, C. Vòng kế tiếp là 1/3, không đặt lại bộ đếm.

**Thay đổi kiến trúc:** không đổi blueprint, không thêm Agent, không đổi bộ công nghệ.

## 7. Lệnh và kiểm tra

Lệnh `.gitignore` và kết quả đầy đủ: `docs/operations/phase-reports/PHASE-00-REPORT.md`, Phụ lục 2. Codex đã chạy lại độc lập: 30/30 và 13/13 khớp. Kiểm tra Bản sửa 3: Phụ lục 3. Không có test tự động vì chưa có code.

## 8. Vấn đề đã biết

1. `tests/fixtures` chỉ lọc theo tên và đuôi tệp, không phát hiện secret trong nội dung tệp.
2. Orphan không nhận diện được chỉ bị giới hạn, không bị dừng.
3. `heavy.lock` không phủ yêu cầu đang chạy trong daemon Ollama.
4. Nếu không ai khởi động Worker, hoặc tiến trình ngoài giữ khóa DB vô thời hạn, job có thể vẫn `running` và cần người xử lý.
5. `flock` qua FFmpeg và hành vi `F_FULLFSYNC` là giả định thiết kế, cần thử thực tế.
6. Repo không có tệp báo cáo gốc của vòng 2.
7. `vi` (PID 3151) vẫn tạm dừng với buffer trống. **Không dùng `:w!` trong phiên đó.**
8. FI-43 chỉ kiểm tra đã gửi yêu cầu giải phóng model, chưa chứng minh tác vụ trong daemon Ollama đã kết thúc trước job mới.
9. Cách ly quyền Keychain giữa các tiến trình Python chưa được xác minh.
10. Luồng TikTok Upload vào inbox chưa xác minh: không rõ intended use và audit có áp dụng hay không.
11. F-01 đã đóng. `REVIEW_RESPONSE.md` Vòng 4 giữ nguyên làm lịch sử, nên vẫn trích câu chữ cũ.
12. `PROJECT_MASTER.md:8, 44` đã được sửa theo chỉ đạo của Project Owner: trạng thái nghiệm thu đã đồng bộ, tên máy đã bỏ.
13. `user.name` và `user.email` vẫn chưa được cấu hình. Hai commit đã tạo dùng danh tính `superemail0707` với email noreply do Project Owner chọn, truyền riêng cho từng commit; commit sau cần danh tính được cấu hình hoặc chỉ định lại. Chi tiết ở báo cáo Phase 0, mục "Chuẩn bị Git checkpoint".
14b. **Repo công khai.** Quét `HEAD` sau push: không secret, tên máy, đường dẫn cá nhân hay email; chỉ có tên tài khoản GitHub. Lịch sử Git không xóa sạch được nếu lỡ đẩy nội dung nhạy cảm, nên quét trước mỗi commit. Q-07 (sao lưu dữ liệu) cần tính tới việc này.
14. `refs/codex/turn-diffs/...` tồn tại trong `.git`. Khi push chỉ đẩy `main`, không dùng `git push --mirror`.

## 9. Trở ngại còn lại

1. Phase 0 đã nghiệm thu. Phase 1 chỉ được phép ở bước 1.0 (không cài đặt, không tải). Nghiệm thu không xác nhận code đã triển khai hay runtime test đã pass.
2. Cài đặt và tải model ở các bước sau cần xác nhận từng lệnh; danh sách ứng viên bước 1.0 cần Owner duyệt trước. Q-03, Q-06 đã trả lời; ngân sách 4 giờ chặt hơn giả định 8 giờ, nên mục tiêu một video mỗi ngày (R2) càng cần số đo thực.
3. Phase 2 cần các quyết định ở mục 5.
4. Chưa có bằng chứng về TTS tiếng Việt, tốc độ render, nhiệt, RAM.
5. Chính sách nền tảng chưa đủ cho bất kỳ adapter nào; TikTok Direct Post `POLICY BLOCKED`; Facebook chưa xác minh.

## 10. Bước tiếp theo đề xuất

SG-002 `ACTIVE` với Amendment A01. RR-003 (vòng 0/3) bị `CHANGES REQUESTED`; Claude đã sửa P1-001 và P1-002; **Codex kết luận APPROVED tại RR-004 (vòng 1/3) và đóng cả hai finding.** **Sau đó Owner chọn S2** (nguyên văn "Chọn S2"). Claude chuyển Qwen3 4B và 8B `q4_K_M` lên **nhóm B theo S2** (LICENSE Apache-2.0 và Ollama MIT đã đọc; dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận; giới hạn định danh đi cùng hồ sơ) và đăng RR-005 (vòng 2/3); **Codex kết luận APPROVED, không có finding mới**. Lượt thuộc về Owner; bảng quyết định cuối cùng ở `REVIEW_RESPONSE.md`. Bước 1.0: `docs/testing/phase1-candidates.md`. **Piper `vais1000` bị loại** (tinh chỉnh từ lessac, dữ liệu Blizzard 2013 chỉ cho nghiên cứu); VieNeu-TTS 0.3B và 0.5B bị loại (dữ liệu CC BY-NC); VieNeu v3 Turbo, Kokoro, Piper `ljspeech` nhóm A. Chưa có TTS tiếng Việt nào đủ điều kiện (R1). Báo cáo pre-approval gốc của Codex không có trong repo. Owner cần quyết định (độc lập nhau): hướng TTS tiếng Việt (`phase1-candidates.md` mục 7); duyệt danh sách model; quyền tải, cài, chạy từng bước; Amendment cho `CURRENT_STATUS.md` (đang lệch, còn ghi Qwen3 nhóm B theo cách cũ và lượt cũ). Claude không tự cài đặt, tải model, commit hay push.

## Trỏ tới MVP hoàn chỉnh (2026-11-05, Claude)

Code MVP mới nhất **không nằm trong repo này**: baseline Owner duyệt (Codex, 2026-11-03) và phần hoàn thiện prompt → video của Claude ở `../AI-VIDEO-FACTORY-BLITE-POC/` (không có `.git`). Chi tiết, kiểm thử và giới hạn: mục "MVP completion — prompt → video — 2026-11-05" trong `../AI-VIDEO-FACTORY-BLITE-POC/HANDOFF_TO_CHATGPT.md`. `src/`, `tests/` ở đây là bản cũ hơn và chưa từng commit. Chưa commit, chưa push; chuyển code vào Git cần Owner quyết định.

## Handoff thư viện nhân vật — 2026-11-05

Đọc [Visual Quality Gate](character_library/CHARACTER_ASSET_REPORT.md) và asset_index.json. 90 PNG nguồn giữ nguyên, 8 bản Mimi v2 có liên kết nguồn. Chờ Owner duyệt 29 In Review. Các pose xoay cần vẽ lại khớp và các mắt Mimi v2 vẫn cần sửa. Không dùng Needs Revision trong tuyển chọn mặc định. Không chuyển sang sản xuất video. SDXL chưa benchmark và chưa chạy thử animation.

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

## EP08 dựng lại bằng Codex ImageGen (visual_rebuild_v01) — 2026-11-07 (Claude, phiên Mac)

**Hình (Implemented, Owner duyệt "Duyệt cả bộ").** 15 sprite mới tạo bằng `codex_ask` (MCP codex-app-server, workspace-write, 600 s/lượt, tuần tự J01–J09) trong `output/ep08_ngay_dau_vs_nam_ba/visual_rebuild_v01/` (`raw/`, `sprites/`, `codex_results/`, `review/before_after.jpg`, `review/storyboard_v01.jpg`, `manifest.json`). Tái dùng 3 hình đã duyệt (NGANG_WARDROBE_010, TI_WARDROBE_006, TI_WARDROBE_008).
- Sửa sau kiểm tra: FIX01 tách nền lại (magenta kín ở TI_Y1_GALA_ADORE 643 px, NGANG_Y1_GALA_SHY 213 px; khói hồng ở TI_Y3_HOME_OFFER_MUG); FIX02 vẽ lại mắt TI_Y3_JERSEY_SOFA_PHONE nhìn xuống điện thoại (raw v2). Bản trước sửa ở `sprites/_superseded/`.
- Lưu ý ImageGen: tối đa **5 ảnh tham chiếu/lần gọi** (J06 lần đầu lỗi `referenced_image_paths must contain at most 5 paths`). Tách nền chỉ bằng flood-fill từ mép sẽ sót magenta ở vùng kín → luôn yêu cầu xoá cả vùng kín magenta bão hoà.
- Thư viện: `register_approved.py` (dùng `library_sync.register`) thêm 15 mục `approved`, `consistency_check=owner_image_approved`, `rebuild=visual_rebuild_v01` vào `asset_index.json` (236 → 251), ảnh ở `character_library/episode_approved/ep08_ngay_dau_vs_nam_ba/`. Thay đổi chỉ thêm mục; backup ngày `metadata_backups/asset_index.2026-11-07.json` là bản sáng 07/11.

**Video (Owner duyệt video cuối 08/11 00:00, "Duyệt, xuất NMT"; đã xuất).** Owner: "Dựng video thay thế bản cũ". `final_video.mp4` v2: 1080×1920, 60 fps, 31,28 s (6 cảnh, 1877 khung), sha256 `8900cec9dafc…`. Bản v1 (đã duyệt, tóc rối v1) sao lưu đầy đủ ở `output/ep08_ngay_dau_vs_nam_ba/_superseded_v1_2d/` (video, segments, stills, export sạch, render/*.py, workflow.json cũ, bản sao `videos-post/` cũ; sha256 video khớp). `render/ep08_scenes.py` dùng sprite mới (hàm `fp`: sprite toàn thân cắt ngang gối ở mép khung chia đôi); kịch bản, giọng, SFX, thời lượng giữ nguyên. Cổng hình và video cuối ghi theo lời Owner trong chat (ghi chú trong workflow.json).
- Xuất 3 nền tảng (tiktok, youtube_shorts, facebook_reels) qua `--export` + `--export-finish`: watermark NMT **PASS** cả 3 (box 842,1789,190×83, opacity 0,85), 31,28 s, −15,2 LUFS (bằng v1), nguồn khớp sha video v2. `videos-post/ngay-dau-yeu-vs-nam-thu-3/` đã thay bằng bản v2; bản sạch mới `render/export/<nền tảng>/…_clean_20261108-*.mp4` (bản sạch v1 không bị ghi đè). Chưa đăng.
- `episode_approved/ep08_ngay_dau_vs_nam_ba/usage.json` ghi lại cho v2 (ghi tay, không dùng `--library-sync` vì sẽ ghi đè ghi chú 15 mục mới); usage v1 ở `_superseded/usage_v1.json`.

**Còn mở:** F05 Ngang (Owner đã duyệt video, chấp nhận) (trước câu chốt) đang cầm cốc riêng trong lúc Tí đưa cốc; `TASKS.md`, `CHANGELOG.md` chưa cập nhật vì tiến trình máy ảo của phiên cloud cũ đang mở hai file này; câu hỏi cũ (watermark khung ngang 170 px; ep08b tóc v2).

### EP08 v2 — sửa phụ đề đè nhân vật + quy tắc cải tiến liên tục (2026-11-08)

- **Owner báo lỗi:** phụ đề đè lên nhân vật ở một vài khung; yêu cầu phụ đề ở dưới, không đè nhân vật; pipeline phải "luôn luôn cải tiến qua từng ngày".
- **Nguyên nhân gốc và cách chặn:** ghi ở `output/_engine/IMPROVEMENT_LOG.md` (mục đầu tiên). Engine `cute_engine.py` thêm `check_subs()` / `--check-subs [nền tảng]` (dựng mỗi khung có và không có sprite để đo phụ đề đè nhân vật), `--mux` và `--export-finish` **tự chặn** khi vi phạm; `sub_tray()`, `tray_top()`, `sub_y_bottom()` cho cảnh toàn khung; `panel_layout()`, `panel_center()` thu khung chia đôi theo vùng an toàn từng nền tảng (chừa zoom `PANEL_ZOOM_MAX` 1,08). Bản gốc không xuất nền tảng của các tập cũ giữ nguyên bố cục khung chia đôi.
- **Trước sửa (đo):** bản gốc F04 99,8%, F05 46,6%; TikTok thêm F01 10%, F02 15%, F03 1%. **Sau sửa:** bản gốc, TikTok, YouTube Shorts, Facebook Reels: 221 khung mẫu/bản, đè 0,0%. Unit test mới `tests/unit/test_subtitle_layout.py`: 6/6 đạt (`python3 -m unittest tests.unit.test_subtitle_layout`).
- `ep08_scenes.py`: cận F02, F04, F05 có dải phụ đề, nhân vật đặt trên `tray_top()`; F05 bỏ má hồng vẽ thêm (sprite đã có).
- Video mới `final_video.mp4` (31,28 s, −18,8 / −1,0 dB, sha256 `0403f43cb03f…`). **Owner duyệt video cuối 08/11** ("Duyệt, xuất video cuối đảm bảo subtitle không đè lên watermark").
- **Phụ đề không chạm watermark:** `check_subs(plat)` thêm đối chiếu hộp phụ đề thật với hộp watermark tính bằng `branding.geometry` (hở ≥ 24 px, `WM_PAD`); `--export-finish` chặn khi chạm. Unit test 8/8, `test_branding` 20/20.
- **Đã xuất lại 08/11 08:45:** 3 nền tảng, watermark PASS (x 842–1032, y 1789–1872), 31,28 s, −15,2 LUFS, nguồn khớp sha video v2; `qa_subtitles_<nền tảng>.json`: 221 khung, đè nhân vật 0,0%, chạm watermark 0. Claude trích khung từ 3 file `_nmt` kiểm tra bằng mắt. Bản sạch mới `render/export/<nền tảng>/…_clean_20261108-0844*.mp4`. Chưa đăng.
- Tài liệu đã cập nhật: `COUPLE_ENGINE.md`, `IMPROVEMENT_LOG.md`, `.claude/commands/couple-engine.md`, `docs/requirements/WATERMARK_NMT.md`, `TASKS.md`, `CHANGELOG.md`, `CURRENT_STATUS.md` (máy ảo phiên cloud cũ giữ handle chỉ đọc trên vài file; Owner yêu cầu cập nhật nên đã sửa theo kiểu chỉ thêm).

### Hình ảnh mặc định và EP10 — 2026-11-08

Owner chốt comic Nhật theo video Ngày đầu yêu vs năm thứ 3 làm mặc định; Mimi là thú cưng của Ngang. EP10 cập nhật bối cảnh bám lời hát. Bảng font Be Vietnam Pro có ba độ đậm, đã kiểm tra glyph và render, chờ Owner chọn. Kịch bản EP10 đang chờ duyệt, mốc nhạc chưa xác minh.

### EP10 — phạm vi nhạc và hình bản 02, 2026-11-08

Owner chọn Itim cho EP10 và chỉ định đoạn từ phần xin số điện thoại đến hết post-chorus đầu. Độ dài theo bản thu, không áp mốc 25–35 giây cũ. Kịch bản mới gồm 13 nhịp, 12 khung, trang phục xanh phấn/vàng bơ và cú lật tuyển người chăm Mimi. Bộ mới ở output/ep10_vi_anh_qua_dep_trai/visual_rebuild_v02/. Chờ duyệt kịch bản/hình bản mới. Mốc cắt âm thanh vẫn chưa xác minh.


### EP10 — Bản video xem trước và Whisper local, 2026-11-08

Thay thế trạng thái chờ duyệt kịch bản/hình v02 ở ghi chú trước: Owner đã duyệt v02 và cho phép tải Whisper Small. Đã chạy faster-whisper Small MIT tại máy (CPU int8; 23,776 s), xử lý lỗi PyAV bằng FFmpeg ndarray. Mốc cắt ASR 31,10–86,35 s. Đã dựng `output/ep10_vi_anh_qua_dep_trai/final_video.mp4`: 55,25 s, 1080×1920/60 fps, 13 cảnh, Itim, twist Con sen mới. Full decode PASS; 514 mẫu phụ đề không đè nhân vật. Lưới trích MP4 `render/video_contact_sheet.jpg`; báo cáo `PRODUCTION_REPORT.md`, `render/video_qa.json`. Animation sprite, chưa rig/lip-sync. Cutout mới vẫn In Review. Âm thanh preview cuối −14,33 LUFS/−3,12 dBTP sau bổ sung headroom AAC; đạt giới hạn đỉnh. **Chờ Owner nghe/xem duyệt video cuối**, chưa xuất videos-post và chưa đăng.

### EP08 v2 — bố cục nội dung 3/4 trên, phụ đề 1/4 dưới (2026-11-08, Owner duyệt video cuối, đã xuất NMT)

- **Xuất 08/11 12:42:** 3 nền tảng, watermark PASS, 31,28 s, −15,2 LUFS, nguồn khớp sha video `dd04ac39a9f0…`; `qa_subtitles_*`: dải 25%, đè nhân vật 0%, ngoài dải 0, chạm watermark 0; đã xem khung từ 3 file `_nmt`. Chưa đăng. Bản xuất 08:45 (bố cục cũ) bị thay; bản sạch các lần trước giữ trong `render/export/<nền tảng>/`.

- **Owner:** phụ đề chỉ chiếm 1/4 khung (3/4 trên cho nội dung), không che watermark; các tỉ lệ khác được linh hoạt nhưng phụ đề không quá 1/3.
- **Engine (`cute_engine.py`):** `CONTENT_FRAC` = 0,75, `SUB_BAND_MAX` = 1/3 (`band_frac()` chặn khi vượt); `tray_top()` = H × CONTENT_FRAC (1440). `subtitle()` tự vẽ dải và đặt phụ đề sát mép trên dải, giống nhau ở mọi bản, tự né watermark nếu nhiều dòng; `panel_layout()` áp dụng cả bản gốc; `check_subs()` thêm `outside_band`. Backup engine trước sửa: chỉ trong scratchpad phiên (không trong repo).
- **Kiểm thử:** `tests/unit/test_subtitle_layout.py` 10/10; `--check-subs` bản gốc + 3 nền tảng: 221 khung, đè nhân vật 0%, ngoài dải 0, chạm watermark 0, dải 25%. Video `final_video.mp4` 31,28 s, −18,8 / −1,0 dB, đã xem lưới khung. **Chờ Owner duyệt video cuối**; `videos-post/` vẫn là bản xuất 08:45 (bố cục cũ) cho tới khi duyệt và xuất lại.
- **Rủi ro:** UI TikTok/Reels che khoảng 300–440 px đáy màn hình, phụ đề y ≈ 1460–1660 có thể bị caption của app che một phần (chưa đo trên app thật).
- **Phát hiện ở `src/` (chưa sửa, cần Scope Grant):** 16:9, 4:5, 1:1 có hộp phụ đề 2–3 dòng chồng lên watermark NMT; chi tiết trong `docs/requirements/WATERMARK_NMT.md` mục 5 và `IMPROVEMENT_LOG.md`. Dải phụ đề của `src/` đạt ≤ 1/3 (19–26%).


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

### EP15 — Chill bên suối rừng (nmt-engine), 2026-11-11 — Owner duyệt video cuối, đã xuất NMT, chưa đăng

- Video thư giãn 90 s, không thoại/không chữ, loop liền mạch; tập `output/ep15_chill_ben_suoi_rung/` (README tập ghi chi tiết).
- Hình: cửa sổ máy quay trên một tranh Owner gửi (Owner chọn cắt cận khi Codex image_gen hết lượt); chuyển động procedural trong `render/ep15_scenes.py` (không rig/lip-sync). Renderer riêng của tập, chưa đổi engine chung.
- Âm thanh: Owner chê bản tổng hợp numpy (v1) và lofi ZHRØ (v2); chốt phương án C — "Slow_Memory_80BPM" + suối + chim, đều CC0 Freesound (preview MP3 128 kbps), tải từng file khi Owner cho phép. Nguồn/SHA: `audio/CREDITS.md`.
- Đã kiểm: 1080×1920 60 fps 5400 khung; master −14,5 LUFS; 3 bản xuất −14,0 LUFS, watermark PASS, cùng SHA `7f01c6dc…`; khung an toàn ở 3 mốc; nối vòng chênh 0,31/255 (raw). Chưa nghe bằng tai, chưa xem trên điện thoại; cover.jpg (1080×1920, toàn cảnh render lại không lá rơi, không chữ/watermark) đã thêm vào 3 thư mục theo yêu cầu Owner, ghi trong manifest; nguồn `render/cover_source.png`.
- Bài học ghi ở `output/_engine/IMPROVEMENT_LOG.md` (2026-11-11). Không commit/push.
