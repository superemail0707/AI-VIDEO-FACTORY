# Sổ cải tiến liên tục — nmt-engine

**Quy tắc (Owner, 08/11/2026):** pipeline phải luôn được cải tiến qua từng ngày. Mỗi lỗi Owner phát hiện, hoặc Claude tự phát hiện sau khi đã gửi duyệt, đều phải đi đủ 4 bước:

1. **Sửa** trong tập đang làm.
2. **Tìm nguyên nhân gốc**, không chỉ sửa triệu chứng.
3. **Chặn tái diễn**: ưu tiên kiểm tra tự động trong engine (chặn ghép hoặc xuất khi vi phạm). Nếu không tự động được, thêm vào checklist mục 4 của `NMT_ENGINE.md` và quy tắc trong `.claude/commands/nmt-engine.md`.
4. **Ghi vào sổ này**: ngày, lỗi, nguyên nhân, cách chặn, cách kiểm tra.

Đầu mỗi phiên làm tập mới: đọc sổ này và áp dụng hết bài học trước khi gửi Owner duyệt. Mỗi mục ghi trạng thái **Tự động** (engine chặn) hoặc **Checklist** (người kiểm).

---

## 2026-11-08 · Phụ đề đè lên nhân vật (EP08 v2) — Tự động

- **Lỗi (Owner):** "Phụ đề của video bị đè lên hình nhân vật ở một vài khung hình. Phụ đề nên đặt ở vị trí bên dưới và không đè lên hình nhân vật."
- **Nguyên nhân gốc:**
  1. Cảnh toàn khung (cận F02, F04, F05) đặt nhân vật kín tới đáy khung, nên phụ đề nằm trên thân nhân vật ở mọi bản. Đo bản gốc: F04 đè 99,8%, F05 46,6% hộp phụ đề.
  2. Khi xuất nền tảng, `platform_export.remap_sub` kéo phụ đề lên y = 1300–1440 để tránh nút giao diện của app, trong khi khung chia đôi dưới kéo tới y = 1472. Máy đẩy vào khung trên (zoom 1,07, `cam()` kẹp mép trên) làm khung dưới trượt xuống thêm khoảng 7%. Đo TikTok: F01 10%, F02 15%, F03 1%.
  3. Không có bước kiểm tra nào đo việc phụ đề chồng lên nhân vật. Lưới khung hình chỉ xem bằng mắt, và chỉ xem bản gốc.
- **Cách chặn (engine `cute_engine.py`):**
  - `check_subs()` / `--check-subs [nền tảng]`: dựng mỗi khung mẫu (6 khung một lần) hai lần, có và không có sprite (`HIDE_SPRITES`). Điểm ảnh khác nhau là nhân vật. Hộp phụ đề được ghi ở `SUB_BOX`. Tỉ lệ nhân vật trong hộp lớn hơn 0,4% thì là lỗi. Báo cáo ghi ở `render/qa_subtitles_<bản>.json`.
  - `--mux` chặn nếu bản gốc lỗi. `--export-finish` chặn nếu bất kỳ nền tảng nào lỗi.
  - `sub_y_bottom()`, `tray_top()`, `sub_tray()`: dải nền phụ đề ở đáy cho cảnh toàn khung; nhân vật đặt phía trên `tray_top()`.
  - `panel_layout()`, `panel_center()`: khi xuất nền tảng, hai khung chia đôi tự thu nhỏ sao cho khung dưới, kể cả khi đẩy máy tới `PANEL_ZOOM_MAX` = 1,08, kết thúc phía trên dải phụ đề.
- **Kiểm tra:** sau khi sửa, `--check-subs` cho bản gốc, TikTok, YouTube Shorts, Facebook Reels đều đạt: 221 khung mẫu mỗi bản, đè lớn nhất 0,0%. Đã xem lưới khung bản gốc, TikTok và Facebook Reels.
- **Bài học cho tập sau:** khi viết cảnh toàn khung, luôn dùng `E.sub_tray(im)` + `subtitle(im, tg, y=E.sub_y_bottom())` và tính vị trí nhân vật từ `E.tray_top()`. Không đặt cứng y = 1610/1700. Đẩy máy trong khung chia đôi không vượt `PANEL_ZOOM_MAX`.

## 2026-11-08 · Phụ đề không được chạm watermark NMT — Tự động

- **Yêu cầu (Owner):** "xuất video cuối đảm bảo subtitle không đè lên watermark".
- **Nguyên nhân gốc (rủi ro):** `branding.py` chỉ so watermark với vùng phụ đề **ước lượng** cố định (`SUBTITLE_ZONES`). Nếu cảnh đặt phụ đề ở chỗ khác (ví dụ dải phụ đề mới), phép so đó không thấy.
- **Cách chặn:** `check_subs(plat)` tính hộp watermark thật bằng `branding.geometry` (cùng hàm lúc chèn, kể cả `watermark.json`) và đối chiếu với hộp phụ đề thật ở mọi khung mẫu, khoảng hở `WM_PAD` = 24 px. `--export-finish` chặn khi chạm, báo cáo ghi ở `qa_subtitles_<nền tảng>.json` (`watermark_violations`).
- **Kiểm tra:** unit test 8/8 (có ca ép phụ đề xuống ngang watermark → bị chặn); ep08 v2: 3 nền tảng × 221 khung, chạm watermark 0.

## 2026-11-08 · Bố cục khung: nội dung 3/4 trên, phụ đề 1/4 dưới (tối đa 1/3) — Tự động

- **Yêu cầu (Owner):** "Bố cục hiển thị nhân vật và subtitle chưa ổn. Subtitle chỉ chiếm 1/4 khung hình, 3/4 ở trên để hiển thị nội dung. Subtitle không được che watermark. Tương tự cho các tỉ lệ video khác: kích thước có thể thay đổi tùy nội dung, nhưng phần subtitle không quá 1/3."
- **Nguyên nhân gốc:** bản trước đặt dải phụ đề theo vùng an toàn của từng nền tảng (y = 1185–1525), nên dải phụ đề của mỗi bản một khác và có lúc lấn lên vùng nội dung. Khung chia đôi ở bản gốc còn kéo xuống tới y = 1472. Không có quy tắc chung về tỉ lệ nội dung/phụ đề.
- **Cách chặn (`cute_engine.py`):**
  - `CONTENT_FRAC` = 0,75 (mặc định), `SUB_BAND_MAX` = 1/3. `tray_top()` = H × CONTENT_FRAC; `band_frac()` **chặn** khi dải phụ đề > 1/3. Tập có thể chỉnh `CONTENT_FRAC` (ví dụ 0,8) tùy nội dung.
  - `subtitle()` luôn vẽ dải nền 1/4 dưới và đặt viên phụ đề sát mép trên dải, giống nhau ở bản gốc và 3 bản nền tảng. Nếu phụ đề nhiều dòng chạm hàng watermark thì tự thu hẹp và dời sang trái.
  - `panel_layout()` áp dụng cho mọi bản: hai khung chia đôi nằm trong vùng nội dung, kể cả khi đẩy máy.
  - `check_subs()` thêm `outside_band`: hộp phụ đề phải nằm trong dải dưới. `--mux` và `--export-finish` chặn khi vi phạm.
- **Kiểm tra:** unit test 10/10 (dải 1/4, chặn dải 40%, phụ đề trong dải ở mọi bản, phát hiện và né watermark). ep08: xem kết quả `qa_subtitles_*.json`.
- **Rủi ro còn lại:** vùng giao diện của TikTok/Reels (caption, nhạc) che khoảng 300–440 px đáy màn hình; phụ đề đặt sát mép trên dải (y ≈ 1460–1660) để ít bị che nhất. Chưa đo trên app thật.
- **Tỉ lệ khác:** pipeline MVP `src/` (16:9, 4:5, 1:1, 9:16) đo ngày 08/11: dải phụ đề chiếm 19–26%, đạt quy tắc ≤ 1/3; nội dung đều nằm trên dải phụ đề. **Nhưng** ở 16:9, 4:5 và 1:1, hộp phụ đề 2–3 dòng chồng lên vị trí watermark NMT (`SUBTITLE_ZONES` ước lượng quá hẹp nên không chặn). `src/` thuộc Scope Grant riêng → đã báo Owner, chờ cho phép sửa.


## 2026-11-08 · EP10 — nhạc/chữ, diễn xuất, hôn và outro

- **Owner phát hiện:** nhân vật ít chuyển động, Mimi đứng yên; môi hai người không khớp, tim chen vùng mặt; chữ/hình đi trước nhạc; twist lộ sớm, thiếu outro; phụ đề thiếu nhấn/icon.
- **Nguyên nhân:** actor cũ chỉ bob 3 px, một sprite Mimi; ghép tâm hai sprite không có contact anchor; dùng mốc cả câu và hiện nguyên câu; reveal đặt theo local t thay vì mốc cuối lời; không có cảnh brand outro. Thử dissolve trong v03 còn tạo hai bóng người/tay, đã bỏ.
- **Sửa trong tập:** 18 key pose dùng thực (8 Mimi), chuyển động trọng tâm/máy quay; một silhouette tại mỗi frame; hình hôn đôi có tiếp xúc môi; forced alignment đúng lời + trim khoảng nghỉ đầu; word reveal/highlight/icon vector; twist sau chữ đời cuối, 1,8 s giữ phản ứng, outro 3,2 s đúng NMT.
- **Tự động tại EP10 v03:** `render/test_revision.py` 7 test; `render/verify_revision.py` decode MP4, 40 khung trước/sau 20 cue và kiểm tra vùng chữ outro; `--qa-subs` 464 khung; kiểm tra opacity phát hiện ghost. Kiểm tra theo timing đã căn, không thay thế duyệt bằng tai.
- **Checklist cho tập ca nhạc sau:** kiểm tra silence trước từ đầu (ASR không phải chuẩn tuyệt đối), đối chiếu hình/gesture với từ khóa, xem cận tiếp xúc/hai silhouette khi tương tác, không đặt tim che mặt, không dissolve hai cơ thể để giả in-between, cần key pose Mimi và brand outro khi brief yêu cầu. Chạy kiểm tra lại trên MP4 thực. Các kiểm tra mới thuộc tập, chưa tuyên bố engine chung tự chặn mọi trường hợp.
- **Bằng chứng:** `output/ep10_vi_anh_qua_dep_trai/revisions/v03/REVISION_NOTES.md`, `render/video_qa.json`, `evidence/ghost_regression.json`; chờ Owner duyệt cuối, chưa xuất.


## 2026-11-08 · EP10 — continuity Mimi/lồng

Owner phát hiện khoảng giây 08 Mimi vào lồng rồi lại ra ngoài không có hành động chuyển tiếp. Nguyên nhân: sprite Ngang b1 có sẵn Mimi trong lồng, được dùng ở hai cảnh S03/S10 trong khi cảnh liền kề dùng mèo ở ngoài. Đã thay cả hai sprite mang lồng và dùng Mimi ở ngoài; giữ lồng rỗng ở cú twist. `revisions/v04/render/check_continuity.py` kiểm tra 6 mẫu, không chọn ngang_b1 và có cat riêng; đã xem MP4 ở giây 08. Checklist: theo dõi trạng thái thú cưng/đạo cụ qua mọi shot, tìm cả các lần lặp sprite có prop gắn liền, không chỉ sửa một khung Owner chỉ ra. Ba bản NMT đã xuất theo yêu cầu Owner; chưa đăng.


## 2026-11-08 · Đổi tên chính thành NMT-engine

Owner đổi tên couple-engine → nmt-engine và yêu cầu mô tả/tài liệu liên quan. CLI chính `nmt_engine.py`, lệnh `/nmt-engine`, guide `NMT_ENGINE.md`, prompt `NMT_ENGINE_PROMPT.md`; tên cũ giữ alias/redirect. Chỉ cập nhật tên trong chú thích của renderer/branding, giữ source và hash các tập đã xuất. Smoke checks kiểm tra help/list/status, alias, scaffold tạm có tiếng Việt/brand NMT và syntax, YAML command; ba MP4 EP10 giữ nguyên SHA-256. Đây là đổi tên/tài liệu, không bổ sung rig, lip-sync, model hay quyền xuất bản.


## 2026-11-08 · Kích thước/khung hiển thị trên điện thoại (NMT-SAFE-916 v1)

- **Owner phát hiện:** TikTok và YouTube Shorts phóng to video, mất 4 góc; phần trên tràn lên vùng tab. Facebook bình thường nhưng cần thống nhất và dời nội dung xuống. Phụ đề cần dời xuống cho cân đối.
- **Đo thực:** 6 file trong `videos-post/` đều 1080×1920, SAR không đặt (1:1), H.264 High yuv420p, 60 fps → **không phải lỗi mã hoá/kích thước file**.
- **Nguyên nhân gốc:** TikTok/Shorts lấp đầy màn hình dài hơn 9:16, cắt khoảng 108 px mỗi bên (màn 20:9) và đè tab ở đỉnh, caption ở đáy. Bố cục cũ đặt nội dung từ y=0, khung bo góc/nhãn chữ sát mép, viên phụ đề EP10 rộng tới x≈1005, watermark mép phải 48 px nằm trong lề cắt. Không có rule vùng an toàn theo chiều ngang và đỉnh, chỉ có rule cho đáy/phụ đề.
- **Sửa:** thêm `safe_frame.py` (hằng số khung chung, `check_box`, CLI `preview` vẽ vùng cắt/giao diện/an toàn lên khung MP4); rule mục 3.2 `NMT_ENGINE.md`; manifest ghi `safe_frame`. Ảnh đo trước khi sửa: `docs/requirements/evidence/safe_frame_ep10_ep08_before.png`.
- **Áp vào engine (Owner chọn "Áp vào engine + EP10"):** `cute_engine.SAFE916` + `safe_post()` trong `frame()`; `check_subs` có `safe_frame_violations` và `require_subs_ok` chặn; watermark `margin_x ≥ 120` ở `wm_box` và `platform_export`. Test `tests/unit/test_subtitle_layout.py` 15/15 (5 test mới; test cũ chạy với `SAFE916=False`). Test mới bắt được lỗi thật: `sub_pill(maxw)` là bề rộng chữ, viên phụ đề rộng thêm 92 px → tràn lề cắt; đã trừ lề.
- **EP10 v05:** renderer `revisions/v05/render/ep10_v05.py` dùng lại cảnh v04, reframe từng khung; outro dùng nền màu trơn (nền mờ hiện bóng chữ tiêu đề).
- **Chưa làm:** watermark mặc định trong `src/` (cần Scope Grant; hiện ghi đè ở engine); EP08 chưa dựng lại; số vùng giao diện là ước lượng, chưa đo trên app thật.


## 2026-11-08 · EP10 v05 → v06: không làm mờ xung quanh, Mimi nằm yên, icon trong phụ đề, ghế ngồi

- **Owner góp ý về v05:**
  - Không được làm mờ phần xung quanh tranh.
  - Mimi nhảy tới lui rời rạc.
  - Còn chữ "Bình Quới".
  - Icon nằm rời dưới phụ đề; sóng nhạc nằm ở dải dưới.
  - Ở cảnh ghế, Tí ngồi cao hơn Ngang.
- **Rule mới (đã ghi vào NMT_ENGINE mục 3.2):**
  - Tranh là khung bo góc trong x 108–972, y 200–1460, xung quanh màu trơn; cấm làm mờ hoặc kéo giãn tranh ra ngoài.
  - Icon diễn đạt nằm trong viên phụ đề.
  - Hiệu ứng "đang phát nhạc" đặt trên tranh.
  - `safe_frame.reframe` đã bỏ nền mờ; test engine 15/15.
- **Checklist diễn xuất:**
  - Thú cưng không đổi vị trí hay động tác liên tục giữa các cảnh nếu kịch bản không cần; khi brief là "không quan tâm" thì giữ một tư thế nghỉ, chỉ thở nhẹ.
  - Hai nhân vật ngồi cùng một ghế phải cùng mặt ghế (đối chiếu đùi/hông, không chỉ chân).
  - Bỏ nhãn địa danh không cần thiết.
- **Công cụ:** `safe_frame.py preview` giờ báo lỗi rõ khi mốc giây vượt thời lượng video.


## 2026-11-08 · Viền phụ đề phải canh giữa màn hình

- **Owner phát hiện ở EP10 v06 đã xuất:** khung viền phụ đề lệch, không nằm giữa màn hình. Owner không yêu cầu sửa video đã xuất; chỉ sửa cho các video tiếp theo.
- **Nguyên nhân:** `safe_frame.SUB_X_CENTER` = 510. Giá trị này lệch trái 30 px để né cột nút bên phải của app, nhưng nút nằm ở x > 950, nên viên phụ đề rộng 800 px canh giữa (x 140–940) vẫn không chạm nút. Ngoài ra, trước đây engine dời phụ đề sang trái khi phụ đề chạm watermark.
- **Sửa:**
  - Đặt `SUB_X_CENTER` = 540.
  - `check_box(..., "subtitle")` báo lỗi khi tâm viền lệch quá 2 px; `check_subs`, `--mux` và `--export-finish` chặn.
  - `safe_post` không dời phụ đề sang ngang nữa; khi chạm watermark thì thu hẹp đều hai bên, giữ tâm.
  - Thêm 2 test: tâm viền ở mọi độ dài câu, mọi nền tảng, cả lúc trượt vào; và `check_box` bắt được tâm 510. Tổng 17/17 test đạt.
- **Ghi chú:** bản EP10 v06 đã xuất vẫn giữ tâm 510 theo yêu cầu Owner. Renderer v06 đọc `SF.SUB_X_CENTER`, nên nếu chạy lại sẽ ra tâm 540, không trùng với file đã giao. Bằng chứng của bản đã giao là `render/video_qa.json` và SHA trong manifest.


## 2026-11-09 · Nút duyệt trong chat

- Owner yêu cầu thêm nút **Duyệt** / **Cần chỉnh** khi hỏi duyệt. Đã ghi vào NMT_ENGINE mục 2, dùng công cụ hỏi có lựa chọn của ứng dụng.
- EP11: Owner đã duyệt kịch bản với F01 và F03 không thoại; workflow hiện là `script_approved`. Lượt duyệt này không cần hỏi lại.


## 2026-11-10 · Hiển thị đầy đủ kịch bản trước khi duyệt — Checklist

- Owner yêu cầu kịch bản rõ ràng ngay trong chat để xem và duyệt trực tiếp.
- Nguyên nhân: lời kết chỉ thông báo chờ duyệt có thể làm nội dung trước đó bị thu gọn, khiến việc xem xét không thuận tiện.
- Cách chặn: command, guide và prompt yêu cầu trình bày đủ từng cảnh, biểu cảm, thoại, âm thanh và outro trước nút Duyệt / Cần chỉnh; không chỉ gửi file hoặc thông báo sẵn sàng. Góp ý quy trình không phải phê duyệt.
- Kiểm tra: đọc lại ba tài liệu; EP13 vẫn chờ duyệt kịch bản. Quy tắc giao tiếp được kiểm thủ công, chưa có kiểm tra tự động UI chat.


## 2026-11-10 · EP13: độ cao bàn, ly vỡ và tranh phủ màn hình — Checklist

- Owner: bàn phải cao hơn để cú rơi nguy hiểm và ly chắc chắn vỡ; tranh phủ95% màn hình, nhân vật/hành động giữ trong vùng tập trung, bỏ viền trắng.
- Nguyên nhân: chọn bàn trà thấp; đạo cụ còn nguyên sau cú rơi; renderer contain tranh rồi safe_post thu thêm một lần vào khung bo góc.
- Sửa EP13: tranh bàn cao, cảnh chạm sàn vỡ và mảnh vỡ liên tục; Ngang cầm chổi/hót rác. Tranh9:16 phủ toàn màn hình, hậu kỳ của tập giữ nguyên nền và chỉ đặt phụ đề an toàn. Giữ bản cũ trong art/v01,v02.
- Chặn tái diễn: mục bố cục ưu tiên mới trong NMT_ENGINE; kiểm thủ công độ cao tương đối, mép bàn/đường rơi, trạng thái ly trước/sau và vùng tập trung; kiểm độ phủ hình trong tập. Không tuyên bố tự động đo ngữ nghĩa ảnh hoặc đã sửa engine chung.


## 2026-11-10 · EP13: chuyển vào outro không lồng hai Mimi — Checklist

- Tự phát hiện trước khi gửi video: iris giữa hai bố cục khiến Mimi cũ và Mimi outro cùng hiện trong một số khung.
- Nguyên nhân: transition mặc định iris0,55s từ template.
- Sửa: cắt thẳng vào outro; render lại F07 và mux. Giữ bản MP4/QA trước sửa trong render để đối chiếu.
- Chặn trong tập: xác minh mọi scene dùng cut; xem MP4 ở21,8s và lưới khung. Chưa thêm chặn chung cho mọi kiểu transition vì một số ngữ cảnh có thể cần iris.


## 2026-11-11 · EP15: nhạc tổng hợp numpy "chưa hay" — Checklist

- Owner nghe bản v1 (piano + suối/gió/chim tổng hợp numpy) và yêu cầu dùng nhạc lofi/tiếng suối/piano miễn phí trên mạng.
- Nguyên nhân: nhạc tổng hợp từng nốt bằng sin + reverb nhiễu nghe đơn điệu, nhân tạo; tiếng suối từ nhiễu lọc không thật. Claude không nghe được âm thanh, chỉ đo âm lượng, nên không tự phát hiện được.
- Sửa EP15: tải (Owner cho phép từng file) hai bản **CC0** từ Freesound: nhạc "Chill Lofi piano music" (ZHRØ, #688675) và tiếng suối "RIVER gurgling in forest" (nicoproson, #642775), bản preview MP3 128 kbps công khai. SHA-256 khoá trong `ep15_audio.py`, nguồn ghi ở `audio/CREDITS.md`, `audio_events.json`. Giữ bản v1 tại `audio/master_v1_synth.wav`.
- Chặn tái diễn (checklist): với video thư giãn/nhạc nền dài, mặc định đề xuất nguồn nhạc thật có giấy phép CC0 (Freesound lọc CC0) hoặc Owner cung cấp; nhạc tổng hợp numpy chỉ dùng cho SFX/nhạc ngắn. Luôn gửi Owner file nghe thử trước khi render dài. Pixabay chặn trình duyệt tự động (Cloudflare 429) — không vượt qua; nếu cần Pixabay thì Owner tự xác minh. Bản gốc WAV trên Freesound cần đăng nhập — không đăng nhập thay Owner.


## 2026-11-11 · EP16: tranh image_gen không tuân vùng an toàn; `--tts` trỏ sai model — Checklist

- **Tự phát hiện trước khi Owner duyệt hình:** tranh F05 (Owner tạo bằng image_gen theo prompt có ràng buộc y 12–74 %) vẫn vẽ nhân vật xuống ≈82 % và đầu Tí ở ≈3 %; phụ đề 1480–1680 đè thân Ngang/Mimi. F02 Mimi chạm mép phụ đề. Ô so sánh F03 rộng 980 px tràn lề cắt x<108/x>972.
- **Nguyên nhân:** image_gen không đảm bảo tuân tỉ lệ bố cục trong prompt; tranh full-bleed 9:16 không thể thu/dời mà vẫn phủ ≥95 %. Ô F03 đặt theo bề rộng khung, không theo vùng an toàn.
- **Sửa:** F02 khung neo đáy z 1,05; F03 ô 830 px tâm x 529; F05 Owner chọn "Cần chỉnh", prompt F05 v02 nêu rõ đáy nhân vật ≤ 70 %, đỉnh đầu ≥ 16 %, đáy 30 % chỉ là nệm.
- **Chặn tái diễn (checklist):** ngay khi nhận tranh, vẽ overlay vùng an toàn (y 200/240/1460/1480/1680, x 108/972) lên từng tranh ở khổ 1080×1920 và kiểm trước khi viết cảnh; cảnh zoom cận chỉ đặt lúc không có phụ đề hoặc khi vùng phụ đề rơi vào gối/nệm. Prompt image_gen ghi tỉ lệ cụ thể (đáy nhân vật ≤ 70 %).
- **TTS:** `tts_vieneu.py` của engine trỏ `~/mnt/AI-VIDEO-FACTORY/...` (đường dẫn máy ảo cũ) và Python hệ thống không có gói `vieneu`. EP16 dùng runner riêng của tập (`render/tts_local.py`, như EP13) với `workspace/venv-vieneu/bin/python`. Engine chung chưa sửa.


## 2026-11-12 · EP17: kiểm vùng an toàn tranh bằng mắt trên ảnh nhỏ bỏ sót lỗi — Checklist

- **Tự phát hiện (sau khi đã báo Owner F01 đạt):** F01 v01 có giày Tí ở y ≈ 1480–1580, nằm trong dải phụ đề. Lần kiểm đầu dùng ảnh ghép 360×640 mỗi tranh, vạch 1460/1480 sát nhau, nên đọc nhầm là đạt. Ngoài ra F07 v01 Owner nhận về là biến thể của F06 (image_gen lặp cảnh trước trong cùng cuộc trò chuyện).
- **Sửa:** F02/F04/F07 v02 tạo lại với cụm "UPPER TWO-THIRDS … LARGE EMPTY foreground" — đạt (đáy nhân vật ≈ y1150). F01 v02 đang chờ Owner tạo. F07 v01 dùng làm nhịp nhấn F06b.
- **Chặn tái diễn (checklist):** kiểm từng tranh ở ≥ 540×960 có lưới toạ độ mỗi 100 px; ghi đáy nhân vật (y) và vị trí mặt của từng tranh vào docstring cảnh trước khi báo đạt. Khi một tranh mới trông gần giống tranh trước, so sai khác điểm ảnh (mean diff) để phát hiện trùng. Prompt image_gen dùng "upper two-thirds / large empty foreground" thay vì chỉ ghi phần trăm.


## 2026-11-12 · EP19: thoại/chữ thừa, hình đi trước tiếng — Checklist

- **Owner góp ý video v1:** (1) cảnh "Ngang quyết tâm bắt chước" và "Đến lượt Tí" không cần lời dẫn và phụ đề, vì hình đã tự kể; (2) bỏ chữ/lời "Cú twist"; (3) đoạn đầu hình hiện trước tiếng; (4) thêm đoạn kết Mimi ngủ ngon lành trong tư thế yoga.
- **Nguyên nhân:** (1)(2) khi kéo kịch bản lên ≥ 60 s, Claude đọc nguyên chú thích khung comic thành lời dẫn cho mọi nhịp, kể cả nhãn kỹ thuật "Cú twist"; (3) engine mặc định câu đầu mỗi cảnh ở 0,35 s và file VieNeu có ~0,1 s im lặng đầu, nên khung đầu hiện ~0,45 s trước tiếng; cảnh cắt hình F01 đặt sớm hơn câu 0,15 s.
- **Sửa EP19:** bỏ V4, V5; V6 còn "Đại sư không tập."; F01 câu đầu ở 0,05 s (`FIRST_LEAD`), cắt hình theo `vt(...)[0] + ONSET` (0,09 s); thêm đoạn kết A02 có thở, má hồng, vương miện, bong bóng ngủ/nước dãi. Tổng 63,5 s.
- **Chặn tái diễn (checklist):** chỉ dùng lời dẫn ở hook và chốt; nhịp hành động mà hình đã rõ thì để không lời. Không đọc nhãn cấu trúc (twist, hook, cảnh 1…) thành thoại/phụ đề. Câu mở của video bắt đầu ≤ 0,1 s; mọi cú cắt hình gắn với một câu thoại thì đặt ở thời điểm tiếng thật bắt đầu (đầu câu + onset đo được), không sớm hơn. Engine chung chưa sửa (độ lệch 0,35 s vẫn mặc định cho các cảnh sau).
