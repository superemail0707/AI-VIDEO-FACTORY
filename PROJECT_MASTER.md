# AI VIDEO FACTORY – PROJECT MASTER

> Nguồn sự thật cao nhất của dự án. Khi các tài liệu mâu thuẫn, thứ tự ưu tiên là:
> quyết định mới nhất của Chủ dự án → `PROJECT_MASTER.md` → `ARCHITECTURE.md` → `DECISIONS.md` → tài liệu còn lại.

| Thuộc tính | Giá trị |
|---|---|
| Trạng thái | Phase 0 – `ACCEPTED` (Project Owner, 2026-10-30), mức tài liệu và thiết kế. Phase 1 – `NOT AUTHORIZED` |
| Phiên bản tài liệu | 1.3 (2026-10-30) |
| Lead Developer | Claude |
| Independent Reviewer | ChatGPT Codex |
| Người quyết định cuối cùng | Chủ dự án |

## 1. Tầm nhìn

Xây dựng một hệ thống phần mềm chạy cục bộ trên máy Mac cá nhân, biến nội dung văn bản thành video hoạt hình 2D hoàn chỉnh, có dashboard quản lý toàn bộ quy trình, có kiểm duyệt của con người trước khi xuất bản và có thể mở rộng thành website hoặc ứng dụng sau này.

## 2. Mục tiêu sản phẩm

- Tạo video hoạt hình 2D từ văn bản, tiếng Việt và tiếng Anh, độ dài tối đa 10 phút.
- Hướng đến năng suất một video mỗi ngày.
- Hỗ trợ nhiều nhân vật, nhiều giọng đọc và lip-sync cơ bản.
- Bốn phong cách: stickman, whiteboard, educational explainer, storytelling nhiều nhân vật.
- Tạo phụ đề, thumbnail, metadata và tệp MP4.
- Đăng lên YouTube, TikTok và Facebook chỉ qua API chính thức và OAuth.
- Dashboard quản lý toàn bộ quy trình.

Mục tiêu đăng TikTok được giữ trong roadmap. D-023: `Approved — Option C`, ngày 2026-10-30, bởi Project Owner; Q-13: `Answered — Option C`. Phương án C chỉ cho phép tiếp tục nghiên cứu, đánh giá TikTok Direct Post. Direct Post tiếp tục `POLICY BLOCKED`: rủi ro chính sách R3-01 chưa được giải quyết, điều kiện G1–G5 vẫn bắt buộc trước khi đề xuất triển khai, và phải có quyết định triển khai riêng của Project Owner.

Chi tiết yêu cầu có mã số nằm tại [docs/requirements/README.md](docs/requirements/README.md).

## 3. Ngoài phạm vi (cho đến khi Chủ dự án quyết định khác)

- Hoạt hình 3D, video sinh bởi mô hình khuếch tán video, lip-sync chân thực.
- Dịch vụ cloud trả phí, GPU thuê ngoài.
- Tự động đăng bài không qua phê duyệt của con người.
- Đăng bài bằng công cụ không chính thức, giả lập trình duyệt, hoặc thư viện dùng API không công khai.
- Hệ thống nhiều người dùng, triển khai internet công khai.

## 4. Phần cứng cố định

| Hạng mục | Brief của Chủ dự án | Đã kiểm tra thực tế (2026-10-30) |
|---|---|---|
| Máy | Apple Mac | `Mac16,12` – MacBook Air, **không có quạt** |
| Chip | Apple M4 | Apple M4, 10 nhân CPU |
| RAM | 16GB | 16 GiB (bộ nhớ hợp nhất dùng chung CPU/GPU) |
| SSD | 512GB | Volume dữ liệu 460 GiB |
| Dung lượng trống | Khoảng 300GB | 342 GiB tại thời điểm kiểm tra |
| Hệ điều hành | macOS Tahoe 26 | macOS 26.0.1 (25A362) |
| Môi trường | Máy cá nhân | Máy cá nhân |

Hệ quả thiết kế từ phần cứng: chạy tuần tự, giải phóng model giữa các bước, chịu được gián đoạn (máy ngủ, gập nắp, giảm xung do nhiệt). Xem mục 8 của [ARCHITECTURE.md](ARCHITECTURE.md).

## 5. Kiến trúc đã duyệt – KHÔNG TỰ Ý THAY ĐỔI

Một **Factory Manager** điều phối bảy Agent. Agent là module logic độc lập, không bắt buộc mỗi Agent có một LLM riêng. Ưu tiên chạy tuần tự.

| # | Agent | Trách nhiệm |
|---|---|---|
| 1 | Athena | Research & Content Strategy |
| 2 | Leonardo | Scriptwriting & Storyboard |
| 3 | Edison | Text-to-Speech & Voice Casting |
| 4 | Pixar | 2D Animation & Lip-sync |
| 5 | Spielberg | Video Editing & Rendering |
| 6 | Tesla | Multi-platform Publishing |
| 7 | Newton | Analytics & Performance |

## 6. Công nghệ đã duyệt

Python, Ollama, FastAPI, SQLite, SQLite-backed Job Queue, Streamlit, SVG + Python, FFmpeg, Whisper/faster-whisper, TTS theo adapter, OAuth + API chính thức. MLX chỉ đánh giá ở giai đoạn tối ưu; OpenToonz là công cụ phụ trợ tùy chọn. Xem [TECH_STACK.md](TECH_STACK.md).

Được phép đề xuất thay đổi khi có bằng chứng kỹ thuật, nhưng phải ghi vào `DECISIONS.md` và được Chủ dự án duyệt trước khi thay đổi kiến trúc cốt lõi.

## 7. Nguyên tắc kỹ thuật

1. Local-first.
2. Modular architecture.
3. Sequential-first.
4. Scene-based rendering.
5. Retry từng tác vụ hoặc từng cảnh.
6. Có logging và trạng thái job.
7. Có Quality Gate.
8. Có human approval trước khi xuất bản.
9. Có kiểm tra bản quyền và license.
10. Không lưu mật khẩu hoặc API secret trong source code.
11. Không tự động xóa dữ liệu quan trọng.
12. Không dùng dịch vụ trả phí nếu chưa được Chủ dự án cho phép.
13. Ưu tiên phần mềm miễn phí và mã nguồn mở.

## 8. Quy tắc làm việc

**A.** Mọi công việc chia thành các phase nhỏ.

**B.** Trước mỗi phase phải trình bày: mục tiêu; file sẽ tạo hoặc sửa; công nghệ; lệnh cần chạy; rủi ro; cách kiểm tra thành công; cách quay lại nếu lỗi.

**C.** Không chuyển phase khi chưa có kết quả kiểm thử và nghiệm thu.

**D.** Sau mỗi phase cập nhật: `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`, và `DECISIONS.md` nếu có quyết định mới.

**E.** Không được tự ý: thay đổi kiến trúc; thêm dịch vụ cloud trả phí; thêm framework lớn không cần thiết; cài phần mềm hệ thống không giải thích; xóa hoặc ghi đè dữ liệu người dùng; tạo API token giả; tuyên bố một chức năng đã hoàn thành khi chưa chạy thử.

**F.** Trước khi chạy lệnh ảnh hưởng đến hệ thống, phải giải thích lệnh và yêu cầu xác nhận.

**G.** Mọi code phải có kiểm thử phù hợp.

**H.** Ưu tiên code rõ ràng, dễ bảo trì và có tài liệu.

## 9. Mô hình phối hợp

| Vai trò | Quyền | Giới hạn |
|---|---|---|
| Chủ dự án | Quyết định cuối cùng, nghiệm thu phase, cấp credentials | – |
| Claude (Lead Developer) | Thiết kế, viết code và tài liệu, chạy test | Dừng ở mỗi cổng nghiệm thu |
| Codex (Independent Reviewer) | Kiểm tra kiến trúc, code, bảo mật, chất lượng | Không sửa code khi chưa được Chủ dự án giao |

Hai AI không được đồng thời chỉnh sửa cùng một file hoặc cùng một nhánh Git. Quy trình đầy đủ tại [docs/workflows/README.md](docs/workflows/README.md).

## 10. Định nghĩa "Hoàn thành"

Một phase chỉ hoàn thành khi: tiêu chí nghiệm thu đạt và có bằng chứng chạy thật; test liên quan pass; tài liệu theo Quy tắc D đã cập nhật; có báo cáo phase và yêu cầu review cho Codex; Chủ dự án đã nghiệm thu.

Mọi trạng thái được ghi bằng đúng một trong các nhãn: **Đã triển khai & kiểm thử**, **Đã triển khai, chưa kiểm thử**, **Triển khai một phần**, **Chưa làm**.

## 11. Bản đồ tài liệu

| Tệp | Vai trò |
|---|---|
| `PROJECT_MASTER.md` | Tầm nhìn, phạm vi, ràng buộc, quy tắc |
| `ARCHITECTURE.md` | Thiết kế hệ thống |
| `IMPLEMENTATION_PLAN.md` | Lộ trình các phase và tiêu chí nghiệm thu |
| `TECH_STACK.md` | Công nghệ, trạng thái duyệt, license |
| `DECISIONS.md` | Nhật ký quyết định |
| `CURRENT_STATUS.md` | Trạng thái hiện tại |
| `TASKS.md` | Công việc |
| `CHANGELOG.md` | Lịch sử thay đổi |
| `HANDOFF_TO_CHATGPT.md` | Bàn giao để AI hoặc lập trình viên khác tiếp tục |
| `REVIEW_REPORT.md` | Báo cáo review kiến trúc của Codex |
| `REVIEW_RESPONSE.md` | Phản hồi của Lead Developer với từng phát hiện |
| `AGENTS.md` | Quy tắc cho Codex |
| `CLAUDE.md` | Quy tắc cho Claude |
| `docs/` | Tài liệu chi tiết theo chủ đề, xem [docs/README.md](docs/README.md) |
