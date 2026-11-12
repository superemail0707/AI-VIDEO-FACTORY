# Prompt mẫu: nmt-engine

Có 3 cách gọi:

1. **Claude Code mở trong thư mục dự án:** gõ `/nmt-engine Ngày đầu yêu vs năm thứ 3`. Lệnh đọc từ `.claude/commands/nmt-engine.md`.
2. **Claude app/AI khác có quyền đọc dự án:** dán prompt đầy đủ ở cuối file. Nếu đã cài skill riêng, dùng tên skill thực tế trong ứng dụng; repo không tự đổi tên skill bên ngoài.
3. **CLI cục bộ:** `python3 output/_engine/nmt_engine.py list` hoặc `new "<chủ đề>"`; sau đó thực hiện theo tài liệu và cổng duyệt của tập.

Dòng gọi nhanh:

```
nmt-engine: <chủ đề>
```

Ví dụ: `nmt-engine: Ngày đầu yêu vs năm thứ 3`

Nếu AI chưa có skill `nmt-engine`, dán prompt đầy đủ sau:

```
Dùng nmt-engine — Ngang Một Tí (dựng hoạt hình 2D có cổng duyệt) trong dự án AI-VIDEO-FACTORY
(/Users/tthanhtaicntt/AI_Projects/AI-VIDEO-FACTORY) để làm một video hài cặp đôi 9:16 cho chủ đề:
"<CHỦ ĐỀ>"

Đọc trước: output/_engine/NMT_ENGINE.md và output/_engine/IMPROVEMENT_LOG.md.
Nếu tiếp tục tập cũ, đọc CURRENT_PREVIEW.json và workflow của revision hiện hành để tránh xuất nhầm bản.

Nhân vật:
- Tí (bạn trai, giọng Hải Đăng)
- Ngang (bạn gái tóc dài, giọng Trúc Ly)
- Mimi (mèo mướp, không nói)
Chỉ dùng sprite approved trong character_library/asset_index.json. Tìm hình trong thư viện trước, chỉ ghép khi không có.
Không sao chép nhân vật, kịch bản hay âm thanh có bản quyền.

Phong cách: hài, đáng yêu, đôi khi hơi "vô tri" nhưng cuốn. Video thoại khoảng 25–35 giây; video theo nhạc dùng đoạn được Owner chọn. 1080×1920, 60 fps.
Phụ đề không ghi tên nhân vật. Góc máy đa dạng, chuyển động mượt và sống.

Làm tuần tự, dừng chờ tôi duyệt ở từng bước. Trình bày nội dung ngay trong chat rồi hỏi duyệt, không bắt tôi mở file:
1. Tạo tập: nmt_engine.py new "<CHỦ ĐỀ>"
2. Kịch bản: hook, 3 nhịp leo thang, twist, câu chốt. Câu thoại ≤ 45 ký tự.
   Chạy --script, đưa toàn bộ kịch bản vào chat → CHỜ TÔI DUYỆT.
   Toàn bộ kịch bản phải hiển thị trực tiếp trong chat, gồm từng cảnh, hành động/biểu cảm, lời thoại hoặc không thoại, âm thanh và outro. Gửi nội dung đầy đủ trước câu hỏi có hai lựa chọn Duyệt / Cần chỉnh; không chỉ gửi đường dẫn file hay thông báo đã sẵn sàng. Lời nhắc và câu trả lời duyệt phải chỉ rõ tập/phiên bản. Yêu cầu cập nhật quy trình hoặc góp ý không được tính là duyệt; chỉ ghi nhận duyệt khi Owner xác nhận rõ ràng.
3. Giọng và bảng hình mẫu: --tts, viết cảnh, --storyboard, tự kiểm tra theo checklist mục 4,
   gửi contact sheet và mô tả từng cảnh → CHỜ TÔI DUYỆT.
4. Dựng video: render từng cảnh, --audio, --mux, kiểm tra lưới khung hình và âm lượng,
   gửi video → CHỜ TÔI DUYỆT.
5. Sau khi tôi duyệt video cuối: viết post.json (caption và hashtag cho từng nền tảng),
   --export cho tiktok, youtube_shorts, facebook_reels, rồi --export-finish,
   vào videos-post/<slug chủ đề>/<nền tảng>/. Báo đường dẫn.

Ghi quyết định duyệt bằng --approve … --by "owner (chat)".
Chỉ dùng tool, plugin, model, mã GitHub miễn phí 100% (ưu tiên chạy cục bộ). Không tự đăng lên mạng, không commit hay push, không ghi DECISIONS.md khi chưa được duyệt.
Nếu tôi chọn "Cần sửa" mà không ghi rõ nội dung, hãy hỏi lại.
```


**Cập nhật Owner 10/11/2026 — ưu tiên quy tắc khung cũ:** hình/bối cảnh phủ ≥95% màn hình, không khung bo góc với nền trắng/kem thừa. Nhân vật/biểu cảm/hành động chính vẫn ở vùng tập trung x108–950,y200–1460; phụ đề canh giữa trong1480–1680, không đè nhân vật/watermark. Ngoại vi là bối cảnh thật, không nền mờ/kéo giãn. Xem mục cập nhật bố cục trong NMT_ENGINE.md.
