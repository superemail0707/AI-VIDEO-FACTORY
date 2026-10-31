# HANDOFF TO CHATGPT – AI VIDEO FACTORY

Cập nhật lần cuối: 2026-10-31, sau khi Owner trả lời "1B, 2A, 4a, 4b" (Amendment A02 của SG-002). Tệp này được duy trì sau mọi phase và giữ lại lịch sử còn liên quan.

## 1. Trạng thái hiện tại

| Mục | Giá trị |
|---|---|
| Phase hiện tại | **Phase 1 – Môi trường & đo đạc nền, bước 1.0.** Phase 0 đã nghiệm thu |
| Tình trạng | **Phase 0: ACCEPTED** (Project Owner, 2026-10-30), mức tài liệu và thiết kế. **Phase 1: PLAN CONFIRMED — step 1.0 only** (Owner xác nhận kế hoạch 2026-10-31; `docs/operations/phase-reports/PHASE-01-PLAN.md`). Chưa được phép cài đặt hay tải model; mỗi lệnh cần xác nhận riêng |
| Cổng đầu vào Phase 1 | Q-03 (video **có** kiếm tiền, license phải cho phép thương mại) và Q-06 (chạy qua đêm, tối đa **4 giờ** cho một video, Owner đã xác nhận) đã trả lời 2026-10-31. D-013 và D-017 đã duyệt 2026-10-31. **Kế hoạch chi tiết Phase 1 đã được Owner xác nhận** (2026-10-31). Không còn cổng đầu vào Phase 1 nào chờ; Owner đã chọn tiêu chuẩn nhóm B là S2 (2026-10-31, nguyên văn "Chọn S2"); Codex đã APPROVED phân loại theo S2 tại RR-005; việc đang chờ là: Owner chọn hướng TTS tiếng Việt, Owner duyệt danh sách model, và quyền tải, cài, chạy từng bước |
| D-023 | **APPROVED — OPTION C** (Project Owner, 2026-10-30) |
| Q-13 | **ANSWERED — OPTION C** |
| TikTok Direct Post | **POLICY BLOCKED** |
| R4-01 | **CLOSED** (Codex focused re-review, ở mức tài liệu) |
| F-01 | **CLOSED** (Codex Final F-01 Verification) |
| Git checkpoint | Commit `def8fdf`, `fb3a19f`, `e83ecec` đã có trên `origin/main` (Project Owner cho phép; Claude xác minh hash khớp). Mỗi lần commit hay push tiếp theo cần cho phép riêng |
| Kết luận Codex mới nhất | **Phase 1.0 hồ sơ nghiên cứu: APPROVED tại RR-004** (vòng 1/3) **và phân loại theo S2 APPROVED tại RR-005** (vòng 2/3). Không phải PASS về license thương mại cuối cùng, danh sách benchmark hay quyền thực thi. **Chọn tiêu chuẩn S2 không thay việc Owner duyệt từng ứng viên và rủi ro dư kèm theo.** (Phase 0: PASS — READY FOR OWNER ACCEPTANCE tại Final F-01 Verification, đã nghiệm thu.) |
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
| SG-002 | **ACTIVE** (Project Owner, 2026-10-31): hồ sơ ứng viên Phase 1.0 và Codex re-review; giới hạn 3 vòng; đã dùng vòng 0, 1 và 2 (RR-003, 004, 005); còn **một vòng cuối (3/3)**. Claude không tự đóng; chỉ Owner quyết định đóng |
| SG-002 Amendment A01 | **APPROVED** (Owner, 2026-10-31): bốn file (`CHANGELOG.md`, `CURRENT_STATUS.md`, `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`) là nhóm A **chỉ đọc**; không đặt lại bộ đếm |
| SG-002 Amendment A02 | **APPROVED** (Owner, 2026-10-31, lời "1B, 2A, 4a, 4b"): Claude được ghi D-024 (tiêu chuẩn S2) vào `DECISIONS.md` và đồng bộ `CURRENT_STATUS.md`; `CHANGELOG.md` vẫn chỉ đọc; không đặt lại bộ đếm. Hai file đó đổi hash so với ảnh chụp RR-005 (thay đổi hợp lệ theo A02) |
| Mã 1B | Danh sách model: **chỉ Qwen3 4B `q4_K_M`**, kèm rủi ro dư; 8B chưa duyệt. Không phải quyền tải, cài, chạy |
| Mã 2A | Nghiên cứu TTS bằng tài liệu: VieNeu v3 Turbo **không có tệp LICENSE trong kho Hugging Face** (chỉ metadata và README), giữ nhóm A; ViZipVoice nhóm A; VietTTS, viXTTS nhóm C. **Vẫn không có TTS tiếng Việt nhóm B (R1)**. Các thay đổi này chưa được Codex review |
| D-024 | **APPROVED** (Owner, S2). **Mã 2G và 4c (Owner, 2026-10-31, nguyên văn "2G, 4C- xác nhận 1-8"):** điều 9 của PHASE-01-PLAN.md **bị bác**; điều 1–8 **được xác nhận**. R1 vẫn mở (báo Owner trước Phase 4 và 5). Mã 3a–3g, 4d, 4e, 4f **chưa trả lời**; chưa có quyền tải, cài, chạy. `CURRENT_STATUS.md` chưa phản ánh 2G/4c (ngoài phạm vi A02) |
| RR-003 | Vòng 0/3: **CHANGES REQUESTED** (Codex), `ANSWERED` |
| RR-004 | Vòng 1/3: **APPROVED** (Codex), `ANSWERED`. Reviewer artifact `docs/operations/reviews/PHASE-01-REVIEW.md` |
| P1-001, P1-002 | **CLOSED** (Codex, RR-004) |
| Quyết định S2 | **Owner chọn S2 ngày 2026-10-31** (nguyên văn "Chọn S2"). Dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận, chỉ cho ứng viên thỏa ba điều kiện, chỉ cho phân loại. Không phải kết luận pháp lý, duyệt danh sách hay quyền tải, cài, chạy. Chưa ghi vào `DECISIONS.md` (ngoài allowlist) |
| RR-005 | Vòng 2/3: **APPROVED** (Codex), `ANSWERED`. Phân loại Qwen3 4B, 8B lên nhóm B theo S2 được chấp nhận để **trình Owner**, không phải "đã duyệt" hay "sẵn sàng chạy" |
| Lượt làm việc | **Project Owner.** Không có RR đang mở. Claude đã dừng. `CURRENT_STATUS.md` đã đồng bộ theo A02. Còn vòng 3/3 của SG-002; chưa dùng. Claude không tự đóng SG-002, không commit, không push |
| Code ứng dụng | **NOT IMPLEMENTED** |
| Runtime testing | **NOT PERFORMED** |
| Phần mềm cài cho dự án, model AI, credentials | **Đã có (2026-10-31, Amendment A03):** Ollama 0.40.13 (Homebrew, kèm 10 gói phụ thuộc gồm `python@3.15`, `mlx`; Homebrew nâng lên 7.0.11) và model `qwen3:4b-q4_K_M` (digest khớp hồ sơ, SHA-256 blob tự tính). Đã tải thêm `qwen3:8b-q4_K_M` (A06, digest khớp, chưa chạy). **Đã đo thô Qwen3 4B** (A04, A05): nạp nguội 2.56 s, 34 token/s, RSS đỉnh 3,277 MB, `format` JSON schema 9/9 hợp lệ so với 2/9 không `format`; **Đo thô 8B (A07, không cô lập):** nạp 3.6 s, ~19 token/s, RSS đỉnh 5,796 MB, swap tăng ~740 MB; `format` giúp chia cảnh nhưng 8B ít lỗi hơn 4B khi không `format` (8/9 so với 2/9). Không bật dịch vụ nền. Credentials: chưa có |
| Git | Nhánh `main` ở `e83ecec`, trùng `origin/main`. **Working tree không sạch:** tài liệu Phase 1 và trạng thái chưa commit, chưa push. **Repo từ xa CÔNG KHAI** (Project Owner xác nhận): không đẩy secret, credentials, dữ liệu vận hành, model hay media |

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
| 1 | ~~D-013, D-017~~ | **Đã duyệt 2026-10-31** (D-013 chỉ duyệt phương pháp benchmark) |
| 2 | D-010, D-016, D-018, D-020 | Duyệt |
| 2 | D-009, D-011 (cùng D-018), D-015 (`.env`) | Duyệt có điều kiện |
| 4 | D-012 | Duyệt có điều kiện, sau số đo Phase 1 |
| 4 | D-014 | Hoãn tới Q-02 và số đo Phase 1 |
| 13 | D-022 | Duyệt |
| 15 | D-019, D-021, D-015 (Keychain) | Duyệt |

Đã duyệt: D-001 đến D-007, D-013, D-017, D-023 (chỉ cho đánh giá, không cấp quyền triển khai), D-024 (tiêu chuẩn S2, chỉ phân loại). Lead Developer: D-008.

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

1. Phase 0 đã nghiệm thu. Phase 1 chỉ được phép ở bước 1.0 (không cài đặt, không tải). Nghiệm thu không xác nhận code đã triển khai hay runtime test đã pass.
2. Cài đặt và tải model ở các bước sau cần xác nhận từng lệnh; danh sách ứng viên bước 1.0 cần Owner duyệt trước. Q-03, Q-06 đã trả lời; ngân sách 4 giờ chặt hơn giả định 8 giờ, nên mục tiêu một video mỗi ngày (R2) càng cần số đo thực.
3. Phase 2 cần các quyết định ở mục 5.
4. Chưa có bằng chứng về TTS tiếng Việt, tốc độ render, nhiệt, RAM.
5. Chính sách nền tảng chưa đủ cho bất kỳ adapter nào; TikTok Direct Post `POLICY BLOCKED`; Facebook chưa xác minh.

## 10. Bước tiếp theo đề xuất

SG-002 `ACTIVE` với Amendment A01. RR-003 (vòng 0/3) bị `CHANGES REQUESTED`; Claude đã sửa P1-001 và P1-002; **Codex kết luận APPROVED tại RR-004 (vòng 1/3) và đóng cả hai finding.** **Sau đó Owner chọn S2** (nguyên văn "Chọn S2"). Claude chuyển Qwen3 4B và 8B `q4_K_M` lên **nhóm B theo S2** (LICENSE Apache-2.0 và Ollama MIT đã đọc; dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận; giới hạn định danh đi cùng hồ sơ) và đăng RR-005 (vòng 2/3); **Codex kết luận APPROVED, không có finding mới**. Lượt thuộc về Owner; bảng quyết định cuối cùng ở `REVIEW_RESPONSE.md`. Bước 1.0: `docs/testing/phase1-candidates.md`. **Piper `vais1000` bị loại** (tinh chỉnh từ lessac, dữ liệu Blizzard 2013 chỉ cho nghiên cứu); VieNeu-TTS 0.3B và 0.5B bị loại (dữ liệu CC BY-NC); VieNeu v3 Turbo, Kokoro, Piper `ljspeech` nhóm A. Chưa có TTS tiếng Việt nào đủ điều kiện (R1). Báo cáo pre-approval gốc của Codex không có trong repo. Owner cần quyết định (độc lập nhau): hướng TTS tiếng Việt (`phase1-candidates.md` mục 7); duyệt danh sách model; quyền tải, cài, chạy từng bước; Amendment cho `CURRENT_STATUS.md` (đang lệch, còn ghi Qwen3 nhóm B theo cách cũ và lượt cũ). Claude không tự cài đặt, tải model, commit hay push.
