# Prompt thiết kế thumbnail NMT — v1 (Owner 18/11/2026)

Nguồn: Owner gửi trong chat 18/11/2026 ("Thay đổi thumbnail cho nmt-engine theo prompt bên dưới"). Đây là chuẩn thumbnail cho mọi tập từ EP26.

**Cách engine áp dụng (Claude ghi):**
- Bước 1–4 (ý tưởng, hình, chữ) Claude làm theo prompt, ghi vào `post.json["thumbnail"]` (`idea`, `text`, `keyword`).
- Hình: image gen (Codex `--art-auto` hoặc `chatgpt_art.py`), prompt `art/PROMPTS_thumb.md`, **không vẽ chữ trong tranh** vì image gen hay sai dấu tiếng Việt; phần trên vùng an toàn để trống cho khối chữ.
- Chữ: dựng bằng `scene_kit.make_thumbnail_v2` (display sans siêu đậm, từ khoá màu nhấn ×1,2–1,4, chữ còn lại trắng, viền tím than + bóng cứng lệch nhẹ, đúng dấu tiếng Việt), đặt trong vùng an toàn 80 % × 70 %.
- Kiểm tra mục 8: hàm ghi `_qa/thumb_small.png` (1/6 kích thước) và `_qa/thumb_safe.png` (che mép ngoài vùng an toàn) để xem trước khi gửi Owner.

---

Bạn là người thiết kế thumbnail cho video kể chuyện.

Đọc kịch bản được cung cấp, sau đó tạo MỘT thumbnail hoàn chỉnh. Tự chọn hình ảnh và câu chữ phù hợp với câu chuyện theo các nguyên tắc dưới đây.

ĐẦU VÀO
- Kịch bản: {{KỊCH_BẢN}}
- Mô tả hoặc ảnh tham chiếu nhân vật: {{NHÂN_VẬT}}
- Tỷ lệ ảnh: {{TỶ_LỆ_ẢNH — mặc định 9:16}}
- Yêu cầu riêng nếu có: {{YÊU_CẦU_RIÊNG}}

1. CHỌN Ý TƯỞNG TRƯỚC KHI THIẾT KẾ

Xác định:
- Ai là nhân vật chính?
- Điều gì bất thường, mâu thuẫn hoặc bất ngờ nhất?
- Cảm xúc nào khiến người xem muốn biết chuyện gì xảy ra?
- Chi tiết hình ảnh nào giúp hiểu tình huống nhanh nhất?

Từ đó chọn MỘT ý tưởng hình ảnh trung tâm.

Không tóm tắt toàn bộ kịch bản lên thumbnail.
Không ghép nhiều cảnh liên tiếp.
Không tiết lộ kết quả nếu sự tò mò nằm ở kết quả đó.
Không dựng tình huống hoặc lời hứa trái với nội dung video.

2. NGUYÊN TẮC HÌNH ẢNH

Thumbnail phải gợi được câu chuyện ngay cả khi bỏ phần chữ.

Ưu tiên:
- Một nhân vật chính; tối đa hai nhân vật nổi bật.
- Một hành động hoặc một mối quan hệ rõ.
- Một đạo cụ quan trọng nếu cần để hiểu tình huống.
- Khuôn mặt lớn và biểu cảm dễ nhận ra.

Nếu có hai nhân vật, tạo sự đối lập cảm xúc phù hợp với kịch bản:
ngạc nhiên – thản nhiên, mong chờ – khó chịu, tự tin – bối rối,
hoặc một cặp cảm xúc khác thực sự có trong câu chuyện.

Nếu câu chuyện không phù hợp với biểu cảm cường điệu, dùng ánh mắt,
tư thế, khoảng cách hoặc đạo cụ để tạo tò mò.

Giữ nhất quán đặc điểm nhận diện theo ảnh hoặc mô tả nhân vật.
Không tự thêm nhân vật hay vật thể làm thay đổi ý nghĩa câu chuyện.

3. PHONG CÁCH THỊ GIÁC

Dùng phong cách comic 2D như mẫu tham chiếu:
- Đường nét đậm, sạch.
- Mảng màu rõ, có khối.
- Nhân vật tách biệt khỏi nền.
- Biểu cảm sinh động.
- Tương phản sáng tối mạnh.
- Chi tiết vừa đủ để đọc tốt trên màn hình nhỏ.

Có thể dùng tia sáng, mảng màu hoặc đường chuyển động để hướng mắt
vào điểm chính. Hiệu ứng phải hỗ trợ cảm xúc câu chuyện.

Không ép mọi câu chuyện dùng cùng một nền hoặc cùng một biểu cảm.

4. CHỌN NỘI DUNG CHỮ

Tự viết một câu móc ngắn, đúng với kịch bản:
- Ưu tiên khoảng 4–8 từ.
- Tối đa 2–3 dòng.
- Chỉ truyền đạt một ý.
- Có chi tiết cụ thể hoặc mâu thuẫn đáng chú ý.
- Không cần đọc tiêu đề video vẫn hiểu được.
- Không dùng câu gây sốc chung chung khi câu chuyện có chi tiết hay hơn.

Hình ảnh cho thấy tình huống.
Chữ bổ sung câu hỏi, mâu thuẫn hoặc góc nhìn khiến người xem tò mò.
Tránh để hình ảnh và chữ chỉ lặp lại cùng một thông tin.

Chọn một từ hoặc cụm từ quan trọng nhất để làm điểm nhấn.
Chỉ hiển thị câu chữ đã chọn; không thêm chú thích nhỏ hoặc đoạn văn.

5. FONT VÀ PHÂN CẤP CHỮ

Dùng một họ chữ display sans-serif siêu đậm, nét dày, hơi hẹp,
hỗ trợ đầy đủ dấu tiếng Việt.

- Chữ chính lớn, dễ đọc khi thu nhỏ.
- Từ khóa lớn hơn phần còn lại khoảng 1,2–1,4 lần.
- Tối đa hai cấp kích thước chữ.
- Có thể nghiêng nhẹ để tạo chuyển động, nhưng không làm khó đọc.
- Không kéo giãn hoặc bóp méo chữ.
- Không dùng font mảnh, quá cầu kỳ hoặc viết tay khó đọc.

Dùng viền tối và bóng cứng lệch nhẹ để tách chữ khỏi nền.
Viền không được làm bít lòng chữ hoặc mất dấu tiếng Việt.

6. MÀU SẮC

Chọn bảng màu phù hợp với cảm xúc câu chuyện và có tương phản mạnh.

Giữ:
- Một nhóm màu nền chủ đạo.
- Một màu nhấn cho từ khóa.
- Một màu chữ phụ.
- Viền tối giúp chữ dễ đọc.

Theo tinh thần mẫu 1:
- Trắng dùng cho phần chữ thông thường.
- Vàng chanh hoặc một màu sáng nổi bật dùng cho từ khóa.
- Tím than hoặc đen dùng cho viền và bóng.
- Băng màu tương phản có thể dùng cho một dòng nhấn.

Không bắt buộc mọi thumbnail đều phải vàng–đỏ.
Không dùng quá ba màu chữ chính.
Không đặt chữ sáng lên nền sáng mà thiếu lớp tách rõ.

7. BỐ CỤC VÀ VÙNG AN TOÀN

Nền phủ tràn toàn bộ khung hình.

Đặt toàn bộ thông tin quan trọng trong vùng giữa:
- 80% chiều rộng.
- 70% chiều cao.
Tương đương chừa khoảng 10% mỗi cạnh trái/phải và 15% trên/dưới.

Đây là vùng an toàn nội bộ để dự phòng cắt mép.
Nếu đầu vào có vùng cắt hoặc vùng giao diện che của nền tảng,
ưu tiên bố trí theo thông số thực tế đó.

Trong vùng an toàn phải có đầy đủ:
- Toàn bộ chữ, dấu và dấu câu.
- Mắt, miệng, biểu cảm chính.
- Đạo cụ hoặc chi tiết quyết định ý nghĩa tình huống.

Nền, hiệu ứng, tóc, vai và phần thân phụ có thể tràn ra ngoài.

Bố trí mặc định:
- Khối chữ ở phần trên của vùng an toàn.
- Nhân vật và hành động ở giữa và phía dưới.
- Khối chữ chiếm khoảng 30–35% chiều cao vùng an toàn.

Được thay đổi vị trí nếu giúp câu chuyện rõ hơn.
Không để chữ che biểu cảm hoặc đạo cụ quan trọng.
Chừa khoảng thở, không đặt chữ sát ranh giới vùng an toàn.

Thu gọn cả cụm nội dung vào giữa thay vì thu nhỏ mọi thứ.
Loại bớt chi tiết phụ để chữ và khuôn mặt vẫn đủ lớn.

8. KIỂM TRA CHẤT LƯỢNG

Trước khi hoàn thiện, kiểm tra:
- Có đúng một điểm thu hút chính không?
- Nhìn nhanh có nhận ra nhân vật và tình huống không?
- Chữ có bổ sung sự tò mò cho hình ảnh không?
- Câu chữ và hình ảnh có đúng nội dung video không?
- Khi thu ảnh còn khoảng 1/6 kích thước, chữ và cảm xúc có rõ không?
- Khi che thử các mép theo vùng an toàn, thông tin chính có còn nguyên không?
- Dấu tiếng Việt và đặc điểm nhân vật có chính xác không?

Nếu chưa rõ, giảm chi tiết, rút ngắn chữ hoặc điều chỉnh bố cục.
Không giải quyết bằng cách thêm chữ và thêm hiệu ứng.

ĐẦU RA
Một thumbnail hoàn chỉnh theo tỷ lệ yêu cầu.
Không tạo bảng nhiều phương án, không watermark, không logo tự thêm.
