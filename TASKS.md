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
- Trạng thái: ACTIVE

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
