# Sổ cải tiến liên tục — nmt-engine

**Quy tắc (Owner, 08/11/2026):** pipeline phải luôn được cải tiến qua từng ngày. Mỗi lỗi Owner phát hiện, hoặc Claude tự phát hiện sau khi đã gửi duyệt, đều phải đi đủ 4 bước:

1. **Sửa** trong tập đang làm.
2. **Tìm nguyên nhân gốc**, không chỉ sửa triệu chứng.
3. **Chặn tái diễn**: ưu tiên kiểm tra tự động trong engine (chặn ghép hoặc xuất khi vi phạm). Nếu không tự động được, thêm vào checklist mục 4 của `NMT_ENGINE.md` và quy tắc trong `.claude/commands/nmt-engine.md`.
4. **Ghi vào sổ này**: ngày, lỗi, nguyên nhân, cách chặn, cách kiểm tra.

Đầu mỗi phiên làm tập mới: đọc sổ này và áp dụng hết bài học trước khi gửi Owner duyệt. Mỗi mục ghi trạng thái **Tự động** (engine chặn) hoặc **Checklist** (người kiểm).

---

## 2026-11-20 · EP32 Owner: "âm thanh gây khó chịu là do outro" — bỏ tiếng outro lúc xuất hiện/biến mất — Tự động

- **Owner (duyệt video cuối EP32 v01):** loại bỏ âm thanh outro lúc xuất hiện và biến mất; giữ âm thanh click vào 3 nút; hình xuất hiện, click, biến mất giữ nguyên.
- **Nguyên nhân:** `scene_kit.subscribe_sfx` phát 13 tiếng trong 7,8 s, gồm pop + vút khói + phụt khi bật và vút thu + vút biến + pop khi tắt — dồn sát nhau ngay sau câu kết, nghe như tạp âm (cùng loại lỗi "nhiều tạp âm" EP31).
- **Chặn (Tự động):** `subscribe_sfx` mặc định chỉ trả tiếng ở 3 nút (tách + ting/tim, tách + ding, tách + chuông); `OUTRO_APPEAR_VANISH_SFX = False`; `appear_vanish=True` chỉ để tái lập tập cũ. Test `test_no_appear_vanish_sfx_by_default`. Mọi tập dùng `K.subscribe_sfx` nhận thay đổi khi dựng lại âm thanh; video đã xuất không đổi.
- **Kiểm EP32:** đo trên MP4 — đoạn outro xuất hiện đỉnh −27,7 dB, thu/biến mất −35,0 dB (chỉ nhạc nền đang tắt dần), 3 nút −17,2 dB; thân video −0,8 dB.

## 2026-11-20 · EP31 v01 Owner: "diễn biến quá nhanh, không kịp đọc/nghe, nhiều tạp âm, chữ chạy trước tiếng, video giật" — Tự động một phần

- **Nhanh:** giọng VieNeu ~4 chữ/giây, nghỉ sau câu 0,45 s, đuôi cảnh 0,6–1,3 s. **Sửa EP31:** giọng `atempo=0.9` (giữ cao độ; bản gốc `audio/voice_orig_v01/`), vào câu 0,5 s, thêm 0,7 s sau mỗi câu (`TAIL_PLUS`) → 66,6 → 83,9 s. **Checklist (mẫu tập mới nên mặc định):** mỗi cảnh thoại ≥ thời lượng câu + 1,2 s; ưu tiên kịp đọc hơn khung 65–75 s.
- **Tạp âm:** ~40 SFX/66 s, nhiều tiếng tổng hợp từ nhiễu (tích tắc 2,5 s, gõ phím, nước phun, thét, ka-ching, xoảng, riser), nhạc 0,42. **Sửa:** ~1 SFX nhẹ/cảnh (≤ 0,22), bỏ loại nhiễu, nhạc 0,3. **Checklist:** ≤ 1 SFX/cảnh trừ cú đấm hài; tránh SFX nhiễu dài > 0,5 s dưới thoại.
- **Chữ trước tiếng:** đo tương quan chéo — giọng đặt đúng tuyệt đối (lệch 0,000 s); gốc là thẻ hiện cả cụm 3–4 chữ ngay chữ đầu. **Chặn (Tự động):** `scene_kit.WORD_REVEAL` — khung thẻ theo cả cụm (không lệch tâm, giữ bài học EP27) nhưng chữ chỉ hiện khi giọng đọc tới; `WORD_HOLD` 0,12 → 0,4 s.
- **Giật:** đo chênh lệch khung: `K.shaken` (sin(t·95) → nhảy ngẫu nhiên từng khung) tạo 34 cú nhảy/3 s; zoom tức thì (F15, F19); `fr()` dò zoom bước 0,01 nhảy nấc; tranh mặt sát lề có zmax ~1,02 → `push` kẹp cứng → đứng hình 70–87 % cảnh. **Sửa trong tập:** bỏ rung, `snap()` zoom êm 0,25 s, `zmax()` dò nhị phân 1 lần/cảnh, `push` co biên độ vào [1, zmax]. Đo lại: cú nhảy chỉ còn ở chuyển cảnh có chủ đích, đứng hình ≤ 19 %/cảnh. **Việc tiếp theo:** đưa `zmax/push/snap` vào `scene_kit` cho mọi tập; thêm kiểm tra tự động "đứng hình/giật" sau `--mux` (đã có đoạn đo bằng numpy trong phiên này).

## 2026-11-20 · EP31 tranh: ChatGPT có 2 ô soạn tin, nhãn chữ bị cắt mép — Tự động một phần

- **ChatGPT web có 2 phần tử `[contenteditable][aria-label="Ask ChatGPT"]` (1 ô ẩn 0×0)** → `locator.fill` lỗi strict mode ở cảnh thứ 2 của lô (cảnh 1 vẫn tạo được). **Chặn (Tự động):** `chatgpt_art.py` chọn ô `>> visible=true`. Chạy lại: 18 tranh + 4 tạo lại, không lỗi. Hồ sơ Chrome bị phiên EP30 giữ → Owner cho đóng (SIGTERM đúng PID).
- **Tranh ChatGPT vẫn đặt mặt sát mép** (A12, A17 mặt ở x ≈ 15 px; A08 Mimi lấn phải; A08 vẽ 2 ngón thay vì 3 ngón theo thoại) → tạo lại 1 lần với `--fix`; 9 tranh còn lại thu `art_fit` 0,82–0,95. **Checklist:** đối chiếu số ngón/cử chỉ với lời thoại trên tấm đo.
- **Bóng chữ mờ "NĂM ĐẦU" sau chữ chính (review video v01, xác minh trên MP4 5,5 s).** Gốc: `E.cam` trả lại chính ảnh vào khi z = 1 → cảnh vẽ chữ đóng dấu/lấp lánh ở khung đầu (z0 = 1,0) lên tranh trong bộ nhớ đệm `art_loader`, in vĩnh viễn cho mọi khung sau (F02 chữ + lấp lánh, F09 'TÕM!', F03/F05 lấp lánh). Có thể đã xảy ra ở tập cũ dùng mẫu `push(…, 1.0, …)`. **Chặn (Tự động):** `scene_kit.cam` luôn trả bản sao. Render lại cả tập; unit test NMT đạt (30 lỗi còn lại thuộc micro_story, thiếu YAML reader — có từ trước).
- **Nhãn chữ dán lên đạo cụ bị cắt** ('SỔ ĐI ĐÁM', 'TIỆC CỦA MÌNH') vì thẻ cố định nhỏ hơn chữ. Sửa trong tập: thẻ tự giãn theo bề rộng chữ. **Checklist:** crop kiểm mọi nhãn dán trên bảng hình trước khi gửi Owner.

## 2026-11-20 · EP30/EP31: tay mọc sau lưng (A03), giám khảo chấm lẻ 0,25, hội đồng người xem chấm ASMR như video hài — Checklist

- **Owner phát hiện ở video cuối EP30 v01:** F03 (A03) Tí đứng chính diện nhưng hai tay giơ tô bột như mọc ra từ sau lưng — sai giải phẫu. Tự soát tranh chỉ đo vị trí (mặt, đáy, đỉnh đầu) nên bỏ sót. **Sửa:** tạo lại A03 bằng `chatgpt_art.py --fix` (dáng ba phần tư, tay mọc từ vai phía trước thân), bản cũ ở `art/v01/_superseded/A03_a01_superseded.png`; render lại F03, mux, review vòng 2. **Checklist:** khi xem tấm đo, soát thêm giải phẫu ở mọi tư thế giơ tay/ôm/với: tay mọc từ vai, đúng 2 tay, khuỷu gập hợp lý; prompt tư thế giơ cao ghi sẵn "arms grow from the shoulders in front of the body, three-quarter view".
- **Giám khảo subagent chấm 1.25/0.75** → `--script-review record` báo lỗi "bước 0,5". **Checklist:** prompt gọi subagent giám khảo luôn ghi "điểm mỗi mục là bội số của 0,5".
- **Hội đồng người xem trừ điểm video ASMR không thoại vì "không cười thành tiếng"** (EP30: 17 → 18/24 qua 3 vòng; rubric 7,0 → 8,0 → 8,0) → chuyển Owner, Owner duyệt. Gợi ý cải tiến (chưa làm): câu hỏi 4 của hội đồng nên đổi thành "thư giãn/dễ chịu" khi `META["format"] = "nondialogue"` và brief là ASMR.
- **Codex hết lượt tới 23/11/2026** → mọi tranh qua ChatGPT web: EP30 17 tranh + 1 tạo lại trong một phiên (19–20/11), không chạm giới hạn; EP31 lùi theo quyết định Owner (chắc 1 tập cho T7).
- **Kiểu nhạc trong `MUSIC` phải là `epic|cute|tense`** (`audio_engine.build` chỉ có 3 khoá; `episode_audio.install` ghi đè đúng các khoá này). Đặt tên khác (vd. 'lofi') → `KeyError` ở `--audio`.

## 2026-11-19 · EP29: ChatGPT Plus hết lượt tạo ảnh giữa lô; tranh ChatGPT lệch continuity — Checklist

- **ChatGPT báo "Plus plan limit for image generations" sau 17 ảnh trong ngày (EP28 tạo trước đó cùng ngày) → còn thiếu A18–A21, mở lại sau ~7 giờ.** `chatgpt_art.py` chỉ thấy tin trả lời rỗng (msg ""). **Checklist:** trước khi tạo tranh, cộng số ảnh đã tạo trong ngày (thumbnail + tranh + tạo lại); một tập ~20 tranh + 3–5 tạo lại, nên không tạo 2 tập trong cùng một ngày; tạo các tranh có thoại/twist trước, tranh phụ sau. Khi lỗi rỗng ở giữa lô: chụp màn hình đọc thông báo giới hạn, không gửi lại liên tục.
- **Tranh vẽ thêm/khác hành động so với prompt** (A08 Ngang ngủ "zzz" thay vì lướt điện thoại; A15 thêm Ngang sát mép trái): đối chiếu từng tranh với notes trước khi chú thích; ghi danh sách tạo lại.
- **Mặt sát lề 9:16 (A05, A11):** ép ngang 0,96–0,97 neo trái + kéo mép phải (không phản chiếu) khi phần lề là nền; nếu lề có vật (đồng hồ) thì kéo 1 cột mép và chọn khung camera z ≥ 1,05 để ẩn dải kéo. Ghi `art_fit.json`.
- **Engine:** `episode_audio` thêm SFX `cash`, `sad_violin`, `birds`, `flutter`, `wind`.
- **Owner 19/11 (tối):** (1) nhạc nền ưu tiên dùng lại kho (`qa_checks.music_library`), `--mux` không chặn trùng; (2) phụ đề chuẩn = kiểu D + font kiểu A (Bold 50, không viền) — **Tự động** (`scene_kit.WORD_*`); (3) tiết kiệm token: `CAST:` + `STRICT` trong prompt ChatGPT (cảnh báo khi thiếu CAST), `art_measure.py` (tấm QA ¼ độ phân giải; thử đo bằng màu da thất bại 16/16 — không dùng), viewer panel + video review chạy subagent `sonnet`; `token_report.py` đo token theo tập.
- **Owner 19/11 (tối, lần 2): phụ đề hiện quá nhiều chữ một lúc.** Gốc: thẻ hiện cả dòng ~7–9 chữ, 1–2 dòng. Sửa: 1 dòng, ≤ 4 chữ, cụm thay nhau theo giọng; ngắt theo khoảng ngừng giọng + dấu câu + luật nghĩa (tên riêng, hư từ), ngắt tay `K.SUB_BREAKS` — **Tự động** (`scene_kit.word_chunks/voice_gaps/sub_chunk_report`, `SUB_BREAKS` sai chữ hoặc cụm > 4 chữ thì dừng). Bộ ước lượng mốc từ hay lệch chỗ ngừng 1 chữ → dời về dấu câu.
- **EP29 render F17:** cảnh trả khung RGB (blend nháy trắng tự làm) → chuyển cảnh `flash` lỗi 'images do not match'. **Tự động:** `cute_engine.frame()` chuẩn hoá khung A/B về RGBA trước mọi chuyển cảnh. Ngoài ra: CLI tập không có `--help` — gọi `epNN.py --help` sẽ render cả tập.
- **EP29 review v01:** số tiền đỏ đóng dấu trần đè tóc nhân vật, chìm trên nền carton. Quy tắc: số tiền/thông báo đặt trên **thẻ nền riêng** (trắng bo góc, viền mực) ở chỗ trống không đè nhân vật, trong lề x 108–972 — Thủ công (soát khung giữa cảnh).
- **EP29 export-finish:** `LIBRARY_ART` dựng bằng hàm phụ `_lib(...)` → `library_sync` (literal_eval) dừng ở bước thư viện sau khi đã xuất video. Quy tắc: `LIBRARY_ART` luôn là dict hằng, chỉ dùng tên hằng chuỗi khai báo đầu file (`_G`, `_O…`) — engine báo lỗi rõ; viết đúng ngay từ lúc soạn cảnh.

## 2026-11-19 · EP28: thumbnail qua ChatGPT THUMBNAIL-CREATE, lô ảnh mẫu 0/3, đầu nhân vật sát đỉnh — Tự động một phần

- **Owner 19/11:** thumbnail chỉ tạo qua ChatGPT/Codex, sau khi kịch bản duyệt bản cuối; gửi kịch bản vào chat **THUMBNAIL-CREATE**, mỗi lần 1 mẫu; compact khi đạt 40 %. EP28: gửi `thumb/EP28_KICH_BAN_DUYET.md` + 3 master → v01 (chữ bị lưới 3:4 TikTok cắt dòng 1) → yêu cầu dời chữ xuống 15 % trong cùng chat → v02 đạt. **Checklist:** luôn vẽ khung 3:4 (y 240–1680) + lề 10 % lên thumbnail trước khi nhận.
- **`chatgpt_art.py --new` báo 0/3 ảnh mẫu** dù tải tay ngay sau đó vẫn được: tải lên ngay sau `goto` khi trang chưa sẵn sàng. **Chặn (Tự động):** chờ 3 s rồi tải; sau 20 s vẫn 0 thì tải lại 1 lần. Dự phòng: `--attached`.
- **Tranh 2:3 đặt đầu nhân vật sát đỉnh (y 110–220) và mặt sát lề** (A11, A12, A19; A04/A07/A08/A09/A15/A16/A17 tạo lại 1 lần với `--fix`). Đầu sát đỉnh: dời tranh xuống 120–140 px, phần trên lấp bằng **màu trời trơn** (lấp bằng phản chiếu lộ bàn tay lộn ngược, kéo giãn hàng đầu thành vệt cây — đã thử, loại). **Checklist:** đo đỉnh đầu bằng thước trên bản 1080×1920 trước khi chú thích; giá trị trong `art_fit.json` (`dy`, `dx`).
- **Review video v01 báo 3 lỗi chặn "mất phụ đề" sai** (8,0/10): lưới mỗi 2 s rơi đúng lúc thẻ phụ đề (chạy theo giọng) đã tắt; trích khung 18/28/56 s trên MP4 → phụ đề có đủ. **Chặn (Tự động):** `video_review.prepare` thêm tấm `subs_mid.jpg` lấy điểm giữa từng câu trong `subtitle.srt` và ghi vào prompt; v02 8,5/10 không lỗi chặn. **Checklist:** lỗi chặn của giám khảo phải trích khung MP4 xác minh trước khi sửa.
- **F05 khung nguệch ngoạc nền trắng không nối với Tí** (góp ý review v01, đúng) → bong bóng đặt trên tranh A04 làm mờ, chấm dẫn từ đầu Tí. Đổi sau khi Owner duyệt bảng hình — báo Owner khi gửi video.
- **Chữ đóng dấu "ỤC ỤC!" mất dấu nặng ở cỡ 96** (lặp bài học EP26) → "BÌ BÕM!". **Checklist:** chữ đóng dấu tránh dấu nặng/hỏi dưới chân chữ hoa.

## 2026-11-19 · EP27: nhạc ngắn bị im giữa video, TTS đọc sai ngày, tranh ChatGPT đặt nhân vật thấp — Tự động một phần

- **Nhạc nền ngắn hơn video (22,5 s / 63 s) → im lặng từ giây 22** (EP26 không lộ vì bản nhạc dài). Gốc: `episode_audio._loader` gọi `ffmpeg -ss off` vượt độ dài file. **Chặn (Tự động):** lặp `-stream_loop -1` và quy offset về `off % độ dài`. Kiểm: `video_review.py prepare` báo `silences: []`.
- **TTS đọc "20/11" thành "hai mươi trên mười một".** Gốc: bộ chuẩn hoá VieNeu hiểu "/" là phép chia khi không có chữ "ngày". **Chặn (Tự động):** `tts_vieneu.spoken()` đổi `dd/mm` → `dd tháng mm` chỉ cho giọng (phụ đề giữ chữ số). Mốc từng từ: `scene_kit._spoken_syllables` đếm âm tiết đọc thật của số/ngày ("20/11" = 5 âm tiết) trước khi ước lượng.
- **Tranh ChatGPT 9:16 vẽ nhân vật thấp và rộng** (chân vào dải phụ đề 1480–1680, mặt sát lề) dù prompt ghi "bottom third empty". Thu nhỏ + phản chiếu lề tạo "bóng ma" nhân vật ở hai bên → loại. **Cách xử lý:** tạo lại bằng `chatgpt_art.py --fix "ZOOM OUT … feet above 72% height, faces ≥ 12% from edges"` rồi dùng camera `fr()` (zoom tối đa mà mặt trong 108–972, đáy nhân vật ≤ 1450). Đã thêm `art_fit.fit_down` (chỉ dùng khi lề là nền trơn). **Checklist:** xem overlay trước khi chú thích; tranh có thoại mà chân > 1460 thì tạo lại.
- **ChatGPT đổi tên ô tải ảnh** ("Attach photos" → "Attach photos or videos") → lô đầu báo 0/3 ảnh mẫu. **Chặn (Tự động):** `chatgpt_art.py` thử tên mới trước, tên cũ sau.
- **Owner 19/11 — duyệt video lần 1 "Cần chỉnh":** (1) nhạc nền to → EP27 hạ 0,7 → 0,42; (2) **từ khoá phụ đề lớn hơn 1 cỡ** → `scene_kit.WORD_KEY_SCALE = 1.2` (mặc định engine, mọi tập mới); (3) phụ đề hiện từng từ để lại từ lẻ ở dòng 2 và thẻ lệch tâm khi đang chạy → **hiện theo dòng** (cả dòng hiện khi giọng tới, từ đang đọc vẫn nhấp), không ngắt ngay sau từ viết hoa giữa câu ("Giáo / sư") — **Tự động** (`word_card`, test `test_partial_reveal_shows_whole_lines`); (4) continuity tranh (hoa trên tóc Tí trước cảnh hắt xì, Mimi mất kính, bối cảnh khác phòng) → tạo lại A03/A05/A12/A13 với câu "SAME ROOM … Mimi ALWAYS wears glasses" — **Checklist:** so từng tranh với bảng continuity trước khi gửi bảng hình.
- **Owner 19/11 — chữ điểm/lịch:** điểm viết kiểu giáo viên chấm ("10đ", "0đ", chữ tay đỏ Marker Felt, gạch chân 2 nét) xuất hiện bằng hiệu ứng đóng dấu; chữ ngày phải nằm đúng vòng tròn/tờ lịch (đo bằng lưới toạ độ trước khi đặt). Thumbnail: chữ + băng đỏ vẽ bằng image gen theo mẫu `references/thumbnail`, rồi kiểm khung lưới 3:4 TikTok (y 240–1680) — **Checklist**.

## 2026-11-19 · EP26 xuất: thư viện thiếu tranh nạp qua biến; loudness bản xuất −15,7 LUFS — Checklist

- **Tự phát hiện:** `--export-finish` chỉ thêm 12/18 tranh vào thư viện: tranh gọi qua `push('A03', …)` (tên là đối số hàm phụ) không khớp regex `art('…')`, giống EP20. Đã khai báo đủ trong `LIBRARY_ART`, `--library-sync` → 19/19.
- **Checklist:** tập dùng hàm phụ nhận tên tranh thì khai báo MỌI tranh trong `LIBRARY_ART`. Việc tiếp theo: `library_sync` quét mọi chuỗi `'A\d+'` có file trong `ART_DIR`.
- **Đo bản xuất:** −15,7 LUFS, đỉnh −1,2 dBFS (mục tiêu −14 LUFS / −1,5 dBTP): giới hạn đỉnh kéo mức tích hợp xuống. Không chặn; theo dõi ở tập sau.

## 2026-11-18 · Owner: chuẩn thumbnail mới (prompt thiết kế v1) — Tự động một phần

- **Owner:** gửi prompt thiết kế thumbnail (một ý tưởng, ≤ 2 nhân vật đối lập, câu móc 4–8 từ, từ khoá vàng chanh ×1,2–1,4, display sans siêu đậm hơi hẹp, viền tối + bóng cứng, vùng an toàn 80 % × 70 %, kiểm bản 1/6 và bản che mép). Góp ý EP26: chữ "QUÀ 19/11 – SỐC VẬY?!", nghiêng, siêu đậm, phóng lớn biểu cảm. Cho tải Oswald (OFL).
- **Nguyên nhân bản trước chưa đạt:** khối chữ đen kiểu cũ, Be Vietnam Pro không có bản hẹp, không có bước kiểm bản 1/6/che mép; image gen tự viết chữ thì đúng dấu nhưng tràn vùng an toàn.
- **Cách chặn:** `prompts/thumbnail_designer_v1.md`; `scene_kit.make_thumbnail_v2` (tranh image gen không chữ + chữ Oswald Bold, từ khoá vàng chanh, viền/bóng tím than, `skew`/`tilt`/`zoom`), tự ghi `_qa/thumb_small.png` + `_qa/thumb_safe.png`, CHẶN khi khối chữ ra ngoài vùng an toàn; `_to_916` giữ nguyên bề ngang tranh 2:3. Test `ThumbnailV2Tests`.
- **Còn là checklist:** chữ không đè mặt — máy chưa biết toạ độ mặt trong tranh thumbnail; người kiểm xem `thumb_safe.png` (EP26 lần 1 "?!" đè đầu Mimi, đã hạ cụm nhân vật).
- **Font:** `output/_engine/fonts/Oswald-VF.ttf` (SHA-256 5b38c246…2817), giấy phép `OFL-Oswald.txt`, nguồn github.com/google/fonts/ofl/oswald.

## 2026-11-18 · EP26: lề art_fit thành vệt kéo giãn; thumbnail che mặt — Tự phát hiện, Checklist + công cụ

- **Tự phát hiện trên bảng hình (trước khi gửi Owner):** 12/18 tranh ChatGPT web về khổ 2:3. Cắt cover-fit mất 8 % mỗi bên rồi `art_fit` thu nhỏ → lề hai bên kéo giãn thành vệt dọc thấy rõ (F03, F08, F09, F12, F13). Thumbnail bản đầu: khối chữ ở 1/3 trên che mặt Mimi và nửa mặt Tí. Chữ "BỤP!" mất dấu nặng ở cỡ lớn trên nền rối; nhãn "TƯỞNG TƯỢNG" đè tóc doodle.
- **Nguyên nhân:** art_fit được thiết kế cho tranh gần 9:16; với 2:3 phần nội dung thật hai bên đã bị cắt bỏ trước khi thu nhỏ. `make_thumbnail` mặc định đặt khối chữ trên cùng mà không biết vị trí mặt.
- **Sửa / chặn:** `art_fit.fit_wide` (giữ nguyên bề ngang, đáy phản chiếu sàn mờ nhạt dần, thu thêm s2 ≥ 0,94); `make_thumbnail(block_y=…)` + rule "khối chữ đặt ở vùng không có mặt" trong NMT_STANDARD_PROCESS mục 4/6; đổi chữ đóng dấu sang từ đọc rõ dấu ("PHỊCH!"), nhãn doodle đặt ở phần giấy trống.
- **Kiểm chứng:** `--check-art` 18/18 đạt; bảng hình xem lại không còn vệt; thumbnail không che mặt. Chưa có kiểm tra tự động "khối chữ thumbnail đè mặt" (cần toạ độ mặt từ safe_annotations — việc tiếp theo).

## 2026-11-18 · Owner: "Chuyện nhỏ!" nhàm, bỏ chữ tiêu đề đầu video, video ≥ 1 phút — Checklist

- **Owner (duyệt EP26 v2 → Cần chỉnh):** Tí nói "Chuyện nhỏ!" quá nhàm, không nên lúc nào cũng nói; không cần chữ tiêu đề đầu video; video ≥ 1 phút; kịch bản phải thú vị, dễ hiểu. Chốt tỷ lệ nhân vật semi-chibi như EP25.
- **Nguyên nhân:** BRAND_NMT biến câu cửa miệng và nhãn tên tập thành "dấu hiệu bắt buộc mọi tập"; Claude áp máy móc. Thời lượng theo D-030 "theo topic" nên EP25/EP26 dưới 1 phút.
- **Sửa:** BRAND_NMT mục 3.1/3.4/4 và NMT_STANDARD_PROCESS mục 1, 3.1, 4 cập nhật (câu cửa miệng tuỳ chọn ≤ 1 lần/3 tập; không nhãn tiêu đề; ≥ 60 s; semi-chibi). EP26 viết lại v4.
- **Còn lại:** khuôn `nmt_engine.py new` và `NMT_ENGINE.md` vẫn nhắc nhãn vàng/"Chuyện nhỏ!" ở vài chỗ — sửa cùng đợt code sau khi Owner duyệt quy trình.

## 2026-11-18 · EP26 thử quy trình chuẩn v2: chưa bản nào đạt 9/10; giám khảo subagent mâu thuẫn — Checklist

- **Bối cảnh:** Owner yêu cầu kịch bản chỉ qua khi ≥ 9/10 hoặc qua review vai người xem. Codex hết lượt (tới 22:50 18/11) → 3 lần chấm rubric bằng subagent Claude mới + 3 lần hội đồng người xem (3 vai, 8 câu).
- **Kết quả:** v1 8,4 · 18/24; v2 8,0 · 20/24 (người xem đạt); v3 7,5 · 18/24. Trình Owner bản v2.
- **Nguyên nhân gốc:** (1) giám khảo chưa hiệu chỉnh cho kết quả dao động ±0,5–1 điểm giữa các bản; góp ý hook mâu thuẫn (v1/v2: "núi bát ở hook làm lộ twist", v3: "hook phải dùng núi bát"); (2) mỗi vòng sửa thêm cảnh để đáp góp ý nên bản sau dài và nhiều đạo cụ liên tục hơn → mất điểm `producible`; (3) trong sổ lỗi 15 lần chấm, chưa lần nào ≥ 9,0.
- **Chặn tái diễn (checklist):** sửa theo góp ý xuất hiện ở ≥ 2 giám khảo, bỏ qua góp ý mâu thuẫn; không tăng số cảnh khi sửa (gộp trước, thêm sau); giới hạn ~16 cảnh/55 s. Ngưỡng 9,0 chỉ có ý nghĩa sau khi hiệu chỉnh giám khảo (`script_review.py calibrate`) — đề xuất trong `NMT_STANDARD_PROCESS.md`.
- **Bằng chứng:** `output/ep26_quoc_te_dan_ong/render/script_review_v2std.json`, `_review_v1..v3/`, sổ `script_review_findings.jsonl`.

## 2026-11-18 · EP25 chọn nhầm outro tai mèo — Tự động + Checklist

- **Owner:** dùng mặc định outro cuối 7,8 giây có xuất hiện và biến mất; bỏ outro icon mèo vì không dùng nữa.
- **Nguyên nhân:** EP25 chọn `outro_cta` 3,6 giây theo phần tài liệu cũ; EP24 đã dùng `subscribe_outro`, nhưng khuôn `new` vẫn tạo End card 3,2 giây và hướng dẫn chính chưa đồng bộ.
- **Sửa:** EP25 dùng `subscribe_outro` + `subscribe_sfx`, 7,8 giây, vào bằng cut. Khuôn tập mới có sẵn cùng renderer/SFX và thời lượng `SUB_DUR`. Đồng bộ NMT_ENGINE, prompt, command và quy tắc nhận diện; bỏ outro tai mèo khỏi luồng dựng mới. Không sửa video/tập cũ.
- **Chặn tái diễn:** test tạo tập thật trong thư mục tạm, kiểm thời lượng/tên cảnh/cut/SFX, thanh hiện giữa cảnh và biến mất ở cuối. Giữ test render các mốc chuyển động và vùng an toàn.
- **Kiểm chứng:** 49 test Phase A/A2 đạt; 5 test outro đạt; kiểm tra riêng EP25 đạt. Preview MP4 `output/ep25_khen_em_hay_khen_doi_dep/preview/outro_v02.mp4`: H.264/AAC, 540×960, 30 fps, 7,800 giây. Đã xem khung trích MP4 khi hiện thanh và cuối cảnh; phần âm thanh chưa được đánh giá bằng tai. Bản đầy đủ vẫn chờ Owner duyệt hình v02.

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


## 2026-11-12 · Giai đoạn A: chuyển 4 bài học từ Checklist sang Tự động

- **Phạm vi:** Owner duyệt Giai đoạn A của `docs/architecture/NMT_PIPELINE_UPGRADE_PLAN.md` ("Duyệt, làm A").
- **EP13 iris lồng hai Mimi → Tự động:** `--check-transitions` (chặn `--mux`) lỗi khi vào End card/Outro không phải `cut`; mẫu tập mới dùng `cut`. Chạy trên bản sao EP12 (End card `iris`, đã xuất trước bài học) → bị chặn đúng.
- **EP19 hình đi trước tiếng → Tự động một phần:** `voice_onset()` đo im lặng đầu WAV; `--check-sync` (chặn `--mux`) lỗi khi câu mở có tiếng thật > 0,20 s (hiệu chỉnh: EP19 đã duyệt = 0,16 s), câu chồng nhau, vượt cuối video; cảnh báo khi hình vào trước tiếng > 0,6 s ở cảnh sau. `K.cut_at(vid)` cho mốc cắt hình theo tiếng. Mẫu tập mới `FIRST_LEAD = 0.05`. Vẫn là checklist: cú cắt giữa cảnh gắn với câu thoại (tập phải dùng `cut_at`).
- **EP16/EP17 tranh lấn vùng an toàn, kiểm trên ảnh nhỏ → Tự động một phần:** `--check-art` đo độ phủ, tỉ lệ, nghi trùng (ngưỡng 20 hiệu chỉnh trên EP17: F07 v01 lặp F06 = 11,7; khác cảnh ≥ 47) và bắt buộc chú thích đáy nhân vật cho từng tranh, kèm overlay 540×960 lưới 100 px. Máy không nhận diện nhân vật: con số đáy/đầu vẫn do người kiểm ghi, máy chặn khi thiếu hoặc vi phạm.
- **EP16 `--tts` trỏ sai model → Đã sửa engine:** `tts_vieneu.py` tìm model trong repo; chạy thật 1 câu (Hải Đăng) 2,4 s.
- **Lỗi do test phát hiện:** bản đầu `coverage()` tính độ lệch màu gộp 3 kênh nên nền kem (255,246,236) không bị coi là viền; sửa thành độ lệch từng kênh, có test `test_cream_frame_fails_coverage`.
- **Kiểm tra:** `PYTHONPATH=src python3 -m unittest discover -s tests/unit` → 299/299 OK (17 test mới `tests/unit/test_nmt_phase_a.py`).


## 2026-11-12 · A2: hiệu chỉnh giám khảo khi Codex hết hạn mức — Tự động

- **Tự phát hiện:** Owner cho phép tiêu lượt Codex; cả 15 lượt `script_review.py calibrate` bị Codex từ chối `usageLimitExceeded` (hết hạn mức tới 16/11/2026 14:47). Bản đầu vẫn chạy hết 15 mẫu và ghi "accuracy 0, pass false" như một kết quả hiệu chỉnh thật.
- **Nguyên nhân:** `calibrate` bắt mọi lỗi theo từng mẫu, không phân biệt lỗi chấm (JSON sai) với lỗi hạ tầng (hết lượt, mất kết nối).
- **Sửa / chặn:** `CodexUnavailable` làm dừng ngay, không ghi file hiệu chỉnh; CLI báo rõ lý do. Lần chạy hỏng được đánh dấu `aborted`, bỏ mục `judges.codex`. Test `test_quota_error_aborts_without_writing`. `art_auto` vốn đã dừng ở lỗi đầu tiên.



## 2026-11-12 · EP20: nhân vật sát lề cắt, phụ đề 2 dòng lố dải, tải ảnh ChatGPT — Tự động một phần

- **Tự phát hiện (trước khi Owner duyệt hình):** 4/20 tranh image_gen đặt nhân vật sát mép dù prompt ghi "central 80% of the width": A14, A14b, A16 (mặt Mimi x ≈ 930–1080, vào lề cắt TikTok/Shorts và cột nút phải); A02 đầu Tí y ≈ 30 (vùng thanh trạng thái). `--check-art` cũ chỉ kiểm theo trục dọc nên không bắt được.
- **Sửa EP20:** tạo lại 4 tranh với khối "COMPOSITION (STRICT): every character inside the CENTRAL 70% of the width … top 18% only background" (bản lùi máy); bản cũ giữ ở `art/v01/_superseded/`.
- **Chặn tái diễn → Tự động:** `safe_annotations.json` nhận thêm `face_x: [x trái, x phải]` của các mặt; `qa_checks.check_art` lỗi khi ra ngoài 108–972, cảnh báo khi thiếu. Test `test_face_in_crop_margin_fails`. Prompt mẫu nên dùng khối COMPOSITION (STRICT) ở trên ngay lần đầu.
- **Phụ đề 2 dòng lố đáy dải (tự phát hiện bằng `--check-subs`):** viên phụ đề trượt vào (`pin < 1`) đặt thấp hơn 26 px nên câu 2 dòng chạm y 1681–1685 > 1680. Sửa gốc trong `scene_kit.make_post`: kẹp đáy viên ≤ `SF.SUB_BOTTOM_MAX`. Mọi tập dùng `K.install_post()` tự nhận.
- **Tải ảnh ChatGPT trong khung trình duyệt của app:** nút tải của Owner đôi khi chỉ để lại file tạm `~/Downloads/.Q6L2SF6YDW.com.anthropic.claudefordesktop.*` (PNG đầy đủ). Cách ổn định: Claude kích hoạt tải bằng thẻ `<a download>` trên blob của ảnh, rồi đối chiếu file tạm theo kích thước/băm và chép vào `art/vNN/<CẢNH>.png`; ảnh Owner tự lưu được so băm và gom vào `_owner_downloads/`, không xoá. Clipboard và POST về localhost đều bị chặn (quyền clipboard; CSP).
- **Chấm kịch bản khi Codex hết lượt:** 3 lần giám khảo subagent Claude đều 7,5/10 → chuyển Owner (đúng quy trình D-029); Owner chọn "Duyệt + sửa góp ý lần 3".
- **`--export-finish` thêm thư viện lỗi/thiếu (tự phát hiện):** (1) `library_sync._scenes_meta` dùng `literal_eval` nên hỏng khi `LIBRARY_ART` dùng hằng chuỗi chung (`_G = '…'`); (2) tranh gọi `art(name)` qua biến (4 ô montage F06) không khớp regex nên chỉ thêm 16/20. Sửa: `_literal_with_consts` thay tên hằng ở đầu file rồi mới `literal_eval`; danh sách tranh hợp thêm các khoá `LIBRARY_ART` có file. Kiểm lại: EP20 đủ 20/20 (asset_index 304 mục), EP19 vẫn đọc 14/14. Toàn bộ test đơn vị 327/327 OK.


## 2026-11-13 · Rule chấm kịch bản > 9,0/10 tự duyệt + sổ lỗi chấm kịch bản — Tự động

- **Yêu cầu (Owner):** "nếu điểm chấm > 90 thì mặc định được duyệt, những lỗi tìm thấy cần được ghi nhận và luôn luôn cải tiến về sau." Owner duyệt trực tiếp EP21 v2 và EP22 v2 (8,0/10, giám khảo subagent chưa hiệu chỉnh) cùng lúc.
- **Bối cảnh:** Codex hết lượt tới 16/11/2026 14:47, nên mọi tập đều phải chấm bằng subagent Claude chưa hiệu chỉnh và luôn chuyển Owner, kể cả khi điểm rất cao. Góp ý của giám khảo chỉ nằm rải rác trong `render/script_review.json` của từng tập, không ai đọc lại khi viết tập sau.
- **Cách chặn (`script_review.py`):** `OWNER_AUTO_ABOVE = 9.0`: tổng > 9,0 thì `auto_gate_ok` với mọi giám khảo (`gate_rule = "owner_above_9"`); đúng 9,0 vẫn chuyển Owner. `record_findings` ghi mỗi lần chấm vào `script_review_findings.jsonl`; `findings` tổng hợp mục mất điểm; `backfill` nạp 7 lần chấm cũ (EP20–EP22).
- **Kiểm tra:** 4 test mới trong `tests/unit/test_nmt_phase_a2.py` (9,5 tự duyệt khi chưa hiệu chỉnh; đúng 9,0 vẫn chuyển Owner; mọi lần chấm vào sổ; không ghi trùng + backfill). Toàn bộ unit test 331/331 OK.
- **Bài học từ sổ (7 lần chấm EP20–EP22):** mất điểm nhiều nhất ở `producible` (cảnh nhồi nhiều khoảnh khắc), `escalation` (lời dẫn dán nhãn "Lần một…", E3 không thêm thông tin mới), `twist` (lộ hung thủ sớm, logic đạo cụ hở), `character_brief` (Ngang thiếu chất drama). Checklist khi viết: mỗi cảnh một key pose, không lời dẫn dán nhãn, mỗi bước leo thang thêm hành động hoặc thông tin mới, kiểm logic đạo cụ qua từng cảnh, cho Ngang ít nhất một nhịp drama.


## 2026-11-13 · Tạo tranh qua ChatGPT web bằng Playwright khi Codex hết lượt — Tự động một phần

- **Yêu cầu (Owner):** "Tạo ảnh thêm một cách nữa là sử dụng Playwright, tôi đã đăng nhập ChatGPT trên chrome… tạo ảnh và download về tự động (đây là cách tạm thời thay thế khi Codex chạm limit)."
- **Trở ngại gặp phải:** (1) hồ sơ Chrome Playwright bị một tiến trình playwright-mcp cũ (mở lúc 09:26) giữ → "Browser is already in use"; Owner cho phép, Claude gửi SIGTERM cho đúng tiến trình Chrome đó, đăng nhập vẫn còn trong hồ sơ. (2) Môi trường `browser_run_code_unsafe` không có `require`/`fs`, chỉ đọc file trong repo hoặc `.playwright-mcp/` → tải ảnh bằng `<a download>` trên blob + `download.saveAs`. (3) Ô nhập ChatGPT là ProseMirror `[contenteditable][aria-label="Ask ChatGPT"]`, không có `#prompt-textarea`; input "Take a photo" không nhận nhiều file → dùng input `aria-label="Attach photos"`.
- **Cách làm:** `output/_engine/chatgpt_art.py` sinh JS theo lô; nén các dòng lặp (khoá nhân vật, bố cục, negative) thành token để file gọn; bỏ qua cảnh đã có file (không ghi đè).
- **Kiểm tra:** 3 test `tests/unit/test_chatgpt_art.py` (khôi phục đúng prompt, câu mở đầu lô, không ghi đè, cảnh lạ bị chặn). Chạy thật: EP21 13/13, EP22 11/11 tranh, không trùng băm, ~941×1672.
- **Rủi ro còn lại:** giao diện ChatGPT đổi nhãn nút/ô nhập thì JS hỏng (báo lỗi, không ghi file dở); ChatGPT có hạn mức tạo ảnh theo gói của Owner. Đây là cách tạm thời; khi Codex có lượt lại thì quay về `--art-auto`.


## 2026-11-13 · EP21/EP22: nhạc nền lặp giữa các tập, thiếu cảnh kêu gọi Like/Share/Subscribe — Tự động

- **Owner góp ý video cuối EP21, EP22:** "Nhạc nền của video sử dụng đi cùng 1 bản nhạc giống nhau, cần đổi nhạc nền khác. Với lại thêm phần hiệu ứng cuối video, Like share và subscribe."
- **Nguyên nhân gốc:** để tiết kiệm bước tải, Claude chép module âm thanh EP20 (hai bản CC0 "Tokyo" + "Blue Sky") sang EP21, EP22; hai bản này đã dùng ở EP18, EP19, EP20 → 5 tập liền một nhạc. Không có kiểm tra nào so nhạc giữa các tập. Cảnh kết kêu gọi tương tác chưa từng là yêu cầu của mẫu tập.
- **Sửa trong tập:** EP21 dùng "Pizzicato strings - bright, fun, boppy" (jstarrcreative, Freesound #742677, CC0), EP22 dùng "Joy Park" (mellotrix9898, #772679, CC0) — Owner cho tải từng file; mỗi tập một bản chạy liền mạch theo thời gian video. Thêm cảnh Outro 3,4 s (EP21 F13, EP22 F12).
- **Chặn tái diễn:** `qa_checks.music_reuse` + `require_music_unique` chặn `--mux` khi SHA nhạc trùng tập khác; `scene_kit.outro_cta` dùng chung; rule ghi trong command và NMT_ENGINE. Test: `tests/unit/test_chatgpt_art.py` (MusicReuseTests 2 test, SafeZoomTests 3 test).
- **Góp ý lần 2 của Owner (cùng ngày):** "3 nút like share và subscribe cùng hiển thị trên 1 hàng và có hiệu ứng click vào, thêm hiệu ứng mèo cho các nút… hoặc hiệu ứng tùy theo topic". Thiết kế lại `outro_cta`: 3 nút tròn có tai mèo trên một hàng, chân mèo Mimi bấm lần lượt (nút lún–nảy, đổi trạng thái, bung hạt), nền động + hạt theo chủ đề (`theme`: EP21 `paws` gợi lại dấu chân vụ án, EP22 `snow` gió mùa), thẻ kính mờ giúp đọc rõ trên nền rối. Thời lượng 3,6 s.

## 2026-11-13 · EP22: `--export-finish` lỗi ở bước thêm thư viện vì `LIBRARY_ART` có biểu thức — Checklist

- **Tự phát hiện:** `'style': _S + ', hồng ngoại xanh'` làm `library_sync._literal_with_consts` báo `malformed node` (chỉ thay được tên hằng, không tính biểu thức). Video 3 nền tảng đã xuất xong trước bước này.
- **Sửa:** khai báo hằng `_S_IR` riêng rồi chạy `--library-sync` bằng tay: EP22 thêm 11/11 tranh (EP21 13/13 tự thêm khi xuất).
- **Checklist:** trong `LIBRARY_ART` chỉ dùng chuỗi hoặc tên hằng chuỗi, không cộng chuỗi/gọi hàm.


## 2026-11-13 · Góp ý Owner về chất lượng nội dung + review video độc lập — Tự động một phần

- **Góp ý (Owner):** nội dung quá học thuật, thiếu từ ngữ đời thường; kịch bản chưa thực sự gây cười; kênh chưa có đặc điểm nhận diện. Không cần đủ 3 nhân vật, không cần thoại/phụ đề cho mọi thứ; biểu cảm cường điệu, nhân vật bựa, nét vẽ nguệch ngoạc cũng gây cười. Cần review video độc lập (hình, âm thanh, phụ đề, chất lượng) trước khi hỏi Owner, tối đa 3 lần.
- **Nguyên nhân gốc:** chủ đề chọn theo "khái niệm" (trọng lực, điều tra, ngoại phạm) thay vì tình huống đời thường; lời dẫn và phụ đề dày; không có dấu hiệu lặp lại giữa các tập; chỉ có giám khảo kịch bản, không có ai xem video thành phẩm trước Owner.
- **Cách chặn:** `docs/marketing/BRAND_NMT.md` (lời hứa kênh, 5 dấu hiệu nhận diện lặp lại, quy tắc viết: tối đa 4–6 câu thoại, chữ cảm thán thay phụ đề, phóng đại); `output/_engine/video_review.py` (prepare → giám khảo độc lập → record; ≥ 8/10 và không lỗi chặn; tối đa 3 lần; sổ `video_review_findings.jsonl`); rule ghi vào command. Test `tests/unit/test_video_review.py` 5/5.

## 2026-11-13 · EP23/EP24: tranh ChatGPT web đặt mặt sát mép, chân xuống dải phụ đề — Tự động một phần

- **Tự phát hiện (overlay `--check-art`):** 5/15 tranh EP23 và 9/12 tranh EP24 có mặt (thường là Mimi) ở x < 108 hoặc > 972; nhiều cảnh có thoại vẽ chân tới y 1580–1685 (đè dải phụ đề 1480–1680) dù prompt ghi "central 70%, bottom third empty".
- **Đã thử:** tạo lại 14 tranh với `--fix` "central 75%, ≥ 12% từ mép" → 10/14 đạt; EP23 A01, A04 tạo lại lần 3 với vị trí cụ thể ("Mimi ở giữa-phải") → mặt đạt nhưng chân vẫn xuống thấp.
- **Cách chặn:** `output/_engine/art_fit.py` thu nhỏ tranh vào giữa (hệ số s, neo mép trên, `x' = 540 + (x−540)·s`, `y' = y·s`), lề đáy phản chiếu mờ, lề hai bên kéo mép mờ mạnh (phản chiếu hai bên sinh "mặt ma"), khung nguệch ngoạc nền trắng thì lề trắng phẳng. Bản gốc giữ ở `_superseded/<CẢNH>_raw.png`, hệ số trong `art_fit.json`, `safe_annotations.json` ghi cả số đo gốc (`raw`) và `fit_scale`. `qa_checks`: khung nguệch ngoạc nền giấy trắng ghi `"paper_bg": "<lý do>"` → độ phủ thấp chỉ cảnh báo. Test `tests/unit/test_art_fit.py` 3/3.
- **Quy trình mới:** tạo lại tối đa 1 lần với `--fix`; còn lệch thì dùng `art_fit.py` (s ≥ 0,82) thay vì tạo lại nhiều lần.

## 2026-11-13 · EP23/EP24: review video độc lập lần 1 chỉ đạt 7,0/10 — Tự động một phần

- **Giám khảo độc lập lần 1:** EP23 7,0 (2 lỗi chặn: F15 zoom "Mimi phán xét" cắt nửa Tí ở mép trái + lộ lề mờ art_fit; im lặng 2,2 s đúng nhịp phán xét), EP24 7,0 (im lặng dài, cảnh đứng hình 6–7 s, thẻ đè tai Mimi). Cả hai trừ điểm độ to bản gốc (-22/-25 LUFS) dù bản xuất nền tảng đã loudnorm về -14.
- **Sửa:** tâm zoom phán xét lấy từ overlay của tranh SAU art_fit (không ước lượng); khung phán xét chừa x 160–960 (không lộ lề mờ); nhạc nền không tắt hẳn mà hạ 0,3 dưới tiếng "tách" + meo trầm; tự đo `silencedetect` ngay sau `--mux`, cắt mọi khoảng lặng > 1,7 s (EP24 có 3,5 s ở 0 s và ~9 s quanh F08–F10); Ken Burns mạnh hơn cho cảnh > 5 s; `K.paper()` kẻ giấy vở trên vùng trắng của khung nguệch ngoạc; prompt `video_review` ghi rõ loudnorm -14 ở bước xuất. Lần 2: EP23 8,5, EP24 8,5 — ĐẠT.
- **Còn lại (không chặn, cần sửa ở khâu tranh/kịch bản tập sau):** cảnh một key pose > 5 s vẫn bị chê đứng hình → kịch bản nên ≤ 4,5 s/key pose hoặc 2 key pose; liền mạch đạo cụ (mũ đầu bếp, vết nhọ, vết cà phê) phải ghi vào prompt từng cảnh; khung nguệch ngoạc nên ≤ 2–3 s; Mimi trong khung nguệch ngoạc cũng phải nét nguệch ngoạc.

## 2026-11-13 · Owner: thẻ "30 PHÚT TRƯỚC" đè mặt; outro theo clip mẫu; --mux ghép bản cũ không báo — Tự động

- **Owner:** thẻ chữ ở trên đè mặt nhân vật → dời xuống y 1380 (trên dải phụ đề). Outro Like/Đăng ký/Thông báo phải **y như clip mẫu** (`avatar_banner/ScreenRecording_11-13-2026 20-55-26_1.mov`), chỉ đổi avatar kênh → `scene_kit.subscribe_outro` + `subscribe_sfx` (7,8 s), avatar `avatar_banner/nmt_channel_avatar.png`; rule trong command. Test `tests/unit/test_subscribe_outro.py` 4/4.
- **Tự phát hiện:** cảnh outro lỗi PIL `x1 < x0` khi thanh trắng còn rất ngắn, nhưng `--mux` vẫn ghép segment cũ (67 s) với tiếng mới (71 s) mà không báo (vòng lặp shell `| tail` nuốt lỗi). **Chặn:** `mux()` kiểm độ dài từng segment so với thời lượng cảnh (lệch > 0,1 s → CHẶN); chạy lô render với `set -o pipefail`; test render mọi khung outro.
- **video_review:** video đổi sau khi đã đạt (Owner yêu cầu sửa) → `prepare` tự mở vòng review mới (tối đa 3 lần/vòng) thay vì từ chối. Giám khảo 3 vòng: EP23 7,0 → 8,5 → (vòng 2) 7,5 → 8,0; EP24 7,0 → 8,5 → (vòng 2) 8,5 → (vòng 3) 8,0.
- **Khung nguệch ngoạc:** đặt giữa tờ giấy vở (`paper_shot`, dời tranh xuống) thay vì để 1/3 dưới trống; bỏ chớp trắng tự thêm khi PLAN đã có chuyển cảnh 'flash'. Chữ "XÌÌÌ!" bị đọc như chữ thường → "XỊT XỊT!".
