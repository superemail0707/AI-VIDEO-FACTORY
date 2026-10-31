# Kế hoạch Phase 1 – Môi trường & đo đạc nền

| Hạng mục | Giá trị |
|---|---|
| Trạng thái kế hoạch | **Đã được Project Owner xác nhận ngày 2026-10-31** |
| Phạm vi cho phép | Bước 1.0 (lập danh sách, chỉ đọc tài liệu, không tải gì). Các bước sau mở từng bước, và **mỗi lệnh cài đặt hay tải model vẫn cần xác nhận riêng** |
| Commit, push | Không được phép khi chưa có chỉ đạo riêng |
| Quyết định liên quan | D-013 (phương pháp benchmark) và D-017 (không dùng công cụ không chính thức) đã `Approved`; Q-03 (có kiếm tiền, license phải cho phép thương mại); Q-06 (qua đêm, tối đa 4 giờ cho một video) |

**Mục tiêu:** thay giả định bằng số đo thật trên máy này, và kiểm chứng sớm rủi ro lớn nhất: giọng tiếng Việt (R1) và khả năng chịu tải, nhiệt (R2).

**Ngân sách thời gian:** mọi bài đo tuân theo giới hạn 4 giờ cho một video. Bài đo bền chạy tối đa 30 phút, khi cắm điện.

## Các bước

| Bước | Nội dung | Điều kiện sang bước sau |
|---|---|---|
| 1.0 | Danh sách ứng viên LLM, rasterize và TTS, kèm license của code, model và từng giọng. Chỉ giữ ứng viên cho phép thương mại và không thuộc diện bị loại theo D-017. **Chỉ đọc tài liệu, không tải gì** | Owner duyệt danh sách |
| 1.1 | Cài công cụ nền: Python môi trường riêng, FFmpeg, Ollama | Mỗi lệnh được Owner xác nhận |
| 1.2 | Benchmark: LLM với tiếng Việt, rasterize SVG, mã hóa `h264_videotoolbox` và `libx264`, faster-whisper; RAM đỉnh | Có số đo thô |
| 1.3 | Spike TTS: phát âm, độ tự nhiên, nhất quán, tốc độ, RAM, ít nhất hai hồ sơ nhân vật; **Owner nghe mù, chấm 1–5** | Owner chấm xong |
| 1.4 | Render bền 30 phút để xem giảm xung nhiệt | Có số đo nhiệt và thông lượng |
| 1.5 | Báo cáo `docs/testing/baseline-*.md` và `baseline-tts.md`; cập nhật ước tính "một video mỗi ngày" | Codex review, Owner nghiệm thu |

## Điều kiện bổ sung trước khi tải hoặc chạy (đề xuất của SG-002; Owner đã xác nhận điều 1–8 và bác điều 9, 2026-10-31)

Phần này là bổ sung của Claude trong phạm vi SG-002. **Ngày 2026-10-31 Owner trả lời "2G, 4C- xác nhận 1-8"**: điều 1–8 được xác nhận, điều 9 bị bác. Các điều đã xác nhận chỉ thắt chặt, không nới lỏng. Codex đã review ở RR-003 và coi đây là đề xuất chưa được Owner xác nhận.

1. **Ứng viên nhóm A** (xem `docs/testing/phase1-candidates.md`) chỉ được nghiên cứu: không tải, không chạy.
2. **Nhóm B** chỉ đủ điều kiện để Claude **đề xuất** Owner cho phép benchmark. Theo tiêu chuẩn S2 mà Owner chọn (điều 10), nhóm B hiện gồm Qwen3 4B và 8B `q4_K_M`; **Codex đã APPROVED phân loại (RR-005)**. Duyệt danh sách, quyền tải và quyền chạy là ba việc riêng: Owner đã duyệt vào danh sách **chỉ Qwen3 4B** (mã 1B, điều 11); quyền tải và đo thô 4B, 8B đã được Owner chỉ đạo riêng (xem `TASKS.md`); 8B chưa có câu duyệt vào danh sách.
3. Trước khi xin tải, hồ sơ phải ghi cho từng artifact: tên chính xác, URL kho và artifact, revision hoặc digest, quantization, voice ID nếu có, link license của mã và trọng số, license dữ liệu và phụ thuộc, điều kiện thương mại, dung lượng tải, ngày xác minh.
4. Phải đọc toàn văn tệp license của đúng artifact. Tóm tắt trang web là chưa đủ để chuyển một ứng viên sang nhóm B nếu có mắt xích dữ liệu hoặc phụ thuộc chưa rõ.
5. Mỗi lần tải: Owner duyệt đúng artifact, tag và dung lượng; Claude kiểm tra dung lượng trống; ghi SHA-256 hoặc digest của tệp đã tải; chỉ dùng tag tường minh (ví dụ `qwen3:4b-q4_K_M`, không dùng tag trơn).
6. Chạy tuần tự, một tác vụ nặng một lúc; giải phóng model sau mỗi bài đo; đo RAM đỉnh riêng từng bước; ngân sách 4 giờ áp dụng cho toàn bộ video.
7. Nhân bản giọng tắt. Không dùng audio tham chiếu của người thật khi chưa có bằng chứng đồng ý.
8. Không ứng viên nào được ghi "đạt" hay "vừa" nếu chưa có số đo thực.
9. ~~Nếu không có TTS tiếng Việt nào qua được bước đọc license gốc, dừng và báo Owner trước khi sang bước 1.1.~~ **BỊ BÁC (Owner, mã 2G, 2026-10-31).** Không còn hiệu lực: bước 1.1 và benchmark Qwen3 4B không bị chặn bởi R1. Quy định cũ của kế hoạch được giữ: nếu không có TTS tiếng Việt đủ điều kiện, báo Owner trước Phase 4 và 5 (R1 vẫn mở). Bỏ điều 9 **không** cấp quyền tải, cài hay chạy.
10. **Cách hiểu "chưa rõ" ở điều 4: Owner đã chọn S2 ngày 2026-10-31** (nguyên văn: "Chọn S2"). Dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận, **chỉ khi** ứng viên thỏa ba điều kiện của S2 tại `phase1-candidates.md` mục 7.1, và chỉ cho tiêu chuẩn phân loại. S2 không phải kết luận pháp lý, không phải duyệt danh sách, không phải quyền tải, cài hay chạy, và không áp dụng cho ứng viên có phát biểu mâu thuẫn hoặc nghi vấn cụ thể.

11. **Mã 1B (Owner, 2026-10-31, nguyên văn "1B, 2A, 4a, 4b"):** danh sách model hiện chỉ có Qwen3 4B `q4_K_M`, kèm rủi ro dư đã nêu ở `phase1-candidates.md` mục 4.1; Qwen3 8B chưa duyệt, chờ số đo 4B. Việc này **không** cấp quyền tải, cài hay chạy.

Các điều 1 đến 8 do Claude đề xuất và **đã được Owner xác nhận** (mã 4c); điều 9 **bị bác** (mã 2G). Điều 10 ghi nhận một quyết định của Owner (S2, nay là D-024) và điều 11 ghi nhận mã 1B. Không điều nào cấp quyền tải, cài hay chạy.

## Công nghệ

Chỉ dùng bộ đã duyệt: Python, Ollama, FFmpeg, faster-whisper, SVG kèm thư viện rasterize ứng viên, và các ứng viên TTS. Không thêm framework mới.

## Lệnh dự kiến và mức ảnh hưởng

| Lệnh | Ảnh hưởng | Ghi chú |
|---|---|---|
| Tạo môi trường Python riêng trong thư mục dự án | Nhẹ, chỉ ghi trong dự án | Python hệ thống là 3.9.6 (kiểm tra 2026-10-31), có thể quá cũ cho một số thư viện; nếu cần bản mới hơn sẽ là một lệnh cài đặt riêng, xin xác nhận |
| `brew install ffmpeg` | **Cài phần mềm hệ thống**, kèm thư viện phụ thuộc | FFmpeg chưa có trên máy |
| `brew install ollama` | **Cài phần mềm hệ thống**, có dịch vụ nền | Chưa có trên máy |
| `ollama pull <model>` | **Tải vài GB** | Chỉ sau khi Owner duyệt model ở bước 1.0 |
| Cài thư viện rasterize và TTS bằng pip | Nằm trong môi trường riêng | Tên gói xác minh ở bước 1.0, không đoán trước |

## File sẽ tạo hoặc sửa

- **Tạo:** tài liệu danh sách ứng viên; `docs/testing/baseline-*.md`, `docs/testing/baseline-tts.md`; mẫu âm thanh và kết quả thô ở `workspace/spikes/` (ngoài Git, đã được `.gitignore` chặn).
- **Sửa:** `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`, và `DECISIONS.md` nếu có quyết định mới.

## Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| Không có giọng tiếng Việt đủ tốt và đúng license (R1) | Spike sớm. Nếu không ứng viên nào đạt, dừng và báo Owner trước khi đầu tư Phase 4 và 5 |
| Giảm xung do nhiệt làm số đo ngắn đánh lừa (R2) | Bài đo bền 30 phút, khi cắm điện |
| Đầy ổ đĩa do tải model | Ghi dung lượng mỗi lần tải; trống khoảng 338 GiB (2026-10-31) |
| Ollama giữ model trong RAM | Giải phóng model giữa các bài đo |
| Chạy song song làm sai số đo | Chạy tuần tự |
| Repo công khai | Mẫu âm thanh và model không vào Git; báo cáo chỉ ghi model phần cứng, không ghi tên máy |

## Cách kiểm tra thành công

- Có số đo thô cho từng ứng viên, kèm lệnh, phiên bản và điều kiện (cắm điện, nhiệt).
- Bảng license có link và ngày kiểm tra cho từng model và giọng.
- Owner đã nghe mù và chấm điểm; không có điểm chất lượng nào do Claude tự đánh giá.
- Báo cáo nêu rõ điều gì đã đo, điều gì chưa.
- Codex review báo cáo; Owner nghiệm thu.

## Cách quay lại

- Môi trường Python riêng: xóa thư mục đó.
- Gói Homebrew: gỡ theo danh sách ghi lại ở bước 1.1.
- Model Ollama: xóa từng model đã tải.
- Không bước nào đụng tới code ứng dụng hay Git.
