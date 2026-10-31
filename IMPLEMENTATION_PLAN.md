# AI VIDEO FACTORY – IMPLEMENTATION PLAN

> Lộ trình này là khung tổng thể. Trước khi bắt đầu mỗi phase, Lead Developer phải trình bày bản kế hoạch chi tiết theo mẫu ở mục 2 và chờ xác nhận. Không có mốc thời gian lịch vì tốc độ phụ thuộc vào nghiệm thu và duyệt API của bên thứ ba.

## 1. Nguyên tắc sắp xếp

- Rủi ro lớn nhất được kiểm chứng sớm nhất: tốc độ render, chất lượng TTS tiếng Việt, khả năng chịu tải của máy.
- Mỗi phase kết thúc bằng thứ chạy được và kiểm tra được.
- Video hoàn chỉnh ngắn (Phase 9) xuất hiện trước khi xây thêm tính năng.
- Mạng xã hội để cuối: chỉ tích hợp khi đã có video tốt để đăng.

## 2. Mẫu kế hoạch trước phase (Quy tắc B)

```markdown
# Kế hoạch Phase N – <tên>
- Mục tiêu:
- File sẽ tạo hoặc sửa:
- Công nghệ sử dụng:
- Lệnh cần chạy (kèm giải thích; đánh dấu lệnh ảnh hưởng hệ thống):
- Rủi ro:
- Cách kiểm tra thành công:
- Cách quay lại nếu có lỗi:
```

## 3. Tổng quan

| Phase | Tên | Kết quả | Trạng thái |
|---|---|---|---|
| 0 | Hồ sơ dự án | Bộ tài liệu | **ACCEPTED** (Project Owner, 2026-10-30), mức tài liệu và thiết kế |
| 1 | Môi trường & đo đạc nền | Công cụ cài đặt, số đo thực, spike TTS | Kế hoạch đã xác nhận (2026-10-31); đang ở bước 1.0, chưa cài đặt gì |
| 2 | Nền tảng lõi | Config, DB, Queue, API, Worker | Chưa làm |
| 3 | Factory Manager | Pipeline chạy với Agent giả lập | Chưa làm |
| 4 | Spielberg cơ bản | Spec cảnh → MP4 | Chưa làm |
| 5 | Pixar: stickman | Hoạt hình stickman | Chưa làm |
| 6 | Edison: TTS | Adapter và giọng Việt, Anh | Chưa làm |
| 7 | Leonardo | Kịch bản và storyboard | Chưa làm |
| 8 | Athena | Research brief | Chưa làm |
| 9 | Vertical slice | Video 60 giây hoàn chỉnh có phụ đề | Chưa làm |
| 10 | Dashboard MVP | Quản lý quy trình trên Streamlit | Chưa làm |
| 11 | Whiteboard & Explainer | Thêm hai phong cách | Chưa làm |
| 12 | Storytelling & Lip-sync | Nhiều nhân vật, nhiều giọng | Chưa làm |
| 13 | Đóng gói nội dung | Thumbnail, metadata, Quality Gate đầy đủ | Chưa làm |
| 14 | Kiểm thử bền 10 phút | Xác nhận năng suất thật | Chưa làm |
| 15 | Tesla: YouTube | Đăng qua API chính thức | Chưa làm |
| 16 | Tesla: TikTok, Facebook | Đăng đa nền tảng | Chưa làm; TikTok Direct Post `POLICY BLOCKED`, Facebook chưa xác minh |
| 17 | Newton | Phân tích hiệu suất | Chưa làm |
| 18 | Tối ưu | MLX, OpenToonz, tinh chỉnh | Chưa làm |
| 19 | Củng cố & bàn giao | Sao lưu, vận hành, tài liệu | Chưa làm |

## 4. Chi tiết

### Phase 0 – Hồ sơ dự án
**Mục tiêu:** bộ tài liệu quản lý, không code. **Nghiệm thu:** Codex review; **Chủ dự án là người duy nhất tuyên bố nghiệm thu.** Review lần 1 kết luận NEEDS REVISION, Bản sửa 1 đã xử lý. Bản sửa 2 xử lý các phát hiện của review lần 2. Review lần 3 kết luận CHANGES REQUESTED; Bản sửa 3 xử lý R3-01, R3-02, R3-03. Review lần 4 kết luận APPROVED WITH CHANGES cho hồ sơ Phase 0; bản cập nhật D-023 xử lý R4-01. Việc ghi nhận D-023 không phải nghiệm thu Phase 0. **Project Owner nghiệm thu Phase 0 ngày 2026-10-30**, căn cứ Codex Final F-01 Verification: PASS. Nghiệm thu không xác nhận code đã triển khai, không xác nhận runtime test đã pass và không cho phép bắt đầu Phase 1.

### Phase 1 – Môi trường & đo đạc nền
**Điều kiện vào:** Phase 0 được nghiệm thu (đã có), D-013 và D-017 được quyết định (đã duyệt 2026-10-31), có trả lời Q-03 và Q-06 (đã trả lời 2026-10-31). **Kế hoạch chi tiết đã được Chủ dự án xác nhận ngày 2026-10-31** ([PHASE-01-PLAN.md](docs/operations/phase-reports/PHASE-01-PLAN.md)). Chỉ bước 1.0 được phép; cài đặt và tải model cần xác nhận từng lệnh.
**Mục tiêu:** cài công cụ đã duyệt và thay giả định bằng số đo.
**Dự kiến cài (sẽ xin xác nhận từng lệnh):** Python, FFmpeg, Ollama, một LLM để benchmark, thư viện rasterize ứng viên, ứng viên TTS của spike.
**Đo:** tốc độ LLM tiếng Việt, tốc độ rasterize SVG, tốc độ mã hóa `h264_videotoolbox` và `libx264`, faster-whisper; RAM đỉnh; **render bền 30 phút để xem giảm xung nhiệt**.
**Nghiệm thu:** `docs/testing/baseline-*.md` có số đo thật; kết quả benchmark D-013 được trình Chủ dự án; ước tính "một video mỗi ngày" được cập nhật; spike TTS hoàn tất theo mục dưới.
**Rủi ro:** dung lượng model; xung đột phiên bản. **Quay lại:** gỡ theo danh sách đã ghi.

#### Spike TTS Việt–Anh

**Phạm vi:** đánh giá khả thi có giới hạn. **Không** xây adapter, không tích hợp pipeline, **không chốt engine**. Tích hợp đầy đủ vẫn ở Phase 6.

1. **Rà soát license trước khi tải.** Kiểm tra riêng code, model và từng giọng, gồm quyền thương mại. Ứng viên không rõ license được ghi nhận và không tải cho tới khi rõ. Loại công cụ thuộc D-017 nếu được duyệt. Giả định có mục đích thương mại cho tới khi có trả lời Q-03.
2. **Ứng viên:** 2–3 cho tiếng Việt, 2 cho tiếng Anh, chọn từ `TECH_STACK.md` mục 3. Danh sách cuối cùng trình trong kế hoạch Phase 1.
3. **Bộ văn bản mẫu cố định**, cùng cho mọi ứng viên: lời kể ngắn; hội thoại; số, ngày tháng, từ viết tắt; câu tiếng Việt nhiều dấu thanh; tiếng Việt xen thuật ngữ tiếng Anh.
4. **Ít nhất hai hồ sơ nhân vật khác biệt** (ví dụ người kể chuyện và nhân vật trẻ) nếu ứng viên hỗ trợ; ghi rõ nếu không hỗ trợ.
5. **Đo trên máy mục tiêu, chạy tuần tự:** thời gian xử lý, hệ số thời gian thực (thời gian sinh chia thời lượng âm thanh), RAM đỉnh, dung lượng model.
6. **Chủ dự án nghe mù, chấm 1–5:** phát âm, độ tự nhiên, độ nhất quán giữa các câu và các lần sinh. Việc chấm phải do người nghe; không có số đo tự động thay thế.
7. **Ghi kết quả** ở `docs/testing/baseline-tts.md`: bảng so sánh, phiên bản, lệnh, bảng license có link và ngày kiểm tra. Mẫu âm thanh lưu ở `workspace/spikes/tts/`, ngoài Git, kèm danh sách SHA-256 trong báo cáo.

**Kết quả của spike:** danh sách rút gọn có bằng chứng, trình Chủ dự án. **Nếu không ứng viên tiếng Việt nào đạt, dừng lại và báo Chủ dự án trước khi đầu tư vào Phase 4–5.**

### Phase 2 – Nền tảng lõi
**Điều kiện vào:** Chủ dự án quyết định D-009, D-010, D-011, D-015 (phần `.env`), D-016, D-018, D-020 (xem mục 6).
**Mục tiêu:** khung dự án, config, migration, Job Queue, FastAPI, Worker, logging.
**Nghiệm thu:** test đơn vị và tích hợp pass; AC-Q1 đến AC-Q19 trong [queue-safety.md](docs/architecture/queue-safety.md); FI-01 đến FI-13, FI-17 đến FI-19, FI-22 đến FI-42, FI-44 đến FI-51 pass kèm oracle OR1–OR6; AC-S1 đến AC-S3 trong [security-and-rights.md](docs/architecture/security-and-rights.md). **Queue chỉ được coi là an toàn sau khi các kiểm thử này thực sự pass.**

### Phase 3 – Factory Manager
**Mục tiêu:** máy trạng thái và Quality Gate với bảy Agent giả lập.
**Nghiệm thu:** run giả lập đi hết pipeline; lỗi giả lập được retry đúng; chặn xuất bản khi chưa duyệt; tiếp tục được sau khởi động lại; FI-14, FI-15, FI-16, FI-20, FI-21, FI-43 pass; kiểm thử thủ công MT-01, MT-02 có kết quả ghi lại.

### Phase 4 – Spielberg cơ bản
**Mục tiêu:** từ scene spec và âm thanh mẫu ra clip, ghép thành MP4.
**Nghiệm thu:** `ffprobe` xác nhận định dạng, thời lượng; render lại một cảnh không đổi cảnh khác.

### Phase 5 – Pixar: stickman
**Mục tiêu:** engine SVG, nhân vật que, tư thế, chuyển động cơ bản.
**Nghiệm thu:** video mẫu 30 giây; ảnh snapshot khung hình ổn định; Chủ dự án xem và đánh giá hình ảnh.

### Phase 6 – Edison: TTS
**Mục tiêu:** adapter TTS và tích hợp đầy đủ, dựa trên kết quả spike ở Phase 1.
**Nghiệm thu:** cập nhật so sánh chất lượng, tốc độ, license nếu ứng viên thay đổi; **Chủ dự án chọn giọng**; engine dự phòng hoạt động được; hồ sơ quyền của giọng hoàn chỉnh.
**Rủi ro lớn:** không có giọng tiếng Việt miễn phí, chất lượng đủ tốt và license phù hợp. **Phương án:** báo Chủ dự án để quyết định.

### Phase 7 – Leonardo
**Mục tiêu:** LLM adapter, tạo kịch bản và storyboard có schema.
**Nghiệm thu:** JSON hợp lệ trên bộ mẫu Việt, Anh; retry khi sai schema; có đo tỷ lệ lỗi.

### Phase 8 – Athena
**Mục tiêu:** chuyển brief và nguồn tài liệu thành research brief có trích dẫn. Phạm vi truy cập web phụ thuộc Q-04.
**Nghiệm thu:** QG1 hoạt động; khẳng định không có nguồn bị đánh dấu.

### Phase 9 – Vertical slice
**Mục tiêu:** từ văn bản đến MP4 stickman 60 giây có phụ đề, Việt và Anh, chạy bằng một lệnh.
**Nghiệm thu:** hai video thật; chỉ số thời gian thực và RAM đỉnh; Chủ dự án xem. **Đây là cổng quyết định lớn:** nếu chất lượng hoặc tốc độ không đạt, xem lại kế hoạch trước khi đi tiếp.

### Phase 10 – Dashboard MVP
**Mục tiêu:** tạo run, xem tiến độ, log, phê duyệt, retry cảnh, xem dung lượng.
**Nghiệm thu:** thực hiện đủ quy trình qua giao diện; dashboard không truy cập DB trực tiếp.

### Phase 11 – Whiteboard & Explainer
**Mục tiêu:** hiệu ứng vẽ tay, biểu đồ và chữ cho video giáo dục.
**Nghiệm thu:** mỗi phong cách có video mẫu 60 giây được duyệt.

### Phase 12 – Storytelling & Lip-sync
**Mục tiêu:** nhiều nhân vật, voice casting, lip-sync cơ bản.
**Nghiệm thu:** video hội thoại 2–3 nhân vật đúng giọng; miệng khớp ở mức cơ bản, bao gồm tiếng Việt.

### Phase 13 – Đóng gói nội dung
**Điều kiện vào:** Chủ dự án quyết định D-022.
**Mục tiêu:** thumbnail, metadata, hồ sơ quyền, Rights Gate, Quality Gate hoàn chỉnh.
**Nghiệm thu:** gói xuất bản bất biến có `package_sha256`; AC-R1 đến AC-R5 và AC-R8 pass.

### Phase 14 – Kiểm thử bền 10 phút
**Mục tiêu:** chạy video 10 phút thật, nhiều ngày liên tiếp.
**Nghiệm thu:** ít nhất 3 video 10 phút liên tiếp thành công; có số đo thời gian, nhiệt, dung lượng; xử lý được ngủ máy giữa chừng; kết luận rõ mục tiêu một video mỗi ngày có đạt không.

### Phase 15 – Tesla: YouTube
**Mục tiêu:** OAuth, upload riêng tư, quản lý quota, đối soát.
**Điều kiện trước:** Chủ dự án quyết định D-019, D-021 và phần Keychain của D-015; **hồ sơ [xác minh chính sách](docs/deployment/platform-verification.md) của YouTube hoàn tất ngay trước khi viết adapter**; Chủ dự án tạo dự án API và cung cấp credentials, Claude không tự tạo.
**Yêu cầu riêng:** mọi upload thử nghiệm đặt tường minh `status.privacyStatus=private`, **không dựa vào giá trị mặc định của API**. Kiểm tra lại quota và yêu cầu upload ngay trước khi triển khai. Ghi nhận ngày 2026-10-30 chỉ là ảnh chụp, xem [platform-verification.md](docs/deployment/platform-verification.md).
**Nghiệm thu:** upload riêng tư thành công qua phê duyệt và Rights Gate; AC-P1 đến AC-P12, AC-P15 đến AC-P17 trong [publishing-reliability.md](docs/architecture/publishing-reliability.md); PF-01 đến PF-22 áp dụng cho YouTube pass với máy chủ giả lập; AC-S3 đến AC-S9, AC-R6, AC-R7 pass; không đăng được khi chưa duyệt.

### Phase 16 – Tesla: TikTok, Facebook
**Điều kiện trước:** hồ sơ xác minh chính sách **riêng cho từng nền tảng** hoàn tất ngay trước adapter đó; hoàn tất thủ tục duyệt app theo yêu cầu đã xác minh; có đích đăng hợp lệ.
**TikTok Direct Post: `POLICY BLOCKED`.** Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. **Không viết, kích hoạt hay sử dụng adapter Direct Post khi chưa đủ năm điều kiện G1–G5** tại [platform-verification.md](docs/deployment/platform-verification.md) mục 3, gồm quyết định triển khai riêng của Project Owner. Việc đã chấp nhận rủi ro không thay thế điều kiện nào. Chỉ sau khi mở cổng, các yêu cầu sau mới áp dụng: truy vấn creator info, tôn trọng lựa chọn quyền riêng tư và giới hạn đăng, cần đồng ý rõ ràng trước khi gửi nội dung, lưu bằng chứng; AC-P13 đến AC-P16.
**Không phụ thuộc Direct Post:** các phase local vẫn tiếp tục theo cổng riêng của chúng. Có thể hỗ trợ xuất MP4, metadata và thumbnail để người dùng đăng thủ công.
**Facebook:** quyền và App Review **chưa được xác minh**. Không bắt đầu adapter này cho tới khi đọc trực tiếp tài liệu chính thức và có hồ sơ xác minh.
**Nghiệm thu:** đăng thử thành công trong giới hạn nền tảng cho phép; các tiêu chí AC-P và PF áp dụng cho từng adapter; lỗi một nền tảng không ảnh hưởng nền tảng khác.

### Phase 17 – Newton
**Mục tiêu:** thu thập số liệu qua API chính thức, báo cáo, gợi ý chủ đề.
**Nghiệm thu:** số liệu khớp với nền tảng; gợi ý chỉ mang tính đề xuất.

### Phase 18 – Tối ưu
**Mục tiêu:** đánh giá MLX, tích hợp OpenToonz nếu cần, tối ưu chỗ nghẽn đã đo.
**Nghiệm thu:** số đo trước và sau; không chấp nhận tối ưu thiếu bằng chứng.

### Phase 19 – Củng cố & bàn giao
**Mục tiêu:** sao lưu, khôi phục, hướng dẫn vận hành, rà soát bảo mật và license.
**Nghiệm thu:** khôi phục thử từ bản sao lưu thành công; Codex review toàn hệ thống; Chủ dự án nghiệm thu.

## 5. Rủi ro tổng thể

| Mã | Rủi ro | Mức | Giảm thiểu | Kiểm chứng tại |
|---|---|---|---|---|
| R1 | Không có TTS tiếng Việt miễn phí đủ tốt, đúng license | Cao | Spike sớm, adapter, so sánh nhiều engine | Phase 1, 6 |
| R2 | Render 10 phút quá lâu do giảm xung trên máy không quạt | Cao | Đo bền sớm, chia cảnh, chạy qua đêm | Phase 1, 14 |
| R3 | Nội dung LLM cục bộ kém hoặc sai sự thật | Cao | Nguồn trích dẫn, người duyệt | Phase 7–9 |
| R4 | Chính sách API hạn chế đăng công khai | Cao | Xác minh ngay trước từng adapter, đưa thời gian duyệt vào dự kiến | Phase 15–16 |
| R5 | Thiếu RAM khi chạy pipeline | Trung bình | Tuần tự, giải phóng model | Phase 1 |
| R6 | Đầy ổ đĩa | Trung bình | Giám sát, chặn run, dọn có xác nhận | Phase 2, 10 |
| R7 | Lip-sync tiếng Việt kém | Trung bình | Chấp nhận mức cơ bản | Phase 12 |
| R8 | Vi phạm bản quyền, chính sách | Trung bình | Manifest license, phê duyệt | Phase 13 |
| R9 | Hai AI sửa chồng lên nhau | Thấp | Nhánh riêng, khóa theo vai trò | Mọi phase |
| R10 | Worker cũ ghi đè kết quả mới | Cao | Fencing, staging theo attempt | Phase 2 |
| R11 | Đăng trùng do kết quả không rõ | Cao | Máy trạng thái upload, đối soát, người duyệt | Phase 15–16 |
| R12 | MVP quá nặng hạ tầng | Trung bình | Một Worker, một tác vụ nặng; chỉ mở rộng khi có số đo | Phase 2–3 |
| R13 | TikTok Direct Post không phù hợp mục đích dùng cá nhân. Project Owner chấp nhận rủi ro cho việc tiếp tục đánh giá (D-023), không phải cho việc triển khai | Cao | Giữ `POLICY BLOCKED` tới khi đủ G1–G5; không mô tả sai mục đích | Trước khi mở cổng Direct Post |

## 6. Cổng quyết định trước phase

Mọi mục trong bảng hiện vẫn là `Proposed`, **trừ D-013, D-017 và D-023** là `Approved` với phạm vi nêu trong dòng của từng mục. Không có mục `Proposed` nào được coi là đã duyệt. Chủ dự án quyết định từng mục; một phase không được bắt đầu khi mục bắt buộc của nó chưa được quyết định. Khuyến nghị chi tiết ở `DECISIONS.md`.

| Quyết định | Nội dung | Trạng thái | Phase đầu tiên dùng | Phải quyết định trước | Khuyến nghị của Lead |
|---|---|---|---|---|---|
| D-023 | Tiếp tục đánh giá TikTok Direct Post có kiểm soát (phương án C) | **Approved** (Project Owner). Direct Post integration: **`POLICY BLOCKED`** | 16 | Đã quyết định. Mở cổng triển khai cần G1–G5, gồm quyết định riêng | – |
| D-013 | Benchmark rasterize (chỉ duyệt phương pháp) | **Approved** (Project Owner, 2026-10-31) | 1 | Đã quyết định | – |
| D-017 | Không dùng công cụ không chính thức | **Approved** (Project Owner, 2026-10-31) | 1 | Đã quyết định | – |
| D-009 | Ba tiến trình | Proposed | 2 | Phase 2 | Duyệt có điều kiện |
| D-010 | Hợp đồng artifact | Proposed | 2 | Phase 2 | Duyệt |
| D-011 | Lease, heartbeat | Proposed | 2 | Phase 2 | Duyệt có điều kiện, cùng D-018 |
| D-018 | Fencing, staging, một Worker | Proposed | 2 | Phase 2 | Duyệt |
| D-015 | Secret: phần `.env` | Proposed | 2 | Phase 2 | Duyệt có điều kiện |
| D-016 | Không tự xóa, chặn khi thiếu đĩa | Proposed | 2 | Phase 2 | Duyệt |
| D-020 | Kiểm soát truy cập cục bộ | Proposed | 2 | Phase 2 | Duyệt |
| D-012 | Đẩy khung hình vào FFmpeg | Proposed | 4 | Phase 4 | Duyệt có điều kiện, sau số đo Phase 1 |
| D-014 | 1080p, 24 fps, 16:9 | Proposed | 4 | Phase 4 | Hoãn tới Q-02 và số đo Phase 1 |
| D-022 | Hồ sơ quyền, Rights Gate | Proposed | 13 | Phase 13 | Duyệt |
| D-019 | Máy trạng thái upload | Proposed | 15 | Phase 15 | Duyệt |
| D-021 | OAuth, vòng đời token | Proposed | 15 | Phase 15 | Duyệt |
| D-015 | Secret: phần Keychain | Proposed | 15 | Phase 15 | Duyệt cùng D-021 |
