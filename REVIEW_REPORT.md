# Independent Architecture Review – AI Video Factory

- Ngày review: 2026-10-30
- Phạm vi: `PROJECT_MASTER.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `TECH_STACK.md`, `AGENTS.md`, `CLAUDE.md`, `DECISIONS.md`, `CURRENT_STATUS.md`, `TASKS.md`, cùng các README liên quan trong `docs/` và báo cáo Phase 0.
- Trạng thái được review: Phase 0, chưa có code; các quyết định D-009 đến D-017 còn `Proposed`.
- Cách review: đọc tài liệu; không chạy code, cài phần mềm hay sửa các tài liệu được review. Chỉ tạo báo cáo này theo yêu cầu.

## PASS: Điểm phù hợp

1. **Bám blueprint Factory Manager + bảy Agent.** `PROJECT_MASTER.md:52-64` định danh rõ Athena, Leonardo, Edison, Pixar, Spielberg, Tesla, Newton; `ARCHITECTURE.md:65-75` mô tả Manager điều phối và chạy tuần tự. Không thấy Agent thứ tám hoặc thay tên/vai trò cốt lõi.
2. **Local-first và Sequential-first được giữ.** `PROJECT_MASTER.md:72-86`, `ARCHITECTURE.md:7-15,121-138` dùng SQLite, Ollama cục bộ, API bind loopback và giới hạn một tác vụ nặng; không thêm dịch vụ cloud trả phí.
3. **Phù hợp hướng thiết kế cho Mac M4 16GB, với điều kiện benchmark.** Có nhận diện máy không quạt, RAM hợp nhất, giải phóng model, theo dõi RAM/dung lượng và đánh dấu dự báo là giả định chưa đo (`ARCHITECTURE.md:121-138,153`). Mục tiêu một video/ngày chưa bị tuyên bố là đã đạt.
4. **Việt-Anh và tính năng nội dung được bao phủ trong yêu cầu/lộ trình.** `docs/requirements/README.md:9-20` liệt kê song ngữ, nhiều nhân vật/giọng, lip-sync và bốn phong cách; Phase 6, 9, 12 có tiêu chí cụ thể trong `IMPLEMENTATION_PLAN.md`.
5. **Có thiết kế scene-based rendering.** `ARCHITECTURE.md:98-106` tách scene spec, clip cảnh, ghép video và retry riêng; Phase 4 có tiêu chí kiểm tra render lại không ảnh hưởng cảnh khác.
6. **Quality Gate và Human Approval được thiết kế rõ.** QG1–QG5 và phê duyệt checksum trước Tesla nằm ở `ARCHITECTURE.md:108-119`; phù hợp D-006 và không có đường tắt bỏ duyệt.
7. **Có đường mở rộng dashboard hợp lý.** Dashboard chỉ gọi FastAPI, lõi tách khỏi UI, và mục mở rộng nêu thay Streamlit bằng frontend web mà không xây hạ tầng đó trước (`ARCHITECTURE.md:7-15,31,191-193`).
8. **Nguyên tắc secret và license đã được nhận diện.** Có đề xuất `.env`/Keychain, che secret khỏi log, OAuth scope tối thiểu, audit log và license manifest (`ARCHITECTURE.md:157-168`). Phần này chưa phải quyết định đã duyệt.
9. **MVP được chia lát tương đối thực dụng.** Có vertical slice 60 giây ở Phase 9, dashboard sau đó, tích hợp mạng xã hội để cuối; không kéo MLX/OpenToonz vào MVP (`IMPLEMENTATION_PLAN.md:3,21-24,41-48`).

## WARNING: Điểm cần chú ý

1. **Ranh giới ba tiến trình và hợp đồng artifact là mở rộng cần duyệt.** D-009, D-010 ở trạng thái Proposed (`DECISIONS.md:52-60`), trong khi `ARCHITECTURE.md:7-15,77-86` trình bày chúng như thiết kế khá cụ thể. Đây không trái blueprint nếu được chấp thuận, nhưng chưa thể coi là đã được Chủ dự án duyệt.
2. **Bằng chứng khả thi trên máy chưa có.** Dự báo 5–7 GB cho LLM và 1–3 GB/video chưa đo (`ARCHITECTURE.md:123-130,153`). TTS tiếng Việt có license phù hợp, render bền và tốc độ đạt mục tiêu vẫn là rủi ro đã biết (`IMPLEMENTATION_PLAN.md` Phase 1, 6, 14; báo cáo Phase 0:65-67).
3. **MVP có thể hơi nặng về hạ tầng.** Streamlit + FastAPI + worker riêng + queue SQLite tự xây + lease/heartbeat + artifact JSON làm tăng số thành phần phải vận hành và debug trên một máy (`ARCHITECTURE.md:7-15,88-95`). Hợp lý nếu cần khôi phục bền, nhưng nên giữ một worker tuần tự và trì hoãn phần phức tạp cho tới khi có use case/benchmark.
4. **Lộ trình chưa kiểm chứng TTS tiếng Việt sớm nhất có thể.** TTS được benchmark Phase 6, trong khi Phase 1 tập trung môi trường/render và Phase 4–5 đã xây renderer/animation. Vì TTS được ghi là rủi ro cao, có thể làm spike TTS sớm hơn hoặc chạy song song về mặt khảo sát (không chạy song song tải nặng), để tránh đầu tư sâu trước khi biết có giọng đạt chất lượng/license.
5. **Khả năng mở rộng chỉ được bảo đảm ở mức ranh giới API.** Chưa có hợp đồng API, versioning, auth khi bind ngoài loopback, migration từ SQLite hoặc kế hoạch tách worker. Điều này phù hợp MVP; cần chốt khi triển khai website/app, không nên hiểu là đã sẵn sàng multi-user.
6. **Bảo mật localhost cần thêm threat model khi có dashboard/API.** Loopback không thay thế CSRF protection cho OAuth callback hay kiểm soát origin/session; tài liệu hiện chưa định nghĩa cơ chế xác thực dashboard, quản lý callback state, lưu/thu hồi token và quyền truy cập tệp workspace. Đây là hạng mục thiết kế trước khi tích hợp OAuth hoặc mở API ra mạng.
7. **Bản quyền: manifest là cần nhưng chưa đủ.** `ARCHITECTURE.md:166-168` yêu cầu nguồn và license nhưng chưa mô tả bằng chứng quyền sử dụng, phạm vi license theo phiên bản model/voice, sự đồng ý khi nhân bản giọng, quy trình rà soát nội dung/nhạc, hoặc cách lưu điều khoản nguồn. TTS voice cloning có consent được nhắc ở `TECH_STACK.md`, nhưng chưa thành gate cụ thể.
8. **Chính sách API cần được cập nhật ngay trước khi làm Tesla.** TikTok docs hiện xác nhận client chưa audit bị giới hạn nội dung riêng tư và cần scope `video.publish` được duyệt ([TikTok Direct Post](https://developers.tiktok.com/docs/en/content-posting-api-get-started)). YouTube Data API `videos.insert` hiện nêu rõ privacy status và nói upload từ project chưa xác minh không tự động bị khóa riêng tư ([YouTube videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)); lịch sử/chính sách có thể khác theo loại project và vẫn cần xác minh khi triển khai. Nhận định ở `TECH_STACK.md:4` được đánh dấu cần kiểm tra lại, nhưng mô tả YouTube tại `TECH_STACK.md:27` nên được cập nhật với điều kiện cụ thể, không để thành giả định triển khai. Facebook quyền/Page/App Review chưa được kiểm tra trong lượt review này.
9. **Kiểm tra .gitignore/secret chưa được tái xác minh trong review này.** Báo cáo Phase 0 nói có kiểm tra một số mẫu (`PHASE-00-REPORT.md:37-45`), nhưng chính sách secret còn Proposed. Cần review mẫu ignore và `.env.example` khi chuyển sang Phase 1/2.
10. **Quy trình làm việc có phụ thuộc tệp handoff chưa tồn tại.** `CURRENT_STATUS.md:23-25` và Phase report nêu `HANDOFF_TO_CHATGPT.md` chưa có trên đĩa; `CLAUDE.md` yêu cầu duy trì. Đây là lỗ hổng bàn giao/quản lý phase, không phải thay đổi kiến trúc sản phẩm.

## BLOCKER: Vấn đề phải sửa trước khi triển khai

1. **Job lease chưa có cơ chế fencing để ngăn worker cũ tiếp tục ghi sau khi lease hết hạn.** `ARCHITECTURE.md:88-95` có lease, heartbeat, retry và idempotency key, nhưng chưa quy định fencing token/generation hay kiểm tra quyền sở hữu lease ngay trước khi commit artifact và cập nhật trạng thái. Nếu worker bị pause lâu, lease hết hạn, worker khác nhận lại job, rồi worker cũ chạy tiếp, hai worker có thể cùng thực thi. Idempotency key chỉ chống trùng nếu mọi thao tác và ghi kết quả được bảo vệ bằng transaction/quyền sở hữu hiện hành; nó không tự ngăn xử lý đồng thời. Cần bổ sung quy tắc fencing/commit có điều kiện và kiểm thử fault injection trước Phase 2–3.
2. **Chống đăng trùng chưa giải quyết trường hợp kết quả API không rõ.** `docs/agents/README.md:44-49` và lược đồ `docs/database/README.md:16` có idempotency key, nhưng API nền tảng có thể đã nhận upload trong khi client timeout trước khi lưu `external_id`. Retry mù có thể đăng hai lần. Trước Phase 15, cần thiết kế trạng thái `unknown/pending reconciliation`, tra cứu/đối soát phía nền tảng khi khả thi, và bắt buộc human review khi không thể xác định kết quả.
3. **Quyết định kiến trúc mở rộng chưa được thông qua trước cổng triển khai nền tảng.** Phase 1 không nên bị chặn bởi toàn bộ D-009–017, nhưng Phase 2 không nên bắt đầu với thiết kế ba tiến trình, queue lease, artifact contract và secret storage khi D-009, D-010, D-011, D-015 còn Proposed. `CURRENT_STATUS.md:31` đang gom duyệt tất cả vào Q-01; cần chủ dự án ghi rõ quyết định trước Phase tương ứng. Đây là blocker quản trị trước Phase 2, không phải bằng chứng Claude đã tự ý thay blueprint.
4. **Không thể tuyên bố tuân thủ quyền API/license chỉ bằng kế hoạch hiện tại.** Trước khi tích hợp một nền tảng hoặc TTS cụ thể, phải xác minh scope, quyền tài khoản, điều khoản thương mại và giới hạn hiện hành cho đúng app/model/voice. Hiện tài liệu chủ động ghi việc này chưa xác minh (`TECH_STACK.md:4,23-35`, `PHASE-00-REPORT.md:47`). Blocker này áp dụng trước tích hợp tương ứng, không chặn dựng khung local MVP.

## RECOMMENDATION: Đề xuất cải tiến

1. Thêm vào hợp đồng queue: `lease_generation`/fencing token tăng đơn điệu; worker chỉ được commit khi token hiện tại còn khớp; artifact ghi vào vùng staging theo attempt rồi atomically promote; kiểm thử worker cũ hồi sinh sau timeout/giấc ngủ.
2. Với Tesla, dùng state machine riêng cho upload (`queued`, `uploading`, `confirmed`, `unknown`, `failed`); không tự retry trạng thái `unknown` trước khi đối soát; lưu request ID, external ID, thời điểm, và bằng chứng phản hồi nhưng không lưu token.
3. Dời một spike TTS Việt/Anh nhỏ lên Phase 1: đo chất lượng nghe, tốc độ, RAM, license và chi phí cho vài ứng viên; chỉ giữ Phase 6 cho adapter và tích hợp đầy đủ. Không yêu cầu chọn engine trước khi có mẫu nghe và license rõ.
4. Giữ cấu hình MVP tối giản: một worker, một job nặng, SQLite; chỉ thêm nhiều worker/concurrency khi đo được nhu cầu. Benchmark throughput và độ tin cậy trước khi cam kết hoàn thành video 10 phút/ngày.
5. Bổ sung bảng “quyết định cần duyệt trước phase” vào `IMPLEMENTATION_PLAN.md`, ánh xạ D-009–017 với phase sử dụng đầu tiên; tránh hiểu `Proposed` là quyết định đã duyệt.
6. Bổ sung checklist quyền nội dung: nguồn/URL và ngày lấy; chủ sở hữu; giấy phép và phiên bản; quyền thương mại/phái sinh; consent giọng; attribution; hash asset; người duyệt. Gate phải fail closed khi metadata quyền thiếu hoặc không rõ.
7. Trước OAuth, đặc tả loopback callback: state/PKCE theo khả năng nhà cung cấp, callback port cố định/được kiểm soát, scope tối thiểu theo tính năng, lưu và thu hồi token trong Keychain, redaction log. Trước khi mở API ra LAN/internet, bổ sung auth và CSRF/origin protection.
8. Cập nhật ghi chú chính sách YouTube/TikTok/Facebook ở Phase 15–16 bằng link chính thức, ngày kiểm tra, scope và trạng thái audit/app review. Chính sách hiện hành nên là điều kiện nghiệm thu của từng adapter, không là cam kết cứng từ Phase 0.
9. Tạo `HANDOFF_TO_CHATGPT.md` sau khi editor được đóng/được bàn giao, như yêu cầu CLAUDE, và làm rõ quy tắc trạng thái Phase 0 để không gọi tài liệu là “triển khai xong” khi các quyết định vẫn chờ nghiệm thu.
10. Không cần thêm Kubernetes, message broker, cloud database, vector database, hay frontend web cho MVP; bộ công nghệ hiện tại đã đủ để kiểm chứng vertical slice.

## FINAL VERDICT: NEEDS REVISION

Blueprint cấp cao được giữ nguyên: Factory Manager + bảy Agent, local-first, sequential-first, scene-based render, song ngữ, nhiều nhân vật/TTS/lip-sync, Quality Gate, Human Approval và API boundary cho UI tương lai đều được phản ánh. Tuy nhiên, chưa nên duyệt hồ sơ để bắt đầu triển khai Phase 2–3 cho tới khi xử lý thiết kế fencing của queue và chốt các quyết định Proposed liên quan. Việc tích hợp publishing phải chờ xử lý trạng thái kết quả không rõ và xác minh policy/permissions hiện hành.

### Vị trí cần cập nhật nếu Chủ dự án quyết định yêu cầu sửa

- `ARCHITECTURE.md:88-95`: fencing, lease expiry và quyền commit của worker.
- `docs/agents/README.md:44-49`, `docs/database/README.md:16`: đối soát upload, idempotency và trạng thái kết quả không rõ.
- `DECISIONS.md:52-80`, `CURRENT_STATUS.md:27-39`, `IMPLEMENTATION_PLAN.md` Phase 1–3: duyệt quyết định theo phase và spike TTS sớm.
- `ARCHITECTURE.md:157-168`, `TECH_STACK.md:23-35`: OAuth threat model, quyền nội dung/license, nguồn chính thức và ngày xác minh API.
- `HANDOFF_TO_CHATGPT.md`: tạo sau khi tệp đang mở trong editor được bàn giao.

Báo cáo này không thay đổi các file được review và không phải phê duyệt thay cho Chủ dự án.
