# Phản hồi Review Kiến trúc của Codex

Tài liệu gồm các phần: **Phản hồi RR-005 (APPROVED) và bảng quyết định cuối cùng** (mới nhất), **Quyết định S2 và RR-005**, **Phản hồi RR-004 (APPROVED)**, **SG-002 vòng 1/3**, **SG-002 vòng 0/3**, **SG-001**, **Vòng 4**, **Vòng 3**, **Vòng 2** và **Vòng 1** (giữ nguyên làm lịch sử).

## SG-002 – Đã sửa P1-003 và P1-004 theo chỉ đạo "Cho sửa, không review" (2026-10-31)

**Trạng thái: `FIX IMPLEMENTED — NOT RE-REVIEWED`.** Không phải CLOSED. Owner chọn không nhờ Codex xác nhận; vòng 3/3 đã hết, không có vòng 4.

- **P1-003:** đã sửa các câu cũ: `phase1-candidates.md` dòng "chưa có danh sách nào được Owner duyệt" (nay: duyệt một phần, chỉ 4B); "chưa chọn hướng nào" (nay: đã chọn 2A); bảng S2 "Codex chưa re-review" (nay: APPROVED ở RR-005); mục 4.2 và bảng danh sách ghi 8B "chưa có câu duyệt vào danh sách", Owner chỉ cho phép tải (A06) và đo thô (A07); `PHASE-01-PLAN.md` điều 2 (ba việc riêng: duyệt danh sách, quyền tải, quyền chạy); `HANDOFF_TO_CHATGPT.md` dòng S2 (đã ghi D-024); câu "không có RR đang mở" của RR-005 ghi là lịch sử. Phần lớn lỗi còn lại của dòng REVIEW_RESPONSE cũ (RR-004, các phản hồi lịch sử) giữ nguyên làm lịch sử, mỗi phản hồi gắn với RR của nó.
- **P1-004:** `phase1-candidates.md` mục 4.8: tách "không có tệp LICENSE riêng" khỏi "có tuyên bố cấp phép trong README"; ghi phần chưa làm là lưu và đối chiếu toàn văn điều khoản README dẫn chiếu tại revision đã chốt; giữ nhóm A; hỏi tác giả không còn được ghi là cách duy nhất.
- **Chưa sửa (ngoài chỉ đạo hoặc allowlist):** `CURRENT_STATUS.md` (dòng Git cũ), mục lặp D-013/D-017 trong `DECISIONS.md`, nhãn A02–A07, xác nhận bằng văn bản quyền commit/push `9838f0a`.
- **Chưa commit.** Các thay đổi này là bản sửa sau RR-006, chưa được Codex review.

## SG-002 – Phản hồi RR-006 vòng 3/3 (cuối): CHANGES REQUESTED (2026-10-31)

**Nguồn:** báo cáo `# Review RR-006` ở đầu [PHASE-01-REVIEW.md](docs/operations/reviews/PHASE-01-REVIEW.md), kết luận **CHANGES REQUESTED — NEEDS REVISION** (không phải BLOCKED). Hai finding: P1-003 (MEDIUM), P1-004 (LOW). Claude không sửa báo cáo Codex.

**Kiểm tra khi nhận lại lượt (workflow mục 7):** đúng lượt của Claude; SG-002 `ACTIVE`; 8 hash nhóm A khớp RR-006 và `TASKS.md` phần trước `## Review Requests` khớp `a79d620b…`; `PHASE-01-REVIEW.md` 39,724 byte, 30,343 byte cuối khớp SHA-256 `9e3919e4…`; báo cáo mới ở đầu file, đúng một `# Review RR-006`; `PHASE-00-REVIEW.md` khớp; `git status --porcelain` chỉ có `HANDOFF_TO_CHATGPT.md`, `TASKS.md`, `PHASE-01-REVIEW.md`; HEAD vẫn `9838f0a`.

### Xác minh từng finding (Claude tự đọc lại trước khi trả lời)

| Finding | Xác minh | Trạng thái |
|---|---|---|
| P1-003 | **Đồng ý, đúng.** Tôi xác nhận: `phase1-candidates.md` dòng 23 còn ghi "chưa có danh sách nào được Owner duyệt" (mâu thuẫn mã 1B ở dòng 20, 38, 4.1); mục 7 dòng 232 còn ghi "chưa chọn hướng nào" dù mục 8 ghi đã chọn 2A; bảng S2 dòng 260 còn ghi "Codex chưa re-review" dù RR-005 đã APPROVED; `PHASE-01-PLAN.md` điều 2 còn ghi "chưa được Owner duyệt" trong khi điều 11 xác nhận duyệt 4B; handoff còn câu cũ về S2 chưa ghi `DECISIONS.md`; `REVIEW_RESPONSE.md` còn câu "không có RR đang mở" của RR-005. Lỗi của tôi: các câu cũ không được cập nhật khi thêm mã 1B, 2A, D-024 | `FIX NOT IMPLEMENTED — AWAITING OWNER` |
| P1-004 | **Đồng ý, đúng.** Tôi đọc lại [README VieNeu v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo/raw/main/README.md) (2026-10-31): license "áp dụng cho mọi artifact" gồm `model.safetensors`, ONNX và tài sản giọng; giọng cài sẵn dùng được cho nội dung kiếm tiền, không cần thêm license hay phí; có tuyên bố người nói đã cấp quyền và đồng ý (chỉ cho giọng cài sẵn). Dòng 162(c) đã ghi đúng ý này, nhưng dòng 162–163 kết luận "không có văn bản license để đọc cho đúng artifact" và "chỉ hỏi tác giả mới làm rõ" mạnh hơn bằng chứng. Cách nói chính xác: thiếu **tệp LICENSE riêng**, còn **tuyên bố cấp phép có trong README**; phần chưa có là toàn văn điều khoản README dẫn chiếu đối chiếu ở đúng revision, bằng chứng độc lập cho dữ liệu huấn luyện, phụ thuộc, consent, và mâu thuẫn "personal use" ở lộ trình GitHub. Nhóm A giữ nguyên | `FIX NOT IMPLEMENTED — AWAITING OWNER` |

**Lý do chưa sửa:** SG-002 đã dùng đủ vòng 0, 1, 2, 3. Workflow mục 9 ghi sau vòng 3 chưa PASS thì dừng và báo Owner; chỉ Owner quyết định tiếp tục, bằng chỉ đạo trực tiếp. Mọi bản sửa sẽ cần một vòng review mà SG-002 không còn. Claude không mở vòng 4, không đặt lại bộ đếm, không đóng SG-002 và không tự đóng finding.

**Hai finding chưa CLOSED** (chỉ báo cáo của Codex mới đóng được). Các phần Codex xác nhận: toàn vẹn mục 7 đạt; 1B, D-024, 2G/4c được ghi đúng; TTS chưa có ứng viên nhóm B; ViZipVoice giữ A; VietTTS và viXTTS giữ C; 12 mục `Proposed` giữ nguyên; không có câu coi nhóm B hay 1B là quyền chạy. Codex **không** đánh giá quyền của cài đặt, tải, benchmark, commit/push và nhãn A03–A07; báo cáo này không hợp thức hóa hay bác bỏ chúng.

**Việc cần Owner quyết định:** (1) có cho sửa P1-003, P1-004 không, và bằng hình thức nào (tiếp tục SG-002 với vòng bổ sung do Owner trực tiếp chỉ đạo, hay SG mới); (2) có nhờ Codex xác nhận bản sửa không; (3) chấp nhận hai điểm còn lại như rủi ro, nếu không sửa; (4) các điểm RR-006 đã nêu: nhãn A02–A07, xác nhận bằng văn bản quyền commit/push, dòng Git cũ trong `CURRENT_STATUS.md`, mục lặp D-013/D-017, đóng SG-002 (4e), 4d, chấm tiếng Việt.

## SG-002 – Câu trả lời của Owner "2G, 4C- xác nhận 1-8" (2026-10-31)

| Mã | Đã ghi | Hệ quả |
|---|---|---|
| 2G | Điều 9 của `PHASE-01-PLAN.md` bị bác | Bước 1.1 và benchmark Qwen3 4B không bị chặn bởi R1. R1 vẫn mở: báo Owner trước Phase 4 và 5 |
| 4c | Điều 1–8 được xác nhận | Là điều kiện bắt buộc trước mọi tải, cài, chạy |

**Không cấp quyền:** tải, cài, chạy (3a–3g chưa trả lời); 4d, 4e, 4f chưa trả lời. Mỗi lệnh vẫn cần xác nhận riêng. **Chưa đồng bộ:** `CURRENT_STATUS.md` còn ghi 2F/2G, 4c "chưa trả lời" vì A02 chỉ cho đồng bộ trạng thái của 1B/2A/4a/4b; cần Owner mở thêm Amendment. Codex chưa review phần này.

## SG-002 – Thực hiện câu trả lời của Owner "1B, 2A, 4a, 4b" (2026-10-31)

Không có Review Request mới; Codex chưa review phần này. Đây là thực hiện đúng bốn mã Owner trả lời, trong Amendment A02.

| Mã | Đã làm | Nơi ghi |
|---|---|---|
| 1B | Danh sách model chỉ có Qwen3 4B `q4_K_M`, kèm rủi ro dư; 8B hoãn tới khi có số đo 4B. Không cấp quyền tải, cài, chạy | `phase1-candidates.md` mục 1, 3, 4.1, 4.2; `PHASE-01-PLAN.md` điều 11 |
| 2A | Nghiên cứu tài liệu TTS tiếng Việt. VieNeu v3 Turbo: kho GitHub có LICENSE Apache-2.0 (chỉ cho mã), **kho Hugging Face của model không có tệp LICENSE**; giữ nhóm A. Thêm ViZipVoice (A), VietTTS và viXTTS (C, dựa trên tóm tắt tìm kiếm, chưa đọc toàn văn). **R1 chưa được giải quyết**. Không liên hệ ai, không tải, không chi tiền | `phase1-candidates.md` mục 4.8, 4.10 |
| 4a | D-024 (tiêu chuẩn S2) ghi vào mục "Đã duyệt" | `DECISIONS.md` |
| 4b | Đồng bộ `CURRENT_STATUS.md` (không gồm `CHANGELOG.md`) | `CURRENT_STATUS.md` |

**Chưa trả lời, Claude không tự quyết:** 2F/2G (Điều 9), 3a–3g, 4c, 4d, 4e, 4f. **Hash:** `DECISIONS.md` và `CURRENT_STATUS.md` đổi so với ảnh chụp RR-005 theo A02; `CHANGELOG.md`, `IMPLEMENTATION_PLAN.md` và `PHASE-01-REVIEW.md` không đổi. Vòng 3/3 của SG-002 chưa dùng.

## SG-002 – Phản hồi RR-005 vòng 2/3: APPROVED và bảng quyết định cuối cùng (2026-10-31)

**Nguồn:** báo cáo `# Review RR-005` trong [PHASE-01-REVIEW.md](docs/operations/reviews/PHASE-01-REVIEW.md), kết luận **APPROVED — PASS cho hồ sơ phân loại theo S2**. Kết luận thuộc về Codex; phần này chỉ ghi nhận. Codex không có finding mới; P1-001, P1-002 vẫn `CLOSED` theo RR-004.

**Kiểm tra khi nhận lại lượt (workflow mục 7):** đúng lượt của Claude; SG-002 `ACTIVE`; 9/9 hash nhóm A khớp RR-005; bốn file chỉ đọc không đổi; 21,512 byte cũ của báo cáo khớp SHA-256 bằng `tail -c`; phần mới 8,831 byte có đúng một báo cáo `# Review RR-005`; `PHASE-00-REVIEW.md` nguyên vẹn; không có nhóm C. SHA-256 chỉ chứng minh nội dung, không chứng minh ai viết phần mới.

RR-005 chuyển `ANSWERED` (lúc đó không có RR đang mở; **nay lịch sử**, xem RR-006 ở trên). Claude không đóng SG-002, không duyệt danh sách, không đổi phân loại.

### Điều APPROVED nói và không nói (theo Codex)

- **Chấp nhận:** Qwen3 4B và 8B `q4_K_M` ở nhóm B để **trình Owner**. Không chấp nhận diễn giải B là đã duyệt hay sẵn sàng chạy.
- **Chọn tiêu chuẩn S2 không thay việc Owner duyệt từng ứng viên và rủi ro dư kèm theo**; mọi phần chưa xác minh phải đi cùng hồ sơ trình Owner, không được đổi thành "đã đủ quyền thương mại".
- Codex đọc trực tiếp trang license blob của hai tag Ollama (blob `d18a5cc71b84`, hiển thị Apache License 2.0) và LICENSE Hugging Face của 4B tại revision đã ghi. **Bằng chứng mới này thuộc báo cáo của Codex; hồ sơ của Claude chưa nhúng nó.**
- Codex **lại không truy cập được** hai manifest registry Ollama, nên digest dài, config và model layer vẫn chỉ là lời Claude báo cáo. Không dùng báo cáo để xác nhận tệp tải về có đúng hash.
- Điều kiện (iii) "không có bằng chứng trái ngược" là kết quả có giới hạn, không phải bằng chứng vắng mặt tuyệt đối.

### Bảng quyết định cuối cùng trình Project Owner

Claude **không tự phê duyệt** mục nào. Các mục độc lập với nhau; bạn có thể trả lời theo mã (ví dụ "1A, 2B, 3 chưa, 4: có").

**1. Qwen3 4B và 8B nhóm B và rủi ro dư**

| Mã | Lựa chọn | Hệ quả |
|---|---|---|
| 1A | Duyệt **cả hai** artifact vào danh sách, kèm rủi ro dư ở bảng dưới | 8B có rủi ro bộ nhớ cao nhất với 16 GB; kế hoạch đã ghi đo 4B trước |
| 1B | Duyệt **chỉ 4B** `q4_K_M` bây giờ; 8B xét lại sau khi có số đo 4B | Claude khuyến nghị: ít rủi ro, khớp thứ tự đo đã ghi |
| 1C | Chưa duyệt | Nhóm B giữ nguyên là phân loại, không có gì để benchmark |

Rủi ro dư cần bạn chấp nhận **riêng cho từng artifact** nếu duyệt: dữ liệu huấn luyện không công bố; chưa biết commit Hugging Face nào là nguồn của GGUF; blob license 11,338 byte chưa so từng byte; manifest và digest dài chưa được xác nhận độc lập; "không tìm thấy bằng chứng trái ngược" là kết quả có giới hạn; tiếng Việt của Qwen3 chưa kiểm chứng; RAM runtime chưa đo. **Không có đánh giá mức độ rủi ro bằng số**; chỉ có thể nói rủi ro license phần còn lại là về nguồn dữ liệu huấn luyện, còn rủi ro vận hành chưa biết cho tới khi đo.

**2. Hướng xử lý TTS tiếng Việt** (hiện không ứng viên nào đủ nhóm B; R1 là rủi ro cao)

| Mã | Hướng | Ghi chú |
|---|---|---|
| 2A | Tiếp tục **nghiên cứu tài liệu**: đọc toàn văn license VieNeu v3 Turbo và tìm thêm ứng viên tiếng Việt | Không cần quyền mới; Claude khuyến nghị |
| 2B | Cho phép **liên hệ tác giả** VieNeu bằng văn bản về dữ liệu huấn luyện và quyền thương mại | Thông tin ra bên ngoài; cần bạn cho phép và duyệt nội dung thư |
| 2C | Cho phép xét **dịch vụ hoặc dữ liệu trả phí** | Hiện cấm; cần bạn duyệt chi phí |
| 2D | Giữ Phase 1 chỉ cho LLM và render, **hoãn TTS tiếng Việt** | Không giải quyết R1 |
| 2E | **Xem lại phạm vi tiếng Việt** trước Phase 4 và 5 | Thay đổi phạm vi sản phẩm |

Kèm theo: **điều 9 của `PHASE-01-PLAN.md`** (dừng trước bước 1.1 nếu không có TTS Việt đủ điều kiện) chặt hơn kế hoạch bạn đã xác nhận. Nếu giữ, mọi cài đặt bị chặn cho tới khi giải quyết TTS; nếu bác, benchmark Qwen3 và render có thể đi trước. Mã **2F: giữ điều 9** hoặc **2G: bác điều 9**.

**3. Quyền tải, cài, benchmark cần cấp riêng** (chưa cấp; mỗi lệnh xin xác nhận riêng)

| Mã | Quyền | Mức ảnh hưởng |
|---|---|---|
| 3a | Cài **Ollama** bằng Homebrew | Phần mềm hệ thống, kèm dịch vụ nền; chưa có trên máy; cách chạy dịch vụ sẽ nêu ở lệnh cụ thể |
| 3b | Tải `qwen3:4b-q4_K_M` | Khoảng 2.6 GB; tag tường minh; ghi lại digest sau khi tải |
| 3c | Tải `qwen3:8b-q4_K_M` | Khoảng 5.2 GB; chỉ sau khi 4B đo xong và còn chỗ |
| 3d | Chạy **benchmark Qwen3** | Đo RAM đỉnh, thời gian nạp, tốc độ, tiếng Việt, giải phóng model; tuần tự, cắm điện, trong ngân sách 4 giờ cho toàn video |
| 3e | Python mới hơn hoặc môi trường riêng | Python hệ thống là 3.9.6; chưa biết có cần không |
| 3f | Cài **FFmpeg** và các benchmark render | Thuộc bước 1.1 và 1.2, quyết định riêng |
| 3g | Lưu kết quả ở `workspace/` (ngoài Git) | Repo công khai; không đưa model hay mẫu âm thanh vào Git |

Tôi **không** xin quyền nào ở bảng này lúc này. Khi bạn cấp, tôi nêu lệnh chính xác, giải thích và chờ xác nhận trước từng lệnh.

**4. Quyết định và đồng bộ tài liệu còn tồn đọng**

| Mã | Việc | Ghi chú |
|---|---|---|
| 4a | Ghi quyết định **S2** vào `DECISIONS.md` | Cần quyền; hiện chỉ có trong `TASKS.md`, hồ sơ ứng viên, kế hoạch và handoff |
| 4b | **Amendment cho `CURRENT_STATUS.md`** (và `CHANGELOG.md` nếu muốn) | File đang lệch; Codex khuyến nghị đồng bộ trước khi dùng nó để duyệt danh sách hoặc giao thực thi |
| 4c | Xác nhận hoặc bác **điều 1 đến 9** của `PHASE-01-PLAN.md` | Hiện chỉ là đề xuất của Claude |
| 4d | Chuẩn hóa trường hợp reviewer artifact **"ABSENT"** trong workflow | Codex khuyến nghị; cần phạm vi riêng |
| 4e | **Đóng SG-002** hay giữ ACTIVE | Đã dùng vòng 0, 1, 2; còn một vòng cuối 3/3 |
| 4f | Cho phép **commit và push** | Nhiều tài liệu chưa vào Git (HEAD vẫn `e83ecec`); repo **công khai**; tôi quét secret trước khi commit |

Thứ tự gợi ý của Claude: 4b và 4a trước, để file trạng thái và quyết định khớp nhau; rồi 1, 2; rồi 3 khi sẵn sàng; 4f sau khi đồng bộ.

**Lượt thuộc về Owner** theo workflow mục 5.

## SG-002 – Quyết định S2 của Owner và RR-005 vòng 2/3 (2026-10-31)

**Quyết định:** trả lời câu hỏi chọn S1 hay S2 cho tiêu chuẩn nhóm B, Project Owner viết nguyên văn **"Chọn S2"**. Claude chép lại; hash không chứng minh được nguồn lời này.

**Cách Claude hiểu quyết định, hẹp nhất có thể:**

- S2 là tiêu chuẩn **phân loại**: dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận, chỉ cho ứng viên thỏa đủ ba điều kiện (i) đọc LICENSE đúng artifact và runtime, (ii) có revision hoặc digest và nêu phần chưa định danh, (iii) không có bằng chứng trái ngược.
- Không là kết luận pháp lý, không là duyệt danh sách model, không là quyền tải, cài, chạy, benchmark, commit, push, liên hệ ngoài hay chi phí.
- Không áp dụng cho TTS hay cho ứng viên có phát biểu mâu thuẫn hoặc nghi vấn cụ thể.
- Các giới hạn định danh và bất định đi cùng hồ sơ; Codex đã lưu ý điều này ở RR-004.

**Việc Claude làm (trong allowlist SG-002):** đối chiếu ba điều kiện cho từng ứng viên (`phase1-candidates.md` mục 7.1); **chỉ Qwen3 4B và 8B `q4_K_M` được chuyển lên nhóm B**, mọi ứng viên khác giữ nguyên (VieNeu v3 Turbo, Kokoro, Piper `ljspeech` vì có phát biểu mâu thuẫn hoặc nghi vấn; các ứng viên còn lại chưa được đánh giá theo S2); đồng bộ `PHASE-01-PLAN.md` điều 2 và 10, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`. Chưa ghi vào `DECISIONS.md` vì ngoài allowlist.

**Điểm Claude tự thấy yếu và đã ghi trong hồ sơ:** (i) mới đọc LICENSE qua công cụ web trả bản tóm tắt, và blob license 11,338 byte trong gói Ollama chưa so từng byte; (ii) Codex chưa xác nhận độc lập manifest Ollama và commit 4B (RR-004); (iii) "không tìm thấy bằng chứng trái ngược" là kết quả tìm kiếm có giới hạn, không phải bằng chứng vắng mặt. Tôi để Codex quyết định ba điểm này có đủ cho nhóm B không.

**Đã dùng vòng:** 0 và 1. RR-005 là vòng 2/3. Nếu Codex còn finding thì vòng 3/3 là vòng cuối, sau đó phải dừng và báo Owner.

**Bàn giao:** RR-005 trong `TASKS.md` (bản có hiệu lực). Claude không tự gọi Codex, không đánh dấu PASS.

## SG-002 – Phản hồi RR-004 vòng 1/3: APPROVED (2026-10-31)

**Nguồn:** báo cáo `# Review RR-004` trong [PHASE-01-REVIEW.md](docs/operations/reviews/PHASE-01-REVIEW.md), kết luận **APPROVED** (PASS cho hồ sơ nghiên cứu trong phạm vi re-review). Kết luận và việc đóng finding thuộc về Codex; phần này chỉ ghi nhận.

**Kiểm tra khi nhận lại lượt (workflow mục 7):** đúng lượt của Claude (RR-004 `OPEN`, đã có báo cáo cùng mã); SG-002 `ACTIVE`; 9/9 hash nhóm A khớp RR-004; bốn file chỉ đọc không đổi; 12,893 byte cũ của báo cáo khớp SHA-256 bằng `tail -c`; phần mới 8,619 byte có đúng một báo cáo `# Review RR-004`; `PHASE-00-REVIEW.md` nguyên vẹn; không có nhóm C. SHA-256 chỉ chứng minh nội dung, không chứng minh ai viết phần mới.

| Mã | Mức | Kết luận của Codex | Phản hồi của Claude |
|---|---|---|---|
| P1-001 | MEDIUM | **CLOSED** | Ghi nhận, không bất đồng |
| P1-002 | LOW | **CLOSED** trong phạm vi file được sửa | Ghi nhận, không bất đồng |

Không có finding mới. RR-004 chuyển `ANSWERED`; không có RR đang mở. **Chỉ báo cáo của Codex đóng finding**; Claude không đóng SG-002 và không đổi trạng thái ứng viên sang nhóm B.

### Điều APPROVED không có nghĩa

Codex nêu rõ đây **không phải** PASS về license thương mại cuối cùng, danh sách benchmark hay quyền thực thi. Nhóm B vẫn trống. Chưa có kết luận nào về RAM, tốc độ, tiếng Việt của Qwen3 hay mục tiêu 4 giờ.

### Giới hạn bằng chứng còn lại (theo Codex và Claude)

- **Digest Ollama và commit 4B chưa được xác nhận độc lập.** Codex xác nhận được commit Qwen3-8B (`b968826d...`, 2025-07-26) nhưng **không truy cập được** hai manifest registry Ollama và API Qwen3-4B. Khi nhận lại lượt tôi đọc lại cả ba nguồn và nhận đúng giá trị đã ghi, nhưng đó là **cùng một công cụ đọc lại, không phải xác nhận độc lập**. Hash này lấy từ registry, không phải tính lại từ weights đã tải.
- Hệ quả "Qwen3 đủ nhóm B nếu chọn S2" là **đánh giá có điều kiện của Claude**, không phải kết luận của reviewer. Nếu Owner chọn S2, các giới hạn định danh (commit Hugging Face so với blob GGUF, blob license chưa so từng byte) và quyền của phụ thuộc **phải đi cùng hồ sơ**, và quyết định phải được ghi rõ là **chấp nhận rủi ro**, không phải giữ nguyên S1.
- Không có TTS tiếng Việt nào đủ điều kiện nhóm B.

### `CURRENT_STATUS.md` đang lệch (ngoài allowlist)

`CURRENT_STATUS.md:25` còn ghi "Nhóm B: Qwen3 4B và 8B". Tôi không sửa vì file là nhóm A chỉ đọc. Codex khuyến nghị: **Owner nên cấp quyền đồng bộ trước khi dùng file này để duyệt danh sách hoặc giao tải, chạy.** `TASKS.md` có giá trị quyết định về lượt.

### Điểm cần Owner phê duyệt hoặc quyết định (độc lập với nhau)

| # | Việc | Ghi chú |
|---|---|---|
| 1 | **Chọn S1 hay S2** (`phase1-candidates.md` mục 7.1) | S2 chỉ đúng nếu bạn chấp nhận rủi ro dư bằng văn bản; sau đó Claude cập nhật nhóm và cần Codex re-review, và vẫn cần bạn duyệt danh sách |
| 2 | **Hướng TTS tiếng Việt** (mục 7) | Chưa có ứng viên nhóm B; liên hệ tác giả hay chi phí đều cần bạn cho phép riêng |
| 3 | **Xác nhận chín điều kiện bổ sung và điều 10** trong `PHASE-01-PLAN.md` | Hiện chỉ là đề xuất của Claude; điều 9 chặt hơn kế hoạch đã xác nhận (dừng trước bước 1.1 nếu không có TTS Việt đủ điều kiện) |
| 4 | **Duyệt danh sách model** | Chưa có gì để duyệt khi nhóm B trống |
| 5 | **Quyền tải, cài, chạy** từng bước | Độc lập với 1 đến 4 |
| 6 | **Mở Amendment cho `CURRENT_STATUS.md`** (và `CHANGELOG.md` nếu muốn) | Để hết lệch trạng thái |
| 7 | **Chuẩn hóa trường hợp reviewer artifact "ABSENT"** trong workflow | Codex khuyến nghị; cần phạm vi riêng |
| 8 | **Đóng SG-002** hay giữ ACTIVE | Chỉ Owner quyết định; đã dùng 1/3 vòng |
| 9 | **Commit và push** các thay đổi hiện có | Cần cho phép riêng; hiện nhiều tài liệu chưa vào Git |

**Lượt thuộc về Owner** theo workflow mục 5.

## SG-002 – Phản hồi RR-003 vòng 0/3 (2026-10-31)

**Nguồn:** báo cáo `# Review RR-003` trong [PHASE-01-REVIEW.md](docs/operations/reviews/PHASE-01-REVIEW.md) (file do Codex tạo; 12,893 byte khi Claude nhận lại lượt), kết luận **CHANGES REQUESTED**. Quyền ghi file này đến từ SG-002. Phần này không sửa báo cáo Codex và không đóng finding.

**Kiểm tra khi nhận lại lượt (workflow mục 7):** đúng lượt của Claude (RR-003 `OPEN`, đã có báo cáo cùng mã); SG-002 `ACTIVE`; 9/9 hash nhóm A khớp RR-003; `PHASE-00-REVIEW.md` giữ nguyên 57,209 byte; file nhóm B mới có đúng một báo cáo `# Review RR-003`; không có đường dẫn nhóm C. SHA-256 chỉ chứng minh nội dung, không chứng minh ai viết phần mới.

| Mã | Mức | Lập trường | Trạng thái |
|---|---|---|---|
| P1-001 | MEDIUM | Đồng ý | `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |
| P1-002 | LOW | Đồng ý | `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |

### P1-001 – Qwen3 nhóm B chưa đáp ứng tiêu chuẩn bằng chứng của chính hồ sơ

- **Nguyên nhân:** tôi đặt tiêu chuẩn "mắt xích dữ liệu hoặc phụ thuộc chưa rõ thì chưa đủ nhóm B" nhưng vẫn xếp Qwen3 vào B dù dữ liệu huấn luyện không công bố và chưa đọc LICENSE; còn TTS bị giữ A vì cùng loại bất định. Không có tiêu chí phân biệt.
- **Bằng chứng đã bổ sung (đọc 2026-10-31):** LICENSE của [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B/raw/main/LICENSE) và [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B/raw/main/LICENSE) là Apache License 2.0; [LICENSE của Ollama](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE) là MIT. Commit đầu kho Hugging Face (4B `1cfa9a72...`, 8B `b968826d...`), digest manifest và model layer của hai artifact Ollama đã ghi vào `phase1-candidates.md` mục 4.1, 4.2. Công cụ trả về bản tóm tắt, không phải tệp nguyên văn, và digest chưa tự tính lại từ tệp tải về.
- **Phần chưa định danh, nêu chính xác:** commit Hugging Face nào là nguồn của blob GGUF trên Ollama; blob license 11,338 byte của Ollama chưa so từng byte với LICENSE Hugging Face.
- **Xử lý:** theo hướng Codex đề ra, **chuyển Qwen3 4B và 8B về nhóm A**; nhóm B hiện trống. Điều này làm tiêu chuẩn và phân loại nhất quán, **không nới tiêu chuẩn**. Thêm mục 7.1 với hai phương án để Owner quyết định (S1 nghiêm ngặt, S2 rủi ro dư có văn bản); Claude không tự áp dụng S2. Thêm điều 10 vào `PHASE-01-PLAN.md`, ghi là đề xuất chưa được Owner xác nhận.
- **Không kết luận Qwen3 cấm thương mại:** hồ sơ nói rõ không tìm thấy điều khoản cấm. Vấn đề chỉ là quy trình xác minh theo tiêu chuẩn của chính hồ sơ.

### P1-002 – Trạng thái bàn giao và cổng kế hoạch mâu thuẫn

- **Nguyên nhân:** tôi sửa `REVIEW_RESPONSE.md` và phần đầu `HANDOFF_TO_CHATGPT.md` khi gỡ BLOCKED nhưng bỏ sót `phase1-candidates.md` dòng 5 và cuối handoff; dòng 11 của handoff còn ghi kế hoạch Phase 1 là điều kiện chờ dù đã được xác nhận.
- **Xử lý:** đồng bộ `phase1-candidates.md` (trạng thái, danh sách việc đang chờ), `HANDOFF_TO_CHATGPT.md` (dòng cổng đầu vào, SG-002, RR-003, RR-004, lượt, Git, bước tiếp theo). Phát hiện thêm lúc sửa: handoff còn ghi `main` ở `fb3a19f` và "working tree sạch", trong khi HEAD là `e83ecec` và còn thay đổi chưa commit; đã sửa. Mô tả BLOCKED cũ giữ lại ở mục "Bàn giao: BLOCKED" bên dưới, có đánh dấu là lịch sử trước Amendment A01.
- **Các việc chờ được tách riêng:** Codex re-review; Owner quyết định tiêu chuẩn nhóm B; Owner chọn hướng TTS tiếng Việt; Owner duyệt danh sách; quyền tải, cài, chạy từng bước.

### Điều chưa xử lý được trong phạm vi SG-002

- `CURRENT_STATUS.md` là nhóm A **chỉ đọc** nên tôi không sửa, và nó đang **lệch**: còn ghi "Nhóm B: Qwen3 4B và 8B" và một số trạng thái lượt cũ. `TASKS.md` có giá trị quyết định về lượt. Cần Owner mở Amendment nếu muốn đồng bộ file này.
- Chưa giải quyết: trường hợp reviewer artifact chưa tồn tại (Codex khuyến nghị chuẩn hóa ABSENT trong workflow). Nằm ngoài allowlist, chờ Owner cấp phạm vi.
- Vẫn chưa xác minh: toàn văn LICENSE của các ứng viên khác, tiếng Việt của Qwen3, RAM runtime, bất kỳ hiệu năng nào. Chưa có TTS tiếng Việt nào đủ điều kiện nhóm B.

**Bàn giao:** RR-004 (vòng 1/3, tiếp nối RR-003) trong `TASKS.md`. Bản có hiệu lực chỉ nằm ở đó; phần này không phải RR thứ hai. Claude không tự gọi Codex.

## SG-002 – Hồ sơ ứng viên Phase 1.0 (2026-10-31)

**Quyền ghi:** file này nằm trong allowlist của SG-002 do Project Owner cấp.

*Phần dưới đây là phản hồi vòng 0/3 cho tình trạng trước Amendment A01 và chỉ giữ làm lịch sử; trạng thái hiện hành nằm ở phần "Phản hồi RR-003" ngay trên.*

**Cập nhật (2026-10-31): hết BLOCKED.** Project Owner chọn lựa chọn 2, bổ sung bốn file vào SG-002 làm nhóm A chỉ đọc (Amendment A01). Claude đã đăng **RR-003**, vòng 0/3, trong `TASKS.md`. Chưa có kết luận review nào của Codex cho Phase 1. Mục "Bàn giao: BLOCKED" bên dưới giữ làm lịch sử về tình trạng trước khi có Amendment A01.

### Nguồn yêu cầu

- Báo cáo pre-approval review của Codex (kết luận `NEEDS REVISION — NOT READY FOR OWNER APPROVAL`) **không có trong repo**: không có `docs/operations/reviews/PHASE-01-REVIEW.md`, và `PHASE-00-REVIEW.md` không chứa báo cáo Phase 1. Tôi chỉ có danh sách yêu cầu do Owner chuyển trong chat. Vì vậy chưa thể đối chiếu từng finding gốc theo mã.
- Không đánh dấu finding nào là `CLOSED`. Chỉ Codex đóng được finding.

### Đối chiếu danh sách yêu cầu của Owner

| Yêu cầu | Xử lý | Vị trí |
|---|---|---|
| Tách A, B, C | Có | `phase1-candidates.md` mục 3 |
| Bảng thông tin bắt buộc cho từng ứng viên (tên, vai trò, URL, artifact, revision, quantization, voice ID, license mã/trọng số/dữ liệu/phụ thuộc, thương mại, RAM và disk, nhóm, chưa xác minh, ngày) | Có, mục 4.1 đến 4.10 | – |
| Piper `vais1000`: model card, dữ liệu, lessac, chuỗi quyền | Loại (nhóm C): tinh chỉnh từ lessac, dữ liệu Blizzard 2013 chỉ cho nghiên cứu | mục 4.3 |
| VieNeu-TTS: phân biệt 0.3B và v3 Turbo, codec, giọng | 0.3B và 0.5B loại (dữ liệu CC BY-NC); v3 Turbo nhóm A | mục 4.7, 4.8 |
| Piper tiếng Anh: giọng cụ thể | Có: `ljspeech` nhóm A; `lessac`, `hfc_*`, `libritts_r` nhóm C | mục 4.4, 4.5 |
| Kokoro: revision, voice, phụ thuộc | Nhóm A; revision gốc không hiển thị, ghi SHA-256 model và 54 giọng | mục 4.9 |
| Qwen3: đúng 4B/8B, tag, quantization; RAM không suy từ dung lượng tải | Nhóm B, tag tường minh; RAM ghi "chưa có nguồn" | mục 4.1, 4.2, 5 |
| Voice cloning mặc định tắt | Ghi ở mục 2 và từng ứng viên | – |
| MacBook Air M4 16 GB, tuần tự, ngân sách 4 giờ cho toàn video | Mục "Mô hình tuần tự" (cách đo, không có số) | mục 5 |
| Bốn trạng thái độc lập | Mục 1 | – |

### Chưa xác minh được

- Toàn văn LICENSE của từng artifact (mới đọc tóm tắt trang); revision gốc của Qwen3 và Kokoro; tiếng Việt của Qwen3; RAM runtime của mọi ứng viên; điều khoản nhà cung cấp TTS đóng trong dữ liệu Kokoro; câu "personal use" của Piper và lộ trình "personal use" của VieNeu.
- **Không có TTS tiếng Việt nào đủ điều kiện nhóm B.**

### Bàn giao: BLOCKED

Kiểm tra theo `AI_REVIEW_WORKFLOW.md` mục 7 cho thấy RR lúc này sẽ **thất bại ở bước kiểm tra của Codex**, vì vậy tôi **không** đăng RR đang `OPEN`.

| Điều kiện | Kết quả |
|---|---|
| HEAD | `e83ecec`, trùng `origin/main` |
| SG-001 `DONE`, RR-002 `ANSWERED`, không RR `OPEN` | Đạt |
| SG-002 `ACTIVE` | Đạt |
| Đường dẫn trong `git status` thuộc nhóm A hoặc B | **KHÔNG ĐẠT:** `CHANGELOG.md`, `CURRENT_STATUS.md`, `DECISIONS.md`, `IMPLEMENTATION_PLAN.md` đang khác HEAD và **nằm ngoài allowlist SG-002**, nên là nhóm C. Chúng được sửa ở các lượt trước theo chỉ đạo của Owner (D-013, D-017, Q-03, Q-06, xác nhận kế hoạch Phase 1) |
| Reviewer artifact | `docs/operations/reviews/PHASE-01-REVIEW.md` **chưa tồn tại**. Mẫu RR của workflow chỉ nêu số byte và hash của file đã có; workflow chưa quy định trường hợp file chưa tồn tại |

**Điều kiện Owner cần giải quyết, chọn một trong hai:**

1. **Cho phép commit** các thay đổi hiện có (gồm bốn file nhóm C) làm mốc sạch. Khi đó RR dùng commit ID làm phiên bản review, không còn nhóm C. Commit cần Owner cho phép riêng; SG không cấp quyền này.
2. **Bổ sung vào SG-002** bốn file trên làm nhóm A (chỉ đọc, giữ nguyên hash) để Codex coi là đã khai báo.

Ngoài ra, nên làm rõ một trong hai: Codex tạo `PHASE-01-REVIEW.md` với đúng một báo cáo đầu tiên (RR khi đó ghi "file chưa tồn tại, kỳ vọng tạo mới"), hoặc Owner chỉ định cách khác. Sửa workflow cho trường hợp này nằm ngoài allowlist SG-002.

**Không tự gọi Codex:** không có công cụ gọi chéo được kiểm chứng.

## SG-001 – Phản hồi RR-002 vòng 1/3 (2026-10-30)

**Nguồn:** báo cáo `# Review RR-002` trong [PHASE-00-REVIEW.md](docs/operations/reviews/PHASE-00-REVIEW.md), kết luận **APPROVED**. Kết luận và việc đóng finding thuộc về Codex; phần này chỉ ghi nhận.

| Mã | Kết luận của Codex | Phản hồi của Claude |
|---|---|---|
| F-001 | **CLOSED** | Ghi nhận, không có bất đồng |
| F-002 | **CLOSED** | Ghi nhận, không có bất đồng |

Không có finding mới. RR-002 chuyển `ANSWERED`. Không có RR đang mở.

**Claude đã kiểm tra khi nhận lại lượt:** 9/9 hash nhóm A khớp RR-002; 51118 byte cũ của báo cáo khớp SHA-256 bằng `tail -c`; phần mới 6091 byte có đúng một báo cáo `# Review RR-002`; không có đường dẫn nhóm C. SHA-256 không chứng minh ai đã viết phần mới.

**Sau khi có APPROVED:** chỉ cập nhật trạng thái trong `TASKS.md` (phần sau `## Review Requests`), `REVIEW_RESPONSE.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`. Các file đã review khác giữ nguyên hash. Vì vậy dòng trạng thái ở `AI_REVIEW_WORKFLOW.md:7` vẫn ghi chờ Codex.

**Không thực hiện:** đóng SG-001, nghiệm thu workflow, commit, push, chuyển phase. Những việc đó thuộc Project Owner.

## SG-001 – Phản hồi RR-001 vòng 0/3 (2026-10-30)

**Nguồn:** báo cáo `# Review RR-001` trong [PHASE-00-REVIEW.md](docs/operations/reviews/PHASE-00-REVIEW.md), kết luận **CHANGES REQUESTED**. Quyền ghi file này đến từ SG-001 Amendment A01 do Project Owner phê duyệt. Phần này không sửa báo cáo Codex và không đóng finding.

| Mã | Mức | Lập trường | Trạng thái |
|---|---|---|---|
| F-001 | MEDIUM | Đồng ý, đã tự xác minh | `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |
| F-002 | MEDIUM | Đồng ý, đã tự xác minh | `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` |

### F-001

- **Nguyên nhân:** mục 7 của workflow dùng một allowlist cho toàn bộ working tree, nên báo cáo hợp lệ của Codex bị coi là thay đổi ngoài phạm vi. Mục 7 cũng vừa bảo dừng, vừa gọi trường hợp đó là finding.
- **Biện pháp:** chia file thành ba nhóm A (Claude-owned), B (Codex-owned review artifact), C (Unrelated). Nhóm A đối chiếu SHA-256. Nhóm B ghi số byte và SHA-256 lúc bàn giao, và sau báo cáo phải chứng minh nội dung cũ còn nguyên, có đúng một báo cáo mới cùng mã RR. Nhóm C luôn dừng. Làm rõ: nội dung sai trong nhóm A là finding; đường dẫn nhóm C là lỗi đầu vào.
- **Không nới lỏng:** không có cơ chế bỏ qua working tree. Không mặc định tin file nhóm B. Hash không khớp vẫn dừng.
- **Giới hạn:** SHA-256 không chứng minh ai đã sửa file. Kiểm tra chứng minh nội dung cũ còn nguyên, không chứng minh phần mới do Codex viết.

### F-002

- **Nguyên nhân:** mục 9 bắt buộc ghi `REVIEW_RESPONSE.md`, trong khi SG-001 cấm file này. Tôi đã nêu rủi ro này khi bàn giao RR-001.
- **Biện pháp:** Project Owner cấp quyền qua Amendment A01, chỉ để phản hồi finding và tạo Review Request. Workflow ghi rõ: file ngoài allowlist thì dừng xin Owner; chỉ báo cáo Codex mới đóng được finding; sau PASS, file ngoài allowlist như `CURRENT_STATUS.md` không bị ghi mà được nêu trong tóm tắt.

### File đã sửa trong vòng này

| File | Phần sửa |
|---|---|
| `TASKS.md` | Thêm Amendment A01; RR-001 thành `ANSWERED`; đăng RR-002 |
| `docs/operations/AI_REVIEW_WORKFLOW.md` | Mục 3, 4, 6, 7, 9, 10, 11, 13; bảng trạng thái; sửa tham chiếu mục ở bảng luồng |
| `AGENTS.md`, `CLAUDE.md` | Làm rõ reviewer artifact, giới hạn SHA-256, điều kiện dừng |
| `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md` | Ghi nhận thay đổi |
| `REVIEW_RESPONSE.md` | Phần này |

`docs/operations/README.md` và `docs/workflows/README.md` không đổi so với RR-001, nhưng vẫn khác baseline Git nên nằm trong snapshot.

### Bằng chứng đã chạy

| Kiểm tra | Kết quả |
|---|---|
| Phân loại `git status --porcelain` | 8 đường dẫn nhóm A, 1 nhóm B, 0 nhóm C (trước khi sửa `REVIEW_RESPONSE.md`) |
| Báo cáo RR-001 so với baseline Git | 42994 byte cũ khớp SHA-256 ở cuối file; `git diff --numstat` là +50, −0; có một tiêu đề `# Review RR-001` |
| Thử chuẩn trên bản sao tạm: thêm báo cáo lên đầu | Được chấp nhận |
| Thử phủ định trên bản sao tạm: sửa kết luận cũ | Bị từ chối, hash khác |
| Trường Amendment A01 | Đủ 8 trường, mỗi trường 1 lần; vẫn 1 SG |
| Liên kết, chuỗi giống secret | 0 liên kết hỏng, 0 file khớp mẫu |
| File được bảo vệ | Không có diff ở `DECISIONS.md`, `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `TECH_STACK.md`, `CURRENT_STATUS.md`, `IMPLEMENTATION_PLAN.md`, `.gitignore`, `REVIEW_REPORT.md` |

Lần chạy đầu của bước phân loại, liên kết và secret bị lỗi cú pháp shell nên không được dùng; kết quả trên là lần chạy lại.

### Chưa thể kiểm chứng

- Chưa hoàn tất vòng FIX → RE-REVIEW thực tế; đây là lần đầu dùng quy tắc nhóm A, B, C.
- Không xác minh được ai đã sửa file.
- Chưa có commit theo từng vòng, nên bằng chứng dựa trên SHA-256 và bàn giao tuần tự.
- `CURRENT_STATUS.md:21` vẫn ghi lượt là Chủ dự án vì file ngoài SG-001; `TASKS.md` có giá trị quyết định.

### Review Request RR-002: bản đối chiếu

**Bản có hiệu lực nằm ở `TASKS.md`, mục `## Review Requests`.** Phần này chỉ là bản đối chiếu, không phải yêu cầu thứ hai. Hash của chính `REVIEW_RESPONSE.md` chỉ có trong `TASKS.md`.

- Scope Grant: SG-001
- Amendment: A01
- Review Request: RR-002, tiếp nối RR-001
- Vòng: 1/3
- Previous review: vòng 0/3, RR-001, CHANGES REQUESTED
- Findings: F-001, F-002
- Baseline Git: def8fdf0b7871abada7dad228e31c1ee96dae7b3
- SHA-256 (nhóm A):
  - `AGENTS.md` 599da96de01f938e589341f529ef891fecf6a17e11c6c11dc6928ee7e27d351a
  - `CHANGELOG.md` d614efc545bcc0aa7e2e5da279470c7a47cfeed57dc122d165902ddbf0a0186e
  - `CLAUDE.md` dfabb9407e1e4e6e8e131170709800035df0a465c56826b601422f5922d083e4
  - `HANDOFF_TO_CHATGPT.md` bf528c532f3356ffa3b1fb160e844273c9841f593b202b993f4420480fc1a2b2
  - `docs/operations/AI_REVIEW_WORKFLOW.md` 90305710bd3cedda08534e6d99db8283dea9388fab2f42c350cba2c310b394fc
  - `docs/operations/README.md` 039a53b45de3b87bbe82d60f96d1af338180015e326c9f15b42d98314f7564cd
  - `docs/workflows/README.md` 75b3b3ec997b2acba1000bdee8d90497c3adac7d546aebd68180b6a384013e0f
  - `TASKS.md` (phần trước `## Review Requests`) b7b81a64b8164557c503fa9677a8aec4ef7f566711afb79838983d3b2d109a7e
- Reviewer artifact (nhóm B) lúc bàn giao:
  - `docs/operations/reviews/PHASE-00-REVIEW.md` 51118 b89b19418301f1ebe577e5928d19ec0a1795ad2fc9096eec55937e204cc10944
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-002` mới ở đầu file; toàn bộ nội dung cũ giữ nguyên
- Lệnh đã chạy và kết quả thật: xem mục "Bằng chứng đã chạy" ở trên
- Chưa kiểm tra được: xem mục "Chưa thể kiểm chứng" ở trên
- Mục tiêu re-review: xác minh F-001, F-002 và hồi quy liên quan
- END-OF-REVIEW-REQUEST

---

## Vòng 4 – Ghi nhận D-023 và khắc phục R4-01 (2026-10-30)

**Nguồn:** [docs/operations/reviews/PHASE-00-REVIEW.md](docs/operations/reviews/PHASE-00-REVIEW.md), Review lần 4, kết luận **APPROVED WITH CHANGES** chỉ cho hồ sơ Phase 0.

| Mã | Mức | Lập trường | Xử lý | Trạng thái |
|---|---|---|---|---|
| R4-01 | LOW | **Đồng ý.** Lỗi nằm ở cách viết của tôi: `IMPLEMENTATION_PLAN.md` ghi "không viết adapter khi chưa có quyết định D-023", nên khi D-023 được duyệt, câu đó đọc ngược thành được viết. `publishing-reliability.md` có hai dòng cùng logic | Bỏ các câu đó. Tách Decision status và integration status. Định nghĩa `POLICY BLOCKED` và cổng G1–G5 tại một nơi chuẩn; tài liệu khác tham chiếu tới đó | **FIX IMPLEMENTED IN DOCUMENTATION — PENDING CODEX RE-REVIEW** |

**Đối chiếu ba điều kiện trình nghiệm thu của Codex:**

| # | Điều kiện | Tình trạng |
|---|---|---|
| 1 | Chủ dự án quyết định D-023/Q-13; nếu chấp nhận rủi ro, ghi rõ Direct Post không được triển khai khi chưa có phương án hợp lệ | Đã ghi nhận |
| 2 | Làm rõ R4-01, giữ cổng chính sách độc lập với phê duyệt nội bộ | Đã sửa, chờ Codex kiểm tra lại |
| 3 | Chủ dự án quyết định nghiệm thu Phase 0 | Chờ. **Phase 0 chưa được nghiệm thu** |

**R3-01:** không đóng. Quyết định D-023 xử lý cấp sản phẩm, còn rủi ro chính sách vẫn còn, thể hiện bằng `POLICY BLOCKED`.

**Khác biệt so với snapshot Review 4:**

- Review 4 ghi không có remote; hiện `git remote -v` cho thấy `origin`. Tôi không tạo remote này, và không đọc hay thay đổi nó.
- Ba file ngoài danh sách được phép vẫn còn cách viết cũ, xem mục dưới.

**Chưa sửa vì ngoài phạm vi được giao, cần Project Owner chỉ đạo:**

| Vị trí | Nội dung cũ | Ảnh hưởng |
|---|---|---|
| `PROJECT_MASTER.md:28` | "Mục tiêu giữ nguyên cho tới khi Chủ dự án quyết định" | Lỗi thời; không gợi ý mở khóa |
| `TECH_STACK.md:63` | "Bị chặn, chờ D-023" | Lỗi thời; vẫn ghi bị chặn |
| `docs/requirements/README.md:24` | "Bị chặn, chờ D-023" | Lỗi thời; vẫn ghi bị chặn |

Cả ba vẫn nói đúng rằng TikTok bị chặn, nên không tạo đường mở khóa. Nhưng "chờ D-023" có thể gợi ý D-023 sẽ gỡ chặn; nên đổi sang `POLICY BLOCKED` khi được cho phép.

---

## Vòng 3 – Bản sửa 3 (2026-10-30)

**Nguồn:** [docs/operations/reviews/PHASE-00-REVIEW.md](docs/operations/reviews/PHASE-00-REVIEW.md), kết luận **CHANGES REQUESTED**. Tài liệu này không đóng kết luận đó; chỉ Chủ dự án quyết định.

| Mã | Mức | Lập trường | Xử lý | Trạng thái |
|---|---|---|---|---|
| R3-01 | HIGH | **Đồng ý.** Tôi tự đọc lại mục Intended Use và xác nhận. Bỏ sót của tôi: Bản sửa 2 đã đọc trang này nhưng chỉ ghi nhận yêu cầu về giao diện | Ghi rõ Direct Post bị chặn và audit không đủ để mở khóa. Chặn adapter ở Phase 16. Thêm rủi ro R13, D-023, Q-13 với ba lựa chọn | **Đã ghi nhận trong tài liệu; chưa giải quyết. Chờ Chủ dự án quyết định** |
| R3-02 | MEDIUM | **Đồng ý.** Đặc tả của tôi mâu thuẫn thật | `pending_outcome` có hai loại. `success` cần manifest và checksum; `failure` cần dữ liệu lỗi hợp lệ, không cần artifact. Cả hai đều fencing và idempotent. Thêm T11a–c, AC-Q18, FI-44 đến FI-49 | Đã đặc tả; `Proposed`; chưa triển khai; chưa kiểm thử |
| R3-03 | LOW | **Đồng ý** | Phát hiện và dịch lịch ở mỗi chu kỳ khi Worker đang sống; thêm bước kẹp không phụ thuộc phát hiện. FI-32 cấm khởi động lại. Thêm AC-Q19, FI-50, FI-51 | Đã đặc tả; `Proposed`; chưa triển khai; chưa kiểm thử |

**Ghi chú về R3-01.** Trang Upload vào inbox không nói gì về intended use hay audit, nên luồng đó **chưa xác minh**, không được coi là đường đi đã mở. Khuyến nghị của tôi là lựa chọn A cộng B, nhưng đây là thay đổi với mục tiêu sản phẩm đã duyệt, nên tôi không tự áp dụng.

**Ngoài phạm vi vòng này, giữ làm việc mở** (mục "Chưa thể xác minh" của Codex):

- FI-43 chỉ kiểm tra đã gửi yêu cầu giải phóng model, chưa chứng minh tác vụ trong daemon Ollama đã kết thúc. Cần bổ sung trước khi tuyên bố bất biến không chồng tải.
- `flock` qua FFmpeg, độ bền `F_FULLFSYNC`, cách ly Keychain giữa các tiến trình cần bằng chứng khi triển khai.
- Facebook App Review vẫn chưa xác minh.

---

## Vòng 2 – Bản sửa 2 (2026-10-30)

**Nguồn phát hiện:** danh sách do Chủ dự án chuyển trong yêu cầu "Final Documentation Revision". **Repo không có tệp báo cáo gốc của vòng 2;** `REVIEW_REPORT.md` vẫn là bản vòng 1. Vì vậy các mã dưới đây do tôi đặt theo mục B–I của yêu cầu. Nếu báo cáo gốc có phát hiện khác, phần này chưa phản hồi các phát hiện đó.

**Quy ước trạng thái.** Mọi mục đặc tả có cùng trạng thái: tài liệu xong; thiết kế `Proposed`; chờ Chủ dự án duyệt; chưa triển khai; chưa kiểm thử. Bảng dưới chỉ nêu ngoại lệ.

**Blueprint:** giữ nguyên. Không thêm Agent, không đổi bộ công nghệ, không có code.

### B. `.gitignore`

**Đây là lỗi của tôi và tự kiểm tra của tôi đã bỏ sót.** Quy tắc `!tests/fixtures/**` đứng sau quy tắc secret nên bỏ chặn cả secret. Bản sửa 1 còn báo `tests/fixtures/a.wav` "tracked" như một kết quả đạt mà không thử secret trong thư mục đó.

| Mã | Yêu cầu | Xử lý | Trạng thái |
|---|---|---|---|
| B-1 | Bỏ phủ định rộng | Chặn mặc định trong `tests/fixtures`, chỉ cho phép 7 định dạng văn bản | **Đã sửa, đã xác minh** |
| B-2 | Secret, token bị chặn trong fixtures | Khối secret đặt cuối tệp để luôn thắng; thêm `*.env` và lọc theo tên | **Đã sửa, đã xác minh** |
| B-3 | DB, model, media bị chặn | Không có ngoại lệ nhị phân; media được sinh lúc test | **Đã sửa, đã xác minh** |
| B-4 | Fixture hợp lệ vẫn theo dõi được | 13/13 đường dẫn, và repo thử thật | **Đã sửa, đã xác minh** |
| B-5 | Ghi lệnh và kết quả | Phụ lục 2 của báo cáo Phase 0 | **Đã ghi** |

**Giới hạn:** tên tệp không phải cách phát hiện nội dung. Một secret nằm trong `tests/fixtures/data.json` vẫn theo dõi được. Quét secret trước commit vẫn cần thiết.

### C. `SQLITE_BUSY`

| Mã | Yêu cầu | Xử lý | Vị trí |
|---|---|---|---|
| C-1 | Retry có giới hạn, backoff | `busy_timeout`, 8 lần thử, backoff có trần | `queue-safety.md` mục 7, 10.2 |
| C-2 | Khi hết ngân sách | Ghi `pending_outcome`, tạm dừng hàng đợi, có giới hạn | Mục 10.3 |
| C-3 | Requeue hay dừng | **Dừng để phục hồi, không requeue.** Requeue cần đúng khóa đang bị chặn và bỏ phí kết quả | Mục 10.3 |
| C-4 | Kiểm tra generation và quyền | Mỗi lần thử là transaction mới, chạy lại fencing; commit idempotent | Mục 5, 10.2 |
| C-5 | Không kẹt `running` vĩnh viễn | Bảng ba tình huống, nêu rõ hai giới hạn thật | Mục 10.6 |
| C-6 | Phân biệt tranh chấp và lỗi job | Theo mã lỗi; tiến trình con không chạm DB | Mục 10.1 |
| C-7 | Chuyển trạng thái, audit | Bảng T1–T10; nhật ký khi DB không ghi được | Mục 10.5 |
| C-8 | Không báo thành công giả | AC-Q10 | Mục 10.5, 12 |
| C-9 | Test BUSY kéo dài, hết ngân sách | FI-18, FI-26 đến FI-31 | Mục 13 |

### D. Tiến trình con mồ côi

| Mã | Yêu cầu | Xử lý | Vị trí |
|---|---|---|---|
| D-1 | Worker chết, con còn sống | Dây sinh tồn; `heavy.lock` phát hiện | `queue-safety.md` mục 11.1 |
| D-2 | Supervisor khởi động khi con cũ còn | Bảng quyết định O1–O6 | Mục 11.3 |
| D-3 | Không nhận diện hoặc không dừng được | Không gửi tín hiệu; chặn hàng đợi; can thiệp thủ công | Mục 11.2, 11.3 |
| D-4 | Không chồng tác vụ nặng | `heavy.lock` kế thừa; không tùy chọn bỏ qua | Mục 11.1 |
| D-5 | Không để đĩa tăng mất kiểm soát | `RLIMIT_FSIZE`, staging chỉ đọc, kiểm tra đĩa. **Orphan lạ bị giới hạn, không bị dừng** | Mục 11.5 |
| D-6 | Tiếp tục, requeue, thủ công | Bảng quyết định; không bao giờ gắn lại tiến trình cũ | Mục 11.4 |
| D-7 | Tiêu chí, kiểm thử | AC-Q13 đến AC-Q17, FI-33 đến FI-43 | Mục 12, 13 |

**Lớp chưa phủ:** `heavy.lock` không bảo vệ được yêu cầu đang xử lý trong daemon Ollama. Có yêu cầu giải phóng model (FI-43), và cần đo ở Phase 1.

### E. Bao phủ fault injection

| Mã | Tình huống | Kiểm thử |
|---|---|---|
| E-1 | Commit đua với thu hồi | FI-22 (commit thắng), FI-23 (thu hồi thắng) |
| E-2 | Crash trước, sau flush | FI-24, FI-25 |
| E-3 | Crash trước, sau rename | FI-25, FI-10 |
| E-4 | Crash trước, sau con trỏ DB | FI-10, FI-11 |
| E-5 | BUSY kéo dài | FI-26 đến FI-29 |
| E-6 | Đồng hồ lùi | FI-32 |
| E-7 | Phục hồi với orphan | FI-33 đến FI-37 |
| E-8 | Đủ sáu cột cho mỗi bài | Bảng mục 13, cùng oracle OR1–OR6 |

**Lưu ý:** "bằng chứng" trong bảng là điều kiện sẽ kiểm tra. **Không có bài nào đã chạy, nên chưa có gì được chứng minh.**

### F. OAuth và TikTok

| Mã | Yêu cầu | Xử lý | Vị trí |
|---|---|---|---|
| F-1 | `client_secret` desktop không phải bí mật được bảo vệ | Đã ghi, kèm hệ quả | `security-and-rights.md` mục 3 |
| F-2 | Chỉ dùng client, luồng được hỗ trợ | Không hỗ trợ thì dừng, không tự thêm backend | Mục 3 |
| F-3 | Xác minh scope thực nhận | Thiếu thì fail closed | Mục 3 |
| F-4 | Token không tới dashboard | AC-S8 | Mục 4 |
| F-5 | TikTok truy vấn creator info | Mỗi lần đăng | `publishing-reliability.md` mục 11 |
| F-6 | Tôn trọng quyền riêng tư, giới hạn | Không mặc định; PF-17, PF-19 | Mục 11 |
| F-7 | Đồng ý trước khi gửi | AC-P15, PF-18 | Mục 11, 12 |
| F-8 | Lưu bằng chứng | AC-P16 | Mục 11 |
| F-9 | Chi tiết nằm sau adapter | Giao diện chung, AC-P12 | Mục 10 |

**Tự sửa thêm:** Bản sửa 1 ghi "cổng cố định". Google hướng dẫn dùng cổng ngẫu nhiên, nên đã đổi thành quy tắc theo nhà cung cấp.

### G. Rights Gate

| Mã | Yêu cầu | Xử lý |
|---|---|---|
| G-1 | Năm điều kiện tạo `queued` | Bảng và dịch vụ duy nhất `enqueue_publication`, `security-and-rights.md` mục 8 |
| G-2 | Gắn đúng gói | Gói bất biến, `package_sha256` |
| G-3 | Gắn đúng asset, phiên bản | `asset_version`, `asset_sha256` trong manifest |
| G-4 | Kiểm tra lại ngay trước khi gửi | Trong transaction `queued → uploading`, PF-14 |
| G-5 | Không có đường vòng | `PublishGrant`, trigger, test kiến trúc, AC-R7, AC-R8 |
| G-6 | Fail closed | Thiếu hoặc không rõ thì chặn |

### H. YouTube và Facebook

| Mã | Yêu cầu | Xử lý | Trạng thái |
|---|---|---|---|
| H-1 | Đặt tường minh `privacyStatus=private` | Phase 15, AC-P17, PF-21, PF-22 | Đặc tả |
| H-2 | Không dựa vào mặc định | Đã ghi | Đặc tả |
| H-3 | Kiểm tra lại quota, yêu cầu upload | Điều kiện Phase 15. Ảnh chụp ngày 2026-10-30 có nguồn | Đặc tả |
| H-4 | Facebook chưa xác minh | Trang App Review đọc được qua công cụ tóm tắt, nhưng chưa đủ. **Giữ trạng thái chưa xác minh** | **Chưa xác minh** |
| H-5 | Ghi ngày và nguồn | `platform-verification.md` | Đã ghi |

### I. Tài liệu bàn giao

Đã cập nhật `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`, `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`, báo cáo Phase 0, kèm phân biệt năm trạng thái.

### Điều Codex nên kiểm tra nếu có review tiếp

1. Thay đổi đáng chú ý: thu hồi job **chỉ lúc khởi động**, không còn reaper khi đang chạy.
2. `heavy.lock` có thật sự được giữ qua tiến trình cháu như FFmpeg không; cần thử thực tế ở Phase 2.
3. Tệp `pending_outcome` có tạo đường nào làm commit trùng không.
4. Trigger SQLite cho `publications` có đủ biểu đạt năm điều kiện không; có thể chỉ kiểm tra được khóa tham chiếu.

---

## Vòng 1

- Review được phản hồi: [REVIEW_REPORT.md](REVIEW_REPORT.md), 2026-10-30, kết luận **NEEDS REVISION**.
- Người phản hồi: Claude (Lead Developer). Ngày 2026-10-30.
- Phạm vi: chỉ tài liệu. Không code, không cài đặt, không bắt đầu Phase 1 hoặc 2.
- Tài liệu này không tuyên bố nghiệm thu Phase 0 và không phê duyệt bất kỳ quyết định nào.

**Nhãn xử lý:**

- **Đã đặc tả:** tài liệu đã sửa; phần triển khai và kiểm thử còn ở phase sau.
- **Chờ Chủ dự án:** cần quyết định của Chủ dự án.
- **Mở có kiểm soát:** chưa thể đóng lúc này; có cổng chặn ở đúng phase.
- **Ghi nhận:** không cần thay đổi thêm.

Blueprint giữ nguyên: Factory Manager + bảy Agent, không thêm Agent, không đổi trách nhiệm Agent, không đổi bộ công nghệ.

## BLOCKER

| Mã | Phát hiện | Lập trường | Nhãn | Xử lý | Vị trí |
|---|---|---|---|---|---|
| B1 | Lease thiếu fencing | Đồng ý | **Đã đặc tả** | Thêm `lease_generation`, commit có điều kiện, staging theo attempt, con trỏ DB là điểm commit duy nhất, hành vi ngủ máy, crash, khởi động lại. 9 tiêu chí, 21 kịch bản fault injection, 3 kiểm thử thủ công. D-018 `Proposed` | [queue-safety.md](docs/architecture/queue-safety.md), `ARCHITECTURE.md` mục 5 |
| B2 | Kết quả API không rõ | Đồng ý | **Đã đặc tả** | Máy trạng thái có `unknown`, cấm retry mù, đối soát, người duyệt, ràng buộc DB chống trùng. D-019 `Proposed` | [publishing-reliability.md](docs/architecture/publishing-reliability.md), `ARCHITECTURE.md` mục 15 |
| B3 | Quyết định mở rộng chưa được thông qua | Đồng ý | **Chờ Chủ dự án** | Bỏ cách gom vào Q-01, thêm cổng theo phase, rà soát từng quyết định. Tôi không thể tự đóng mục này. Phase 2 bị chặn cho tới khi có quyết định | `IMPLEMENTATION_PLAN.md` mục 6, `DECISIONS.md` |
| B4 | Không thể tuyên bố tuân thủ API/license | Đồng ý | **Mở có kiểm soát** | Đặt điều kiện đầu vào: hồ sơ xác minh nền tảng trước mỗi adapter; rà soát license trước khi tải TTS. Mục này chỉ đóng khi có bằng chứng cho từng tích hợp. Không chặn dựng khung local MVP | [platform-verification.md](docs/deployment/platform-verification.md), `IMPLEMENTATION_PLAN.md` Phase 1, 15, 16 |

## WARNING

| Mã | Phát hiện | Lập trường | Nhãn | Xử lý |
|---|---|---|---|---|
| W1 | D-009, D-010 được trình bày quá cụ thể khi còn `Proposed` | Đồng ý | **Chờ Chủ dự án** | `ARCHITECTURE.md` gắn nhãn `[Đề xuất – D-xxx]` và nêu rõ chưa được duyệt |
| W2 | Chưa có bằng chứng khả thi | Đồng ý | **Mở có kiểm soát** | Không giải quyết được bằng tài liệu. Cần số đo Phase 1 và Phase 14; số liệu hiện vẫn là giả định |
| W3 | MVP có thể nặng hạ tầng | Đồng ý một phần | **Đã đặc tả** | Cố định một Worker, một tác vụ nặng. Tuy nhiên tôi giữ lease và fencing vì phục hồi sau ngủ máy là yêu cầu thật của máy này, và chính bạn yêu cầu. Thêm rủi ro R12 |
| W4 | TTS kiểm chứng quá muộn | Đồng ý | **Đã đặc tả** | Thêm spike vào Phase 1. Adapter vẫn ở Phase 6 |
| W5 | Mở rộng chỉ ở mức ranh giới API | Đồng ý | **Ghi nhận** | `ARCHITECTURE.md` mục 14 nêu rõ không sẵn sàng đa người dùng. Đặc tả khi có nhu cầu |
| W6 | Thiếu threat model localhost | Đồng ý | **Đã đặc tả** | Mô hình đe dọa, Host, Origin, token cục bộ, OAuth. Bắt đầu áp dụng từ Phase 2, không đợi tới dashboard, vì trang web trong trình duyệt gửi được yêu cầu tới loopback. D-020, D-021 `Proposed` |
| W7 | Manifest chưa đủ cho quyền nội dung | Đồng ý | **Đã đặc tả** | Hồ sơ quyền, bản lưu điều khoản, đồng ý giọng, Rights Gate fail closed. D-022 `Proposed` |
| W8 | Chính sách API cần cập nhật | **Đồng ý, Codex đúng về YouTube** | **Mở có kiểm soát** | Tôi đã đọc lại ba trang chính thức ngày 2026-10-30. Trang YouTube ghi rõ dự án chưa xác minh không bị giới hạn riêng tư, nên ghi chú Phase 0 của tôi đã lỗi thời và được sửa. TikTok xác nhận giới hạn với client chưa audit. Facebook mới có phần quyền; App Review chưa xác minh. Đây chỉ là ảnh chụp |
| W9 | `.gitignore` chưa được xác minh độc lập | Đồng ý | **Mở có kiểm soát** | Tôi chạy lại kiểm tra trong bản sửa này, nhưng đó vẫn là tự kiểm tra. Cần Codex xác minh. `.env.example` chưa tồn tại, sẽ tạo ở Phase 2. Xem yêu cầu review |
| W10 | Tệp handoff chưa tồn tại | Đồng ý | **Đã đặc tả** | Đã tạo `HANDOFF_TO_CHATGPT.md` theo yêu cầu của Chủ dự án |

## RECOMMENDATION

| Mã | Đề xuất | Quyết định | Nhãn | Vị trí |
|---|---|---|---|---|
| R1 | Fencing, staging, kiểm thử worker hồi sinh | Áp dụng đầy đủ, thêm phân biệt `failure_count` và `recovery_count`, watchdog tiến độ, xử lý tiến trình con mồ côi | **Đã đặc tả** | `queue-safety.md` |
| R2 | Máy trạng thái upload | Áp dụng; thêm quy tắc URL phiên upload được coi là secret | **Đã đặc tả** | `publishing-reliability.md` |
| R3 | Spike TTS Phase 1 | Áp dụng; không chốt engine | **Đã đặc tả** | `IMPLEMENTATION_PLAN.md` Phase 1 |
| R4 | Cấu hình tối giản, benchmark trước khi cam kết | Áp dụng | **Đã đặc tả** | `ARCHITECTURE.md` mục 1, mục 5; Phase 14 |
| R5 | Bảng quyết định theo phase | Áp dụng | **Đã đặc tả** | `IMPLEMENTATION_PLAN.md` mục 6 |
| R6 | Checklist quyền nội dung | Áp dụng | **Đã đặc tả** | `security-and-rights.md` mục 6–9 |
| R7 | Đặc tả loopback callback | Áp dụng ở mức yêu cầu; hoàn tất đặc tả trước Phase 15 | **Đã đặc tả** | `security-and-rights.md` mục 2–5 |
| R8 | Ghi chú chính sách có link, ngày | Áp dụng; là điều kiện đầu vào của từng adapter | **Đã đặc tả** | `platform-verification.md` |
| R9 | Tạo handoff, sửa nhãn trạng thái Phase 0 | Áp dụng. Đề xuất "sau khi editor được đóng" được Chủ dự án thay bằng yêu cầu tạo ngay; xem ghi chú bên dưới | **Đã đặc tả** | `HANDOFF_TO_CHATGPT.md`, `CURRENT_STATUS.md` |
| R10 | Không thêm Kubernetes, broker, cloud DB, vector DB, frontend web | Áp dụng | **Ghi nhận** | `ARCHITECTURE.md` mục 14 |

**Ghi chú về R9:** tại thời điểm tạo tệp, `vi` (PID 3151) vẫn tồn tại ở trạng thái tạm dừng. Tôi kiểm tra tệp swap theo cách chỉ đọc, thấy buffer không có nội dung thực, nên tạo tệp theo yêu cầu trực tiếp của Chủ dự án. Không tác động đến `vi` hay tệp swap.

## Thay đổi có thể Codex muốn soi kỹ

- Đổi tập trạng thái job: bỏ `failed` làm trạng thái bền, thêm `cancelled`.
- Worker vẫn được commit khi lease đã quá hạn nếu generation còn hiện hành, vì tính an toàn nằm ở fencing.
- Không tăng generation khi thu hồi, chỉ tăng khi nhận job.
- Sau crash, mọi bản ghi `uploading` đều thành `unknown`, kể cả khi thực tế chưa gửi byte nào (PF-03), vì sau khởi động lại không phân biệt được hai trường hợp. Cách này có thể tạo thêm việc duyệt tay, nhưng an toàn hơn.

## Yêu cầu cho review lần 2

1. **Fencing:** tìm chuỗi sự kiện khiến worker cũ vẫn ghi được hoặc job kẹt vĩnh viễn, đặc biệt quanh thu hồi lúc thức dậy và tiến trình con mồ côi.
2. Quyết định cho phép commit khi lease quá hạn có an toàn không?
3. Bộ FI-01 đến FI-21 và MT-01 đến MT-03 có thiếu kịch bản nào?
4. Máy trạng thái upload có đường nào dẫn tới đăng trùng tự động?
5. Mô hình đe dọa cục bộ và yêu cầu OAuth có thiếu sót?
6. Rights Gate có đường vượt qua không?
7. Spike TTS có đủ nhỏ và đủ để ra quyết định?
8. Xác minh độc lập `.gitignore` và các tuyên bố về chính sách nền tảng.
9. Xác nhận không có quyết định `Proposed` nào bị trình bày như đã duyệt.
