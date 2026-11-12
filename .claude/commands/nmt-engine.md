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
1. **Kịch bản**
   - Điền `META` và `PLAN` trong `output/epNN_<slug>/render/epNN.py`.
   - Cấu trúc: hook trong 2 giây đầu, 3 nhịp leo thang, twist, câu chốt dễ thương. Video thoại thường khoảng 25–35 giây; video theo nhạc dùng thời lượng đoạn Owner chọn. Mỗi câu thoại tối đa khoảng 45 ký tự.
   - Chạy `python3 epNN.py --script`, rồi trình bày toàn bộ kịch bản trong chat.
   - Toàn bộ kịch bản phải hiển thị trực tiếp trong chat, gồm từng cảnh, hành động/biểu cảm, lời thoại hoặc không thoại, âm thanh và outro. Gửi nội dung đầy đủ trước câu hỏi có hai lựa chọn Duyệt / Cần chỉnh; không chỉ gửi đường dẫn file hay thông báo đã sẵn sàng. Lời nhắc và câu trả lời duyệt phải chỉ rõ tập/phiên bản. Yêu cầu cập nhật quy trình hoặc góp ý không được tính là duyệt; chỉ ghi nhận duyệt khi Owner xác nhận rõ ràng.
   - ⛔ CHỜ Owner duyệt. Khi duyệt: `--approve script --by "owner (chat)"`.
2. **Giọng và hình mẫu**
   - Với video thoại: chạy `--tts`. Với video theo nhạc: dùng âm thanh/đoạn đã được Owner cung cấp và duyệt, căn lời tại máy bằng workflow của tập; không tạo TTS chồng bài hát. Viết `epNN_scenes.py`, rồi chạy `--storyboard` khi tập dùng CLI chuẩn.
   - Tự kiểm tra theo checklist ở mục 4 của NMT_ENGINE.md.
   - Gửi `contact_sheet.png` kèm mô tả từng cảnh.
   - ⛔ CHỜ duyệt. Khi duyệt: `--approve visual`.
3. **Video**
   - Render từng cảnh, mỗi lượt dưới 180 s. Sau đó chạy `--audio` và `--mux`.
   - Kiểm tra lưới khung hình và `volumedetect`, rồi gửi `final_video.mp4`.
   - ⛔ CHỜ duyệt. Khi duyệt: `--approve final`.
4. **Xuất đa nền tảng**
   - Viết `post.json`, chạy `--export tiktok|youtube_shorts|facebook_reels …`, rồi `--export-finish`.
   - Kết quả nằm ở `videos-post/<slug>/<nền tảng>/`. **Không tự đăng.**
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
