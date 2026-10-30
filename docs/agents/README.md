# Đặc tả Agent

Hợp đồng chung: [ARCHITECTURE.md](../../ARCHITECTURE.md) mục 4. Các trường dữ liệu cụ thể được chốt khi đến phase của từng Agent.

**Áp dụng cho mọi Agent ([queue-safety.md](../architecture/queue-safety.md)):** Agent chạy trong tiến trình con, nhận thư mục staging riêng theo generation, không ghi DB và không tự promote artifact. Đầu vào được lấy qua DB và kiểm tra checksum. Supervisor quyết định commit theo fencing.

## Factory Manager

Điều phối, không chứa logic nghiệp vụ. Sở hữu máy trạng thái, Quality Gate, Rights Gate và quản lý tài nguyên. Chuyển trạng thái run nằm trong cùng transaction với commit job.

## Athena – Research & Content Strategy

- **Đầu vào:** brief, ngôn ngữ, phong cách, độ dài mục tiêu, nguồn tham khảo.
- **Đầu ra:** `research_brief.json`: thông điệp chính, dàn ý, khẳng định kèm nguồn.
- **Không làm:** viết lời thoại; tự ý mở rộng nguồn ngoài phạm vi Q-04.
- **Lỗi đặc thù:** khẳng định không có nguồn được đánh dấu để người kiểm tra.

## Leonardo – Scriptwriting & Storyboard

- **Đầu vào:** `research_brief.json`, phong cách.
- **Đầu ra:** `script.json` (cảnh, nhân vật, lời thoại), `storyboard.json` (bố cục, hành động).
- **Không làm:** chọn engine giọng; vẽ.
- **Lỗi đặc thù:** LLM trả JSON sai thì retry có giới hạn; kịch bản quá dài thì yêu cầu rút gọn.

## Edison – Text-to-Speech & Voice Casting

- **Đầu vào:** `script.json`, bảng nhân vật.
- **Đầu ra:** âm thanh từng câu, `voice_manifest.json` (engine, giọng, license), timing.
- **Không làm:** sửa nội dung lời thoại.
- **Lỗi đặc thù:** chuẩn hóa số, ngày tháng, từ viết tắt theo ngôn ngữ; retry theo từng câu; kiểm tra thời lượng so với số từ.

## Pixar – 2D Animation & Lip-sync

- **Đầu vào:** `storyboard.json`, timing, âm thanh, thư viện asset.
- **Đầu ra:** scene spec, dữ liệu viseme, SVG theo khung hình theo yêu cầu.
- **Không làm:** mã hóa video.
- **Lỗi đặc thù:** thiếu asset thì dừng cảnh đó, không thay thế ngầm.

## Spielberg – Video Editing & Rendering

- **Đầu vào:** scene spec, âm thanh, nhạc đã có license.
- **Đầu ra:** clip từng cảnh, phụ đề (SRT), MP4, thumbnail, metadata, `render_report.json`.
- **Không làm:** xuất bản.
- **Lỗi đặc thù:** retry theo cảnh; kiểm tra lại bằng `ffprobe`.

## Tesla – Multi-platform Publishing

- **Đầu vào:** gói xuất bản **có phê duyệt hợp lệ và Rights Gate đạt**, kiểm tra theo checksum.
- **Đầu ra:** bản ghi xuất bản và bằng chứng theo nền tảng.
- **Không làm:** đăng khi chưa duyệt, retry mù, dùng API không chính thức.
- **Lỗi đặc thù:** theo [publishing-reliability.md](../architecture/publishing-reliability.md). Lỗi từng nền tảng xử lý độc lập. Timeout hoặc crash khi `uploading` dẫn tới `unknown` và đối soát; không xác định được thì chuyển người duyệt. Đây là thay đổi về độ tin cậy, không đổi trách nhiệm của Tesla.
- **Điều kiện trước adapter:** hoàn tất [xác minh chính sách](../deployment/platform-verification.md).
- **Ranh giới:** adapter chỉ chạy với `PublishGrant`; chi tiết riêng từng nền tảng nằm trong adapter. Xem [security-and-rights.md](../architecture/security-and-rights.md) mục 8.

## Newton – Analytics & Performance

- **Đầu vào:** bản ghi xuất bản, API phân tích của nền tảng.
- **Đầu ra:** báo cáo hiệu suất, gợi ý chủ đề.
- **Không làm:** tự thay đổi cấu hình hay nội dung; gợi ý chỉ mang tính đề xuất.
