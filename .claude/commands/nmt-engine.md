---
description: "NMT-engine (Ngang Một Tí) — dựng video hoạt hình 2D Tí, Ngang, Mimi: đời thường, hài, hội thoại hoặc theo nhạc; storyboard, phụ đề, outro và bản xuất NMT. Dùng /nmt-engine <chủ đề>."
argument-hint: <chủ đề>
---

Chủ đề: **$ARGUMENTS**

Bạn đang chạy **NMT-engine — Ngang Một Tí**, bộ dựng video hoạt hình 2D có cổng duyệt của dự án này, với Tí, Ngang và mèo Mimi là thú cưng của Ngang. Lệnh này tạo **video hoàn chỉnh**, không chỉ kịch bản. Tuy vậy, phải đi tuần tự và **dừng chờ Owner duyệt ở từng bước**.

Trước khi làm, đọc `output/_engine/NMT_ENGINE.md` (nguồn sự thật), `output/_engine/IMPROVEMENT_LOG.md` (bài học từ lỗi đã gặp, bắt buộc áp dụng) và `CLAUDE.md`.

## Các bước

0. Chạy `python3 output/_engine/nmt_engine.py list`.
   - Nếu chủ đề đã có tập, đọc `CURRENT_PREVIEW.json` nếu có và workflow của revision đang hoạt động; tiếp tục đúng bản hiện hành.
   - Nếu chưa có, chạy `python3 output/_engine/nmt_engine.py new "$ARGUMENTS"`.
1. **Kịch bản — theo chuẩn "Viral Storyboard Agent V2.0"** (`output/_engine/prompts/viral_storyboard_agent_v2.md`, D-030; đọc toàn văn trước khi viết)
   - PHASE 1 Ideation: phân tích topic (8 câu hỏi), tạo 3 concept A Relatable / B Absurd meme / C Cinematic parody thật sự khác cơ chế, chấm thang 100 (hook 15, hình 20, twist 20, nhịp 15, đồng cảm 10, nhân vật 10, sản xuất 10). **Tự chọn concept điểm cao nhất** (gần điểm: ưu tiên twist hình ảnh mạnh, ít thoại), **hiện bảng so sánh trong chat rồi viết tiếp** (Owner 12/11). Giữ nguyên nội dung/nhân vật/kết thúc Owner đã định trong brief.
   - PHASE 2–3: HSETL (hook 0–3 s ưu tiên cho thấy kết quả trước, setup, E1/E2/E3 khác nhau, gieo chi tiết cho twist, khoảng lặng trước twist, last laugh), 1 cơ chế hài chính + ≤ 2 bổ trợ, style A–G (≤ 3) đặt trên master S1/S2/S3 đã duyệt. Thời lượng **theo topic** (D-030), ghi `META["duration_s"]`; không thêm cảnh lặp để đủ giờ. Ghi `META["ideation"]`, `comedy`, `twist_seed`, `visual_styles`, `audience`; mỗi cảnh trong `notes` gồm mục đích, hình, biểu cảm cụ thể, hành động, góc máy + chuyển máy, SFX, nhạc, continuity. Lời dẫn không kể lại điều hình đã rõ. Mỗi câu thoại tối đa 45 ký tự.
   - PHASE 4 (sau khi kịch bản qua cổng): prompt ảnh 10 phần → `art/PROMPTS_v01.md`; prompt Image-to-Video 10 phần → `art/I2V_PROMPTS_v01.md` (xuất kèm cho Owner; engine vẫn tự dựng key pose). PHASE 6: `post.json` có 3 tiêu đề (tò mò/hài/ngắn), thumbnail (mô tả + prompt, không lộ hết twist), caption, câu hỏi gợi mở (không kéo tương tác giả tạo).
   - PHASE 5 tự soát 15 câu QC của Agent V2.0 trước khi chạy `--script-review`; không tuyên bố video chắc chắn viral.
   - Chạy `python3 epNN.py --script`, rồi trình bày toàn bộ kịch bản trong chat.
   - Toàn bộ kịch bản phải hiển thị trực tiếp trong chat, gồm từng cảnh, hành động/biểu cảm, lời thoại hoặc không thoại, âm thanh và outro. Gửi nội dung đầy đủ trước câu hỏi có hai lựa chọn Duyệt / Cần chỉnh; không chỉ gửi đường dẫn file hay thông báo đã sẵn sàng. Lời nhắc và câu trả lời duyệt phải chỉ rõ tập/phiên bản. Yêu cầu cập nhật quy trình hoặc góp ý không được tính là duyệt; chỉ ghi nhận duyệt khi Owner xác nhận rõ ràng.
   - **Chấm tự động (D-029, 12/11/2026):** chạy `python3 epNN.py --script-review`. Luật cứng (≤ 45 ký tự, Mimi không nói, không đọc nhãn "twist/hook", không TODO, thời lượng, hook ≤ 2 s) rồi giám khảo Codex độc lập chấm thang 10. **Quy trình chuẩn v2 (D-032, Owner 18/11/2026; đọc `output/_engine/NMT_STANDARD_PROCESS.md`): qua khi rubric ≥ 9/10 VÀ hội đồng người xem đạt (`--script-review viewer-prompt` → subagent Claude MỚI **model `sonnet`** (Owner 19/11/2026: tiết kiệm chi phí) → `--script-review viewer <file.json>`) → cổng kịch bản tự duyệt**: vẫn trình bày đủ kịch bản + điểm trong chat, không chờ. Chưa đạt → sửa đúng theo góp ý, `--script`, `--script-review` (không chấm lại bản cũ). Codex lỗi/hết lượt → `--script-review prompt`, gọi subagent Claude MỚI (không đưa lịch sử; giám khảo rubric giữ model mặc định Opus để điểm ổn định) chấm theo file đó, rồi `--script-review record <file.json> --judge claude-subagent`.
   - **Rule Owner 13/11/2026:** tổng điểm **> 9,0/10 (> 90/100) → mặc định được duyệt**, kể cả khi giám khảo (vd. subagent Claude) chưa qua hiệu chỉnh; đúng 9,0 trở xuống mà giám khảo chưa hiệu chỉnh thì vẫn chuyển Owner. Mọi lần chấm (điểm mất theo mục, góp ý, lỗi luật cứng) tự ghi vào `output/_engine/script_review_findings.jsonl`. **Trước khi viết kịch bản tập mới** chạy `python3 output/_engine/script_review.py findings` và tránh lặp các lỗi đứng đầu danh sách; lỗi Owner phát hiện thêm thì ghi vào `IMPROVEMENT_LOG.md`.
   - ⛔ Chuyển Owner duyệt khi: 3 lần chưa đạt, giám khảo chưa qua hiệu chỉnh (`script_review.py calibrate`), hoặc `META["script_gate"]="owner"`. Khi đó trình bản điểm cao nhất kèm điểm, góp ý cả 3 lần; khi duyệt: `--approve script --by "owner (chat)"`.
2. **Giọng và hình mẫu**
   - Với video thoại: chạy `--tts`. Với video theo nhạc: dùng âm thanh/đoạn đã được Owner cung cấp và duyệt, căn lời tại máy bằng workflow của tập; không tạo TTS chồng bài hát. Viết `epNN_scenes.py`, rồi chạy `--storyboard` khi tập dùng CLI chuẩn.
   - **Tranh tự động (D-029):** viết `art/PROMPTS_v01.md` (mỗi cảnh `### A01 — …` + khối ```prompt```, theo mẫu `_engine/prompts/art_scene_v1.md`: nhân vật ở 2/3 trên, 1/3 dưới trống), rồi `python3 epNN.py --art-auto`. Mỗi cảnh một phiên Codex mới, tự kiểm và tạo lại tối đa 3 lần, ngân sách 3 × số cảnh + 3 lượt. Codex hết lượt → **cách tạm thời (Owner 13/11/2026): tạo qua ChatGPT web bằng Playwright** — `python3 output/_engine/chatgpt_art.py <tập> A01,…,A06 [--new]` rồi chạy `browser_run_code_unsafe` với file JS in ra (hồ sơ Chrome Playwright có sẵn đăng nhập ChatGPT của Owner; lô đầu `--new` để đính kèm 3 master reference; ≤ 6 cảnh mỗi lô; cảnh đã có file thì bỏ qua). Nếu hồ sơ bị một cửa sổ Playwright cũ chiếm ('Browser is already in use') thì hỏi Owner trước khi đóng cửa sổ đó. Không lái được ChatGPT → DỪNG báo Owner; không dùng dịch vụ trả phí, không đăng nhập thay Owner. Cảnh lỗi bố cục sau khi xem overlay: `--art-auto A01 --fix "đáy nhân vật quá thấp …"`.
   - **Tiết kiệm token khâu tranh (Owner 19/11/2026):** mỗi prompt có dòng `CAST: <chỉ các nhân vật trong khung>`; `chatgpt_art.py` tự nối luật khung chặt (`STRICT`). Đo vị trí bằng `python3 output/_engine/art_measure.py <tập>` → xem MỘT tấm `art/v01/_qa/measure_sheet*.jpg` (¼ độ phân giải, có thước) thay cho nhiều lượt xem ảnh lớn; screenshot trình duyệt chỉ khi có lỗi.
   - Tự kiểm tra theo checklist ở mục 4 của NMT_ENGINE.md. Với tranh image_gen: chạy `--check-art`, xem `art/vNN/_qa/*_overlay.jpg`, ghi `safe_annotations.json` rồi chạy lại đến khi đạt (`--storyboard` bị chặn nếu chưa đạt). Cảnh mới dùng `import scene_kit as K` thay vì chép hàm phụ (mục 4.1).
   - Gửi `contact_sheet.png` kèm mô tả từng cảnh.
   - ⛔ CHỜ duyệt. Khi duyệt: `--approve visual`.
3. **Video**
   - **Rule Owner 13/11/2026:** (a) **nhạc nền (Owner 19/11/2026, thay rule 13/11): ưu tiên dùng lại nhạc có sẵn trong kho nếu hợp tập** (`qa_checks.music_library("output")` liệt kê theo SHA + tập đã dùng + nguồn); chỉ tìm và tải nhạc CC0 mới khi kho không có bản phù hợp — tải mới vẫn phải xin Owner từng file. `--mux` chỉ báo nhạc đã dùng ở tập nào, không chặn (muốn bắt buộc nhạc riêng: `META["music_unique"]=True`). (b) Mọi video kết bằng cảnh **Outro** "Đăng ký" kiểu lower-third **y như clip mẫu của Owner** (`avatar_banner/ScreenRecording_11-13-2026 20-55-26_1.mov`, Owner 13/11/2026 lần 2): `SCENES.append(("Fxx", 7.8, "Outro", "cut", 0.0))` + `FUNCS["Fxx"] = lambda t: K.subscribe_outro(t, art("<tranh cảnh cuối>"))` + `SFX += K.subscribe_sfx("Fxx")` — avatar kênh (`avatar_banner/nmt_channel_avatar.png`) bật ra, vệt khói, thanh trắng LIKE · ĐĂNG KÝ · CHUÔNG, con trỏ bấm lần lượt, thu vào và biến mất. **Owner xác nhận 18/11/2026: bỏ outro icon/chân mèo khỏi mọi bản dựng mới, dùng mặc định outro 7,8 s này; không gọi `K.outro_cta` hoặc `OUTRO_TAPS`. Kiểm tra cả xuất hiện và biến mất trên MP4.**
   - Render từng cảnh, mỗi lượt dưới 180 s. Sau đó chạy `--audio` và `--mux` (`--mux` tự chặn khi `--check-transitions`/`--check-sync` lỗi). Cuối tập chạy `--metrics` để ghi số đo.
   - Kiểm tra lưới khung hình và `volumedetect`.
   - **Review video độc lập (rule Owner 13/11/2026, bắt buộc trước khi gửi Owner):** `python3 output/_engine/video_review.py prepare <tập>` → gọi subagent Claude MỚI **model `sonnet`** (không lịch sử; Owner 19/11/2026) đọc `render/video_review/vNN/prompt.md` + các lưới khung hình, ghi JSON → `video_review.py record <tập> <file.json> --judge claude-subagent`. Đạt khi ≥ 8/10 và không còn lỗi chặn. Chưa đạt: sửa, render lại, `prepare` lại; tối đa 3 lần, sau đó gửi Owner kèm điểm và lỗi còn lại. Gửi `final_video.mp4` cho Owner kèm kết quả review.
   - **Bộ nhận diện kênh:** viết kịch bản và dựng theo `docs/marketing/BRAND_NMT.md` (khung nguệch ngoạc, Mimi phán xét, mở bằng kết quả/phản ứng — **không chữ tiêu đề đầu video**, không ép "Chuyện nhỏ!" (Owner 18/11); video ≥ 60 s; phụ đề chữ trắng nền đen + keyword vàng chạy theo giọng `K.word_sub` — 1 dòng, ≤ 4 chữ/cụm, ngắt theo nhịp giọng; sau `--tts` soát `K.sub_chunk_report(<tập>)`, câu cụt nghĩa thì chỉnh `K.SUB_BREAKS` (Owner 19/11); thumbnail theo `output/_engine/prompts/thumbnail_designer_v1.md` (tranh image gen không chữ + `K.make_thumbnail_v2`, kiểm bản 1/6 và che mép); ảnh kết + outro 7,8 s, SFX outro ×0,5, nhạc outro 35 %; từ ngữ đời thường, phóng đại).
   - ⛔ CHỜ duyệt. Khi duyệt: `--approve final`.
4. **Xuất đa nền tảng**
   - Viết `post.json`, chạy `--export tiktok|youtube_shorts|facebook_reels …`, rồi `--export-finish`.
   - Kết quả nằm ở `videos-post/unpost/<slug>/<nền tảng>/`. **Không tự đăng.** Đăng xong 3 nền tảng: ghi `PUBLISHED.json` rồi chuyển cả thư mục sang `videos-post/posted/<slug>/`.
   - `--export-finish` tự thêm hình của tập vào thư viện (sprite ghép + tranh cảnh, Owner 12/11/2026). Khai báo `LIBRARY_ART` trong `epNN_scenes.py` để mục thư viện có mô tả; báo Owner số hình đã thêm. Renderer riêng thì chạy `--library-sync` bằng tay.

## Quy tắc

- Chỉ dùng sprite có trạng thái approved trong `character_library/asset_index.json`.
- Phải tìm hình trong thư viện trước. Chỉ ghép ảnh khi thiếu hình, và phải nói rõ với Owner.
- Mimi không nói. Phụ đề không ghi tên nhân vật.
- **Bố cục khung: nội dung 3/4 trên, phụ đề 1/4 dưới** (Owner 08/11/2026). Mọi nhân vật, khung, đạo cụ nằm trên `E.tray_top()`. Được chỉnh `E.CONTENT_FRAC` tùy nội dung, nhưng dải phụ đề không bao giờ quá 1/3 khung (engine chặn).
- **Phụ đề đặt ở dưới, KHÔNG đè lên nhân vật và KHÔNG chạm watermark NMT** (Owner 08/11/2026), ở bản gốc lẫn 3 bản nền tảng. Cảnh toàn khung dùng `E.sub_tray(im)` + `subtitle(im, tg, y=E.sub_y_bottom())` và đặt nhân vật phía trên `E.tray_top()`; cảnh chia đôi tự thu theo `E.panel_layout()`. Chạy `python3 epNN.py --check-subs [nền tảng]` trước khi gửi duyệt; `--mux` và `--export-finish` tự chặn khi phụ đề đè nhân vật.
- **Cải tiến liên tục mỗi ngày** (Owner 08/11/2026): mỗi lỗi Owner phát hiện phải (1) sửa trong tập, (2) tìm nguyên nhân gốc, (3) thêm quy tắc hoặc **kiểm tra tự động** vào engine để lỗi không lặp lại ở tập sau, (4) ghi vào `output/_engine/IMPROVEMENT_LOG.md`. Đầu mỗi phiên làm tập mới, đọc sổ này và áp dụng hết các bài học trước khi gửi Owner duyệt.
- Hỏi duyệt ngay trong chat bằng câu hỏi lựa chọn. Không bắt Owner mở file.
- Nếu Owner chọn "Cần sửa" mà không ghi rõ, phải hỏi lại.
- Chỉ dùng tool, plugin, model và mã GitHub miễn phí 100%, ưu tiên chạy cục bộ. Không dùng dịch vụ tính credit như Canva AI.
- Không commit, không push, không ghi `DECISIONS.md` khi chưa được duyệt. Xin phép trước khi cài phần mềm.

- Phong cách mặc định: comic Nhật theo video mẫu đã duyệt, giữ Style C và nhận diện của ba nhân vật; chọn font hợp nội dung, kiểm tra dấu tiếng Việt.
- Tập theo nhạc: kiểm tra mốc từng từ, highlight/icon khi phù hợp, Mimi/đạo cụ xuyên các shot, tiếp xúc khi tương tác, cú twist và outro NMT. Key pose không mặc định là rig hoặc lip-sync.
- Xem README/workflow của revision khi tập có renderer riêng. Đổi tên engine không đổi các script/hash/media của tập đã xuất.


**Cập nhật Owner 10/11/2026 — ưu tiên quy tắc khung cũ:** hình/bối cảnh phủ ≥95% màn hình, không khung bo góc với nền trắng/kem thừa. Nhân vật/biểu cảm/hành động chính vẫn ở vùng tập trung x108–950,y200–1460; phụ đề canh giữa trong1480–1680, không đè nhân vật/watermark. Ngoại vi là bối cảnh thật, không nền mờ/kéo giãn. Xem mục cập nhật bố cục trong NMT_ENGINE.md.
