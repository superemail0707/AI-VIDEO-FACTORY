# HANDOFF TO CHATGPT – AI VIDEO FACTORY

Cập nhật lần cuối: 2026-10-30, sau khi push `fb3a19f` và xác nhận repo công khai. Tệp này được duy trì sau mọi phase và giữ lại lịch sử còn liên quan.

## 1. Trạng thái hiện tại

| Mục | Giá trị |
|---|---|
| Phase hiện tại | Phase 0 – Hồ sơ dự án, đã nghiệm thu |
| Tình trạng | **Phase 0: ACCEPTED** (Project Owner, 2026-10-30), chỉ ở mức tài liệu và thiết kế. **Phase 1: NOT AUTHORIZED** |
| Cổng đầu vào Phase 1 | Vẫn hiệu lực: quyết định D-013, D-017; trả lời Q-03, Q-06; kế hoạch Phase 1 được xác nhận |
| D-023 | **APPROVED — OPTION C** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Git checkpoint | Commit `def8fdf` và `fb3a19f` đã có trên `origin/main` (Project Owner cho phép; Claude xác minh hash khớp). Mỗi lần commit hay push tiếp theo cần cho phép riêng |
| Kết luận Codex mới nhất | **PASS — READY FOR OWNER ACCEPTANCE** (Final F-01 Verification) |
| Kết luận Codex vòng 4 | **APPROVED WITH CHANGES**, chỉ cho hồ sơ Phase 0 (`docs/operations/reviews/PHASE-00-REVIEW.md`) |
| Kết luận Codex vòng 3 | CHANGES REQUESTED |
| Kết luận Codex vòng 1 | NEEDS REVISION |
| Vòng 2 | Phát hiện do Chủ dự án chuyển; repo không có tệp báo cáo gốc |
| Quy tắc D-023 | Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API. Mở cổng cần G1–G5 (`docs/deployment/platform-verification.md` mục 3) |
| Workflow Claude–Codex | Mức B theo phê duyệt có điều kiện; tài liệu ở `docs/operations/AI_REVIEW_WORKFLOW.md`; Codex **APPROVED** tại RR-002; **Project Owner nghiệm thu** ngày 2026-10-30; mức C chưa đạt |
| SG-001 | **DONE** (Project Owner đóng, 2026-10-30); Amendment A01 đã áp dụng; đã dùng 1/3 vòng |
| RR-001 | Vòng 0/3: CHANGES REQUESTED, finding F-001, F-002 |
| RR-002 | Vòng 1/3: **APPROVED**, trạng thái `ANSWERED` |
| F-001, F-002 | **CLOSED** (Codex, RR-002) |
| Lượt làm việc | Project Owner. Không có RR đang mở. Claude đã dừng |
| Code ứng dụng | **NOT IMPLEMENTED** |
| Runtime testing | **NOT PERFORMED** |
| Phần mềm cài cho dự án, model AI, credentials | **Chưa có** |
| Git | Nhánh `main` ở `fb3a19f`, trùng `origin/main`; working tree sạch. **Repo từ xa CÔNG KHAI** (Project Owner xác nhận): không đẩy secret, credentials, dữ liệu vận hành, model hay media |

## 2. Phân biệt trạng thái

| Hạng mục | Tài liệu | Thiết kế | Chủ dự án duyệt | Triển khai | Kiểm thử |
|---|---|---|---|---|---|
| Bộ tài liệu Phase 0 | Xong | – | Đã nghiệm thu | – | Kiểm tra tài liệu đã chạy |
| `.gitignore` | Xong | – | Đã nghiệm thu | **Xong** | **Đã xác minh** bằng lệnh |
| Queue: fencing, staging, BUSY, orphan | Xong | `Proposed` | Chờ, trước Phase 2 | Chưa làm | Chưa làm |
| Máy trạng thái upload, adapter | Xong | `Proposed` | Chờ, trước Phase 15 | Chưa làm | Chưa làm |
| TikTok Direct Post | Xong | **`POLICY BLOCKED`** | D-023 `Approved` chỉ cho đánh giá; chưa có quyết định triển khai | Không được triển khai | Chưa làm |
| Truy cập cục bộ | Xong | `Proposed` | Chờ, trước Phase 2 | Chưa làm | Chưa làm |
| OAuth, token | Xong | `Proposed` | Chờ, trước Phase 15 | Chưa làm | Chưa làm |
| Rights Gate, gói xuất bản | Xong | `Proposed` | Chờ, trước Phase 13 | Chưa làm | Chưa làm |
| Spike TTS | Xong | Đã lên kế hoạch | Theo Phase 1 | Chưa làm | Chưa làm |
| Mọi tính năng sản phẩm | – | – | – | Chưa làm | Chưa làm |

**Không tuyên bố queue an toàn.** Thiết kế chỉ mới được lập luận. Chỉ có `.gitignore` là cấu hình đã có hiệu lực và đã xác minh.

## 3. Blueprint đã duyệt

Factory Manager + bảy Agent (Athena, Leonardo, Edison, Pixar, Spielberg, Tesla, Newton). Local-first, sequential-first, scene-based rendering, SQLite, Quality Gate, phê duyệt của con người trước khi xuất bản, adapter module hóa. Máy mục tiêu: MacBook Air M4 không quạt (`Mac16,12`), 16GB, macOS 26. Xem `PROJECT_MASTER.md`.

## 4. Phát hiện review

### Vòng 4

| Mã | Mức | Vấn đề | Tình trạng |
|---|---|---|---|
| R4-01 | LOW | Lựa chọn C có thể bị hiểu là được triển khai Direct Post | **CLOSED** ở mức tài liệu (Codex) |
| F-01 | LOW | Ba dòng hiện hành chưa đồng bộ D-023 | **CLOSED** (Codex Final F-01 Verification) |

### Vòng 3 (chi tiết ở `REVIEW_RESPONSE.md`)

| Mã | Mức | Vấn đề | Tình trạng |
|---|---|---|---|
| R3-01 | HIGH | TikTok Direct Post xung đột với mục đích dùng cá nhân; audit không đủ để mở khóa | Đã có quyết định D-023. **Rủi ro chính sách chưa giải quyết**, giữ `POLICY BLOCKED` |
| R3-02 | MEDIUM | `pending_outcome` chưa tách thành công và lỗi | Codex: PASS ở mức đặc tả; chưa kiểm thử |
| R3-03 | LOW | Đồng hồ lùi khi Worker đang sống | Codex: PASS ở mức đặc tả; chưa kiểm thử |

### Vòng 2 (chi tiết ở `REVIEW_RESPONSE.md`)

| Mục | Vấn đề | Tình trạng |
|---|---|---|
| B | `.gitignore` phủ định quá rộng, làm lộ secret trong fixtures | **Đã sửa và xác minh** |
| C | `SQLITE_BUSY` chưa có hành vi khi hết ngân sách | Đã đặc tả |
| D | Tiến trình con mồ côi | Đã đặc tả |
| E | Thiếu kịch bản fault injection | Đã đặc tả, nay là FI-01 đến FI-51 |
| F | OAuth, TikTok | Đã đặc tả |
| G | Rights Gate chưa có ranh giới bắt buộc | Đã đặc tả |
| H | YouTube, Facebook | Đã đặc tả; **Facebook vẫn chưa xác minh** |

### Vòng 1

| Mã | Vấn đề | Tình trạng |
|---|---|---|
| B1 | Thiếu fencing | Đã đặc tả, chờ duyệt D-011, D-018 |
| B2 | Kết quả upload không rõ | Đã đặc tả, chờ duyệt D-019 |
| B3 | Quyết định chưa được duyệt trước Phase 2 | **Mở, chờ Chủ dự án** |
| B4 | Chưa xác minh quyền API và license | **Mở có kiểm soát**, đóng theo từng tích hợp |
| W2 | Chưa có bằng chứng khả thi | **Mở**, cần số đo Phase 1, 14 |
| W8 | Chính sách API | Ảnh chụp đã cập nhật; xác minh lại trước mỗi adapter |
| W9 | `.gitignore` | **Đã đóng ở vòng 2** |
| W1, W3–W7, W10, R1–R10 | Xem `REVIEW_RESPONSE.md` | Đã xử lý hoặc ghi nhận |

## 5. Quyết định chờ Chủ dự án

Tất cả là `Proposed`. Không có mục nào được duyệt thay cho Chủ dự án.

| Trước phase | Quyết định | Khuyến nghị |
|---|---|---|
| 1 | D-013, D-017 | Duyệt |
| 2 | D-010, D-016, D-018, D-020 | Duyệt |
| 2 | D-009, D-011 (cùng D-018), D-015 (`.env`) | Duyệt có điều kiện |
| 4 | D-012 | Duyệt có điều kiện, sau số đo Phase 1 |
| 4 | D-014 | Hoãn tới Q-02 và số đo Phase 1 |
| 13 | D-022 | Duyệt |
| 15 | D-019, D-021, D-015 (Keychain) | Duyệt |

Đã duyệt: D-001 đến D-007, D-023 (chỉ cho đánh giá, không cấp quyền triển khai). Lead Developer: D-008.

## 6. Lịch sử thay đổi

**Bản sửa 1:** tạo `REVIEW_RESPONSE.md`, `HANDOFF_TO_CHATGPT.md`, ba đặc tả trong `docs/architecture/`, `docs/deployment/platform-verification.md`. Thêm D-018 đến D-022, spike TTS, cổng quyết định.

**Bản sửa 2:**

- `.gitignore`: chặn mặc định trong `tests/fixtures`, khối secret đặt cuối.
- `queue-safety.md`: viết lại; thêm `SQLITE_BUSY`, tiến trình mồ côi, `heavy.lock`, 43 kịch bản có đủ cột, oracle OR1–OR6. Thu hồi job chỉ lúc Worker khởi động.
- `publishing-reliability.md`: ranh giới adapter, TikTok, YouTube, Facebook, tiêu chí bổ sung.
- `security-and-rights.md`: `client_secret`, xác minh scope, token không tới dashboard, năm điều kiện tạo `queued`, `PublishGrant`.
- Cập nhật `platform-verification.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `DECISIONS.md`, `TECH_STACK.md`, các README trong `docs/`.

**Bản sửa 3:**

- R3-01: `platform-verification.md` mục 3, chặn TikTok ở `publishing-reliability.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `docs/requirements`; thêm rủi ro R13, D-023, Q-13.
- R3-02: `pending_outcome` hai loại `success`, `failure`; T11a–c; AC-Q18; FI-44 đến FI-49.
- R3-03: phát hiện và dịch lịch khi Worker đang sống, bước kẹp độc lập; AC-Q19; FI-32 sửa lại; FI-50, FI-51.

**Ghi nhận D-023 và R4-01:**

- D-023 `Approved`, phương án C; hai trạng thái độc lập; cổng G1–G5 ở `platform-verification.md` mục 3.
- `IMPLEMENTATION_PLAN.md`, `publishing-reliability.md`: bỏ cách viết khiến quyết định có thể bị hiểu là điều kiện đủ.

**Workflow mức B:** thêm `docs/operations/AI_REVIEW_WORKFLOW.md`; cập nhật `AGENTS.md`, `CLAUDE.md`, `TASKS.md`, `docs/workflows/README.md`, `docs/operations/README.md`. SG-001 và RR-001 nằm trong `TASKS.md`.

**Amendment A01:** Project Owner cấp thêm `REVIEW_RESPONSE.md` cho Claude và xác nhận reviewer artifact của Codex. Workflow chia file thành nhóm A, B, C. Vòng kế tiếp là 1/3, không đặt lại bộ đếm.

**Thay đổi kiến trúc:** không đổi blueprint, không thêm Agent, không đổi bộ công nghệ.

## 7. Lệnh và kiểm tra

Lệnh `.gitignore` và kết quả đầy đủ: `docs/operations/phase-reports/PHASE-00-REPORT.md`, Phụ lục 2. Codex đã chạy lại độc lập: 30/30 và 13/13 khớp. Kiểm tra Bản sửa 3: Phụ lục 3. Không có test tự động vì chưa có code.

## 8. Vấn đề đã biết

1. `tests/fixtures` chỉ lọc theo tên và đuôi tệp, không phát hiện secret trong nội dung tệp.
2. Orphan không nhận diện được chỉ bị giới hạn, không bị dừng.
3. `heavy.lock` không phủ yêu cầu đang chạy trong daemon Ollama.
4. Nếu không ai khởi động Worker, hoặc tiến trình ngoài giữ khóa DB vô thời hạn, job có thể vẫn `running` và cần người xử lý.
5. `flock` qua FFmpeg và hành vi `F_FULLFSYNC` là giả định thiết kế, cần thử thực tế.
6. Repo không có tệp báo cáo gốc của vòng 2.
7. `vi` (PID 3151) vẫn tạm dừng với buffer trống. **Không dùng `:w!` trong phiên đó.**
8. FI-43 chỉ kiểm tra đã gửi yêu cầu giải phóng model, chưa chứng minh tác vụ trong daemon Ollama đã kết thúc trước job mới.
9. Cách ly quyền Keychain giữa các tiến trình Python chưa được xác minh.
10. Luồng TikTok Upload vào inbox chưa xác minh: không rõ intended use và audit có áp dụng hay không.
11. F-01 đã đóng. `REVIEW_RESPONSE.md` Vòng 4 giữ nguyên làm lịch sử, nên vẫn trích câu chữ cũ.
12. `PROJECT_MASTER.md:8, 44` đã được sửa theo chỉ đạo của Project Owner: trạng thái nghiệm thu đã đồng bộ, tên máy đã bỏ.
13. `user.name` và `user.email` vẫn chưa được cấu hình. Hai commit đã tạo dùng danh tính `superemail0707` với email noreply do Project Owner chọn, truyền riêng cho từng commit; commit sau cần danh tính được cấu hình hoặc chỉ định lại. Chi tiết ở báo cáo Phase 0, mục "Chuẩn bị Git checkpoint".
14b. **Repo công khai.** Quét `HEAD` sau push: không secret, tên máy, đường dẫn cá nhân hay email; chỉ có tên tài khoản GitHub. Lịch sử Git không xóa sạch được nếu lỡ đẩy nội dung nhạy cảm, nên quét trước mỗi commit. Q-07 (sao lưu dữ liệu) cần tính tới việc này.
14. `refs/codex/turn-diffs/...` tồn tại trong `.git`. Khi push chỉ đẩy `main`, không dùng `git push --mirror`.

## 9. Trở ngại còn lại

1. Phase 0 đã nghiệm thu, nhưng Phase 1 chưa được phép bắt đầu. Nghiệm thu không xác nhận code đã triển khai hay runtime test đã pass.
2. Phase 1 cần D-013, D-017, Q-03, Q-06 và kế hoạch được xác nhận.
3. Phase 2 cần các quyết định ở mục 5.
4. Chưa có bằng chứng về TTS tiếng Việt, tốc độ render, nhiệt, RAM.
5. Chính sách nền tảng chưa đủ cho bất kỳ adapter nào; TikTok Direct Post `POLICY BLOCKED`; Facebook chưa xác minh.

## 10. Bước tiếp theo đề xuất

Không có Scope Grant đang chạy. Trước Phase 1, Project Owner quyết định D-013, D-017 và trả lời Q-03, Q-06. Claude không tự commit, push hay bắt đầu Phase 1.
