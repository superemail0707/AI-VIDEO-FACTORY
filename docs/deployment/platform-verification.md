# Xác minh chính sách nền tảng

**Việc này là bắt buộc ngay trước khi triển khai mỗi publishing adapter.** Ảnh chụp ở mục 2 chỉ phục vụ lập kế hoạch. Nó không phải cam kết, và không có nghĩa dự án đã được cấp quyền nào.

## 1. Hồ sơ phải có trước khi viết adapter

Tạo `docs/deployment/verification-<platform>.md`:

- Ngày kiểm tra, người kiểm tra.
- Link tài liệu chính thức và ngày cập nhật trên trang.
- Scope cần cho từng tính năng.
- Trạng thái audit, App Review của app của Chủ dự án.
- Loại tài khoản và đích đăng được hỗ trợ.
- Quota và giới hạn.
- Luồng OAuth, hỗ trợ PKCE, cách thu hồi token.
- Khả năng đối soát: tra cứu theo định danh, tiếp tục phiên upload, liệt kê nội dung, idempotency.
- **Tính phù hợp mục đích sử dụng (intended use)** của dự án cá nhân với từng API. Đây là điều kiện riêng, không được suy ra từ việc có scope hay qua audit.
- Yêu cầu nhãn nội dung AI, thiết lập trẻ em, hiển thị bắt buộc.
- Điều khoản sử dụng API liên quan đến nội dung tự động và thương mại.
- Kết luận: tiến hành, tiến hành có điều kiện, hay dừng.

Hồ sơ cũ hơn 30 ngày khi bắt đầu Phase phải kiểm tra lại. Điều gì không xác minh được thì coi là không được hỗ trợ.

## 2. Ảnh chụp kiểm tra ngày 2026-10-30

Chỉ đọc tài liệu công khai qua công cụ tóm tắt web, chưa thử API, chưa xác minh đủ các mục ở trên.

| Nền tảng | Nội dung ghi nhận | Nguồn |
|---|---|---|
| YouTube | Trang ghi video từ dự án API chưa xác minh **không** bị giới hạn ở chế độ riêng tư. `videos.insert` có quota 100 lượt mỗi ngày, trong nhóm quota riêng cho upload. Cần một trong các scope được liệt kê, như `youtube.upload`. Trang cập nhật 2026-10-15 UTC | [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert) |
| TikTok | Nội dung của client chưa audit bị giới hạn ở chế độ riêng tư. App cần được duyệt scope `video.publish` và người dùng phải ủy quyền. Có `publish_id` và endpoint tra trạng thái. Trang không mô tả cơ chế idempotency | [Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started) |
| Facebook | API đăng lên Pages. Cần `pages_show_list`, `pages_read_engagement`, `pages_manage_posts` và Page access token của người có quyền `CREATE_CONTENT`. Trang này không đề cập trang cá nhân, tra trạng thái hay idempotency | [Video API Publishing](https://developers.facebook.com/docs/video-api/guides/publishing) |

**Bổ sung trong Bản sửa 2 (cũng ngày 2026-10-30):**

| Nền tảng | Nội dung ghi nhận | Nguồn |
|---|---|---|
| YouTube | `videos.insert` tốn 1 đơn vị trong nhóm quota riêng, mặc định 100 lượt mỗi ngày, tách khỏi 10.000 đơn vị dùng chung. Trang cập nhật 2026-10-15 UTC | [Quota](https://developers.google.com/youtube/v3/determine_quota_cost) |
| Google OAuth | Ứng dụng desktop là public client, không giữ được secret. Luôn dùng PKCE. Phải chống CSRF. Phải xác minh scope thực nhận. Loopback dùng cổng ngẫu nhiên còn trống. Thu hồi có thể ảnh hưởng mọi client của dự án. Trang cập nhật 2026-10-29 UTC | [OAuth cho ứng dụng cài đặt](https://developers.google.com/identity/protocols/oauth2/native-app) |
| TikTok | Truy vấn creator info cần `video.publish`; trả `creator_nickname`, `privacy_level_options`, trạng thái tương tác, `max_video_post_duration_sec`; có lỗi giới hạn đăng như `spam_risk_too_many_posts`, `reached_active_user_cap` | [Query Creator Info](https://developers.tiktok.com/doc/content-posting-api-reference-query-creator-info) |
| TikTok | Không có giá trị quyền riêng tư mặc định; chỉ đưa tùy chọn được phép; tương tác không bật sẵn; có xem trước; không gửi nội dung trước khi người dùng đồng ý rõ ràng. Client chưa audit: chỉ `SELF_ONLY`, tài khoản phải ở chế độ riêng tư, tối đa 5 người dùng mỗi 24 giờ; mỗi creator có giới hạn khoảng 15 bài mỗi ngày | [Content Sharing Guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines) |
| Facebook | Trang App Review ghi: người không có vai trò với app thì app phải qua App Review; chỉ người có vai trò thì không cần. Trang không nêu quyền cụ thể cho đăng Page | [App Review](https://developers.facebook.com/docs/app-review) |

**Trạng thái sẵn sàng:**

| Nền tảng | Trạng thái để triển khai |
|---|---|
| YouTube | Chưa sẵn sàng. Cần hồ sơ đầy đủ ngay trước Phase 15 |
| TikTok Direct Post | **`POLICY BLOCKED`.** Audit không phải thủ tục đủ để mở khóa. D-023 `Approved` không thay đổi trạng thái này. Xem mục 3 |
| TikTok Upload (inbox) | **Chưa xác minh.** Chưa có hồ sơ riêng |
| Facebook | **Chưa xác minh.** Các ghi nhận trên đến từ công cụ tóm tắt và chưa đủ để kết luận về quyền, App Review, hay loại token phù hợp cho dự án. Phải đọc trực tiếp tài liệu chính thức trước khi dựa vào |

**Chưa xác minh:** quy trình App Review và phân loại quyền của Facebook, audit TikTok của app cụ thể, PKCE của TikTok và Facebook, loại OAuth client cho ứng dụng cục bộ ở TikTok và Facebook, phương thức đối soát của YouTube và Facebook, nhãn nội dung AI.

## 3. TikTok: xung đột với mục đích dùng cá nhân (R3-01)

**Bằng chứng.** Mục Intended Use trong [Content Sharing Guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines), dưới phần Direct Post API, đọc ngày 2026-10-30:

- API client phải hướng tới đối tượng rộng, không giới hạn ở nhóm nội bộ hoặc sử dụng riêng tư.
- Trường hợp không được chấp nhận gồm công cụ tiện ích giúp upload nội dung lên tài khoản do bạn hoặc nhóm của bạn quản lý.

**Đối chiếu.** `PROJECT_MASTER.md` mục 3 loại trừ hệ thống nhiều người dùng. AI Video Factory là công cụ cục bộ của một Chủ dự án đăng lên tài khoản của chính họ, đúng với trường hợp bị loại.

**Kết luận.** Trạng thái tích hợp: **`POLICY BLOCKED`**, tức chưa có bằng chứng phương án sử dụng hiện tại đáp ứng chính sách TikTok. Hoàn thiện OAuth, consent và giao diện không giải quyết điều kiện này. Chưa nộp audit, nên đây **không phải** quyết định từ chối của TikTok với một app cụ thể, mà là rủi ro khả thi có bằng chứng chính sách.

**Luồng Upload vào inbox.** [Tài liệu](https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content) mô tả scope `video.upload`: nội dung vào inbox dưới dạng nháp, creator tự hoàn tất trong TikTok. Trang này không nói về audit, giới hạn với client chưa audit hay intended use. Phần Intended Use nói trên nằm dưới Direct Post và không xác nhận có áp dụng cho Upload hay không. **Vì vậy không được coi Upload là đường đi đã mở.** Nếu nghiên cứu luồng này, phải giữ kết luận và hồ sơ riêng; kết luận về Direct Post không áp dụng sang Upload và ngược lại.

**Quyết định đã ghi nhận (D-023, Q-13).** Project Owner chọn phương án C ngày 2026-10-30. Toàn văn ở `DECISIONS.md`. Các phương án A (hoãn) và B (đánh giá Upload) không được chọn. Nhờ điều 8 của quyết định, vẫn có thể hỗ trợ xuất MP4, metadata và thumbnail để người dùng đăng thủ công.

| Trạng thái | Giá trị |
|---|---|
| Decision status (D-023) | `Approved` |
| Direct Post integration status | `POLICY BLOCKED` |

**Phê duyệt phương án C chỉ cho phép tiếp tục đánh giá khả năng tích hợp. Quyết định này không cấp quyền triển khai TikTok Direct Post API.**

**Điều kiện mở cổng triển khai.** Mục này là bản chuẩn; tài liệu khác tham chiếu tới đây. Direct Post chỉ được xem xét mở cổng khi đủ **cả năm** điều kiện:

| # | Điều kiện | Bằng chứng tối thiểu | Hiện tại |
|---|---|---|---|
| G1 | Có hồ sơ đánh giá chính sách cập nhật, có dẫn nguồn | `verification-tiktok.md` theo mục 1, có link và ngày kiểm tra | Chưa có |
| G2 | Xác minh được phương án sử dụng cụ thể đáp ứng Intended Use | Mô tả phương án và đối chiếu từng yêu cầu Intended Use | Chưa có; phạm vi hiện tại khớp trường hợp bị loại |
| G3 | Có bằng chứng phù hợp về quyền truy cập, OAuth, scope và điều kiện nền tảng | Hồ sơ theo mục 1 cho đúng app của dự án | Chưa có |
| G4 | Các yêu cầu Rights Gate, Human Approval, bảo mật và publishing reliability được đáp ứng theo Phase | Kết quả nghiệm thu của các phase liên quan | Chưa có |
| G5 | Project Owner ban hành quyết định triển khai riêng | Mục quyết định mới, tách khỏi D-023 | Chưa có |

**Quy tắc áp dụng:**

- G1–G4 là điều kiện tiên quyết của G5. D-023 không phải G5.
- **Việc Project Owner đã chấp nhận rủi ro không được dùng để bỏ qua bất kỳ điều kiện nào trên.**
- OAuth, scope, audit hay quyết định nội bộ, riêng lẻ hoặc gộp lại, đều không phải bằng chứng đủ để sử dụng API.
- Chưa đủ bằng chứng thì giữ `POLICY BLOCKED`.
- Trong lúc bị chặn, được phép nghiên cứu chính sách và đánh giá khả năng tích hợp. Không được triển khai, kích hoạt hoặc sử dụng Direct Post API.

**Không được:** mở sản phẩm cho nhiều người dùng chỉ để đáp ứng intended use, hay mô tả sai mục đích sử dụng trong hồ sơ audit. Mọi thay đổi phạm vi sản phẩm cần Project Owner phê duyệt riêng.
