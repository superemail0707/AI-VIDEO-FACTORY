# Phản hồi Review Kiến trúc của Codex

Tài liệu gồm năm phần: **SG-001** (mới nhất), **Vòng 4**, **Vòng 3**, **Vòng 2** và **Vòng 1** (giữ nguyên làm lịch sử).

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
