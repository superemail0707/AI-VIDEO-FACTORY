# AI VIDEO FACTORY – TECH STACK

> **Chưa có phần mềm nào được cài cho dự án.** Tài liệu này mô tả định hướng, không phải trạng thái đã cài.
> Mọi thông tin về license, phiên bản và chính sách nền tảng phải được xác minh lại từ nguồn chính thức trước khi đưa vào sử dụng.

## 1. Hiện trạng máy (kiểm tra 2026-10-30, bằng `command -v`)

| Công cụ | Trạng thái |
|---|---|
| Git | Có (`/usr/bin/git`) |
| Python | Có `/usr/bin/python3` của hệ thống; chưa kiểm tra phiên bản; không dùng cho dự án |
| Xcode Command Line Tools | Có |
| Homebrew | Có (`/opt/homebrew/bin/brew`) |
| FFmpeg, Ollama, Node, uv | Chưa có |

## 2. Công nghệ đã duyệt

| Lớp | Công nghệ | Vai trò | Ghi chú |
|---|---|---|---|
| Ngôn ngữ | Python | Ngôn ngữ chính | Phiên bản chốt ở Phase 1 theo độ tương thích thư viện |
| LLM runtime | Ollama | Chạy LLM cục bộ | Model chọn bằng benchmark |
| Backend | FastAPI | API nội bộ | |
| Database | SQLite | Trạng thái | Chế độ WAL |
| Queue | SQLite-backed Job Queue | Hàng đợi | Tự xây, không thêm broker |
| Dashboard | Streamlit | MVP | |
| Animation | SVG + Python | Engine chính | |
| Video | FFmpeg | Render, ghép | |
| STT | Whisper / faster-whisper | Căn timing, phụ đề | Không dùng Metal trên Apple Silicon với faster-whisper; đo ở Phase 1 |
| TTS | Adapter | Việt và Anh | Spike ở Phase 1; engine chọn ở Phase 6, sau khi có bằng chứng |
| Publishing | API chính thức + OAuth | YouTube, TikTok, Facebook | |
| Tối ưu | MLX | Chỉ đánh giá ở phase tối ưu | |
| Phụ trợ | OpenToonz | Chỉnh cảnh phức tạp, tùy chọn | Không phải phụ thuộc của pipeline |

## 3. Ứng viên cần đánh giá (CHƯA duyệt)

Thêm bất kỳ mục nào đều cần ghi vào `DECISIONS.md`.

| Nhu cầu | Ứng viên | Tiêu chí | Phase |
|---|---|---|---|
| Rasterize SVG | resvg, CairoSVG, trình duyệt headless | Tốc độ, độ chính xác, bộ nhớ, license | 1 |
| TTS tiếng Việt | Piper (giọng vi), VieNeu-TTS, F5-TTS bản tiếng Việt | Chất lượng, tốc độ trên M4, **license của code, model và từng giọng** | 1 (spike), 6 |
| TTS tiếng Anh | Piper, Kokoro | Như trên | 1 (spike), 6 |
| Lip-sync | Rhubarb Lip Sync; suy ra từ timing hoặc biên độ | Độ khớp với tiếng Việt, license | 12 |
| LLM | Các model lượng tử hóa khoảng 7–9B qua Ollama | Tiếng Việt, JSON hợp lệ, RAM, tốc độ | 1, 7 |
| Kiểm thử | pytest, ruff | Tiêu chuẩn cộng đồng | 2 |
| Môi trường Python | `venv` + phụ thuộc đã ghim | Tối thiểu công cụ | 1 |

**Lưu ý bắt buộc khi chọn:**

- Một số model TTS có license phi thương mại (ví dụ dòng XTTS của Coqui). Nếu kênh có kiếm tiền, phải loại trừ. Liên quan Q-03.
- Không dùng `edge-tts` hay các thư viện tương tự: dùng dịch vụ không chính thức, trái nguyên tắc local-first và trái quy tắc dùng API chính thức.
- Giọng hệ thống macOS (lệnh `say`) cần kiểm tra điều khoản trước khi dùng cho nội dung xuất bản.
- Bản FFmpeg có libx264 là GPL. Việc này không ảnh hưởng khi dùng như công cụ cục bộ, nhưng cần xem lại nếu sau này phân phối ứng dụng.
- Giọng nhân bản phải có sự đồng ý của chủ giọng.

## 4. Ràng buộc API nền tảng

Ảnh chụp có nguồn và ngày kiểm tra nằm tại [docs/deployment/platform-verification.md](docs/deployment/platform-verification.md). **Xác minh chính sách là việc bắt buộc ngay trước mỗi adapter.** Ảnh chụp không phải cam kết và không có nghĩa dự án đã được cấp quyền nào.

| Nền tảng | Ghi nhận ngày 2026-10-30 | Ảnh hưởng dự kiến |
|---|---|---|
| YouTube Data API v3 | Tài liệu ghi video từ dự án chưa xác minh không bị giới hạn riêng tư; có quota upload. Sửa lại ghi chú ở Bản Phase 0, vốn đã lỗi thời | Xác minh lại trước Phase 15 |
| TikTok Content Posting API | Client chưa audit bị giới hạn riêng tư; app cần được duyệt scope `video.publish`. **Direct Post xung đột với mục đích dùng cá nhân (R3-01)** | **`POLICY BLOCKED`.** D-023 `Approved — Option C` (2026-10-30, Project Owner), Q-13 `Answered — Option C`: chỉ cho phép tiếp tục nghiên cứu, đánh giá. G1–G5 vẫn bắt buộc trước khi đề xuất triển khai, và phải có quyết định triển khai riêng của Project Owner. Mục tiêu giữ trong roadmap. Audit không đủ để mở khóa |
| Facebook Pages | **Chưa xác minh.** Có ghi nhận sơ bộ từ công cụ tóm tắt; quyền, App Review và trang cá nhân chưa đủ căn cứ | Chủ dự án có thể cần một Page |

Việc nộp hồ sơ duyệt do Chủ dự án thực hiện. Thời gian duyệt nằm ngoài kiểm soát kỹ thuật, nên không được coi là cam kết tiến độ.

## 5. Ngân sách chi phí

Chi phí phần mềm mục tiêu là 0. Mọi chi phí phát sinh phải được Chủ dự án duyệt trước.
