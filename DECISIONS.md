# AI VIDEO FACTORY – DECISIONS

Nhật ký quyết định. Không xóa mục cũ; khi thay đổi, thêm mục mới và đánh dấu mục cũ `Superseded`.

**Trạng thái:**

- `Approved`: Chủ dự án đã duyệt.
- `Proposed`: Lead Developer đề xuất, **chờ Chủ dự án duyệt**, chưa có hiệu lực ràng buộc.
- `Accepted (Lead)`: quyết định không thuộc kiến trúc cốt lõi, trong thẩm quyền Lead Developer, có thể bị Chủ dự án bác.
- `Superseded`: đã thay thế.

**Mẫu:**

```markdown
## D-XXX – Tiêu đề
- Ngày / Trạng thái / Người quyết định:
- Bối cảnh:
- Quyết định:
- Bằng chứng:
- Phương án đã cân nhắc:
- Hệ quả:
```

## Đã duyệt

### D-001 – Một Factory Manager và bảy Agent
Ngày 2026-10-30. `Approved`, Chủ dự án. Athena, Leonardo, Edison, Pixar, Spielberg, Tesla, Newton. Agent là module logic độc lập, không bắt buộc mỗi Agent có một LLM. Thay đổi cần duyệt lại.

### D-002 – Bộ công nghệ định hướng
Ngày 2026-10-30. `Approved`, Chủ dự án. Như `TECH_STACK.md` mục 2. MLX chỉ đánh giá ở giai đoạn tối ưu.

### D-003 – Nguyên tắc kỹ thuật
Ngày 2026-10-30. `Approved`, Chủ dự án. Như `PROJECT_MASTER.md` mục 7.

### D-004 – Chạy tuần tự trên Mac
Ngày 2026-10-30. `Approved`, Chủ dự án. Ưu tiên tuần tự để tiết kiệm RAM.

### D-005 – Vai trò Claude và Codex
Ngày 2026-10-30. `Approved`, Chủ dự án. Claude là Lead Developer, Codex là Independent Reviewer, Chủ dự án quyết định cuối cùng. Hai AI không đồng thời sửa cùng file hoặc cùng nhánh Git.

### D-006 – Phê duyệt của con người trước khi xuất bản
Ngày 2026-10-30. `Approved`, Chủ dự án. Bắt buộc. Thiết kế không cung cấp tùy chọn tắt.

### D-007 – Duy trì `HANDOFF_TO_CHATGPT.md`
Ngày 2026-10-30. `Approved`, Chủ dự án (quy tắc trong `CLAUDE.md`). Cập nhật sau mọi phase, đọc lại trước mọi phase.

### D-023 – TikTok Direct Post: tiếp tục đánh giá có kiểm soát (Q-13, phương án C)
Ngày 2026-10-30. `Approved`, Project Owner.

Mục này có **hai trạng thái độc lập**:

| Trạng thái | Giá trị | Ý nghĩa |
|---|---|---|
| Decision status | `Approved` | Project Owner đã phê duyệt phương án tiếp tục đánh giá có kiểm soát |
| Direct Post integration status | `POLICY BLOCKED` | Chưa có bằng chứng phương án sử dụng hiện tại đáp ứng chính sách TikTok |

**Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API.** `D-023 Approved` không có nghĩa `Direct Post Approved for Implementation`.

- **Người phê duyệt:** Project Owner.
- **Ngày phê duyệt:** 2026-10-30.
- **Nguồn:** xác nhận trực tiếp của Project Owner trong cuộc trao đổi với ChatGPT Architecture Advisor, do Project Owner chuyển cho Claude. Repo không lưu biên bản cuộc trao đổi đó.
- **Bối cảnh:** R3-01 (Direct Post xung đột với mục đích dùng cá nhân) và R4-01 (lựa chọn C có thể bị hiểu là được triển khai).

**Nội dung phê duyệt:**

1. Giữ mục tiêu TikTok Direct Post trong roadmap dài hạn.
2. Cho phép tiếp tục nghiên cứu chính sách và đánh giá khả năng tích hợp hợp lệ.
3. Chấp nhận rủi ro rằng phạm vi sử dụng cá nhân hiện tại có thể không đáp ứng TikTok Intended Use.
4. Không cho phép triển khai, kích hoạt hoặc sử dụng Direct Post API khi chưa xác minh được phương án phù hợp chính sách.
5. Không coi OAuth, scope, audit hoặc quyết định nội bộ là bằng chứng đủ để sử dụng API.
6. Không tự chuyển AI Video Factory sang multi-user hoặc SaaS.
7. Tiếp tục cho phép phát triển các phần local độc lập với TikTok Direct Post.
8. Có thể hỗ trợ xuất MP4, metadata và thumbnail để người dùng đăng thủ công.
9. Mọi thay đổi phạm vi sản phẩm hoặc quyết định mở khóa Direct Post phải được Project Owner phê duyệt riêng.

**Cổng triển khai:** Direct Post chỉ được xem xét mở cổng khi đủ năm điều kiện G1–G5 tại `docs/deployment/platform-verification.md` mục 3. Việc Project Owner đã chấp nhận rủi ro **không** được dùng để bỏ qua điều kiện nào. Chưa đủ bằng chứng thì giữ `POLICY BLOCKED`.

**Khác biệt với bản ghi trước.** Bản `Proposed` mô tả C là "giữ Direct Post và chấp nhận rủi ro", và Lead Developer khuyến nghị A cộng B. Project Owner chọn C theo nội dung ở trên, hẹp hơn mô tả cũ; nội dung ở trên có hiệu lực. A và B không được chọn. Luồng Upload vào inbox vẫn chưa xác minh; nếu nghiên cứu, phải có kết luận và hồ sơ riêng.

**Không suy ra từ quyết định này:** nghiệm thu Phase 0, cho phép bắt đầu Phase 1, hay thay đổi trạng thái D-009 đến D-022.

### D-013 – Chọn thư viện rasterize SVG bằng benchmark
Ngày 2026-10-31. `Approved`, Project Owner ("Duyệt cả hai", trả lời yêu cầu duyệt D-013 và D-017). Nội dung đề xuất ngày 2026-10-30 được duyệt nguyên văn: chốt ở Phase 1 giữa resvg, CairoSVG và trình duyệt headless bằng benchmark trên máy mục tiêu, vì đây là chỗ nghẽn có khả năng lớn nhất nhưng chưa có số đo.
- **Phạm vi của phê duyệt:** chỉ duyệt **phương pháp** đo. Việc chọn thư viện cuối cùng vẫn trình Project Owner sau khi có số liệu.
- **Không suy ra:** cho phép cài đặt, cho phép bắt đầu Phase 1, hay chọn sẵn thư viện nào. Mỗi lệnh cài đặt vẫn cần giải thích và xác nhận.

### D-017 – Không dùng TTS hoặc công cụ đăng bài không chính thức
Ngày 2026-10-31. `Approved`, Project Owner ("Duyệt cả hai"). Nội dung đề xuất ngày 2026-10-30 được duyệt nguyên văn: loại `edge-tts` và thư viện tương tự, kể cả miễn phí, vì trái nguyên tắc local-first và nguyên tắc dùng API chính thức, và có rủi ro điều khoản dịch vụ.
- **Áp dụng cho:** danh sách ứng viên của spike TTS ở Phase 1; mọi công cụ TTS, đăng bài hay nguồn nội dung dùng dịch vụ không chính thức hoặc không được hỗ trợ.
- **Kết hợp Q-03:** ứng viên còn phải có license cho phép thương mại.
- **Không suy ra:** cho phép bắt đầu Phase 1, hay duyệt bất kỳ ứng viên cụ thể nào.

### D-024 – Tiêu chuẩn bằng chứng S2 cho ứng viên nhóm B (Phase 1.0)
Ngày 2026-10-31. `Approved`, Project Owner ("Chọn S2"; ghi vào file theo "1B, 2A, 4a, 4b", mã 4a). Chi tiết: [phase1-candidates.md](docs/testing/phase1-candidates.md) mục 7.1.
- **Nội dung:** một ứng viên chỉ được xếp nhóm B khi (i) đã đọc toàn văn LICENSE của đúng artifact và runtime; (ii) đã ghi revision hoặc digest và nêu rõ phần chưa xác định được; (iii) không có bằng chứng trái ngược. Dữ liệu huấn luyện không công bố là rủi ro dư do Project Owner chấp nhận bằng văn bản, đi kèm artifact.
- **Phạm vi hẹp:** chỉ là tiêu chuẩn **phân loại**. Không phải kết luận pháp lý, không phải duyệt danh sách model, không phải quyền tải, cài hay chạy. Không áp dụng cho TTS tiếng Việt.
- **Không suy ra:** duyệt bất kỳ ứng viên nào. Việc duyệt từng ứng viên là quyết định riêng (Qwen3 4B `q4_K_M` được duyệt vào danh sách theo mã 1B, ghi tại `phase1-candidates.md`; 8B chưa duyệt).

## Quyết định trong thẩm quyền Lead Developer

### D-008 – Ngôn ngữ tài liệu
Ngày 2026-10-30. `Accepted (Lead)`. Tài liệu viết bằng tiếng Việt, giữ thuật ngữ kỹ thuật tiếng Anh, để Chủ dự án đọc trực tiếp. Code, tên định danh và commit message dùng tiếng Anh. Phần do Chủ dự án viết bằng tiếng Anh trong `CLAUDE.md` được giữ nguyên.

## Chờ Chủ dự án duyệt

Các mục dưới đây không thay đổi kiến trúc đã duyệt, chỉ làm rõ cách hiện thực. Chủ dự án duyệt **riêng từng mục, theo cổng phase** ở `IMPLEMENTATION_PLAN.md` mục 6, không gom chung. Bản rà soát ở cuối tệp này chỉ là khuyến nghị; mọi mục vẫn là `Proposed`.

### D-009 – Ba tiến trình, dashboard chỉ gọi API
Ngày 2026-10-30. `Proposed`. Streamlit → FastAPI → SQLite, Worker tách riêng. **Lý do:** tác vụ dài không chặn API; thay được Streamlit bằng web sau này; chỉ một nơi viết logic. **Phương án bỏ:** Streamlit gọi thẳng DB, đơn giản hơn nhưng khóa cứng giao diện vào dữ liệu.

### D-010 – Hợp đồng Agent bằng artifact có schema
Ngày 2026-10-30. `Proposed`. Agent trao đổi qua tệp JSON có `schema_version`, không gọi nhau trực tiếp. **Lý do:** kiểm tra được, retry được, xem lại được, chạy lại từng bước được.

### D-011 – Job Queue dùng lease và heartbeat
Ngày 2026-10-30. `Proposed`. **Lý do:** máy cá nhân có thể ngủ hoặc tắt giữa chừng; job phải tự phục hồi.

### D-012 – Đẩy khung hình vào FFmpeg, không lưu PNG mặc định
Ngày 2026-10-30. `Proposed`. **Lý do:** 14.400 khung hình mỗi video 10 phút ở 24 fps. Giả định 100–200 KB/ảnh, tức 1,4–2,9 GB tệp tạm mỗi video. Tạm thời lưu khung hình chỉ khi debug.

### D-013 – Chọn thư viện rasterize SVG bằng benchmark
Đã được duyệt ngày 2026-10-31. Xem mục "Đã duyệt". Bản ghi này giữ làm lịch sử: ngày 2026-10-30, `Proposed`, chốt ở Phase 1 giữa resvg, CairoSVG và trình duyệt headless.

### D-014 – Đầu ra mặc định 1080p, 24 fps, H.264/AAC, 16:9
Ngày 2026-10-30. `Proposed`. **Lý do:** 24 fps ít hơn 20% khung hình so với 30 fps và phù hợp hoạt hình 2D. Bản dọc 9:16 phụ thuộc Q-02.

### D-015 – Quản lý secret
Ngày 2026-10-30. `Proposed`. Cấu hình trong `.env` bị Git bỏ qua, OAuth token trong macOS Keychain. **Lý do:** không lưu token dạng rõ trên đĩa.

### D-016 – Không tự xóa, chặn run khi thiếu dung lượng
Ngày 2026-10-30. `Proposed`. Dashboard đề xuất dọn, người xác nhận. Worker từ chối run mới dưới ngưỡng dung lượng.

### D-017 – Không dùng TTS hoặc công cụ đăng bài không chính thức
Đã được duyệt ngày 2026-10-31. Xem mục "Đã duyệt". Bản ghi này giữ làm lịch sử: ngày 2026-10-30, `Proposed`, loại `edge-tts` và thư viện tương tự.

### D-018 – Fencing, staging theo attempt và một Worker
Ngày 2026-10-30. `Proposed`. Bổ sung cho D-011 theo BLOCKER 1 của Codex. `lease_generation` tăng đơn điệu, commit có điều kiện, đầu ra ghi vào staging theo generation, con trỏ trong DB là điểm commit duy nhất, khóa hệ điều hành bảo đảm một Worker. Đặc tả: `docs/architecture/queue-safety.md`.

### D-019 – Máy trạng thái upload và đối soát
Ngày 2026-10-30. `Proposed`. `queued`, `uploading`, `confirmed`, `unknown`, `failed`. Không retry mù; không xác định được thì người duyệt. Đặc tả: `docs/architecture/publishing-reliability.md`.

### D-025 – Watermark NMT chèn ở bước xuất cuối của Spielberg, Quality Gate chặn khi lỗi
- Ngày 2026-11-07. `Proposed` (Owner yêu cầu quy tắc và cho ghi vào DECISIONS; nội dung kỹ thuật dưới đây chờ Owner duyệt).
- Bối cảnh: Owner yêu cầu mọi video xuất bản của "Ngang Một Tí" có watermark trong file, giữ bản sạch, chặn xuất bản khi lỗi.
- Quyết định đề xuất: module `core/branding.py` (Pillow + FFmpeg overlay, công nghệ đã duyệt); chèn sau Quality Gate cơ bản, trên bản sạch của Spielberg; bản đăng `*_nmt.mp4`; báo cáo `watermark_report.json`; Tesla kiểm tra PASS + checksum + duyệt người. Vị trí mặc định dưới-phải (Owner chọn), dọc 190 px / 0,85 / mép 48 px; ngang 240 px / 0,85 / mép 40 × 170 px.
- Bằng chứng: `docs/requirements/WATERMARK_NMT.md` mục 6.
- Phương án đã cân nhắc: watermark YouTube Studio (bị loại: không nằm trong file, chỉ YouTube); chèn vào ảnh nguồn hay từng cảnh (bị loại theo yêu cầu Owner).
- Hệ quả: thêm bước mã hoá lại (~30 s cho video 31 s 60 fps trong VM); thương hiệu phải được khai báo khi xuất.

### D-026 – Facebook Reels đăng trực tiếp qua Graph API, không qua Postiz
- Ngày 2026-11-08. `Approved` (Owner, chat: "Approve option A", gồm cả quyền chạy một bài thử DRAFT thật trên Trang). Codex chưa review.
- Bối cảnh: Postiz đăng video Facebook bằng `file_url` trỏ tới `http://localhost:4007/uploads/...` (`STORAGE_PROVIDER=local`). Máy chủ Meta không tải được địa chỉ này nên mọi lần đăng video Facebook qua Postiz đều sẽ lỗi.
- Quyết định: Tesla dùng adapter `publishing/facebook_reels.py` upload thẳng byte MP4 đã duyệt theo luồng Reels của Graph API (`video_reels` start → `rupload.facebook.com` → finish với `video_state` `DRAFT` hoặc `PUBLISHED`), rồi đọc lại video từ Meta (Trang sở hữu, các phase, `published`) làm bước xác minh độc lập. YouTube và TikTok vẫn đi qua Postiz. OAuth vẫn làm trong Postiz; adapter chỉ đọc Page token đã lưu trong Postgres của stack `avf-postiz` vào bộ nhớ, không ghi ra file hay log, không đặt token trong URL. Chỉ cho phép hai host của Meta.
- Cổng LIVE cho Facebook: phải có `facebook_contract.json` (`PASS_DRAFT_ONLY`) của đúng integration, do lệnh `facebook-draft-test` tạo; Owner vẫn `approve` từng job trong terminal. Với nội dung AI, chấp nhận dòng công bố AI trong caption vì video là hoạt hình 2D, không phải nội dung chân thực; Graph API không có trường nhãn AI đã kiểm chứng. Điểm này cần Codex review.
- Bằng chứng: test DRAFT thật ngày 2026-11-08, video `1124038717286057` trên Trang "Ngang Một Tí" (`1474012595784934`): uploading/processing `complete`, `video_status=ready`, `published=false`, `page_matches=true`. Unit test `tests/unit/test_facebook_reels.py` 20/20, toàn bộ 190/190.
- Phương án đã cân nhắc: (B) tunnel `cloudflared` công khai Postiz – phải cài phần mềm, lộ trang đăng nhập, phải đổi `FRONTEND_URL` và kết nối lại kênh; (C) lưu trữ đám mây S3/R2 – cần tài khoản, có thể phát sinh phí.
- Hệ quả (D-026): Facebook không hiện trong lịch Postiz. Phụ thuộc schema bảng `Integration` của image Postiz đã cài; nâng cấp Postiz phải chạy lại test. App Facebook phải ở chế độ Live, nếu không bài chỉ hiển thị với người có vai trò trong app.

### D-027 – Tự động hoá đăng ba nền tảng, một lần duyệt mỗi tập
- Ngày 2026-11-08. `Approved` (Owner chọn trong phiếu hỏi: "1 approval per video", "Inbox now + apply for Direct Post", "AI line in description", "macOS background service"). Codex chưa review.
- Bối cảnh: Owner muốn "tất cả tự động hoá". Trước đó mỗi manifest cần duyệt riêng, LIVE của YouTube/TikTok bị chặn cứng vì chưa có bộ xác minh độc lập, worker phải chạy tay.
- Quyết định:
  1. Tesla `prepare-episode <videos-post/slug>` đọc gói đã duyệt (watermark PASS, final approved, checksum khớp), tự soạn nội dung từng nền tảng từ `post.json` (lọc câu kêu gọi tag/share kiểu engagement bait, thêm câu hỏi bình luận, hashtag, dòng công bố AI) và tạo một manifest `LIVE` cho mỗi nền tảng. Owner duyệt **một lần cho cả tập** bằng `approve-episode <slug>` trong terminal (cụm xác nhận gồm slug và checksum gộp). Duyệt tập đồng thời là xác nhận quyền (rights) của tập.
  2. TikTok: `UPLOAD` vào hộp nháp (Owner bấm Đăng trong app), `video_made_with_ai=true`. Direct Post vẫn `POLICY BLOCKED` (D-023) cho tới khi TikTok duyệt Production **và** Owner xác nhận riêng việc gỡ chặn.
  3. YouTube: hoạt hình 2D, công bố AI bằng dòng trong mô tả. Lần đầu luôn `private`; khi bộ xác minh đọc lại đúng kênh và `privacyStatus=private`, ghi `youtube_contract.json`; từ đó tập mới mới được `public`. Bộ xác minh: YouTube Data API `videos.list` bằng token Postiz đã lưu (đọc vào bộ nhớ), dự phòng oEmbed công khai.
  4. Worker chạy nền bằng LaunchAgent của user (`service install`), không sudo, gỡ bằng `service uninstall`.
- Phương án đã cân nhắc: không duyệt (bị loại: lỗi đi thẳng ra công khai); adapter YouTube riêng để đặt `containsSyntheticMedia` (để sau, Postiz không hỗ trợ).
- Hệ quả: an toàn vẫn fail-closed: thiếu bộ xác minh, sai kênh, đổi tên kênh, ranh giới gửi chưa rõ đều dừng ở `RECONCILE_REQUIRED`/`POLICY_BLOCKED`, không tự đăng lại.

### D-028 – Cầu nối loopback cho Postiz và tắt SSRF guard nội bộ
- Ngày 2026-11-08. `Approved` (Owner chọn "Port bridge + SSRF off" và "Yes, add resubmit"). Codex chưa review.
- Bối cảnh: lần chạy thật ep08, YouTube và TikTok qua Postiz đều `ERROR` trước khi gọi nền tảng. Postiz đọc lại video từ `http://localhost:4007/uploads/...` nhưng trong container không có gì nghe ở 4007 (Postiz chạy cổng 5000) và SSRF guard của Postiz chặn mọi IP loopback/private ("Blocked IP").
- Quyết định: thêm service `postiz-loopback` (`alpine/socat:1.8.0.3`, pin digest `sha256:beb4a68d…b015e`, 32 MB RAM) dùng chung network namespace với `postiz`, chuyển `127.0.0.1:4007 → 127.0.0.1:5000`; đặt `DISABLE_SSRF_PROTECTION=true`. Thêm lệnh `resubmit JOB_ID`: chỉ khi Postiz báo đúng bài đó `ERROR` và không có `releaseURL`, Owner gõ cụm xác nhận trong terminal; ghi sự kiện `RESUBMIT_AFTER_PROVIDER_ERROR`. Job Facebook trực tiếp không bao giờ đủ điều kiện.
- Bằng chứng: trong container `fetch` file MP4 qua `localhost:4007/uploads/...` → 200, đúng 12 710 973 byte; Mac vẫn mở `localhost:4007` được.
- Phương án đã cân nhắc: adapter trực tiếp YouTube/TikTok như D-026 (nhiều code, phải tự refresh token, dễ lệch với Postiz); đổi `FRONTEND_URL` sang cổng 5000 (trùng AirPlay Receiver của macOS, phải đăng ký lại mọi OAuth redirect).
- Hệ quả/rủi ro: SSRF guard tắt cho mọi tính năng Postiz (webhook, preview URL). Chấp nhận vì Postiz chỉ bind `127.0.0.1`, tắt đăng ký, một người dùng. Nâng cấp Postiz phải kiểm tra lại cả hai điểm.

### D-020 – Kiểm soát truy cập API và dashboard cục bộ
Ngày 2026-10-30. `Proposed`. Allowlist Host, kiểm tra Origin, token API cục bộ, phê duyệt kèm checksum, quyền tệp chặt. **Lý do:** trang web bất kỳ trong trình duyệt vẫn gửi được yêu cầu tới `127.0.0.1`. Đặc tả: `docs/architecture/security-and-rights.md` mục 2.

### D-021 – OAuth và vòng đời token
Ngày 2026-10-30. `Proposed`. `state`, PKCE nơi hỗ trợ, scope tối thiểu, Keychain, thu hồi, che log. Đặc tả: `docs/architecture/security-and-rights.md` mục 3–5.

### D-022 – Hồ sơ quyền và Rights Gate fail closed
Ngày 2026-10-30. `Proposed`. Mở rộng manifest license thành hồ sơ quyền; thiếu hoặc không rõ thì chặn; nhân bản giọng mặc định tắt. Đặc tả: `docs/architecture/security-and-rights.md` mục 6–8.

### Mở rộng trong Bản sửa 2 (2026-10-30)

Các mở rộng dưới đây thuộc phạm vi quyết định đã có, không tạo mã mới. **Trạng thái mọi mục vẫn là `Proposed`.**

- **D-018:** thêm khóa `heavy.lock` kế thừa, dây sinh tồn, `RLIMIT_FSIZE`, xử lý `SQLITE_BUSY` bằng `pending_outcome` và tạm dừng hàng đợi, chỉ thu hồi job lúc Worker khởi động.
- **D-019:** thêm ranh giới adapter, `publish_intents`, yêu cầu TikTok và YouTube theo tài liệu đã đọc.
- **D-021:** thêm nguyên tắc `client_secret` của ứng dụng desktop không phải bí mật được bảo vệ, xác minh scope thực nhận, không đưa token tới dashboard, quy tắc cổng callback theo nhà cung cấp.
- **D-022:** thêm gói xuất bản bất biến, năm điều kiện tạo `queued`, kiểm tra lại trước khi gửi, `PublishGrant`.

**Bản sửa 3:** D-018 thêm `pending_outcome` hai loại `success`, `failure` và xử lý đồng hồ lùi khi Worker đang sống. Trạng thái vẫn là `Proposed`.

## Rà soát D-009 đến D-017 (Bản sửa 1, 2026-10-30)

Đây là **khuyến nghị của Lead Developer, không phải phê duyệt.** Chi phí trên máy là ước tính định tính, chưa đo.

### D-009 – Ba tiến trình
- **Nói đơn giản:** màn hình (Streamlit), cổng tiếp nhận (FastAPI) và người làm việc (Worker) chạy tách nhau. Màn hình chỉ nói chuyện với cổng tiếp nhận.
- **Lợi ích:** render dài không làm treo giao diện; Worker chết không kéo sập dashboard; sau này thay được giao diện.
- **Chi phí trên máy:** thêm hai tiến trình Python thường trực và thêm việc khởi động, debug. Có thể tắt dashboard khi render để giảm bộ nhớ.
- **Phase đầu tiên phụ thuộc:** Phase 2.
- **Khuyến nghị: duyệt có điều kiện.** Chỉ một Worker; đo bộ nhớ lúc rỗi ở Phase 2.

### D-010 – Hợp đồng artifact
- **Nói đơn giản:** các Agent không gọi nhau, mà để lại kết quả dưới dạng tệp có cấu trúc cho bước sau đọc.
- **Lợi ích:** xem lại được, kiểm tra được, chạy lại một bước được, Agent thật sự độc lập.
- **Chi phí trên máy:** rất nhỏ về tài nguyên; chi phí chính là công viết và giữ schema.
- **Phase đầu tiên phụ thuộc:** Phase 2 (schema), Phase 3 (dùng thực tế).
- **Khuyến nghị: duyệt.** Chỉ định nghĩa schema khi có Agent thật cần.

### D-011 – Lease và heartbeat
- **Nói đơn giản:** Worker "mượn" job trong một thời hạn và liên tục báo còn sống. Ngừng báo thì job có thể được lấy lại.
- **Lợi ích:** tự phục hồi sau khi máy ngủ hoặc tiến trình chết.
- **Chi phí trên máy:** ghi DB mỗi vài giây, không đáng kể; thêm độ phức tạp về logic và kiểm thử.
- **Phase đầu tiên phụ thuộc:** Phase 2.
- **Khuyến nghị: duyệt có điều kiện, chỉ khi duyệt cùng D-018.** Riêng D-011 chưa an toàn, đây là BLOCKER 1 của Codex.

### D-012 – Đẩy khung hình thẳng vào FFmpeg
- **Nói đơn giản:** vẽ xong khung nào đưa ngay vào bộ mã hóa, không lưu hàng nghìn ảnh ra đĩa.
- **Lợi ích:** tiết kiệm ước tính 1,4–2,9 GB tệp tạm mỗi video, giảm ghi SSD.
- **Chi phí trên máy:** khó xem lại khung hình lỗi; nếu lỗi giữa cảnh phải render lại cả cảnh. Tạm thời lưu khung hình khi debug.
- **Phase đầu tiên phụ thuộc:** Phase 4; bằng chứng từ Phase 1.
- **Khuyến nghị: duyệt có điều kiện,** sau khi benchmark Phase 1 cho thấy cách này chạy ổn định. Không cần quyết trước Phase 1.

### D-013 – Chọn thư viện rasterize bằng benchmark
- **Nói đơn giản:** thử vài công cụ chuyển SVG thành ảnh trên chính máy này rồi mới chọn.
- **Lợi ích:** chọn theo số đo cho chỗ có thể là nghẽn lớn nhất.
- **Chi phí trên máy:** cài tạm vài thư viện; trình duyệt headless tốn dung lượng và bộ nhớ hơn.
- **Phase đầu tiên phụ thuộc:** Phase 1.
- **Khuyến nghị: duyệt.** Đây là duyệt phương pháp, không phải chọn công cụ. Kết quả cuối vẫn trình Chủ dự án.

### D-014 – 1080p, 24 fps, H.264/AAC, 16:9
- **Nói đơn giản:** định dạng chuẩn cho video ngang.
- **Lợi ích:** ít hơn 20% khung hình so với 30 fps, tương thích rộng.
- **Chi phí trên máy:** bản dọc 9:16 có thể cần render riêng, tức thời gian render có thể gấp đôi nếu đăng TikTok với bố cục riêng.
- **Phase đầu tiên phụ thuộc:** Phase 4. Phase 1 có thể đo ở thông số này mà không cần chốt.
- **Khuyến nghị: hoãn** cho tới khi trả lời Q-02 và có số đo Phase 1.

### D-015 – Quản lý secret
- **Nói đơn giản:** cấu hình thường để trong `.env` ngoài Git; khóa đăng nhập nền tảng để trong Keychain của macOS.
- **Lợi ích:** không có token dạng rõ trên đĩa.
- **Chi phí trên máy:** rất nhỏ; Keychain có thể hiện hộp thoại xác nhận, gây gián đoạn khi chạy không giám sát, cần kiểm tra ở Phase 15.
- **Phase đầu tiên phụ thuộc:** Phase 2 (`.env`, chưa có secret nền tảng), Phase 15 (Keychain).
- **Khuyến nghị: duyệt có điều kiện.** Duyệt phần `.env` trước Phase 2. Phần Keychain duyệt cùng D-021 trước Phase 15.

### D-016 – Không tự xóa, chặn run khi thiếu dung lượng
- **Nói đơn giản:** hệ thống chỉ đề xuất dọn, người mới được xóa; đĩa gần đầy thì không bắt đầu video mới.
- **Lợi ích:** an toàn dữ liệu, tránh đầy đĩa giữa chừng.
- **Chi phí trên máy:** đĩa đầy dần vì dữ liệu mồ côi cũng được giữ; cần dọn định kỳ thủ công.
- **Phase đầu tiên phụ thuộc:** Phase 2 (kiểm tra dung lượng), Phase 10 (giao diện dọn).
- **Khuyến nghị: duyệt.** Ngưỡng dung lượng chốt theo số đo Phase 1.

### D-017 – Không dùng TTS hoặc công cụ đăng bài không chính thức
- **Nói đơn giản:** không dùng các công cụ miễn phí chạy nhờ dịch vụ của bên khác theo cách không được hỗ trợ.
- **Lợi ích:** tránh rủi ro điều khoản, gián đoạn đột ngột, phụ thuộc mạng.
- **Chi phí trên máy:** không có; đổi lại ít lựa chọn hơn, có thể chất lượng giọng thấp hơn.
- **Phase đầu tiên phụ thuộc:** Phase 1 (danh sách ứng viên TTS spike).
- **Khuyến nghị: duyệt** trước Phase 1.
