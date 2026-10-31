# Phase 1 – Bước 1.0: danh sách ứng viên và license (bản sửa 3, SG-002)

| Hạng mục | Giá trị |
|---|---|
| Trạng thái tài liệu | **Dự thảo, chưa được Project Owner duyệt.** Codex review RR-003 (vòng 0/3) `CHANGES REQUESTED`; sau bản sửa, Codex review RR-004 (vòng 1/3) kết luận **`APPROVED`** và đóng P1-001, P1-002. Đây là PASS cho hồ sơ nghiên cứu, **không** phải PASS về license thương mại cuối cùng, danh sách benchmark hay quyền thực thi. Tình trạng BLOCKED trước Amendment A01 chỉ là lịch sử và đã hết. **Owner chọn S2 ngày 2026-10-31**; Codex review RR-005 (vòng 2/3) kết luận **`APPROVED`** cho phân loại theo S2 (Qwen3 4B, 8B ở nhóm B), với điều kiện rủi ro dư đi cùng từng artifact. Vẫn **không** phải PASS về license thương mại cuối cùng, duyệt danh sách hay quyền thực thi |
| Việc đang chờ | (1) Owner chọn hướng TTS tiếng Việt tiếp theo (mục 7; đã chọn 2A: nghiên cứu tài liệu); (2) ~~Owner duyệt danh sách~~ đã duyệt riêng **Qwen3 4B** (1B), 8B chưa; (3) quyền tải, cài, chạy từng bước. Ba việc này **độc lập với nhau** và độc lập với việc chọn S2. Lượt thuộc về Owner |
| Ngày xác minh | 2026-10-31 |
| Ràng buộc | Q-03: video có kiếm tiền, license phải cho phép thương mại. D-017: không dùng công cụ không chính thức. Q-06: tối đa 4 giờ cho **toàn bộ** một video |
| Máy | MacBook Air M4, 16 GB RAM, SSD 512 GB; local-first, tuần tự |
| Nguồn yêu cầu sửa | Danh sách yêu cầu do Project Owner chuyển trong chat. **Báo cáo pre-approval của Codex không có trong repo** (file review duy nhất vẫn là `PHASE-00-REVIEW.md`), nên tôi chưa đối chiếu được từng finding gốc |

## 1. Bốn trạng thái độc lập

Bốn trạng thái dưới đây **không tương đương nhau**:

| Trạng thái | Giá trị hiện tại |
|---|---|
| Phương pháp benchmark | Đã duyệt (D-013, 2026-10-31); chỉ duyệt phương pháp |
| Kế hoạch Phase 1 | Đã xác nhận (2026-10-31) |
| Danh sách model | **Duyệt một phần (mã 1B, Owner, 2026-10-31): chỉ Qwen3 4B `q4_K_M`**, kèm rủi ro dư ở mục 4.1 (dữ liệu huấn luyện không công bố; commit nguồn GGUF chưa định danh; tiếng Việt và RAM chưa đo). **Qwen3 8B: chưa có câu duyệt vào danh sách** (Owner chỉ cho phép tải ở A06 và đo thô ở A07). Chưa có TTS nào trong danh sách |
| Quyền tải, cài, chạy | **CHƯA cấp.** Mỗi lệnh cần xác nhận riêng |

**Nhóm B không phải lệnh triển khai.** Nhóm B chỉ nghĩa là đủ bằng chứng để đề xuất Owner cho phép benchmark. **Theo S2, nhóm B hiện gồm Qwen3 4B và 8B** (mục 3); Codex đã `APPROVED` phân loại này (RR-005); danh sách model đã được Owner duyệt **một phần**: chỉ Qwen3 4B `q4_K_M` (mã 1B). Qwen3 8B: Owner cho phép tải (A06) và đo thô (A07) nhưng **chưa có câu duyệt 8B vào danh sách**. Duyệt danh sách, quyền tải và quyền chạy là ba việc riêng.

## 2. Giới hạn của bằng chứng

- Thông tin lấy từ trang công khai (Hugging Face, GitHub, PyPI, Ollama, trang dataset) qua công cụ tóm tắt web. **Toàn văn LICENSE mới được đọc cho Qwen3 4B, Qwen3 8B và runtime Ollama (2026-10-31, mục 4.1, 4.2); các ứng viên khác chưa.** Công cụ trả về bản tóm tắt chứ không phải tệp nguyên văn, nên đây vẫn không phải ý kiến pháp lý.
- Nhóm B yêu cầu bằng chứng cho **từng artifact cụ thể**. Một license ghi ở metadata của kho không đủ nếu dữ liệu huấn luyện hay phụ thuộc có license khác. **Cách hiểu "chưa rõ" của dự án nằm ở mục 7.1: Owner đã chọn S2 (2026-10-31)**, nghĩa là dữ liệu huấn luyện không công bố là rủi ro dư do Owner chấp nhận, chỉ khi đủ ba điều kiện (i), (ii), (iii); Claude không áp dụng cách hiểu nào nới hơn S2.
- **Chuỗi quyền** gồm: dữ liệu huấn luyện, mô hình gốc nếu có tinh chỉnh, trọng số, giọng, mã chạy và phụ thuộc. Một mắt xích phi thương mại làm hỏng cả chuỗi.
- Chưa có số đo hiệu năng nào. Không có dòng nào dưới đây khẳng định đã đạt yêu cầu 4 giờ.
- **Nhân bản giọng mặc định tắt** cho mọi ứng viên TTS, kể cả khi mô hình hỗ trợ. Không dùng audio tham chiếu của người thật khi chưa có bằng chứng đồng ý ghi nhận (`security-and-rights.md` mục 7).
- SG-002 chỉ cấp quyền nghiên cứu và sửa tài liệu. Không có quyền tải, cài, chạy hay liên hệ bên ngoài.

## 3. Phân loại tóm tắt

| Nhóm | Ứng viên |
|---|---|
| **B – đủ điều kiện đề xuất benchmark** (theo S2 mà Owner chọn 2026-10-31; **Codex APPROVED phân loại tại RR-005; không phải quyền tải**) | **Qwen3 4B `q4_K_M`** (Owner duyệt vào danh sách, 1B); **Qwen3 8B `q4_K_M`** (chưa duyệt) |
| **A – chỉ nghiên cứu** | Piper `en_US-ljspeech-medium`; VieNeu-TTS v3 Turbo; Kokoro v1.0; Piper `vi_VN-25hours_single` và các giọng `en_US` chưa đọc model card; resvg; CairoSVG; faster-whisper; Gemma 3 4B |
| **C – loại vòng này** | Piper `vi_VN-vais1000-medium`; Piper `vi_VN-vivos`; VieNeu-TTS 0.3B và 0.5B; F5-TTS; Piper `en_US-lessac`, `hfc_female`, `hfc_male`, `libritts_r`; Gemma 3 12B |

> **Phát hiện quan trọng: hiện không có ứng viên TTS tiếng Việt nào đủ điều kiện nhóm B.** Rủi ro R1 đang thành hiện thực. Xem mục 7.

## 4. Hồ sơ từng ứng viên

### 4.1 Qwen3 4B – nhóm B theo S2 (Codex APPROVED phân loại; **Owner duyệt vào danh sách, mã 1B, 2026-10-31**; không phải quyền tải)

| Trường | Giá trị |
|---|---|
| Tên | Qwen3 4B, đóng gói qua Ollama |
| Vai trò | LLM |
| Repository chính thức | https://github.com/QwenLM/Qwen3 |
| Artifact | https://ollama.com/library/qwen3:4b-q4_K_M (gốc: https://huggingface.co/Qwen/Qwen3-4B) |
| Định danh artifact Ollama | Tag `4b-q4_K_M`, digest ngắn `2bfd38a7daaf`. Manifest ([registry.ollama.ai](https://registry.ollama.ai/v2/library/qwen3/manifests/4b-q4_K_M)): config `sha256:5efd52d6d9f24db4a33df0d706ee6037edf026027281bb9568bb066ebc5a4f31`; **model layer `sha256:163553aea1b1de62de7c5eb2ef5afb756b4b3133308d9ae7e42e951d8d696ef5`, 2,620,774,592 byte**; license layer `sha256:d18a5cc71b84bc4af394a31116bd3932b42241de70c77d2b76d69a314ec8aa12`, 11,338 byte. Giá trị đọc qua công cụ tóm tắt, **chưa tự tính lại từ tệp tải về** |
| Revision gốc (Hugging Face) | Đầu kho `Qwen/Qwen3-4B` hiện là commit `1cfa9a7208912126459214e8b04321603b3df60c`, `lastModified` 2025-07-26 ([API](https://huggingface.co/api/models/Qwen/Qwen3-4B)); `base_model` là `Qwen/Qwen3-4B-Base`. **Phần chưa định danh:** commit nào của kho này mà bản GGUF trên Ollama được chuyển đổi từ đó. Trang Ollama ghi bản `4b-q4_K_M` cập nhật "1 year ago", có thể trước commit hiện tại |
| Quantization | `Q4_K_M`, 4.02B tham số, kiến trúc `qwen3` |
| Voice ID | Không áp dụng |
| License mã và trọng số | Apache-2.0. **Đã đọc LICENSE:** [Qwen3-4B/LICENSE](https://huggingface.co/Qwen/Qwen3-4B/raw/main/LICENSE) là "Apache License, Version 2.0, January 2004" (dòng "Copyright 2024 Alibaba Cloud" chỉ nằm trong phần phụ lục mẫu). Blob license đi kèm artifact Ollama (11,338 byte) hiển thị là Apache License 2.0 trên trang Ollama; **chưa so từng byte với LICENSE Hugging Face** |
| License runtime | Ollama: "MIT License, Copyright (c) Ollama" ([LICENSE](https://raw.githubusercontent.com/ollama/ollama/main/LICENSE)) |
| Dữ liệu huấn luyện | **Không được công bố** trên các trang đã đọc. Đây là điểm duy nhất chưa rõ trong chuỗi. Owner đã chọn S2 (mục 7.1): coi đây là rủi ro dư do Owner chấp nhận, **chỉ cho artifact này, chỉ cho tiêu chuẩn phân loại**, không phải kết luận pháp lý |
| Thương mại | Apache-2.0 cho phép, kèm điều kiện giữ thông báo license. Không tìm thấy điều khoản cấm thương mại; **hồ sơ không kết luận Qwen3 cấm thương mại** |
| Dung lượng tải | 2.6 GB (Ollama; độ tin cậy cao cho dung lượng tải) |
| **Đã tải (2026-10-31, Amendment A03)** | `ollama pull qwen3:4b-q4_K_M` bằng Ollama 0.40.13. Digest manifest `2bfd38a7daaf4b1037efe517ccb73d1a3bbd4822cf89f1a82be1569050a114e0`; config, model layer, license layer **khớp** các giá trị ở trên; **SHA-256 blob model đã tự tính lại từ tệp tải về và khớp** `163553aea1b1…`. Blob license (11,338 byte) vẫn chưa so từng byte với LICENSE Hugging Face. Mới tải, **chưa chạy** |
| RAM runtime | **Chưa có nguồn.** Không suy ra từ dung lượng tải; benchmark phải đo, gồm cả bộ nhớ cho ngữ cảnh |
| **Lưu ý tag** | Tag trơn `qwen3:4b` có digest `359d7dd4bcda`, trùng `4b-thinking-2507-q4_K_M`, **không phải** `4b-q4_K_M`. Chỉ dùng tag tường minh |
| Chưa xác minh | Tiếng Việt: trang chỉ nói "100+ ngôn ngữ", không nêu tên tiếng Việt. Liên kết giữa commit Hugging Face và blob Ollama. Ngữ cảnh 40K theo Ollama; chưa đo |
| Ngày xác minh | 2026-10-31 |

### 4.2 Qwen3 8B – nhóm B theo S2 (Codex APPROVED phân loại; **chưa có câu duyệt vào danh sách**; Owner cho phép tải (A06) và đo thô (A07); không phải quyền chạy thêm)

| Trường | Giá trị |
|---|---|
| Tên, vai trò | Qwen3 8B, LLM |
| Repository, artifact | https://github.com/QwenLM/Qwen3; https://ollama.com/library/qwen3:8b-q4_K_M (gốc: https://huggingface.co/Qwen/Qwen3-8B) |
| Định danh artifact Ollama | Tag `8b-q4_K_M`, digest ngắn `500a1f067a9f` (trùng tag trơn `qwen3:8b`, nhưng chỉ dùng tag tường minh). Manifest ([registry.ollama.ai](https://registry.ollama.ai/v2/library/qwen3/manifests/8b-q4_K_M)): config `sha256:05a61d37b08453e59290add468e3bb2f688e23a01e967fecb0e2fa41218cea76`; **model layer `sha256:a3de86cd1c132c822487ededd47a324c50491393e6565cd14bafa40d0b8e686f`, 5,225,374,496 byte**; license layer `sha256:d18a5cc71b84bc4af394a31116bd3932b42241de70c77d2b76d69a314ec8aa12`, 11,338 byte (cùng blob với 4B). Đọc qua công cụ tóm tắt, **chưa tự tính lại** |
| Revision gốc (Hugging Face) | Đầu kho `Qwen/Qwen3-8B` hiện là commit `b968826d9c46dd6066d109eabc6255188de91218`, `lastModified` 2025-07-26 ([API](https://huggingface.co/api/models/Qwen/Qwen3-8B)). **Phần chưa định danh:** commit mà bản GGUF Ollama được chuyển đổi từ đó |
| Quantization | `Q4_K_M`, 8.19B tham số |
| License | Apache-2.0. **Đã đọc LICENSE:** [Qwen3-8B/LICENSE](https://huggingface.co/Qwen/Qwen3-8B/raw/main/LICENSE) là Apache License 2.0 (phụ lục mẫu ghi "Copyright 2024 Alibaba Cloud"). Runtime Ollama: MIT |
| Dữ liệu huấn luyện | Không được công bố trên các trang đã đọc. Rủi ro dư do Owner chấp nhận theo S2 (mục 7.1), chỉ cho artifact này và chỉ cho phân loại |
| Thương mại | Apache-2.0 cho phép, kèm điều kiện giữ thông báo license; không kết luận Qwen3 cấm thương mại |
| Dung lượng tải | 5.2 GB (Ollama) |
| **Đã tải (2026-10-31, Amendment A06)** | `ollama pull qwen3:8b-q4_K_M`, Ollama 0.40.13. Digest manifest `500a1f067a9f…`, config, model layer 5,225,374,496 byte và license layer **khớp**; SHA-256 blob model tự tính lại và khớp `a3de86cd1c13…`. Owner cho phép **tải**; **chưa chạy, chưa đo**. Rủi ro RAM bên dưới vẫn còn nguyên |
| RAM runtime | **Chưa có nguồn.** Rủi ro cao với 16 GB RAM chia sẻ với hệ điều hành và các bước khác; chỉ đo một mình, tuần tự |
| Chưa xác minh | Tiếng Việt như 4B; liên kết giữa commit Hugging Face và blob Ollama |
| Ngày xác minh | 2026-10-31 |

### 4.3 Piper `vi_VN-vais1000-medium` – nhóm C

| Trường | Giá trị |
|---|---|
| Tên, vai trò | Piper voice `vi_VN-vais1000-medium`, TTS tiếng Việt |
| Repository | https://huggingface.co/rhasspy/piper-voices (commit thư mục `217ddc79818708b078d0d14a8fae9608b9d77141`) |
| Artifact | `vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx` (63.2 MB), 22,050 Hz, 1 speaker |
| Voice ID | `vi_VN-vais1000-medium` |
| Chuỗi quyền | Model card: "Finetuned from U.S. English lessac voice (medium quality)." Bộ **lessac** huấn luyện từ dữ liệu Blizzard 2013, **license chỉ cho mục đích nghiên cứu, loại trừ rõ việc dùng thương mại và phát triển, thương mại hóa tổng hợp giọng** ([license](https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html)) |
| Dữ liệu tiếng Việt | VAIS-1000: model card ghi CC BY 4.0, nhưng **trang IEEE DataPort không nêu license** và yêu cầu thuê bao ([trang dataset](https://ieee-dataport.org/documents/vais-1000-vietnamese-speech-synthesis-corpus)) |
| Phụ thuộc | Engine Piper (xem 4.6) |
| Thương mại | **Không đủ điều kiện:** giọng tinh chỉnh từ checkpoint huấn luyện bằng dữ liệu nghiên cứu-only |
| Lý do loại | Một mắt xích (lessac/Blizzard 2013) loại trừ thương mại. Cần luật sư mới có thể kết luận ngược lại, vượt phạm vi tài liệu này |
| Ngày xác minh | 2026-10-31 |

### 4.4 Piper `en_US-ljspeech-medium` – nhóm A

| Trường | Giá trị |
|---|---|
| Tên, vai trò | Piper voice `en_US-ljspeech-medium`, TTS tiếng Anh |
| Repository, artifact | https://huggingface.co/rhasspy/piper-voices; `en/en_US/ljspeech/medium/en_US-ljspeech-medium.onnx` (63.5 MB); commit thư mục `217ddc79818708b078d0d14a8fae9608b9d77141`, các tệp sửa lần cuối ở commit `bae641dcb5a608cff81ccaf7ff018baaca1a33e1` |
| Voice ID | `en_US-ljspeech-medium`; 1 speaker, 22,050 Hz |
| Chuỗi quyền | Model card: "Trained from scratch"; dữ liệu LJ Speech, "License: public domain" ([keithito.com](https://keithito.com/LJ-Speech-Dataset/)). Kho giọng ghi MIT |
| Điểm tốt | Không có checkpoint gốc; dữ liệu public domain. **Chuỗi sạch nhất trong các giọng Piper đã kiểm tra** |
| Vì sao vẫn nhóm A | (1) Tài liệu `VOICES.md` của kho Piper hiện hành (GPL-3.0) ghi "Piper is intended for personal use and text to speech research only", **chưa giải quyết được** mâu thuẫn với GPL-3.0 hay ý nghĩa với dùng thương mại; (2) engine GPL-3.0 và phụ thuộc `espeak-ng` GPL-3.0 chưa đánh giá đầy đủ; (3) chỉ có **một** giọng nữ, không đủ cho hai hồ sơ nhân vật khác biệt |
| Dung lượng, RAM | 63.5 MB (Hugging Face); RAM: **chưa có nguồn** |
| Ngày xác minh | 2026-10-31 |

### 4.5 Các giọng Piper khác đã kiểm tra – nhóm C

| Giọng | Lý do loại | Nguồn |
|---|---|---|
| `vi_VN-vivos-x_low` | Dữ liệu InfoRe/VIVOS **CC BY-NC-SA 4.0** | [model card](https://huggingface.co/rhasspy/piper-voices/blob/main/vi/vi_VN/vivos/x_low/MODEL_CARD) |
| `en_US-lessac-medium` | Dữ liệu Blizzard 2013, nghiên cứu-only | Như 4.3 |
| `en_US-hfc_female-medium`, `hfc_male-medium` | Dữ liệu CC BY-NC-SA 4.0 và tinh chỉnh từ lessac | model card từng giọng |
| `en_US-libritts_r-medium` | Dữ liệu CC BY 4.0 nhưng "Fine-tuned from English lessac medium" | [model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts_r/medium/MODEL_CARD) |

`vi_VN-25hours_single` **chưa đọc model card**, nên là nhóm A, không phải C. Các giọng `en_US` còn lại (`amy`, `arctic`, `bryce`, `danny`, `joe`, `john`, `kathleen`, `kristin`, `kusal`, `l2arctic`, `libritts`, `mike`, `norman`, `reza_ibrahim`, `ryan`, `sam`) **chưa đọc model card**; coi là nhóm A cho tới khi đọc, đặc biệt phải kiểm tra chuỗi tinh chỉnh từ lessac.

### 4.6 Engine Piper

| Trường | Giá trị |
|---|---|
| Kho hiện hành | https://github.com/OHF-Voice/piper1-gpl, license **GPL-3.0** |
| Chưa xác minh | Quan hệ với `rhasspy/piper` cũ; câu "personal use and text to speech research only" trong `docs/VOICES.md`; license `espeak-ng` ([GPL-3.0 trở lên](https://github.com/espeak-ng/espeak-ng)) |
| Ghi chú | Dùng cục bộ không phân phối thì GPL ít ràng buộc hơn; ràng buộc sẽ tăng nếu sau này đóng gói ứng dụng |

### 4.7 VieNeu-TTS 0.3B và 0.5B – nhóm C

| Trường | Giá trị |
|---|---|
| Tên, vai trò | VieNeu-TTS-0.3B (huấn luyện từ đầu) và VieNeu-TTS 0.5B (tinh chỉnh từ `neuphonic/neutts-air`), TTS tiếng Việt |
| Artifact | https://huggingface.co/pnnbao-ump/VieNeu-TTS-0.3B; https://huggingface.co/pnnbao-ump/VieNeu-TTS |
| License ghi ở thẻ model | `apache-2.0` (metadata) |
| **Mâu thuẫn** | (1) [PyPI `vieneu` 1.0.6](https://pypi.org/project/vieneu/1.0.6/) (ngày 2026-01-12) ghi 0.3B "Released under **CC BY-NC 4.0** (Non-Commercial)... Commercial use is prohibited without authorization"; (2) dữ liệu huấn luyện [VieNeu-TTS-1000h](https://huggingface.co/datasets/pnnbao-ump/VieNeu-TTS-1000h) là **CC BY-NC 4.0**, chỉ cho nghiên cứu hoặc giáo dục, nguồn không công bố, **không có thông tin đồng ý của người nói** |
| Phụ thuộc | NeuCodec: Apache-2.0 và "Commercial use permitted" ([card](https://huggingface.co/neuphonic/neucodec)); NeuTTS Air: Apache-2.0, có watermark Perth ([card](https://huggingface.co/neuphonic/neutts-air)) |
| Thương mại | **Không đủ điều kiện:** huấn luyện bằng dữ liệu phi thương mại, tác giả yêu cầu liên hệ nếu dùng thương mại |
| Nhân bản giọng | Hỗ trợ từ 3–5 giây audio tham chiếu; thẻ model không nêu yêu cầu đồng ý. **Mặc định tắt** theo [security-and-rights.md](../architecture/security-and-rights.md) mục 7 |
| Ngày xác minh | 2026-10-31 |

### 4.8 VieNeu-TTS v3 Turbo – nhóm A

| Trường | Giá trị |
|---|---|
| Tên, vai trò | VieNeu-TTS v3 Turbo, TTS tiếng Việt (và Anh) |
| Artifact | https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo; `model.safetensors` 262 MB (kho 2.16 GB) |
| Revision | Commit kho `61b85e3d937fbbacb387714180e8182823512523` (khoảng một tháng trước thời điểm đọc). Thẻ model dẫn SDK PyPI `vieneu` 3.7.1; PyPI hiện ghi 3.8.3 (2026-09-23) |
| Quantization | Có `gguf`, `onnx`, `onnx_int8` trong kho; chưa xác định tag nào sẽ dùng |
| Voice ID | 23 giọng cài sẵn, mặc định "Minh Quân"; danh sách theo thẻ model (Anh Khôi, Mai Anh, Minh Quân, Minh Đức, Adam, Kim Thanh, Ngọc Huyền, Minh Triết, Ngọc Linh, Mỹ Duyên, Phạm Tuyên, Thái Sơn, Quỳnh Anh, Thanh Bình, Thùy Dung, Thục Đoan, Trúc Ly, Đức Trí, Xuân Vĩnh, Đoan Trang, Ngọc Trân, Quang Sơn, Mạnh Dũng). Thẻ nói danh sách chính thức lấy từ `list_preset_voices()`; **ID kỹ thuật chưa xác minh** |
| License | Apache-2.0 ở metadata và mục License; kho GitHub cũng Apache-2.0. Codec MOSS-Audio-Tokenizer-Nano: Apache-2.0 ([card](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano)) |
| Thương mại | Thẻ model nói giọng cài sẵn "may be used in commercial and monetized content" |
| Vì sao nhóm A | (1) Dữ liệu huấn luyện (~10.000 giờ Anh–Việt) **"not publicly disclosed"**, dataset gated, không có license nguồn; (2) quyền và sự đồng ý của người nói giọng cài sẵn chỉ là **tuyên bố, không có tài liệu**; (3) phonemizer `sea-g2p` chưa nêu license; (4) [README GitHub](https://github.com/pnnbao97/VieNeu-TTS/blob/main/README.md) liệt kê v3 Turbo là "on-device, personal use" ở lộ trình, **mâu thuẫn chưa giải quyết** với Apache-2.0 và tuyên bố thương mại; (5) cùng tác giả từng phát hành 0.3B với dữ liệu phi thương mại |
| Nhân bản giọng | Thẻ model cấm nhân bản người thật khi chưa được phép. **Mặc định tắt** trong dự án |
| RAM | Thẻ nói đường CPU không cần torch (ONNX Runtime), `int8` cần CPU có VNNI; **không nêu RAM**; chưa rõ hỗ trợ macOS arm64. Cần đo |
| Có thể làm rõ bằng | Hỏi tác giả bằng văn bản về dữ liệu huấn luyện và quyền thương mại; việc liên hệ bên ngoài cần Owner cho phép |
| **Kết quả đọc license (mã 2A, 2026-10-31)** | (a) [Kho GitHub](https://github.com/pnnbao97/VieNeu-TTS) có LICENSE là mẫu Apache-2.0: chỉ áp cho **mã**. (b) **Kho Hugging Face của model không có tệp LICENSE** (danh sách tệp tại commit `61b85e3d…`: README, config, `model.safetensors`, onnx, gguf…); license được khai ở metadata `apache-2.0` và mục License/FAQ của README. **Thiếu tệp LICENSE riêng không có nghĩa nhà phát hành không cấp phép cho trọng số**: README (đọc trực tiếp 2026-10-31) nói Apache-2.0 áp dụng cho mọi artifact, gồm `model.safetensors`, ONNX và tài sản giọng. (c) README nói license "áp dụng cho mọi artifact trong kho", giọng cài sẵn dùng được cho nội dung thương mại và kiếm tiền; sự đồng ý của người nói chỉ là tuyên bố cho các giọng/trọng số đi kèm; cần ghi công hai dự án; cấm nhân bản người thật khi chưa được phép. (d) Dữ liệu huấn luyện ~10.000 giờ Anh–Việt, quy trình "not publicly disclosed", dataset gated. (e) **Chênh lệch số giọng:** thẻ model liệt kê 23 giọng, thư mục `gguf/voices` có 25 thư mục (có thêm `adam_bua`, `thien_tam_duc`; tên `minh_quan_pro`), chưa đối chiếu. |
| Kết luận 2A | Tuyên bố cấp phép **có** (README), nhưng **chưa lưu và đối chiếu toàn văn điều khoản mà README dẫn chiếu cho artifact tại revision đã chốt** (README đọc là bản hiện hành, chưa chứng minh trùng với commit `61b85e3d…`). Còn bất định: dữ liệu huấn luyện không công bố; consent chỉ là tuyên bố của nhà phát hành cho giọng cài sẵn; phụ thuộc (`sea-g2p`); mâu thuẫn "personal use" ở lộ trình GitHub. S2 không áp dụng cho TTS. **Giữ nhóm A**, không phải kết luận là nhà phát hành không cấp phép. Hỏi tác giả (cần Owner cho liên hệ ngoài) là một cách làm rõ, không phải cách duy nhất; có thể lưu và đối chiếu thêm bằng tài liệu |
| Ngày xác minh | 2026-10-31 |

### 4.9 Kokoro v1.0 – nhóm A

| Trường | Giá trị |
|---|---|
| Tên, vai trò | Kokoro-82M v1.0, TTS tiếng Anh (không có tiếng Việt) |
| Repository, artifact | https://github.com/hexgrad/kokoro; https://huggingface.co/hexgrad/Kokoro-82M |
| Version, revision | v1.0 (2025-01-27); SHA-256 của model `496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4` (theo thẻ model); **commit Hugging Face không được hiển thị**; gói `kokoro>=0.9.2` |
| Voice ID | 54 giọng, 8 ngôn ngữ. Tiếng Anh Mỹ: `af_heart`, `af_bella`, `af_nicole`, `am_michael`, `am_fenrir`, `am_puck`... Tiếng Anh Anh: `bf_emma`, `bm_george`... Đánh giá chất lượng ghi trong VOICES.md (ví dụ `af_bella` A-, `bf_emma` B-) |
| License | Mã và trọng số Apache-2.0 |
| Dữ liệu huấn luyện | Thẻ nói chỉ dùng dữ liệu "permissive/non-copyrighted", gồm domain công cộng, license Apache hay MIT, và **"synthetic audio from closed TTS models by large providers"**. Ghi nhận CC BY: Koniwa `tnc` (CC BY 3.0), SIWIS (CC BY 4.0) |
| Phụ thuộc | `misaki` (license chưa nêu trên trang đã đọc); `espeak-ng` GPL-3.0 trở lên |
| Vì sao nhóm A | Dữ liệu tổng hợp từ TTS đóng của nhà cung cấp lớn: **điều khoản của các nhà cung cấp đó có thể hạn chế dùng đầu ra để huấn luyện**; chưa đọc. License `misaki` chưa xác minh. Chưa có từng giọng được nêu nguồn |
| Dung lượng, RAM | 82M tham số; dung lượng tệp không nêu; RAM chưa có nguồn. Thẻ nêu chạy được trên Apple Silicon bằng `PYTORCH_ENABLE_MPS_FALLBACK=1` |
| Ngày xác minh | 2026-10-31 |

### 4.10 Ứng viên khác

| Ứng viên | Nhóm | Ghi chú |
|---|---|---|
| ViZipVoice ([contextboxai/ViZipvoice](https://huggingface.co/contextboxai/ViZipvoice)) | A (mã 2A, mới) | Fine-tune từ k2-fsa/ZipVoice; thẻ ghi Apache-2.0 và đề nghị ghi công ZipVoice. ~7.000 giờ (≈6.500 Việt, 500 Anh), **không nêu nguồn dữ liệu và license từng nguồn**; không có commit/revision (chỉ `checkpoint-1860000.pt`, FP16); không nêu dung lượng; hỗ trợ nhân bản giọng, 30 audio mẫu trong `audio/` **không có tài liệu đồng ý**. License của ZipVoice gốc và dữ liệu chưa đọc. Chưa đạt (i), (ii) của S2; không áp dụng S2 cho TTS. Chỉ nghiên cứu |
| VietTTS ([dangvansam/viet-tts](https://huggingface.co/dangvansam/viet-tts)) | **C** | Mã Apache-2.0 nhưng model huấn luyện sẵn và mẫu âm thanh **CC BY-NC** (theo kết quả tìm kiếm; chưa đọc toàn văn thẻ) |
| viXTTS (capleaf/viXTTS) | **C** | Coqui Public Model License: chỉ phi thương mại (theo kết quả tìm kiếm; chưa đọc toàn văn) |
| F5-TTS | **C** | Mã MIT nhưng model huấn luyện sẵn **CC-BY-NC** (dữ liệu Emilia); trang không nêu model tiếng Việt ([repo](https://github.com/SWivid/F5-TTS)) |
| Gemma 3 4B | A | "Gemma Terms of Use" chưa đọc nội dung |
| Gemma 3 12B | **C** | 8.2 GB, quá nặng cho vòng đầu với RAM 16 GB |
| resvg | A | Apache-2.0 hoặc MIT; cách dùng từ Python chưa xác minh. Vai trò ngoài LLM, TTS; chưa kiểm tra lại vòng này |
| CairoSVG | A | LGPL-3.0; chưa kiểm tra lại vòng này |
| faster-whisper | A | MIT; trang chỉ nêu GPU NVIDIA, không nêu Apple Silicon; license trọng số Whisper chưa đọc; chưa kiểm tra lại vòng này |

## 5. Tài nguyên và ngân sách

| Mục | Điều đã biết | Mức tin cậy |
|---|---|---|
| Dung lượng tải LLM | Qwen3 4B Q4_K_M 2.6 GB; 8B Q4_K_M 5.2 GB | Cao (trang Ollama) |
| Dung lượng giọng Piper | ~63 MB mỗi giọng medium | Cao (liệt kê Hugging Face) |
| Dung lượng VieNeu v3 Turbo | `model.safetensors` 262 MB; kho 2.16 GB | Cao |
| **RAM runtime** | **Chưa có nguồn cho bất kỳ ứng viên nào.** Dung lượng tải không phải RAM runtime | Chưa biết; benchmark phải đo |
| Ổ đĩa | Khoảng 338 GiB trống (2026-10-31) | Cao |
| Thời gian | Tối đa 4 giờ cho **toàn bộ** video, gồm nghiên cứu, kịch bản, TTS, hoạt hình, render, phụ đề. Không đưa ra hiệu năng nào khi chưa đo | – |

### Mô hình tuần tự trên MacBook Air M4 16 GB

Không có con số RAM hay thời gian nào ở đây; đây là cách đo, không phải kết quả.

| Nguyên tắc | Nội dung |
|---|---|
| Bộ nhớ chung | 16 GB dùng chung cho macOS, công cụ chạy nền và model. Dung lượng tải không phải mức dùng RAM |
| Thứ tự dự kiến mỗi video | LLM (Athena, Leonardo) → TTS (Edison) → rasterize SVG (Pixar) → FFmpeg (Spielberg); faster-whisper khi cần phụ đề. Mỗi bước nạp model, chạy, giải phóng rồi mới sang bước sau |
| Không cộng dồn | Chỉ một tác vụ nặng tại một thời điểm, nên điều kiện "vừa RAM" xét **từng bước riêng**; mức đỉnh của video là đỉnh lớn nhất của một bước, không phải tổng |
| Cần đo cho mỗi ứng viên | RAM đỉnh; thời gian nạp lần đầu; thời gian xử lý; swap; hiện tượng giảm xung nhiệt; kết quả sau khi giải phóng model |
| Ngân sách | 4 giờ cho **toàn bộ** video (Q-06), gồm cả thời gian nạp và giải phóng model giữa các bước. Cách chia giữa các bước chưa quyết, chỉ chốt sau khi có số đo |
| Thứ tự đo | Qwen3 4B trước, 8B sau và chỉ khi 4B đủ chỗ; 8B có rủi ro bộ nhớ cao nhất |
| Kết luận | **Chưa ứng viên nào được coi là "vừa" hay "đạt" trước khi đo** |

## 6. Điểm chưa chắc chắn

1. Báo cáo gốc của Codex không có trong repo; chưa đối chiếu từng finding.
2. Nhận định license đến từ tóm tắt trang; toàn văn LICENSE mới đọc cho Qwen3 4B, 8B và Ollama (qua công cụ tóm tắt, không phải tệp nguyên văn).
3. Qwen3: chưa biết commit Hugging Face nào là nguồn của blob Ollama; tiếng Việt chưa xác nhận; dữ liệu huấn luyện không công bố.
4. Piper: câu "personal use and research only" chưa giải quyết; `25hours_single` và các giọng `en_US` khác chưa đọc.
5. VieNeu v3 Turbo: dữ liệu huấn luyện không công bố, mâu thuẫn với lộ trình "personal use".
6. Kokoro: điều khoản của nhà cung cấp TTS đóng mà dữ liệu tổng hợp lấy từ đó; license `misaki`.
7. Hồ sơ hai nhân vật khác biệt cho tiếng Anh: Piper `ljspeech` chỉ có một giọng; Kokoro có nhiều giọng nhưng đang nhóm A.

## 7. Hệ quả cho R1 và lựa chọn của Project Owner

Không có TTS tiếng Việt nào hiện đủ điều kiện nhóm B. Các hướng (Owner đã chọn **hướng 2: nghiên cứu tài liệu**, mã 2A; kết quả ở mục 4.8 và 4.10. Các hướng còn lại chưa chọn; hướng 1 phần hỏi tác giả cần Owner cho liên hệ ngoài):

| Hướng | Nội dung | Ghi chú |
|---|---|---|
| 1 | Tiếp tục nghiên cứu VieNeu v3 Turbo: đọc toàn văn license và hỏi tác giả | Cần Owner cho phép liên hệ bên ngoài |
| 2 | Tìm thêm ứng viên TTS tiếng Việt chưa nghiên cứu | Chỉ nghiên cứu tài liệu |
| 3 | Dùng dịch vụ hay dữ liệu thương mại trả phí | **Cần Owner cho phép chi phí**; hiện cấm |
| 4 | Giữ Phase 1 chỉ cho LLM và render, hoãn TTS tiếng Việt | Không giải quyết R1 |
| 5 | Xem lại phạm vi tiếng Việt trước Phase 4 và 5 | Thay đổi phạm vi cần Owner |

### 7.1 Tiêu chuẩn bằng chứng cho nhóm B (Owner đã chọn S2, 2026-10-31)

**Vấn đề (P1-001):** hồ sơ đặt ra tiêu chuẩn "mắt xích dữ liệu hoặc phụ thuộc chưa rõ thì chưa đủ nhóm B", nhưng không nói "chưa rõ" gồm những gì. Cùng một loại bất định (dữ liệu huấn luyện không công bố) đã khiến TTS bị giữ ở nhóm A nhưng Qwen3 từng được xếp B mà không có tiêu chí phân biệt. Claude **không tự chọn** tiêu chuẩn; hai phương án để Owner quyết định:

| Phương án | Nội dung | Hệ quả |
|---|---|---|
| **S1 – nghiêm ngặt** (giữ nguyên chữ của tiêu chuẩn hiện tại) | Nhóm B đòi mọi mắt xích trong chuỗi, kể cả nguồn dữ liệu huấn luyện, phải được tài liệu hóa | Nhóm B gần như luôn trống với mô hình trọng số mở, vì dữ liệu huấn luyện thường không công bố. Không ứng viên nào benchmark được |
| **S2 – rủi ro dư có chủ ý** (đề xuất của Claude; **Owner đã chọn ngày 2026-10-31**) | Nhóm B đòi: (i) đã đọc toàn văn LICENSE của đúng artifact và runtime; (ii) revision hoặc digest đã ghi, phần chưa định danh nêu chính xác; (iii) **không có bằng chứng trái ngược** trong chuỗi (không có mắt xích phi thương mại, không có phát biểu mâu thuẫn từ nhà phát hành). Dữ liệu huấn luyện không công bố được ghi là **rủi ro dư, do Owner chấp nhận bằng văn bản khi duyệt**, không phải điều kiện đã thỏa | Qwen3 4B và 8B đủ nhóm B. VieNeu v3 Turbo vẫn A vì có phát biểu mâu thuẫn ("personal use"); Kokoro vẫn A vì có nghi vấn cụ thể (âm thanh tổng hợp từ TTS đóng); Piper `ljspeech` vẫn A vì câu "personal use" chưa giải quyết |

**Quyết định của Owner:** ngày 2026-10-31, trả lời câu hỏi "chọn S1 hay S2 cho tiêu chuẩn nhóm B", Project Owner viết nguyên văn: "Chọn S2". Claude chép lại; hash không chứng minh được nguồn lời này, nên Owner cần đọc dòng này.

**Phạm vi của quyết định S2, hiểu hẹp nhất có thể:**

- Là **tiêu chuẩn phân loại nhóm B**. Dữ liệu huấn luyện không công bố được coi là **rủi ro dư do Owner chấp nhận**, chỉ cho các ứng viên **thỏa đủ ba điều kiện (i), (ii), (iii)** ở trên.
- **Không** là kết luận pháp lý hay kết luận license thương mại cuối cùng. **Không** là duyệt danh sách model. **Không** là quyền tải, cài, chạy, benchmark, commit, push, liên hệ ngoài hay chi phí. Các việc đó vẫn cần Owner quyết định riêng.
- **Không** áp dụng cho TTS, hay cho ứng viên có phát biểu mâu thuẫn hoặc nghi vấn cụ thể.
- Các giới hạn định danh và các bất định liệt kê ở mục 4.1, 4.2 và 6 **đi cùng hồ sơ**; chấp nhận rủi ro dữ liệu huấn luyện không xóa chúng.

**Đối chiếu ba điều kiện S2 (Claude đánh giá; Codex đã APPROVED phân loại tại RR-005, vòng 2/3):**

| Ứng viên | (i) Đọc LICENSE đúng artifact và runtime | (ii) Revision hoặc digest, nêu phần chưa định danh | (iii) Không có bằng chứng trái ngược | Nhóm theo S2 |
|---|---|---|---|---|
| Qwen3 4B `q4_K_M` | Có: Apache-2.0 (Hugging Face) và MIT (Ollama) được Codex đối chiếu độc lập ở RR-003. **Hạn chế:** blob license 11,338 byte trong gói Ollama chưa so từng byte | Có: digest manifest và model layer, commit đầu kho. **Hạn chế:** Codex không truy cập được manifest và API 4B ở RR-004, nên chưa xác nhận độc lập; chưa biết commit nguồn của GGUF | Không tìm thấy | **B** |
| Qwen3 8B `q4_K_M` | Như 4B | Như 4B; Codex xác nhận độc lập commit đầu kho 8B, chưa xác nhận manifest | Không tìm thấy | **B** |
| VieNeu-TTS v3 Turbo | Chưa đọc toàn văn | Có commit kho; dữ liệu không công bố | **Có phát biểu mâu thuẫn:** lộ trình "personal use" so với Apache-2.0 | A |
| Kokoro v1.0 | Chưa đọc toàn văn; `misaki` chưa nêu license | Có SHA-256 model, thiếu commit | **Có nghi vấn cụ thể:** âm thanh tổng hợp từ TTS đóng | A |
| Piper `en_US-ljspeech-medium` | Chưa đọc toàn văn | Có commit | **Có điểm chưa giải quyết:** câu "personal use and research only" | A |
| resvg, CairoSVG, faster-whisper, Gemma 3 4B, các giọng Piper chưa đọc | Chưa kiểm tra theo S2 | – | – | A (chưa đánh giá) |
| Các ứng viên nhóm C | – | – | Có mắt xích phi thương mại | C |

Chỉ Qwen3 được chuyển lên B. Codex đã `APPROVED` phân loại này tại RR-005 (vòng 2/3), kèm lưu ý: chọn **tiêu chuẩn** S2 không thay việc Owner duyệt **từng ứng viên và rủi ro dư kèm theo**; mọi phần chưa xác minh phải đi cùng hồ sơ trình Owner. Owner vẫn phải duyệt danh sách và cấp quyền tải riêng.

## 8. Bước tiếp theo

Owner đã trả lời "1B, 2A, 4a, 4b": danh sách model chỉ có Qwen3 4B `q4_K_M`; nghiên cứu TTS tiếp tục bằng tài liệu (kết quả ở 4.8 và 4.10: vẫn **không có TTS tiếng Việt nào đủ nhóm B**, R1 còn nguyên). Chờ Owner chỉ đạo: hướng TTS tiếp (mục 7, gồm cho phép liên hệ tác giả VieNeu), quyền tải, cài, chạy từng bước. Codex đã `APPROVED` hồ sơ tại RR-004 và phân loại theo S2 tại RR-005; các thay đổi sau RR-005 (1B, 2A) **chưa được Codex review**. **Nhóm B và việc duyệt danh sách chưa phải quyền tải hay chạy.** Không có gì được tải, cài hay chạy.
