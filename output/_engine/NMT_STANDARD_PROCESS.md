# Quy trình chuẩn NMT v2 — một format, một nhận diện

Trạng thái: **bản nháp, chờ Owner duyệt** (Claude lập 18/11/2026 theo yêu cầu Owner cùng ngày).
Phạm vi: mọi tập mới từ EP26. Tập cũ giữ nguyên. Khi được duyệt, tài liệu này là **checklist sản xuất**; `NMT_ENGINE.md` vẫn là nguồn sự thật về lệnh và cổng, `BRAND_NMT.md` về nhận diện.

---

## 0. Thống kê 11 tập gần nhất (EP15–EP25)

| Tập | Thời lượng | Câu thoại | Chấm kịch bản (các lần) | Review video tốt nhất | Outro | Nhạc nền |
|---|---|---|---|---|---|---|
| EP15 | 90,0 s | 0 | – | – | – | Freesound CC0 (lofi + suối) |
| EP16 | 27,6 s | 7 | – | – | – | – |
| EP17 | 40,6 s | 9 | – | – | – | – |
| EP18 | 45,0 s | 0 | – | – | – | – |
| EP19 | 63,5 s | 5 | – | – | – | Tokyo / Blue Sky |
| EP20 | 81,4 s | 29 | 7,5 · 7,5 · 7,5 → Owner | – | – | Tokyo / Blue Sky (lặp) |
| EP21 | 71,5 s | 6 | 7,5 · 8,0 | – | tai mèo | Pizzicato (CC0) |
| EP22 | 70,7 s | 13 | 7,0 · 8,0 | – | tai mèo | Joy Park (CC0) |
| EP23 | 71,4 s | 6 | 7,5 · 7,5 · 8,0 | 8,5 | subscribe 7,8 s | Quirky cinematic |
| EP24 | 71,3 s | 4 | 7,5 · 8,5 | 8,5 | subscribe 7,8 s | Cute Happy BG |
| EP25 | 31,1 s | 8 | Owner duyệt trực tiếp | 9,0 | subscribe 7,8 s | tổng hợp numpy |

Công cụ tranh: 100 % image_gen (Codex `--art-auto` hoặc ChatGPT web qua Playwright). Giọng: VieNeu cục bộ (Tí = Hải Đăng, Ngang = Trúc Ly). Font: Be Vietnam Pro (Bold/ExtraBold).

**Điều đang chạy tốt** (giữ): cổng duyệt khoá SHA; `--check-art/--check-subs/--check-sync/--check-transitions`; nhạc không lặp (`music_reuse`); outro `subscribe_outro` 7,8 s; review video độc lập; sổ lỗi chấm kịch bản.

**Điểm lệch format giữa các tập** (lý do cần chuẩn hoá):
1. **Thời lượng nhảy 28–90 s.** BRAND ghi 65–75 s, D-030 ghi "theo topic", EP25 chỉ 31 s.
2. **Kiểu phụ đề 3 loại:** viên trắng viền hồng chữ đen (`cute_engine.sub_pill`, EP16–EP24); chữ trắng viền đen + từ khoá vàng nền đen, hiện theo từng từ (EP25, code riêng của tập `ep25_scenes.py`). Chưa có hàm dùng chung.
3. **Thumbnail không có khuôn:** EP25 có `make_cover.py` riêng (khung đen chữ trắng/vàng); các tập khác lấy khung hình bất kỳ qua `THUMB`.
4. **Kịch bản hiếm khi qua chuẩn lần đầu:** 12 lần chấm, chưa lần nào ≥ 9,0. Mất điểm nhiều nhất: `visual_comedy` −6, `twist` −6, `producible` −6, `escalation` −5,5, `character_brief` −4 (`script_review.py findings`).
5. **Review video mất điểm lặp lại:** một key pose đứng > 5 s, khoảng lặng dài, zoom "Mimi phán xét" cắt nhân vật, đạo cụ không liền mạch (mũ, vết bẩn), tranh lề `art_fit` lộ khi lia máy.
6. **Âm lượng outro** chưa có quy tắc: SFX outro giữ nguyên mức, không hạ nhạc.
7. **Mâu thuẫn tài liệu (đã chốt: semi-chibi như EP25):** Agent V2.0 ghi Tí "đầu 2,5–3 lần" (chibi), trong khi `TI_MASTER_REFERENCE.png` vẽ ≈ 7,5 đầu; tranh EP23–EP25 thực tế là semi-chibi đầu to. Cần Owner chốt một tỷ lệ (đề xuất: theo tranh đã duyệt EP25, đầu ≈ 1/5 thân).

---

## 1. Format cố định của một tập NMT

| Mốc | Nội dung | Thời lượng |
|---|---|---|
| Hook | Kết quả/phản ứng mạnh nhất trước, kèm một câu hỏi gợi tò mò. **Không chữ tiêu đề đầu video** (Owner 18/11) | 0–3 s |
| Setup | Bối cảnh đời thường + **gieo chi tiết cho twist** (nhìn thấy được khi tắt tiếng) | 3–12 s |
| E1 → E2 → E3 | Ba bước leo thang **khác loại**, mỗi bước thêm hành động/thông tin mới | 12–35 s |
| Lặng | 0,6–1,0 s im (chỉ nhạc rất nhỏ) trước twist | — |
| Twist | Lật bằng hình, ít chữ; được phép 1 khung nguệch ngoạc ≤ 2 s | 35–45 s |
| Last laugh | Hậu quả cuối hoặc callback chi tiết đã gieo | 45–52 s |
| Mimi phán xét | Zoom giật, nửa mí, "tách" + meo trầm | ~1,2 s |
| Ảnh kết + Outro | Tranh kết riêng (ấm, đóng câu chuyện) làm nền cho `subscribe_outro` 7,8 s | 7,8 s |

- **Tổng ≥ 60 s** (gồm outro 7,8 s; Owner 18/11), tối đa ~75 s. Không thêm cảnh lặp để đủ giờ: kéo dài bằng tình tiết mới, không bằng giữ hình.
- **Mỗi key pose ≤ 4,5 s**; dài hơn thì tách 2 tranh hoặc đổi góc máy.
- **Thoại vừa đủ để dễ hiểu** (thường 6–10 câu), mỗi câu ≤ 45 ký tự, tiếng Việt đời thường. Không lời dẫn kể chuyện.
- Không bắt buộc đủ 3 nhân vật. Mimi không bao giờ nói.

---

## 2. Nghiên cứu kịch bản từ brief

1. **Đọc brief nguyên văn**, tách: yêu cầu bắt buộc (nhân vật, kết, độ dài) và phần tự do.
2. **Nghiên cứu topic** (Agent V2.0 mục XVI): sự thật nền (ngày, nguồn gốc), cách người Việt nói về topic, meme đang có, nỗi niềm chung. Ghi nguồn/giả định vào `META["research"]`. Không dùng từ học thuật.
3. **8 câu hỏi phân tích topic** (Agent V2.0 bước 1), tìm "insight đời thường": câu mà người xem nghĩ "y chang nhà mình".
4. **3 concept khác cơ chế** A Relatable / B Absurd meme / C Cinematic parody, chấm thang 100 → chọn điểm cao nhất (gần điểm: twist hình mạnh, ít thoại). Hiện bảng trong chat.
5. **Đọc sổ lỗi** `python3 output/_engine/script_review.py findings` và mục mới nhất của `IMPROVEMENT_LOG.md` trước khi viết.

---

## 3. Viết storyboard và cổng chấm 9/10

### 3.1 Viết
- Mỗi cảnh trong `notes`: mục đích · hình · biểu cảm cụ thể (mắt, miệng, tóc, mồ hôi) · hành động · góc máy + chuyển máy · SFX · nhạc · continuity (trang phục, đạo cụ, vết bẩn mang sang cảnh sau).
- Mỗi cảnh **một khoảnh khắc**; hai hành động thì tách cảnh.
- Ngang có ít nhất một nhịp drama phóng đại; Mimi gây ra hoặc chứng kiến hỗn loạn mà vẫn tỉnh bơ.
- **Không ép câu cửa miệng "Chuyện nhỏ!"** (Owner 18/11: nhàm). Chỉ dùng khi thật sự hợp tình huống, không quá 1 lần/3 tập.

### 3.2 Hai vòng chấm — **chỉ qua khi ≥ 9,0/10 và qua hội đồng người xem**
1. **Tự soát** 15 câu QC Agent V2.0 (Claude).
2. **Giám khảo rubric** độc lập (Codex, hoặc subagent Claude mới không có lịch sử): `--script-review`. Ngưỡng **≥ 9,0/10** (thay mức 8,0 cũ).
3. **Hội đồng người xem** (subagent mới, đóng vai 3 người xem: dân văn phòng 25 tuổi lướt TikTok, cặp đôi đang yêu, người không biết kênh). Trả lời có/không + lý do cho 8 câu:
   1. Hiểu topic trong 3 giây đầu không?
   2. Có muốn xem tiếp sau giây thứ 3 không?
   3. Tắt tiếng vẫn hiểu câu chuyện không?
   4. Có cười thành tiếng ít nhất một lần không? Ở giây nào?
   5. Twist có bất ngờ mà vẫn "à, hợp lý" không?
   6. Xem xong được gì (đồng cảm, mẹo, cảm xúc)?
   7. Có muốn tag/gửi cho ai không?
   8. Có cảnh nào chán, thừa, khó hiểu không?
   **Đạt khi câu 1, 3, 5 "có" ở cả 3 vai và tổng ≥ 20/24.**
4. Chưa đạt → sửa đúng góp ý, chấm lại bản mới; tối đa 3 vòng, sau đó trình Owner bản điểm cao nhất kèm toàn bộ góp ý.
5. **Bài học EP26:** chỉ sửa theo góp ý lặp lại ở ≥ 2 giám khảo; không tăng số cảnh khi sửa. Ngưỡng 9,0 cần giám khảo đã hiệu chỉnh — trước khi hiệu chỉnh, điểm subagent chỉ là tham khảo và Owner quyết.
6. Qua cả hai vòng → vẫn **trình đủ kịch bản trong chat** với nút Duyệt / Cần chỉnh (Owner có quyền chặn).

---

## 4. Hình ảnh theo nhân vật master

**Nguồn danh tính:** `character_library/{ti,ngang,mimi}/*_MASTER_REFERENCE.png` đính kèm mọi lô tạo tranh. Master luôn thắng mô tả chữ.

| Mục | Tí | Ngang | Mimi |
|---|---|---|---|
| Nhận diện khoá | Tóc đen bồng vuốt lệch, mắt đen to | Tóc nâu đậm dài xoăn gợn, mặt tròn | Mướp nâu xám, 3 sọc trán, mắt xanh lá, mõm/ngực kem, chân trắng |
| Trang phục mặc định | Áo thun navy, quần jean xanh, giày kem | Áo/váy nâu đất – terracotta, giày sáng | — |
| Biểu cảm thương hiệu | Tự đắc lấp lánh → mắt chấm trắng, hàm rớt, tóc dựng, thác mồ hôi | Ôm ngực ngã ngửa, má phồng, gân giận, tóc bùng | Nửa mí phán xét, tỉnh bơ |
| Cử chỉ | Ưỡn ngực, chống nạnh, giơ ngón cái tự tin | Tay ôm má, chỉ tay drama, khoanh tay | Đẩy đồ rơi, ngồi trên chỗ cao, liếm chân |

- **Phong cách và tỷ lệ (Owner chốt 18/11):** semi-chibi đầu to như tranh đã duyệt EP25 (không theo tỷ lệ 7,5 đầu của sheet master; master chỉ khoá nhận diện mặt, tóc, màu). Comic Nhật (nét bao rõ, màu phẳng + cel shading nhẹ, nền nội thất ấm pastel). Khung nguệch ngoạc (doodle) chỉ ở cú đấm hài, ≤ 2 s.
- **Prompt ảnh 10 phần** (tiếng Anh, Agent V2.0 mục X) trong `art/PROMPTS_v01.md`; mỗi prompt có khối `COMPOSITION (STRICT)`: mọi mặt trong 70 % giữa bề ngang, đầu dưới 12 % trên, 1/3 dưới là nền trống (sàn/thảm), **không chữ trong tranh** (chữ do engine vẽ).
- **Continuity:** bảng đạo cụ/trang phục theo cảnh ghi trong `notes`, chép vào prompt từng cảnh.
- **Công cụ:** `--art-auto` (Codex image_gen) → hết lượt thì `chatgpt_art.py` qua Playwright. Không dịch vụ tính credit.
- **Review tranh:** `--check-art` + overlay 540×960 + `safe_annotations.json` (đáy nhân vật, đỉnh đầu, `face_x`); so master từng tranh: đúng tóc/màu áo/mắt, đủ ngón, Mimi đúng sọc. Lệch → `--fix` 1 lần, còn lệch → `art_fit.py` (s ≥ 0,82). **Tranh 2:3 (1024×1536)**: dùng `art_fit.fit_wide` (giữ nguyên bề ngang, đáy phản chiếu sàn mờ) thay cho cắt rồi thu nhỏ — tránh vệt kéo giãn hai bên (bài học EP26).

---

## 5. Chữ tiếng Việt trên video

- **Font:** Be Vietnam Pro (OFL) — Bold cho phụ đề, ExtraBold cho chữ đóng dấu/thumbnail. Kiểm dấu đủ (ă â ê ô ơ ư đ + 5 thanh).
- **Phụ đề (Owner 19/11/2026: kiểu D + font kiểu A — chuẩn chung từ EP29):** chữ **trắng** Be Vietnam Pro **Bold 50 px, không viền chữ** (font của kiểu A EP23–24), trên **thẻ nền đen** bo góc co theo chữ (độ mờ ~85 %); **chỉ 1 dòng, mỗi lúc tối đa 4 chữ** (Owner 19/11 tối): câu chia cụm 3–4 chữ (`K.word_chunks`), cụm hiện khi giọng tới chữ đầu cụm rồi được cụm sau thay; chỗ ngắt theo **khoảng ngừng của giọng** (`K.voice_gaps`, dời chỗ ngừng lệch về dấu câu) + dấu câu, không tách tên riêng, không kết cụm bằng hư từ (cây/của/vì…); câu máy ngắt cụt nghĩa thì chỉnh tay `K.SUB_BREAKS = {'V12': 'Em xoá | vì thanh toán hết | rồi đó anh!'}`. **Bắt buộc** in `K.sub_chunk_report(<tập>)` và soát từng câu sau `--tts` (đọc lên phải trôi, không cụt nghĩa). Từ đang đọc nhấp 2 px; từ khoá vàng #FFD45C to 1,2× trên ô đen; rộng ≤ 710 px; tâm x = 540, dải 1480–1680. Hằng số `scene_kit.WORD_SUB_SIZE/WORD_FONT_WEIGHT/WORD_STROKE`. Ảnh so sánh kiểu A–D: `docs/marketing/subtitle_styles/`.
- **Từ khoá:** 1–2 từ mỗi câu, **chữ vàng #FFD45C** trên ô nền đen đậm; khai báo `KEYWORDS = {"V03": {"nhìn", "kỹ"}}`.
- **Chạy theo giọng:** từ hiện dần theo mốc âm tiết (`core.wordtime.estimate`, khoá SHA của file giọng); từ đang đọc nhấp lên 2 px; viên nảy nhẹ theo biên độ giọng.
- **Chữ đóng dấu trên hình** (RẦM!, XOẢNG!, ??) thay phụ đề cho âm thanh; không ghi tên nhân vật; không đọc nhãn cấu trúc.
- *Việc cần làm sau khi duyệt:* chuyển `caption_card/word_state` của EP25 thành hàm chung `scene_kit.word_captions()` + `build_word_timing` vào engine (để mọi tập cùng một kiểu).

---

## 6. Thumbnail

**Chuẩn hiện hành (Owner 18/11/2026): [`prompts/thumbnail_designer_v1.md`](prompts/thumbnail_designer_v1.md)** — một ý tưởng trung tâm, tối đa 2 nhân vật đối lập cảm xúc, câu móc 4–8 từ, từ khoá màu nhấn ×1,2–1,4, display sans siêu đậm, viền tối + bóng cứng, vùng an toàn 80 % × 70 %, kiểm tra bản 1/6 và bản che mép. Tranh do image gen vẽ (không chữ), chữ dựng bằng `scene_kit.make_thumbnail_v2`. Các dòng dưới là bản cũ, theo file trên khi khác nhau.


- Khung 1080×1920 lấy từ **tranh thật của tập** (khoảnh khắc phản ứng mạnh nhất, trước twist).
- **Nhân vật:** mặt lớn chiếm ≥ 35 % khung, biểu cảm cực đại (mắt chấm trắng/má phồng/hàm rớt), nhìn về phía chữ hoặc ống kính.
- **Chữ:** 2 dòng, 2–5 từ mỗi dòng, ExtraBold 100–120 px, dòng 1 trắng, dòng 2 vàng, viền đen 7 px, trên khối đen bo góc đặt ở vùng **không có mặt** (1/3 trên hoặc 1/3 dưới, `block_y`); **không bao giờ che mặt** (bài học EP26: khối ở trên che mặt Mimi → dời xuống chân).
- **Câu chữ:** tạo khoảng trống tò mò (câu hỏi, "?!", con số), **không lộ twist**.
- Có `cover.jpg` cho 3 nền tảng. *Việc cần làm:* hàm chung `scene_kit.make_thumbnail(art, line1, line2, focus)` thay `make_cover.py` của từng tập.

---

## 7. Giọng, nhịp, góc quay, âm thanh

- **Giọng:** VieNeu cục bộ; Tí Hải Đăng, Ngang Trúc Ly. Câu đầu tiếng thật ≤ 0,20 s (`--check-sync`). Câu ngắn, có ngắt "…" để tạo nhịp.
- **Nhịp:** cắt mỗi 1,5–3 s (đổi góc/zoom trong cùng tranh tính là một nhịp); không khoảng lặng > 1,7 s trừ nhịp lặng trước twist; không cảnh đứng hình > 4,5 s.
- **Góc máy:** mỗi tập dùng ít nhất 4 loại: toàn, trung, cận mặt, chèn đạo cụ, góc thấp "anh hùng", zoom giật, rung khi va chạm. Zoom phán xét lấy tâm từ overlay tranh sau `art_fit`, chừa x 160–960.
- **SFX:** theo nhóm Agent V2.0 mục XII (boing, whoosh, record scratch, boom, sweat drop, tiny meow, im lặng đột ngột); không quá 1 SFX/1,5 s.
- **Nhạc nền (Owner 19/11/2026):** ưu tiên dùng lại bản CC0 có sẵn trong kho nếu hợp tập (`qa_checks.music_library`); chỉ tìm/tải bản mới khi không có bản phù hợp (Owner cho tải từng file); nhạc dưới thoại ≈ −24 dB so với giọng; `--mux` chỉ báo nhạc dùng lại, không chặn.
- **Loudness:** bản gốc −16 đến −14 LUFS, đỉnh ≤ −1,5 dBTP; bản xuất loudnorm −14 LUFS.

---

## 8. Ảnh kết và Outro

- **Ảnh kết riêng** (`A_closing`): khoảnh khắc ấm/đóng câu chuyện, bố cục chừa 1/3 dưới trống cho thanh đăng ký. Giữ 1,0–1,5 s trước khi outro bắt đầu (cùng tranh, cắt thẳng).
- **Outro:** `K.subscribe_outro(t, art('<ảnh kết>'))` + `K.subscribe_sfx(sid)` 7,8 s, cut vào, không phụ đề, không tai mèo.
- **Giảm âm outro (mới):** SFX outro nhân **0,5**; nhạc nền trong outro hạ còn **35 %** mức thân video và fade-out 1,5 s cuối. Đo: LUFS đoạn outro thấp hơn thân video ≥ 6 LU. *Việc cần làm:* thêm tham số `gain` cho `subscribe_sfx` và `outro_duck` cho dựng âm thanh.
- Kiểm trên MP4: thanh xuất hiện, bấm đủ 3 nút, thu lại, avatar biến mất.

---

## 9. Thứ tự cổng (không đổi so với NMT_ENGINE)

1. Kịch bản: ≥ 9,0 + hội đồng người xem → trình chat → Owner.
2. Tranh + giọng + storyboard → Owner duyệt hình.
3. Render → `--mux` → review video độc lập ≥ 8/10 không lỗi chặn → Owner duyệt video cuối.
4. Xuất 3 nền tảng + thumbnail → `videos-post/unpost/`. Không tự đăng.

## Chi phí token (Owner 19/11/2026)

- Giám khảo rubric kịch bản: subagent model mặc định (Opus). Hội đồng người xem và review video: subagent **model `sonnet`**.
- Khâu tranh: dòng `CAST:` + luật `STRICT` trong `chatgpt_art.py`; đo vị trí bằng `art_measure.py` (một tấm QA ¼ độ phân giải).
- Mỗi tập một phiên mới, `/compact` sau khi duyệt kịch bản và sau bảng hình. Đo lại bằng `python3 output/_engine/token_report.py` (báo cáo `docs/operations/TOKEN_COST_REPORT_2026-11-19.md`).
