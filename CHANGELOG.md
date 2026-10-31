# CHANGELOG

Ghi lại thay đổi đáng chú ý theo từng phase. Định dạng dựa trên Keep a Changelog.

## [Unreleased]

### Phase 1 – Bắt đầu bước 1.0 (2026-10-31)

#### Added

- `docs/operations/phase-reports/PHASE-01-PLAN.md`: kế hoạch Phase 1, Project Owner xác nhận 2026-10-31.
- `docs/testing/phase1-candidates.md`: dự thảo danh sách ứng viên và license, chờ Owner duyệt.

#### Changed (bản sửa sau Codex pre-approval review)

- `docs/testing/phase1-candidates.md` viết lại: phân loại A, B, C; hồ sơ từng ứng viên (nguồn, revision, quantization, voice ID, license, chuỗi quyền, tài nguyên, điểm chưa xác minh); tách bốn trạng thái phương pháp, kế hoạch, danh sách, quyền tải.
- Loại Piper `vais1000` (chuỗi quyền qua lessac/Blizzard 2013 chỉ cho nghiên cứu) và VieNeu-TTS 0.3B, 0.5B (dữ liệu CC BY-NC). Không còn TTS tiếng Việt nào đủ điều kiện nhóm B.
- `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`: đồng bộ; Codex re-review BLOCKED vì chưa có Scope Grant.

#### Changed

- D-013, D-017 `Approved`; Q-03 (có kiếm tiền), Q-06 (4 giờ) đã trả lời. Cập nhật `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`, `CURRENT_STATUS.md`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`.

#### Không có

- Cài đặt, tải model, code ứng dụng, commit, push. Bước 1.0 chỉ đọc tài liệu.

### Workflow mức B được nghiệm thu (2026-10-30)

Project Owner nghiệm thu tài liệu workflow mức B và đóng SG-001 sau khi Codex kết luận `APPROVED` tại RR-002. Đã dùng 1/3 vòng. Chỉ cập nhật dòng trạng thái trong workflow, không đổi quy tắc. Mức C chưa đạt. Không thay đổi phase.

Sau đó, theo cho phép của Project Owner: dọn trạng thái cũ trong `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`, và tạo một commit cục bộ trên `main`. Commit này chưa push.

### RR-002 vòng 1/3 (2026-10-30)

Codex kết luận `APPROVED`, đóng F-001 và F-002, không có finding mới. RR-002 chuyển `ANSWERED`. Workflow chưa được Project Owner nghiệm thu; SG-001 vẫn `ACTIVE`.

### SG-001 Amendment A01 (2026-10-30, chờ Codex vòng 1/3)

#### Changed

- `TASKS.md`: ghi Amendment A01 do Project Owner phê duyệt; RR-001 chuyển `ANSWERED`; đăng RR-002 tiếp nối, vòng 1/3, không đặt lại bộ đếm.
- `docs/operations/AI_REVIEW_WORKFLOW.md`: F-001, chia file thành nhóm A, B, C, thêm kiểm tra reviewer artifact theo số byte và SHA-256; F-002, quy định phản hồi finding, trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` và đường sau PASS.
- `AGENTS.md`, `CLAUDE.md`: làm rõ reviewer artifact, giới hạn của SHA-256 và điều kiện dừng.
- `REVIEW_RESPONSE.md`: phản hồi F-001, F-002.

#### Không có

- Code, script điều phối, cài đặt, commit, push, tạo nhánh, sửa báo cáo Codex, đóng finding, nghiệm thu workflow.

### Workflow Claude–Codex mức B (2026-10-30, chờ Codex review)

#### Added

- `docs/operations/AI_REVIEW_WORKFLOW.md`: Scope Grant, Review Request, kiểm tra đầu vào, quyền ghi, giới hạn 3 vòng, điều kiện dừng, mức A, B, C.
- `TASKS.md`: mục Scope Grants, Review Requests, SG-001, RR-001.

#### Changed

- `AGENTS.md`: lượt có thể đến từ Review Request hợp lệ trong Scope Grant; thêm kết luận `BLOCKED`; trỏ tới workflow.
- `CLAUDE.md`: nhánh phase chỉ dùng khi Chủ dự án cho phép; trỏ tới workflow.
- `docs/workflows/README.md`: thay mục quy trình lặp lại bằng liên kết; giữ quy tắc nhánh.
- `docs/operations/README.md`: thêm chỉ mục.

#### Không có

- Code ứng dụng, script điều phối, cài đặt, commit, push, tạo nhánh, thay đổi quyết định. Workflow chưa được kiểm chứng bằng một vòng thực tế.

### Phase 0 – Nghiệm thu

`2026-10-30 — Phase 0 accepted by Project Owner following Codex Final F-01 PASS.`

Nghiệm thu chỉ ở mức documentation/design. Không xác nhận application code đã triển khai, không xác nhận runtime test đã pass và không cho phép bắt đầu Phase 1.

Commit đầu tiên được tạo cục bộ trên `main` theo cho phép của Project Owner. Chưa push.

### Phase 0 – Sửa F-01 (2026-10-30)

#### Changed

- `PROJECT_MASTER.md`, `TECH_STACK.md`, `docs/requirements/README.md`: đồng bộ ba dòng hiện hành với D-023 `Approved — Option C` và Q-13 `Answered — Option C`. TikTok Direct Post vẫn `POLICY BLOCKED`; mục tiêu giữ trong roadmap.
- `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`: ghi R4-01 `CLOSED` theo Codex và F-01 chờ xác minh.

#### Không có

- Code, cài đặt, commit, push, thay đổi D-009 đến D-022, nghiệm thu Phase 0, bắt đầu Phase 1.

### Phase 0 – Ghi nhận D-023/Q-13 và khắc phục R4-01 (2026-10-30, chờ Codex kiểm tra lại)

#### Changed

- `DECISIONS.md`: D-023 chuyển sang `Approved` theo quyết định của Project Owner, phương án C. Bản ghi được chuyển sang mục "Đã duyệt", không tạo bản trùng. Tách Decision status và Direct Post integration status.
- `docs/deployment/platform-verification.md` mục 3: định nghĩa `POLICY BLOCKED` và năm điều kiện mở cổng G1–G5.
- `IMPLEMENTATION_PLAN.md`, `docs/architecture/publishing-reliability.md`: bỏ cách viết khiến quyết định D-023 có thể bị hiểu là điều kiện đủ để viết adapter.
- `CURRENT_STATUS.md`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`, báo cáo Phase 0: đồng bộ. Sửa dòng Git: đã có remote `origin`.

#### Không có

- Code ứng dụng, adapter TikTok, OAuth, gọi API, credentials, cài đặt, commit, push, thay đổi D-009 đến D-022, nghiệm thu Phase 0.

### Phase 0 – Bản sửa 3 theo Codex review vòng 3 (2026-10-30, chờ Chủ dự án quyết định)

#### Added

- `platform-verification.md` mục 3: xung đột TikTok Direct Post với mục đích dùng cá nhân, ba lựa chọn.
- D-023 ở trạng thái `Proposed`, Q-13, rủi ro R13.
- `queue-safety.md`: T11a–c, AC-Q18, AC-Q19, FI-44 đến FI-51.

#### Changed

- `queue-safety.md`: `pending_outcome` có hai loại `success`, `failure` với yêu cầu riêng; phát hiện đồng hồ lùi và dịch lịch khi Worker đang sống, kèm bước kẹp độc lập; FI-32 cấm khởi động lại.
- TikTok được đánh dấu bị chặn ở `publishing-reliability.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `docs/requirements`. Mục tiêu sản phẩm giữ nguyên chờ Chủ dự án quyết định.

#### Không có

- Code ứng dụng, phần mềm cài đặt, phê duyệt thay Chủ dự án, thay đổi mục tiêu sản phẩm.

### Phase 0 – Bản sửa 2 theo Codex review vòng 2 (2026-10-30, chờ Chủ dự án quyết định nghiệm thu)

#### Fixed

- `.gitignore`: bỏ `!tests/fixtures/**`, vốn làm secret, token, DB, model và media trong `tests/fixtures` không còn bị chặn. Thay bằng chặn mặc định, cho phép 7 định dạng văn bản, khối secret đặt cuối. Thêm `*.env`, `*.p8`, `*.jks`. Đã xác minh.
- `security-and-rights.md`: bỏ yêu cầu "cổng cố định" cho callback, không đúng với mọi nhà cung cấp.

#### Added

- `queue-safety.md`: `SQLITE_BUSY`, tiến trình mồ côi, `heavy.lock`, FI-22 đến FI-43, AC-Q10 đến AC-Q17, oracle OR1–OR6.
- `publishing-reliability.md`: ranh giới adapter, yêu cầu TikTok, YouTube, Facebook, AC-P12 đến AC-P17, PF-14 đến PF-22.
- `security-and-rights.md`: xác minh scope, `client_secret` desktop, token không tới dashboard, năm điều kiện tạo `queued`, `PublishGrant`, AC-S7 đến AC-S9, AC-R4 đến AC-R8.
- Ghi nhận chính sách ngày 2026-10-30 có nguồn.

#### Changed

- Thu hồi job chỉ xảy ra lúc Worker khởi động; `lease_expires_at` dùng để hiển thị `stalled`.
- Lược đồ khái niệm: thêm `packages`, `rights_reviews`, `publish_intents`; `approvals` gắn `package_sha256`.
- Phase 2, 3, 13, 15, 16: cập nhật tiêu chí nghiệm thu.
- D-018, D-019, D-021, D-022: mở rộng phạm vi, trạng thái vẫn `Proposed`.

#### Không có

- Code ứng dụng, phần mềm cài đặt, thay đổi bộ công nghệ, Agent mới, phê duyệt thay Chủ dự án, tuyên bố tuân thủ nền tảng.

### Phase 0 – Bản sửa 1 theo Codex review (2026-10-30, chờ review lần 2)

#### Added

- `REVIEW_RESPONSE.md`: phản hồi từng BLOCKER, WARNING, RECOMMENDATION.
- `HANDOFF_TO_CHATGPT.md`.
- `docs/architecture/queue-safety.md`: fencing, staging, phục hồi, tiêu chí nghiệm thu, fault injection.
- `docs/architecture/publishing-reliability.md`: máy trạng thái upload, đối soát, chống đăng trùng.
- `docs/architecture/security-and-rights.md`: mô hình đe dọa, OAuth, token, log, quyền nội dung, Rights Gate.
- `docs/deployment/platform-verification.md`: quy trình và ảnh chụp chính sách có nguồn.
- D-018 đến D-022, ở trạng thái `Proposed`.
- Spike TTS Việt–Anh trong Phase 1.
- `IMPLEMENTATION_PLAN.md` mục 6: cổng quyết định theo phase.

#### Changed

- `DECISIONS.md`: thêm rà soát D-009 đến D-017. Trạng thái giữ nguyên `Proposed`.
- `ARCHITECTURE.md`: gắn nhãn đề xuất; viết lại mục 5, 10, 11; thêm mục 15. Tập trạng thái job đổi thành `queued`, `running`, `succeeded`, `dead`, `cancelled`.
- `CURRENT_STATUS.md`: bỏ cách gom quyết định vào Q-01; không còn gọi Phase 0 là "triển khai xong".
- `TECH_STACK.md`: sửa ghi chú YouTube đã lỗi thời theo tài liệu chính thức.
- Bổ sung `docs/` về DB, Agent, kiểm thử, yêu cầu.

#### Không có

- Code ứng dụng, phần mềm cài đặt, thay đổi bộ công nghệ, Agent mới, phê duyệt thay Chủ dự án.

### Phase 0 – Hồ sơ dự án (2026-10-30, chờ nghiệm thu)

#### Added

- Tài liệu quản lý: `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`.
- Hướng dẫn AI: `AGENTS.md`, phần hướng dẫn mới trong `CLAUDE.md`.
- Tài liệu chi tiết trong `docs/`, mẫu báo cáo phase, báo cáo Phase 0.
- `.gitignore`.

#### Changed

- `CLAUDE.md`: thêm nội dung phía trên quy tắc bàn giao của Chủ dự án; quy tắc đó giữ nguyên.

#### Không có

- Code ứng dụng, phần mềm cài đặt, model AI, credentials, tích hợp mạng xã hội.
