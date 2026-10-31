# Review RR-006
- Ngày: 2026-10-31. Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-002 | Vòng: 3/3 (cuối) | Tiếp nối: RR-005.
- Baseline Git: `9838f0a2ca1073d152bb43ef1c6c2a7473c81d9d`, nhánh `main`; snapshot SHA-256 trong RR-006.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION** cho hồ sơ trong phạm vi. Đầu vào toàn vẹn hợp lệ; đây không phải BLOCKED.
- Phạm vi: chỉ năm mục “Nội dung thuộc SG-002” và hồi quy liên quan trong RR-006. Không đánh giá quyền hoặc tính hợp lệ của mục “Ngoài phạm vi”, không xác nhận số đo hay sự kiện tải model.

## Phát hiện

### [MEDIUM] P1-003 – Trạng thái hiện hành chưa đồng bộ với các quyết định 1B, 2A và D-024
- Vị trí: `docs/testing/phase1-candidates.md:23`, `:232`, `:260`; `docs/operations/phase-reports/PHASE-01-PLAN.md:30`; `HANDOFF_TO_CHATGPT.md:11`, `:38`; `REVIEW_RESPONSE.md:15`, `:33`.
- Bằng chứng: bảng danh sách và mục 4.1 ghi Owner duyệt riêng Qwen3 4B theo 1B, nhưng đoạn sau bảng bốn trạng thái vẫn nói “chưa có danh sách nào được Owner duyệt”; PLAN điều 2 cũng ghi chưa được Owner duyệt, trong khi điều 11 xác nhận duyệt 4B. Mục 7 nói “chưa chọn hướng nào” dù mục 8 ghi đã chọn 2A. Handoff ghi D-024 đã được ghi tại dòng 34 nhưng dòng 38 nói S2 chưa ghi vào DECISIONS. Bảng S2 còn ghi Codex chưa re-review dù RR-005 đã APPROVED. REVIEW_RESPONSE còn nói không có RR mới/không có RR OPEN; RR-006 đang OPEN theo TASKS.
- Tình huống gây lỗi: người tiếp nhận không xác định được điều gì đã được quyết định, điều gì còn chờ và báo cáo nào là hiện hành. TASKS ưu tiên khi xác định lượt giúp tránh bế tắc, nhưng không làm các phát biểu hiện hành sai trở thành nhất quán. Đây là mâu thuẫn hồ sơ trong mục 1, 4, 5 của RR, không phải kết luận về quyền của các thao tác ngoài phạm vi.
- Yêu cầu khắc phục: đồng bộ các câu hiện hành với 1B (chỉ 4B), 2A (nghiên cứu tài liệu), D-024 đã ghi và RR-006 vòng cuối; nếu giữ bản cũ làm lịch sử, gắn mốc/nhãn hết hiệu lực rõ ràng. Bảo toàn phân biệt phân loại B, duyệt từng artifact và quyền thực thi riêng. Không dùng yêu cầu này để mở rộng quyền hoặc tự sửa file ngoài phạm vi được Owner cấp.
- Trong phạm vi SG: có.

### [LOW] P1-004 – Lập luận thiếu LICENSE riêng của VieNeu mạnh hơn bằng chứng
- Vị trí: `docs/testing/phase1-candidates.md:162–163`.
- Bằng chứng: hồ sơ ghi không có tệp LICENSE trong kho model rồi kết luận “không có văn bản license ... cho đúng artifact trọng số”, điều kiện (i) không thỏa và “chỉ hỏi tác giả ... mới có thể làm rõ”. Chính dòng 162(c) đã ghi README tuyên bố license áp dụng cho mọi artifact. Đọc trực tiếp [model card chính thức](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo/raw/main/README.md) ngày 2026-10-31: FAQ nêu Apache-2.0 áp dụng cho trọng số, ONNX và tài sản giọng đi kèm, cho phép nội dung kiếm tiền và có tuyên bố đồng ý của người nói/quyền chủ thể. Thiếu tệp tên LICENSE riêng không tự chứng minh thiếu tuyên bố cấp phép cho trọng số.
- Tình huống gây lỗi: Owner có thể hiểu nhầm rằng nhà phát hành không cấp phép trọng số, hoặc liên hệ tác giả là con đường duy nhất, thay vì phân biệt tuyên bố cấp phép hiện có với phần bằng chứng độc lập còn thiếu.
- Yêu cầu khắc phục: ghi chính xác “chưa lưu/đối chiếu toàn văn điều khoản được README dẫn chiếu cho artifact tại revision đã chốt”; tách điều này khỏi việc không có tệp LICENSE riêng. Giữ rõ bất định dữ liệu, phụ thuộc, consent và phát biểu roadmap cần làm rõ. Không tự chuyển VieNeu lên B, không mở rộng S2 sang TTS và không liên hệ tác giả khi chưa được phép.
- Trong phạm vi SG: có. Phân loại A vẫn hợp lý; finding về độ chính xác của lý do, không phải kết luận đủ quyền thương mại. Nguồn web là snapshot hiện hành, chưa chứng minh README ở commit đã ghi giống hoàn toàn snapshot này.

## Đã tự xác minh

### Toàn vẹn mục 7 – PASS
1. TASKS có đúng một RR OPEN: RR-006; chưa có báo cáo cùng mã trước lượt này. SG-002 ACTIVE, có lời Owner trích nguyên văn, RR tham chiếu đúng SG.
2. RR-006 có END-OF-REVIEW-REQUEST. Chuỗi vòng RR-003/004/005/006 là 0/1/2/3, không reset hoặc vượt giới hạn.
3. HEAD và nhánh đúng baseline. Working tree đầu lượt chỉ có `HANDOFF_TO_CHATGPT.md`, `TASKS.md`, đều nhóm A; không có đường dẫn nhóm C.
4. Cả 9 hash nhóm A khớp RR-006, gồm TASKS chỉ băm phần trước `## Review Requests`.
5. Reviewer artifact Phase 1: 30,343 byte, SHA-256 `9e3919e458fb6909343a7d7ebde9171c05dd5c1b7cd39d6bb84b8829f1471a6a`. Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp.

### Kết quả đối chiếu nội dung
- 1B được ghi rõ ở bảng danh sách, mục 4.1/4.2 và PLAN điều 11: chỉ Qwen3 4B `q4_K_M`; 8B chưa duyệt tại quyết định đó. Không suy từ đây sang đánh giá các chỉ đạo ngoài phạm vi xảy ra sau.
- D-024 (`DECISIONS.md:94–99`) ghi đủ ba điều kiện S2, lời “Chọn S2”, rủi ro dư theo artifact và giới hạn phân loại; không thành quyền tải/cài/chạy, không áp dụng TTS tiếng Việt. Đối chiếu nội dung quyết định còn lại với bản trước và lịch sử review: 12 mục D-009–012, D-014–016, D-018–022 vẫn Proposed. D-013/D-017 có bản ghi lịch sử chỉ dẫn tới mục đã duyệt; không phát hiện phê duyệt mới từ D-024.
- PLAN điều 1–8 được ghi xác nhận theo “2G, 4C- xác nhận 1-8”, điều 9 bị bác, điều 11 chỉ duyệt danh sách 4B. R1 không chặn LLM theo điều 9 đã bỏ, nhưng vẫn phải trình Owner trước Phase 4/5.
- Không thấy câu biến nhóm B hoặc riêng 1B thành quyền chạy, hoặc biến số đo thô thành PASS chất lượng tiếng Việt. Không đánh giá bản thân số đo.
- TTS: chưa có cơ sở nâng ứng viên tiếng Việt lên B theo tiêu chuẩn hiện ghi; R1 còn mở. ViZipVoice giữ A hợp lý vì chưa hoàn tất license/định danh/chuỗi dữ liệu. [Model card ViZipVoice](https://huggingface.co/contextboxai/ViZipvoice) xác nhận checkpoint `checkpoint-1860000.pt`, FP16, fine-tune ZipVoice và khoảng 7,000 giờ; chưa chốt revision artifact độc lập.
- VietTTS giữ C phù hợp: [model card nhà phát hành](https://huggingface.co/dangvansam/viet-tts/raw/main/README.md) tách mã Apache-2.0 với model/âm thanh CC BY-NC. viXTTS giữ C phù hợp: [model card](https://huggingface.co/capleaf/viXTTS/raw/main/README.md) dẫn Coqui Public Model License; [LICENSE của model gốc XTTS-v2](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt) hạn chế model và đầu ra cho phi thương mại. Các nguồn truy cập 2026-10-31; đây là kiểm tra tài liệu, không xác nhận quyền của người phát hành đối với mọi dữ liệu.
- P1-001/P1-002 vẫn CLOSED theo RR-004; P1-003 là mâu thuẫn trạng thái mới sau các quyết định Owner, không đảo kết luận cũ về phân loại Qwen3.

## Chưa thể xác minh và giới hạn
- Không kiểm chứng độc lập nguồn gốc lời Owner được Claude chép vào file; hash không chứng minh tác giả hoặc phê duyệt.
- Không kiểm tra quyền/tính hợp lệ của cài đặt, tải, benchmark, commit/push hoặc nhãn A03–A07. Theo yêu cầu trực tiếp của Owner, các mục đó được loại khỏi kết luận SG-002; báo cáo này không hợp thức hóa hoặc bác bỏ chúng, cũng không quyết định hình thức cấp quyền cần dùng cho chúng.
- Không truy cập remote, không tải model, không chạy Ollama/benchmark; không xác minh digest tệp tải, hiệu năng, tiếng Việt, đầy đủ consent hay license mọi phụ thuộc. README GitHub hiện hành không thay bằng chứng runtime trên Mac.
- Không mở lại thiết kế Phase 0; không sửa Git cũ trong CURRENT_STATUS hay mục lịch sử D-013/D-017. Không cấp quyền sửa các tài liệu đó.

## Bàn giao
- **NEXT ACTOR: Claude**, chỉ đọc/phản hồi báo cáo và tóm tắt findings cho Owner theo workflow. **NEXT DECISION: Project Owner** vì đã dùng hết vòng 3/3 mà chưa PASS. Không tự mở vòng 4, gia hạn SG, đóng SG hay bắt đầu việc mới.
- Owner quyết định việc sửa/tiếp tục hoặc chấp nhận các điểm còn lại; reviewer không tự nghiệm thu. Chỉ thêm báo cáo này vào đầu file review; toàn bộ 30,343 byte lịch sử được giữ nguyên.

---

# Review RR-005

- Scope Grant: **SG-002**, Amendment **A01** | Vòng: **2/3**.
- Baseline Git: `e83ecec6493919a335de96b3183a508ecb7b4fbd`, `main`.
- Ngày: **2026-10-31**.
- Kết luận: **APPROVED — PASS cho hồ sơ phân loại theo S2 trong phạm vi RR-005**.
- **NEXT ACTOR: Claude**, phản hồi kết quả trong allowlist rồi chuyển **Project Owner** quyết định hướng TTS Việt, duyệt danh sách và quyền tải/cài/chạy. Reviewer không quyết định các việc đó.

## Phát hiện

Không có finding mới phải sửa trong phạm vi lần này. P1-001 và P1-002 vẫn **CLOSED** theo RR-004. Kết luận chỉ áp dụng cho hồ sơ nghiên cứu/phân loại; không chứng nhận license thương mại cuối cùng hoặc cấp quyền thực thi.

## Đã tự xác minh

### 1. Đầu vào

- Đọc workflow, SG-002/A01, RR-005 và các phần candidates, kế hoạch, handoff, phản hồi liên quan. SG ACTIVE; RR-004 ANSWERED; RR-005 là RR OPEN duy nhất, có end marker, vòng **1/3 → 2/3**, không reset.
- HEAD đúng baseline. **9/9 hash nhóm A khớp**, gồm TASKS dùng prefix trước Review Requests; không có đường dẫn thay đổi ngoài nhóm A hoặc file reviewer nhóm B.
- Trước khi ghi, PHASE-01-REVIEW.md đúng **21.512 byte**, SHA-256 `0eeec6f17a23ea7bc84226d4202ee57b4be2b3619d8bfd36dd0e2ebdb1b9fa87`; chưa có báo cáo RR-005. Bốn file chỉ đọc theo A01 giữ nguyên hash RR-003/RR-004.

### 2. Quyết định S2 được giới hạn đủ hẹp

Candidates mục 7.1 và REVIEW_RESPONSE ghi lời Owner là **“Chọn S2”**, đặt trong câu hỏi chọn tiêu chuẩn S1/S2. Có căn cứ trong hồ sơ để review theo tiêu chuẩn S2 được khai báo; hash không chứng minh nguồn lời này.

Cách áp dụng hiện hành chỉ chuyển **hai artifact Qwen3 Q4_K_M** sang nhóm đủ điều kiện **đề xuất** benchmark. Văn bản không coi S2 là kết luận pháp lý, duyệt danh sách, quyền tải/cài/chạy, ngân sách, quyền liên hệ ngoài hoặc commit/push; không tự áp dụng sang TTS.

Phân biệt quan trọng khi Owner duyệt sau này: chọn **tiêu chuẩn S2** không thay thế việc duyệt **từng ứng viên và các rủi ro dư kèm theo**. Mọi phần chưa xác minh phải đi cùng hồ sơ trình Owner, không được đổi thành “đã đủ quyền thương mại” chỉ vì lựa chọn S2.

### 3. Ba điều kiện S2 đối với Qwen3

**(i) Bằng chứng license đúng artifact/runtime — đạt ở mức tài liệu nguồn công khai phục vụ phân loại.** Ngày 2026-10-31, reviewer truy cập được trực tiếp trang license blob gắn với [Qwen3 4B Q4_K_M](https://ollama.com/library/qwen3:4b-q4_K_M/blobs/d18a5cc71b84) và [Qwen3 8B Q4_K_M](https://ollama.com/library/qwen3:8b-q4_K_M/blobs/d18a5cc71b84), cùng định danh blob ngắn `d18a5cc71b84`; nội dung hiển thị Apache License 2.0. Đã đối chiếu LICENSE của [Qwen3-4B tại revision được ghi](https://huggingface.co/Qwen/Qwen3-4B/raw/1cfa9a7208912126459214e8b04321603b3df60c/LICENSE) và [Ollama runtime](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE): Apache-2.0 và MIT tương ứng. LICENSE 8B đã được đọc độc lập trong RR-003.

Đây là đọc văn bản công khai gắn với tag/blob, không chỉ suy từ badge license của kho. Không yêu cầu hai LICENSE giống từng byte để kết luận cùng loại license; vẫn chưa xác minh hash nhị phân của blob hoặc quyền đầy đủ của mọi dependency/runtime version sẽ cài. Phần xác nhận nguồn mới này thuộc báo cáo reviewer, không có nghĩa Claude đã cập nhật hồ sơ của họ bằng bằng chứng reviewer.

**(ii) Định danh và phần chưa biết — đạt mức hồ sơ nghiên cứu, có giới hạn.** Hai tag tường minh, digest ngắn, model-layer digest, kích thước và commit đầu kho được khai báo; hồ sơ nói rõ chưa biết commit gốc dùng để chuyển GGUF. Không đánh đồng commit đầu kho với nguồn chuyển đổi, không đánh đồng hash layer với manifest hoặc hash tính lại từ weights. Metadata tag/dung lượng đã được đối chiếu từ Ollama ở các lượt trước. URL manifest registry của cả hai bản không truy cập được qua công cụ web trong lượt này; không độc lập chứng nhận toàn bộ digest dài/config/model-layer mới dựa riêng vào lời Claude. Không cần tải weights để hoàn tất phân loại nghiên cứu này, và không được dùng báo cáo làm xác nhận các tệp sẽ tải là đúng hash.

**(iii) Không có bằng chứng trái ngược — chưa thấy trong phạm vi nguồn đã đọc.** Các nguồn Qwen/Ollama đã kiểm tra không cho thấy điều khoản phi thương mại trái với Apache/MIT được công bố. Đây là kết quả kiểm tra có giới hạn, không chứng minh tuyệt đối không có tranh chấp hoặc mọi dữ liệu huấn luyện đều hợp lệ. Theo S2, phần dữ liệu không công bố được giữ là rủi ro dư để Owner xem xét khi duyệt; không còn bị trình bày là đã kiểm tra đủ chuỗi theo S1.

Với ba giới hạn trên được giữ trong hồ sơ, **chấp nhận phân loại Qwen3 4B/8B ở nhóm B để trình Owner**, không chấp nhận diễn giải B là model đã được duyệt hoặc sẵn sàng chạy.

### 4. Tính nhất quán phân loại và hồi quy

- Các ứng viên khác giữ A/C; lần này không tự chuyển TTS sang B. VieNeu/Kokoro/Piper còn kiểm tra license/định danh/quyền giọng hoặc phát biểu chưa làm rõ; chỉ riêng việc thiếu đọc LICENSE đã đủ để chưa qua S2. Không suy kết luận vi phạm từ lời quảng bá “personal use”, dữ liệu không công bố hay việc cùng tác giả từng dùng license khác.
- Việc giữ Kokoro ở A không phải kết luận âm thanh tổng hợp từ TTS đóng chắc chắn trái điều khoản. Nó là điểm cần kiểm tra cụ thể trong hồ sơ chưa hoàn tất; reviewer không mở rộng kiểm chứng TTS trong RR này.
- Bốn trạng thái phương pháp, kế hoạch, danh sách và quyền thực thi vẫn tách biệt. Candidates mục 1/3/8, kế hoạch điều 2/10 và handoff đều giữ danh sách chưa duyệt, chưa quyền tải/cài/chạy.
- Kế hoạch điều 10 ghi quyết định S2; điều 1–9 vẫn được đánh dấu đề xuất chưa Owner xác nhận. Điều 9 chặn trước bước 1.1 nếu thiếu TTS Việt vẫn cần Owner quyết định riêng; chọn S2 không tự xác nhận cả gói kế hoạch bổ sung.
- Ngân sách 4 giờ vẫn cho toàn video, RAM chưa có số đo, chạy tuần tự và voice cloning tắt. Không có tuyên bố đã benchmark/đạt hiệu năng, quyền chi phí hoặc mở TikTok Direct Post phát sinh.
- DECISIONS chưa ghi S2 và CURRENT_STATUS còn trạng thái cũ vì đều chỉ đọc trong SG-002. Handoff/RR đã cảnh báo điều này. Owner cần cho phép đồng bộ trước khi dùng các file đó làm căn cứ duyệt danh sách hoặc giao thực thi. Reviewer không sửa thay và không coi đây là quyền cấp thêm cho Claude. TASKS vẫn là nguồn lượt theo workflow.

## Chưa thể xác minh

- Hash weights/blob thực tế, manifest dài, nguồn chuyển đổi GGUF, toàn bộ dependency của bản runtime sẽ cài, tiếng Việt/RAM/tốc độ/chất lượng và ngân sách 4 giờ. Không có benchmark hay model nào được tải trong lượt này.
- Danh tính tác giả từ SHA-256, nguyên bản cuộc trao đổi Owner chọn S2 ngoài phần chép trong hồ sơ, quyền dùng thương mại cuối cùng hoặc sự vắng mặt tuyệt đối của bằng chứng trái ngược.
- Chưa có TTS Việt đủ nhóm B; hướng xử lý R1, danh sách cuối cùng và mọi quyền thực thi vẫn phải trình Owner.

## Bàn giao

**NEXT ACTOR: Claude** phản hồi APPROVED trong allowlist, nêu rõ phân loại được reviewer chấp nhận với rủi ro dư vẫn đi cùng từng artifact; sau đó chuyển **Owner** quyết định hướng TTS Việt, duyệt danh sách và quyền tải/cài/chạy riêng. Claude không tự đóng SG-002, chuyển bước, commit hoặc push.

Chỉ thêm đúng một báo cáo RR-005 lên đầu file này; giữ nguyên toàn bộ 21.512 byte lịch sử RR-004/RR-003 phía cuối và không sửa PHASE-00-REVIEW.md hoặc bất kỳ tài liệu Claude nào.

---

# Review RR-004

- Scope Grant: **SG-002**, Amendment **A01** | Vòng: **1/3**.
- Baseline Git: `e83ecec6493919a335de96b3183a508ecb7b4fbd`, nhánh `main`.
- Ngày: **2026-10-31**.
- Kết luận workflow: **APPROVED**. Kết quả theo yêu cầu Owner: **PASS cho hồ sơ nghiên cứu trong phạm vi re-review**.
- RR có hiệu lực là **RR-004** OPEN, tiếp nối RR-003 ANSWERED vòng 0/3. Cách gọi “RR-003 vòng 1/3” trong lời giao được hiểu là lượt tiếp nối; không sửa mã/hồ sơ RR.
- **NEXT ACTOR: Claude**, ghi nhận/phản hồi kết quả trong allowlist rồi trình Owner. Sau phản hồi, **Owner** quyết định tiêu chuẩn bằng chứng, hướng TTS, duyệt hồ sơ/danh sách và cấp quyền riêng nếu muốn bước sau.

## Kết luận finding

| Finding | Kết luận Codex | Bằng chứng bản sửa |
|---|---|---|
| **P1-001 – Qwen3 nhóm B không khớp tiêu chuẩn bằng chứng** | **CLOSED** | Candidates mục 3 và 4.1/4.2 chuyển cả Qwen3 4B/8B về A, nhóm B trống. Mục 7.1 tách S1/S2 và giữ quyết định cho Owner; kế hoạch điều 10 không cho tự chuyển B khi chưa có quyết định. Không còn khẳng định ứng viên đã qua chính tiêu chuẩn đang đề xuất |
| **P1-002 – Trạng thái bàn giao/cổng kế hoạch mâu thuẫn** | **CLOSED trong phạm vi file được sửa** | Candidates dòng 5–6, mục 8 và HANDOFF dòng 11, 29–33, mục 10 đã ghi RR-004, SG-002 ACTIVE, kế hoạch đã xác nhận và các việc chờ riêng biệt. BLOCKED cũ trong REVIEW_RESPONSE được gắn rõ là lịch sử trước A01 |

Không phát hiện finding mới cần sửa để thông qua hồ sơ nghiên cứu của vòng này. **Không phải PASS về license thương mại cuối cùng, shortlist benchmark hoặc quyền thực thi.**

## Đã tự xác minh

### Tính hợp lệ và bảo toàn phiên bản

- Đọc lại workflow, SG-002/A01, RR-004, phản hồi của Claude, candidates, kế hoạch và các phần handoff liên quan. SG-002 ACTIVE, vòng **0/3 → 1/3**, không đặt lại bộ đếm; chỉ RR-004 OPEN và có end marker.
- HEAD đúng baseline; **9/9 hash nhóm A khớp**, TASKS dùng prefix trước Review Requests. Mọi đường dẫn thay đổi thuộc chín file A hoặc PHASE-01-REVIEW.md nhóm B; không có nhóm C.
- Reviewer artifact trước lượt này đúng **12.893 byte**, SHA-256 `048d5475d53fe07e5f9993d46f62e9ae29f9157bee78d92edc75f26a54770bd6`; chưa có báo cáo RR-004.
- Bốn hash chỉ đọc CHANGELOG, CURRENT_STATUS, DECISIONS, IMPLEMENTATION_PLAN không đổi so với RR-003; việc khai báo snapshot không bị biến thành quyền sửa. Claude không tự đóng P1-001/P1-002 trong phản hồi; trạng thái trước lượt này vẫn pending Codex verification.

### P1-001 và tiêu chuẩn S1/S2

- `phase1-candidates.md:23`, `:38–39`, `:46`, `:68` đều xác nhận nhóm B trống, Qwen3 là nhóm A. Điều này đủ khắc phục mâu thuẫn phân loại ở RR-003, dù rủi ro nguồn dữ liệu chưa được giải quyết.
- Mục 7.1 trình S1 giữ tiêu chuẩn đầy đủ và S2 chấp nhận rủi ro dư bằng văn bản; S2 được ghi rõ **đề xuất, chưa áp dụng**. Dòng 244 yêu cầu Owner chọn và Codex re-review sau đổi phân loại; không quyết định thì B tiếp tục trống. Không có đường tự nới tiêu chuẩn để tải/chạy.
- Hệ quả “Qwen3 đủ nhóm B nếu S2” được hiểu là đánh giá có điều kiện của Claude, chưa phải kết luận reviewer về chuỗi quyền. Các giới hạn định danh/blob license và quyền phụ thuộc vẫn phải đi cùng hồ sơ khi Owner quyết định; không được xóa chúng bằng phê duyệt chung.
- License Apache-2.0 của Qwen3 và MIT của Ollama đã được đối chiếu độc lập ở RR-003. Lượt này không tìm thấy bằng chứng mới phủ định chúng, và không kết luận thiếu công bố dữ liệu nghĩa là cấm thương mại.
- Bản sửa đã phân biệt đúng: commit HEAD của kho Hugging Face không tự chứng minh commit nguồn của bản GGUF Ollama; model-layer digest không phải manifest digest; đọc hash từ registry không phải tự tính hash từ weights. Không buộc tải weights để hoàn tất review nghiên cứu.
- Kiểm tra nguồn public metadata trong lượt này: [Hugging Face API Qwen3-8B](https://huggingface.co/api/models/Qwen/Qwen3-8B) trả commit `b968826d9c46dd6066d109eabc6255188de91218` và ngày sửa 2025-07-26, phù hợp hồ sơ. Hai URL manifest registry Ollama và API Qwen3-4B không truy cập được qua công cụ web trong lượt này; **không xác nhận độc lập các digest layer/commit 4B mới thêm**. Chúng vẫn là thông tin Claude báo cáo, chưa phải artifact đã được reviewer chứng nhận. Vì Qwen3 đang A, giới hạn này không làm nó được phép benchmark hoặc mở lại mâu thuẫn P1-001.

### P1-002 và hồi quy trạng thái/quyền

- Candidates/handoff hiện hành thống nhất việc đang chờ: re-review, Owner chọn tiêu chuẩn, hướng TTS Việt, duyệt danh sách, quyền tải/cài/chạy. Kế hoạch đã xác nhận không còn được ghi là điều kiện chưa hoàn tất trong dòng cổng handoff.
- HANDOFF cuối file không còn vừa ACTIVE vừa “BLOCKED vì chưa có SG”; head Git và dirty working tree cũng được mô tả đúng.
- `CURRENT_STATUS.md:25` vẫn ghi Qwen3 ở B. Đây là sai lệch được khai báo rõ trong RR/handoff và file đó ngoài quyền sửa của SG-002. **Owner nên cấp quyền đồng bộ CURRENT_STATUS trước khi dùng nó để duyệt danh sách hoặc giao tải/chạy.** Không coi dòng này là bằng chứng đã qua nhóm B, không sửa file và không đòi Claude vượt allowlist. Đây là việc bàn giao Owner đã được nêu, không phải finding mới do bản sửa gây ra.
- Handoff còn dòng kết luận Codex “mới nhất” trỏ final Phase 0, nhưng có các dòng RR-003/RR-004 cụ thể ngay dưới và TASKS là nguồn lượt. Đọc trạng thái theo mã RR hiện hành, không dùng dòng lịch sử Phase 0 để suy PASS Phase 1.
- Kế hoạch điều 1–10 vẫn được ghi là **đề xuất chưa Owner xác nhận**. Điều 9 thắt cổng TTS tới trước 1.1, cần quyết định Owner riêng như đã ghi. Điều 10 giữ B trống trước quyết định tiêu chuẩn. Không có điều nào cấp quyền tải/cài/chạy; chọn S2 về sau phải được ghi rõ là quyết định chấp nhận rủi ro, không thể mô tả đơn thuần là giữ nguyên tiêu chuẩn S1.
- RAM vẫn chưa có số đo; dung lượng tải không bị coi là RAM chạy. Giữ tuần tự, một tác vụ nặng, giải phóng model và ngân sách **4 giờ cho toàn video**. Voice cloning mặc định tắt. Không có quyền commit/push, liên hệ tác giả, chi phí, đổi scope hay mở TikTok Direct Post được thêm.

## Chưa thể xác minh

- Tính toàn vẹn của weights, nguồn chuyển đổi GGUF, đầy đủ license mọi dependency/giọng, tốc độ, RAM, tiếng Việt, chất lượng hoặc mục tiêu 4 giờ: chưa tải và chưa benchmark; không có kết quả runtime nào được công nhận.
- Nguồn gốc phê duyệt chép trong SG/A01 không thể chứng minh bằng SHA-256; yêu cầu trực tiếp hiện tại cho phép review, không cấp quyền khác.
- Việc Owner chọn S1/S2, hướng TTS Việt và duyệt ứng viên chưa diễn ra trong snapshot. Kết luận APPROVED này chỉ xác nhận hồ sơ đã giải quyết hai finding, không thay Owner quyết định.

## Bàn giao

**NEXT ACTOR: Claude** phản hồi APPROVED, ghi nhận P1-001/P1-002 CLOSED theo báo cáo này trong file được cấp quyền, rồi tóm tắt cho Owner các quyết định còn chờ, gồm sai lệch CURRENT_STATUS ngoài SG. Không tự đóng SG hoặc đổi trạng thái ứng viên sang B. Sau phản hồi, lượt thuộc **Owner** theo mục 5/11 workflow.

Chỉ thêm báo cáo RR-004 này lên đầu PHASE-01-REVIEW.md. Toàn bộ 12.893 byte báo cáo RR-003 giữ nguyên phía cuối; PHASE-00-REVIEW.md và mọi tài liệu Claude không sửa. Không tải model, benchmark, commit hoặc push.

---

# Review RR-003

- Scope Grant: **SG-002**, Amendment **A01** | Vòng: **0/3**.
- Baseline Git: `e83ecec6493919a335de96b3183a508ecb7b4fbd`, nhánh `main`.
- Ngày review: **2026-10-31**.
- Kết luận workflow: **CHANGES REQUESTED**. Kết luận theo yêu cầu Owner: **NEEDS REVISION**.
- **NEXT ACTOR: Claude**, sửa và phản hồi trong allowlist SG-002, đăng RR mới vòng 1/3. Những quyết định về tiêu chuẩn chấp nhận rủi ro/quyền tải hoặc hướng TTS vẫn thuộc Owner, không được suy ra từ finding.
- Chỉ review hồ sơ nghiên cứu Phase 1.0; không tải model, cài đặt, benchmark, commit/push, liên hệ tác giả hoặc mở phase/bước tiếp theo.

## Kiểm tra đầu vào

**Hợp lệ.** RR-003 là RR OPEN duy nhất, tham chiếu SG-002 ACTIVE và Amendment A01, vòng 0/3 độc lập với SG-001 đã đóng. Có END-OF-REVIEW-REQUEST và chưa có báo cáo RR-003.

- HEAD đúng baseline; **9/9 hash nhóm A khớp**, gồm TASKS chỉ băm phần trước Review Requests. Working tree có đúng chín đường dẫn được khai báo; không có nhóm C.
- Bốn file CHANGELOG, CURRENT_STATUS, DECISIONS, IMPLEMENTATION_PLAN được A01 khai báo chỉ đọc. Việc đưa vào snapshot không tạo quyền sửa chúng.
- SG-002 cho Codex **tạo** PHASE-01-REVIEW.md; RR ghi rõ file chưa tồn tại. Đã xác minh file vắng mặt trước khi ghi, không coi file vắng mặt là tệp rỗng có hash giả. Đây là baseline tạo mới được SG và lời giao trực tiếp của Owner xác định, không bỏ qua một mismatch nào.
- PHASE-00-REVIEW.md vẫn có hash đầy đủ `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`, khớp prefix RR cung cấp; file này không được sửa trong lượt review.

## Phát hiện

### [MEDIUM] P1-001 – Qwen3 nhóm B chưa đáp ứng chính tiêu chuẩn bằng chứng mà hồ sơ đặt ra

- Vị trí: `docs/testing/phase1-candidates.md:26–28`, `:37`, `:53–58`, `:72–76`; `docs/operations/phase-reports/PHASE-01-PLAN.md:31–32`.
- Bằng chứng: hồ sơ xác nhận chưa đọc toàn văn LICENSE, Qwen3 chưa có revision gốc và chưa rõ dữ liệu huấn luyện, nhưng cả 4B/8B được gắn nhóm B đủ điều kiện đề xuất benchmark. Điều kiện bổ sung số 4 lại nói tóm tắt trang không đủ để chuyển nhóm B nếu dữ liệu/phụ thuộc chưa rõ; điều kiện số 3 đòi hồ sơ artifact và link license tương ứng. Phần bổ sung được ghi là chưa Owner duyệt, nên không được trình bày như tiêu chuẩn Owner đã áp dụng; dù vậy tài liệu phải nhất quán giữa tiêu chuẩn đang đề xuất và kết quả phân loại của nó.
- Tình huống gây lỗi: Owner nhìn nhóm B như kết quả đã vượt kiểm tra license, trong khi phần giới hạn bằng chứng và tiêu chuẩn chuyển nhóm phủ định điều đó. TTS bị giữ A vì nguồn dữ liệu chưa rõ, nhưng Qwen3 có cùng loại bất định lại qua B mà không có tiêu chí phân biệt.
- Đã kiểm chứng độc lập: tệp LICENSE hiện hành của [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B/raw/main/LICENSE) và [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B/raw/main/LICENSE) là Apache-2.0; [Ollama LICENSE](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE) là MIT. Do đó **không kết luận Qwen3 cấm thương mại**. Vấn đề là hồ sơ chưa ghi đủ quá trình xác minh theo chính tiêu chuẩn của nó, không phải đã tìm thấy điều khoản cấm.
- Yêu cầu khắc phục: đọc và ghi nguồn LICENSE đúng artifact/runtime dự kiến, gắn revision/digest hoặc nêu chính xác phần chưa định danh. Sau đó hoặc chuyển Qwen3 về A cho tới khi đủ tiêu chuẩn đã nêu, hoặc trình một tiêu chuẩn bằng chứng/rủi ro nhất quán để Owner quyết định. Không tự nới tiêu chuẩn và không dùng việc reviewer đọc LICENSE thay cho cập nhật hồ sơ Claude.
- Trong phạm vi SG: **có** với sửa hồ sơ/kế hoạch đề xuất; **không** với tự duyệt tiêu chuẩn rủi ro, cấp quyền tải/chạy hay sửa DECISIONS ngoài quyền.

### [LOW] P1-002 – Trạng thái bàn giao và cổng kế hoạch còn mâu thuẫn

- Vị trí: `docs/testing/phase1-candidates.md:5`; `HANDOFF_TO_CHATGPT.md:11`, `:178`.
- Bằng chứng: candidates vẫn ghi bàn giao BLOCKED; cuối handoff vừa nói SG-002 ACTIVE/RR-003 chờ Codex vừa nói chưa có Scope Grant nên BLOCKED. Handoff dòng 11 còn ghi kế hoạch chi tiết là điều kiện còn lại, trong khi dòng 10, TASKS và PHASE-01-PLAN đều ghi kế hoạch đã xác nhận.
- Tình huống gây lỗi: người tiếp nhận tưởng phải cấp SG hoặc xác nhận kế hoạch lại, hoặc không biết đang chờ review, duyệt danh sách hay quyết định hướng TTS. TASKS hiện vẫn đủ rõ để reviewer xác định lượt, nên đây không phải lỗi đầu vào làm dừng review.
- Yêu cầu khắc phục: đồng bộ trạng thái hiện hành trong candidates/handoff; nếu giữ mô tả BLOCKED cũ thì gắn rõ là lịch sử trước A01. Giữ riêng các việc còn chờ: re-review, Owner duyệt danh sách/hướng TTS, và quyền cài/tải/chạy từng bước.
- Trong phạm vi SG: **có**, cả hai file đều thuộc allowlist ghi của Claude.

## Đối chiếu pre-approval NEEDS REVISION

| Nội dung trước đây | Kết quả hiện tại |
|---|---|
| Tách nghiên cứu / đủ điều kiện đề xuất benchmark / loại | Đã có A/B/C; quyền tải độc lập được nêu rõ. Chưa đóng hoàn toàn vì P1-001 |
| Định danh model và nguồn | Cải thiện rõ: tag Q4_K_M, digest ngắn, đường dẫn artifact, một số revision, voice ID và nguồn. Các ứng viên A vẫn chưa phải đề nghị tải; không ép chúng trở thành danh sách đã duyệt |
| Piper vais1000 và chuỗi lessac | Đã tìm và ghi nhận chuỗi nguồn; loại bảo thủ khỏi vòng thương mại hiện tại có căn cứ rủi ro |
| VieNeu phân biệt biến thể | Đã tách 0.3B/0.5B với v3 Turbo, codec và giọng; không suy license của một biến thể sang biến thể khác |
| Piper tiếng Anh / Kokoro | Đã chỉ định ljspeech và các voice Kokoro; đều nhóm A và giữ điểm chưa rõ, không tuyên bố benchmark được phép |
| RAM và ngân sách | PASS ở mức hồ sơ: dung lượng tải tách RAM, không khẳng định vừa RAM/đạt tốc độ; 4 giờ cho toàn video; chạy tuần tự và giải phóng model |
| Quyền hạn | PASS: bốn trạng thái độc lập; danh sách chưa Owner duyệt, không tải/cài/chạy, không liên hệ/chi phí hoặc thay đổi phạm vi tự động |
| Đồng bộ handoff | Chưa đóng: P1-002 |

## Đã tự xác minh nguồn và giới hạn diễn giải

Đọc nguồn chính thức ngày **2026-10-31**, không tải weights hoặc dataset:

- [Ollama Qwen3 tags](https://registry.ollama.com/library/qwen3/tags): các digest ngắn `2bfd38a7daaf` và `500a1f067a9f`, Q4_K_M, dung lượng 2,6/5,2 GB phù hợp hồ sơ. Tag trơn 4B hiện khác bản Q4_K_M gốc như hồ sơ cảnh báo. Đây là metadata nguồn hiện hành, chưa phải hash tệp đã tải; không suy RAM từ chúng.
- [Piper vais1000 model card](https://huggingface.co/rhasspy/piper-voices/blob/main/vi/vi_VN/vais1000/medium/MODEL_CARD) ghi fine-tune từ lessac; [lessac model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/lessac/medium/MODEL_CARD) dẫn Blizzard 2013; [license Blizzard](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html) giới hạn Research Purposes và loại trừ các mục đích thương mại được mô tả trong đó. Chuỗi này đủ để không cho qua kiểm tra quyền của dự án hiện tại. Không coi đó là phán quyết pháp lý rằng mọi trọng số/đầu ra phái sinh đều tự động chịu cùng license; việc xếp C là quyết định sàng lọc thận trọng khi chưa chứng minh quyền phù hợp.
- [Piper ljspeech model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/ljspeech/medium/MODEL_CARD) ghi public domain cho dữ liệu, một speaker và trained from scratch; giữ A cho các kiểm tra engine/phụ thuộc còn lại không tạo quyền chạy.
- [VieNeu-TTS-1000h dataset card](https://huggingface.co/datasets/pnnbao-ump/VieNeu-TTS-1000h) ghi CC BY-NC 4.0, nghiên cứu/giáo dục và giới hạn truy cập. Có căn cứ giữ các biến thể liên quan ngoài shortlist thương mại khi chưa giải quyết mâu thuẫn. Trang PyPI vieneu 1.0.6 không truy cập được trong lượt này; **không xác nhận độc lập** câu trích PyPI hay suy chắc quyền downstream từ dataset license.
- [VieNeu v3 Turbo model card](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) có FAQ cấp quyền thương mại cho model/preset, xác nhận từ nhà phát hành về quyền/consent và nói dữ liệu nội bộ không công bố. Vì vậy phải ghi nhận đây là bằng chứng tuyên bố từ nhà phát hành, không phải hoàn toàn không có bằng chứng quyền. Giữ A theo mức rủi ro thận trọng của dự án có thể hợp lý; không tự kết luận vi phạm vì thiếu dataset công khai hoặc vì license biến thể cũ. Chưa xác minh tài liệu riêng cho từng người nói/phụ thuộc.
- Những câu tổng quát kiểu "một mắt xích phi thương mại làm hỏng cả chuỗi" cần được hiểu là quy tắc fail-closed của dự án, không phải kết luận pháp lý phổ quát. Chỉ bổ sung bằng chứng hoặc Owner quyết định mức chấp nhận mới có thể thay đổi cách sàng lọc; reviewer không cấp quyền thương mại.

## Kế hoạch bổ sung và quyền hạn

Chín điều kiện bổ sung PHASE-01-PLAN mục 25–37 được đánh dấu **đề xuất, chưa được Owner xác nhận**. Không điều kiện nào cấp quyền tải/cài/chạy. Yêu cầu số 9 dừng trước bước 1.1 khi không có TTS Việt đủ điều kiện là **cổng chặt hơn kế hoạch cũ**, vốn yêu cầu báo Owner trước Phase 4–5; cần Owner quyết định rõ khi trình kế hoạch, không coi là phê duyệt đã có. P1-001 phải được giải quyết để nhóm B nhất quán với điều kiện số 4.

Chưa có TTS Việt nhóm B không chứng minh toàn bộ hướng TTS Việt bất khả thi. Đây là khoảng trống bằng chứng của shortlist hiện tại, cần Owner chọn hướng nghiên cứu, không tự đổi scope, dùng dịch vụ trả phí hay liên hệ tác giả.

## Chưa thể xác minh

- Không có benchmark, RAM runtime, tốc độ, chất lượng giọng hoặc kết quả 4 giờ/video; không chạy test mô phỏng thay cho ứng viên thật.
- Chưa kiểm tra đầy đủ toàn bộ license/phụ thuộc, mọi revision và mọi model card của các ứng viên A/C. Không có kết luận đủ quyền thương mại cho tất cả model trong danh sách.
- Không có bản pre-approval lưu thành file trong repo; đối chiếu yêu cầu gốc từ chính lịch sử chat hiện có và bảng yêu cầu RR-003, không tạo mã finding cũ giả định.
- SHA-256 chỉ chứng minh snapshot khớp, không chứng minh tác giả. Không tự xác nhận lại push/remote hoặc phê duyệt Owner chỉ từ lời tự báo cáo của Claude.

## Ghi báo cáo lần đầu và bàn giao

Đối với file review mới: baseline là **ABSENT**, không phải SHA-256 của zero bytes. Sau lượt này Claude kiểm tra file mới có đúng một báo cáo RR-003, không có lịch sử nào cần tail; RR tiếp theo phải ghi đầy đủ byte count/hash của file đã tồn tại. Không dùng `tail -c 0` làm bằng chứng lịch sử, không dùng prefix hash của PHASE-00 thay cho hash PHASE-01. Khuyến nghị chuẩn hóa trường hợp ABSENT trong workflow ở một phạm vi được Owner cấp sau; lượt này không sửa workflow.

**NEXT ACTOR: Claude** cho P1-001/P1-002 trong allowlist. Chỉ Owner duyệt danh sách, điều kiện bổ sung và mọi quyền triển khai sau đó. SG-002 vẫn do Owner quản lý; Codex không sửa TASKS/SG/RR hay tài liệu Claude. Chỉ tạo file reviewer artifact Phase 1 này; giữ nguyên PHASE-00-REVIEW.md.
