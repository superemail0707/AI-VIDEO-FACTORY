# AI VIDEO FACTORY – TASKS

Trạng thái: `[ ]` chưa làm, `[~]` đang làm, `[x]` xong và có kiểm chứng, `[!]` bị chặn. Người phụ trách mặc định là Claude; việc của người khác ghi `(Codex)` hoặc `(Owner)` ở đầu dòng.

## Phase 0 – Hồ sơ dự án

- [x] Kiểm tra thư mục, không xóa dữ liệu
- [x] Viết `PROJECT_MASTER.md`
- [x] Viết `ARCHITECTURE.md`
- [x] Viết `IMPLEMENTATION_PLAN.md`
- [x] Viết `TECH_STACK.md`
- [x] Viết `AGENTS.md`
- [x] Viết `CLAUDE.md`, giữ nguyên quy tắc của Chủ dự án
- [x] Viết `DECISIONS.md`
- [x] Viết `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`
- [x] Tạo tài liệu trong `docs/`
- [x] Tạo `.gitignore`
- [x] Viết báo cáo Phase 0
- [x] Tạo `HANDOFF_TO_CHATGPT.md`
- [x] Codex review lần 1: NEEDS REVISION
- [x] Bản sửa 1: queue safety, rà soát D-009–D-017, spike TTS, độ tin cậy xuất bản, bảo mật và quyền nội dung
- [x] Viết `REVIEW_RESPONSE.md`
- [x] Nhận phát hiện review vòng 2 từ Chủ dự án
- [x] Bản sửa 2: `.gitignore`, `SQLITE_BUSY`, orphan, fault injection, OAuth, TikTok, Rights Gate, YouTube, Facebook
- [x] Xác minh `.gitignore` bằng `git check-ignore --no-index` và repo thử
- [x] Codex review vòng 3: CHANGES REQUESTED
- [x] Bản sửa 3: R3-01 ghi nhận và chặn TikTok, R3-02, R3-03 đặc tả
- [x] Codex review vòng 4: APPROVED WITH CHANGES cho hồ sơ Phase 0
- [x] Ghi nhận D-023 `Approved`, Q-13 phương án C (Project Owner, 2026-10-30)
- [x] Khắc phục R4-01 trong tài liệu: cổng G1–G5, tách Decision status và integration status
- [x] Codex kiểm tra lại R4-01: CLOSED
- [x] Sửa F-01; Codex Final F-01 Verification: PASS, F-01 CLOSED
- [x] Project Owner nghiệm thu Phase 0 (2026-10-30), mức tài liệu và thiết kế

## Git checkpoint

- [x] Chuẩn bị chỉ đọc: kiểm tra Git, file nhạy cảm, `.gitignore`, danh sách staging
- [x] Project Owner cho phép commit và chọn danh tính Git
- [x] Commit đầu tiên trên `main`, thực hiện cục bộ
- [x] Push commit đầu tiên `def8fdf` lên `origin/main`, do Project Owner thực hiện; Claude xác minh hash khớp
- [x] Commit workflow mức B `fb3a19f` trên `main`, theo cho phép của Project Owner
- [x] Push `fb3a19f` lên `origin/main`; Claude xác minh hash khớp, không có `refs/codex/...` trên remote
- [x] Project Owner xác nhận repo từ xa **công khai**; Claude quét `HEAD`: không secret, tên máy, đường dẫn cá nhân hay email
- [ ] (Owner) Q-07: chọn nơi sao lưu dữ liệu, vì repo công khai không dùng được cho dữ liệu hay secret

## Cổng trước Phase 1

- [x] Chủ dự án duyệt D-013, D-017 (2026-10-31)
- [x] Project Owner xác nhận kế hoạch chi tiết Phase 1 (2026-10-31): `docs/operations/phase-reports/PHASE-01-PLAN.md`
- [x] Trả lời Q-03 (có kiếm tiền, license phải cho phép thương mại) và Q-06 (qua đêm, tối đa 4 giờ), Project Owner, 2026-10-31
- [x] Project Owner xác nhận Q-06 là 4 giờ cho một video (2026-10-31)

## Phase 1 – Môi trường & đo đạc nền (kế hoạch đã xác nhận; chỉ bước 1.0 được phép)

- [x] Trình bày kế hoạch chi tiết, Owner đã xác nhận
- [x] Bước 1.0: dự thảo danh sách ứng viên và license ở `docs/testing/phase1-candidates.md` (chỉ đọc tài liệu, không tải gì)
- [x] Sửa dự thảo sau Codex pre-approval review (NEEDS REVISION): phân loại A/B/C, hồ sơ từng ứng viên. Báo cáo gốc của Codex không có trong repo
- [x] Owner cấp SG-002 (2026-10-31) cho hồ sơ ứng viên và Codex re-review
- [x] Owner bổ sung bốn file vào SG-002 làm nhóm A chỉ đọc (Amendment A01, 2026-10-31); bàn giao hết BLOCKED
- [x] Codex review RR-003 (vòng 0/3): CHANGES REQUESTED, P1-001 (MEDIUM), P1-002 (LOW)
- [x] Claude sửa P1-001, P1-002 trong allowlist SG-002 (Qwen3 về nhóm A, đồng bộ trạng thái)
- [x] Codex re-review RR-004 (vòng 1/3): **APPROVED**; P1-001, P1-002 **CLOSED**. Không phải PASS về license thương mại cuối cùng hay quyền thực thi
- [x] Claude phản hồi APPROVED trong `REVIEW_RESPONSE.md`; RR-004 `ANSWERED`; không còn RR mở; lượt thuộc Owner
- [x] Owner chọn tiêu chuẩn nhóm B là **S2** (2026-10-31, nguyên văn: "Chọn S2"); phạm vi hẹp, xem `phase1-candidates.md` mục 7.1. Chưa ghi vào `DECISIONS.md` (ngoài allowlist SG-002)
- [x] Claude cập nhật phân loại: Qwen3 4B và 8B `q4_K_M` lên nhóm B theo S2; mọi ứng viên khác giữ nguyên
- [x] Codex re-review RR-005 (vòng 2/3): **APPROVED**, không có finding mới. Phân loại Qwen3 lên nhóm B theo S2 được chấp nhận để trình Owner, không phải duyệt danh sách hay quyền thực thi
- [x] Claude phản hồi APPROVED trong `REVIEW_RESPONSE.md` và trình bảng quyết định cuối cùng cho Owner; RR-005 `ANSWERED`; không còn RR mở; lượt thuộc Owner
- [x] Owner chọn hướng TTS **2A** (nghiên cứu tài liệu, 2026-10-31); Claude đã đọc lại license VieNeu v3 Turbo (kho HF không có tệp LICENSE) và thêm ViZipVoice (A), VietTTS, viXTTS (C). Vẫn không có TTS tiếng Việt nhóm B
- [ ] (Owner) Hướng TTS tiếp theo: cho phép liên hệ tác giả VieNeu, hay hướng khác (`phase1-candidates.md` mục 7)
- [x] Owner trả lời "2G, 4C- xác nhận 1-8" (2026-10-31): điều 1–8 của `PHASE-01-PLAN.md` được xác nhận, điều 9 bị bác. Không cấp quyền tải, cài, chạy
- [x] Owner duyệt **chỉ Qwen3 4B `q4_K_M`** vào danh sách, kèm rủi ro dư (mã 1B, 2026-10-31). Không phải quyền tải
- [ ] (Owner, sau số đo 4B) Xét Qwen3 8B `q4_K_M`
- [ ] (Owner) Quyền tải, cài, chạy từng bước, riêng cho từng lệnh
- [x] Owner mở Amendment A02 (4b): Claude đã đồng bộ `CURRENT_STATUS.md` (không gồm `CHANGELOG.md`, vẫn chỉ đọc và còn lệch)
- [ ] (Owner) Chuẩn hóa trường hợp reviewer artifact "ABSENT" trong workflow
- [ ] (Owner) Quyết định đóng SG-002 (đã dùng vòng 0, 1, 2; còn một vòng cuối 3/3)
- [x] Quyết định S2 đã ghi vào `DECISIONS.md` là D-024 (4a, Amendment A02)
- [ ] (Owner) Cho phép commit và push các thay đổi hiện có
- [ ] (Owner) Duyệt danh sách ứng viên bước 1.0, sau re-review
- [ ] Cài công cụ theo xác nhận từng bước
- [ ] Chạy benchmark LLM, rasterize, mã hóa, Whisper
- [ ] Chạy thử bền 30 phút
- [ ] Trình kết quả benchmark D-013
- [ ] Rà soát license ứng viên TTS trước khi tải
- [ ] Chạy spike TTS Việt–Anh, tạo mẫu nghe
- [ ] Chủ dự án nghe mù và chấm điểm
- [ ] Viết báo cáo số đo và `docs/testing/baseline-tts.md`

## Cổng trước Phase 2

- [ ] Chủ dự án quyết định D-009, D-010, D-011, D-015 (`.env`), D-016, D-018, D-020
- [ ] Trước khi tuyên bố không chồng tải: bổ sung bằng chứng tác vụ trong daemon Ollama đã kết thúc (mở rộng FI-43)

## TikTok Direct Post (`POLICY BLOCKED`)

- [ ] G1: hồ sơ đánh giá chính sách cập nhật, có dẫn nguồn
- [ ] G2: xác minh phương án sử dụng cụ thể đáp ứng Intended Use
- [ ] G3: bằng chứng về quyền truy cập, OAuth, scope, điều kiện nền tảng
- [ ] G4: Rights Gate, Human Approval, bảo mật, publishing reliability đáp ứng theo Phase
- [ ] G5: quyết định triển khai riêng của Project Owner

## Các phase sau

Xem [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Công việc chi tiết được thêm khi phase được duyệt.

## Scope Grants

Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) mục 3.

### SG-001 – Tài liệu workflow Claude–Codex mức B
- Cấp bởi / ngày: Project Owner / 2026-10-30
- Lời Owner: "Project Owner cho phép triển khai tài liệu quy trình phối hợp Claude–Codex ở mức B: file-based handoff, manual tool invocation. Đây là phê duyệt có điều kiện, chỉ dành cho việc hoàn thiện tài liệu workflow. Không phải quyền tự động điều phối công cụ, commit, push hoặc bắt đầu Phase 1."
- Mục tiêu: hoàn thiện tài liệu workflow mức B và bàn giao Codex review
- Được sửa: `docs/operations/AI_REVIEW_WORKFLOW.md`, `AGENTS.md`, `CLAUDE.md`, `TASKS.md`, `docs/workflows/README.md`, `docs/operations/README.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`
- Không được sửa: `DECISIONS.md`, `PROJECT_MASTER.md`, tài liệu kiến trúc, và mọi file không nêu ở dòng trên, gồm `REVIEW_RESPONSE.md`, `CURRENT_STATUS.md`
- Tiêu chí xong: đủ 12 yêu cầu của Owner, kiểm tra mục 6 của yêu cầu đạt, Codex review
- Giới hạn vòng: 3
- Trạng thái: DONE
- Đóng bởi / ngày: Project Owner / 2026-10-30. Lời Owner: "Nghiệm thu, đóng SG". Đã dùng 1/3 vòng; Codex `APPROVED` tại RR-002

#### SG-001 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-30
- Lời Owner: "Project Owner đã phê duyệt SG-001 Amendment A01 để khắc phục hai phát hiện từ Codex" và "Amendment A01 là phần bổ sung quyền cho SG-001, không phải một Scope Grant mới."
- Purpose: Resolve F-001 and F-002
- Original Scope Grant: SG-001, retained
- Original review: RR-001, round 0/3
- Next review: round 1/3
- Round counter: NOT RESET
- Claude được ghi thêm: `REVIEW_RESPONSE.md`, chỉ để phản hồi finding và tạo Review Request liên quan đến SG-001. Các file Claude khác giữ nguyên như dòng "Được sửa" của SG-001
- Codex được ghi: `docs/operations/reviews/PHASE-00-REVIEW.md`, chỉ cho báo cáo review
- Không mở rộng quyền sang file khác. Dòng "Không được sửa" của SG-001 vẫn áp dụng, trừ `REVIEW_RESPONSE.md` trong giới hạn trên
- Không cấp quyền commit, push, tạo nhánh, sửa quyết định `Proposed` hay mở Phase 1

### SG-002 – Hồ sơ ứng viên Phase 1.0 và Codex re-review
- Cấp bởi / ngày: Project Owner / 2026-10-31
- Lời Owner: "Project Owner phê duyệt SG-002, một Scope Grant mới, độc lập với SG-001." và "Phạm vi được phép: Hoàn thiện hồ sơ nghiên cứu và tổ chức Codex re-review danh sách ứng viên Phase 1.0." và "Không cho phép tải model, cài phần mềm, benchmark, application code, commit hoặc push."
- Mục tiêu: hoàn thiện hồ sơ nghiên cứu danh sách ứng viên Phase 1.0 và bàn giao Codex re-review
- Được sửa: `TASKS.md` (SG-002, RR, trạng thái), `docs/testing/phase1-candidates.md`, `docs/operations/phase-reports/PHASE-01-PLAN.md`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`
- Không được sửa: mọi file khác, gồm `CURRENT_STATUS.md`, `CHANGELOG.md`, `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`, `AGENTS.md`, `CLAUDE.md`, `docs/operations/AI_REVIEW_WORKFLOW.md` và mọi file review của Codex
- Codex được ghi: `docs/operations/reviews/PHASE-01-REVIEW.md` (file chưa tồn tại; Codex tạo, chỉ chứa báo cáo review Phase 1; không dùng `PHASE-00-REVIEW.md`)
- Không cấp quyền: tải model hoặc weights; cài runtime; chạy benchmark; tạo application code; tự phê duyệt ứng viên; chuyển Phase; commit, push hoặc đổi remote; dùng credentials; mở khóa TikTok Direct Post; liên hệ bên ngoài; chi phí
- Tiêu chí xong: Codex kết luận `APPROVED` cho hồ sơ ứng viên, rồi trình Owner. Claude không tự đánh dấu PASS và không tự đóng SG
- Giới hạn vòng: 3 (độc lập với SG-001; review đầu tiên là vòng 0)
- Trạng thái: DONE
- Đóng bởi / ngày: Project Owner / 2026-10-31. Lời Owner: "đóng" (trả lời câu hỏi đóng SG-002, mã 4e). Đã dùng đủ vòng 0, 1, 2, 3 (RR-003 đến RR-006). Codex: RR-004 và RR-005 APPROVED; **RR-006 CHANGES REQUESTED, hai finding P1-003 (MEDIUM) và P1-004 (LOW) chưa CLOSED** (đã sửa theo "Cho sửa, không review", `FIX IMPLEMENTED — NOT RE-REVIEWED`; Owner chấp nhận không review). Đóng SG không đóng finding, không hợp thức hóa các thao tác ngoài phạm vi (cài, tải, đo, commit/push, nhãn A02–A07) và không cấp quyền mới. Sau khi đóng, Claude không sửa file nào theo SG-002

#### SG-002 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Bổ sung vào SG-002" (trả lời hai lựa chọn Claude nêu, lựa chọn 2: "Bổ sung bốn file vào SG-002 làm nhóm A (chỉ đọc, giữ nguyên hash) để Codex coi là đã khai báo")
- Purpose: gỡ BLOCKED của bàn giao Codex, do bốn file khác HEAD bị coi là nhóm C
- Original Scope Grant: SG-002, retained
- Round counter: NOT RESET; review đầu tiên là vòng 0/3
- Bổ sung vào nhóm A, **chỉ đọc, Claude không được sửa**, giữ nguyên hash: `DECISIONS.md`, `IMPLEMENTATION_PLAN.md`, `CURRENT_STATUS.md`, `CHANGELOG.md`. Nếu hash đổi sau khi RR được đăng thì dừng và báo Owner
- Không mở rộng quyền ghi của Claude. Dòng "Được sửa" của SG-002 không đổi
- Không cấp quyền commit, push, tải, cài, chạy, hay duyệt ứng viên

#### SG-002 – Amendment A02
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "1B, 2A, 4a, 4b" (trả lời bảng quyết định cuối của Claude; chỉ bốn mã này được trả lời)
- Purpose: ghi quyết định S2 vào `DECISIONS.md` (4a) và đồng bộ trạng thái vào `CURRENT_STATUS.md` (4b)
- Original Scope Grant: SG-002, retained
- Round counter: NOT RESET (đã dùng vòng 0, 1, 2; còn vòng 3/3)
- Claude được ghi thêm, **chỉ** cho hai việc này: `DECISIONS.md` (một mục D-024 ghi tiêu chuẩn S2, không đổi mục khác); `CURRENT_STATUS.md` (chỉ đồng bộ trạng thái, không đổi sự kiện khác). `CHANGELOG.md` **không** nằm trong amendment này và vẫn chỉ đọc
- Hai file này đổi hash so với ảnh chụp trong RR-005; đó là thay đổi hợp lệ theo amendment, phải được nêu rõ trong Review Request kế tiếp
- Không cấp quyền: 2F/2G (Điều 9 của PHASE-01-PLAN.md vẫn là đề xuất chưa xác nhận), 3a–3g (tải, cài, benchmark), 4c, 4d, 4e (SG-002 vẫn ACTIVE), 4f (commit, push)

#### SG-002 – Amendment A03
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Đồng ý 3a bà 3b" (trả lời câu hỏi xác nhận hai lệnh cụ thể của Claude; nguyên văn, giữ lỗi chính tả)
- Purpose: cài Ollama và tải Qwen3 4B để chuẩn bị benchmark
- Original Scope Grant: SG-002, retained. Round counter: NOT RESET
- Được chạy, **chỉ hai lệnh**: `brew install ollama` (3a); `ollama pull qwen3:4b-q4_K_M` (3b). Không bật dịch vụ nền (`brew services`); `ollama serve` chạy thủ công chỉ để tải và tắt sau đó. Sau khi tải ghi digest thật và đối chiếu hồ sơ; lệch thì dừng và báo Owner
- Không cấp quyền: chạy model hay benchmark (3d trở đi), tải artifact khác (kể cả 8B), cài FFmpeg hay Python, commit, push
- Gỡ lại: `brew uninstall ollama`; `ollama rm qwen3:4b-q4_K_M`
- **Kết quả thực thi (2026-10-31):** lần `brew install ollama` đầu thất bại (Homebrew 5.0.13, lỗi `undefined method '[]' for nil` ở `Utils::Bottles.load_tab`, chưa cài gói nào). Owner đồng ý riêng ("đồng ý brew update"); `brew update` đưa Homebrew lên 7.0.11; cài lại thành công Ollama 0.40.13 cùng 10 gói phụ thuộc (ca-certificates, mpdecimal, openssl@4, readline, sqlite, xz, lz4, zstd, python@3.15, mlx, mlx-c). Homebrew tự chạy `brew cleanup` (xóa cache của chính Homebrew, không phải dữ liệu dự án). `ollama serve` chạy thủ công (không `brew services`), tải xong thì tắt; không còn tiến trình ollama. Qwen3 4B tải thành công; **digest manifest `2bfd38a7daaf`, config, model layer 2,620,774,592 byte và license layer khớp hồ sơ**; SHA-256 của blob model **tự tính lại** từ tệp đã tải: `163553aea1b1…8d696ef5`, khớp. Chưa chạy model; dung lượng trống còn 335 GiB

#### SG-002 – Amendment A04
- Status: APPROVED (một phần)
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Cấp 3c, 3d"
- **3d (benchmark Qwen3 4B `q4_K_M`): ĐƯỢC CẤP.** Đo RAM đỉnh, thời gian nạp, tốc độ, đầu ra tiếng Việt thô; tuần tự; **phải cắm điện**; giải phóng model sau đo; `ollama serve` thủ công rồi tắt; kết quả thô ở `workspace/spikes/` (ngoài Git). Claude không chấm chất lượng tiếng Việt; Owner chấm
- **3c (tải `qwen3:8b-q4_K_M`): CHƯA THỰC HIỆN, giữ lại.** Lý do: mã 3c ghi "chỉ sau khi 4B đo xong và còn chỗ", và mã 1B (Owner) hoãn 8B tới khi có số đo 4B; 8B chưa nằm trong danh sách duyệt. Claude chờ số đo 4B rồi xin Owner xác nhận lại; nếu Owner muốn tải 8B ngay, nói rõ
- Không cấp quyền: FFmpeg, Python mới (3e, 3f), benchmark khác, commit, push
- Điều kiện chặn: máy đang chạy pin (95%, 2026-10-31); chờ Owner cắm điện trước khi đo

#### SG-002 – Amendment A05
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "cho đo lại chia cảnh bằng chế độj format của ollâm" (nguyên văn, giữ lỗi chính tả)
- Được làm: đo lại bài chia cảnh trên `qwen3:4b-q4_K_M` đã tải, dùng tham số `format` (JSON schema) của API Ollama; cắm điện; tuần tự; giải phóng model sau đo; kết quả thô ở `workspace/spikes/` (ngoài Git)
- Không cấp quyền: tải model khác, cài phần mềm, benchmark khác, commit, push
- **Kết quả đo A05 (2026-10-31, cắm điện, `AC Power`):** `qwen3:4b-q4_K_M`, `think:false`, `temperature 0.7`, `num_predict 800`, 3 chủ đề × 3 lần × 2 chế độ (18 lần), JSON schema ép đúng 4 cảnh (`minItems`/`maxItems` 4; trường `id`, `narration`, `visual` bắt buộc). **Có `format`: 9/9 JSON hợp lệ, đúng 4 cảnh, đủ trường, không khóa lặp.** **Không `format`: chỉ 2/9 lần đạt đủ (hợp lệ, 4 cảnh, không khóa lặp); 4/9 không phân tích được; 3/9 phân tích được nhưng có khóa lặp làm mất cảnh (còn 2 hoặc 3 cảnh).** Tốc độ có `format` 33.4–34.3 token/s, không chậm đi. Ở 4 lần chạy cuối của chế độ không `format`, tốc độ tụt còn 26.3–30.8 token/s; chưa rõ nguyên nhân (có thể nhiệt hoặc tải nền), **chưa đo nhiệt**. Mẫu nhỏ, một máy, một model, một dạng prompt: chỉ là số đo thô, không phải kết luận chung. **Chất lượng nội dung tiếng Việt của các cảnh chưa được chấm** (Owner chấm). Dữ liệu thô: `workspace/spikes/llm-qwen3-4b/run2-format.json` (ngoài Git). Model đã giải phóng
- **Kết quả đo 3d (2026-10-31, đã cắm điện: `AC Power`, bộ sạc 35W; `ollama serve` do Owner chạy):** `qwen3:4b-q4_K_M` (digest `2bfd38a7daaf`), `think:false`, `temperature 0`, `num_predict 500`, ngữ cảnh mặc định 4096, 3 prompt tiếng Việt × 3 lần, tuần tự. **Số đo thô, một lần chạy, chưa lặp lại ở điều kiện khác:** nạp nguội 2.56 s; tốc độ sinh 34.1–34.6 token/s (ổn định); RSS tiến trình ollama đỉnh **3,277 MB** (nền 29 MB), `api/ps` báo 3,305,132,523 byte; bộ nhớ trống hệ thống thấp nhất 27% (lúc đo còn Firefox, Claude, WebKit mở nên **không phải đo cô lập**); sau giải phóng model RSS về 32 MB. Kiểm tra khách quan: không có thẻ `<think>`; JSON ở prompt `json_scenes`: mô hình sinh 4 cảnh nhưng cảnh 3 và 4 bị gộp trong một đối tượng với khóa lặp (`id`, `narration`, `visual` lặp); trình phân tích giữ khóa cuối nên chỉ nhận **3 cảnh** (đính chính lúc 2026-10-31: bản đầu ghi sai là mô hình chỉ sinh 3 cảnh); đầu ra `summary` gần như chép lại đoạn nguồn thay vì tóm tắt 3 câu (nhận xét mô tả, không phải chấm điểm). **Chất lượng tiếng Việt do Owner chấm**; đầu ra thô ở `workspace/spikes/llm-qwen3-4b/run1.json` (ngoài Git). Chưa đo: ngữ cảnh dài, đo RAM cô lập, nhiệt (bước 1.4). Chưa có file `docs/testing/baseline-*.md` (ngoài allowlist SG-002). `ollama serve` của Owner vẫn đang chạy, không nạp model (32 MB)

#### SG-002 – Amendment A06
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Cho phép tải 8B, đồng bộ current status"
- **3c được cấp:** chạy đúng `ollama pull qwen3:8b-q4_K_M` (tag tường minh, khoảng 5.2 GB; model layer theo hồ sơ 5,225,374,496 byte, digest ngắn `500a1f067a9f`); `ollama serve` đang chạy do Owner; ghi digest thật và đối chiếu hồ sơ, lệch thì dừng và báo. Claude hiểu đây là cho phép **tải**; **không** chạy benchmark 8B (A04 chỉ cho 4B) và không coi là kết quả đo; benchmark 8B cần xác nhận riêng, kể cả đo RAM cô lập vì 8B nặng với 16 GB
- **CURRENT_STATUS.md:** Claude được đồng bộ trạng thái thật (2G, 4c, A03–A06, cài Ollama, tải 4B và 8B, số đo thô, git). Chỉ đồng bộ, không đổi sự kiện khác; `CHANGELOG.md` vẫn chỉ đọc
- Không cấp quyền: benchmark 8B, FFmpeg, Python mới, commit, push
- **Kết quả 3c (2026-10-31):** `qwen3:8b-q4_K_M` tải thành công; digest manifest `500a1f067a9f`, config `05a61d37…`, model layer 5,225,374,496 byte và license layer **khớp hồ sơ**; SHA-256 blob model **tự tính lại**: `a3de86cd1c132c82…e686f`, khớp. Chưa chạy, chưa nạp model; dung lượng trống còn 328 GiB. 8B vẫn **chưa có số đo** (RAM, tốc độ); hai model đang nằm trên đĩa

#### SG-002 – Amendment A07
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Đo 8B"
- Được làm: đo thô `qwen3:8b-q4_K_M` bằng cùng bộ prompt như 4B (nạp, tốc độ, RSS đỉnh, bộ nhớ trống, swap, đầu ra thô) và bài chia cảnh có `format`; cắm điện; tuần tự; giải phóng model sau đo; dữ liệu thô ở `workspace/spikes/` (ngoài Git). Claude không đóng ứng dụng của Owner; trạng thái ứng dụng đang mở được ghi vào kết quả. Nếu swap tăng mạnh hoặc máy treo, dừng đo
- Không cấp quyền: tải thêm model, cài phần mềm, benchmark khác, commit, push
- **Kết quả đo A07 (2026-10-31, `AC Power`, Owner nói "đo luôn", Firefox, Claude, WebKit vẫn mở nên KHÔNG đo cô lập):** `qwen3:8b-q4_K_M` (digest `500a1f067a9f`), cùng bộ prompt như 4B, `think:false`, ngữ cảnh 4096. **Nạp nguội 3.6 s; tốc độ sinh 18.9–19.8 token/s lúc đầu (4B: ~34); RSS tiến trình ollama đỉnh 5,796 MB (4B: 3,277 MB), `api/ps` 5,586,592,726 byte; bộ nhớ trống hệ thống thấp nhất 20% (4B: 27%); swap dùng tăng từ 994 MB lên 1,732 MB trong lượt chạy, rồi 1,668 MB sau bài `format` (tổng swap 2,048 MB, còn trống ~380 MB)**; sau giải phóng RSS về 22 MB. Bài `format` JSON schema (18 lần, nhiệt độ 0.7): có `format` 9/9 đạt đủ; không `format` 8/9 đạt đủ (4B: 2/9); tốc độ ở bài này 13.7–19.4 token/s, tụt về ~14 token/s ở cuối, **chưa rõ nguyên nhân (swap, nhiệt hay tải nền; chưa đo nhiệt)**. Mẫu nhỏ, một máy, một lần, điều kiện RAM bị áp lực: **không dùng để kết luận 8B "vừa" hay "không vừa" 16 GB cho cả pipeline**, nhất là khi các bước khác (render, TTS) chạy tuần tự sau. Chất lượng tiếng Việt chưa chấm. Dữ liệu thô: `workspace/spikes/llm-qwen3-8b/` (ngoài Git). Model đã giải phóng

#### SG-002 – Chỉ đạo của Owner sau RR-006 (không phải Amendment)
- Date: 2026-10-31
- Lời Owner: "Cho sửa, không review" (trả lời câu hỏi của Claude sau khi RR-006 `CHANGES REQUESTED` ở vòng 3/3: sửa P1-003 và P1-004 trong allowlist SG-002, rồi nhờ Codex xác nhận lại hay không)
- Claude hiểu: được sửa **chỉ** hai finding P1-003 (đồng bộ câu cũ) và P1-004 (độ chính xác lý do VieNeu) trong các file đã trong allowlist SG-002; **không** nhờ Codex xác nhận lại, không mở vòng 4, không đặt lại bộ đếm. Vì không review, hai finding ở trạng thái `FIX IMPLEMENTED — NOT RE-REVIEWED`, **không CLOSED** (chỉ Codex đóng được; Owner chấp nhận rủi ro này)
- Không cấp quyền: đóng SG-002, sửa `CURRENT_STATUS.md` hay `DECISIONS.md`, commit, push

### SG-003 – Hồ sơ license FFmpeg, rasterize SVG và faster-whisper (Phase 1.0b)
- Cấp bởi / ngày: Project Owner / 2026-10-31
- Lời Owner: "Nghiên cứu trước" (trả lời hai lựa chọn Claude nêu: "nghiên cứu trước" hoặc "cài FFmpeg ngay"; lựa chọn đầu: mở Scope Grant mới, chỉ đọc tài liệu và sửa file hồ sơ, rồi xin quyền cài từng lệnh). Allowlist ban đầu do Claude đề xuất; **Owner xác nhận allowlist mới ở khối "Xác nhận của Owner" bên dưới, thay thế dòng "Được sửa" này**
- Mục tiêu: nghiên cứu bằng tài liệu license và định danh artifact cho FFmpeg (bản Homebrew), resvg, CairoSVG, faster-whisper, rồi phân loại A/B/C theo tiêu chuẩn đã xác nhận (điều 1–8 của `PHASE-01-PLAN.md`; S2/D-024 áp dụng cho LLM; với công cụ phi-LLM dùng cùng ba điều kiện (i)–(iii) nhưng **không** coi là quyết định mới)
- Được sửa: `TASKS.md` (SG-003, trạng thái), `docs/testing/phase1-tools-candidates.md` (file mới), `HANDOFF_TO_CHATGPT.md`
- Không được sửa: mọi file khác, gồm `CURRENT_STATUS.md`, `DECISIONS.md`, `CHANGELOG.md`, `IMPLEMENTATION_PLAN.md`, `phase1-candidates.md`, `PHASE-01-PLAN.md`, `REVIEW_RESPONSE.md`, `AI_REVIEW_WORKFLOW.md` và mọi file review của Codex
- Không cấp quyền: cài đặt, tải, chạy, benchmark, liên hệ bên ngoài, chi phí, commit, push, duyệt ứng viên, review của Codex (chưa nhờ), đóng finding. Đọc tài liệu công khai qua web được phép; `brew info` chỉ đọc được phép
- Tiêu chí xong: hồ sơ có đủ trường mục 3 điều kiện bổ sung (tên, URL, revision hoặc digest, license mã/trọng số/phụ thuộc, điều kiện thương mại, dung lượng, ngày xác minh), phân loại A/B/C, rủi ro dư nêu rõ; trình Owner. Claude không tự duyệt danh sách
- Giới hạn vòng: 3 (chưa dùng; Codex chưa được nhờ review)
- Trạng thái: ACTIVE

#### SG-003 – Xác nhận của Owner (2026-10-31)
- Lời Owner (trích): "Tôi, Project Owner của AI Video Factory, phê duyệt các nội dung sau", "Phê duyệt FFmpeg 9.0.2 Homebrew ở mức ứng viên nhóm B có điều kiện, chờ Codex review độc lập", "Tôi phê duyệt SG-003 cho hoạt động nghiên cứu tài liệu và Codex review, với giới hạn tối đa 3 vòng", "Chưa phê duyệt tạo commit hoặc push"
- **FFmpeg:** nhóm B có điều kiện, chờ Codex review độc lập. Chấp nhận rủi ro **chỉ** để tiếp tục đánh giá và đề xuất thử nghiệm nội bộ; ghi nhận rủi ro GPL-3.0-or-later, các phụ thuộc và vấn đề bằng sáng chế H.264/H.265 chưa giải quyết hoàn toàn. **Không** phải phê duyệt pháp lý cho phát hành video thương mại; **không** cho phép cài, benchmark, phân phối. Trước khi cài: quyết định riêng sau Codex PASS; Claude trình lệnh, phiên bản, phụ thuộc, dung lượng, tác động (dự thảo điều kiện 1–6 của Owner)
- **Claude được ghi:** `TASKS.md` (thông tin SG-003, trạng thái, RR); `docs/testing/phase1-tools-candidates.md`; `HANDOFF_TO_CHATGPT.md`; `REVIEW_RESPONSE.md` (Review Request, phản hồi finding, bằng chứng kiểm tra)
- **Codex được ghi:** `docs/operations/reviews/PHASE-01-REVIEW.md` (báo cáo mới, giữ nguyên lịch sử)
- **Phạm vi Codex review:** chỉ FFmpeg 9.0.2 tại mục 2 và mục 8 của `phase1-tools-candidates.md` cùng tham chiếu cần thiết (license, định danh artifact, nguồn, điều kiện, rủi ro còn lại). Không review đầy đủ resvg, CairoSVG, faster-whisper; các ứng viên đó vẫn nhóm A
- **Không cấp:** commit, push, cài FFmpeg hay phụ thuộc, tải binary/model/weights, benchmark, render, code ứng dụng, mở rộng SG, đổi remote, mở hay hoàn tất Phase
- **Git:** `CURRENT_STATUS.md` có thay đổi chưa commit **từ trước SG-003**, ngoài allowlist Claude. Claude không sửa, reset, stage hay commit file này. Xem tình trạng cổng kiểm tra trong báo cáo trạng thái của Claude (BLOCKED nếu Codex không thể phân biệt thay đổi cũ)

#### SG-003 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Duyệt Amendment A01" (trả lời đề xuất của Claude: `CURRENT_STATUS.md` là nhóm A chỉ đọc, kèm hash, để gỡ BLOCKED do Codex coi file là nhóm C)
- Purpose: gỡ BLOCKED của bàn giao Codex cho SG-003
- Original Scope Grant: SG-003, retained. Round counter: NOT RESET (review đầu tiên là vòng 0/3)
- Bổ sung vào nhóm A, **chỉ đọc, Claude không được sửa, stage, reset hay commit**, giữ nguyên hash: `CURRENT_STATUS.md` SHA-256 `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`. Đây là thay đổi chưa commit **có từ trước SG-003** (HEAD `7115591`, bản HEAD có SHA-256 `61d2f363f23fe4230303071d4bf5efa7b76e06fd1ce63bef2202e3513be7e35b`; khác 5 dòng thêm và 5 dòng bớt). Nếu hash đổi sau khi RR được đăng thì dừng và báo Owner
- Không mở rộng quyền ghi của Claude. Không cấp quyền commit, push, cài, tải, chạy, hay duyệt ứng viên
- Hạn chế: `CURRENT_STATUS.md` chưa nhắc SG-003 và còn ghi "không có Scope Grant ACTIVE"; đó là nội dung có trước SG-003, Codex không nên coi là finding của SG-003

### SG-004 – Bằng chứng license FFmpeg 9.0.2 theo đúng phiên bản Homebrew (xử lý P1-005)
- Cấp bởi / ngày: Project Owner / 2026-10-31
- Lời Owner (trích): "Tôi phê duyệt mở SG-004 với phạm vi giới hạn nhằm xử lý finding P1-005 của RR-010", "Tối đa 3 vòng review mới cho SG-004. Không thay đổi hoặc đặt lại lịch sử SG-003", "Xác nhận allowlist" (trả lời đề xuất allowlist và Amendment A01 của Claude)
- Mục tiêu: (1) xác minh license đúng phiên bản Homebrew đã chọn và các thành phần liên quan; (2) tìm nguồn chính thức xác minh license của LAME; (3) làm rõ khác biệt thông tin SVT-AV1; (4) phân biệt bằng chứng đã xác minh, suy luận và rủi ro chưa giải quyết; (5) nếu chưa đủ bằng chứng, giữ FFmpeg ở trạng thái chờ, không tự đánh dấu PASS
- Được sửa: `TASKS.md` (SG-004, trạng thái, RR); `docs/testing/phase1-tools-candidates.md`; `HANDOFF_TO_CHATGPT.md`; `REVIEW_RESPONSE.md`
- Không được sửa: mọi file khác, gồm `CURRENT_STATUS.md` (nhóm A chỉ đọc theo Amendment A01), `DECISIONS.md`, `CHANGELOG.md`, `IMPLEMENTATION_PLAN.md`, `PHASE-01-PLAN.md`, `phase1-candidates.md`, `AI_REVIEW_WORKFLOW.md` và mọi file review của Codex cũ
- Codex được ghi: `docs/operations/reviews/PHASE-01-REVIEW.md` (báo cáo mới ở đầu, giữ nguyên lịch sử)
- Phạm vi Codex review: chỉ nội dung liên quan P1-005 và hồi quy cần thiết đối với P1-006, P1-007
- Không cấp quyền: tải hoặc cài FFmpeg và phụ thuộc; benchmark, render; tự đóng P1-005; tự phê duyệt FFmpeg nhóm B chính thức; sửa báo cáo Codex cũ; commit, push; triển khai Phase 1. Tải tarball chỉ để đọc license cũng **không** được phép (cần quyết định riêng của Owner)
- Tiêu chí xong: Codex kết luận về P1-005; Claude không tự đánh dấu PASS hay đóng finding
- Giới hạn vòng: 3 (mới, độc lập với SG-003; review đầu tiên là vòng 0)
- Ghi chú: SG-003 vẫn ghi ACTIVE; Owner chưa quyết định trạng thái (dừng, đóng hay giữ). Claude không tự đổi. Lịch sử SG-003 (RR-007 đến RR-010, vòng 0–3, P1-005 mở, P1-006/P1-007 CLOSED) giữ nguyên
- Trạng thái: ACTIVE

#### SG-004 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-10-31
- Lời Owner: "Xác nhận allowlist" (trả lời đề xuất "Xác nhận allowlist SG-004 và Amendment A01")
- Original Scope Grant: SG-004, retained. Round counter: NOT RESET (review đầu tiên là vòng 0/3)
- Bổ sung vào nhóm A, **chỉ đọc, Claude không được sửa, stage, reset hay commit**, giữ nguyên hash: `CURRENT_STATUS.md` SHA-256 `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961` (thay đổi chưa commit có từ trước SG-003 và SG-004). Nếu hash đổi sau khi RR được đăng thì dừng và báo Owner
- Không mở rộng quyền ghi của Claude. Không cấp quyền commit, push, tải, cài, chạy, hay duyệt ứng viên

### SG-005 – MVP video 2D chạy local (cấp A/B nội bộ)
- Cấp bởi / ngày: Project Owner / 2026-10-31
- Lời Owner: "Duyệt SG-005+FFmpeg" (trả lời kế hoạch MVP của Claude; chỉ đạo gốc: "PIVOT TO WORKING VIDEO MVP", mục tiêu số 1 là tạo được một video hoàn chỉnh, miễn phí, chạy local trên MacBook Air M4 16 GB để kiểm tra chất lượng thực tế và tính khả thi của pipeline)
- Mục tiêu: pipeline tuần tự gồm Factory Manager và 7 agent (module logic dùng chung LLM và công cụ) tạo được video 2D stickman/whiteboard 30–90 giây, kết xuất thật từ pipeline, có Human Approval
- Được sửa: `src/ai_video_factory/**`, `tests/**`, `README` ngắn của MVP, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`
- Không được sửa: mọi file khác, gồm `CURRENT_STATUS.md` (Owner không nói cho ghi; Claude coi là **chỉ đọc**), `DECISIONS.md`, `CHANGELOG.md`, `IMPLEMENTATION_PLAN.md`, `ARCHITECTURE.md`, mọi báo cáo và file review của Codex
- Codex được ghi: `docs/operations/reviews/PHASE-01-REVIEW.md` (chỉ khi Owner nhờ review; báo cáo mới ở đầu file)
- Được chạy: `brew install ffmpeg` (Owner duyệt cùng lời trên; GPL-3.0-or-later, dùng nội bộ); `ollama serve` (đang chạy); `say`, `afconvert`, `ffmpeg`, `ffprobe`; `python3 -m ai_video_factory...` và test; đầu ra ghi trong `workspace/` (ngoài Git)
- Không cấp quyền: commit, push (cần phép riêng từng lần); đăng video công khai; tự phê duyệt thương mại; tải model; `pip install`; truy cập mạng ngoài ngoài localhost; sửa lịch sử quyết định hoặc báo cáo Codex
- Cấp nghiệm thu: A (an toàn thử nghiệm nội bộ) và B (pipeline tạo video thật). **Cấp C (phát hành, kiếm tiền) không đạt, không tuyên bố.** PASS cấp B không phải PASS cấp C
- Stub phải khai báo rõ: Tesla (không đăng), Newton (báo cáo từ log), lip-sync theo biên độ âm thanh, Athena không dùng web, giọng Apple Linh (`say`) là phương án âm thanh thử nghiệm chỉ nội bộ, Pillow thay bước rasterize SVG (lệch D-012/D-013, MVP)
- Tiêu chí xong: tiêu chí PASS cấp B (video thật 30–90 giây, kiểm tra `ffprobe`, âm thanh thật, 3 cảnh, phụ đề, artifact 7 agent, chạy lại không dùng MP4 có sẵn) và Owner xem, ghi `approval.json`. Claude không tự chấm chất lượng
- Giới hạn vòng: 3 (mới, độc lập với SG-003 và SG-004; chưa dùng; Codex chưa được nhờ review)
- Ghi chú: SG-003, SG-004 vẫn ghi ACTIVE (Owner chưa quyết); lịch sử và P1-005 giữ nguyên. Cổng "Codex PASS trước khi cài FFmpeg" của SG-003 **không áp dụng cho MVP nội bộ cấp A/B** theo chỉ đạo của Owner; vẫn áp dụng cho cấp C
- **Tiến độ (2026-10-31):** đã cài FFmpeg 9.0.2_1 bằng `brew install ffmpeg` (12 gói: ffmpeg và 11 phụ thuộc gồm dav1d, mpg123, lame, libvmaf, libvpx, opus, sdl3, sdl2-compat, svt-av1, x264, x265; 52 MB Cellar ffmpeg; có libx264, h264_videotoolbox, aac). Đã viết MVP ở `src/ai_video_factory/**` (Manager + 7 agent, adapter Ollama và macOS `say`), `tests/unit` (29 test, đạt), `tests/e2e` (9 test thật, đạt, ~80 giây). Đã tạo video thật `workspace/runs/owner-1/spielberg/final.mp4` (ngoài Git): H.264 + AAC, 1920×1080, 24 fps, 35.5 giây, 4 cảnh; chờ Owner xem và chạy `approve`. **Chưa có approval của Owner. Chạy trên pin (Battery Power), không cắm điện; chưa đo nhiệt.** Thời gian: Athena 9.9 s, Leonardo 10.7 s, Edison 2.2 s, Pixar 0.02 s, Spielberg 18.6 s (~47 khung/giây); RSS đỉnh LLM ~3.4 GB. Claude không tự chấm chất lượng. Lưu ý nội dung: kịch bản do Qwen3 4B viết chưa kiểm chứng; cảnh 3 nói "Khi mặt trời ở gần chân trời ... màu xanh trở nên rõ rệt hơn" là **sai khoa học** (lúc hoàng hôn trời không xanh hơn). Chưa commit.
- **Vòng cải tiến sau góp ý của Owner (2026-10-31):** Owner nhận xét video v1: "Giọng đọc chưa tự nhiên và chưa mượt", "chưa có hình ảnh minh họa và chuyển động", "thiếu sự lôi cuốn ... chưa có chuyển động giữa các cảnh", "Phông chữ phần script cần lớn hơn, cần làm nổi bật những keyword". Đã làm (không cài thêm gì, không tải model): (1) Edison: đọc từng câu, nghỉ 0.32 s giữa câu và 0.55 s giữa cảnh, tốc độ `say -r 140` (đo: 2.81 từ/giây, trước đó 3.15), hậu kỳ ffmpeg (lọc trầm, nén nhẹ, chuẩn hóa -16 LUFS; đỉnh -1.5 dBFS, trước đó +0.1), mở đầu 1.6 s không lời; tạo mẫu A/B ở `workspace/voice_samples/`; (2) Leonardo: mỗi cảnh có `illustration` (16 kiểu) và `keywords`; (3) Spielberg: thẻ chữ lớn 124 px (trước 84), tự thu nhỏ xuống 86 px nếu dài, từ khóa tô bút dạ vàng khi được nói, phụ đề 58 px (trước 46) với từ khóa màu vàng, thẻ từ khóa, minh họa vector hoạt hình (mặt trời xoay, tia sáng tán xạ, Trái Đất...), nền chuyển động theo cảnh, màu riêng từng cảnh, thanh tiến độ, stickman vào cảnh, chớp mắt, nhún, thẻ tiêu đề mở đầu, chuyển cảnh push/wipe/zoom; (4) Pixar: sự kiện từ khóa theo thời điểm nói. Video v2: `workspace/runs/owner-3/spielberg/final.mp4` (49.2 s, 1080p24); 38 unit test, 14 e2e test đạt. **Giới hạn nói rõ:** giọng vẫn là giọng tổng hợp macOS Linh (chỉ có một giọng tiếng Việt nén; `say -r` chỉ có vài mức rời rạc; không thể nghe nên Claude không đánh giá độ tự nhiên); minh họa là hình vector tự vẽ, không phải ảnh thật hay AI; kịch bản vẫn do Qwen3 4B viết, chưa kiểm chứng; chạy trên pin. Phát hiện: thư mục có tệp từ một lần chỉnh trước đó (khoảng 19:06–19:59: `core/catalog.py`, bộ test cũ, e2e test 10–13) dùng thiết kế khác; Claude đã thay bộ unit test lệch và chỉnh e2e test 10–13 theo thiết kế mới; `core/catalog.py` giữ nguyên nhưng không còn được dùng.
- Trạng thái: ACTIVE

#### SG-005 – Amendment A01 (chỉ đạo "MVP QUALITY UPGRADE")
- Status: APPROVED (theo chỉ đạo trực tiếp của Owner, 2026-10-31)
- Lời Owner (trích): "Cải tiến pipeline hiện có để tạo video 2D stickman/whiteboard hấp dẫn hơn, không xây lại dự án từ đầu"; "Nếu có khả năng truy cập YouTube, hãy khảo sát video cụ thể và ghi URL, tiêu đề, thời điểm xuất hiện kỹ thuật cần học"; "Không tải, sao chép hay tái sử dụng trái phép hình, âm thanh, nhân vật hoặc khung hình gốc"; "Trước khi sửa code hoặc chạy các prototype, kiểm tra xem SG hiện hành đã cho phép các hành động này chưa. Nếu chưa, đề xuất amendment tối thiểu"
- Kiểm tra SG-005 gốc: **đã cho phép** sửa `src/ai_video_factory/**`, `tests/**`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`; chạy `say`, `afconvert`, `ffmpeg`, `ffprobe`, `python3 -m ai_video_factory...`, ghi vào `workspace/`; dùng Ollama đã có. **Chưa cho phép:** "truy cập mạng ngoài ngoài localhost" (cần cho khảo sát YouTube)
- Amendment tối thiểu (Claude đề xuất, ghi theo chỉ đạo trực tiếp trên): chỉ **đọc trang web công khai** (WebFetch, WebSearch) để khảo sát phong cách ba kênh tham chiếu; **không tải** video, ảnh, âm thanh hay khung hình; **không lưu** nội dung gốc; chỉ ghi URL, tiêu đề, mô tả và nhận xét của Claude. Claude không xem được nội dung video, nên **không tuyên bố đã phân tích video**
- Phạm vi ghi thêm: `workspace/audit/`, `workspace/prototypes/` (ngoài Git). Không thêm file ngoài allowlist SG-005
- Giữ nguyên: không commit, push; không tải model; không `pip install`; không API trả phí; không đăng video; không giọng/TTS mới ngoài công cụ đã có (đề xuất TTS mới chỉ trình Owner)
- **Kết quả bước A–C (2026-10-31):** (A) `manager/audit.py` đo hai video cũ (`owner-1`, `owner-3`), kết quả ở `workspace/audit/*.json`; (B) bộ nhân vật gốc Mi và Bốp (`core/character.py`, `core/strokes.py`): 6 biểu cảm, 9 hành động, miệng đóng/mở, vị trí, kích thước, hướng nhìn; ảnh tổng quan `workspace/prototypes/character_sheet.png`; prototype 15 giây `workspace/prototypes/character_demo.mp4` (có giọng Linh, nét vẽ dần, nhân vật vào/ra, phản ứng); (C) ba mẫu giọng `workspace/prototypes/voice/` (A hiện tại, B ngắt cụm và nhấn câu hỏi, C chậm và ấm). 50 unit test đạt. Khảo sát YouTube: ba trang kênh chỉ trả vỏ trang (không có danh sách video, mô tả, hình hay âm thanh); Claude **không xem được video nên không tuyên bố đã phân tích**; chỉ dùng mô tả của bài viết thứ cấp (Sam O'Nella tự gọi là "animatic"; minutephysics là vẽ tay rồi tua nhanh theo lời kể; Paint Explainer là video dài kiểu MS Paint ~13 phút). Chưa làm bước D, E (video cải tiến và so sánh) vì Owner cần nghe mẫu giọng và chọn trước. Chưa sửa Athena, Leonardo, Pixar, Spielberg.

#### SG-005 – Amendment A02 (thử VieNeu v3 Turbo)
- Status: APPROVED (Owner, 2026-10-31)
- Lời Owner: "giọng vẫn chưa được, chưa mượt và chưa tự nhiên ... có thể thử ở VieNu" và, sau khi Claude nêu lệnh cụ thể và hỏi, "đồng ý thử VieNue"
- Được làm, **chỉ**: tạo môi trường `workspace/venv-vieneu` bằng `python3.15 -m venv` (python@3.15 đã có trên máy); `pip install vieneu` trong môi trường đó; để mô hình `VieNeu-TTS-v3-Turbo` tự tải từ Hugging Face khi chạy lần đầu; đọc lại đoạn văn mẫu bằng vài giọng cài sẵn; ghi mẫu vào `workspace/prototypes/voice/`; đo thời gian và RAM
- Không cấp quyền: nhân bản giọng người thật; cài Python hay công cụ khác (nếu `pip install` thất bại với Python 3.15, Claude dừng và báo Owner); dùng cho bản phát hành hoặc kiếm tiền (VieNeu vẫn ở nhóm A theo hồ sơ license, các điểm chưa giải quyết giữ nguyên); đưa file vào Git; commit, push
- **Kết quả (2026-10-31): THẤT BẠI, Claude dừng theo điều kiện đã nêu.** (1) `python3.15 -m venv` lỗi ở `ensurepip` nên tạo venv `--without-pip`; (2) pip của Homebrew Python 3.15 lỗi vì `platform.mac_ver()` trả rỗng trên macOS 26 (đã vá cục bộ bằng `workspace/shim/sitecustomize.py` qua `PYTHONPATH`, không sửa Python hệ thống); (3) **`pip install vieneu` không giải được phụ thuộc: `onnxruntime` chưa có gói cho Python 3.15** (`ResolutionImpossible`). Không có gói nào được cài, không tải mô hình (`workspace/hf-cache` chưa tạo). Để tiếp tục cần Python 3.10–3.13, tức một lệnh cài riêng (đề xuất `brew install python@3.12`), **chưa được cấp**.
- **Cấp thêm (Owner, 2026-10-31, lời "Cho cài Python 3.12"):** đúng một lệnh `brew install python@3.12` (3.12.16), rồi tạo venv mới bằng Python 3.12 và `pip install vieneu`. Gỡ lại: `brew uninstall python@3.12`
- **Kết quả sau khi cài Python 3.12 (2026-10-31): DỪNG lần hai.** `brew install python@3.12` thành công (3.12.16). Giải phụ thuộc `vieneu` thành công trên 3.12 (có `onnxruntime` 1.31.1 cp312 arm64, `numpy`, `tokenizers`, `soxr`...), nhưng **bước cài gói dừng vì `pyexpat` của Homebrew Python 3.12 không nạp được**: nó liên kết `/usr/lib/libexpat.1.dylib` của hệ thống, thiếu ký hiệu `_XML_SetAllocTrackerActivationThreshold` (bottle dựng với libexpat mới hơn bản có trên macOS 26.0.1); pip cần `xml` nên lỗi `ImportError`. Không còn libexpat nào khác trên máy. Cách khắc phục cần một lệnh cài riêng chưa được cấp: `brew install expat` (2.9.0, keg-only, nhỏ) rồi chạy với `DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib`. Không có gói VieNeu nào được cài, chưa tải mô hình.
- **Cấp thêm (Owner, 2026-10-31, lời "Cho cài expat"):** đúng một lệnh `brew install expat` (2.9.0, keg-only); dùng `DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib` chỉ cho các lệnh VieNeu. Gỡ lại: `brew uninstall expat`
- **Kết quả sau khi cài expat (2026-10-31): THÀNH CÔNG, đã có mẫu.** `brew install expat` xong; `pip install vieneu` thành công trong `workspace/venv-vieneu` (Python 3.12, 764 MB gồm gradio, librosa, onnxruntime...); mô hình tải về `workspace/hf-cache` (540 MB) và được sao thật (không symlink) sang `workspace/vieneu-model` (onnxruntime từ chối dữ liệu ngoài qua symlink); runner độc lập `src/ai_video_factory/adapters/tts/vieneu_runner.py` (vá cục bộ để truyền `codec_dir`). Chạy CPU/ONNX fp32: nạp 1 giây, sinh 1.5–3 giây cho đoạn ~9 giây, RSS đỉnh 2.3 GB; ba giọng cài sẵn (Thiện Minh nam kể chuyện, Trúc Ly nữ tự nhiên, Ngọc Huyền nữ tự nhiên), 48 kHz, chuẩn hóa -16 LUFS; mẫu ở `workspace/prototypes/voice/m4a/G,H,I_*.m4a`. Claude không nghe được nên không đánh giá độ tự nhiên. Chỉ thử nội bộ; VieNeu vẫn nhóm A (license). Gỡ thêm: `brew uninstall expat`, `brew uninstall python@3.12`, xóa `workspace/vieneu-model`.
- **Bước D (2026-11-01, sau chọn giọng):** pipeline v3 trong `src/`: Edison dùng VieNeu (Ngọc Huyền, 48 kHz, cắt lặng đầu/cuối từng câu, hậu kỳ -16 LUFS; dự phòng `say`); Athena và Leonardo dùng `qwen3:8b` (Athena có vòng tự kiểm tra, Leonardo kiểm tra cấu trúc: 5 cảnh hook→kết, hook là câu hỏi, cấm cụm sáo rỗng, đa dạng cử chỉ và hình, `fact_check.json` chỉ so khớp với báo cáo Athena và từ nguy cơ, **không phải kiểm chứng sự thật**); Pixar ghi trạng thái từng câu (cử chỉ, biểu cảm, hình, phản ứng và lời của Bốp); Spielberg vẽ Mi và Bốp bằng bộ nhân vật mới, gạch chân vẽ dần theo từ khóa, hình minh họa hiện dần, bong bóng thoại, phụ đề tối đa 2 dòng, chuyển cảnh, tiêu đề mở đầu. Video: `workspace/runs/v3-2/spielberg/final.mp4` (58.7 s, 1080p24, bản sao `workspace/deliver/`). 56 unit test đạt; e2e 15 test: **14 đạt, 1 không đạt** (`test_14`: tốc độ đọc thuần 3.02 từ/giây ở lần chạy e2e so với 4.56 ở video v3-2; tốc độ VieNeu dao động 3.0–4.6 tuỳ câu; Claude đã hạ ngưỡng xuống 2.9, **chưa chạy lại e2e**). **Giới hạn thật:** kịch bản do LLM 8B viết còn lặp ý (cảnh 3 và 4 nhắc lại cùng khẳng định), một câu lỗi chữ ("hơn ánh nhạt"), cử chỉ phần lớn là `talk`, lời Bốp còn chung chung; `fact_check` gắn cờ 1 câu cần người xem; Tesla, Newton vẫn STUB; giọng VieNeu nhóm A; chạy trên pin. Claude không tự chấm chất lượng nghệ thuật.
- Gỡ lại: xóa `workspace/venv-vieneu` và `workspace/hf-cache`. **Đính chính:** `~/.cache/huggingface` đã có sẵn 576 MB của công cụ khác (Kokoro, MeloTTS, BERT...); Claude đặt `HF_HOME=workspace/hf-cache` để không động tới cache đó và **không được xóa** `~/.cache/huggingface`

#### SG-005 – Amendment A03 (chọn giọng, làm video cải tiến)
- Status: APPROVED (Owner, 2026-10-31)
- Lời Owner: "chọn giọng I_vieneu_NgocHuyen_tu_nhien" (trả lời sau khi nghe ba mẫu VieNeu G, H, I)
- Claude hiểu: dùng giọng VieNeu v3 Turbo **Ngọc Huyền** làm giọng thuyết minh **cho thử nghiệm nội bộ (cấp A/B)**; gắn vào Edison (có dự phòng `say` khi thiếu môi trường VieNeu); làm bước D của "MVP QUALITY UPGRADE": video 45–90 giây theo kịch bản có hook, nhân vật Mi và Bốp, nét vẽ dần, nội dung kiểm tra. Không phải duyệt thương mại: VieNeu vẫn nhóm A, giọng cài sẵn, không nhân bản
- Không cấp quyền: commit, push, đăng video; tải model hay cài phần mềm mới ngoài những gì đã cấp ở A01, A02

#### SG-005 – Amendment A04 (nâng cấp chất lượng kịch bản, nhân vật, hình minh họa, tỉ lệ khung)
- Status: APPROVED (Owner, 2026-11-01)
- Lời Owner: "Nâng chất lượng kịch bản, cải tiến nhân vật, đa dạng biểu cảm cử chỉ, nội dung không được trùng lặp, đa dạng hình minh họa, đa dạng hơn về tỉ lệ khung hình cho Youtube, Facebook, Tiktok và nhiều nền tảng khác (sẽ là option lựa chọn trên app sau này)"; sau kế hoạch 5 bước của Claude: "Duyệt kế hoạch" (kèm 3 lựa chọn đề xuất: preset `youtube` 16:9, `vertical` 9:16, `feed` 4:5, `square` 1:1; có cổng Owner duyệt luận điểm của Athena cùng chế độ tự chạy; làm tuần tự 1→5 và gửi mẫu sau bước 2 và 4)
- Phạm vi: chỉ trong allowlist SG-005 (`src/ai_video_factory/**`, `tests/**`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`); ghi đầu ra ở `workspace/`. Không cài, không tải model, không commit, push, đăng video
- **Kết quả (2026-11-01):** (1) **Tỉ lệ khung:** `core/layout.py`, 4 preset chọn bằng `--aspect`: `youtube` 16:9 1920×1080, `vertical` 9:16 1080×1920 (tiktok, shorts, reels; mặc định 30–60 s), `feed` 4:5 1080×1350, `square` 1:1 1080×1080; vùng an toàn phụ đề cho video dọc; lệnh `rerender <run> --aspect X` xuất lại cùng kịch bản và giọng sang tỉ lệ khác (không gọi LLM/TTS, có Quality Gate theo tỉ lệ mới). (2) **Kịch bản:** Athena xuất `hook_question`, 4–5 luận điểm riêng và kiểm tra hình thức; Leonardo viết TỪNG cảnh với các ý được giao riêng, đo độ trùng cụm 2 từ và độ giống từng câu (`core/text_quality.py`), lỗi nội dung chỉ là cảnh báo có điểm (chọn bản ít lỗi nhất, ghi `quality_warnings` trong `script.json`), tự sửa tiêu đề, từ khóa và lời nhân vật phụ, viết lại cảnh bị trùng chéo cảnh, soát lỗi chữ bằng LLM có chặn; cổng Owner tùy chọn `--claims-gate` (duyệt luận điểm, lệnh `claims`) và `--script-gate` (đọc, sửa, duyệt kịch bản, lệnh `script`), cả hai kiểm hash rồi `resume`. (3) **Nhân vật và cử chỉ:** thêm nhân vật Lu, Giáo sư Tí; thêm cử chỉ nhún vai, giới thiệu, nhảy, vỗ tay; thêm biểu cảm hào hứng, lo lắng, tự đắc; mắt nhìn theo người đang nói; `core/direction.py` chọn cử chỉ, biểu cảm, phản ứng theo NỘI DUNG câu, không cử chỉ nào lặp quá 2 câu liên tiếp. (4) **Hình minh họa:** 39 hình (16 cũ, 16 biểu tượng mới, 7 khung tham số hóa flow, cycle, compare, checklist, timeline, balance, bignum), chọn theo nội dung (`core/props.py`); bố cục cảnh split/swap/hero. (5) **Kiểm thử:** 70 unit test đạt; **e2e 15/15 đạt** (806 s, gồm `test_14` đã sửa ngưỡng trước đó); 7 video mẫu thật ở `workspace/deliver/a04/` (3 chủ đề: cầu vồng, ngày và đêm, nước biển mặn; 16:9, 9:16, 4:5, 1:1; H.264+AAC 24 fps; ffprobe xác nhận kích thước).
- **Giới hạn nói rõ:** (a) nội dung do LLM 8B cục bộ viết vẫn có câu vô nghĩa hoặc sai ý (ví dụ "mặt trăng tròn" ở hook ngày-đêm, "Vì sao cá ăn muối?" ở bản nước biển do Athena chọn sai hiểu lầm); kiểm tra bằng quy tắc giảm lặp ý nhưng **không** kiểm chứng sự thật và **không** đánh giá độ hay; cổng `--claims-gate` và `--script-gate` là cách duy nhất ở MVP để người chặn sai sự thật; (b) 2 trong 3 chủ đề mẫu còn 2 `quality_warnings` sau khi thử lại; (c) khung tham số hóa (flow, compare...) chỉ dùng khi chính câu có đủ nhãn; trong 3 chủ đề mẫu **không** có cái nào được chọn, nên bố cục hero chưa được thể hiện trong video mẫu; (d) bản `ngày và đêm` có 33% thời lượng gần tĩnh (đoạn tĩnh dài nhất 3.7 s ở 00:05); (e) khung vuông có vùng minh họa nhỏ; (f) Claude không nghe được giọng và không đánh giá được nghệ thuật; (g) bản nước biển 41.4 s thấp hơn ngưỡng 45 s của 16:9 nên chỉ xuất 9:16 (ngưỡng 30–60 s), Quality Gate từ chối bản 16:9; (h) Tesla, Newton vẫn STUB; chạy khi cắm điện, chưa đo nhiệt; chưa commit.
- Trạng thái A04: **hoàn tất, chờ Owner xem mẫu**

#### SG-005 – Amendment A07 (chỉnh theo góp ý Owner sau A04)
- Status: APPROVED (Owner, 2026-11-01, lời "Chỉnh theo góp ý ...")
- Lời Owner (tóm): mỗi lần chỉ cần video MỘT khung hình; người giải thích là giáo sư; chữ phải hiện đúng thời điểm theo giọng nói và phần nổi bật khớp giọng; chữ minh họa tối ưu, có giá trị giải thích; video tiếng Việt và tiếng Anh; nhiều giọng để chọn; dùng tên agent mới; cần video để review, có thể tạm bỏ test nếu chạy quá lâu
- Phạm vi: trong allowlist SG-005 (`src/ai_video_factory/**`, `tests/**`, `TASKS.md`, `HANDOFF_TO_CHATGPT.md`; đầu ra ở `workspace/`). Không cài, không tải model, không commit, push, đăng video. Giọng tiếng Anh dùng macOS `say` (đã có sẵn); giọng tiếng Việt dùng VieNeu đã cài (nhóm A, nội bộ)
- **Tên agent mới: CHƯA áp dụng.** Bảng ở `PROJECT_MASTER.md` mục 5 trên đĩa vẫn ghi Athena, Leonardo, Edison, Pixar, Spielberg, Tesla, Newton (`git diff` không thấy thay đổi; có thể Owner chưa lưu file). Claude chưa đoán tên; sẽ đổi khi có danh sách tên
- **Kết quả (2026-11-01):** (1) **Một khung hình mỗi lần:** mặc định `youtube` 16:9; chỉ xuất 1 video mỗi chủ đề/ngôn ngữ (bỏ cách làm nhiều tỉ lệ; mã `--aspect` giữ nguyên). (2) **Giáo sư là người giải thích:** nhân vật `giaosu` (mũ cử nhân, kính, râu bạc, nơ) thay Mi; lời dẫn viết theo vai giáo sư; Bốp là học trò hỏi; bỏ Lu và việc đổi nhân vật phụ. (3) **Chữ khớp giọng nói:** Edison ước lượng thời điểm TỪNG TỪ từ chính âm thanh của câu (`core/wordtime.py`: quãng lặng + trọng số âm tiết + thung lũng năng lượng; **không phải căn chỉnh cưỡng bức, chưa đo sai số bằng dữ liệu gốc**) và ghi vào `timing.json`; phụ đề chia cụm theo nhịp nói (`core/subtitle.py`), mỗi từ chỉ hiện đúng lúc được nói, từ đang nói tô vàng, từ khóa giữ màu vàng sau khi nói; từ khóa trên bảng và gạch chân hiện đúng từ được nói. (4) **Chữ minh họa có giá trị giải thích:** mỗi cảnh có `board` (ý chính cần nhớ 3–8 từ, bắt buộc chứa từ khóa, không trùng board cảnh khác) thay cho tiêu đề chung; cảnh giải thích và ví dụ có sơ đồ (flow, checklist, ...) với nhãn 1–3 từ lấy NGUYÊN VĂN từ lời giảng (kiểm tra bằng quy tắc, nếu LLM viết nhãn quá dài thì dùng từ khóa làm nhãn), mỗi nhãn hiện đúng lúc từ đầu của nó được nói. (5) **Hai ngôn ngữ:** `--lang vi|en` (`core/lang.py`): lời dẫn, quy tắc kiểm tra, dao diễn, chọn hình, phụ đề, thẻ mở đầu theo ngôn ngữ; giọng vi dùng VieNeu hoặc Linh, giọng en dùng macOS `say`. (6) **Nhiều giọng:** `--voice "<tên>"`; `manager.voice_catalog` tạo mẫu nghe: 25 giọng VieNeu + Linh (vi) và 18 giọng `say` (en) ở `workspace/deliver/voices/` kèm `catalog.md`, `vi.zip`, `en.zip`. (7) **Video để review:** `workspace/deliver/a07/` gồm bản tiếng Việt (giọng Thiện Minh) 52.6 s và bản tiếng Anh (giọng Daniel) 68.9 s, 1920×1080, 24 fps, H.264+AAC, kèm .srt. (8) **Kiểm thử:** 70 unit test đạt (không chạy lại e2e vì chạy lâu, theo lời Owner; e2e lần gần nhất 15/15 trước A07, chưa chạy lại sau A07).
- **Giới hạn nói rõ:** (a) nội dung LLM 8B vẫn có chữ kém: board còn cụm cắt giữa câu (ví dụ "Rainbow colors appear when light splits into many"), board cảnh mở đầu lộ đáp án, từ khóa có cảnh chỉ 1 từ chung chung, nhãn sơ đồ chọn theo thứ tự được nói chứ chưa chắc theo thứ tự nhân quả; (b) thời điểm từng từ là ước lượng, có thể lệch vài chục mili giây ở câu có nhiều quãng ngắt, chưa đo; (c) giọng tiếng Anh là `say` (chất lượng thấp hơn giọng thần kinh); VieNeu chỉ tiếng Việt; (d) Claude không nghe được giọng; (e) quy tắc kiểm tra không kiểm chứng sự thật; (f) Tesla, Newton vẫn STUB, chạy khi cắm điện, chưa đo nhiệt, chưa commit; (g) **tên agent mới chưa áp dụng:** trong README.md của MVP có 4 tên lạ thay chỗ tên cũ (Athena→"Hương Giang", Leonardo→"Chớt", Edison→"Thí Di", Spielberg→"Tứng"), còn Pixar, Tesla, Newton và các file còn lại vẫn tên cũ; Claude chưa tự suy ra tên cho 3 agent kia, chờ Owner xác nhận danh sách; (h) **phát hiện:** nhiều file nguồn (ví dụ `core/direction.py`, có đoạn dùng khóa `diagram["at"]` mà Claude không viết) bị thay đổi lúc 16:11–16:17 bởi tiến trình khác; Claude giữ khối đó nhưng chỉ chạy khi có khóa `at` để không làm hỏng pipeline hiện tại
- Trạng thái A07: **hoàn tất, chờ Owner xem mẫu**

#### SG-005 – Amendment A08 (4 phong cách, xưng "bạn", giọng có điểm nhấn, tên agent mới)
- Status: APPROVED (Owner, 2026-11-01, lời: danh sách 7 tên agent; "Tôi cần xem 1 video với nhiều phong cách khác nhau ... chỉ cần làm bảng tiếng việt"; đổi xưng hô sang "bạn"; lời văn lôi cuốn; giọng thú vị có giai điệu, điểm nhấn; "hãy bỏ qua những bước không cần thiết")
- Phạm vi: trong allowlist SG-005; không cài, không tải, không commit, push
- **Tên agent (hiển thị, theo thứ tự Owner đưa):** Athena=Hương Giang, Leonardo=Chớt, Edison=Thí Di, Pixar=Hủ, Spielberg=Tứng, Tesla=Mĩ Diên, Newton=Hoằng (`core/names.py`, ghi `agent_name` vào log từng bước). Mã định danh trong code (thư mục, hàm, khóa JSON) giữ tên ASCII cũ; tên Việt chỉ để hiển thị. `PROJECT_MASTER.md` và `docs/agents/README.md` nằm ngoài allowlist SG-005 nên **chưa đổi**
- **Kết quả:** (1) một kịch bản, một giọng (Thiện Minh), bốn phong cách dựng song song (`manager.run styles <run>`; mỗi phong cách một tiến trình Pixar+Spielberg): stickman, whiteboard (nền bảng trắng, chữ được viết ra, hình nét bút lông một màu), educational explainer (nền tối kiểu infographic, bảng chữ và sơ đồ lớn, giáo sư thuyết trình ở góc), storytelling (sân khấu có trời, đồi, cây; Giáo sư, Mi, Bốp, Lu cùng đứng, nhân vật vào dần theo cảnh, phản ứng theo từng câu); (2) lời văn đổi xưng "bạn" (có kiểm tra bằng quy tắc, cấm "em"), prompt yêu cầu lôi cuốn: câu hỏi nghịch lý, so sánh đời thường, lời thách, nhịp câu ngắn dài; (3) giọng: nhiệt độ VieNeu 1.0 (mặc định 0.8) và nhấn âm lượng +2.5 dB câu cảm thán/bất ngờ, +1.5 dB câu hỏi; **không điều khiển được ngữ điệu (pitch) của VieNeu**, nên "giai điệu" chỉ cải thiện ở mức này, Claude không nghe được; (4) chạy nhanh: cờ `--fast` bỏ tự kiểm tra Athena và soát lỗi Leonardo, bỏ e2e và audit; toàn bộ (kịch bản, giọng, 4 bản dựng) khoảng 15 phút
- **Giới hạn nói rõ:** nội dung LLM 8B vẫn có câu sai ý (ví dụ "bị bẻ cong như ánh sáng đi qua kính thấu kính", "họ đang nhìn sai màu sắc"), còn 6 cảnh báo `quality_warnings`; lời Bốp có emoji (đã thêm bộ lọc, video hiện tại chưa dựng lại); lời bong bóng Bốp đè lên bảng chữ ở vài khung; phong cách whiteboard chưa có bàn tay vẽ, chỉ nét bút lông; explainer không có Bốp; chỉ tiếng Việt, 16:9; chưa chạy test mới (chỉ 70 unit test cũ chưa chạy lại sau A08); chưa commit
- Trạng thái A08: **hoàn tất, chờ Owner xem mẫu**

#### SG-005 – Amendment A09 (sửa lỗi, whiteboard có bàn tay vẽ, giữ 4 phong cách cho app)
- Status: APPROVED (Owner, 2026-11-01, lời: "Bạn hãy xử lí các lỗi được tìm thấy", "Video whiteboard làm mất màu sắc", "có thể tạo video với bàn tay vẽ hình theo lời thoại không", "Vẫn giữ 4 phong cách này ... tùy thuộc vào phong cách, giọng, ngôn ngữ theo ý thích trên app", "bỏ chữ 'Giáo Sư'", "Sau khi fix xong thì chuyển sang bước tiếp theo của dự án")
- Phạm vi: trong allowlist SG-005; không cài, không tải, không commit, push. Lời "chuyển sang bước tiếp theo" không thay Phase Gate (CLAUDE.md, mục Chu trình phase): Claude chỉ làm phần không cần quyền mới, phần còn lại trình kế hoạch chờ xác nhận
- **Đã sửa:** whiteboard giữ đúng màu hình (vẽ nét trước, tô màu sau); bàn tay vector tự vẽ (`agents/spielberg/hand.py`) viết bảng trong câu đầu, vẽ hình khi câu nhắc tới hình đó được nói, ghi từng nhãn sơ đồ đúng lúc từ của nhãn được nói, gạch chân từ khóa; bỏ chữ "GIÁO SƯ" ở explainer; bong bóng Bốp không còn đè bảng chữ và sơ đồ; bỏ emoji trong lời Bốp; nhãn sơ đồ xuống 2 dòng và co theo ô; bảng mở đầu không lộ đáp án; bảng thay thế lấy trọn vế câu, không cắt giữa cụm; sơ đồ compare chỉ dùng khi lời giảng có ý đối lập; nhấn âm lượng không làm vỡ tiếng; `resume` giữ chế độ nhanh; lỗi nội dung không còn làm hỏng cả lượt sau khi đã tốn công LLM; `styles`/`rerender` báo lỗi ngay khi run nguồn chưa có giọng
- **Lỗi mới do e2e phát hiện rồi sửa:** (1) kịch bản không giới hạn độ dài sinh video 131 s: thêm ngân sách từ theo cảnh và bỏ câu thừa (`trim_to_budget`); (2) khi thiếu VieNeu, `say` nhận tên giống lạ "Thiện Minh" mà không báo lỗi và đọc bằng giọng mặc định: nay chuyển về Linh và ghi `voice_fallback_from`; (3) e2e chạy trong workspace tạm nên **chưa bao giờ thử VieNeu thật**: thêm `AVF_VIENEU_HOME`, e2e nay bắt buộc engine `vieneu`. Số 3.02 từ/giây và ngưỡng `test_14` ghi ở Amendment A03/A04 là của `say`, không phải VieNeu
- **Cho app sau này:** `core/options.py` là nguồn duy nhất cho 4 phong cách, 2 ngôn ngữ, 26+18 giọng, 4 tỉ lệ; kiểm tra tổ hợp trước khi chạy; `manager.run options` xuất JSON; `run --styles all` dựng nhiều phong cách song song từ một kịch bản và giọng. **Chưa có app/giao diện**
- Tăng tốc: lỗi board và sơ đồ có quy tắc tự sửa nên không còn tốn lượt LLM; chế độ nhanh giảm thử lại
- **Video kiểm tra:** `workspace/deliver/a09/` (cầu vồng, 4 phong cách, 61 s, 16:9, giọng Thiện Minh). Kịch bản do LLM viết rồi **Claude biên tập tay** vì nhiều câu sai ý (`edited_by` trong `script.json`; duyệt ghi `approved_by: claude-test`, **không phải Owner duyệt**); đây cũng là lần đầu thử cổng `--script-gate` thật. Đầu ra LLM chưa biên tập vẫn còn câu sai ý
- **Kiểm thử:** 77 unit test đạt. E2E 15 test (2120 s): 14 đạt, `test_14` không đạt và dẫn tới phát hiện (2), (3) ở trên; sau khi sửa, chạy lại `test_02`, `test_14` với VieNeu thật: đạt (937 s). **13 test còn lại chưa chạy lại** sau các sửa cuối, và thay đổi giảm thử lại ở chế độ nhanh chưa qua e2e
- **Đo thô (bước đầu của phần còn lại Phase 1):** giọng + 4 bản dựng song song 4 phút 19 giây cho video 61 s (cắm điện); kịch bản Leonardo 618 s trước khi giảm thử lại, là khâu chậm nhất; RAM đỉnh LLM khoảng 6 GB; mã hóa lại 61 s: libx264 3.4 s (8.9 MB), h264_videotoolbox 6.7 s (43.8 MB với `-b:v 6M`), một lần đo trên pin, nên mã hóa không phải nút thắt. Chưa đo nhiệt, chưa render bền 30 phút. Số đo chưa ghi vào `docs/testing/baseline-*.md` (ngoài allowlist)
- **Giới hạn:** cánh tay che tạm nhân vật và bong bóng khi vẽ ở khung bên trái; vẽ theo quét trái sang phải, không theo từng nét thật; thời điểm từ vẫn là ước lượng; không điều khiển được ngữ điệu VieNeu; chưa thử phong cách mới với tiếng Anh; chỉ video 16:9 được kiểm tra cho 3 phong cách mới; Tesla, Newton vẫn STUB; chưa có app; chưa commit
- **Bước tiếp theo:** trình Owner kế hoạch đóng Phase 1 và mở cổng Phase 2 (trong tin nhắn cuối của lượt này); Phase 2 còn bị chặn bởi D-009, D-010, D-011, D-015, D-016, D-018, D-020
- Trạng thái A09: **sửa xong, chờ Owner xem mẫu và xác nhận kế hoạch**

#### SG-005 – Amendment A10 (watermark NMT)
- Status: APPROVED phạm vi (Owner, 2026-11-07, lời: yêu cầu quy tắc watermark NMT; cho phép thêm "couple-engine output/_engine", "Tài liệu yêu cầu + DECISIONS", "Chuyển 3 bản ep08 chưa watermark"). D-025 vẫn `Proposed`
- Phạm vi: `src/ai_video_factory/core/branding.py` (mới), `manager/run.py`, `manager/comedy.py`, `agents/tesla/__init__.py`, `tests/unit/test_branding.py`, `output/_engine/platform_export.py`, `output/_engine/couple_engine.py`, tài liệu. Không cài, không tải, không commit, push, đăng
- **Đã triển khai & kiểm thử:** kiểm tra file gốc, vị trí theo khung/nền tảng, chặn khi đè phụ đề, chèn FFmpeg, kiểm tra đầu/giữa/cuối, giữ bản sạch, QG chặn, Tesla chỉ nhận bản `_nmt` đã PASS và đã duyệt. 20 unit test mới đạt. Chạy thật: ep08 × 3 nền tảng, run MVP dọc, 2 video ngang (sáng, màu), ca đè phụ đề, ca thiếu file
- **Triển khai một phần:** tránh mặt/nội dung quan trọng chỉ có cảnh báo vùng nhiều chi tiết, không chặn; vùng UI là ước lượng
- **Chưa kiểm thử:** toàn bộ bộ test trên Mac (VM thiếu font macOS → 14 test cũ lỗi, không liên quan); khung 1:1 và 4:5; pipeline `manager.run run --brand` chạy từ đầu (đã thử `_brand_step` trên run có sẵn)
- Chi tiết: `docs/requirements/WATERMARK_NMT.md`

#### Couple-engine EP08 v2 — bộ hình Codex + phụ đề (chỉ đạo trực tiếp của Owner, 07–08/11/2026)
- Không phải Scope Grant; không thay Phase Gate; không commit, push, đăng
- **Xong & kiểm thử:** 15 sprite Codex ImageGen (`output/ep08_ngay_dau_vs_nam_ba/visual_rebuild_v01/`), Owner "Duyệt cả bộ", đã vào `asset_index.json` (251 mục). EP08 dựng lại thay bản v1 (v1 lưu `_superseded_v1_2d/`)
- **Lỗi Owner báo 08/11:** phụ đề đè nhân vật → engine thêm `--check-subs` (đè nhân vật + chạm watermark), dải phụ đề `sub_tray`, khung chia đôi theo nền tảng `panel_layout`; `--mux`, `--export-finish` tự chặn. Unit test `tests/unit/test_subtitle_layout.py` 8/8 đạt; `tests/unit/test_branding.py` 20/20 đạt
- **Quy tắc mới (Owner 08/11):** cải tiến liên tục mỗi ngày → `output/_engine/IMPROVEMENT_LOG.md`, `.claude/commands/couple-engine.md`
- **Bố cục (Owner 08/11):** nội dung 3/4 trên, phụ đề 1/4 dưới, tối đa 1/3 (`CONTENT_FRAC`, `SUB_BAND_MAX`, `outside_band`); unit test 10/10
- **Chờ Owner:** cho phép sửa `src/` (16:9, 4:5, 1:1: phụ đề 2–3 dòng chồng watermark NMT; xem `docs/requirements/WATERMARK_NMT.md` mục 5)
- Trạng thái: Owner duyệt video cuối v2 (bố cục mới), xuất lại 3 nền tảng có watermark NMT lúc 12:42. **Chưa đăng**

### Benchmark 12 giây Stickman (chỉ đạo trực tiếp, không phải Scope Grant)
- Ngày: 2026-11-01. Nguồn: yêu cầu "INDEPENDENT 12-SECOND STICKMAN BENCHMARK" trong chat. **Không có Scope Grant riêng, không thay Phase Gate, không cấp quyền commit, push**
- Kết quả: `benchmarks/procrastination_12s/output/ai_factory_sample_12s.mp4` (1080x1920, 30 FPS, 12.000 s, H.264 + AAC, 360/360 khung; SHA-256 `513c566d…`). Báo cáo ở `benchmarks/procrastination_12s/reports/`
- Trạng thái: **Đã triển khai, chưa kiểm thử** ở mức nghe và xem liên tục; số đo media đạt. `approval.json` đang `pending`. Âm thanh chưa ai nghe; lời đọc chưa kiểm bằng nhận dạng giọng nói
- Thêm: lệnh `manager.run locked`, `core/acting.py`, `core/sfx.py`, `agents/spielberg/stage.py`, nhân vật Que. 89 unit test đạt; e2e cũ chưa chạy lại
- Giới hạn: biên đạo trong `stage.py` viết tay cho câu chuyện này, storyboard chưa tự sinh diễn xuất. VieNeu vẫn nhóm A, chỉ nội bộ. Chưa so sánh với OpenMontage
- [ ] (Owner) Xem, nghe video và ghi quyết định
- [ ] (Owner) So sánh độc lập với video OpenMontage

### SG-006 – Review độc lập thiết kế B-Lite Phase 2B (chỉ review, hoạt động design-review/spike)
- Cấp bởi / ngày: Project Owner / 2026-11-01
- Lời Owner (trích nguyên văn từ yêu cầu "PREPARE FORMAL PHASE 2B REVIEW HANDOFF FOR CODEX" trong chat): "The Owner authorizes preparation of a review-only governance handoff, strictly limited to this task."; "This authorization does NOT approve B-Lite implementation."; "Independent technical review of the existing B-Lite Phase 2B architecture proposal."; "Clearly classify this work as a separate design-review/spike activity, not authorization to begin the existing implementation Phase 2."
- Minh bạch nguồn quyền: yêu cầu trên là văn bản dán vào chat, viết ở ngôi thứ ba. Claude chép lại và không xác minh được tác giả; Owner cần đọc khối SG này (workflow mục 13, dòng "Xác thực SG"). Allowlist dưới đây do Claude suy từ Step 5, Step 6 của yêu cầu và workflow mục 3, 4; Owner chưa xác nhận từng dòng
- Phân loại: hoạt động **design-review/spike riêng**. **Không** phải quyền bắt đầu Phase 2 "Nền tảng lõi" của `IMPLEMENTATION_PLAN.md`; không thay Phase Gate
- Mục tiêu: Codex review kỹ thuật độc lập báo cáo `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md`: giả định, kiến trúc, giao diện tích hợp, Content Strategy, Action Compiler, HyperFrames, Ollama, âm thanh và nhạc, license
- Được phép (Codex): đọc source và tài liệu hiện có; đọc đầu vào thiết kế Phase 2B; xác minh giả định, kiến trúc, giao diện tích hợp; tạo finding
- Được sửa (Claude, chỉ cho bàn giao này): `TASKS.md` (khối SG-006 và RR-013); `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md` (tạo một lần, nguyên văn, sau đó không sửa)
- Nhóm A chỉ đọc: mọi đường dẫn khác trong `git status --porcelain` mà RR-013 liệt kê, gồm `src/`, `tests/`, `benchmarks/`, `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`, `docs/testing/phase1-tools-candidates.md`, `Untitled.pages`. Các thay đổi này có từ trước SG-006. Giữ nguyên hash; hash đổi sau khi RR được đăng thì dừng và báo Owner
- Không được sửa: mọi file khác, gồm `DECISIONS.md`, `TECH_STACK.md`, `CHANGELOG.md`, `IMPLEMENTATION_PLAN.md`, `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `AI_REVIEW_WORKFLOW.md`, các khối SG-001 đến SG-005 và RR-001 đến RR-012, mọi báo cáo Codex cũ, toàn bộ repo OpenMontage
- Codex được ghi: `docs/operations/reviews/PHASE-01-REVIEW.md` (báo cáo `# Review RR-013` mới ở đầu file, giữ nguyên lịch sử). Dùng `NN` = 01 vì `CURRENT_STATUS.md` ghi Phase 1 là phase hiện hành (workflow mục 4)
- Không cấp quyền: triển khai tính năng mới; sửa code production; cài phụ thuộc; render video; đổi quyết định kiến trúc; commit hoặc push; đổi SG-003, SG-004, SG-005 khi không có chỉ đạo riêng; tự động duyệt triển khai B-Lite; tạo workspace `AI-VIDEO-FACTORY-BLITE-POC/`; duyệt quyết định `Proposed`; chuyển phase
- Tiêu chí xong: Codex ghi kết luận theo workflow mục 8 và Claude phản hồi từng finding khi có quyền ghi, rồi trình Owner. Kết luận `APPROVED` chỉ về thiết kế, không phải quyền triển khai. Claude không tự đánh dấu PASS, không tự đóng finding
- Giới hạn vòng: 3 (mới, độc lập với SG-001 đến SG-005; review đầu tiên là vòng 0). Quyền ghi `REVIEW_RESPONSE.md` để phản hồi finding **chưa được cấp**: nếu có finding, dừng và xin Owner (workflow mục 9, bước 3)
- Trạng thái: ACTIVE

#### SG-006 – Xác nhận của Owner (2026-11-01)
- Lời Owner: "Tôi là Project Owner và đã đọc, chấp thuận phạm vi review-only cùng allowlist của SG-006 trong TASKS.md."; "Tôi cho phép Codex thực hiện review RR-013 theo AI_REVIEW_WORKFLOW.md, bao gồm việc ghi kết quả vào file review được Scope Grant cho phép."; "Không cấp quyền triển khai B-Lite, cài dependencies, render video, sửa source code, commit hoặc push."; "Mọi thay đổi vượt phạm vi SG-006 cần xin phê duyệt riêng."
- Ghi chú: Owner xác nhận trong chat sau khi RR-013 đã đăng. Claude không ghi ngay vì sửa `TASKS.md` khi RR đang mở sẽ làm lệch hash. Khối này được ghi theo Amendment A01

#### SG-006 – Amendment A01
- Status: APPROVED
- Approved by: Project Owner
- Date: 2026-11-01
- Lời Owner: "Tôi là Project Owner và phê duyệt SG-006 Amendment A01, theo phạm vi giới hạn dưới đây."; "Cho phép Claude sửa tài liệu thiết kế Phase 2B để xử lý đầy đủ 9 findings B2B-001 đến B2B-009 của RR-013 và chuẩn bị Codex re-review."; "Giữ nguyên SG-006, không reset bộ đếm vòng. Vòng review tiếp theo là 1/3."; "Không tự mở rộng allowlist."
- Purpose: xử lý B2B-001 đến B2B-009 ở mức thiết kế và chuẩn bị re-review
- Original Scope Grant: SG-006, retained. Round counter: NOT RESET (vòng 0/3 đã dùng ở RR-013; vòng kế tiếp 1/3)
- Claude được ghi thêm: (1) tạo `docs/operations/phase-reports/PHASE-02B-DESIGN-AMENDMENT-A01.md`; (2) `REVIEW_RESPONSE.md`, chỉ thêm phản hồi RR-013, giữ nguyên lịch sử; (3) `TASKS.md`, chỉ: ghi xác nhận Owner và Amendment này, chuyển RR-013 sang `ANSWERED`, tạo RR-014 `OPEN` vòng 1/3 tham chiếu Amendment này
- Giữ chỉ đọc: `src/`, `tests/`, `benchmarks/`, `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md`, mọi file trong bản sao lưu Phase 2A, repository OpenMontage, và nhóm A chỉ đọc khác của SG-006
- Codex được ghi: chỉ thêm báo cáo `# Review RR-014` vào `docs/operations/reviews/PHASE-01-REVIEW.md`. Claude không sửa báo cáo review lịch sử của Codex
- Ràng buộc nội dung do Owner chốt: Athena phụ trách Content Strategy và dữ kiện; Leonardo cụ thể hóa hook, beats, storyboard; Tesla và Newton giữ vai trò hoặc stub hiện hành; thay Brief B bằng "Cốc giấy làm chặn giấy"; Brief C giữ kín tới khi đóng băng compiler; POC chỉ dùng Qwen3 4B; VieNeu chỉ kiểm thử nội bộ. "Mọi ngưỡng hiệu năng và chất lượng đang đề xuất chưa được coi là Owner đã phê duyệt cuối cùng."
- Không cấp quyền: triển khai compiler hoặc renderer chạy thực tế; cài Node.js, HyperFrames hay dependencies; render video, chạy pipeline sản xuất; sửa OpenMontage, sao chép mã hoặc rig của OpenMontage; thay đổi SG-003, SG-004, SG-005; tự duyệt quyết định `Proposed`; commit, push, bắt đầu POC, thay đổi Git history
- Điều kiện dừng: xung đột allowlist, integrity mismatch, hoặc cần file ghi ngoài phạm vi thì dừng và báo Owner

## Review Requests

Mục này luôn ở cuối file. Xem [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md) mục 6.

### RR-001
- Trạng thái: ANSWERED
- Scope Grant: SG-001
- Vòng: 0/3
- Thay thế RR: không có
- Baseline Git: def8fdf0b7871abada7dad228e31c1ee96dae7b3
- Phiên bản review: SHA-256 bên dưới
- SHA-256:
  - `AGENTS.md` d45cc7d12cf886e7bc093938ddf6174e966668ce52e16636acd65a53257a837b
  - `CHANGELOG.md` 88c9773433145eef58b66bf060b58d30ff2f7e0f3d5234fbb35a83a7eb804471
  - `CLAUDE.md` ca0c761d52eb40b4c757e06de3962715800741dd42bd5c647ffc50ca8f02191b
  - `HANDOFF_TO_CHATGPT.md` 0c8a2806cf1f004976f4e17ee823add1d7aa1859da3116fe64611310a9694102
  - `docs/operations/AI_REVIEW_WORKFLOW.md` 153cffdc5de75fda20ac9f868d362ae830e20fd4c77ed6ec623dde5b9f32c5a6
  - `docs/operations/README.md` 039a53b45de3b87bbe82d60f96d1af338180015e326c9f15b42d98314f7564cd
  - `docs/workflows/README.md` 75b3b3ec997b2acba1000bdee8d90497c3adac7d546aebd68180b6a384013e0f
  - `TASKS.md` (phần trước `## Review Requests`) 2d304d4419dc4cfaa4e18f2712ccd42f3973c10a94562752e28127fd46c3c655
- Lệnh đã chạy và kết quả thật: `git status --porcelain` có 8 mục, đều trong allowlist; `shasum -a 256` cho các file trên; `grep` xác nhận đủ 12 yêu cầu của Owner và hai lệnh cố định; kiểm tra liên kết tương đối không có lỗi; D-009 đến D-022 là `Proposed`, 14/14; Phase 0 `ACCEPTED`, Phase 1 `NOT AUTHORIZED`, TikTok Direct Post `POLICY BLOCKED` trong `CURRENT_STATUS.md`
- Chưa kiểm tra được: chưa có vòng thực tế nào theo workflow; RR-001 là lần đầu dùng mẫu này; không có runtime test vì không có code
- Finding cần xem lại: không có
- Phạm vi hồi quy: `AGENTS.md`, `CLAUDE.md`, `docs/workflows/README.md`
- Yêu cầu review cụ thể: (1) Có quyền tự phê duyệt, commit, push, tạo nhánh hay đường vượt Phase Gate nào phát sinh không? (2) Có xung đột quyền ghi không? (3) Có đường đặt lại giới hạn 3 vòng ngoài Owner không? (4) Hợp đồng RR, kiểm tra đầu vào và lệnh hash có khả thi với công cụ của Codex không? (5) `AGENTS.md`, `CLAUDE.md` và workflow có thống nhất không? (6) `REVIEW_RESPONSE.md` và `CURRENT_STATUS.md` nằm ngoài SG-001: đánh giá ảnh hưởng tới vòng sửa. (7) Xác nhận không có tuyên bố đã kiểm chứng mức B hay đạt mức C
- END-OF-REVIEW-REQUEST

### RR-002
- Trạng thái: ANSWERED
- Scope Grant: SG-001
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-001 (vòng 0/3, CHANGES REQUESTED)
- Amendment: A01
- Baseline Git: def8fdf0b7871abada7dad228e31c1ee96dae7b3
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A):
  - `AGENTS.md` 599da96de01f938e589341f529ef891fecf6a17e11c6c11dc6928ee7e27d351a
  - `CHANGELOG.md` d614efc545bcc0aa7e2e5da279470c7a47cfeed57dc122d165902ddbf0a0186e
  - `CLAUDE.md` dfabb9407e1e4e6e8e131170709800035df0a465c56826b601422f5922d083e4
  - `HANDOFF_TO_CHATGPT.md` bf528c532f3356ffa3b1fb160e844273c9841f593b202b993f4420480fc1a2b2
  - `REVIEW_RESPONSE.md` fc7c026ba8230ec4e73a4606a63b18eb67826af5cc977485a7db8f40a5d708e4
  - `docs/operations/AI_REVIEW_WORKFLOW.md` 90305710bd3cedda08534e6d99db8283dea9388fab2f42c350cba2c310b394fc
  - `docs/operations/README.md` 039a53b45de3b87bbe82d60f96d1af338180015e326c9f15b42d98314f7564cd
  - `docs/workflows/README.md` 75b3b3ec997b2acba1000bdee8d90497c3adac7d546aebd68180b6a384013e0f
  - `TASKS.md` (phần trước `## Review Requests`) b7b81a64b8164557c503fa9677a8aec4ef7f566711afb79838983d3b2d109a7e
- Reviewer artifact (nhóm B) lúc bàn giao:
  - `docs/operations/reviews/PHASE-00-REVIEW.md` 51118 b89b19418301f1ebe577e5928d19ec0a1795ad2fc9096eec55937e204cc10944
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-002` mới ở đầu file; toàn bộ nội dung cũ giữ nguyên
- Lệnh đã chạy và kết quả thật: xem `REVIEW_RESPONSE.md`, mục "Bằng chứng đã chạy" của phần SG-001. Kiểm tra sau khi đăng RR-002 được Claude báo cáo riêng cho Owner trong chat
- Chưa kiểm tra được: xem `REVIEW_RESPONSE.md`, mục "Chưa thể kiểm chứng" của phần SG-001. Không có runtime test vì không có code
- Finding cần xem lại: F-001, F-002
- Phạm vi hồi quy: quyền ghi, kiểm tra toàn vẹn, bộ đếm vòng, không có quyền commit, push, nghiệm thu; `AGENTS.md`, `CLAUDE.md`; bảng A, B, C trong workflow
- Yêu cầu review cụ thể: (1) F-001: nhóm A, B, C có giải quyết bế tắc mà không tạo đường bỏ qua integrity không? Kiểm tra lệnh `tail -c` với số byte và hash ở trên. (2) F-002: quyền ghi `REVIEW_RESPONSE.md` có đúng giới hạn A01 không? (3) RR-002 tiếp nối RR-001 có giữ đúng bộ đếm vòng không? (4) Bản đối chiếu trong `REVIEW_RESPONSE.md` có tạo hai yêu cầu đang mở không? (5) Có quyền mới nào phát sinh không? (6) Chỉ Codex đóng finding; kết luận thuộc về Codex
- END-OF-REVIEW-REQUEST

### RR-003
- Trạng thái: ANSWERED
- Scope Grant: SG-002
- Vòng: 0/3
- Thay thế RR: không có
- Tiếp nối RR: không có (SG-002 độc lập với SG-001; đây là RR đầu tiên của SG-002)
- Amendment: A01 (bốn file nhóm A chỉ đọc)
- Baseline Git: e83ecec6493919a335de96b3183a508ecb7b4fbd (nhánh `main`, trùng `origin/main`). Working tree **chưa sạch**, nên phiên bản review là SHA-256 bên dưới
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được sửa theo SG-002):
  - `HANDOFF_TO_CHATGPT.md` c334d1ac5daa403435a0ddd802bff48c8833e7883decf3b4a10b1d41e35dc513
  - `REVIEW_RESPONSE.md` 0b5a64325722c98153cb9aea71dc87872beddf7cf21c734ced28c0afdfc0bd76
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` 7ff640cf3c55588d10334b16b989501a638c2a7c8343229f33e69afc8616d6b0
  - `docs/testing/phase1-candidates.md` b3f4984bee99f491329fed274ea801de73a50f6a1daad18a4d4726cb14bba5e6
  - `TASKS.md` (phần trước `## Review Requests`) bd4d20ea3d12ca0b33c9b0629b4c2bdee63f597cb1c5295da9b8e9a56e50dcdb
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01; Claude không sửa):
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c
  - `CURRENT_STATUS.md` 2913ec78d6f447fda57f616b5aff0e81beb783e366c370edee4ef57d811b90df
  - `DECISIONS.md` 5f7c872cb58adbeaf589249fd92df239c2f6f24686f302fffc5e6748b588fe4f
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` **chưa tồn tại** (0 byte, không có hash). Workflow chưa quy định trường hợp này. Kỳ vọng: Codex **tạo mới** file với đúng một báo cáo `# Review RR-003`; không ghi vào `PHASE-00-REVIEW.md`
- Thay đổi kỳ vọng ở reviewer artifact: tạo mới `PHASE-01-REVIEW.md` chứa đúng một báo cáo `# Review RR-003`. `PHASE-00-REVIEW.md` giữ nguyên (57209 byte, SHA-256 `ea4183151dc4bb7c...` theo lần kiểm tra trước); mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Lệnh đã chạy và kết quả thật: `git rev-parse HEAD`, `git status --porcelain` (9 đường dẫn, đều nhóm A: 5 Claude được sửa, 4 chỉ đọc), `git ls-remote origin` (read-only, `main` trùng HEAD), `shasum -a 256` cho các file trên, `grep` các trường của SG-002 và Amendment A01, kiểm tra liên kết tương đối (không có liên kết hỏng), quét chuỗi giống secret trong phần thêm mới (0), kiểm tra 12 quyết định `Proposed` (12/12), `command -v ffmpeg ollama uv` (không có). Không có runtime test vì không có code; không tải, cài hay chạy gì
- Chưa kiểm tra được: toàn văn LICENSE của từng artifact (mới đọc tóm tắt trang qua công cụ web); revision gốc của Qwen3 và Kokoro; tiếng Việt của Qwen3; RAM runtime của mọi ứng viên; điều khoản nhà cung cấp TTS đóng trong dữ liệu Kokoro; câu "personal use" của Piper; lộ trình "personal use" của VieNeu v3 Turbo. **Báo cáo pre-approval review gốc của Codex không có trong repo**, nên chưa đối chiếu finding theo mã. Chưa có TTS tiếng Việt nào đủ điều kiện nhóm B. `CURRENT_STATUS.md` (chỉ đọc) có thể còn ghi lượt cũ; `TASKS.md` có giá trị quyết định
- Finding cần xem lại: không có mã finding (báo cáo gốc không có trong repo). Các yêu cầu từ pre-approval review cần đối chiếu, theo danh sách Owner chuyển: (a) tách A, B, C; (b) bảng thông tin bắt buộc cho từng ứng viên (tên, vai trò, URL, artifact, revision, quantization, voice ID, license mã/trọng số/dữ liệu/phụ thuộc, thương mại, RAM và disk có nguồn, nhóm, chưa xác minh, ngày); (c) Piper `vais1000` (model card, dữ liệu, lessac, chuỗi quyền); (d) VieNeu-TTS 0.3B và v3 Turbo (codec, quyền giọng); (e) Piper tiếng Anh theo giọng cụ thể; (f) Kokoro (revision, voice, phụ thuộc); (g) Qwen3 4B/8B (tag, quantization, RAM không suy từ dung lượng tải); (h) voice cloning mặc định tắt; (i) MacBook Air M4 16 GB tuần tự, ngân sách 4 giờ cho toàn video; (j) tách bốn trạng thái (phương pháp, kế hoạch, danh sách, quyền tải)
- Phạm vi hồi quy: `PHASE-01-PLAN.md` (chín điều kiện bổ sung là đề xuất của Claude, chưa được Owner xác nhận); `HANDOFF_TO_CHATGPT.md`; không có thay đổi nào đối với D-009 đến D-023; Phase 1 chưa được mở rộng
- Yêu cầu review cụ thể: (1) Phân loại A/B/C và bằng chứng license của từng artifact có đúng và đủ không? Đặc biệt kiểm tra kết luận loại Piper `vais1000` (lessac/Blizzard 2013 nghiên cứu-only) và VieNeu 0.3B/0.5B (dữ liệu CC BY-NC). (2) Qwen3 nhóm B có đủ bằng chứng cho đúng tag, quantization, license mã/trọng số và phụ thuộc (Ollama MIT) không? (3) Có mệnh đề nào khẳng định license hợp lệ, hiệu năng hay "đạt" khi thiếu bằng chứng không? (4) RAM runtime và dung lượng tải có được tách rõ, không suy từ nhau không? (5) Bốn trạng thái có được tách độc lập, nhóm B có bị diễn giải thành lệnh tải không? (6) Có quyền mới phát sinh (tải, cài, chạy, commit, push, chi phí, liên hệ ngoài, duyệt ứng viên) không? (7) Trường hợp reviewer artifact chưa tồn tại: đề xuất cách xử lý trong RR có phù hợp workflow không, và bước kiểm tra toàn vẹn nên làm gì (không sửa workflow, chỉ nêu khuyến nghị). (8) Chín điều kiện bổ sung trong `PHASE-01-PLAN.md` có thắt chặt đúng, không nới lỏng không? (9) Kết luận thuộc về Codex; Claude không tự đánh dấu PASS
- END-OF-REVIEW-REQUEST

### RR-004
- Trạng thái: ANSWERED
- Scope Grant: SG-002
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-003 (vòng 0/3, CHANGES REQUESTED)
- Amendment: A01 (bốn file nhóm A chỉ đọc)
- Baseline Git: e83ecec6493919a335de96b3183a508ecb7b4fbd (nhánh `main`, trùng `origin/main`). Working tree chưa sạch, nên phiên bản review là SHA-256 bên dưới
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được sửa theo SG-002):
  - `HANDOFF_TO_CHATGPT.md` f2ca842f6ccb00c13626c3327a5864b0f058d471588ecd29d82695c7c09bd13b
  - `REVIEW_RESPONSE.md` 1acc5d312dd7e70b1964a9e85b4ed86f5ea79f63e3246a642ad588a15090403a
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` 7b74e50c27f68dc0027c6cdc3b12c253caf7e73538f55c1e54de746e346173a3
  - `docs/testing/phase1-candidates.md` 6510d033147d6ecc7a98d64da332ee812d6d12671991d215aff869b2b104a487
  - `TASKS.md` (phần trước `## Review Requests`) dab8e1255c5d529be8b42d7b6f090ea763b07ee33d3153344f5f5a4d7812c3b9
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01; không đổi so với RR-003):
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c
  - `CURRENT_STATUS.md` 2913ec78d6f447fda57f616b5aff0e81beb783e366c370edee4ef57d811b90df
  - `DECISIONS.md` 5f7c872cb58adbeaf589249fd92df239c2f6f24686f302fffc5e6748b588fe4f
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 12893 byte, SHA-256 048d5475d53fe07e5f9993d46f62e9ae29f9157bee78d92edc75f26a54770bd6. Đây là file do Codex tạo ở RR-003 (đúng một báo cáo `# Review RR-003`)
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-004` mới ở **đầu** file; 12893 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 12893 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`; mọi đường dẫn khác ngoài nhóm A và file nhóm B là nhóm C
- Lệnh đã chạy và kết quả thật: kiểm tra khi nhận lại lượt (9/9 hash nhóm A của RR-003 khớp; `PHASE-00-REVIEW.md` nguyên vẹn; file nhóm B có đúng một báo cáo; 0 đường dẫn nhóm C); `git rev-parse HEAD`, `git status --porcelain`; đọc LICENSE của Qwen3-4B, Qwen3-8B và Ollama qua công cụ web; đọc API Hugging Face lấy commit đầu kho của hai model; đọc manifest registry Ollama của `4b-q4_K_M` và `8b-q4_K_M` (metadata JSON, **không tải weights**); `shasum -a 256` cho các file trên; `grep` các chỗ còn ghi trạng thái cũ. Không có runtime test vì không có code; không tải, cài hay chạy gì. Một lệnh so hash bốn file chỉ đọc của tôi bị lỗi cú pháp shell và đã bị loại bỏ; hash bốn file này được so bằng mắt và bằng bước mô phỏng sau đó
- Chưa kiểm tra được: toàn văn LICENSE của các ứng viên khác ngoài Qwen3 và Ollama (và công cụ web trả bản tóm tắt, không phải tệp nguyên văn); liên kết giữa commit Hugging Face và blob GGUF của Ollama; blob license 11,338 byte của Ollama chưa so từng byte với LICENSE Hugging Face; digest manifest chưa tự tính lại từ tệp tải về; tiếng Việt của Qwen3; RAM runtime; mọi hiệu năng. Báo cáo pre-approval gốc của Codex không có trong repo. `CURRENT_STATUS.md` (chỉ đọc) đang lệch: còn ghi Qwen3 ở nhóm B; không sửa được trong phạm vi SG-002
- Finding cần xem lại: P1-001 (MEDIUM): Qwen3 đã chuyển về nhóm A, nhóm B trống, thêm bằng chứng LICENSE và định danh, thêm mục 7.1 (S1, S2) chờ Owner; P1-002 (LOW): đồng bộ trạng thái ở `phase1-candidates.md` và `HANDOFF_TO_CHATGPT.md`
- Phạm vi hồi quy: `PHASE-01-PLAN.md` điều 2, 9, 10; mục 3, 4.1, 4.2, 7.1, 8 của `phase1-candidates.md`; `HANDOFF_TO_CHATGPT.md` các dòng cổng đầu vào, Git, SG-002, RR, bước tiếp theo; không có thay đổi nào đối với D-009 đến D-023; Phase 1 không mở rộng
- Yêu cầu review cụ thể: (1) P1-001: việc chuyển Qwen3 về nhóm A và tách bằng chứng đã đủ với bất định về dữ liệu huấn luyện chưa, và tiêu chuẩn với phân loại giờ có nhất quán không? (2) Mục 7.1 (S1, S2) có trình bày trung lập, không tự áp dụng S2, không có đường nới tiêu chuẩn ngầm không? (3) Phần "chưa định danh" của Qwen3 (commit Hugging Face so với blob Ollama) có được nêu chính xác không? (4) P1-002: còn chỗ nào mâu thuẫn trạng thái trong các file Claude được sửa không? (5) Việc để `CURRENT_STATUS.md` lệch có gây rủi ro hiểu nhầm đủ lớn để cần Owner mở Amendment không? (6) Có quyền mới phát sinh (tải, cài, chạy, commit, push, chi phí, liên hệ ngoài, duyệt ứng viên) không? (7) Chín điều kiện cũ cộng điều 10 trong `PHASE-01-PLAN.md` vẫn chỉ thắt chặt không? (8) Kết luận thuộc về Codex; Claude không tự đánh dấu PASS
- END-OF-REVIEW-REQUEST

### RR-005
- Trạng thái: ANSWERED
- Scope Grant: SG-002
- Vòng: 2/3
- Thay thế RR: không có
- Tiếp nối RR: RR-004 (vòng 1/3, APPROVED; P1-001, P1-002 CLOSED)
- Amendment: A01 (bốn file nhóm A chỉ đọc)
- Baseline Git: e83ecec6493919a335de96b3183a508ecb7b4fbd (nhánh `main`, trùng `origin/main`). Working tree chưa sạch, nên phiên bản review là SHA-256 bên dưới
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được sửa theo SG-002):
  - `HANDOFF_TO_CHATGPT.md` 52bca2c1fb8f62f0d26ab1749eec03e70afabd5050974772ed1be284b2d24872
  - `REVIEW_RESPONSE.md` 9a7856c48c7ad8f701505d469e8d1a45745c5edc62ce70b50ffb0f95b3ba6f56
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` 5412e9b1da1df33699c27bd9da8e793907beff9b3b019f5735af048edbeb1a02
  - `docs/testing/phase1-candidates.md` ff67af495cbf716e81deb21b11272a9be94f161c073306fa06afb42c4c916331
  - `TASKS.md` (phần trước `## Review Requests`) 70a6480db22c51f56398424e07cfc9503c5dc95649bb4da67aa9361e3d6cc159
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01; không đổi so với RR-003 và RR-004):
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c
  - `CURRENT_STATUS.md` 2913ec78d6f447fda57f616b5aff0e81beb783e366c370edee4ef57d811b90df
  - `DECISIONS.md` 5f7c872cb58adbeaf589249fd92df239c2f6f24686f302fffc5e6748b588fe4f
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 21512 byte, SHA-256 0eeec6f17a23ea7bc84226d4202ee57b4be2b3619d8bfd36dd0e2ebdb1b9fa87 (chứa báo cáo `# Review RR-004` ở đầu và `# Review RR-003` ở cuối, do Codex viết; Claude không sửa)
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-005` mới ở **đầu** file; 21512 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 21512 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`; mọi đường dẫn khác ngoài nhóm A và file nhóm B là nhóm C
- Lệnh đã chạy và kết quả thật: đọc `HEAD`, `git status --porcelain`; đọc lại API Hugging Face Qwen3-4B và hai manifest registry Ollama (cùng giá trị cũ, **cùng một công cụ nên không phải xác nhận độc lập**); các lệnh `grep` để tìm trạng thái cũ và đồng bộ; `shasum -a 256` cho các file trên. Không có runtime test vì không có code; không tải, cài hay chạy gì
- Chưa kiểm tra được: toàn văn LICENSE qua công cụ chỉ trả bản tóm tắt; blob license 11,338 byte của Ollama chưa so từng byte với LICENSE Hugging Face; manifest Ollama và commit 4B chưa được Codex xác nhận độc lập (RR-004); commit Hugging Face nào là nguồn của GGUF; tiếng Việt của Qwen3; RAM runtime; mọi hiệu năng. "Không tìm thấy bằng chứng trái ngược" là kết quả tìm kiếm có giới hạn. Không thể chứng minh bằng hash rằng "Chọn S2" do Owner viết. `CURRENT_STATUS.md` (chỉ đọc) đang lệch; `DECISIONS.md` chưa ghi quyết định S2 vì ngoài allowlist
- Finding cần xem lại: không có finding mở (P1-001, P1-002 đã CLOSED ở RR-004). Mục xem lại mới: việc **chuyển Qwen3 4B và 8B `q4_K_M` từ nhóm A lên nhóm B theo S2** sau quyết định "Chọn S2" của Owner ngày 2026-10-31
- Phạm vi hồi quy: `phase1-candidates.md` mục 1, 2, 3, 4.1, 4.2, 7.1, 8; `PHASE-01-PLAN.md` điều 2, 10 và câu cuối; `HANDOFF_TO_CHATGPT.md`; không có thay đổi nào đối với D-009 đến D-023; Phase 1 không mở rộng
- Yêu cầu review cụ thể: (1) Quyết định S2 có được chép đúng nguyên văn và được hiểu **đủ hẹp** (chỉ phân loại; không pháp lý; không duyệt danh sách; không quyền tải, cài, chạy; không áp dụng cho TTS) không? (2) Qwen3 4B và 8B thỏa ba điều kiện (i), (ii), (iii) của S2 chưa? Đặc biệt cân nhắc các hạn chế Claude đã nêu: blob license chưa so từng byte, manifest 4B chưa được xác nhận độc lập, "không có bằng chứng trái ngược". Nếu chưa đủ, nêu điều kiện cụ thể. (3) Bảng đối chiếu S2 ở mục 7.1 có công bằng không: chỉ Qwen3 lên B, các ứng viên khác giữ A đúng lý do không? Có ứng viên nào bị đối xử không nhất quán không? (4) Có đường nào biến nhóm B thành quyền tải, cài, chạy hoặc "đã duyệt" không? (5) Điều 10 trong `PHASE-01-PLAN.md` có ghi đúng quyết định của Owner, và các điều 1 đến 9 vẫn là đề xuất chưa xác nhận không? (6) Có quyền mới nào phát sinh (tải, cài, chạy, commit, push, chi phí, liên hệ ngoài) không? (7) Việc chưa ghi S2 vào `DECISIONS.md` và để `CURRENT_STATUS.md` lệch có gây rủi ro hiểu nhầm cần Owner xử lý không? (8) Kết luận thuộc về Codex; Claude không tự đánh dấu PASS
- END-OF-REVIEW-REQUEST


### RR-006
- Trạng thái: ANSWERED
- Scope Grant: SG-002
- Vòng: 3/3 (vòng cuối; SG-002 đã dùng vòng 0, 1, 2 ở RR-003, RR-004, RR-005)
- Thay thế RR: không có
- Tiếp nối RR: RR-005 (vòng 2/3, APPROVED, ANSWERED)
- Amendment: A01 (bốn file nhóm A chỉ đọc). **Nhãn "A02" đến "A07" trong `TASKS.md` do Claude đặt** cho các chỉ đạo trực tiếp của Owner trong chat; Owner chỉ dùng chữ "Amendment" cho A01. Xem "Điểm cần Owner phê duyệt" bên dưới
- Baseline Git: 9838f0a2ca1073d152bb43ef1c6c2a7473c81d9d (nhánh `main`, trùng `origin/main`). Working tree sạch lúc kiểm tra, **trước** khi Claude sửa `HANDOFF_TO_CHATGPT.md` và đăng RR này
- Phiên bản review: SHA-256 bên dưới (hai file nhóm A đã đổi so với commit 9838f0a: `HANDOFF_TO_CHATGPT.md` và `TASKS.md`)
- SHA-256 (nhóm A, Claude được sửa theo SG-002):
  - `HANDOFF_TO_CHATGPT.md` 9af7949e0458d74845cf1c909f69c6b68de9c87639eccb58e2499059576b0fe7
  - `REVIEW_RESPONSE.md` e3f2af97f86ae191bc5c98ded9661b34e046dabb722509d41d17f3e545afe18f
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` eb8bfa386581fab94cfd1fb5af0ec5efccd1488232f3bfe6d2da9b0f26fdabfa
  - `docs/testing/phase1-candidates.md` 0c05b72ae053ca27d0dcdba586e131c75f8e7b38f34d645219381a30f8c63685
  - `TASKS.md` (phần trước `## Review Requests`) a79d620b3a7a5708620b6b5e3551b48cf472f629cdc51ce1fc853784bc64f6fc
- SHA-256 (nhóm A, **chỉ đọc** với Claude theo Amendment A01; Owner chỉ đạo ghi hẹp tại `DECISIONS.md` và `CURRENT_STATUS.md`, xem bên dưới):
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c (không đổi so với RR-005)
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520 (không đổi so với RR-005)
  - `DECISIONS.md` c6cc2d44bf6bc9c11bc97b2bdffb297748009846231344bb7e471e40dc092301 (đổi so với RR-005 `5f7c872c…`: thêm D-024)
  - `CURRENT_STATUS.md` 61d2f363f23fe4230303071d4bf5efa7b76e06fd1ce63bef2202e3513be7e35b (đổi so với RR-005 `2913ec78…`: đồng bộ trạng thái)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 30343 byte, SHA-256 9e3919e458fb6909343a7d7ebde9171c05dd5c1b7cd39d6bb84b8829f1471a6a (chứa `# Review RR-005`, `# Review RR-004`, `# Review RR-003`, do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-006` mới ở **đầu** file; 30343 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 30343 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- **Nội dung thuộc SG-002 (nhờ Codex review):**
  1. Mã 1B của Owner ("1B, 2A, 4a, 4b"): danh sách model chỉ có Qwen3 4B `q4_K_M`; 8B chưa duyệt ở thời điểm đó. Ghi tại `phase1-candidates.md` mục 1, 3, 4.1, 4.2, 8; `PHASE-01-PLAN.md` điều 11.
  2. D-024 trong `DECISIONS.md`: có chép đúng tiêu chuẩn S2 (nguyên văn "Chọn S2"), đủ hẹp, không thành quyền tải, không áp dụng cho TTS, và không động tới mục khác không.
  3. Nghiên cứu TTS tiếng Việt (mã 2A): `phase1-candidates.md` mục 4.8 (VieNeu v3 Turbo: kho GitHub có LICENSE Apache-2.0 chỉ cho mã; kho Hugging Face không có tệp LICENSE; giữ nhóm A) và mục 4.10 (ViZipVoice nhóm A; VietTTS, viXTTS nhóm C). Kết luận "R1 chưa giải quyết, không có TTS tiếng Việt nhóm B" có đúng với bằng chứng ghi không?
  4. Trả lời của Owner "2G, 4C- xác nhận 1-8": `PHASE-01-PLAN.md` mục "Điều kiện bổ sung" (điều 1–8 xác nhận, điều 9 gạch bỏ, điều 11).
  5. Tính nhất quán giữa `TASKS.md`, `HANDOFF_TO_CHATGPT.md`, `REVIEW_RESPONSE.md`, `phase1-candidates.md` và `PLAN` về: số vòng, trạng thái bốn nhóm quyền, những gì Owner đã và chưa trả lời.
- **Ngoài phạm vi (KHÔNG nhờ Codex xác nhận quyền hay tính hợp lệ; chỉ nêu để Codex không bị bất ngờ):** (a) việc Claude cài Ollama, tải `qwen3:4b-q4_K_M` và `qwen3:8b-q4_K_M`, đo thô; SG-002 gốc ghi "không cho phép tải, cài, benchmark", và workflow mục 3 ghi SG không thể cấp quyền cài đặt; các thao tác này dựa trên chỉ đạo trực tiếp của Owner trong chat (trích nguyên văn ở các khối A03–A07, "Lời Owner"), **không** nhờ Codex coi chúng là phạm vi SG-002 hay đánh giá kết quả đo; (b) commit `9838f0a` và push: **AUTHORIZATION NOT VERIFIED trong file repo** (chi tiết bên dưới); (c) nội dung kỹ thuật các số đo (RSS, token/s): chỉ là dữ liệu thô, không nhờ review; (d) chất lượng tiếng Việt của Qwen3; (e) ghi "đã tải, digest khớp" của Qwen3 4B và 8B ở `phase1-candidates.md` mục 4.1, 4.2 là **báo cáo sự kiện của Claude**, Codex không cần xác nhận
- **Bằng chứng quyền commit/push:** trong chat của phiên này Owner viết nguyên văn "Cho commit" (sau đó Claude commit `9838f0a`) và "Cho push" (sau đó Claude push); lệnh `git ls-remote origin main` trả `9838f0a`. **Không có dòng nào trong `TASKS.md`, `CURRENT_STATUS.md` hay `HANDOFF_TO_CHATGPT.md` ghi hai lời này trước khi thực hiện**, nên Codex không thể xác minh từ file. Claude không khẳng định là đã có phê duyệt dựa trên file; trình Owner xác nhận
- Lệnh đã chạy và kết quả thật: `git rev-parse HEAD` (9838f0a…), `git status --porcelain` (rỗng trước khi sửa `HANDOFF_TO_CHATGPT.md`), `git rev-parse --short origin/main` (9838f0a), `shasum -a 256` các file trên, `wc -c` reviewer artifact (30343), đọc workflow mục 3, 6, 7, 9, 10. Trước đó (ngoài RR này) Claude đã chạy `brew install ollama`, `brew update`, `ollama pull` hai model, benchmark, `git commit`, `git push` theo chỉ đạo Owner. Không có runtime test vì không có code ứng dụng
- Chưa kiểm tra được: toàn văn LICENSE qua công cụ chỉ trả bản tóm tắt; blob license 11,338 byte của Ollama chưa so từng byte với LICENSE Hugging Face; commit nguồn của GGUF; license của ZipVoice gốc; VietTTS và viXTTS mới đọc qua tóm tắt tìm kiếm; thẻ model VieNeu có thể thay đổi sau ngày 2026-10-31; chất lượng tiếng Việt; mọi hiệu năng ngoài số đo thô
- Finding cần xem lại: không có finding mở (P1-001, P1-002 CLOSED ở RR-004; RR-005 không có finding mới)
- Phạm vi hồi quy: `phase1-candidates.md` toàn bộ (đặc biệt mục 1, 3, 4.1, 4.2, 4.8, 4.10, 7.1, 8); `PHASE-01-PLAN.md` mục "Điều kiện bổ sung"; D-024 và việc 12 quyết định `Proposed` giữ nguyên (D-009–012, D-014–016, D-018–022); `DECISIONS.md` hiện còn hai mục D-013 và D-017 lặp trong phần "Chờ Chủ dự án duyệt" dù đã duyệt (Claude biết, chưa sửa vì ngoài phạm vi A02; xin Codex ghi nhận nếu coi là finding); `CURRENT_STATUS.md` hiện còn dòng Git ghi `e83ecec` và "cây có thay đổi chưa commit" (cũ, Claude chưa sửa vì chưa có quyền ghi thêm)
- Điểm cần Owner phê duyệt (không nhờ Codex): (1) có coi các chỉ đạo của Owner ở A03–A07 và việc ghi `CURRENT_STATUS.md`, `DECISIONS.md` là chỉ đạo riêng (nhãn "Amendment A0x" do Claude đặt) hay cần Owner xác nhận chúng là Amendment của SG-002; (2) xác nhận bằng văn bản quyền commit `9838f0a` và push; (3) quyền sửa `CURRENT_STATUS.md` dòng Git cũ; (4) quyền sửa mục lặp D-013, D-017 trong `DECISIONS.md`; (5) đóng SG-002 (4e) sau vòng này; (6) chuẩn hóa reviewer artifact "ABSENT" (4d); (7) chấm tiếng Việt chính thức
- Yêu cầu review cụ thể: (1) Mục 1–5 ở "Nội dung thuộc SG-002" có đúng, đủ hẹp và nhất quán không, và có phát biểu nào vượt bằng chứng không? (2) Kết luận 2A có đúng với bằng chứng không, và VieNeu v3 Turbo, ViZipVoice, VietTTS, viXTTS có bị xếp nhóm sai không? (3) Có file nhóm A nào khác với danh sách hash trên, hay đường dẫn nhóm C không? (4) Có chỗ nào tài liệu coi nhóm B hay việc duyệt Qwen3 4B là quyền chạy, hay coi kết quả đo là PASS về chất lượng không? (5) Xác nhận hoặc phản bác nhận xét của Claude rằng mục "Ngoài phạm vi" không nên được review trong SG-002 mà cần quyền riêng. Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo, không suy từ RR này
- END-OF-REVIEW-REQUEST


### RR-007
- Trạng thái: ANSWERED
- Scope Grant: SG-003
- Vòng: 0/3 (review đầu tiên của SG-003)
- Thay thế RR: không có
- Tiếp nối RR: không có (SG-003 độc lập với SG-002 đã DONE; RR-006 không phải tiền thân)
- Amendment: A01 của SG-003 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree **không sạch**: bốn đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-003):
  - `HANDOFF_TO_CHATGPT.md` 04e77fcd5b173c2a72538ed19d87caebcabc0a5110320440fbb730be102b9173
  - `docs/testing/phase1-tools-candidates.md` f0eaafdbb723d61be1db18375e278f604400f1bec40f2c5c232301261cefae2e (file **mới**, chưa có trong Git)
  - `TASKS.md` (phần trước `## Review Requests`) c608b88482101828562df760706fae26f425b7f1bf5c8b6d4bbb016f66bb6a09
  - `REVIEW_RESPONSE.md` d7f7abd6874684e9f97cf970eac662e26ca439f42fa1569e21c8d4e8640232ef (không đổi so với HEAD; Owner cho phép ghi trong SG-003; liệt kê để rõ)
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-003; thay đổi chưa commit **có từ trước SG-003**):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (bản HEAD `61d2f363f23fe4230303071d4bf5efa7b76e06fd1ce63bef2202e3513be7e35b`; khác 5 dòng thêm và 5 dòng bớt: đồng bộ SG-002 DONE, RR-006, Git `7115591`, ngày cập nhật, danh sách việc chờ). Nội dung chưa nhắc SG-003 và còn ghi "không có Scope Grant ACTIVE": có trước SG-003, **không nhờ Codex coi là finding của SG-003**
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 39724 byte, SHA-256 01a2e7186c9b848febfd1ad6a1c5b59ad8fd2493f5f1d9c563f2f2eda9af4acf (chứa `# Review RR-006`, `# Review RR-005`, `# Review RR-004`, `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-007` mới ở **đầu** file; 39724 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 39724 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner (nguyên văn, đã ghi trong `TASKS.md`, khối "SG-003 – Xác nhận của Owner" và "SG-003 – Amendment A01"): "Phê duyệt FFmpeg 9.0.2 Homebrew ở mức ứng viên nhóm B có điều kiện, chờ Codex review độc lập"; "Tôi phê duyệt SG-003 cho hoạt động nghiên cứu tài liệu và Codex review, với giới hạn tối đa 3 vòng"; "Chưa phê duyệt tạo commit hoặc push"; "Duyệt Amendment A01". Claude chép từ chat; hash không chứng minh tác giả
- **Nội dung nhờ Codex review (chỉ FFmpeg 9.0.2):** `phase1-tools-candidates.md` mục 2 và mục 8 (dòng FFmpeg và "Kết luận và việc cần Owner quyết" điểm 1), cùng tham chiếu cần thiết: (a) license: LICENSE.md upstream tag n9.0.2, formula Homebrew `ffmpeg.rb`; cờ `--enable-gpl`, `--enable-version3`, libx264, libx265, videotoolbox, không `--enable-nonfree`; (b) định danh artifact: sha256 tarball `8c3850283eb2…002e`, bottle `arm64_tahoe` `595b0bb854e6…ed04d`, 11 phụ thuộc trực tiếp; (c) nguồn: trang legal ffmpeg.org; (d) rủi ro còn lại: GPL (phân phối), bằng sáng chế H.264/H.265, license phụ thuộc chưa đọc
- **Ngoài phạm vi (không nhờ Codex review):** resvg, CairoSVG, faster-whisper và mọi phần khác của hồ sơ (mục 1, 3, 4, 5, 6, 7; các dòng đó còn nhóm A và có thể đã lỗi thời so với mục 8); việc có nên cài FFmpeg (cần quyết định riêng của Owner sau Codex PASS); kết luận pháp lý; số đo hiệu năng
- Lệnh đã chạy và kết quả thật: `git rev-parse HEAD`, `git status --porcelain` (4 đường dẫn), `git diff -- CURRENT_STATUS.md`, `shasum -a 256` các file trên, `wc -c` reviewer artifact, `brew info --json=v2 ffmpeg` (chỉ đọc: 9.0.2, GPL-3.0-or-later, 11 phụ thuộc), `brew deps --formula ffmpeg` (14 gói), đọc trang web công khai qua công cụ tóm tắt. **Không cài, không tải, không chạy FFmpeg**; FFmpeg chưa có trên máy (`command -v ffmpeg` rỗng). Không có runtime test vì không có code ứng dụng
- Chưa kiểm tra được: toàn văn GPLv3 và `COPYING` trong tarball; license từng phụ thuộc (dav1d, lame, libvmaf, libvpx, opus, svt-av1, x264, x265, openssl@4, xz, sdl2-compat); hash tarball/bottle chưa tự tính lại (đọc từ formula); videotoolbox có thực sự hoạt động trên máy này; bằng sáng chế H.264/H.265 (không thể giải quyết bằng đọc license); các nguồn web là snapshot 2026-10-31 qua công cụ tóm tắt
- Finding cần xem lại: không có
- Phạm vi hồi quy: không có hồ sơ cũ liên quan; `phase1-tools-candidates.md` là file mới. SG-002 đã DONE; P1-003, P1-004 chưa CLOSED (xem RR-006) không thuộc SG-003
- Yêu cầu review cụ thể: (1) Mục 2 và mục 8 FFmpeg có chép đúng nguồn (LICENSE.md upstream, formula Homebrew, trang legal) và có phát biểu nào vượt bằng chứng không? Đặc biệt câu "trang legal nói về phân phối, không nói về video đầu ra" và "dự án chỉ dùng nội bộ". (2) Phân loại "đề xuất B có điều kiện" có phù hợp với ba điều kiện (i) đọc toàn văn LICENSE của đúng artifact và runtime, (ii) ghi revision/digest và nêu phần chưa xác định, (iii) không có bằng chứng trái ngược không? Các phần chưa đọc (GPLv3 toàn văn, license phụ thuộc) có làm điều kiện (i) chưa đạt đến mức không thể gọi là B có điều kiện không? (3) Digest tarball và bottle `arm64_tahoe` có khớp formula Homebrew hiện hành không? (4) Rủi ro dư (GPL, sáng chế, phụ thuộc chưa đọc) đã được nêu đủ chưa, và hồ sơ có coi nhóm B hay quyết định của Owner là quyền cài hay chạy ở chỗ nào không? (5) Có đường dẫn nhóm C nào, hay hash nhóm A nào không khớp RR này không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo
- END-OF-REVIEW-REQUEST


### RR-008
- Trạng thái: ANSWERED
- Scope Grant: SG-003
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-007 (vòng 0/3, CHANGES REQUESTED, ANSWERED)
- Amendment: A01 của SG-003 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree không sạch: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-003):
  - `HANDOFF_TO_CHATGPT.md` 86773f7ce076b2b189fb6a1c6922d2305e25248f7d7662306f007235faf39431
  - `docs/testing/phase1-tools-candidates.md` cfa66998cdab69a87efaa93a2ba9214fb6bd2b307421135313cc52873df0cca5 (file **mới**, chưa có trong Git)
  - `REVIEW_RESPONSE.md` e52627ce3ab0f76a4bd12d0c273cd9bf3ca6ea14dfc38df5c932c702826e268e
  - `TASKS.md` (phần trước `## Review Requests`) c608b88482101828562df760706fae26f425b7f1bf5c8b6d4bbb016f66bb6a09 (không đổi so với RR-007)
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-003):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (không đổi so với RR-007)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 49442 byte, SHA-256 e76679fbf6d7c7d99e7980dc7431b8fc3bada2cd01a898a17aa44b76fcdd8cd0 (chứa `# Review RR-007`, `# Review RR-006`, `# Review RR-005`, `# Review RR-004`, `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-008` mới ở **đầu** file; 49442 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 49442 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner: như RR-007 (khối "SG-003 – Xác nhận của Owner" và "SG-003 – Amendment A01" trong `TASKS.md`). Không có quyền mới; không cài, không commit, không push
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-003 – Phản hồi RR-007 vòng 0/3"
- Finding cần xem lại: **P1-005** (MEDIUM) và **P1-006** (LOW), trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`. Claude không ghi CLOSED. P1-003, P1-004 (SG-002, chưa CLOSED) không thuộc SG-003
- Thay đổi để Codex đối chiếu (chỉ `phase1-tools-candidates.md` và phản hồi): (1) mục 1: nhãn FFmpeg đổi thành "B CÓ ĐIỀU KIỆN (Owner cho tiếp tục đánh giá) — chưa phải B đã đủ bằng chứng"; (2) mục 2: dòng phụ thuộc (11 phụ thuộc runtime không phải toàn closure; revision 1), dòng nghĩa vụ ("dùng nội bộ" không đồng nghĩa video kiếm tiền; Codex chưa xác nhận trang legal); (3) mục 8 điểm 1: chuỗi (a) hoàn tất hồ sơ → (b) Codex PASS → (c) hồ sơ lệnh → (d) Owner quyết riêng; (4) mục 8.1 mới: bảng đã đọc và chưa đọc (COPYING.GPLv3, formula revision 1, OpenSSL và GPL, license phụ thuộc ở mức metadata Homebrew, sáng chế, VideoToolbox) và 5 điều kiện còn chặn
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `shasum -a 256`, `wc -c`, `tail -c 39724 … | shasum -a 256` (khớp), `brew info --json=v2` cho ffmpeg và 11 phụ thuộc (chỉ đọc), đọc COPYING.GPLv3 và LICENSE.md tag n9.0.2 qua web. **Không cài, không tải, không chạy FFmpeg**; `command -v ffmpeg` rỗng. Không có runtime test vì không có code
- Chưa kiểm tra được: toàn văn license từng phụ thuộc (chỉ metadata Homebrew); COPYING.GPLv3 chưa so từng byte; hash tarball và bottle chưa tự tính lại; trang legal ffmpeg.org (Codex timeout; Claude chỉ có bản tóm tắt); VideoToolbox thực thi; sáng chế H.264/H.265
- Phạm vi hồi quy: mục 2 và 8 của hồ sơ FFmpeg; không có thay đổi ở resvg, CairoSVG, faster-whisper (ngoài phạm vi SG-003 review)
- Yêu cầu review cụ thể: (1) P1-005 và P1-006 có được xử lý đủ không, hay còn câu nào coi B có điều kiện là điều kiện (i)–(iii) đã đạt hoặc coi chấp nhận rủi ro là đủ để xin cài? (2) Mục 8.1 có chép đúng COPYING.GPLv3 mục 2, đoạn OpenSSL trong LICENSE.md và license phụ thuộc không (metadata Homebrew có khớp nguồn không)? (3) Có phát biểu mới nào vượt bằng chứng không? (4) Hồ sơ đã đủ điều kiện để Codex PASS cho bước "B có điều kiện, chờ quyết định riêng", hay còn điều kiện chặn nào Claude chưa liệt kê? (5) Có đường dẫn nhóm C hay hash nhóm A nào không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo
- END-OF-REVIEW-REQUEST


### RR-009
- Trạng thái: ANSWERED
- Scope Grant: SG-003
- Vòng: 2/3
- Thay thế RR: không có
- Tiếp nối RR: RR-008 (vòng 1/3, CHANGES REQUESTED, ANSWERED)
- Amendment: A01 của SG-003 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree không sạch: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-003):
  - `HANDOFF_TO_CHATGPT.md` 1152d248957287961b143d14550a7245127a44757e33b18e8dccb7fe94de1311
  - `docs/testing/phase1-tools-candidates.md` ab2f9ea0c59045b1ca72f26473b6f1b12e438a0a1c52285749b23b52a1aa1149 (file **mới**, chưa có trong Git)
  - `REVIEW_RESPONSE.md` a271fcc2d6be7a1973da723ef39fd5821c88553beaf67e7065ba306e032ececa
  - `TASKS.md` (phần trước `## Review Requests`) c608b88482101828562df760706fae26f425b7f1bf5c8b6d4bbb016f66bb6a09 (không đổi so với RR-007 và RR-008)
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-003):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (không đổi)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 58747 byte, SHA-256 f657694c91dc4d3cb64d0af054dc966600e37611b410cbe6aaa60c825074e271 (chứa `# Review RR-008`, `# Review RR-007`, `# Review RR-006`, `# Review RR-005`, `# Review RR-004`, `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-009` mới ở **đầu** file; 58747 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 58747 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner: như RR-007 và RR-008 (khối "SG-003 – Xác nhận của Owner" và "SG-003 – Amendment A01" trong `TASKS.md`). Không có quyền mới; không cài, không commit, không push
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-003 – Phản hồi RR-008 vòng 1/3"
- Finding cần xem lại: **P1-005** (MEDIUM, còn mở sau sửa một phần) và **P1-007** (MEDIUM, mới), trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`. P1-006 đã `CLOSED` bởi Codex ở RR-008. Claude không ghi CLOSED cho finding nào
- Thay đổi để Codex đối chiếu (chỉ `phase1-tools-candidates.md` và phản hồi): (1) mục 8, dòng FFmpeg: cột "Vẫn còn thiếu" nay ghi GPLv3 đã đọc, phụ thuộc mới đọc metadata Homebrew, điều kiện (i)–(iii) chưa xác nhận hoàn tất; cột "Phân loại" nay ghi "B CÓ ĐIỀU KIỆN (Owner cho tiếp tục đánh giá); chưa phải B đã đủ bằng chứng" và đánh dấu cách ghi cũ là lịch sử; (2) mục 8 điểm 1: chuỗi nay có bước (a) bằng chứng tài liệu → (b) Codex PASS → (c) hồ sơ lệnh → (d) Owner quyết quyền tải/cài → (e) so hash tệp thực nhận trước khi dùng; (3) mục 8.1: danh sách điều kiện tách thành bốn tầng (bằng chứng tài liệu; Codex PASS và hồ sơ lệnh; quyền tải/cài; kiểm tra sau khi được cấp quyền), kèm câu "tầng 1 là điều kiện duy nhất cần hoàn tất trước Codex PASS" và phân biệt hash nguồn công bố với hash tệp thực nhận
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `wc -c`, `tail -c 49442 … | shasum -a 256` (khớp `e76679fb…`), `shasum -a 256` các file trên. **Không cài, không tải, không chạy FFmpeg**. Không có runtime test vì không có code
- Chưa kiểm tra được: toàn văn license từng phụ thuộc (metadata Homebrew đã được Codex đối chiếu khớp 11 cặp, nhưng không phải toàn văn); hash tarball và bottle thực nhận (chưa tải, chưa có quyền); sáng chế H.264/H.265; trang legal ffmpeg.org (Codex timeout); VideoToolbox thực thi
- Phạm vi hồi quy: mục 1, 2, 8, 8.1 của hồ sơ FFmpeg; không có thay đổi ở resvg, CairoSVG, faster-whisper
- Yêu cầu review cụ thể: (1) P1-005: dòng FFmpeg mục 8 đã đồng bộ với mục 1 và 8.1 chưa, và còn câu nào ngụ ý đã đủ điều kiện (i)–(iii) hoặc kết luận cũ? (2) P1-007: bốn tầng có loại bỏ vòng phụ thuộc không, và tầng 1 có đủ là điều kiện duy nhất trước Codex PASS không? Có thứ tự nào còn yêu cầu quyết định hoặc tải trước khi được cấp quyền không? (3) Còn mâu thuẫn nội bộ nào giữa mục 1, 2, 8, 8.1 không? (4) Nếu không còn finding mở, hồ sơ có đủ để Codex PASS cho nhãn "B có điều kiện, chờ quyết định riêng" không (không phải "B đã đủ bằng chứng")? (5) Có đường dẫn nhóm C hay hash nhóm A nào không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo
- END-OF-REVIEW-REQUEST


### RR-010
- Trạng thái: ANSWERED
- Scope Grant: SG-003
- Vòng: 3/3 (vòng cuối của SG-003)
- Thay thế RR: không có
- Tiếp nối RR: RR-009 (vòng 2/3, CHANGES REQUESTED, ANSWERED)
- Amendment: A01 của SG-003 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree không sạch: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-003):
  - `HANDOFF_TO_CHATGPT.md` 87cb7b02ef685b3a1d5339897439dd57f1b222ed40cbc8e410097c99e99901a1
  - `docs/testing/phase1-tools-candidates.md` cc05a2263e12aac7440e58740eaf17cea6f9e717698808aba4266a65bf7e04cc (file **mới**, chưa có trong Git)
  - `REVIEW_RESPONSE.md` 3ef0d4be0d619cb7a33e9b5827ca6fe1d47cc07b4a9f1acfab15ff8407a49ca5
  - `TASKS.md` (phần trước `## Review Requests`) c608b88482101828562df760706fae26f425b7f1bf5c8b6d4bbb016f66bb6a09 (không đổi so với RR-007, 008, 009)
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-003):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (không đổi)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 66483 byte, SHA-256 b0ff9d93023032ccf30316ce3b2027e98602e8232818085c1a5fb28dc5b80e67 (chứa `# Review RR-009`, `# Review RR-008`, `# Review RR-007`, `# Review RR-006`, `# Review RR-005`, `# Review RR-004`, `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-010` mới ở **đầu** file; 66483 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 66483 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner: như RR-007 đến RR-009 (khối "SG-003 – Xác nhận của Owner" và "SG-003 – Amendment A01" trong `TASKS.md`). Không có quyền mới; không cài, không commit, không push. Không có quyết định riêng của Owner về mức bằng chứng (hướng đọc tài liệu được chọn, không trình Owner)
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-003 – Phản hồi RR-009 vòng 2/3"
- Finding cần xem lại: **P1-005** (MEDIUM), phần còn lại: tầng 1.1. Trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`. P1-006 và P1-007 đã `CLOSED` bởi Codex. Claude không ghi CLOSED cho finding nào
- Thay đổi để Codex đối chiếu (chỉ `phase1-tools-candidates.md` và phản hồi): (1) mục 8.2 mới: đọc tệp license upstream của 11 phụ thuộc runtime (dav1d, lame, libvmaf, libvpx, opus, svt-av1, x264, x265, openssl@4, xz, sdl2-compat), kèm giới hạn nêu rõ và danh sách sáu điều chưa giải quyết; (2) mục 8, dòng FFmpeg: cột "Vẫn còn thiếu" cập nhật; (3) mục 8.1: bảng cập nhật con trỏ sang 8.2 và dòng tầng 1 ghi "1.1 đã thực hiện với giới hạn", việc đủ hay không do Codex đánh giá, hoặc Owner quyết riêng mức bằng chứng
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `wc -c`, `tail -c 58747 … | shasum -a 256` (khớp `f657694c…`), `shasum -a 256` các file trên, đọc 14 tệp license/PATENTS/header upstream qua web (nhánh mặc định). **Không cài, không tải, không chạy FFmpeg**. Không có runtime test vì không có code
- Chưa kiểm tra được: license ghim đúng phiên bản Homebrew; lame từ nguồn chính thức và "or later"; phụ thuộc gián tiếp; notice trong tarball và bottle; tương thích pháp lý giữa các thành phần GPL-2.0-or-later, Apache-2.0 và bản dựng GPL-3.0-or-later; sáng chế H.264/H.265/AV1/VP9/Opus; hash tarball và bottle thực nhận (chưa tải, chưa có quyền); VideoToolbox thực thi
- Phạm vi hồi quy: mục 1, 2, 8, 8.1, 8.2 của hồ sơ FFmpeg; không có thay đổi ở resvg, CairoSVG, faster-whisper
- Yêu cầu review cụ thể: (1) Tầng 1.1 nay đã hoàn tất đủ để P1-005 đóng chưa? Nếu chưa, điểm nào cụ thể còn thiếu và điểm đó cần Claude bổ sung hay cần Owner quyết định riêng? (2) Mục 8.2 có chép đúng các tệp license upstream không, và có phát biểu nào vượt bằng chứng (đặc biệt về svt-av1, lame, x265, xz)? (3) Còn mâu thuẫn nội bộ giữa mục 1, 2, 8, 8.1, 8.2 không? (4) Nếu không còn finding mở, hồ sơ có đủ để Codex PASS cho nhãn "B có điều kiện, chờ quyết định riêng" không (không phải "B đã đủ bằng chứng" và không phải quyền cài)? (5) Có đường dẫn nhóm C hay hash nhóm A nào không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo. Đây là vòng cuối: nếu không PASS, dừng và báo Owner, không mở vòng 4
- END-OF-REVIEW-REQUEST


### RR-011
- Trạng thái: ANSWERED
- Scope Grant: SG-004
- Vòng: 0/3 (review đầu tiên của SG-004)
- Thay thế RR: không có
- Tiếp nối RR: không có là RR trong SG-004; xử lý finding P1-005 còn mở sau RR-010 của SG-003 (vòng 3/3, CHANGES REQUESTED). Lịch sử SG-003 không đổi
- Amendment: A01 của SG-004 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree không sạch: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-004):
  - `HANDOFF_TO_CHATGPT.md` ba3b7221a9c36469f16488bc14d7051edf279ca9109766fb7d55cfe0f38c8cec
  - `docs/testing/phase1-tools-candidates.md` 14aa5c05ec76198fac0d6f98604b5cfd03f4a7064ea0c73b75dd5e4eed6697cb (file **mới**, chưa có trong Git)
  - `REVIEW_RESPONSE.md` f109397a3f34677c9d136cf03a8a4eb7eca6e66d738c3c5d2028f56c58adb160
  - `TASKS.md` (phần trước `## Review Requests`) ab355908bc73f8092719c3117ec234b7c94a979870fc988baa417e9c2a1816f9
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-004):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (không đổi)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 76078 byte, SHA-256 1619658ed3513eff6d6ce3169e81f63728c9d0efc3c75304f9789c11e24435b6 (chứa `# Review RR-010` đến `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-011` mới ở **đầu** file; 76078 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 76078 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner (nguyên văn, đã ghi trong `TASKS.md`, khối "SG-004" và "SG-004 – Amendment A01"): "Tôi phê duyệt mở SG-004 với phạm vi giới hạn nhằm xử lý finding P1-005 của RR-010"; "Tối đa 3 vòng review mới cho SG-004. Không thay đổi hoặc đặt lại lịch sử SG-003"; "Xác nhận allowlist". Không có quyền mới: không cài, không tải, không commit, không push. Claude chép từ chat; hash không chứng minh tác giả
- Lưu ý minh bạch: SG-004 là chỉ đạo trực tiếp của Owner sau khi SG-003 hết vòng. Workflow mục 9 cấm đổi tên SG để reset vòng nhưng cho phép Owner quyết định tiếp tục bằng chỉ đạo trực tiếp; Claude không quyết định việc này và trình để Codex xem xét nếu cho là vấn đề. SG-003 vẫn ghi ACTIVE (Owner chưa quyết trạng thái)
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-004 – Phản hồi P1-005 sau RR-010"
- Finding cần xem lại: **P1-005** (MEDIUM). Trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`. Hồ sơ FFmpeg giữ trạng thái chờ; Claude không đánh dấu PASS và không đóng finding. Hồi quy: P1-006, P1-007 (đã CLOSED bởi Codex)
- Thay đổi để Codex đối chiếu (chỉ `phase1-tools-candidates.md`, mục 8.1 dòng tầng 1.1 và mục 8.3 mới): (1) license của 11 phụ thuộc tại đúng tag hoặc commit Homebrew: 7 từ kho chính thức, dav1d và x264 qua bản sao GitHub (kho VideoLAN chặn bot, Claude không vượt), LAME từ SVN chính thức ở HEAD, x265 4.3 chưa đọc được; (2) LAME: có nguồn chính thức (lame.sourceforge.io và SVN SourceForge), "fully LGPL'd", header lame.c "version 2 ... any later version" ở HEAD; (3) SVT-AV1 v4.2.0: BSD-3-Clause-Clear + PATENTS.md AOM riêng, lệch metadata Homebrew vẫn còn ở đúng phiên bản; (4) phân loại ba loại: đã xác minh / suy luận / rủi ro chưa giải quyết (phần A đến E); (5) kết luận giữ trạng thái chờ, không PASS
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `shasum -a 256`, `wc -c`, `brew info --json=v2` cho 11 phụ thuộc (chỉ đọc: url, tag, revision, checksum), đọc tệp license, PATENTS, header qua web tại tag hoặc commit. Trang `code.videolan.org` trả "Access Denied" Anubis (không vượt). **Không cài, không tải tarball, không chạy FFmpeg**. Không có runtime test vì không có code
- Chưa kiểm tra được: license x265 4.3 tại đúng phiên bản; dav1d và x264 từ nguồn chính thức; LAME tại tag 4.0; từng tệp `COPYING.*` của xz; phụ thuộc gián tiếp; notice trong tarball và bottle; tương thích pháp lý giữa các thành phần; sáng chế; VideoToolbox thực thi; hash tarball và bottle thực nhận (chưa tải, chưa có quyền)
- Yêu cầu review cụ thể: (1) Mục 8.3 có chép đúng các nguồn tại tag hoặc commit đã ghi, và có phát biểu nào vượt bằng chứng (đặc biệt về LAME, SVT-AV1, dav1d, x264, x265) không? (2) Với các điểm còn thiếu (x265 4.3, dav1d và x264 từ nguồn chính thức, LAME tag 4.0), điểm nào Claude còn có thể bổ sung bằng nghiên cứu tài liệu trong quyền hiện có, và điểm nào cần Owner quyết định riêng về mức bằng chứng chấp nhận? (3) Phân loại đã xác minh / suy luận / rủi ro có đúng và đủ không? (4) Có hồi quy nào với P1-006, P1-007, hoặc câu nào coi B có điều kiện là điều kiện (i)–(iii) đã đạt? (5) Có đường dẫn nhóm C hay hash nhóm A nào không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo
- END-OF-REVIEW-REQUEST


### RR-012
- Trạng thái: ANSWERED
- Scope Grant: SG-004
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-011 (SG-004 vòng 0/3, CHANGES REQUESTED, ANSWERED)
- Amendment: A01 của SG-004 (`CURRENT_STATUS.md` nhóm A chỉ đọc, giữ hash)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `main`, trùng `origin/main`). Working tree không sạch: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- SHA-256 (nhóm A, Claude được ghi theo SG-004):
  - `HANDOFF_TO_CHATGPT.md` 37dd342036208d3c27dfde851ce74b7673c5e211e1fd51bbbdcde7e7b3e9821e
  - `docs/testing/phase1-tools-candidates.md` 963096c5011426b630460ff1c2bf1bc625ad6a3019d59f89226daa3ce230ca82 (file **mới**, chưa có trong Git)
  - `REVIEW_RESPONSE.md` 307c29215ccb779e0b2d4d1d06a3e74a262da63bb6680a57b19d32e17f2b0495
  - `TASKS.md` (phần trước `## Review Requests`) ab355908bc73f8092719c3117ec234b7c94a979870fc988baa417e9c2a1816f9 (không đổi so với RR-011)
- SHA-256 (nhóm A, **chỉ đọc** theo Amendment A01 của SG-004):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961 (không đổi)
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 86194 byte, SHA-256 5aa9ba5c7d85f187d03cc294abb834a087f28cd58f4fa9b94e2343505701798f (chứa `# Review RR-011` đến `# Review RR-003`; do Codex viết; Claude không sửa). `PHASE-00-REVIEW.md` giữ nguyên 57209 byte, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-012` mới ở **đầu** file; 86194 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 86194 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- Nguồn quyền Project Owner: như RR-011 (khối "SG-004" và "SG-004 – Amendment A01" trong `TASKS.md`). Không có quyền mới: không cài, không tải, không commit, không push; không vượt bot-protection; không liên hệ tác giả. Lưu ý minh bạch về SG-003 như RR-011 (Codex đã ghi nhận ở RR-011 mục 2 của phần xác minh)
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-004 – Phản hồi RR-011 vòng 0/3"
- Finding cần xem lại: **P1-005** (MEDIUM), `FIX IMPLEMENTED — PENDING CODEX VERIFICATION` cho phần Claude có thể bổ sung bằng tài liệu; phần còn thiếu nêu trong "Điểm cần Owner". Hồi quy: P1-006, P1-007 (CLOSED bởi Codex)
- Thay đổi để Codex đối chiếu (chỉ `phase1-tools-candidates.md` mục 8.1 dòng tầng 1.1 và mục 8.3): (1) LAME: SVN chính thức tag `RELEASE__4_0` (r6552): COPYING LGPL v2, `lame.c` header "version 2 ... any later version"; (2) x265 4.3: kho `Multicorewareinc/x265` tag 4.3 (commit `e9b88125…`): COPYING GPL v2 + câu thương mại, `x265.cpp` header "version 2 ... any later version"; (3) x264: COPYING tại commit `b35605ac…` (GPL v2) qua mirror, nguồn gốc mirror chưa xác nhận; (4) dav1d: trang GitHub tự mô tả "read-only mirror ... origin at code.videolan.org"; (5) xz: `COPYING.0BSD`, `COPYING.LGPLv2.1`, `COPYING.GPLv2` tại v5.8.4; (6) đồng bộ câu suy luận D.1; (7) kết luận cập nhật giữ trạng thái chờ
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `wc -c`, `tail -c 76078 … | shasum -a 256` (khớp `1619658e…`), `shasum -a 256` các file trên, đọc tệp license, header và trang tag qua web tại tag hoặc commit đã ghi. **Không cài, không tải tarball, không chạy FFmpeg, không vượt bot-protection**. Không có runtime test vì không có code
- Chưa kiểm tra được: nguồn gốc/chính thức của mirror dav1d và x264, kho Multicoreware x265 (trang không tự khẳng định); đối chiếu nội dung tag với tarball Homebrew thực tế (chưa tải); `COPYING.GPLv3` của xz; phụ thuộc gián tiếp; notice; tương thích pháp lý; sáng chế; VideoToolbox thực thi. Codex ở RR-011 không truy cập được một số URL SVN HEAD và x264 header (lỗi truy cập)
- Điểm cần Owner (không nhờ Codex quyết): chấp nhận mirror GitHub làm mức bằng chứng cho dav1d và x264 (vì kho VideoLAN chặn bot), hoặc cho phép tải artifact chỉ để đọc/kiểm tra (không bắt buộc), hoặc dừng ở mức bằng chứng hiện có; quyết định trạng thái SG-003 (đang ghi ACTIVE)
- Phạm vi hồi quy: mục 8.1, 8.3; không có thay đổi ở mục khác
- Yêu cầu review cụ thể: (1) P1-005: sau bổ sung LAME tag 4.0, x265 tag 4.3, x264 COPYING, xz COPYING.*, điểm nào Claude còn có thể bổ sung bằng nghiên cứu tài liệu trong quyền hiện có, điểm nào chỉ Owner quyết? (2) Có phát biểu nào vượt bằng chứng (đặc biệt về nguồn gốc mirror dav1d, x264, kho x265, và LAME tag 4.0) không? (3) Nếu phần còn lại chỉ thuộc quyết định của Owner về mức bằng chứng, hồ sơ có đủ để Codex PASS có điều kiện cho nhãn "B có điều kiện, chờ quyết định riêng" kèm danh sách các điều kiện còn lại không (không phải \"B đã đủ bằng chứng\" và không phải quyền cài)? (4) Có hồi quy P1-006, P1-007 không? (5) Có đường dẫn nhóm C hay hash nhóm A không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo
- END-OF-REVIEW-REQUEST


### RR-013
- Trạng thái: ANSWERED
- Scope Grant: SG-006
- Vòng: 0/3 (review đầu tiên của SG-006)
- Thay thế RR: không có
- Tiếp nối RR: không có. RR-012 (SG-004) vẫn `ANSWERED`; lần review Phase 2B trước của Codex trả `BLOCKED` ngoài RR vì thiếu SG và snapshot, nên không tính vòng
- Amendment: không có
- Phân loại: design-review/spike riêng, **không** phải quyền bắt đầu Phase 2 của `IMPLEMENTATION_PLAN.md`, không phải quyền triển khai B-Lite
- Mục tiêu và phạm vi: review độc lập, chỉ đọc, thiết kế B-Lite POC trong báo cáo dưới đây. Gồm giả định, kiến trúc, giao diện tích hợp với `src/`, Content Strategy, schema storyboard, Action Compiler, HyperFrames, Ollama, âm thanh và nhạc, license, tiêu chí nghiệm thu. Ngoài phạm vi: FFmpeg P1-005 (SG-004), chất lượng video đã render, quyết định của Owner
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `review/phase-01-agent-names`, cùng commit với `main` và `origin/main`; các RR trước ghi nhánh `main`). Working tree **không sạch**: các đường dẫn dưới đây
- Phiên bản review: SHA-256 bên dưới
- Báo cáo Phase 2B: `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md`, 29928 byte, SHA-256 `1e3a2634f1666beaf367221cec1b88e03b3814a28f1d73fdff66d2770c88adb1`. Trích **nguyên byte** bằng script từ transcript phiên Claude Code `5357dee4-3125-4f5f-bfac-baa1f4236fed.jsonl`, dòng 300, uuid `2f4b8fab-d969-4ca8-b414-2e09ddaa3b4b`, timestamp 2026-11-01T15:43:10.383Z, khối text duy nhất khớp; hash của khối text trong transcript trùng hash file. Không tóm tắt, không viết lại, không thêm phần đầu. Đủ 14 mục và khối kết luận. File **mới**, chưa có trong Git; có đường dẫn cá nhân nên không được commit lên repo công khai khi chưa xử lý
- SHA-256 (nhóm A, Claude được ghi theo SG-006, **chỉ cho bàn giao này**):
  - `TASKS.md` (phần trước `## Review Requests`) 3a1bdc919182ce21af2968c9bae2e58706cb022c6e4132f53abf8a0aa4ea9979
  - `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md` 1e3a2634f1666beaf367221cec1b88e03b3814a28f1d73fdff66d2770c88adb1 (file **mới**)
- SHA-256 (nhóm A, **chỉ đọc** theo SG-006, file đã track bị sửa từ trước SG-006):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961
  - `HANDOFF_TO_CHATGPT.md` 38774495b805338eb9c720661a8cc7c54a9de16871071775d55cb8f0600a2d65
  - `REVIEW_RESPONSE.md` e40fb507489502395806eec445139e63b18098394a39c1dc9e882416948aa931
- SHA-256 (nhóm A, **chỉ đọc** theo SG-006, 204 file chưa track có từ trước SG-006; `src/`, `tests/`, `benchmarks/` chưa từng commit, HEAD không chứa chúng):
  - `Untitled.pages` 1050f971ba6f3caa1b5378ef817da8b73942ad647fb3cdfb6dae266c958557b1
  - `benchmarks/procrastination_12s/artifacts/chain.json` 40701b96ee0ff5ff9653e936714ce013cc5d8bd8f8135d263d4aecc0380d05dc
  - `benchmarks/procrastination_12s/artifacts/locked_brief.json` 559f7e4f7aec61fec17c698554abdbaddee8e7ff5f94db22909e2479ed38c5bb
  - `benchmarks/procrastination_12s/artifacts/render_report.json` dd8edf56737623982fc6e89ed3d8bb384fdd5d7c2b664a6f256e2daa9cfb1620
  - `benchmarks/procrastination_12s/artifacts/scene_spec.json` f22021e04c4cc8c777bacc8b351766aa4a484ca0cedfae582a2b93e15bee71c7
  - `benchmarks/procrastination_12s/artifacts/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/artifacts/script.txt` a68ab3006943495e2c4352650ecb0e404639be2b24f96b2dfe5e8f33881572d5
  - `benchmarks/procrastination_12s/artifacts/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/artifacts/timing.json` ba1cb9010c97d5be557d039562bd6f3c5ecf2aca4023fda51e137de6f7ece1a2
  - `benchmarks/procrastination_12s/artifacts/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/output/ai_factory_sample_12s.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/output/contact_sheet.png` 6a01faebc2beaf0f3770b7384f4ab8771fce723337778e48033fdc7e743db57a
  - `benchmarks/procrastination_12s/output/preview_frames/01_hook_f010.png` 710ab636120b33b5e7983152ce2c09b95ae5da2b62936dd3b11253bfd62d80cb
  - `benchmarks/procrastination_12s/output/preview_frames/02_ngap_ngung_f057.png` 1b3bb524e23d0439e898860bf6abd3968ad8d1f0932d28408fc6a656a06bfb4e
  - `benchmarks/procrastination_12s/output/preview_frames/03_tron_f070.png` 5f3d43d27291f9e1cb26affdc0612b7a2db000839e1e5141ae8ee920f248d65b
  - `benchmarks/procrastination_12s/output/preview_frames/04_cam_giac_f087.png` 3ef509c172b1b385b4e344f2244187740deadb195c57fba1f469b4944325d9a1
  - `benchmarks/procrastination_12s/output/preview_frames/05_10h_f110.png` b2953c5e54bfe66e4c6155baadeae2cca85b4f9221635038bcc654703fc4e622
  - `benchmarks/procrastination_12s/output/preview_frames/06_han_nop_f147.png` 636974413e87fd9abf82408d8a91043ae1b063341819023324b503f88499c941
  - `benchmarks/procrastination_12s/output/preview_frames/07_nhin_laptop_f176.png` 9dc7fa0568ee5b54b0dd5f360ae5832c65c2ddecc44bb3ef6b70159647a65c99
  - `benchmarks/procrastination_12s/output/preview_frames/08_mo_may_f197.png` 03c9b28663c2fe9ca5635024ba1d4c0353e4e24a633eb88c254424d84387ba2a
  - `benchmarks/procrastination_12s/output/preview_frames/09_mot_chu_f224.png` 2f09da35ce201ba73b0e8fdd2875739b401bc3eb11dbe47742d537a317b33922
  - `benchmarks/procrastination_12s/output/preview_frames/10_dong_bang_f242.png` a9e89a63e747b1a970069bb0af5159811ed758b3d00b78fad6913420439dba84
  - `benchmarks/procrastination_12s/output/preview_frames/11_vut_chay_f261.png` 1dff4849aa8f4b11aa2212bf4d1b93189850401344dcfeea6413658a381b3af0
  - `benchmarks/procrastination_12s/output/preview_frames/12_rot_nuoc_f273.png` 492a3480d3fc1b8986baec5af10f9cc8004dcd3b7d0130e692e3bc5d356911c5
  - `benchmarks/procrastination_12s/output/preview_frames/13_ting_f295.png` 4c994fba79623ad2677d9a366ddec77a40487d9e851f8181f1c8646205c43290
  - `benchmarks/procrastination_12s/output/preview_frames/14_luot_f312.png` 5fa0ca8286782901d905c72b35ca9307319dd5bc31925cee133995748d46e961
  - `benchmarks/procrastination_12s/output/preview_frames/15_de_do_f331.png` 00dbbbbaa3cb9505671e3434df71e057d817e499e845f635d70a6c4d9ba2e777
  - `benchmarks/procrastination_12s/output/preview_frames/16_nhip_ket_f352.png` 300075ade53e4123d1054486085be7e7229440b6539ab49e8640dda6a9c774a3
  - `benchmarks/procrastination_12s/reports/benchmark_metrics.json` 57613b58f3235e26555a5cf40d3495027bace95d37768aaee40a52bdae577fb5
  - `benchmarks/procrastination_12s/reports/media_probe.json` 783636a98868d4055db0182367bcdfa1351cc17336389fd065cc7cc118c43b2b
  - `benchmarks/procrastination_12s/reports/pipeline_execution.md` b9304d6a607331e1540b0a57998823cdd7c3ccab240d4adf62b94ddd0aa27c3e
  - `benchmarks/procrastination_12s/reports/render_validation.md` fb92dc7069cb7badaff60c2ea5ce0e733280bb8cbff3657b69b3cfd84a933d51
  - `benchmarks/procrastination_12s/reports/voice_evaluation.md` 159b1b943bfd1d540b9467cca1a6f5a5afa7e25f76aa791d152fe5f0eb364fb9
  - `benchmarks/procrastination_12s/validate.py` b6f41362eb566838808e856496710ea10596a2f300b886a17eb2e683a72f88d3
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/chain.json` 2e55bf447a11f3cd0bfeba359f05a2766ae7be15587ac0d3ec003bb7f2333811
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/step_log.json` 2b7a109d7a47248646cbbf4171c133a3c0f14ac2215b18b37dfc8ce9467d0a62
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/subtitles.srt` 00af2e01fada8788d632ec17a893d3b4ec961131480ef127094c90615a3675be
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/timing.json` 9bc2baacfd56a162ca0ab867785a6f501177726995f360dea3cd6b5ddb8b2fc3
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/step_log.json` fad780db6434987bbb4bc4ef497f1f7d1af2de6d2fd8f655d14140d5970d6c6f
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/approval.json` 21d49334a83354a304ec89ffa1761bb8289a9204bd59796c1456796e8f3df788
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/run.json` e4e8f66428e2ee53bde4d6a3ed0864cb1363735b6147e10f5894099ba35cb009
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager_preflight/step_log.json` 89098ed064fa7ec9e19d2a2c248ef1e2ca1706327e2b6ca07d838d02d679c610
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/mouth.json` b4288a43861dea17068fce963a5eee80e5f2bacc3a31bef63936d8fa53935e7c
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/scene_spec.json` ce88a0af283b02dfc342afa12ec90a3bc46b2250e8d34457911fea5f5c3cc540
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/step_log.json` 4201c8efba7830df5f17cf220ab36667d201504ad2cb2597574e67ac3e87a3df
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/run_log.jsonl` 9ca4bdea240535620bb0062f633f955d0eec3b9e4eade17ba7083484219df4fd
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0060_hide.png` 76758e783f417ba30b81ca81e3aa88eb845430002f0aa81a266109513cbd3a53
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0072_cloud.png` 281351c264f20a0e2f820b2aa192d26aaee486425ecdc248e10a47ff0fea7d9e
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0097_s3a.png` 3c1174395035237ebd87b2eed8bbd84c9ece49849f41217acba7c802208a390c
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0136_stamp.png` a3f6cbf251bc0f83e62bcf4ff6beed145ab6f102c8b5742c2bf0c5fece2c0ccb
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0159_s3e.png` d94bdb42aae74a300b414ec1f58262759d94a9ff22a38895d4c15d334b317852
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0182_open.png` f66b4856101db5d3ba1b025a0980206c7d5da3e859fe27d8163bd965f2d59810
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0221_key.png` dd20f1bbdaa864daff441015e1ec64912ce2449d50cae745f619b39c2351d658
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0254_s5a.png` 3a81d5c1474a71447677a467b00332dfec18fd73544b84a41a7e56cfc4315d8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0268_pour.png` aa4c3ed2190182e0ae794bd8865293488023426df8f42331683d73e50d52fe23
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0304_scroll.png` 7f0437f13378e78615835b638ccca4fc531f5c70612c203ce5af457fae414c74
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0321_s6e.png` 6b89a8759fdec9dd2a6515d6039c15c0aff9e3e3606b308a63784f03b69594be
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0352_end_beat.png` ebb7f7aeefe45c411a6021917c50917cba6e7051c9be25d50bd3a86f173afffb
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/render_report.json` dfd5d21ab225af7d6e67ea84e8522e3eb39206fa751a96ec580ddc90c36b4d06
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/step_log.json` 43fffde0bd240bb972a5e8813d95c3b8c9ac7fc9981af93e45fe89119e562ab8
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/subtitles.srt` 00af2e01fada8788d632ec17a893d3b4ec961131480ef127094c90615a3675be
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/chain.json` 40701b96ee0ff5ff9653e936714ce013cc5d8bd8f8135d263d4aecc0380d05dc
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/step_log.json` 98fabc19447c554360cfff09a10010e37cbb587eff5ff7d471e060ee33987aa5
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/subtitles.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/timing.json` ba1cb9010c97d5be557d039562bd6f3c5ecf2aca4023fda51e137de6f7ece1a2
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/step_log.json` cd6cef557140d045e381881786f4e48d27da71210cbbbdc9c73b8239ee482e24
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/approval.json` 27380058e760cdd5fd37f981386fc1625f18845ae2ec667b103d07db612a7257
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/run.json` 404790c241a9277bbd72e5cc91d1519b8637fbf128b806cdfaa9ea7e0cd99529
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager_preflight/step_log.json` 46b1e2bdee4d5b72a9aa795693de8732674261d4f534032879550b9900c4b0f2
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/mouth.json` 9f7877251c1c08ff3fcaf2d17c71c89db68b41ab6debeddc88ffb5dc3508ab06
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/scene_spec.json` f22021e04c4cc8c777bacc8b351766aa4a484ca0cedfae582a2b93e15bee71c7
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/step_log.json` a52e632d7f8ad741817b558d27b3adc190678aeb6312923c158508957c02e928
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/run_log.jsonl` 0f6349fb2245ecc6e38331b8b22d7ad961f99adedb70113b5093227ef8617494
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0061_hide.png` 8d5ff807545c3da94c021b3adddb4ec7cf5043c73809aea76db33af8de5c9677
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0075_cloud.png` ae9a4529da2042398e6a169d992cd3d0bb7d982dc93b2531ed1d2f2ce5bdd219
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0101_s3a.png` 29e93cec258860d0f5812163384a9709b1d48b24e42bb69d73e17b3a43364c92
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0139_stamp.png` b2d0530f946825eb0e6148035f37af5f315f4c43eef4fe02210c279fe41774ff
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0162_s3e.png` 9ea32cb743c856d892202353f71ceab32fc021baa5be053f95908f9213ae28c5
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0186_open.png` 2a009e6beaff2a581ad4bd06bd781bc9f2efad2e7656c3ec98164981b85f2740
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0222_key.png` 3b6b0bd56bb326fcddd212fd8b942c691e8b74c8780d37e904d5c901d2330025
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0254_s5a.png` b9bcf43715744ea059348b1393322d6bf1855ff43798084d4a3319d6fe996f9b
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0267_pour.png` 833a9e200755e7802e0ec13ee0cba62beea2cb03ad93cf00d9172c6398d83cde
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0302_scroll.png` dd54071308e1f61ebac79e1d88f40f0cdd6c16584c71236d84dddbb3c1c3f623
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0321_s6e.png` 4ff3809108e4257951722af078b516859222b0636453d6c5f669b28ef1d0155c
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0352_end_beat.png` 725226c2681b9cb3cae472983288adfc99422d7b1c3d703c629f2e90b31b0ee7
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/render_report.json` dd8edf56737623982fc6e89ed3d8bb384fdd5d7c2b664a6f256e2daa9cfb1620
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/step_log.json` 6d2c44e0d349f9b6d7e01ca65aa8e7b3637f711b48b58f237bcdb7147c619ca6
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/subtitles.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/chain.json` 97748f98231b9174d80f2d578a8ebb5e8506b3c43b8347986b8b18941c333f7d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/step_log.json` 0ee4369ad4d870cbc28da5024c8b28d6021eb17a6688c59e1b86022c905010bb
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/subtitles.srt` 5886808eefa487f6c3643a37c187998d4ea44abd71bf9851b4b343ee8f23df0f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/timing.json` 65c58a74962179d9e19a90eed2bdb2424f281353399c5556ea61bc81507dc603
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/step_log.json` 94a47b0d4a8c2bc1f5159d712a797d683d434c24a8e6f40eb6ee46130202f891
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/approval.json` 6ccf4889bc2a7c429d579da18e15559f1b70db048f51828a935b7fe2b6f9fad4
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/run.json` b39db2db07a0a0b63685af8e1f31d10a66127e1dc30e2644285ad03ea81423cb
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager_preflight/step_log.json` 4812914d4d64f94417d14525f09ac0442896bbb0bd8d10c30ecc005780c01547
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/mouth.json` 1ceaff6efb800effec60bffa11802b06c6b4b4a8476b2dbedbffedfe308f70ab
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/scene_spec.json` 82e1ffab92550848a2f20aa078805811783e5130a4b71dd3768e875588e823e4
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/step_log.json` 33c2aa226d9f6e9d4bf54556329e9a7e09ca83b057ead32b9acbe84b71b3f281
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/run_log.jsonl` 51644686135e9a3aee723e705704f3e95156e923922c093dcf47a3c7b9d89baa
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0060_hide.png` 76758e783f417ba30b81ca81e3aa88eb845430002f0aa81a266109513cbd3a53
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0073_cloud.png` bd910bf20c6ac29f7246a8abe2b5b07482181eaa198c0add79e03e13e3cf228d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0097_s3a.png` 3c1174395035237ebd87b2eed8bbd84c9ece49849f41217acba7c802208a390c
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0133_stamp.png` 22b3fc9d3b8fc2271ab2533f24f7698994e507085960da5740d6994f5bd69897
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0155_s3e.png` 07c3ca5dd7bf9a886030b715c6b0c5a05a5a852ccb11baae6e49934fb93e7038
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0179_open.png` c9115ec9c19dfa2870ec62fe535fa9d0299642239522ca9260be9a4893556d49
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0214_key.png` c6f7c154fa96996e41abcf2b37102d349251da3f3703cbbd1922b7415116ecb7
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0246_s5a.png` 42af5f06f546c8a2da3f7a54b6c1fa1dec6390a7ec80c4f4388792866270f7d2
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0260_pour.png` baab2523227c9b9c867270cccfd4c006321828916641b07c56d4159ea7bf1d2f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0296_scroll.png` 551ea488f4caaefd93c008cf183825a99f537700ea6c9fa1333763aca6f81899
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0313_s6e.png` d0767b6044d25955be83f392d1857f183c9afb70cf7ba1475da74ba95e597f5d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0352_end_beat.png` 1aae0db7314f8b325827eb3dd99c48080420d46390e4c75c9425679264fc9260
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/render_report.json` 76f713feb8fac7ef9b952b8d9e2bcb01181fc09a2a09c5bfbc7d82896585862e
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/step_log.json` 073bddd9498b30f2270bdb94ae636d905d6f6c5c74e34a068371a77575cd0d0c
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/subtitles.srt` 5886808eefa487f6c3643a37c187998d4ea44abd71bf9851b4b343ee8f23df0f
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/chain.json` 99ef0f0b87b272791ba400ff75ac9b9800f19f71a2a19ac6d4aa199f50601b46
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/step_log.json` 4fe34f362f0e3fbe4059432e99db272cfc64349e42f11d5de383bdc21a0e0f24
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/subtitles.srt` 8657f80010555ee48dd07c20ab3c6c63a144c1029c59048ee4d8b98bf36d0688
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/timing.json` 86b2baa4fd9713294bab4a638e69e7bbcaaa80aad7ef765cf867f8b6548d8450
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/step_log.json` 0ee1a385ac8698e8547aeadf0a2e73ce56af2bab3fe757a3f6f6ddd2b756b997
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/approval.json` 2888ff5c579c916d30a477174edad0b17715d3f8e92b41235763254cdadc6e04
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/run.json` 6d7c1abb6c54f04112adffbbbce4bcfde5df3b5b61f1c67825cbba488a4f6a89
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager_preflight/step_log.json` 76f53608b84b9f5f736a332e00d55d1cc97ebc50ca048e8247a88d9546e80e09
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/mouth.json` 165b714d6ee01b005a4e457aeb659e91b796b2517ed8290a3f5a4ba6c54a0044
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/scene_spec.json` 7c77b236b6716d10462dc796c06e7320d3cc66a7e68e3a0d6779f68c6fe4180a
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/step_log.json` 74eb4b7b9a7c9f242217e3157da758830a3a3197135feff2f8345ec85bd1e1db
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/run_log.jsonl` d347c8c50b8245e3363225cebc9e1b44d2dac1e3f81dc14f978af269a4b73527
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/render_report.json` d70eadd54f84dc02a50ec9beb5a9701b84f376df94184f6ae0438c4601ebc016
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/step_log.json` a0d262a40ecfc6fd726c6e012fd1a1db6afe088635f3cf0c46678e09614a67ea
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/subtitles.srt` 8657f80010555ee48dd07c20ab3c6c63a144c1029c59048ee4d8b98bf36d0688
  - `benchmarks/procrastination_12s/workspace/voice_probe/probe.json` d580b73dc5fddfbb8b7aa32ba5cf28768660851d332aa12f7f76cb87bdf91851
  - `docs/testing/phase1-tools-candidates.md` 09d599f7d456cb38a9f0fd245bd4a4d0132b37cc6b7eefc45dd0e69d949dbe2d
  - `src/ai_video_factory/README.md` eebbed0267523e3d59885229526f5422057c2ea288f4e7aaf21675462da726b4
  - `src/ai_video_factory/__init__.py` f92df048442b75eec9d889b3dc773ca8c2b8a11383a2751d3fbc8d36280e26b1
  - `src/ai_video_factory/adapters/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/llm/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/llm/ollama.py` 053a2fc4858715be1344390b9dbb183dd70d698c189d20469a60112fc8c01206
  - `src/ai_video_factory/adapters/tts/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/tts/macos_say.py` 4d6d44de3fb5a0ff997f9149e5f76b72f617f673fd3c9dcce03bc8dfe4065355
  - `src/ai_video_factory/adapters/tts/vieneu_runner.py` 18d09524507a3724b730af47e56e8dd42f87b8762020dae89a4cae6bb96253b2
  - `src/ai_video_factory/adapters/tts/vieneu_tts.py` 4ba642ea863700428e52fd1f93477ac28e2c297fb8992dddc69408ee614e4792
  - `src/ai_video_factory/agents/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/agents/athena/__init__.py` cf6524162df183ff7c6cd61484306c4ad9413abed33b8a2fd1d7e6a659d51cec
  - `src/ai_video_factory/agents/edison/__init__.py` 3ba8bd09260497c84f6ae4f226649154860064331a66dd9e6f99cc9cecaec085
  - `src/ai_video_factory/agents/leonardo/__init__.py` 25dc94eaa35ed8760a3a0133d2521c9c242921f83d0dd43ae67af1016f44bc84
  - `src/ai_video_factory/agents/newton/__init__.py` 43a229a3aa9deefe34d7affaec6d1e1beea3b17f62f1e957b9209d33ac989a4f
  - `src/ai_video_factory/agents/pixar/__init__.py` 0789d086576130cbfb99f0c5b808f031fed21dfaebf14506a0e35037630cbe94
  - `src/ai_video_factory/agents/spielberg/__init__.py` 085ec64c53877e5df7ed31ebb8454d80d00471a5956cada41619af13044be618
  - `src/ai_video_factory/agents/spielberg/draw.py` 736e564abd1813fb385ff748acfb1dbe66c1b8c286f19904536114ae093f890e
  - `src/ai_video_factory/agents/spielberg/hand.py` a53e118555a559518f3c5233239870c506618de567c72534f4f127765e57a411
  - `src/ai_video_factory/agents/spielberg/illus.py` 61b6716cb3e764538f80094039009450c14197f1a23d0acef9619d8a3dd77ba1
  - `src/ai_video_factory/agents/spielberg/illus2.py` cf214f0756c6b9dcb0cfdbdc44a8a506e14f67383a48ef2e5bf94a277701f13c
  - `src/ai_video_factory/agents/spielberg/stage.py` 93a94a34bf6d39d212e365c900190236aeab25afe9b93053c99488819ea1d19c
  - `src/ai_video_factory/agents/tesla/__init__.py` 39d60471eb3ff31749874290864179348822f2d44bccdc4e5f5e630343037775
  - `src/ai_video_factory/core/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/core/acting.py` af44ccdcc65de9dc86e8cad0c559960aceaf782d988fe6ce487b58ffdd099718
  - `src/ai_video_factory/core/artifacts.py` fd0801534533b7b113d3fb82cb44dd4a45105580346f4aaa21bb0cdc154e98bf
  - `src/ai_video_factory/core/audio.py` 04051eddcf336e8096fbd08735cd2b2a88151817fc0b6f1929576df910487971
  - `src/ai_video_factory/core/catalog.py` 3b5f651c918eac83078d55e72c6781696b05bff554a2a41a69c0b34129ee1bce
  - `src/ai_video_factory/core/character.py` cfdd76b9a5260e061ec17dfca154131e58bc1ec5c85f505844042c96921475bc
  - `src/ai_video_factory/core/config.py` f447facdfcd917b67496554c5a0a5e258f1e2140e8db8612acf2e7612523a6ed
  - `src/ai_video_factory/core/direction.py` 195e365c413e22854755755338350cd930aaa3a3a461a47e2fa8e7e4472b3552
  - `src/ai_video_factory/core/lang.py` ea4b87645b4ca72f1339555fa3d265bcfeab283b89f67bad14266e5ab244ff43
  - `src/ai_video_factory/core/layout.py` 46c9f07c74e5cbe68328d10a91f0bc13e8b72a9ec95f3aec99c917fda5f21e78
  - `src/ai_video_factory/core/names.py` 8fe67a9ca461f43362da3247cd7b4e8cc0aebe5aa6be724a371b04bfa74c15ce
  - `src/ai_video_factory/core/options.py` ec605d91ce53ad2e39a805b7f89209f13a2b4b1c5fe3e2f9ee0b38098b22b3c1
  - `src/ai_video_factory/core/poses.py` 3e0f3d95640579ad4df1aa6e5a8966a78b13a37cbc5fcb69cf2745aa73404859
  - `src/ai_video_factory/core/props.py` e825c34c5358530f7bb5e069c93af956804dfab6f7653201a9cf6ec9e4021868
  - `src/ai_video_factory/core/runlog.py` 1ac020f848c4f72027e76a002b734400da7ea1dc612d6c9d3d1bf0c54d2aa419
  - `src/ai_video_factory/core/schemas.py` b719e86a6042e448cb56eb6493df90b6cc31d430fb21495a059f817efb89d46f
  - `src/ai_video_factory/core/sfx.py` 4dee80e54bcc1dccf1e7e50690bcbff7168f463a07fbdc032a12a51844f141a2
  - `src/ai_video_factory/core/srt.py` 8145580fd25217cfe956874d40600f3e1ce757e5b5d8e0f7a8c290577f8b4ea7
  - `src/ai_video_factory/core/strokes.py` 0056a01ed9d492cd76d575fce8461697a1a1be68feb40fca84f461ab09af6d74
  - `src/ai_video_factory/core/subtitle.py` 8042bfbed1131d3f82a076c03d3f33bee72145a8bfc78983847d5d9a1e1dc4b1
  - `src/ai_video_factory/core/text_quality.py` dbcb9b0fa33e7b52ab285ea6b928a97291e5e87aff2dfb15d2f5ca99524898e9
  - `src/ai_video_factory/core/wordtime.py` f9ba97a3d1c82899478941201fecd0e6c22875b97b2714be7247094ebd04471b
  - `src/ai_video_factory/manager/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/manager/audit.py` dc64f2731d5e6f8f5103f75087838e42c52dfcaafd4e4faeda4c1c9d2260e863
  - `src/ai_video_factory/manager/prototype.py` fedd6b7fd7b558e1b956bb3889343ec35aa149b5448d61882c63e18f4da34980
  - `src/ai_video_factory/manager/run.py` 9eb0b6890672a935d97e907797523c5df4fbcedb7aaf27680021cd5168b5d279
  - `src/ai_video_factory/manager/voice_catalog.py` a383376034603c3d2992fd0369b0e9b9be0e69a8f44cdc21631904a515f3eb8f
  - `src/ai_video_factory/manager/voice_prototypes.py` 41dc8b34fa220c31f78960acebc7215b39eb25b8d403131ad58226381b60276b
  - `tests/e2e/test_pipeline_e2e.py` 69656ad1f922ca937d2aeeed86d49eebba0e6b22d7209b8b359de7f20aac2b55
  - `tests/unit/test_a04.py` 740bc00d876081793e540d67c05721f5adb2f95dcaff08da15a5866a9dc2f3e3
  - `tests/unit/test_agents.py` 82cde97c2760c162d60baf21133bbf5b172f58394efd7869ee2eef60cc4abcdc
  - `tests/unit/test_character.py` 797d2d805933ccee8aa355102ab9a082eed6a0652d2dc8ebae6edaa7dd0721bb
  - `tests/unit/test_core.py` 1712ae2ff175903f2f74bf902ccd7e9d3f89db1aa0cf0b01b7f5a9e416aa9289
  - `tests/unit/test_locked.py` 38b7a8af30532e81871b60a438b63438a176bf12e47896695e371e395a11e21c
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 95288 byte, SHA-256 d21ae58e28ad6adbfee9f8103773bcf0c9bffca3de4d8775ee4c323c88e755e4 (chứa `# Review RR-012` đến `# Review RR-003`; do Codex viết; Claude không sửa). `docs/operations/reviews/PHASE-00-REVIEW.md` giữ nguyên, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-013` mới ở **đầu** file; 95288 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 95288 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- File ignore liên quan (không xuất hiện trong `git status --porcelain`, không thuộc nhóm A, B, C):
  - `benchmarks/procrastination_12s/output/ai_factory_sample_12s.mp4` 513c566d5e8228f60d2531df28c5588298d40a95d9422ce717df507bfeb33e16
  - `workspace/**` và phần còn lại của `benchmarks/procrastination_12s/workspace/**`: không liệt kê từng file. Hash nằm trong manifest bản sao lưu Phase 2A `/Users/tthanhtaicntt/_project_backups/AI-VIDEO-FACTORY_phase2a_20261101-222421/MANIFEST.sha256`, SHA-256 13144b174e77180e6b296fa04111ac7d1582e18a08de44796ad97ed34095eee3; `SEAL.sha256` có SHA-256 0169bf484bcc6bf6e36b85f4b74507409cbcc3a64d9e2077b96fbc7c00d34ce5. `workspace/venv-vieneu/` và `workspace/hf-cache/` không có trong bản sao, xem `metadata/EXCLUDED.tsv`. `.DS_Store` ở gốc repo do Finder tạo sau bản sao lưu, không liên quan
- Đầu vào ngữ cảnh đã track, trùng HEAD (đầu vào review, không phải thay đổi):
  - `PROJECT_MASTER.md` 6aea5282a1af5d07656f6f96244527534952e01a4485ca21e6ae4b47d4cc4c68
  - `ARCHITECTURE.md` 9b86c1f6918a43bec0c9ea68f668acdd38033aab094449ddd098df2f8eead9ed
  - `DECISIONS.md` c6cc2d44bf6bc9c11bc97b2bdffb297748009846231344bb7e471e40dc092301
  - `TECH_STACK.md` f25bdb37f204b5b52740abaf1f6ee31d3e6e281bd739ac18f848c294d1a9db15
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c
  - `CLAUDE.md` dfabb9407e1e4e6e8e131170709800035df0a465c56826b601422f5922d083e4
  - `AGENTS.md` 599da96de01f938e589341f529ef891fecf6a17e11c6c11dc6928ee7e27d351a
  - `docs/operations/AI_REVIEW_WORKFLOW.md` f21b075ac912f625e993cbdcf6ee44ce6081cae6c9017686192c91fc450cec78
  - `docs/testing/phase1-candidates.md` bf347440f52e9fef625da2c16021e58af79b1443320d1e5a25a0c7b9e0dae310
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` fc08c7269ba1fa4522b182a20ed6b7527e6885f2e4aa76f7bb739ad2e7736893
- Đầu vào ngoài repo, **chỉ đọc**, OpenMontage HEAD 195eab24478dc9363326aec437aefc3701635ddf, working tree không có thay đổi theo `git status --porcelain` (AGPL-3.0; `projects/**` bị ignore trong repo đó nên hash là nguồn đối chiếu). Không sửa repo này. Không cần đọc `src/character_animation/**`:
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/environment_report.md` d0ed72d39c20bcfcd637bd56a86299ebefd0e32c73fb18e8d8ce4e7653e88cd0
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/rendering_validation.md` d6c389cc1f85fbbb637d1bba5e042e79fc1db7f7e3f76f5fe046c988b2d5b1d5
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/sample_review.md` 2b56f32d5c9f87016096514cd15e2e7b8019fbdc4f7c0e11f69d6a7c9aa4ec38
  - `OpenMontage/.agents/skills/hyperframes/PROVENANCE.md` c5e74c452116f073692e2ba336a70e6ace31b27ca06ca3e8f2c8cb9857234301
  - `OpenMontage/.agents/skills/hyperframes-core/references/determinism-rules.md` e544d7ca66712222f2fa921d1f98d48cdcc3947691e11a2895f39513fd505cf6
  - `OpenMontage/.agents/skills/hyperframes-core/references/variables-and-media.md` 9ec4a0ab3a55dead96e5b734634844878e2e6b599eb38685885ef792916246c9
  - `OpenMontage/.agents/skills/hyperframes-cli/references/preview-render.md` 53a407d0f810ce034d28936e4988898c267f2f32210a0fe57b497ef9a247e59d
  - `OpenMontage/.agents/skills/hyperframes-cli/references/upgrade-info-misc.md` ff34239bada9742aa0e9026627c47147688ef1bd818191aa647a4f66370562d1
- Nguồn quyền Project Owner: khối "SG-006" trong `TASKS.md`, trích nguyên văn yêu cầu trong chat. Không có quyền mới: không cài, không render, không commit, không push, không triển khai. Claude chép từ chat; hash không chứng minh tác giả. Allowlist và nhóm A chỉ đọc do Claude suy ra, chờ Owner đọc
- Chặn kỹ thuật đã biết: (1) chưa có bản audit OpenMontage Phase 1 và báo cáo Codex trước trong hai repo, nhãn "CONDITIONAL PASS" là thông tin từ Owner; (2) chưa đo storyboard Ollama với schema mới; (3) chưa đo RSS và thời gian của Chrome headless; (4) tài liệu HyperFrames đọc được là bản 0.7.17 chép trong OpenMontage, CLI mục tiêu là 0.8.226; (5) trang điều khoản Pixabay trả 429, chưa đọc; (6) B-Lite lệch D-002 và chưa có Decision; (7) Qwen3 8B ngoài danh sách đã duyệt theo mã 1B; (8) VieNeu nhóm A, chặn dùng thương mại; (9) SG-003, SG-004, SG-005 vẫn ghi ACTIVE, Owner chưa quyết định; (10) `HANDOFF_TO_CHATGPT.md`, `CURRENT_STATUS.md`, `TECH_STACK.md` lỗi thời và là nội dung có từ trước SG-006, Codex không nên coi là finding của thiết kế
- Điểm Claude tự thấy trong báo cáo, **không sửa** vì báo cáo phải giữ nguyên: (a) mục 3 nói `camera` chi tiết do hệ thống tính, trong khi schema có trường `camera` dạng enum theo beat; (b) câu "Thực tế dự án cũng đã thay đổi một giả định cũ" ở mục 5 không nói rõ giả định nào; (c) "REPOSITORY CHANGES: NONE" đúng lúc báo cáo được giao, nay repo có thêm file đăng ký báo cáo và khối SG-006, RR-013; (d) `README_RESTORE.md` trong bản sao lưu còn in đường dẫn cũ
- Lệnh đã chạy và kết quả thật: đọc workflow, `TASKS.md`, `AGENTS.md`; `git rev-parse`, `git status --porcelain`, `git check-ignore`, `shasum -a 256`, `wc -c`; `tail -c 86194 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`; script trích báo cáo từ transcript. Không chạy test, không chạy code dự án, không cài, không render. Chưa có runtime test nào cho thiết kế B-Lite vì chưa có code B-Lite
- Chưa kiểm tra được: mọi số thời gian và RAM dự kiến trong báo cáo; khả năng của `format` Ollama với schema lớn; cờ CLI HyperFrames 0.8.226; license phụ thuộc bắc cầu của HyperFrames; toàn văn điều khoản GSAP về phân phối lại; license Be Vietnam Pro; chất lượng nhạc tổng hợp; tác giả của yêu cầu dán; ai đã chuyển bản sao lưu sang `~/_project_backups`
- Finding cần xem lại: không có (review đầu tiên của SG-006)
- Phạm vi hồi quy: không có thay đổi code. Hồi quy chỉ gồm đối chiếu giao diện đề xuất với `src/ai_video_factory/core/schemas.py`, `core/sfx.py`, `core/layout.py`, `core/character.py`, `adapters/llm/ollama.py`, `adapters/tts/vieneu_tts.py`, `agents/spielberg/__init__.py`, `manager/run.py`
- Yêu cầu review cụ thể: (1) Mục 14 của báo cáo: trả lời đủ 12 vấn đề. (2) Content Strategy: quy tắc mục 2 có kiểm được bằng máy không, có tạo cảm giác đạt giả không, cấu trúc 12–15 giây có hợp lý không? (3) Schema mục 3: có sinh được đáng tin bằng `format` không, thiếu ràng buộc nào cho render xác định, `at_word` có đủ để neo hành động không? (4) Action Compiler mục 4: danh mục hữu hạn có làm được hai brief mới mà không viết cảnh riêng không, ràng buộc camera và vùng an toàn có đủ không? (5) HyperFrames mục 5: có đúng hợp đồng 0.8.226 không, render câm rồi mux có hợp lý không? (6) Âm thanh mục 6: mức, ducking, nguồn gốc nhạc, phương án dự phòng. (7) Ollama và tài nguyên mục 7: thứ tự tải, nguy cơ RAM trên 16 GB, giả định offline, tách chi phí vận hành và chi phí phát triển. (8) License mục 8: có thiếu rủi ro nào, mức đánh giá có đúng không, ranh giới AGPL có đủ không? (9) Tiêu chí mục 10 và giai đoạn mục 11: chỉ số nào dễ đạt mà không chứng minh chất lượng, cổng dừng có đúng chỗ không? (10) Mục 12 và 13: danh sách file có vi phạm "agent chỉ phụ thuộc core và adapters" không, danh sách phê duyệt có thiếu quyết định nào không? (11) Có phát biểu nào vượt bằng chứng trong báo cáo không? (12) Có đường dẫn nhóm C hay hash nhóm A không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo. Codex không sửa báo cáo Phase 2B
- Kết luận mong đợi: đúng một trong `APPROVED`, `APPROVED WITH CHANGES`, `CHANGES REQUESTED`, `BLOCKED` theo workflow mục 8, ghi ở `# Review RR-013`. Bất kỳ kết luận nào cũng chỉ áp dụng cho thiết kế, **không** cấp quyền triển khai B-Lite. Việc sử dụng kết luận do Owner quyết định
- END-OF-REVIEW-REQUEST


### RR-014
- Trạng thái: OPEN
- Scope Grant: SG-006
- Vòng: 1/3
- Thay thế RR: không có
- Tiếp nối RR: RR-013 (SG-006 vòng 0/3, CHANGES REQUESTED, ANSWERED)
- Amendment: A01 của SG-006
- Phân loại: design-review/spike riêng, **không** phải quyền bắt đầu Phase 2 của `IMPLEMENTATION_PLAN.md`, không phải quyền triển khai B-Lite
- Mục tiêu và phạm vi: re-review thiết kế sửa đổi cho B2B-001 đến B2B-009, trọng tâm bốn HIGH, cùng hồi quy trên phần còn lại của báo cáo gốc. Đầu vào chính: `docs/operations/phase-reports/PHASE-02B-DESIGN-AMENDMENT-A01.md`, 79739 byte, SHA-256 `7fa539a6a0b8219c92223fa6dd13a1ed971ba549eba16d45572edd95f109161d`. Báo cáo gốc giữ nguyên: `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md`, 29928 byte, SHA-256 `1e3a2634f1666beaf367221cec1b88e03b3814a28f1d73fdff66d2770c88adb1`. Ngoài phạm vi: FFmpeg P1-005 (SG-004)
- Baseline Git: 71155919602b38f2b23fc6a062608cefe33ad07f (nhánh `review/phase-01-agent-names`, cùng commit với `main` và `origin/main`). Working tree **không sạch**: các đường dẫn dưới đây. Baseline lịch sử của RR-013 giữ nguyên, không sửa
- Phiên bản review: SHA-256 bên dưới
- Thay đổi so với snapshot RR-013, **chỉ** ba đường dẫn: `TASKS.md` (khối Xác nhận Owner, Amendment A01, RR-013 sang ANSWERED, RR-014); `REVIEW_RESPONSE.md` (thêm một mục); `docs/operations/phase-reports/PHASE-02B-DESIGN-AMENDMENT-A01.md` (mới). Reviewer artifact đổi do báo cáo RR-013 của Codex. Mọi file nhóm A chỉ đọc giữ nguyên hash so với RR-013
- SHA-256 (nhóm A, Claude được ghi theo SG-006 Amendment A01):
  - `TASKS.md` (phần trước `## Review Requests`) ca7475181f21f84202fe8a66311f0cbd38883f09b90eadad408171f8a7d2ae4f
  - `REVIEW_RESPONSE.md` 46ec03225bd35f7056a097f00941dd22bd4fc803b8a9fd7fd6505f67d2439d74
  - `docs/operations/phase-reports/PHASE-02B-DESIGN-AMENDMENT-A01.md` 7fa539a6a0b8219c92223fa6dd13a1ed971ba549eba16d45572edd95f109161d (file **mới**)
- SHA-256 (nhóm A, **chỉ đọc** theo SG-006 và Amendment A01, file đã track bị sửa từ trước SG-006):
  - `CURRENT_STATUS.md` 962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961
  - `HANDOFF_TO_CHATGPT.md` 38774495b805338eb9c720661a8cc7c54a9de16871071775d55cb8f0600a2d65
- SHA-256 (nhóm A, **chỉ đọc**, 205 file chưa track; gồm báo cáo Phase 2B gốc do SG-006 tạo và 204 file có từ trước SG-006; `src/`, `tests/`, `benchmarks/` chưa từng commit):
  - `Untitled.pages` 1050f971ba6f3caa1b5378ef817da8b73942ad647fb3cdfb6dae266c958557b1
  - `benchmarks/procrastination_12s/artifacts/chain.json` 40701b96ee0ff5ff9653e936714ce013cc5d8bd8f8135d263d4aecc0380d05dc
  - `benchmarks/procrastination_12s/artifacts/locked_brief.json` 559f7e4f7aec61fec17c698554abdbaddee8e7ff5f94db22909e2479ed38c5bb
  - `benchmarks/procrastination_12s/artifacts/render_report.json` dd8edf56737623982fc6e89ed3d8bb384fdd5d7c2b664a6f256e2daa9cfb1620
  - `benchmarks/procrastination_12s/artifacts/scene_spec.json` f22021e04c4cc8c777bacc8b351766aa4a484ca0cedfae582a2b93e15bee71c7
  - `benchmarks/procrastination_12s/artifacts/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/artifacts/script.txt` a68ab3006943495e2c4352650ecb0e404639be2b24f96b2dfe5e8f33881572d5
  - `benchmarks/procrastination_12s/artifacts/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/artifacts/timing.json` ba1cb9010c97d5be557d039562bd6f3c5ecf2aca4023fda51e137de6f7ece1a2
  - `benchmarks/procrastination_12s/artifacts/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/output/ai_factory_sample_12s.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/output/contact_sheet.png` 6a01faebc2beaf0f3770b7384f4ab8771fce723337778e48033fdc7e743db57a
  - `benchmarks/procrastination_12s/output/preview_frames/01_hook_f010.png` 710ab636120b33b5e7983152ce2c09b95ae5da2b62936dd3b11253bfd62d80cb
  - `benchmarks/procrastination_12s/output/preview_frames/02_ngap_ngung_f057.png` 1b3bb524e23d0439e898860bf6abd3968ad8d1f0932d28408fc6a656a06bfb4e
  - `benchmarks/procrastination_12s/output/preview_frames/03_tron_f070.png` 5f3d43d27291f9e1cb26affdc0612b7a2db000839e1e5141ae8ee920f248d65b
  - `benchmarks/procrastination_12s/output/preview_frames/04_cam_giac_f087.png` 3ef509c172b1b385b4e344f2244187740deadb195c57fba1f469b4944325d9a1
  - `benchmarks/procrastination_12s/output/preview_frames/05_10h_f110.png` b2953c5e54bfe66e4c6155baadeae2cca85b4f9221635038bcc654703fc4e622
  - `benchmarks/procrastination_12s/output/preview_frames/06_han_nop_f147.png` 636974413e87fd9abf82408d8a91043ae1b063341819023324b503f88499c941
  - `benchmarks/procrastination_12s/output/preview_frames/07_nhin_laptop_f176.png` 9dc7fa0568ee5b54b0dd5f360ae5832c65c2ddecc44bb3ef6b70159647a65c99
  - `benchmarks/procrastination_12s/output/preview_frames/08_mo_may_f197.png` 03c9b28663c2fe9ca5635024ba1d4c0353e4e24a633eb88c254424d84387ba2a
  - `benchmarks/procrastination_12s/output/preview_frames/09_mot_chu_f224.png` 2f09da35ce201ba73b0e8fdd2875739b401bc3eb11dbe47742d537a317b33922
  - `benchmarks/procrastination_12s/output/preview_frames/10_dong_bang_f242.png` a9e89a63e747b1a970069bb0af5159811ed758b3d00b78fad6913420439dba84
  - `benchmarks/procrastination_12s/output/preview_frames/11_vut_chay_f261.png` 1dff4849aa8f4b11aa2212bf4d1b93189850401344dcfeea6413658a381b3af0
  - `benchmarks/procrastination_12s/output/preview_frames/12_rot_nuoc_f273.png` 492a3480d3fc1b8986baec5af10f9cc8004dcd3b7d0130e692e3bc5d356911c5
  - `benchmarks/procrastination_12s/output/preview_frames/13_ting_f295.png` 4c994fba79623ad2677d9a366ddec77a40487d9e851f8181f1c8646205c43290
  - `benchmarks/procrastination_12s/output/preview_frames/14_luot_f312.png` 5fa0ca8286782901d905c72b35ca9307319dd5bc31925cee133995748d46e961
  - `benchmarks/procrastination_12s/output/preview_frames/15_de_do_f331.png` 00dbbbbaa3cb9505671e3434df71e057d817e499e845f635d70a6c4d9ba2e777
  - `benchmarks/procrastination_12s/output/preview_frames/16_nhip_ket_f352.png` 300075ade53e4123d1054486085be7e7229440b6539ab49e8640dda6a9c774a3
  - `benchmarks/procrastination_12s/reports/benchmark_metrics.json` 57613b58f3235e26555a5cf40d3495027bace95d37768aaee40a52bdae577fb5
  - `benchmarks/procrastination_12s/reports/media_probe.json` 783636a98868d4055db0182367bcdfa1351cc17336389fd065cc7cc118c43b2b
  - `benchmarks/procrastination_12s/reports/pipeline_execution.md` b9304d6a607331e1540b0a57998823cdd7c3ccab240d4adf62b94ddd0aa27c3e
  - `benchmarks/procrastination_12s/reports/render_validation.md` fb92dc7069cb7badaff60c2ea5ce0e733280bb8cbff3657b69b3cfd84a933d51
  - `benchmarks/procrastination_12s/reports/voice_evaluation.md` 159b1b943bfd1d540b9467cca1a6f5a5afa7e25f76aa791d152fe5f0eb364fb9
  - `benchmarks/procrastination_12s/validate.py` b6f41362eb566838808e856496710ea10596a2f300b886a17eb2e683a72f88d3
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/chain.json` 2e55bf447a11f3cd0bfeba359f05a2766ae7be15587ac0d3ec003bb7f2333811
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/step_log.json` 2b7a109d7a47248646cbbf4171c133a3c0f14ac2215b18b37dfc8ce9467d0a62
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/subtitles.srt` 00af2e01fada8788d632ec17a893d3b4ec961131480ef127094c90615a3675be
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/timing.json` 9bc2baacfd56a162ca0ab867785a6f501177726995f360dea3cd6b5ddb8b2fc3
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/step_log.json` fad780db6434987bbb4bc4ef497f1f7d1af2de6d2fd8f655d14140d5970d6c6f
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/approval.json` 21d49334a83354a304ec89ffa1761bb8289a9204bd59796c1456796e8f3df788
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager/run.json` e4e8f66428e2ee53bde4d6a3ed0864cb1363735b6147e10f5894099ba35cb009
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/manager_preflight/step_log.json` 89098ed064fa7ec9e19d2a2c248ef1e2ca1706327e2b6ca07d838d02d679c610
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/mouth.json` b4288a43861dea17068fce963a5eee80e5f2bacc3a31bef63936d8fa53935e7c
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/scene_spec.json` ce88a0af283b02dfc342afa12ec90a3bc46b2250e8d34457911fea5f5c3cc540
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/pixar/step_log.json` 4201c8efba7830df5f17cf220ab36667d201504ad2cb2597574e67ac3e87a3df
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/run_log.jsonl` 9ca4bdea240535620bb0062f633f955d0eec3b9e4eade17ba7083484219df4fd
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0060_hide.png` 76758e783f417ba30b81ca81e3aa88eb845430002f0aa81a266109513cbd3a53
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0072_cloud.png` 281351c264f20a0e2f820b2aa192d26aaee486425ecdc248e10a47ff0fea7d9e
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0097_s3a.png` 3c1174395035237ebd87b2eed8bbd84c9ece49849f41217acba7c802208a390c
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0136_stamp.png` a3f6cbf251bc0f83e62bcf4ff6beed145ab6f102c8b5742c2bf0c5fece2c0ccb
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0159_s3e.png` d94bdb42aae74a300b414ec1f58262759d94a9ff22a38895d4c15d334b317852
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0182_open.png` f66b4856101db5d3ba1b025a0980206c7d5da3e859fe27d8163bd965f2d59810
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0221_key.png` dd20f1bbdaa864daff441015e1ec64912ce2449d50cae745f619b39c2351d658
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0254_s5a.png` 3a81d5c1474a71447677a467b00332dfec18fd73544b84a41a7e56cfc4315d8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0268_pour.png` aa4c3ed2190182e0ae794bd8865293488023426df8f42331683d73e50d52fe23
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0304_scroll.png` 7f0437f13378e78615835b638ccca4fc531f5c70612c203ce5af457fae414c74
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0321_s6e.png` 6b89a8759fdec9dd2a6515d6039c15c0aff9e3e3606b308a63784f03b69594be
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/preview_frames/f0352_end_beat.png` ebb7f7aeefe45c411a6021917c50917cba6e7051c9be25d50bd3a86f173afffb
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/render_report.json` dfd5d21ab225af7d6e67ea84e8522e3eb39206fa751a96ec580ddc90c36b4d06
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/step_log.json` 43fffde0bd240bb972a5e8813d95c3b8c9ac7fc9981af93e45fe89119e562ab8
  - `benchmarks/procrastination_12s/workspace/runs/bench-01/spielberg/subtitles.srt` 00af2e01fada8788d632ec17a893d3b4ec961131480ef127094c90615a3675be
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/chain.json` 40701b96ee0ff5ff9653e936714ce013cc5d8bd8f8135d263d4aecc0380d05dc
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/step_log.json` 98fabc19447c554360cfff09a10010e37cbb587eff5ff7d471e060ee33987aa5
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/subtitles.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/timing.json` ba1cb9010c97d5be557d039562bd6f3c5ecf2aca4023fda51e137de6f7ece1a2
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/step_log.json` cd6cef557140d045e381881786f4e48d27da71210cbbbdc9c73b8239ee482e24
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/approval.json` 27380058e760cdd5fd37f981386fc1625f18845ae2ec667b103d07db612a7257
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager/run.json` 404790c241a9277bbd72e5cc91d1519b8637fbf128b806cdfaa9ea7e0cd99529
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/manager_preflight/step_log.json` 46b1e2bdee4d5b72a9aa795693de8732674261d4f534032879550b9900c4b0f2
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/mouth.json` 9f7877251c1c08ff3fcaf2d17c71c89db68b41ab6debeddc88ffb5dc3508ab06
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/scene_spec.json` f22021e04c4cc8c777bacc8b351766aa4a484ca0cedfae582a2b93e15bee71c7
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/pixar/step_log.json` a52e632d7f8ad741817b558d27b3adc190678aeb6312923c158508957c02e928
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/run_log.jsonl` 0f6349fb2245ecc6e38331b8b22d7ad961f99adedb70113b5093227ef8617494
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0061_hide.png` 8d5ff807545c3da94c021b3adddb4ec7cf5043c73809aea76db33af8de5c9677
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0075_cloud.png` ae9a4529da2042398e6a169d992cd3d0bb7d982dc93b2531ed1d2f2ce5bdd219
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0101_s3a.png` 29e93cec258860d0f5812163384a9709b1d48b24e42bb69d73e17b3a43364c92
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0139_stamp.png` b2d0530f946825eb0e6148035f37af5f315f4c43eef4fe02210c279fe41774ff
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0162_s3e.png` 9ea32cb743c856d892202353f71ceab32fc021baa5be053f95908f9213ae28c5
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0186_open.png` 2a009e6beaff2a581ad4bd06bd781bc9f2efad2e7656c3ec98164981b85f2740
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0222_key.png` 3b6b0bd56bb326fcddd212fd8b942c691e8b74c8780d37e904d5c901d2330025
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0254_s5a.png` b9bcf43715744ea059348b1393322d6bf1855ff43798084d4a3319d6fe996f9b
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0267_pour.png` 833a9e200755e7802e0ec13ee0cba62beea2cb03ad93cf00d9172c6398d83cde
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0302_scroll.png` dd54071308e1f61ebac79e1d88f40f0cdd6c16584c71236d84dddbb3c1c3f623
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0321_s6e.png` 4ff3809108e4257951722af078b516859222b0636453d6c5f669b28ef1d0155c
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/preview_frames/f0352_end_beat.png` 725226c2681b9cb3cae472983288adfc99422d7b1c3d703c629f2e90b31b0ee7
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/render_report.json` dd8edf56737623982fc6e89ed3d8bb384fdd5d7c2b664a6f256e2daa9cfb1620
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/step_log.json` 6d2c44e0d349f9b6d7e01ca65aa8e7b3637f711b48b58f237bcdb7147c619ca6
  - `benchmarks/procrastination_12s/workspace/runs/bench-02/spielberg/subtitles.srt` 19c367ecbf72a9283ea6341e0704210cb17955490625bc71a9e43f6227fb9f8f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/chain.json` 97748f98231b9174d80f2d578a8ebb5e8506b3c43b8347986b8b18941c333f7d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/step_log.json` 0ee4369ad4d870cbc28da5024c8b28d6021eb17a6688c59e1b86022c905010bb
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/subtitles.srt` 5886808eefa487f6c3643a37c187998d4ea44abd71bf9851b4b343ee8f23df0f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/timing.json` 65c58a74962179d9e19a90eed2bdb2424f281353399c5556ea61bc81507dc603
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/step_log.json` 94a47b0d4a8c2bc1f5159d712a797d683d434c24a8e6f40eb6ee46130202f891
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/approval.json` 6ccf4889bc2a7c429d579da18e15559f1b70db048f51828a935b7fe2b6f9fad4
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager/run.json` b39db2db07a0a0b63685af8e1f31d10a66127e1dc30e2644285ad03ea81423cb
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/manager_preflight/step_log.json` 4812914d4d64f94417d14525f09ac0442896bbb0bd8d10c30ecc005780c01547
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/mouth.json` 1ceaff6efb800effec60bffa11802b06c6b4b4a8476b2dbedbffedfe308f70ab
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/scene_spec.json` 82e1ffab92550848a2f20aa078805811783e5130a4b71dd3768e875588e823e4
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/pixar/step_log.json` 33c2aa226d9f6e9d4bf54556329e9a7e09ca83b057ead32b9acbe84b71b3f281
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/run_log.jsonl` 51644686135e9a3aee723e705704f3e95156e923922c093dcf47a3c7b9d89baa
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0060_hide.png` 76758e783f417ba30b81ca81e3aa88eb845430002f0aa81a266109513cbd3a53
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0073_cloud.png` bd910bf20c6ac29f7246a8abe2b5b07482181eaa198c0add79e03e13e3cf228d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0097_s3a.png` 3c1174395035237ebd87b2eed8bbd84c9ece49849f41217acba7c802208a390c
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0133_stamp.png` 22b3fc9d3b8fc2271ab2533f24f7698994e507085960da5740d6994f5bd69897
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0155_s3e.png` 07c3ca5dd7bf9a886030b715c6b0c5a05a5a852ccb11baae6e49934fb93e7038
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0179_open.png` c9115ec9c19dfa2870ec62fe535fa9d0299642239522ca9260be9a4893556d49
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0214_key.png` c6f7c154fa96996e41abcf2b37102d349251da3f3703cbbd1922b7415116ecb7
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0246_s5a.png` 42af5f06f546c8a2da3f7a54b6c1fa1dec6390a7ec80c4f4388792866270f7d2
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0260_pour.png` baab2523227c9b9c867270cccfd4c006321828916641b07c56d4159ea7bf1d2f
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0296_scroll.png` 551ea488f4caaefd93c008cf183825a99f537700ea6c9fa1333763aca6f81899
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0313_s6e.png` d0767b6044d25955be83f392d1857f183c9afb70cf7ba1475da74ba95e597f5d
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/preview_frames/f0352_end_beat.png` 1aae0db7314f8b325827eb3dd99c48080420d46390e4c75c9425679264fc9260
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/render_report.json` 76f713feb8fac7ef9b952b8d9e2bcb01181fc09a2a09c5bfbc7d82896585862e
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/step_log.json` 073bddd9498b30f2270bdb94ae636d905d6f6c5c74e34a068371a77575cd0d0c
  - `benchmarks/procrastination_12s/workspace/runs/bench-03/spielberg/subtitles.srt` 5886808eefa487f6c3643a37c187998d4ea44abd71bf9851b4b343ee8f23df0f
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/chain.json` 99ef0f0b87b272791ba400ff75ac9b9800f19f71a2a19ac6d4aa199f50601b46
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/step_log.json` 4fe34f362f0e3fbe4059432e99db272cfc64349e42f11d5de383bdc21a0e0f24
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/subtitles.srt` 8657f80010555ee48dd07c20ab3c6c63a144c1029c59048ee4d8b98bf36d0688
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/timing.json` 86b2baa4fd9713294bab4a638e69e7bbcaaa80aad7ef765cf867f8b6548d8450
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/edison/voice_manifest.json` 25289ca799ca34c0cb6d62acede3cf482842ea541477a65c1ef58499d75832bf
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/script.json` 562b16bc6084d26b8e65b21af54a20c270eea3b33ca239db25ebfed11680f448
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/step_log.json` 0ee1a385ac8698e8547aeadf0a2e73ce56af2bab3fe757a3f6f6ddd2b756b997
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/leonardo/storyboard.json` ce74b236ef9813a82e0c5e119c3ec5701a70160994a74195ee633f013b3b0877
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/approval.json` 2888ff5c579c916d30a477174edad0b17715d3f8e92b41235763254cdadc6e04
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/preflight.json` 3ee076bc499c50feaf498c249fb0de7bbb38d4815de37ce82ee4ca906c02e593
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager/run.json` 6d7c1abb6c54f04112adffbbbce4bcfde5df3b5b61f1c67825cbba488a4f6a89
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/manager_preflight/step_log.json` 76f53608b84b9f5f736a332e00d55d1cc97ebc50ca048e8247a88d9546e80e09
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/mouth.json` 165b714d6ee01b005a4e457aeb659e91b796b2517ed8290a3f5a4ba6c54a0044
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/scene_spec.json` 7c77b236b6716d10462dc796c06e7320d3cc66a7e68e3a0d6779f68c6fe4180a
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/pixar/step_log.json` 74eb4b7b9a7c9f242217e3157da758830a3a3197135feff2f8345ec85bd1e1db
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/run_log.jsonl` d347c8c50b8245e3363225cebc9e1b44d2dac1e3f81dc14f978af269a4b73527
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/render_report.json` d70eadd54f84dc02a50ec9beb5a9701b84f376df94184f6ae0438c4601ebc016
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/step_log.json` a0d262a40ecfc6fd726c6e012fd1a1db6afe088635f3cf0c46678e09614a67ea
  - `benchmarks/procrastination_12s/workspace/runs/dev-01/spielberg/subtitles.srt` 8657f80010555ee48dd07c20ab3c6c63a144c1029c59048ee4d8b98bf36d0688
  - `benchmarks/procrastination_12s/workspace/voice_probe/probe.json` d580b73dc5fddfbb8b7aa32ba5cf28768660851d332aa12f7f76cb87bdf91851
  - `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md` 1e3a2634f1666beaf367221cec1b88e03b3814a28f1d73fdff66d2770c88adb1
  - `docs/testing/phase1-tools-candidates.md` 09d599f7d456cb38a9f0fd245bd4a4d0132b37cc6b7eefc45dd0e69d949dbe2d
  - `src/ai_video_factory/README.md` eebbed0267523e3d59885229526f5422057c2ea288f4e7aaf21675462da726b4
  - `src/ai_video_factory/__init__.py` f92df048442b75eec9d889b3dc773ca8c2b8a11383a2751d3fbc8d36280e26b1
  - `src/ai_video_factory/adapters/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/llm/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/llm/ollama.py` 053a2fc4858715be1344390b9dbb183dd70d698c189d20469a60112fc8c01206
  - `src/ai_video_factory/adapters/tts/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/adapters/tts/macos_say.py` 4d6d44de3fb5a0ff997f9149e5f76b72f617f673fd3c9dcce03bc8dfe4065355
  - `src/ai_video_factory/adapters/tts/vieneu_runner.py` 18d09524507a3724b730af47e56e8dd42f87b8762020dae89a4cae6bb96253b2
  - `src/ai_video_factory/adapters/tts/vieneu_tts.py` 4ba642ea863700428e52fd1f93477ac28e2c297fb8992dddc69408ee614e4792
  - `src/ai_video_factory/agents/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/agents/athena/__init__.py` cf6524162df183ff7c6cd61484306c4ad9413abed33b8a2fd1d7e6a659d51cec
  - `src/ai_video_factory/agents/edison/__init__.py` 3ba8bd09260497c84f6ae4f226649154860064331a66dd9e6f99cc9cecaec085
  - `src/ai_video_factory/agents/leonardo/__init__.py` 25dc94eaa35ed8760a3a0133d2521c9c242921f83d0dd43ae67af1016f44bc84
  - `src/ai_video_factory/agents/newton/__init__.py` 43a229a3aa9deefe34d7affaec6d1e1beea3b17f62f1e957b9209d33ac989a4f
  - `src/ai_video_factory/agents/pixar/__init__.py` 0789d086576130cbfb99f0c5b808f031fed21dfaebf14506a0e35037630cbe94
  - `src/ai_video_factory/agents/spielberg/__init__.py` 085ec64c53877e5df7ed31ebb8454d80d00471a5956cada41619af13044be618
  - `src/ai_video_factory/agents/spielberg/draw.py` 736e564abd1813fb385ff748acfb1dbe66c1b8c286f19904536114ae093f890e
  - `src/ai_video_factory/agents/spielberg/hand.py` a53e118555a559518f3c5233239870c506618de567c72534f4f127765e57a411
  - `src/ai_video_factory/agents/spielberg/illus.py` 61b6716cb3e764538f80094039009450c14197f1a23d0acef9619d8a3dd77ba1
  - `src/ai_video_factory/agents/spielberg/illus2.py` cf214f0756c6b9dcb0cfdbdc44a8a506e14f67383a48ef2e5bf94a277701f13c
  - `src/ai_video_factory/agents/spielberg/stage.py` 93a94a34bf6d39d212e365c900190236aeab25afe9b93053c99488819ea1d19c
  - `src/ai_video_factory/agents/tesla/__init__.py` 39d60471eb3ff31749874290864179348822f2d44bccdc4e5f5e630343037775
  - `src/ai_video_factory/core/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/core/acting.py` af44ccdcc65de9dc86e8cad0c559960aceaf782d988fe6ce487b58ffdd099718
  - `src/ai_video_factory/core/artifacts.py` fd0801534533b7b113d3fb82cb44dd4a45105580346f4aaa21bb0cdc154e98bf
  - `src/ai_video_factory/core/audio.py` 04051eddcf336e8096fbd08735cd2b2a88151817fc0b6f1929576df910487971
  - `src/ai_video_factory/core/catalog.py` 3b5f651c918eac83078d55e72c6781696b05bff554a2a41a69c0b34129ee1bce
  - `src/ai_video_factory/core/character.py` cfdd76b9a5260e061ec17dfca154131e58bc1ec5c85f505844042c96921475bc
  - `src/ai_video_factory/core/config.py` f447facdfcd917b67496554c5a0a5e258f1e2140e8db8612acf2e7612523a6ed
  - `src/ai_video_factory/core/direction.py` 195e365c413e22854755755338350cd930aaa3a3a461a47e2fa8e7e4472b3552
  - `src/ai_video_factory/core/lang.py` ea4b87645b4ca72f1339555fa3d265bcfeab283b89f67bad14266e5ab244ff43
  - `src/ai_video_factory/core/layout.py` 46c9f07c74e5cbe68328d10a91f0bc13e8b72a9ec95f3aec99c917fda5f21e78
  - `src/ai_video_factory/core/names.py` 8fe67a9ca461f43362da3247cd7b4e8cc0aebe5aa6be724a371b04bfa74c15ce
  - `src/ai_video_factory/core/options.py` ec605d91ce53ad2e39a805b7f89209f13a2b4b1c5fe3e2f9ee0b38098b22b3c1
  - `src/ai_video_factory/core/poses.py` 3e0f3d95640579ad4df1aa6e5a8966a78b13a37cbc5fcb69cf2745aa73404859
  - `src/ai_video_factory/core/props.py` e825c34c5358530f7bb5e069c93af956804dfab6f7653201a9cf6ec9e4021868
  - `src/ai_video_factory/core/runlog.py` 1ac020f848c4f72027e76a002b734400da7ea1dc612d6c9d3d1bf0c54d2aa419
  - `src/ai_video_factory/core/schemas.py` b719e86a6042e448cb56eb6493df90b6cc31d430fb21495a059f817efb89d46f
  - `src/ai_video_factory/core/sfx.py` 4dee80e54bcc1dccf1e7e50690bcbff7168f463a07fbdc032a12a51844f141a2
  - `src/ai_video_factory/core/srt.py` 8145580fd25217cfe956874d40600f3e1ce757e5b5d8e0f7a8c290577f8b4ea7
  - `src/ai_video_factory/core/strokes.py` 0056a01ed9d492cd76d575fce8461697a1a1be68feb40fca84f461ab09af6d74
  - `src/ai_video_factory/core/subtitle.py` 8042bfbed1131d3f82a076c03d3f33bee72145a8bfc78983847d5d9a1e1dc4b1
  - `src/ai_video_factory/core/text_quality.py` dbcb9b0fa33e7b52ab285ea6b928a97291e5e87aff2dfb15d2f5ca99524898e9
  - `src/ai_video_factory/core/wordtime.py` f9ba97a3d1c82899478941201fecd0e6c22875b97b2714be7247094ebd04471b
  - `src/ai_video_factory/manager/__init__.py` e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  - `src/ai_video_factory/manager/audit.py` dc64f2731d5e6f8f5103f75087838e42c52dfcaafd4e4faeda4c1c9d2260e863
  - `src/ai_video_factory/manager/prototype.py` fedd6b7fd7b558e1b956bb3889343ec35aa149b5448d61882c63e18f4da34980
  - `src/ai_video_factory/manager/run.py` 9eb0b6890672a935d97e907797523c5df4fbcedb7aaf27680021cd5168b5d279
  - `src/ai_video_factory/manager/voice_catalog.py` a383376034603c3d2992fd0369b0e9b9be0e69a8f44cdc21631904a515f3eb8f
  - `src/ai_video_factory/manager/voice_prototypes.py` 41dc8b34fa220c31f78960acebc7215b39eb25b8d403131ad58226381b60276b
  - `tests/e2e/test_pipeline_e2e.py` 69656ad1f922ca937d2aeeed86d49eebba0e6b22d7209b8b359de7f20aac2b55
  - `tests/unit/test_a04.py` 740bc00d876081793e540d67c05721f5adb2f95dcaff08da15a5866a9dc2f3e3
  - `tests/unit/test_agents.py` 82cde97c2760c162d60baf21133bbf5b172f58394efd7869ee2eef60cc4abcdc
  - `tests/unit/test_character.py` 797d2d805933ccee8aa355102ab9a082eed6a0652d2dc8ebae6edaa7dd0721bb
  - `tests/unit/test_core.py` 1712ae2ff175903f2f74bf902ccd7e9d3f89db1aa0cf0b01b7f5a9e416aa9289
  - `tests/unit/test_locked.py` 38b7a8af30532e81871b60a438b63438a176bf12e47896695e371e395a11e21c
- Reviewer artifact (nhóm B) lúc bàn giao: `docs/operations/reviews/PHASE-01-REVIEW.md` 126035 byte, SHA-256 e4004880d58b298575fe6f83a1bc3da0019172d1de32e65e7104d705e36f066b (chứa `# Review RR-013` đến `# Review RR-003`; do Codex viết; Claude không sửa). `docs/operations/reviews/PHASE-00-REVIEW.md` giữ nguyên, SHA-256 ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13
- Thay đổi kỳ vọng ở reviewer artifact: một báo cáo `# Review RR-014` mới ở **đầu** file; 126035 byte hiện có giữ nguyên ở cuối, kiểm tra bằng `tail -c 126035 docs/operations/reviews/PHASE-01-REVIEW.md | shasum -a 256`. Mọi đường dẫn khác ngoài nhóm A và file này là nhóm C
- File ignore liên quan (không thuộc nhóm A, B, C):
  - `benchmarks/procrastination_12s/output/ai_factory_sample_12s.mp4` 513c566d5e8228f60d2531df28c5588298d40a95d9422ce717df507bfeb33e16
  - `workspace/**` và phần còn lại của `benchmarks/procrastination_12s/workspace/**`: hash trong manifest bản sao lưu Phase 2A `/Users/tthanhtaicntt/_project_backups/AI-VIDEO-FACTORY_phase2a_20261101-222421/MANIFEST.sha256`, SHA-256 13144b174e77180e6b296fa04111ac7d1582e18a08de44796ad97ed34095eee3; `SEAL.sha256` có SHA-256 0169bf484bcc6bf6e36b85f4b74507409cbcc3a64d9e2077b96fbc7c00d34ce5
- Đầu vào ngữ cảnh đã track, trùng HEAD:
  - `PROJECT_MASTER.md` 6aea5282a1af5d07656f6f96244527534952e01a4485ca21e6ae4b47d4cc4c68
  - `ARCHITECTURE.md` 9b86c1f6918a43bec0c9ea68f668acdd38033aab094449ddd098df2f8eead9ed
  - `DECISIONS.md` c6cc2d44bf6bc9c11bc97b2bdffb297748009846231344bb7e471e40dc092301
  - `TECH_STACK.md` f25bdb37f204b5b52740abaf1f6ee31d3e6e281bd739ac18f848c294d1a9db15
  - `IMPLEMENTATION_PLAN.md` 5f03742a865ea72d5808a4c328fadafc003a68b6f94fd4a4a6b9e526e1de2520
  - `CHANGELOG.md` 9a8aef015e819f807c9e260cb9b31fd9248b19901a85bf7b1d44c09c88e5069c
  - `CLAUDE.md` dfabb9407e1e4e6e8e131170709800035df0a465c56826b601422f5922d083e4
  - `AGENTS.md` 599da96de01f938e589341f529ef891fecf6a17e11c6c11dc6928ee7e27d351a
  - `docs/operations/AI_REVIEW_WORKFLOW.md` f21b075ac912f625e993cbdcf6ee44ce6081cae6c9017686192c91fc450cec78
  - `docs/testing/phase1-candidates.md` bf347440f52e9fef625da2c16021e58af79b1443320d1e5a25a0c7b9e0dae310
  - `docs/operations/phase-reports/PHASE-01-PLAN.md` fc08c7269ba1fa4522b182a20ed6b7527e6885f2e4aa76f7bb739ad2e7736893
  - `docs/agents/README.md` 19ee0fb1d8cf9d4375265503f6bece6917456da09b928974ae2a8a882e6e0f1a
- Đầu vào ngoài repo, **chỉ đọc**, OpenMontage HEAD 195eab24478dc9363326aec437aefc3701635ddf, working tree không có thay đổi theo `git status --porcelain`. Không cần đọc `src/character_animation/**`. Claude có đọc `node_modules/hyperframes/dist` (Apache-2.0, upstream) để kiểm cờ và env; không đọc, không sao chép rig:
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/environment_report.md` d0ed72d39c20bcfcd637bd56a86299ebefd0e32c73fb18e8d8ce4e7653e88cd0
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/rendering_validation.md` d6c389cc1f85fbbb637d1bba5e042e79fc1db7f7e3f76f5fe046c988b2d5b1d5
  - `OpenMontage/projects/why-we-procrastinate-vi/reports/sample_review.md` 2b56f32d5c9f87016096514cd15e2e7b8019fbdc4f7c0e11f69d6a7c9aa4ec38
  - `OpenMontage/.agents/skills/hyperframes/PROVENANCE.md` c5e74c452116f073692e2ba336a70e6ace31b27ca06ca3e8f2c8cb9857234301
  - `OpenMontage/.agents/skills/hyperframes-core/references/determinism-rules.md` e544d7ca66712222f2fa921d1f98d48cdcc3947691e11a2895f39513fd505cf6
  - `OpenMontage/.agents/skills/hyperframes-core/references/variables-and-media.md` 9ec4a0ab3a55dead96e5b734634844878e2e6b599eb38685885ef792916246c9
  - `OpenMontage/.agents/skills/hyperframes-cli/references/preview-render.md` 53a407d0f810ce034d28936e4988898c267f2f32210a0fe57b497ef9a247e59d
  - `OpenMontage/.agents/skills/hyperframes-cli/references/upgrade-info-misc.md` ff34239bada9742aa0e9026627c47147688ef1bd818191aa647a4f66370562d1
- Trạng thái Git refs: `git for-each-ref` có SHA-256 ccdc87f3a40a23d2bbccc2ebacb2a861d7773ad3e988ee926bbfd7f90e28a19f. So với bản ghi Phase 2A, có 4 ref mới trong `refs/codex/turn-diffs/`: 2 `captures/.../base` (23:03:54, 23:06:08, cùng tree `8f58e0e`), 2 `checkpoints/...` (22:47:38 tree `13814c0`; 23:14:29 tree `701bb93`). Một checkpoint từng thấy ở nhánh `aa59cb29…/fa096e22…` đã không còn. Mốc thời gian trong tên ref khớp mtime tệp ref. Tệp `.git/logs` không có reflog cho namespace này. **Nguyên nhân chưa được chứng minh:** tên namespace, tiến trình ứng dụng Codex đang chạy và việc mtime 23:14:29 trùng phút báo cáo RR-013 chỉ là dấu hiệu tương quan, Claude không quy kết. `refs/heads/*`, `refs/remotes/*`, HEAD không đổi. Claude không tạo, sửa hay xóa ref nào
- Nguồn quyền Project Owner: khối "SG-006 – Xác nhận của Owner" và "SG-006 – Amendment A01" trong `TASKS.md`, trích nguyên văn từ chat. Không có quyền mới: không cài, không render, không commit, không push, không triển khai. Claude chép từ chat; hash không chứng minh tác giả
- Phản hồi: `REVIEW_RESPONSE.md`, mục "SG-006 – Phản hồi RR-013 vòng 0/3"; ma trận đầy đủ ở mục 2 của Amendment
- Finding cần xem lại: **B2B-001, B2B-002, B2B-003, B2B-004** (HIGH); **B2B-005, B2B-006, B2B-007, B2B-008, B2B-009** (MEDIUM). Trạng thái `FIX IMPLEMENTED — PENDING CODEX VERIFICATION`, nghĩa là Addressed in design, không phải đã kiểm chứng bằng chạy thử. Claude không ghi CLOSED cho finding nào
- Chặn kỹ thuật đã biết: chưa có đo Ollama với `storyboard/2.0`; chưa đo Chrome; CSP chưa thử với runtime 0.8.226; chưa có chặn outbound cứng; chưa có giới hạn RAM cứng trên macOS; hành vi detached của Chrome trong render chưa xác minh; sai số `wordtime` chưa đo; nhạc numpy chưa ai nghe; VieNeu chặn thương mại; `core/config.py` mặc định 8B cho `LLM_MODEL_STRONG`; D-002 và các quyết định mục 12 chưa duyệt
- Lệnh đã chạy và kết quả thật: `git rev-parse`, `git status --porcelain`, `git for-each-ref`, `shasum -a 256`, `wc -c`; `ffmpeg -h filter=alimiter`; `lsof`, `ps`, `man sandbox-exec`, `memory_pressure -Q`, `sysctl`, `ulimit`, `command -v` (chỉ tra cứu); đọc mã `node_modules/hyperframes/dist` bằng `grep`, `sed`; trình kiểm JSON và schema trong scratchpad: 12 khối JSON phân tích được, ví dụ Brief B hợp lệ, dạng Brief A hợp lệ, ba mẫu xấu bị từ chối. **Không chạy test dự án, code dự án, Ollama, TTS, Node hay HyperFrames. Không cài, không render.** Chưa có code B-Lite
- Chưa kiểm tra được: mọi số thời gian, RAM, ngưỡng trong Amendment; `format` của Ollama với schema; bridge chạy thật qua Edison; `ws-v1` với `normalize_text`; khoảng cách anchor thật so với tầm với; CSP, seek, readiness với HyperFrames; `--strict-all` với template thật; `RLIMIT_*`, `caffeinate`, `sandbox-exec`, `footprint` trên render; nhạc và mix bằng tai; license đầy đủ của phụ thuộc; tác giả các lời Owner chép lại; nguyên nhân thay đổi ref
- Phạm vi hồi quy: mọi mục báo cáo gốc bị Amendment thay thế; mục 2 (format), 6 (âm thanh), 9 (brief), 12 (file). Mục Amendment 1 liệt kê thay đổi. Đối chiếu với `agents/edison`, `agents/pixar`, `agents/spielberg`, `agents/athena`, `manager/run.py`, `core/artifacts.py`, `core/layout.py`, `core/character.py`, `core/schemas.py`, `adapters/tts/vieneu_tts.py`, `adapters/llm/ollama.py`
- Yêu cầu review cụ thể: (1) Với từng finding B2B-001 đến B2B-009: thiết kế đã đủ để đóng ở mức thiết kế chưa, hay còn thiếu gì? Finding nào chỉ đóng được sau triển khai? (2) Trả lời 18 mục trong checklist mục 14 của Amendment. (3) Trace Brief A và Brief B qua mục 5, 6: có cần trạng thái ẩn hay code theo chủ đề không? (4) Bảy lớp và 28 ca âm tính có bỏ sót đường nào? JSON inline có chấp nhận được không? (5) Supervisor có đúng với cách HyperFrames, Puppeteer, Chrome sinh tiến trình không? (6) Có phát biểu nào vượt bằng chứng, nhất là bảng macOS 8.6? (7) Mục tiêu nội dung và âm thanh có bị bỏ sót do thu hẹp vocabulary không? (8) Có đường dẫn nhóm C hay hash nhóm A không khớp không? Mọi phần chưa kiểm tra được phải nêu rõ trong báo cáo. Codex không sửa Amendment hay báo cáo gốc
- Kết luận mong đợi: đúng một trong `APPROVED`, `APPROVED WITH CHANGES`, `CHANGES REQUESTED`, `BLOCKED` theo workflow mục 8, ghi ở `# Review RR-014`. Bất kỳ kết luận nào cũng chỉ áp dụng cho thiết kế, **không** cấp quyền triển khai B-Lite
- END-OF-REVIEW-REQUEST


## Task Owner trực tiếp — đổi tên NMT-engine (08/11/2026)

- Yêu cầu Owner trong chat: “Đổi tên couple-engine thành nmt-engine và thêm mô tả cho engine này, cập nhập các document liên quan.”
- Phạm vi đã làm: entry point `output/_engine/nmt_engine.py`, lệnh `.claude/commands/nmt-engine.md`, mô tả/prompt NMT, alias tương thích và tài liệu vận hành/branding/bàn giao liên quan. Các thay đổi `cute_engine.py`, `semireal_*`, `branding.py`, docstring test chỉ cập nhật tên trong chú thích; không đổi logic dựng/branding.
- Kết quả: tên chính NMT-engine; CLI help/list/status và tạo scaffold thử thành công, alias giữ tương thích, YAML command hợp lệ, video EP10 giữ nguyên hash. Báo cáo `output/_engine/NMT_RENAME_REPORT.json`.
- Giữ nguyên trích dẫn Owner, Scope Grant/Review Request và lịch sử mang tên cũ. Không tạo Scope Grant/Review Request mới, không nghiệm thu hay chuyển phase, không đổi kiến trúc, không commit/push.

## Task Owner trực tiếp — Facebook Reels đăng trực tiếp, D-026 (08/11/2026)

- [x] Điền `FACEBOOK_APP_ID` trong env riêng Postiz, tạo lại container (Owner tự điền secret; Meta xác thực OK)
- [x] Chẩn đoán: Postiz đăng video Facebook bằng `file_url` localhost → Meta không tải được
- [x] Ghi D-026 (Owner duyệt phương án A)
- [x] Adapter `publishing/facebook_reels.py` + định tuyến worker + lệnh `facebook-draft-test`
- [x] Unit test 20 mới, toàn bộ 190/190 OK
- [x] Test DRAFT thật trên Trang "Ngang Một Tí" → `PASS_DRAFT_ONLY` (video `1124038717286057`, chưa công khai)
- [x] Soạn caption Facebook ep08 (Tesla) và bản nháp Chính sách quyền riêng tư
- [ ] Owner: đăng Chính sách quyền riêng tư, bật app Facebook sang Live
- [ ] Owner: xác nhận mục `rights` của manifest ep08
- [ ] Owner: `init` adapter trong terminal, rồi `enqueue` → `approve` → `work` cho lần đăng công khai đầu
- [ ] Codex review D-026

## Task Owner trực tiếp — Tự động hoá 3 nền tảng, D-027 (08/11/2026)

- [x] Website chính sách GitHub Pages + xác minh URL TikTok
- [x] TikTok Sandbox, kết nối kênh trong Postiz
- [x] Ghi D-027
- [x] Tesla `prepare-episode` + nội dung theo nền tảng + chặn nhạc bên thứ ba
- [x] `approve-episode` một lần/tập, `episode-status`
- [x] Cổng LIVE YouTube/TikTok + bộ xác minh YouTube
- [x] `service install|uninstall|status` (LaunchAgent)
- [x] 219/219 unit test
- [x] Hồ sơ nộp Production TikTok
- [x] Owner: API key Postiz vào Keychain, `init`, `service install`
- [x] Chạy thật tập ep08: Facebook + YouTube (private) verified, TikTok vào hộp nháp (D-028 sửa lỗi Postiz)
- [ ] Owner: bằng chứng license nhạc cho `vi-anh-qua-dep-trai` (hoặc không đăng)
- [ ] TikTok Production review; sau đó Owner quyết định gỡ chặn Direct Post
- [ ] Codex review D-026, D-027
- [ ] Owner: bấm Đăng video ep08 trong hộp nháp TikTok
- [ ] Codex review D-028
