# Review RR-013
- Scope Grant: SG-006 | Vòng: 0/3 | Ngày: 2026-11-01 (Asia/Ho_Chi_Minh)
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`; phiên bản thực tế: snapshot SHA-256 RR-013, không chỉ commit (src/tests/benchmarks chưa track).
- Đầu vào chính: `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md`, 29928 byte, SHA-256 `1e3a2634f1666beaf367221cec1b88e03b3814a28f1d73fdff66d2770c88adb1`.
- Kết luận: **CHANGES REQUESTED** — hướng kiến trúc khả thi có điều kiện, nhưng hợp đồng dữ liệu, compiler, an toàn runtime và tiêu chí thử chưa đủ để triển khai.
- Đây là review thiết kế/spike riêng, không nghiệm thu, không mở Phase 2, không cấp quyền cài/chạy POC. Không đóng P1-005 hay thay đổi lịch sử SG khác.

## 1. Kết luận điều hành và quyết định thiết kế chấp nhận

Chấp nhận về hướng: LLM chỉ sinh dữ liệu; validator độc lập; TTS trước khi chốt timeline; compiler không dùng LLM; template JS cố định; render câm rồi mux; chạy tuần tự; hai nhánh R (tham chiếu) và L (Ollama); lưu đầu ra LLM/TTS để replay; human approval cuối pipeline. Chưa có bằng chứng B-Lite chạy được vì chưa triển khai, và review này không chạy model, TTS hoặc renderer.

Không có API trả phí bắt buộc trong chuỗi đề xuất. Đây là khả thi về thiết kế, chưa VERIFIED end-to-end. Điện, khấu hao máy/SSD, thời gian phát triển, thuê bao công cụ lập trình và thời gian duyệt vẫn là chi phí. License thương mại còn chặn ở VieNeu; không thể suy từ “chạy local, không API trả phí” thành “đủ quyền kiếm tiền”.

## 2. Findings cần sửa trước triển khai

### [HIGH] B2B-001 — Thiếu hợp đồng nối storyboard mới với Edison, Pixar và Spielberg
- Vị trí: `docs/operations/phase-reports/PHASE-02B-DESIGN-REPORT.md:18`, `:70`, `:340`; `src/ai_video_factory/agents/edison/__init__.py:92`; `src/ai_video_factory/agents/pixar/__init__.py:85`; `src/ai_video_factory/agents/spielberg/__init__.py:47`.
- Bằng chứng: Edison đọc `leonardo/script.json` theo `scenes`, Pixar đọc cả script/storyboard theo `scenes`, Spielberg đọc `scene_spec.json` và `mouth.json`. Đề xuất thay bằng `story_beats` và `timeline.json`, nhưng chưa định nghĩa bridge, schema timing/timeline hay tích hợp Edison. Danh sách file mới không thể hiện đầy đủ thay đổi đó.
- Tình huống gây lỗi: storyboard mới qua validator nhưng agent cũ không tìm thấy `scenes`; beat không ánh xạ được câu/word; render hoặc lip-sync thiếu artifact.
- Yêu cầu khắc phục: đặc tả rõ đầu vào/đầu ra/version của từng bước; bảng beat→scene→sentence→word; giữ lời đọc đúng checksum sau normalize; quyết định bridge sang Edison cũ hay entry point mới. Khai báo FPS, kích thước, tổng frame, sample rate, asset/rig version, interpolation và camera trong timeline. Tách core thuần khỏi IO/subprocess trong adapter.
- Trong phạm vi SG: có, review; sửa thiết kế cần Owner cấp quyền riêng.

### [HIGH] B2B-002 — Action vocabulary chưa diễn đạt đủ brief, thiếu state machine và scheduler
- Vị trí: báo cáo `:120`, `:254`, `:266`.
- Bằng chứng: schema chỉ có actor/action/target/expression/at_word. Không có initial pose, tay đang cầm gì, đích đặt đồ, thời lượng, quan hệ parent, trạng thái prop, thứ tự hành động đồng thời. Brief A cần điện thoại đã cầm, ngồi, nút gửi và xóa tin, thay đêm→sáng. Brief B cần nắp phủ chảo và lửa tắt; các hiệu ứng đó chưa có ngữ nghĩa dữ liệu. `use_item` quá rộng để phân biệt gõ/xóa/nhấn.
- Tình huống gây lỗi: `use_item` không có pickup trước; hai hành động cùng tay/cùng frame; đồ vật dịch chuyển tức thời; compiler phải viết nhánh riêng theo topic hoặc tự bịa state.
- Yêu cầu khắc phục: chốt initial_state; target là ID instance và anchor rõ; action parameters hữu hạn; pre/postcondition; occupancy tay/pose/prop ownership; duration/start/end; luật xung đột và persistence/reset qua cut. Việc tự chèn hành động chỉ qua rule versioned đã duyệt, ghi report; không đủ thời gian thì reject. Định nghĩa clamp/fail IK ngoài tầm với, sweep collision, transform camera và text bounds ở screen space qua toàn đoạn. Safe zone hiện chỉ là hộp cho chữ, không phải solver va chạm.
- Trong phạm vi SG: có, review.

### [HIGH] B2B-003 — Data-only và textContent chưa đủ ngăn browser thực thi nội dung LLM
- Vị trí: báo cáo `:149`.
- Bằng chứng: chưa quy định cách chèn JSON, policy asset/URL/SVG, selector, CSP hay network enforcement. `textContent` chỉ bảo vệ nơi gán chữ, không bảo vệ HTML chứa JSON hoặc thuộc tính khác.
- Tình huống gây lỗi thiết kế: narration chứa `</script><script>…` nếu JSON được nhúng inline không escape; asset path `../`; SVG có script/event/foreignObject/URL; action ID được ghép thành selector, expression hoặc filtergraph.
- Yêu cầu khắc phục: runtime chỉ nhận cấu trúc đã validate, số hữu hạn và giới hạn kích thước; ưu tiên JSON riêng qua cùng origin; nếu nhúng inline phải escape theo ngữ cảnh HTML. Không eval/Function/innerHTML hay code template từ dữ liệu. Resolve path trong asset root, chặn symlink thoát root, remote URL và SVG chủ động; map ID tới object allowlist. Chặn outbound ở browser và kiểm tra nguồn local; subprocess dùng argv cố định, không shell. Ca kiểm thử ác ý phải là negative tests trước render.
- Đây là lỗ hổng trong đặc tả an toàn, chưa phải exploit đã tái hiện trên code B-Lite (code chưa tồn tại).
- Trong phạm vi SG: có, review.

### [HIGH] B2B-004 — Thiếu supervisor, giới hạn tài nguyên và phục hồi cho tiến trình con
- Vị trí: báo cáo `:149`, `:204`, `:323`; `src/ai_video_factory/adapters/tts/vieneu_tts.py:33`; `src/ai_video_factory/adapters/llm/ollama.py:13`.
- Bằng chứng: workers=1 không giới hạn toàn bộ cây Chrome/Node/FFmpeg. Chưa có wall timeout, progress timeout, kill/reap descendants, staging/atomic promotion, cancellation, disk budget. Adapter VieNeu hiện gọi subprocess không timeout; Ollama mặc định timeout HTTP 900s, keep_alive 5m, không khớp budget Ollama 5 phút nếu dùng nguyên trạng.
- Tình huống gây lỗi: Chrome treo, sleep/wake hoặc TTS không thoát khiến pipeline vượt budget; retry chồng orphan; MP4 dở bị coi thành công. `keep_alive:0` là yêu cầu unload, chưa chứng minh model đã nhả tài nguyên.
- Yêu cầu khắc phục: supervisor chung cho các bước nặng, process group và cleanup có giới hạn; xác nhận model unload trước bước sau; tổng budget gồm retry và hai lượt LLM; một attempt dir riêng, chỉ promote sau QC, không ghi đè/xóa đầu ra cũ. Ghi peak memory toàn cây, memory pressure, swap delta và free disk. Thay “swap nặng” bằng ngưỡng đo/thời hạn Owner duyệt; ưu tiên dừng có kiểm soát, giữ bằng chứng. POC CLI không cần tự xây queue production hoặc tự duyệt D-018.
- Trong phạm vi SG: có, review.

### [MEDIUM] B2B-005 — storyboard/1.0 mới là ví dụ dữ liệu; timing và vai trò chưa khép kín
- Vị trí: báo cáo `:70`, `:287`; `src/ai_video_factory/core/wordtime.py:1`.
- Bằng chứng: chuỗi `a | b` và `<enum>` không phải JSON Schema thực thi. Format hài dùng ESCALATION nhưng enum beat role không có escalation. Camera “chi tiết không do LLM sinh” vẫn cần phân biệt enum intent với camera đã resolve. Wordtime ghi rõ ước lượng, chưa đo sai số thực.
- Tình huống: at_word âm hoặc trỏ sai do tokenize/normalize; payoff trỏ beat không tồn tại; ID trùng; action vượt biên beat; câu ngắn không đủ thời lượng hành động. Schema đúng vẫn có thể kể sai hoặc bịa fact.
- Yêu cầu: JSON Schema thật, required/additionalProperties, min/maxItems, giới hạn chữ/số, unique IDs và referential integrity ở Python; quy tắc format-specific; enums thống nhất. Tokenization tiếng Việt versioned, at_word zero-based và scope beat/sentence rõ, map sang text đã normalize. Timing ghi method/uncertainty; đo alignment trên mẫu nghe có đánh dấu, ví dụ đề xuất p95 sai lệch ≤150ms cho cue thường, cue nhạy dùng mốc câu/audio xác minh. Không gọi ước lượng word timing là timing từ chính xác. Resolve duration sau TTS; không pad im lặng để che thiếu nội dung.
- Trong phạm vi SG: có, review.

### [MEDIUM] B2B-006 — 80% và nhịp thay hình có thể cho kết quả đạt giả
- Vị trí: báo cáo `:42`, `:287`.
- Bằng chứng: 20 lần/format chưa phân biệt prompt mới với lặp seed, first-pass với after-retry. Movement 0.3s/cut mỗi 3s không chứng minh retention. 26–42 âm tiết ở 4.29 âm tiết/s chỉ khoảng 6.1–9.8s lời, chưa tự bảo đảm video 12–15s.
- Yêu cầu: 80% chỉ là gate thăm dò; 100% artifact được chấp nhận phải qua structural/semantic/safety gate. Báo first-pass, after-retry, timeout, unsupported, human accept và latency riêng. Đóng băng prompt/schema/compiler trước held-out; 20 prompt mới/format, phân tầng ngôn ngữ/số/ký tự lạ/action hợp lệ và không hỗ trợ. Đề xuất ≥90% valid sau tối đa 3 attempt là mục tiêu POC tiếp theo do Owner chốt, không suy ra production reliability từ 40 mẫu. Không âm thầm sửa JSON hay sửa code theo held-out.
- Trong phạm vi SG: có, review.

### [MEDIUM] B2B-007 — HyperFrames strict chưa bảo đảm media sẵn sàng và offline
- Vị trí: báo cáo `:149`, `:204`.
- Bằng chứng độc lập: package HyperFrames cài tại OpenMontage là 0.8.226, engines node>=22, có esbuild và optional sharp; không thấy lifecycle install script trong package gốc. `dist/render-NEZLBRAY.js:1665` quy định strict chỉ chặn lint errors, strict-all thêm warnings; best-effort mặc định true. `:1659` mô tả no-best-effort chặn missing/unready media. Telemetry opt-out khác update check.
- Yêu cầu: fail closed với readiness; dùng strict-all nếu đó là policy đã chọn hoặc phân loại warning cụ thể; không coi lint/validate/snapshot là QC nội dung. Ghim nguồn/lock/integrity/runtime/browser/fonts; xác nhận install hooks toàn cây. Bổ sung HYPERFRAMES_NO_UPDATE_CHECK=1 và kiểm tra auto-install/update path; env opt-out không thay network isolation. npm ci vẫn có thể cần mạng nếu cache thiếu: quy trình setup online được cấp phép khác runtime offline. Không dùng cache chung có quyền cập nhật nếu cần độc lập; artifact browser riêng, hash/version/provenance. no-browser-gpu là software rendering, chưa chứng minh ít RAM hoặc nhanh hơn.
- Trong phạm vi SG: có, review.

### [MEDIUM] B2B-008 — alimiter không tự chứng minh true peak và chất lượng nhạc
- Vị trí: báo cáo `:167`, `:287`.
- Bằng chứng: báo cáo gắn ≤-1dBTP “qua alimiter” nhưng chưa quy định oversampling, auto-level, latency compensation hoặc đo sau AAC. Mã upstream alimiter có auto-level mặc định bật, latency compensation mặc định tắt; cần cấu hình rõ thay vì dựa tên filter.
- Yêu cầu: mix ở sample rate cố định; loudness/true-peak measurement sau encode/decode final AAC; cân nhắc loudnorm hai lượt và headroom codec, kiểm tra sample count/PTS và bù delay. Định nghĩa chênh 12dB/6dB đo trên stem/window nào; không so peak với LUFS. Envelope ducking lấy vùng lời có bảo vệ đầu âm tiết, không chỉ word estimate. Chấp nhận precomputed gain thay sidechain nếu được nghe kiểm tra; sidechain cũng có thể lặp lại với chain cố định. Không ép nâng bản mix lên -14 bằng nhạc/SFX làm che lời; mục tiêu là profile POC, không quy luật mọi nền tảng.
- Trong phạm vi SG: có, review.

### [MEDIUM] B2B-009 — Brief B rủi ro cao hơn cần thiết; quyền và gate chưa đủ rõ
- Vị trí: báo cáo `:235`, `:266`, `:380`.
- Bằng chứng: brief chữa cháy vẫn được giữ dù yêu cầu review ban đầu đề nghị thay; schema fact_ref chỉ ở hook, không bao quát claims trong lời. Gate tối thiểu track.json không bảo đảm quyền toàn gói, và dùng nội bộ không tự miễn các hạn chế license.
- Yêu cầu: thay Brief B bằng ví dụ đời thường bên dưới; mọi claim có evidence mapping, reviewer xác minh sự hỗ trợ của nguồn, không chỉ tồn tại ID. Phân biệt quyền thử nội bộ và quyền phát hành; không đưa VieNeu vào output thương mại khi chưa clearance. Asset manifest phải bao gồm rig/props/font/SFX/voice/model/runtime và checksum evidence, approved scope; synthetic track cho phép nguồn generator nội bộ, không ép license_url bịa. D-022 vẫn Proposed; gate POC chỉ là kiểm soát hẹp được Owner cho phép, không nghiệm thu D-022. GSAP và phụ thuộc cần rà đúng artifact/use-case trước cài, không chỉ trước lúc “làm app”.
- Trong phạm vi SG: có, review.

## 3. Tương thích Factory Manager + 7 Agent

Không cần thêm agent. Content Strategy hiện thuộc Athena theo PROJECT_MASTER; đề xuất chuyển hết sang Leonardo cần giữ Athena chịu trách nhiệm audience/facts/strategy hoặc Owner duyệt phân công mới. Leonardo cụ thể hóa hook/beat/storyboard. Edison giữ voice/timing; Pixar compiler; Spielberg dựng/mix/QC. Bảng POC mới chỉ liệt kê năm agent: ghi rõ Tesla là disabled publishing stub và Newton chỉ benchmark/log stub, không xóa khỏi kiến trúc. Approval gắn checksum đầu ra; đổi bất kỳ media/metadata nào phải mất hiệu lực duyệt.

Danh sách module tự nó không tạo cross-agent import, phù hợp hướng agent→core/adapters. Nhưng `core/mixdown.py`/QC nếu gọi FFmpeg phải tách logic thuần với executor adapter; manager chỉ orchestration, không nhét story/renderer logic vào `blite.py`. Không gọi toàn bộ đó là “sửa tối thiểu” trước khi liệt kê bridge Edison và schema migration.

## 4. Content Quality Gate và hai brief

Cấu trúc thay theo genre/duration là đúng; CTA tùy chọn, video 12–15s không ép đủ sáu phần. Mở đầu cần vấn đề/ham muốn rõ, một hành động nhìn hiểu được, payoff trả đúng lời hứa. Không suy số lần cut thành retention; cảnh giữ lâu có thể cần cho người xem hiểu. Các luật “hôm nay”, “ai cũng” là warning có ngữ cảnh, không đủ làm máy phát hiện sai sự thật. Human duyệt liên kết opening_visual↔hook và payoff↔promise; string matching không làm được.

Gate đề nghị: (1) máy kiểm cấu trúc/facts refs/duration/action khả thi/không asset thiếu; (2) Owner chấm từng video hook rõ trong 3s, tò mò hoặc cảm xúc phù hợp, diễn tiến dễ hiểu, hành động có nghĩa, payoff và CTA; từng mục cốt lõi ≥4/5, không lấy trung bình che một mục hỏng; (3) không sai claim/khó hiểu nghiêm trọng. “Muốn xem lại” là đánh giá chủ quan, chưa phải retention thực từ người xem.

Brief A “Đừng bấm Gửi”: giữ, nhưng quyết định “chạm nút” là hover hay đã gửi; lời và hình phải nhất quán với “chưa gửi”. Đêm→sáng cần scene-state dữ liệu hữu hạn; xóa draft cần action có nghĩa đã định nghĩa, không custom handler theo brief.

Thay Brief B: “Cốc giấy làm chặn giấy”. Ví dụ Owner tinh chỉnh: “Giấy cứ bay? Đặt chiếc cốc lên góc giấy. Bỏ tay ra: tờ giấy đã nằm yên.” Problem→pick_up→put_down→result, dùng paper/cup/desk, không chữa cháy, không claim an toàn. Gió/giấy chuyển động chỉ thêm nếu là prop-state/action dữ liệu tổng quát đã duyệt; có thể mở đầu bằng giấy lệch nhẹ. A là micro-story về quyết định, B là explainer tương tác vật; cả hai cùng compiler. Brief C giữ kín, cung cấp sau freeze và nằm trong capability envelope đã công bố; ngoài vocabulary phải reject đúng, không coi renderer phải làm được mọi chủ đề.

## 5. Nhạc, SFX và acceptance bằng nghe

NumPy phù hợp kiểm chứng pipeline và provenance, chưa đủ chứng minh nhạc tự nhiên. Cắt scope từ bốn mood xuống hai đoạn ngắn tense/playful hoặc warm, generator version+seed+source hash+PCM hash và quyền nguồn đầy đủ. Không dùng sample/model nhạc chưa duyệt. Match phách với payoff phải bảo đảm đủ head/tail, không âm thầm loop hoặc cắt nốt; fade theo sample, không click và không đổi duration.

Owner nghe nhạc riêng và bản mix trên loa máy cùng tai nghe, âm lượng bình thường. Chấm riêng độ tự nhiên, mood phù hợp, nhịp hỗ trợ câu chuyện, chuyển/kết đoạn, mức gây phân tâm: đề xuất mỗi mục ≥3/5 cho POC, không lỗi nghiêm trọng; lời nghe hiểu đầy đủ, không pumping/click/chói/giật mình, không che từ quan trọng. Ghi rõ thiết bị và người chấm. Đạt loudness nhưng nhạc bị từ chối thì MUSIC chưa PASS; fallback “none” cho phép kiểm phần khác nhưng không hoàn tất bằng chứng narration+music+SFX.

## 6. HyperFrames 0.8.226: đã kiểm và giới hạn

Đọc trực tiếp upstream npm package đã cài trong node_modules OpenMontage, không chạy CLI và không đọc/copy rig dự án. Xác nhận cờ local render: --fps, --quality high, --workers 1, --output, --strict, --strict-all, --no-browser-gpu. Node>=22; bản 24.22.2 chưa được review tarball/license đầy đủ. Managed Chrome constant đúng 152.0.7977.30 (`dist/chunk-WE42NVH7.js:22`); xác nhận constant không đồng nghĩa kiểm binary cache thực nhận. Các path/code dependency bổ sung không thuộc snapshot hash RR; cần ghi lại provenance khi cấp phép triển khai.

Template còn cần composition root metadata, duration/size/FPS, registration/readiness, assets/fonts loaded, seek ở thời điểm bất kỳ và không phụ thuộc history. Python resolve frame/keyframes; JS chỉ interpolation đã chốt, không tự tính IK, random hoặc state theo lần render. Test seek đảo thứ tự, frame đầu/cuối và action boundary; serialization sort keys/float quantization/finite values và version mọi dependency để đạt byte-identical timeline. MP4/pixel reproducibility là cấp khác; SSIM chỉ phản ánh sai khác ảnh, không chứng minh đúng câu chuyện hoặc đúng timing.

Nguồn chính thức trực tuyến được đọc bổ trợ, không thay tài liệu đúng phiên bản: [HyperFrames CLI](https://hyperframes.app/docs/5-packages/cli), [rendering](https://hyperframes.app/docs/3-guides/4-rendering). Metadata package ghi Apache-2.0, upstream [LICENSE](https://raw.githubusercontent.com/heygen-com/hyperframes/main/LICENSE) phù hợp về tên license; chưa audit toàn bộ bundled code và transitive notices đúng artifact.

## 7. License, backup và governance

GSAP Standard không phải OSI; điều khoản giới hạn tool cho phép dựng animation không code cạnh tranh với Webflow, và yêu cầu giữ proprietary notices. Chưa thể kết luận app tương lai được phép chỉ vì POC nội bộ hoặc không commit GSAP. Owner cần review đúng use-case và license artifact 3.15.0; scope POC hẹp, không UI builder/public service. [Điều khoản chính thức](https://gsap.com/community/standard-license/).

OpenMontage: tên điều khiển/ý tưởng đọc trong report không tự chứng minh có hoặc không có tác phẩm phái sinh. Không sao chép rig, assets, helper hay bundle được sửa riêng. Ghi hồ sơ tự viết, nguồn upstream độc lập và history; AGPL/UNLICENSED phải tách artifact, không mặc định một nhãn xóa được nghĩa vụ của nhãn kia. Đây là giới hạn đánh giá kỹ thuật, chưa clearance pháp lý. Không thay đổi OpenMontage; HEAD/status và tám đầu vào ngữ cảnh đều khớp RR.

VieNeu giữ internal-only theo governance hiện tại, chưa clearance thương mại. Qwen3 4B là lựa chọn duy nhất trong execution scope POC đề nghị; S2 phân loại 8B không phải quyền chạy. FFmpeg P1-005 nằm ngoài RR này, không đóng lại bằng lời “dùng nội bộ”. Node/Chrome/font và optional/bundled packages phải có full notice/license inventory, không chỉ trường license của lockfile.

Backup: tự đọc/hash 2.544 file snapshot và 44 file seal, tất cả khớp. MANIFEST/SEAL khớp hash RR. README_RESTORE còn trỏ AI_Projects/_project_backups thay vị trí hiện tại `~/_project_backups`. Không chạy restore và không xác minh lại khả năng dựng venv/model từ exclusions. Không đọc/in secret values; hash là kiểm tra byte, không chứng minh tác giả, ai di chuyển hoặc backup độc lập về thiết bị. Cùng SSD không bảo vệ mất máy/ổ; Q-07 và bản sao độc lập còn cần Owner quyết. Sửa hướng dẫn recovery bằng amendment/correction có provenance, không âm thầm phá seal snapshot.

SG-006 chỉ cho review, không cho triển khai; SG-003/004/005 vẫn ACTIVE không tự cấp quyền mới. Spike tách biệt có thể hợp lệ nếu Owner duyệt ngoại lệ thử nghiệm rõ; không được dùng nhãn spike để đưa vào production hoặc bỏ Phase Gate. D-002/Node/backend, hợp đồng artifact và audio cần quyết định riêng; D-009..D-022 vẫn giữ trạng thái. Không quy tài liệu trạng thái cũ thành finding mới của Phase 2B.

## 8. Phạm vi POC và S0–S9 điều chỉnh (đề nghị, chưa được phép chạy)

| Bước | Công việc nhỏ nhất | Cổng |
|---|---|---|
| S0 | Owner duyệt kế hoạch sửa thiết kế, scope spike, workspace/backup và quyền từng thao tác | Không cài/code trước quyền thực thi mới |
| S1 | Chốt contracts, schema/vocabulary/state và negative fixtures, provenance/license desk review | Resolve B2B-001/002/003 trước runtime |
| S2 | Ollama 4B với schema đầy đủ, test unseen; ghi first-pass/retry/semantic accept và ngân sách | Không đạt thì dừng trước rig phức tạp |
| S3 | Compiler thuần, một actor/scene, 6–8 action cần thiết, 3 props; invalid/state conflict/out-of-range tests; freeze | Canonical timeline hai lần byte-identical; không sửa theo topic |
| S4 | Cấp phép cài Node/HyperFrames/fonts đúng artifact; offline cache và executable provenance | License/install hooks/readiness reviewed |
| S5 | Một clip tham chiếu ngắn độc lập OpenMontage; kiểm seek/readiness/cancel/timeout/RAM/disk | Đạt supervisor và profile tài nguyên trước E2E |
| S6 | Mẫu nhạc riêng và mix lời+SFX, đo AAC cuối, Owner nghe | Chất lượng nhạc là gate riêng |
| S7 | A/B nhánh R rồi L, cùng runtime hash; không sửa source/scene code giữa brief | Log đầy đủ cả thất bại; không sửa tay storyboard L |
| S8 | Brief C held-out sau freeze; replay và benchmark lặp, so Pillow nếu cần | Sai thì ghi fail; sửa compiler phải có freeze và held-out mới |
| S9 | Báo cáo bằng chứng, review độc lập, Owner quyết | Không tự chuyển phase, publish, commit/push |

Pillow interpreter đầy đủ, IK phong phú, 20 action/12 props/4 mood, camera shake/whip và nhiều bối cảnh không phải điều kiện cho test nhỏ đầu tiên. POC có thể dùng các pose/keyframe hữu hạn, camera static/push-in, một căn phòng chung và screen-state hữu hạn. Production sau này mới mở rộng vocabulary, đa nhân vật, camera/collision phức tạp, queue/recovery đầy đủ và commercial TTS, qua scope riêng.

Benchmark ghi machine/OS/power state, model digest/prompt/options/schema hashes, warm/cold, tất cả attempts, code/assets/fonts/browser/runtime hashes, wall time theo stage, RSS toàn cây/swap/disk, QC và điểm người nghe. Đề xuất ba replay cache và ba run LLM mới/brief; không coi cached replay là bằng chứng generation mới. Kiểm offline production với loopback vẫn hoạt động, không outbound/API secret, không cloud fallback; chụp trạng thái/hash repo gốc trước/sau, không copy/symlink dependency từ OpenMontage.

## 9. Trả lời 12 câu hỏi mục 14

1. AGPL: chưa đủ để clearance; cần nguồn rig độc lập và ranh giới artifact như mục 7.
2. D-002: backend JS/Node là thay đổi cần Owner quyết riêng trước code; D-013 chỉ duyệt phương pháp benchmark.
3. Ollama: format hỗ trợ JSON Schema, không bảo đảm semantic correctness; ví dụ nested array/enum phải đo đúng schema/model, xem B2B-005/006 và [tài liệu Ollama](https://docs.ollama.com/capabilities/structured-outputs).
4. Browser: có đường injection nếu implementation dùng inline JSON/HTML/asset không an toàn; chưa có B-Lite code để khẳng định exploit, xem B2B-003.
5. Determinism: có hướng đúng, chưa đầy đủ readiness/seek/serialization; đã đối chiếu cờ 0.8.226 thay vì dựa duy nhất 0.7.17.
6. Python/JS: khả thi nếu transform/interpolation thống nhất, JS không giải IK lại và test boundary/seek.
7. Supply chain: ignore-scripts không audit bundled code hoặc bảo đảm offline; shared writable Chrome cache không đủ độc lập.
8. Audio: gain envelope hợp lý, cần speech-region chính xác và nghe; true peak phải đo final AAC, không suy từ limiter. Tham chiếu [alimiter upstream](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/libavfilter/af_alimiter.c), [filter documentation](https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/doc/filters.texi); chưa kiểm exact build bằng chạy lệnh.
9. Rights Gate: gate POC hẹp không mâu thuẫn mục tiêu fail-closed, nhưng không duyệt D-022 và không thay publishing rights gate.
10. Acceptance: cut frequency/schema validity/loudness/trung bình điểm đều có thể đạt giả; bắt buộc held-out và gate nội dung/nghe từng mục.
11. 8B: không trong quyền thực thi đề nghị; không cần 8B để chứng minh POC 4B.
12. Spike: không đi vòng gate nếu cách ly, giới hạn và Owner duyệt; tích hợp vào sản phẩm cần gate gốc.

## 10. Owner cần quyết định và bước tiếp

Bước tiếp theo: giao Claude sửa **thiết kế**, chưa triển khai, theo B2B-001..009; cấp allowlist thích hợp vì SG-006 hiện không cho sửa lại báo cáo và chưa cho REVIEW_RESPONSE.md. Giữ nguyên bản báo cáo đã hash, tạo bản bổ sung/sửa theo quyền Owner; RR mới tiếp nối tăng vòng, không sửa RR-013 hoặc lịch sử review.

Trước thực thi POC, Owner cần duyệt riêng: quyết định backend/Node/contracts/audio và phân công Athena; SG triển khai hẹp; workspace mới không remote, nguồn snapshot và quyền không ảnh hưởng repo gốc; từng lệnh cài/tải/chạy; profile 1080x1920/30fps thử nghiệm; 4B-only; VieNeu internal-only; use-case GSAP và nguồn nhạc/font; Brief B mới/held-out C; ngưỡng tài nguyên/thời gian và acceptance; correction recovery và backup độc lập. Không có việc nào trong danh sách này được review tự duyệt.

## Đã tự xác minh

- RR-013 OPEN/SG-006 ACTIVE/vòng 0/3/END marker hợp lệ; chỉ đạo Owner hiện tại kích hoạt lượt review. Lời SG chép lại có giới hạn xác thực đã công khai; hash không chứng minh tác giả.
- 221 hash file trong repo khớp RR (TASKS chỉ phần trước Review Requests); không nhóm C khi mở review; reviewer artifact 95288 byte đúng hash; HEAD khớp. Tám hash ngữ cảnh OpenMontage khớp, HEAD `195eab24478dc9363326aec437aefc3701635ddf`, status sạch.
- Đọc toàn bộ báo cáo 14 mục; đọc mã hợp đồng/schema/Ollama/TTS/wordtime/Pixar/render/manager và layout, bảng biểu cảm nhân vật; đối chiếu PROJECT_MASTER/ARCHITECTURE/DECISIONS cùng status/handoff/review response và phase plan/index hiện có. Không sửa code, không chạy test ứng dụng.
- Hash toàn bộ snapshot và seal backup như mục 7; xác minh mismatch đường dẫn trong recovery doc.
- Đọc metadata và phần CLI dependency upstream đã cài để xác minh flags, version, Chrome constant và env update/telemetry; không chạy CLI, không đọc/copy code rig OpenMontage.

## Chưa thể xác minh

- Runtime B-Lite, benchmark số đo cũ, chất lượng hình/giọng/nhạc, word alignment accuracy, unseen generation và memory Chrome; không render, không gọi Ollama/TTS, không cài hoặc tải model.
- Khả năng recovery môi trường từ exclusions; backup trên thiết bị độc lập; người di chuyển backup/Finder attribution; audit OpenMontage/Codex gốc không có trong snapshot RR.
- Full legal clearance, license tất cả dependency/bundled code đúng phiên bản, GSAP redistribution/use-case tương lai, exact FFmpeg filter behavior bản đã cài, binary Chrome cache integrity. Một số trang FFmpeg/GNU timeout; dùng raw FFmpeg upstream bổ trợ, không thay kiểm exact artifact.

CODEX PHASE 2B REVIEW

ARCHITECTURE: CONDITIONAL PASS

CONTENT STRATEGY: CONDITIONAL PASS

ACTION COMPILER DESIGN: FAIL

MUSIC SYSTEM: CONDITIONAL PASS

ZERO-PAID-API FEASIBILITY: CONDITIONAL

LICENSE AND GOVERNANCE: CONDITIONAL

IMPLEMENTATION READINESS: NOT READY

---

# Review RR-012
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-004, Amendment A01 | Vòng: 1/3 | Tiếp nối RR-011.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh main; snapshot SHA-256 trong RR-012.
- Kết luận: **APPROVED WITH CHANGES — KHÔNG PHẢI PASS** theo workflow mục 8. P1-005 đã bổ sung phần lớn bằng chứng, còn điều kiện chấp nhận/xác minh nguồn; chưa CLOSED. P1-006/P1-007 vẫn CLOSED.
- Phạm vi: P1-005 và hồi quy P1-006/P1-007 tại mục 8.1, 8.3 của hồ sơ FFmpeg. Không mở review công cụ khác, runtime hoặc quyền cài.

## Phát hiện và điều kiện còn lại

### [MEDIUM] P1-005 – Phần bổ sung đạt về cấu trúc hồ sơ; chờ xác minh hoặc Owner chấp nhận giới hạn nguồn
- Vị trí: `docs/testing/phase1-tools-candidates.md:125`, `:172–182`, `:194`.
- Tiến bộ được xác nhận: đã chỉ rõ license tại tag LAME 4.0 và x265 4.3 thay vì HEAD, có COPYING x264 tại commit, đọc thêm các điều khoản XZ; tách đúng suy luận khỏi bằng chứng và giữ trạng thái chờ. Không còn yêu cầu sửa nhãn hoặc vòng phụ thuộc.
- Còn thiếu cho kết luận độc lập: công cụ lượt này không đọc được hai URL LAME tại tag và header x265 mà Claude dẫn; nguồn mirror x264 chưa có đối chiếu upstream ngoài metadata/commit đã ghi. Vì thế reviewer chưa thể xác nhận toàn bộ phần bằng chứng đúng artifact. Đây không phải bằng chứng nguồn sai hoặc license cấm thương mại.
- Điều kiện để đóng: bổ sung đối chiếu đọc được về phần còn thiếu, hoặc **Owner quyết định riêng** chấp nhận chính các giới hạn nguồn/khả năng xác minh này. Không tự suy phê duyệt đó từ việc Owner đã cho B có điều kiện. Reviewer không phát hành “PASS có điều kiện” để bỏ qua điều kiện đầu vào còn mở.
- Không đặt thêm điều kiện tùy tiện: repo x265 4.3 trùng repo/tổ chức trong URL artifact của formula là bằng chứng liên quan trực tiếp; **không cần** một câu tự nhận “kho chính thức” riêng mới được nghiên cứu hoặc đối chiếu. Dav1d dưới tổ chức videolan tự nêu upstream là bằng chứng hỗ trợ nguồn gốc, không mặc định xếp là không chính thức. Không bắt buộc tải artifact hoặc đối chiếu từng byte trước review; đó là kiểm tra sau quyền tải.
- Trong phạm vi SG: có. Không có finding mới; P1-005 còn OPEN do giới hạn bằng chứng, không phải vì thiếu câu tuyên bố pháp lý hoặc chưa giải quyết toàn bộ sáng chế.

## Đã tự xác minh

### Toàn vẹn mục 7 – PASS
- SG-004 ACTIVE, có lời Owner và A01; RR-011 ANSWERED, RR-012 mới nhất và duy nhất OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã. Vòng 0 → 1/3 đúng.
- HEAD/nhánh đúng baseline. Working tree đầu lượt gồm CURRENT_STATUS, HANDOFF, REVIEW_RESPONSE, TASKS, reviewer artifact và file mới phase1-tools-candidates; mọi đường dẫn A/B, không nhóm C.
- Năm hash A khớp RR-012; TASKS chỉ băm phần trước `## Review Requests`. CURRENT_STATUS giữ hash A01 `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`, chỉ đọc.
- Reviewer artifact: 86,194 byte, SHA-256 `5aa9ba5c7d85f187d03cc294abb834a087f28cd58f4fa9b94e2343505701798f`. Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp.
- SG-004 tiếp tục theo chỉ đạo Owner đã ghi nhận RR-011; lịch sử SG-003 không reset, không tự quyết trạng thái SG-003.

### Đối chiếu bổ sung – truy cập 2026-10-31
- [x265 COPYING tại 4.3](https://raw.githubusercontent.com/Multicorewareinc/x265/4.3/COPYING) đọc được, là GPLv2. [Header cùng tag](https://raw.githubusercontent.com/Multicorewareinc/x265/4.3/source/x265.cpp) trả Cache miss; chưa xác nhận độc lập câu “or later” và câu thương mại trong header tại 4.3. Việc công cụ không truy cập được không bác bỏ lời Claude đã đọc. Thiếu đối chiếu tarball không tự tạo blocker mới trước quyền tải.
- [x264 COPYING tại commit b35605ac…](https://raw.githubusercontent.com/mirror/x264/b35605ace3ddf7c1a5d67a2eb553f034aef41d55/COPYING) nay đọc được, là GPLv2. Điểm “COPYING tại commit chưa đọc” của RR-011 đã có bằng chứng bổ sung; phần còn lại là quan hệ nguồn mirror và grant/header, không phải chưa ghim COPYING.
- [Trang dav1d GitHub](https://github.com/videolan/dav1d) xác nhận tự mô tả read-only mirror, dẫn origin code.videolan.org. Kết hợp COPYING tại tag đã đọc ở RR-011, không có cơ sở nói nguồn chắc chắn giả/không chính thức. Đối chiếu tarball và nguồn gốc đầy đủ vẫn chưa làm; Owner có thể chấp nhận giới hạn mà không bắt buộc tải.
- [LAME COPYING tại RELEASE__4_0](https://sourceforge.net/p/lame/svn/HEAD/tree/tags/RELEASE__4_0/COPYING?format=raw) và [lame.c cùng tag](https://sourceforge.net/p/lame/svn/HEAD/tree/tags/RELEASE__4_0/libmp3lame/lame.c?format=raw) không truy cập được qua công cụ. Tên đường dẫn đã chuyển từ trunk sang tag đúng như hồ sơ; nội dung, revision r6552 và ngày tag vẫn là Claude báo cáo, chưa được tôi xác nhận độc lập. Không gọi SVN tag dưới URL HEAD là trunk: HEAD ở đây chọn revision kho, còn đường dẫn đang là tags/RELEASE__4_0.
- [XZ COPYING.0BSD tại v5.8.4](https://raw.githubusercontent.com/tukaani-project/xz/v5.8.4/COPYING.0BSD) và [COPYING.LGPLv2.1](https://raw.githubusercontent.com/tukaani-project/xz/v5.8.4/COPYING.LGPLv2.1) đọc được, khớp loại điều khoản ghi. [COPYING.GPLv2](https://raw.githubusercontent.com/tukaani-project/xz/v5.8.4/COPYING.GPLv2) trả Cache miss. Không lấy COPYING.GPLv3 của build system làm blocker riêng cho license liblzma runtime khi bảng chỉ dẫn đã phân biệt và không có bằng chứng mới cho thấy nó áp dụng cho binary đó.
- Dòng suy luận 186 đã đồng bộ LAME tại tag, x265 tại tag, x264 tại commit. Các nguồn tag khác/SVT-AV1 không thay trong phạm vi sửa và đã đối chiếu RR-011; không tra cứu lại chỉ để lặp xác minh.

### Hồi quy
- P1-006 CLOSED: Codex PASS và hồ sơ lệnh vẫn đi trước quyết định riêng Owner, không biến B có điều kiện thành quyền cài/chạy.
- P1-007 CLOSED: bốn tầng giữ thứ tự. Hash nguồn công bố khác hash thực nhận; không yêu cầu tải trước quyền tải hoặc có quyết định cuối để xin chính quyết định đó.
- Hồ sơ không ghi (i)–(iii) hoàn tất, không tự đóng P1-005, không kết luận miễn nghĩa vụ GPL/sáng chế. Phân loại đã xác minh/suy luận/rủi ro nhìn chung trung thực; “đã đọc” của Claude được phân biệt với những nguồn Codex tự đọc được.

## Chưa thể xác minh và phần còn có thể làm
- Claude có thể tiếp tục **nghiên cứu tài liệu** trong SG: tìm URL đọc được của LAME tại cùng tag/revision; dẫn header/grant x265 tại tag hoặc commit phát hành; nguồn công khai liên hệ mirror x264 với upstream. Không khẳng định chỉ Owner mới có thể bổ sung các bằng chứng này. Không vượt bot-protection, liên hệ tác giả hoặc tải tarball khi chưa có quyền.
- Nếu không có nguồn đọc được trong quyền hiện tại, lựa chọn chấp nhận mirror/giới hạn xác minh, cho tải chỉ để kiểm tra hoặc dừng là **quyết định Owner**. Đây là điều kiện cần tách khỏi việc sửa tài liệu; không cần tiếp tục lặp RR chỉ để nói lại cùng giới hạn.
- Chưa kiểm tra tarball/bottle, toàn closure/notice, tương thích pháp lý cuối cùng, sáng chế, binary hoặc VideoToolbox. Không tải, cài, chạy, render/benchmark, truy cập Git remote, commit/push hoặc sửa index.
- Không phê duyệt FFmpeg nhóm B chính thức, cài/chạy, Phase Gate hay đóng SG; hash không xác minh nguồn gốc lời Owner.

## Bàn giao
- **NEXT ACTOR: Claude** – phản hồi báo cáo và trình Owner rõ phần điều kiện P1-005 còn lại. **NEXT DECISION: Project Owner** nếu chọn chấp nhận mức bằng chứng hoặc cấp quyền ngoài SG; APPROVED WITH CHANGES không phải PASS để sang cài.
- Nếu có bằng chứng/sửa đổi mới và tiếp tục review theo SG, vòng kế là **2/3**. P1-005 chưa CLOSED; P1-006/P1-007 vẫn CLOSED.
- Chỉ thêm báo cáo này ở đầu reviewer artifact; bảo toàn 86,194 byte lịch sử.

---

# Review RR-011
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-004, Amendment A01 | Vòng: 0/3.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh main; snapshot SHA-256 trong RR-011.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION**. Integrity PASS; P1-005 còn OPEN, có bằng chứng bổ sung đáng kể. P1-006/P1-007 vẫn CLOSED, không có hồi quy cần mở lại.
- Phạm vi: P1-005 và hồi quy P1-006/P1-007 tại mục 8.1, 8.3 của `docs/testing/phase1-tools-candidates.md`; tham chiếu lịch sử để đối chiếu. Không review công cụ khác, runtime hoặc quyết định cài.

## Phát hiện

### [MEDIUM] P1-005 – PARTIALLY FIXED, OPEN: chưa hoàn tất bằng chứng đúng artifact cho phần còn lại
- Vị trí: `docs/testing/phase1-tools-candidates.md:125`, `:172–182`, `:194`.
- Phần đạt: mục 8.3 ghim nguồn theo tag/commit, ghi rõ nguồn chính thức/mirror/HEAD, có nguồn LAME chính thức ở mức thông tin chung và tách suy luận khỏi sự kiện. SVT-AV1 đã đối chiếu đúng v4.2.0; không còn thiếu bước xác định chênh lệch có phải do khác phiên bản hay không. Không yêu cầu Claude phải giải thích động cơ của người ghi metadata Homebrew để ghi nhận license upstream.
- Phần còn thiếu: LAME chỉ có grant/header được Claude báo cáo tại SVN HEAD, chưa gắn 4.0; x265 chưa có license/header tại nguồn release 4.3; dav1d/x264 chưa có đối chiếu nguồn gốc mirror theo mức bằng chứng hồ sơ đang áp dụng; x264 COPYING tại đúng commit chưa được đọc. XZ tại tag đã đọc bảng chỉ dẫn, nhưng còn thiếu văn bản điều khoản được dẫn chiếu cho phần áp dụng.
- Bằng chứng: chính bảng B/C và kết luận dòng 194 nêu các giới hạn này và giữ (i)–(iii) chưa hoàn tất. RR-011 không có quyết định riêng của Owner chấp nhận mức bằng chứng thay thế. Công khai thiếu sót là đúng nhưng chưa làm tầng 1.1 đủ điều kiện PASS theo hồ sơ hiện hành.
- Tình huống gây lỗi: PASS bị dùng làm cổng sang đề xuất cài tập phiên bản đã định danh, dù license đang đối chiếu vẫn có phần thuộc HEAD, mirror chưa kiểm chứng hoặc phiên bản khác.
- Khuyến nghị trong quyền nghiên cứu: tìm tệp LICENSE/COPYING/header trên kho phát hành chính thức của **x265 4.3** (ưu tiên đúng Multicorewareinc đã được formula dẫn thay vì chỉ mirror cũ); tìm tag hoặc revision SVN tương ứng **LAME 4.0**; đọc COPYING tại commit x264 đã ghi và đối chiếu nguồn gốc mirror bằng thông tin công khai; đọc các tệp license XZ áp dụng tại v5.8.4. Không tải tarball, không vượt bot-protection, không liên hệ tác giả từ finding này.
- Khi cần Owner: nếu nguồn không tiếp cận được hoặc chỉ có mirror/HEAD, trình Owner quyết định rõ mức bằng chứng được chấp nhận; hoặc xin quyền riêng tải artifact chỉ để đọc/kiểm tra nếu Owner chọn cách đó. Không coi đây là điều kiện bắt buộc phải tải. Không có bằng chứng hiện tại để reviewer quyết rằng bắt buộc mua giấy phép hay phải có kết luận pháp lý toàn hệ thống.
- Trong phạm vi SG: có. Không nâng chênh lệch metadata hay lỗi truy cập thành kết luận phần mềm không được phép thương mại; nhãn B có điều kiện do Owner cho đánh giá vẫn giữ nguyên.

## Đã tự xác minh

### Toàn vẹn và tính hợp lệ bàn giao – PASS
1. SG-004 ACTIVE, có lời Owner cho mở SG xử lý P1-005 và tối đa ba vòng mới; A01 xác nhận allowlist. RR-011 mới nhất, duy nhất OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã. Vòng đầu 0/3 hợp lệ.
2. Ghi nhận minh bạch: SG-003 đã dùng hết vòng 0–3 nhưng vẫn ghi ACTIVE vì Owner chưa quyết trạng thái. Quyền tiếp tục lần này xuất phát từ **chỉ đạo trực tiếp của Owner trong SG-004**, không từ Claude tự đổi tên SG. Workflow cho Owner quyết định tiếp tục sau hết vòng; không coi việc này tự động vi phạm quy tắc cấm Claude reset. Không sửa/xóa lịch sử SG-003, không tự đóng SG-003 hoặc diễn giải ACTIVE thành được tiếp tục vòng cũ.
3. HEAD/nhánh đúng baseline. Working tree đầu lượt gồm CURRENT_STATUS, HANDOFF, REVIEW_RESPONSE, TASKS, reviewer artifact và file mới phase1-tools-candidates; không đường dẫn nhóm C.
4. Năm hash nhóm A khớp RR-011; TASKS chỉ băm phần trước `## Review Requests`. CURRENT_STATUS đúng A01 chỉ đọc: `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`.
5. Reviewer artifact: 76,078 byte, SHA-256 `1619658ed3513eff6d6ce3169e81f63728c9d0efc3c75304f9789c11e24435b6`. Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp bàn giao.

### Nguồn 8.3 – truy cập 2026-10-31
- Đọc được nguồn tại tag mà Claude ghi: [libvmaf v3.2.1](https://raw.githubusercontent.com/Netflix/vmaf/v3.2.1/LICENSE), [libvpx v1.17.0](https://raw.githubusercontent.com/webmproject/libvpx/v1.17.0/LICENSE), [Opus v1.6.1](https://raw.githubusercontent.com/xiph/opus/v1.6.1/COPYING), [OpenSSL 4.1.0](https://raw.githubusercontent.com/openssl/openssl/openssl-4.1.0/LICENSE.txt), [XZ v5.8.4](https://raw.githubusercontent.com/tukaani-project/xz/v5.8.4/COPYING), [SDL2-compat release-2.32.74](https://raw.githubusercontent.com/libsdl-org/sdl2-compat/release-2.32.74/LICENSE.txt). Nội dung loại license tương ứng khớp mô tả; XZ đúng là bảng phân loại và dẫn tới các tệp COPYING khác. Đọc đúng tag không đồng nghĩa đã kiểm tra nội dung tarball/bottle thực nhận.
- [SVT-AV1 LICENSE tại v4.2.0](https://gitlab.com/AOMediaCodec/SVT-AV1/-/raw/v4.2.0/LICENSE.md) là Clear BSD và loại trừ cấp quyền sáng chế trong chính tệp đó; [PATENTS.md cùng tag](https://gitlab.com/AOMediaCodec/SVT-AV1/-/raw/v4.2.0/PATENTS.md) có grant AOM riêng theo Necessary Claims và điều kiện. Đủ xác nhận chênh với metadata BSD-3-Clause đã được đối chiếu ở vòng trước **không chỉ do đọc nhánh mặc định khác phiên bản**. Nguyên nhân metadata ghi như vậy vẫn chưa biết; hồ sơ đánh dấu suy luận là đúng. Grant riêng không chứng minh quyền sáng chế không giới hạn.
- [dav1d COPYING tại 1.5.4 trên GitHub](https://raw.githubusercontent.com/videolan/dav1d/1.5.4/COPYING) đọc được, khớp BSD hai điều kiện. Chưa xác minh liên kết tổ chức/mirror với nguồn tarball Homebrew; không khẳng định GitHub chắc chắn không chính thức chỉ từ việc repo khác hostname.
- [Trang LAME chính thức](https://lame.sourceforge.io/about.php) xác nhận mô tả dự án là fully LGPL'd, nhưng không xác nhận grant cụ thể tại release 4.0. Hai URL SVN HEAD được Claude dẫn không truy cập được qua công cụ lượt này; không xác nhận độc lập header/COPYING ở đó. [x264 header tại commit đã ghi](https://raw.githubusercontent.com/mirror/x264/b35605ace3ddf7c1a5d67a2eb553f034aef41d55/x264.c) trả Cache miss; không coi lỗi truy cập là bằng chứng Claude mô tả sai.

### Phân loại bằng chứng và hồi quy
- Phân nhóm A/B/C/D/E nhìn chung đúng mức: tag chính thức, mirror/HEAD có giới hạn, chưa đọc được, suy luận, rủi ro. Một tag hoặc commit đã ghi là sự kiện khác với việc đủ bằng chứng nguồn gốc/điều khoản cho artifact; hồ sơ không tự đánh dấu đủ quyền.
- Dòng 186 nói header x264 ở HEAD/nhánh mặc định là mô tả chưa chính xác với dòng 173 ghi commit cụ thể. Đọc cùng bảng B vẫn thấy giới hạn thật là nguồn mirror và COPYING tại commit, không phải chưa ghim header. Đây là ghi chú cần đồng bộ khi sửa P1-005, không mở finding riêng hoặc phủ nhận commit đã được khai báo.
- P1-006 vẫn CLOSED: cổng Codex PASS và quyết định riêng của Owner không bị thay bởi nhãn B có điều kiện. P1-007 vẫn CLOSED: bốn tầng giữ thứ tự, hash thực nhận sau quyền tải và trước sử dụng; không tái tạo vòng phải tải hoặc được phê duyệt trước để xin chính quyền đó.

## Chưa thể xác minh
- LAME 4.0, x265 4.3, nguồn mirror chính thức dav1d/x264 và văn bản đầy đủ áp dụng cho mọi phần còn thiếu; các mục này vẫn chưa đủ để đóng P1-005. Tính đầy đủ của nguồn không được chứng minh chỉ bằng báo cáo Claude hay hash.
- Không tải tarball/bottle/model, cài, chạy, benchmark/render, vượt bot-protection, liên hệ bên ngoài, truy cập Git remote, commit/push hoặc sửa index. Chưa kiểm tra hash thực nhận, binary, notice, toàn closure, VideoToolbox hoặc hiệu năng.
- Không xác nhận pháp lý cuối cùng/đầy đủ quyền sáng chế. Không mở rộng review công cụ khác hay tự quyết trạng thái SG-003/SG-004; không thay Phase Gate. Hash không xác thực người viết hoặc lời Owner gốc.

## Bàn giao
- **NEXT ACTOR: Claude** – phản hồi P1-005, bổ sung tài liệu trong allowlist hoặc trình Owner nếu cần chấp nhận mức bằng chứng/nguồn thay thế hay quyền ngoài phạm vi. Nếu có sửa và review tiếp, vòng kế là **1/3 của SG-004**.
- P1-005 OPEN; P1-006/P1-007 vẫn CLOSED. Không PASS cho hồ sơ hiện tại; không có quyền tải/cài/chạy từ báo cáo.
- Chỉ thêm báo cáo này vào đầu reviewer artifact; giữ nguyên 76,078 byte lịch sử.

---

# Review RR-010
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-003, Amendment A01 | Vòng: **3/3, cuối** | Tiếp nối RR-009.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh `main`; snapshot SHA-256 trong RR-010.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION**. Integrity PASS. P1-005 vẫn OPEN; P1-006/P1-007 vẫn CLOSED. Hết vòng: dừng và trình Owner, không mở vòng 4.
- Phạm vi: P1-005 và hồ sơ FFmpeg tại mục 1, 2, 8, 8.1, 8.2. Không review công cụ khác, SG-002, hiệu năng hoặc quyết định cài.

## Phát hiện

### [MEDIUM] P1-005 – Có tiến bộ về nguồn license, nhưng chưa đủ đóng tầng 1.1 cho artifact đã định danh
- Vị trí: `docs/testing/phase1-tools-candidates.md:125`, `:134`, `:139`, `:143`, `:150`.
- Đã xác minh phần sửa: 8.2 bổ sung liên kết, mô tả license/header/PATENTS cho 11 phụ thuộc; công khai nhánh mặc định, thiếu ghim phiên bản, nguồn LAME không chính thức và lệch SVT-AV1. Không còn lỗi đồng nhất nhãn Owner cho đánh giá với B hoàn tất bằng chứng. Nhãn B có điều kiện của Owner vẫn được giữ.
- Phần còn thiếu cụ thể: (1) chưa gắn các văn bản đọc được với đúng phiên bản hoặc commit của 11 phụ thuộc mà Homebrew liệt kê; (2) LAME 4.0 chưa có nguồn chính thức xác nhận grant và “or later”, hiện chỉ là bản sao không chính thức; (3) SVT-AV1 ghi BSD-3-Clause ở metadata nhưng nguồn nhánh hiện tại là BSD-3-Clause-Clear, chưa đối chiếu LICENSE/PATENTS tại v4.2.0 để biết có phải khác phiên bản hay metadata thiếu. Những thiếu sót này liên quan trực tiếp điều kiện đọc license đúng artifact, không phải yêu cầu phải tải hoặc chạy trước review.
- Bằng chứng: dòng 134 và 150 tự xác nhận các giới hạn trên; RR-010 xác nhận không có quyết định riêng của Owner về mức bằng chứng thay thế. Việc đọc tài liệu nhánh mặc định giúp nghiên cứu nhưng chưa chứng minh điều khoản áp dụng cho đúng phiên bản dự kiến cài. Không thể coi tầng 1.1 hoàn tất chỉ vì đã có một tệp cho mỗi tên gói.
- Tình huống gây lỗi: PASS có thể được dùng như cổng chuyển sang xin cài đúng tập artifact, trong khi nguồn license đối chiếu thuộc tập phiên bản chưa xác định; chênh lệch hoặc bản sao chưa kiểm chứng bị chuyển thành rủi ro đã chấp nhận mà không có quyết định tương ứng.
- Hướng xử lý trình Owner: Claude có thể bổ sung bằng chứng chỉ đọc tại tag/commit đúng và nguồn LAME chính thức, giải thích chênh SVT-AV1; nhưng **sau vòng này không tự tiếp tục chu trình sửa/re-review**. Owner quyết định có cho tiếp tục hay chấp nhận riêng mức bằng chứng giới hạn. Không suy quyết định đó từ nhãn B có điều kiện trước đây.
- Trong phạm vi SG: có. Không yêu cầu xóa rủi ro sáng chế, có ý kiến luật sư, đọc mọi license không liên quan hoặc tải binary để đóng finding này. Thiếu notice/binary là giới hạn giai đoạn sau; không dùng chúng tạo điều kiện phải có trước khi được phép tải.

## Đã tự xác minh

### Toàn vẹn mục 7 – PASS
- Đúng lượt: RR-010 mới nhất, duy nhất OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã. SG-003 ACTIVE, có lời Owner và A01. RR-009 ANSWERED; chuỗi 0/1/2/3 liên tục, không vượt giới hạn.
- HEAD và nhánh đúng baseline. Working tree đầu lượt: CURRENT_STATUS, HANDOFF, REVIEW_RESPONSE, TASKS, reviewer artifact và file mới phase1-tools-candidates; không có đường dẫn nhóm C.
- Cả năm hash A khớp RR-010; TASKS băm phần trước `## Review Requests`. CURRENT_STATUS giữ đúng A01 chỉ đọc: `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`.
- Reviewer artifact: 66,483 byte, SHA-256 `b0ff9d93023032ccf30316ce3b2027e98602e8232818085c1a5fb28dc5b80e67`. Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp bàn giao.

### Đối chiếu nguồn 8.2 – truy cập 2026-10-31
- [SVT-AV1 LICENSE.md](https://gitlab.com/AOMediaCodec/SVT-AV1/-/raw/master/LICENSE.md) đúng là Clear BSD và loại trừ cấp quyền sáng chế trong chính tệp đó. [PATENTS.md](https://gitlab.com/AOMediaCodec/SVT-AV1/-/raw/master/PATENTS.md) có grant AOM riêng, phạm vi Necessary Claims cùng điều kiện. Không coi đây là bằng chứng không cần xử lý sáng chế. Việc hồ sơ ghi có chênh metadata là đúng; gọi “nhỏ” không chứng minh tác động nhỏ. Chưa đối chiếu v4.2.0.
- [x265 header](https://raw.githubusercontent.com/videolan/x265/master/source/x265.cpp) xác nhận GPL v2 hoặc mới hơn và tùy chọn thương mại riêng; [COPYING](https://raw.githubusercontent.com/videolan/x265/master/COPYING) là GPLv2. Có tùy chọn thương mại không tự làm nhánh GPL không dùng được cho thương mại; hồ sơ không được suy bắt buộc mua license. Chưa gắn nguồn này với artifact x265 4.3.
- [XZ COPYING](https://raw.githubusercontent.com/tukaani-project/xz/master/COPYING) hỗ trợ cách tách liblzma 0BSD, script GPLv2+, getopt_long LGPLv2.1+ và license build system. Đây là **bảng chỉ dẫn license**, còn dẫn tới COPYING.0BSD/COPYING.LGPLv2.1/COPYING.GPLv2/COPYING.GPLv3; đọc chỉ bảng này chưa đồng nghĩa đọc đầy đủ mọi điều khoản được dẫn chiếu. Không xác nhận từ nguồn này thành phần thực tế đã liên kết trong bottle chưa tải.
- [LAME mirror](https://raw.githubusercontent.com/gypified/libmp3lame/master/COPYING) không truy cập được qua công cụ (Cache miss). Không xác nhận độc lập bản tóm tắt của Claude, cũng không coi lỗi truy cập là bằng chứng tác giả sai. Giới hạn nguồn không chính thức đã được ghi trung thực.
- Các tệp nhánh mặc định đọc được phù hợp mô tả loại license: [dav1d](https://raw.githubusercontent.com/videolan/dav1d/master/COPYING) BSD hai điều kiện; [libvmaf](https://raw.githubusercontent.com/Netflix/vmaf/master/LICENSE) BSD-2-Clause-Patent; [libvpx LICENSE](https://raw.githubusercontent.com/webmproject/libvpx/main/LICENSE) và [PATENTS](https://raw.githubusercontent.com/webmproject/libvpx/main/PATENTS); [Opus](https://raw.githubusercontent.com/xiph/opus/main/COPYING); [x264 header](https://raw.githubusercontent.com/mirror/x264/master/x264.c) GPLv2-or-later; [OpenSSL](https://raw.githubusercontent.com/openssl/openssl/master/LICENSE.txt) Apache-2.0; [sdl2-compat](https://raw.githubusercontent.com/libsdl-org/sdl2-compat/main/LICENSE.txt) zlib. Đối chiếu này không xác nhận đúng release Homebrew hoặc toàn bộ chuỗi quyền.

### Hồi quy
- Mục 8 vẫn phân biệt B có điều kiện với (i)–(iii) chưa hoàn tất. Mục 1/8.1 còn một số câu lịch sử “mới đọc metadata”/“chưa đọc toàn văn”; 8.2 công khai chính xác giới hạn của phần đọc thêm. Không mở finding mới chỉ để dọn các câu cũ; chúng không giải quyết phần thiếu P1-005.
- P1-006/P1-007 không tái xuất hiện: chuỗi bằng chứng tài liệu → Codex PASS → hồ sơ lệnh → Owner cấp quyền riêng → kiểm tra sau tải vẫn tách biệt. Hash thực nhận không trở lại thành điều kiện phải có trước quyền tải.
- Không thấy tuyên bố (i)–(iii) đã đạt, rủi ro sáng chế đã hết, VideoToolbox đã chạy hoặc có quyền cài/chạy trong phần thay đổi. Nội dung sáu giới hạn ở dòng 150 không bị biến thành kết quả PASS.

## Chưa thể xác minh
- License tại đúng release/commit của các phụ thuộc, nguồn LAME chính thức, nguyên nhân lệch SVT-AV1; toàn văn mọi điều khoản/notice và phụ thuộc gián tiếp. Không xác nhận tương thích pháp lý cuối cùng hoặc đầy đủ quyền sáng chế từ việc đọc tên license.
- Không tải tarball/bottle/model, so hash tệp thực nhận, cài/chạy FFmpeg, benchmark/render, kết nối Git remote, commit/push hoặc sửa index. Chưa xác minh binary, tổng dung lượng, VideoToolbox hoặc hiệu năng.
- Trang legal chưa được xác minh độc lập ở các lượt trước; không dùng nó làm bằng chứng mới. Hash không xác minh tác giả hoặc nguồn lời Owner.
- Không review công cụ khác, không đóng findings SG-002, không sửa CURRENT_STATUS hoặc thay quyết định/Phase Gate.

## Bàn giao cuối SG-003
- **NEXT ACTOR: Project Owner** – đã hết vòng 3/3 mà chưa PASS. Claude chỉ phản hồi/tóm tắt báo cáo để Owner quyết định, không tự mở vòng 4, gia hạn, đổi SG để reset hoặc tiếp tục sửa theo vòng lặp.
- Owner quyết định bước tiếp theo và mức bằng chứng chấp nhận; reviewer không tự nghiệm thu, đóng SG hay cho phép cài. P1-005 vẫn OPEN; P1-006/P1-007 vẫn CLOSED.
- Chỉ thêm báo cáo này ở đầu reviewer artifact; bảo toàn 66,483 byte lịch sử.

---

# Review RR-009
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-003, Amendment A01 | Vòng: 2/3 | Tiếp nối RR-008.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh `main`; snapshot SHA-256 trong RR-009.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION**. Các lỗi diễn đạt đã sửa; chưa thể PASS hồ sơ theo điều kiện bằng chứng mà chính hồ sơ còn ghi chưa hoàn tất.
- Phạm vi: P1-005, P1-007 và hồi quy FFmpeg tại mục 1, 2, 8, 8.1. Không mở review công cụ khác, SG-002, hiệu năng hoặc quyết định cài.

## Phát hiện và kết luận từng finding

### [MEDIUM] P1-005 – Phần đồng bộ đã đạt; phần bằng chứng license vẫn OPEN
- Vị trí: `docs/testing/phase1-tools-candidates.md:18`, `:96`, `:110`, `:117`, `:125`, `:130`.
- Đã sửa và tự xác minh: dòng FFmpeg mục 8 nay ghi GPLv3 đã đọc, phụ thuộc chỉ có metadata, (i)–(iii) chưa được xác nhận hoàn tất; nhãn B có điều kiện khớp mục 1 và 8.1. Cách ghi cũ được đánh dấu lỗi thời. Phần mâu thuẫn đã nêu riêng ở RR-008 đã được giải quyết.
- Còn thiếu: tầng 1.1 yêu cầu đọc toàn văn license phụ thuộc runtime **hoặc** có quyết định riêng của Owner chấp nhận metadata là đủ để vào review; trạng thái ghi “1.1 chưa xong”. Dòng 130 đặt tầng 1 là điều kiện cần trước Codex PASS. RR-009 không bổ sung toàn văn hoặc quyết định riêng đó; RR còn xác nhận chưa đọc toàn văn từng phụ thuộc. Vì vậy chưa có bằng chứng để cho PASS theo cổng hiện hành.
- Tình huống gây lỗi: PASS cho nhãn B có điều kiện lúc này có thể được dùng làm bước (b) ở dòng 103 dù bước (a) chưa hoàn tất. Ghi nhận trung thực thiếu sót không đồng nghĩa thiếu sót đã được giải quyết.
- Yêu cầu tiếp theo: hoàn tất phần đọc/đối chiếu license cần thiết theo tầng 1.1 trong quyền nghiên cứu hiện có, hoặc trình Owner quyết định riêng về mức bằng chứng được chấp nhận. Không suy quyết định đó từ lời Owner đã cho tiếp tục đánh giá B có điều kiện; không yêu cầu phải tải binary hay giải quyết hết sáng chế để sửa tài liệu.
- Trong phạm vi SG: có. Đây là phần thiếu bằng chứng đã nêu từ P1-005/RR-007 và được hồ sơ giữ thành cổng ở tầng 1.1, không phải một yêu cầu tải hoặc benchmark mới. **Không đóng P1-005 chỉ vì đã sửa nhãn.** Không thu hồi quyết định B có điều kiện của Owner.

### P1-007 – CLOSED (Codex xác minh)
- Vị trí: `docs/testing/phase1-tools-candidates.md:103`, `:121–130`.
- Chuỗi mới tách: bằng chứng tài liệu → Codex PASS và hồ sơ lệnh → Owner cấp quyền riêng → so hash tệp thực nhận trước sử dụng. Quyết định Owner và hash sau tải không còn là điều kiện phải có để xin chính quyết định đó.
- Tải chỉ để kiểm tra digest cũng cần quyết định riêng; hash công bố trong formula được phân biệt với hash thực nhận. Tầng 4 không chặn review hay xin quyền. Đã loại vòng phụ thuộc mà P1-007 mô tả.
- Tầng 1 đủ là **nhóm điều kiện đầu vào** cho review trong phạm vi hiện hành; nhưng “đủ để định nghĩa thứ tự” khác “đã hoàn tất”. Việc 1.1 chưa xong không làm vòng phụ thuộc quay lại, chỉ giữ cổng bằng chứng còn mở.

### Hồi quy P1-006
- Vẫn CLOSED theo RR-008: dòng 103 giữ Codex PASS, hồ sơ lệnh và quyết định riêng của Owner; không coi B có điều kiện là quyền tải/cài/chạy. Không phát hiện finding mới cần mở trong phần thay đổi được kiểm tra.

## Đã tự xác minh

### Toàn vẹn mục 7 – PASS
1. Đọc workflow, SG-003, xác nhận Owner và Amendment A01. SG ACTIVE; RR-009 là RR mới nhất và duy nhất OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã trước lượt này. RR-008 ANSWERED; vòng 0 → 1 → 2/3 liên tục.
2. HEAD `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh main, đúng baseline.
3. Năm hash nhóm A khớp RR: HANDOFF, hồ sơ tools, REVIEW_RESPONSE, TASKS phần trước `## Review Requests`, CURRENT_STATUS. Hash CURRENT_STATUS vẫn `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`, đúng A01 chỉ đọc.
4. Working tree đầu lượt gồm CURRENT_STATUS, HANDOFF, REVIEW_RESPONSE, TASKS, reviewer artifact và file mới phase1-tools-candidates; đều A/B, không nhóm C.
5. Reviewer artifact 58,747 byte, SHA-256 `f657694c91dc4d3cb64d0af054dc966600e37611b410cbe6aaa60c825074e271`. Phase 0 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp bàn giao.

### Nội dung và giới hạn kết luận
- Đối chiếu trực tiếp dòng FFmpeg ở mục 1/2/8/8.1 và phản hồi RR-008: nhãn Owner cho tiếp tục đánh giá được giữ, không thành B hoàn tất bằng chứng hoặc kết luận thương mại cuối cùng.
- Mục 2 vẫn chứa thông tin lần đọc đầu về digest/COPYING; dòng 35 dẫn tới mục 8/8.1 cho trạng thái hiện hành, nơi ghi rõ hai digest công bố và GPLv3 đã đọc. Không dùng các ghi chú cũ đó để phủ nhận bằng chứng mới đã ghi hoặc mở finding mới về cùng lịch sử.
- Hai digest công bố, revision 1, cờ dựng và 11 cặp metadata license giữ nguyên so với RR-008, nơi Codex đã đối chiếu nguồn. Lượt này kiểm tra hồi quy tài liệu, không tra cứu lại hoặc tái xác nhận trạng thái nguồn từ xa. Không có thay đổi license/codec mới được đưa vào làm kết luận.
- Phân biệt dùng công cụ nội bộ với video kiếm tiền, GPL với sáng chế, cờ VideoToolbox với thực thi thực tế vẫn còn. Không thấy lời cấp quyền cài/chạy hoặc tuyên bố chất lượng/hiệu năng PASS trong phần được review.

## Chưa thể xác minh
- Chưa có toàn văn license từng phụ thuộc và notice áp dụng cho bản dựng, toàn closure, hay quyết định riêng được ghi rõ cho phép dùng metadata thay việc đọc đó. Không suy điều này từ việc Owner cho B có điều kiện.
- Không tải tarball/bottle, so hash thực nhận, cài, chạy FFmpeg, render/benchmark, kết nối Git remote, commit/push hoặc sửa index. Chưa xác minh runtime VideoToolbox, sáng chế hoặc quyền thương mại cuối cùng.
- Trang legal chưa được Codex xác nhận độc lập ở các vòng trước; lượt này không bổ sung xác minh web. Hash không xác minh tác giả hoặc nguồn gốc lời Owner.
- Không đánh giá nội dung cũ của CURRENT_STATUS thành finding SG-003; không đóng finding SG-002 hoặc mở review các công cụ ngoài FFmpeg.

## Bàn giao
- **NEXT ACTOR: Claude** – phản hồi phần P1-005 còn thiếu; tiếp tục đọc tài liệu trong allowlist nếu phù hợp, hoặc trình Owner quyết định riêng về mức bằng chứng. P1-007 CLOSED; P1-006 vẫn CLOSED.
- Nếu có bản sửa và tiếp tục review, lượt kế tiếp là **3/3**, không reset bộ đếm. Không tự đóng SG hoặc cấp quyền tải/cài.
- Chỉ thêm báo cáo này vào đầu reviewer artifact; giữ nguyên 58,747 byte lịch sử.

---

# Review RR-008
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-003, Amendment A01 | Vòng: 1/3 | Tiếp nối RR-007.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh `main`; snapshot SHA-256 trong RR-008.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION**. Integrity PASS; P1-005 chưa đóng, P1-006 CLOSED; có hồi quy mới P1-007 trong mục 8.1.
- Phạm vi: hai finding và phần FFmpeg tại mục 1, 2, 8, 8.1 của `docs/testing/phase1-tools-candidates.md`. Không review resvg/CairoSVG/faster-whisper, SG-002, quyền cài hoặc hiệu năng.

## Phát hiện và đối chiếu finding

### [MEDIUM] P1-005 – PARTIALLY FIXED, OPEN: bảng FFmpeg mục 8 vẫn mang kết luận cũ
- Vị trí: `docs/testing/phase1-tools-candidates.md:96`; đối chiếu `:18`, `:110`, `:114`.
- Bằng chứng: mục 1 và 8.1 đã phân biệt đúng B có điều kiện do Owner cho đánh giá với B hoàn tất bằng chứng. Tuy nhiên dòng FFmpeg mục 8 vẫn ghi “Đề xuất B, kèm rủi ro dư Owner phải chấp nhận riêng” và “Chưa đọc toàn văn GPLv3”, trong khi mục 8.1 ghi đã đọc COPYING.GPLv3. Mục 8 chưa được gắn nhãn lịch sử hay chỉ dẫn rõ rằng kết luận phân loại đã được mục 8.1 thay thế; nó còn là bảng kết quả đọc tiếp hiện hành.
- Tình huống gây lỗi: người dùng bảng mục 8 thay bảng mục 1 có thể hiểu đã đủ để đề xuất B chỉ cần chấp nhận rủi ro; các phần không thống nhất về GPL đã đọc hay chưa. Việc thêm bảng mới chưa loại hết cách hiểu đã nêu ở P1-005.
- Yêu cầu khắc phục: đồng bộ chính dòng FFmpeg tại mục 8 với nhãn B có điều kiện, trạng thái GPL đã đọc và giới hạn license phụ thuộc; hoặc đánh dấu rõ dòng này là lịch sử đã được thay thế. Tiếp tục công khai rằng metadata không thay toàn văn và điều kiện (i)–(iii) chưa được xác nhận hoàn tất. Không tự thay quyết định Owner.
- Trong phạm vi SG: có. Không yêu cầu phải tải binary để sửa mâu thuẫn tài liệu này.

### P1-006 – CLOSED (Codex xác minh)
- Vị trí: `docs/testing/phase1-tools-candidates.md:103`.
- Mục 8 điểm 1 đã ghi đủ chuỗi hoàn tất hồ sơ → **Codex PASS** → trình lệnh/phiên bản/revision/phụ thuộc/dung lượng/tác động → **Owner quyết định riêng**. Chấp nhận rủi ro hoặc nhãn B có điều kiện không được coi là quyền cài/chạy. Nội dung sửa đáp ứng finding P1-006; vấn đề phân tầng điều kiện mới bên dưới không phủ nhận việc đã bổ sung cổng PASS.

### [MEDIUM] P1-007 – Danh sách điều kiện mới tạo vòng phụ thuộc trước và sau cấp quyền
- Vị trí: `docs/testing/phase1-tools-candidates.md:103`, `:121–126`.
- Bằng chứng: bước (a) yêu cầu hoàn tất điều kiện mục 8.1 trước bước (b) Codex PASS và trước khi trình Owner ở (c)–(d). Nhưng danh sách 8.1 lại chứa chính Codex PASS và quyết định Owner sau hồ sơ lệnh; còn việc so hash sau tải cũng được ghi là điều kiện chặn bước xin cài. Hiện chưa có quyền tải. Đây là trộn điều kiện đầu vào hồ sơ với các bước tiếp theo và kiểm tra sau tải.
- Tình huống gây lỗi: theo thứ tự viết hiện tại, phải có quyết định cuối để hoàn tất hồ sơ dùng xin chính quyết định đó; hoặc phải tải trước khi được cấp quyền. Người thực hiện không thể hoàn tất checklist tuần tự trong quyền hiện có.
- Yêu cầu khắc phục: tách (1) bằng chứng tài liệu cần cho review, (2) Codex PASS và hồ sơ trình Owner, (3) quyền tải/cài riêng, (4) kiểm tra digest tệp sau tải được phép và trước sử dụng. Phân biệt hash nguồn đã công bố với hash tệp thực nhận. Nếu việc tải chỉ để kiểm tra cần xảy ra trước, phải trình Owner quyết định riêng, không suy quyền từ finding. Không yêu cầu tự tải hoặc nới tiêu chuẩn license.
- Trong phạm vi SG: có; phát sinh ở mục 8.1 mới sau RR-007.

## Đã tự xác minh

### Kiểm tra toàn vẹn mục 7 – PASS
- SG-003 ACTIVE, có lời Owner và A01. RR-007 ANSWERED, RR-008 là RR mới nhất và duy nhất OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã. Vòng 0 → 1/3 đúng, không reset.
- HEAD/nhánh khớp baseline. Working tree gồm CURRENT_STATUS, HANDOFF, REVIEW_RESPONSE, TASKS, reviewer artifact và file mới phase1-tools-candidates; mọi đường dẫn thuộc A/B, không có nhóm C.
- Năm hash A khớp RR-008. TASKS chỉ băm phần trước `## Review Requests`. CURRENT_STATUS vẫn đúng hash A01 `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961`, không sửa và không mở review nội dung cũ.
- Reviewer artifact: 49,442 byte, SHA-256 `e76679fbf6d7c7d99e7980dc7431b8fc3bada2cd01a898a17aa44b76fcdd8cd0`. Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp.

### Nguồn và hồi quy FFmpeg
- Đọc lại [formula FFmpeg](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/f/ffmpeg.rb) ngày 2026-10-31: 9.0.2 revision 1; hai hash tarball/bottle arm64_tahoe vẫn khớp mục 8. Cờ và phạm vi macOS không thay so với RR-007; đây là đối chiếu nguồn, không phải hash binary tải thực tế.
- [COPYING.GPLv3 tag n9.0.2](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/COPYING.GPLv3), mục 2, hỗ trợ việc phân biệt chạy chương trình, không chuyển giao và đầu ra tùy nội dung có phải covered work. Bản tóm tắt ở 8.1 không chứng minh miễn mọi nghĩa vụ; không tìm thấy kết luận mới rằng GPL hoặc sáng chế đã được giải quyết. Không cần so từng byte với một bản GPL khác mới có thể đọc và phân tích văn bản tại tag này.
- Mô tả OpenSSL ở 8.1 phản ánh đối chiếu RR-007: hướng dẫn LICENSE.md tổng quát cần đọc cùng kiểm tra phiên bản trong configure; không có cơ sở từ riêng tên OpenSSL để kết luận bản dựng bất hợp lệ. Chưa xác nhận license toàn chuỗi.
- Đối chiếu metadata phiên bản/license: [dav1d](https://formulae.brew.sh/api/formula/dav1d.json), [lame](https://formulae.brew.sh/api/formula/lame.json), [libvmaf](https://formulae.brew.sh/api/formula/libvmaf.json), [libvpx](https://formulae.brew.sh/api/formula/libvpx.json), [opus](https://formulae.brew.sh/api/formula/opus.json), [svt-av1](https://formulae.brew.sh/api/formula/svt-av1.json), [x264](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/x/x264.rb), [x265](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/x/x265.rb), [openssl@4](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/o/openssl@4.rb), [xz](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/x/xz.rb), [sdl2-compat](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/s/sdl2-compat.rb). Cả 11 cặp phiên bản/license ở dòng 117 khớp snapshot nguồn truy cập 2026-10-31. Đây chỉ là metadata formula, không phải toàn văn license hoặc toàn dependency closure.
- Hồ sơ nói rõ dùng công cụ nội bộ khác phát hành video kiếm tiền; có cờ VideoToolbox không chứng minh runtime hay quyền codec. Rủi ro license phụ thuộc, notice, sáng chế và binary thực tế vẫn công khai, không biến số đo thành PASS.

## Chưa thể xác minh
- Chưa đọc đầy đủ license từng phụ thuộc/notice trong tarball hoặc bottle; chưa tải hay kiểm tra hash tệp thực nhận; chưa xác minh toàn closure, tổng dung lượng cài hoặc điều kiện sáng chế. Chưa có cơ sở PASS cho “B đã đủ bằng chứng”. Owner cho đánh giá B có điều kiện vẫn được ghi nhận, không bị reviewer thu hồi.
- Trang legal đã timeout ở RR-007; lượt này không dùng trang đó làm bằng chứng mới để xác nhận nội dung đầu ra/sáng chế. Các giới hạn ở mục 2 và 8.1 được giữ; không kết luận pháp lý.
- Không tải binary/model, cài, chạy FFmpeg, benchmark, render, truy cập Git remote, commit/push hoặc thay index. Không kiểm chứng nguồn gốc lời Owner bằng hash.
- Các phần ngoài FFmpeg và P1-003/P1-004 không được đánh giá hoặc đóng trong lượt này.

## Bàn giao
- **NEXT ACTOR: Claude** – phản hồi P1-005 còn mở và P1-007 mới; sửa trong allowlist, lập snapshot/RR mới vòng 2/3 nếu tiếp tục. P1-006 CLOSED bởi báo cáo này.
- Chưa PASS cho hồ sơ hiện tại; không có quyền cài/chạy từ review. Owner vẫn giữ quyết định riêng, SG-003 chưa tự đóng.
- Chỉ thêm báo cáo này ở đầu file review; bảo toàn 49,442 byte lịch sử.

---

# Review RR-007
- Ngày: 2026-10-31 | Reviewer: Codex, Independent Reviewer.
- Scope Grant: SG-003, Amendment A01 | Vòng: 0/3.
- Baseline Git: `71155919602b38f2b23fc6a062608cefe33ad07f`, nhánh `main`; phiên bản review là snapshot SHA-256 trong RR-007.
- Kết luận: **CHANGES REQUESTED — NEEDS REVISION**. Đầu vào toàn vẹn hợp lệ; không phải BLOCKED.
- Phạm vi: FFmpeg 9.0.2 tại mục 2 và mục 8 của `docs/testing/phase1-tools-candidates.md`, cùng nguồn và điều kiện liên quan. Không review các công cụ còn lại, finding SG-002, hiệu năng hoặc quyết định có nên cài.

## Phát hiện

### [MEDIUM] P1-005 – Chưa phân biệt B có điều kiện do Owner cho đánh giá với việc đã đạt tiêu chuẩn bằng chứng
- Vị trí: `docs/testing/phase1-tools-candidates.md:96`, `:103`.
- Bằng chứng: dòng FFmpeg chuyển sang “Đề xuất B” sau khi đọc LICENSE.md nhưng đồng thời xác nhận chưa đọc GPLv3 và license từng phụ thuộc. RR-007 yêu cầu kiểm tra ba tiêu chí, trong đó (i) là đọc toàn văn LICENSE của đúng artifact/runtime. LICENSE.md ở tag n9.0.2 là hướng dẫn xác định license và dẫn tới COPYING.GPLv3 để biết điều khoản thực tế; không thay toàn văn GPLv3. Danh sách phụ thuộc chưa đọc cũng chưa đủ để khẳng định không có bằng chứng trái ngược trong toàn bộ chuỗi.
- Tình huống gây lỗi: chấp nhận rủi ro dư được hiểu thành đã hoàn tất điều kiện (i), rồi hồ sơ trình xin cài dù chưa qua review đầy đủ như Owner yêu cầu. Việc ghi thiếu sót công khai là đúng, nhưng chưa giải quyết sự khác nhau giữa “đủ bằng chứng nhóm B” và “Owner cho tiếp tục đánh giá có điều kiện”.
- Yêu cầu khắc phục: giữ nguyên quyết định Owner cho B có điều kiện, chờ review; không coi reviewer đã xác nhận đạt (i)–(iii). Bổ sung đối chiếu COPYING.GPLv3, các thông báo áp dụng cho bản dựng và license phụ thuộc theo phiên bản liên quan; ghi rõ phần đã đọc, chưa đọc, điều kiện còn chặn PASS. Nếu tiếp tục dùng nhãn B có điều kiện, phân biệt nhãn này với B đã hoàn tất bằng chứng, thay vì dùng chấp nhận rủi ro để thay bước xác minh. Không tự thay quyết định của Owner hoặc mở rộng phạm vi.
- Trong phạm vi SG: có.

### [LOW] P1-006 – Điểm xin cài thiếu cổng Codex PASS đã được Owner đặt
- Vị trí: `docs/testing/phase1-tools-candidates.md:103`.
- Bằng chứng: câu hiện hành nói nếu Owner chấp nhận GPL/sáng chế thì Claude có thể xin quyền cài. Khối “SG-003 – Xác nhận của Owner” trong TASKS quy định trước khi cài phải có quyết định riêng **sau Codex PASS**, cùng hồ sơ lệnh/phiên bản/phụ thuộc/dung lượng/tác động. Mục 8 chưa mang điều kiện PASS vào điểm chuyển bước này.
- Tình huống gây lỗi: người tiếp nhận dùng câu ở mục 8 làm checklist, xem việc chấp nhận rủi ro là đủ để sang xin cài mặc dù review chưa PASS.
- Yêu cầu khắc phục: ghi rõ chuỗi: hoàn tất điều kiện hồ sơ → Codex PASS → trình Owner hồ sơ lệnh cụ thể → Owner quyết định riêng. Việc Owner cho B có điều kiện và việc xin review không phải quyền cài/chạy.
- Trong phạm vi SG: có. Không phát hiện câu nào trực tiếp cho phép tự chạy lệnh; đây là thiếu điều kiện bàn giao.

## Đã tự xác minh

### Kiểm tra toàn vẹn mục 7 – PASS
- Đúng lượt: RR-007 là RR mới nhất, OPEN, có END-OF-REVIEW-REQUEST; chưa có báo cáo cùng mã. SG-003 ACTIVE, có lời Owner trích và xác nhận phạm vi review; vòng đầu 0/3, không reset vòng SG-002.
- HEAD đúng baseline; working tree đầu lượt gồm `CURRENT_STATUS.md`, `HANDOFF_TO_CHATGPT.md`, `TASKS.md`, file mới `docs/testing/phase1-tools-candidates.md`. Không có đường dẫn nhóm C.
- Năm hash nhóm A khớp hoàn toàn: HANDOFF, hồ sơ tools, TASKS phần trước `## Review Requests`, REVIEW_RESPONSE và CURRENT_STATUS. Amendment A01 đưa CURRENT_STATUS vào A chỉ đọc; hash `962096ec5feeb910b5e3314062fdda46decdf86f22af289982e704cb7d3fb961` đúng. Không đánh giá nội dung cũ của file này thành finding SG-003.
- Reviewer artifact: 39,724 byte, SHA-256 `01a2e7186c9b848febfd1ad6a1c5b59ad8fd2493f5f1d9c563f2f2eda9af4acf`; Phase 0: 57,209 byte, SHA-256 `ea4183151dc4bb7cfb6a437c0abc9adbb21725ccd3b132a0e0abb23aedd19c13`. Đều khớp RR.

### Nguồn, định danh và cờ dựng
Nguồn công khai được đọc trực tiếp ngày 2026-10-31; không tải tarball/bottle hay binary.

- [Formula Homebrew hiện hành](https://raw.githubusercontent.com/Homebrew/homebrew-core/HEAD/Formula/f/ffmpeg.rb) xác nhận 9.0.2, **revision 1**, GPL-3.0-or-later; hai hash trong hồ sơ khớp từng ký tự: tarball `8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e`; bottle arm64_tahoe `595b0bb854e692d7f6f89b866e860afacfdab5e3698451555547f58f523ed04d`. Ghi revision 1 khi lập hồ sơ lệnh; HEAD của formula là nguồn thay đổi được, phải đối chiếu lại trước thao tác sau này.
- Formula có 11 phụ thuộc trực tiếp được liệt kê đúng cho macOS; còn pkgconf là phụ thuộc build và bzip2/libxml2 lấy từ macOS. Không coi 11 là toàn bộ closure hoặc khẳng định máy sẽ cài đúng 14 gói. Có cờ GPL, version3, x264, x265, OpenSSL; VideoToolbox/AudioToolbox theo nhánh macOS; không thấy enable-nonfree trong args.
- [LICENSE.md tag n9.0.2](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/LICENSE.md) phù hợp mô tả chuyển LGPL/GPL, version3 và thư viện x264/x265. Nó dẫn tới các tệp COPYING cho điều khoản. Phần cuối còn cảnh báo OpenSSL/GPL; không nên suy chỉ từ thiếu cờ nonfree rằng đã đủ bằng chứng license của toàn binary.
- Đối chiếu bổ sung [configure cùng tag](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/configure), đoạn kiểm tra OpenSSL: OpenSSL từ 3.0.0 dùng cùng GPL cần version3; nhánh OpenSSL cũ có kiểm tra khác. Vì vậy không kết luận formula openssl@4 + GPLv3 tự mâu thuẫn hay không thể phân phối chỉ từ cảnh báo tổng quát trong LICENSE.md. Vẫn cần đọc license đúng phiên bản phụ thuộc; chưa kiểm chứng binary thực tế.

### Nội bộ, đầu ra và giới hạn GPL
- [COPYING.GPLv3 của tag n9.0.2](https://raw.githubusercontent.com/FFmpeg/FFmpeg/n9.0.2/COPYING.GPLv3), mục 2, phân biệt quyền chạy chương trình, việc không chuyển giao bản sao và điều kiện license có áp dụng cho đầu ra tùy nội dung đầu ra có phải covered work hay không. Có thể dùng điều khoản này để viết hồ sơ chính xác hơn; không nên suy quyền video từ sự im lặng của trang legal.
- “Dùng nội bộ” có thể mô tả cách sử dụng công cụ FFmpeg trong phạm vi hiện tại; không có nghĩa video kiếm tiền cũng chỉ dùng nội bộ, không phải kết luận miễn mọi nghĩa vụ GPL hoặc sáng chế. Hồ sơ hiện có câu không phải kết luận pháp lý và không khẳng định GPL chắc chắn không ảnh hưởng đầu ra; giữ giới hạn này.
- Owner cho tiếp tục đánh giá B có điều kiện được ghi trong SG, không thành quyền cài, chạy, phân phối hay phê duyệt pháp lý video thương mại. Rủi ro GPL/phụ thuộc và sáng chế được công khai; GPL và bằng sáng chế là hai vấn đề riêng. Có cờ VideoToolbox không chứng minh chạy được hay đã giải quyết quyền codec trên máy này.

## Chưa thể xác minh
- Trang `https://ffmpeg.org/legal.html` timeout qua công cụ web; thử thêm hostname www cũng timeout. Không xác nhận độc lập câu trang legal “không nói về video đầu ra” hoặc toàn bộ mô tả sáng chế trên trang. Không biến lỗi truy cập thành bằng chứng nguồn sai; các điều khoản GPL nêu trên là nguồn khác được đọc trực tiếp.
- Không đọc/kiểm định đầy đủ license mọi phụ thuộc và notice trong bottle; không so tarball/bottle tải thực tế với digest. Nguồn formula là snapshot hiện hành, không bảo đảm bất biến trong tương lai.
- Không xác minh thực thi VideoToolbox, RAM, nhiệt, tốc độ, dung lượng cài hoặc đầy đủ quyền thương mại/sáng chế. Không chạy FFmpeg, brew install, tải binary/model, render, benchmark; không kết nối Git remote, commit/push hoặc sửa index.
- Hash không chứng minh nguồn gốc lời Owner hay tác giả thay đổi. Không đóng P1-003/P1-004, không mở lại SG-002, không nghiệm thu/chuyển phase hoặc tự phê duyệt ứng viên.

## Bàn giao
- **NEXT ACTOR: Claude** – phản hồi P1-005/P1-006, sửa trong allowlist nếu đồng ý, lập snapshot/RR mới vòng 1/3 theo workflow. Nếu bất đồng hoặc cần quyền ngoài phạm vi, trình Owner.
- Không có quyền cài hay chạy từ báo cáo này. Owner vẫn quyết định riêng sau khi có Codex PASS và hồ sơ thao tác cụ thể.
- Chỉ thêm báo cáo này lên đầu reviewer artifact; giữ nguyên 39,724 byte lịch sử.

---

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
