# Yêu cầu bảo mật và quyền nội dung

> **Trạng thái:** yêu cầu tương lai, `Proposed` (D-015, D-020, D-021, D-022). Chưa có OAuth client, chưa có quyền API nào được cấp, chưa có code.

## 1. Mô hình đe dọa

| Tác nhân | Ví dụ | Biện pháp chính |
|---|---|---|
| Trang web độc hại trong trình duyệt của Chủ dự án | Gửi yêu cầu tới `127.0.0.1`, DNS rebinding | Kiểm tra Host, Origin, token API |
| Nội dung không tin cậy | Nguồn tham khảo chứa lệnh cho LLM | Coi là dữ liệu; LLM không có quyền xuất bản |
| Tiến trình khác hoặc người dùng khác trên máy | Đọc DB, log, token | Quyền tệp, Keychain |
| Lỗi vận hành | Secret lọt vào log hoặc Git | Che dữ liệu, `.gitignore`, quét repo |
| Phụ thuộc bên thứ ba | Gói độc hại | Ghim phiên bản, rà soát trước khi cài |

**Ngoài phạm vi MVP:** kẻ tấn công đã kiểm soát tài khoản macOS của Chủ dự án.

**Loopback không phải là cơ chế xác thực.** Trình duyệt vẫn gửi được yêu cầu tới `127.0.0.1`.

## 2. Kiểm soát truy cập dashboard và API cục bộ

Áp dụng từ Phase 2 (API) và Phase 10 (dashboard).

- API và Streamlit bind `127.0.0.1`. Bind địa chỉ khác làm ứng dụng từ chối khởi động. Chưa có cấu hình mở LAN.
- **Allowlist Host:** chỉ `127.0.0.1:<port>` và `localhost:<port>`, để chống DNS rebinding.
- **Kiểm tra Origin** trên mọi yêu cầu thay đổi trạng thái; không bật CORS rộng.
- **Token API cục bộ:** sinh ngẫu nhiên khi cài đặt, lưu tệp quyền `0600` ngoài repo. Dashboard gửi token ở phía server; token không đi vào trình duyệt.
- Yêu cầu thay đổi trạng thái chỉ nhận JSON, không nhận form đơn giản.
- Giữ bảo vệ XSRF mặc định của Streamlit.
- **Phê duyệt** phải gửi kèm SHA-256 của artifact đang xem; server so khớp trước khi ghi nhận.
- `workspace/` quyền `0700`; DB, log, tệp token quyền `0600`.
- **Trước khi mở API ra LAN hoặc internet** phải có đặc tả xác thực, CSRF, TLS và được Chủ dự án duyệt. MVP không làm việc này.

## 3. OAuth

Phải hoàn tất đặc tả trước Phase 15. Khả năng của từng nền tảng phải xác minh riêng; không giả định.

- **Chỉ dùng loại OAuth client và luồng mà nhà cung cấp hỗ trợ cho ứng dụng cục bộ**, theo hồ sơ xác minh. Nếu nhà cung cấp không hỗ trợ luồng cục bộ, dừng và báo Chủ dự án; không tự thêm backend trung gian hay dịch vụ cloud.
- Mở đăng nhập trong trình duyệt hệ thống. Không dùng webview nhúng.
- **`state`:** ngẫu nhiên, mật mã mạnh, một lần dùng, có hạn, gắn với yêu cầu đang chờ. Sai hoặc thiếu `state` thì từ chối.
- **PKCE:** dùng `S256` ở mọi nền tảng hỗ trợ. Nền tảng không hỗ trợ thì ghi nhận lý do trong hồ sơ xác minh.
- **Callback:** URI đúng theo cách nhà cung cấp quy định, bind `127.0.0.1`. **Quy tắc cổng theo nhà cung cấp:** Google hướng dẫn dùng cổng ngẫu nhiên còn trống, trong khi một số nhà cung cấp yêu cầu đăng ký trước. Máy chủ callback chỉ sống trong thời gian ủy quyền và đóng ngay sau một lần nhận. Bản sửa 1 ghi "cổng cố định" là không đúng cho mọi nhà cung cấp.
- Mã ủy quyền, `state`, query string của callback không được ghi log.

**`client_secret` của ứng dụng cài cục bộ không phải là bí mật được bảo vệ.** Ứng dụng desktop là public client: secret nằm trên máy người dùng có thể bị trích xuất. Vì vậy:

- Bảo mật không được dựa vào `client_secret`. Lớp bảo vệ thực sự là PKCE, `state`, callback chính xác và token trong Keychain.
- Nếu nhà cung cấp cấp secret, giá trị vẫn nằm ngoài repo và ngoài log, lưu trong Keychain. Chủ dự án tự tạo và nhập; Claude không tạo và không tạo giá trị giả cho môi trường thật.
- Không nhúng secret vào bản phân phối. Nếu sau này phân phối ứng dụng, phải đánh giá lại riêng.

**Scope tối thiểu:** mỗi tính năng có bảng scope riêng, chỉ xin scope cần cho tính năng đó, xin khi cần. Tesla và Newton dùng ủy quyền tách biệt nếu nền tảng cho phép. Mọi scope đều phải lấy từ tài liệu chính thức đã xác minh; scope trong tài liệu này không có giá trị như một sự cấp quyền.

**Xác minh scope thực tế sau OAuth.** Người dùng có thể chỉ cấp một phần. Sau khi đổi token, so sánh scope thực nhận với scope yêu cầu:

- Thiếu scope bắt buộc: fail closed, tắt tính năng tương ứng, hiển thị rõ, không gọi API.
- Thừa scope: không dùng, cảnh báo, đề nghị ủy quyền lại với scope hẹp hơn.
- Lưu danh sách scope đã cấp (không lưu token) vào audit.
- Nền tảng không trả danh sách scope: ghi nhận trong hồ sơ xác minh và dùng cách kiểm tra chính thức khác nếu có.

## 4. Lưu trữ và thu hồi token

- Token lưu trong macOS Keychain, tách theo nền tảng và tài khoản. Không ghi ra đĩa dạng rõ, không lưu trong SQLite, không truyền qua dòng lệnh hoặc biến môi trường cho tiến trình con không cần.
- Lấy token trong thời gian ngắn nhất, chỉ ở adapter của Tesla hoặc Newton.
- **Token nhà cung cấp không bao giờ đi tới dashboard.** Không có API nào trả token. Không đặt token vào `st.session_state`, HTML, cookie hay thông báo lỗi. Dashboard chỉ nhận thông tin an toàn: đã kết nối, tên hiển thị, scope đã cấp, thời điểm hết hạn. Tiến trình Streamlit không có quyền đọc mục Keychain của token.
- **Ngắt kết nối** trên dashboard: gọi endpoint thu hồi của nền tảng nếu có, xóa khỏi Keychain, ghi audit. Nếu thu hồi từ xa thất bại, hiển thị rõ để người dùng thu hồi thủ công trên nền tảng. Phạm vi thu hồi có thể rộng hơn một token: Google ghi rằng thu hồi có thể làm mất hiệu lực mọi token của các client trong cùng dự án, nên hồ sơ xác minh phải ghi rõ hành vi này.
- Refresh thất bại thì dừng, chuyển người xử lý, không thử lặp vô hạn.
- Nghi ngờ lộ token: thu hồi, xoay vòng, ghi sự cố.

## 5. Che dữ liệu nhạy cảm trong log

- Logging theo **allowlist trường** khi có thể, không phải blocklist.
- Che: `Authorization`, `Cookie`, `access_token`, `refresh_token`, `code`, `state`, `client_secret`, API key, query string của URL, URL phiên upload.
- Áp dụng cho log, thông báo lỗi, traceback, dòng lệnh tiến trình con, bằng chứng xuất bản.
- Không log thân yêu cầu hay phản hồi của nền tảng khi chưa qua lọc.
- **Kiểm thử:** dùng giá trị canary ghi rõ là dữ liệu test, chạy luồng giả lập, quét log, DB và workspace. Giá trị canary không phải và không được trình bày như credentials thật.
- Trước mỗi lần đánh dấu phase hoàn thành, quét secret trong repo.

## 6. Hồ sơ quyền của asset

Mọi asset đi vào video đều có bản ghi. "Asset" gồm: nhạc, hiệu ứng âm thanh, font, hình ảnh, tài liệu nguồn, giọng, model sinh nội dung.

| Trường | Yêu cầu |
|---|---|
| `source_url` / nguồn gốc | Bắt buộc; tự tạo thì ghi rõ |
| `retrieved_at` | Ngày lấy |
| `rights_holder` | Chủ sở hữu |
| `license_name`, `license_version` | Bắt buộc, gồm phiên bản |
| `license_snapshot_path`, `license_snapshot_sha256` | Bản lưu điều khoản tại thời điểm lấy |
| `commercial_use` | `yes`, `no`, `unknown` |
| `derivatives_allowed` | `yes`, `no`, `unknown` |
| `attribution_required`, `attribution_text` | Văn bản ghi công cụ thể |
| `asset_version` | Phiên bản của asset; đổi nội dung là phiên bản mới, hồ sơ quyền phải xét lại |
| `asset_sha256` | Hash tệp đã dùng |
| `expires_at` | Nếu license có thời hạn |
| `reviewed_by`, `reviewed_at` | Người duyệt |

Với model và engine: thêm tên, phiên bản, hash; license của **code, model và giọng được đánh giá riêng**, vì có thể khác nhau.

## 7. Giọng và nhân bản giọng

- **Nhân bản giọng mặc định tắt.** Không có sự đồng ý thì không bật.
- Giọng nhân bản yêu cầu bằng chứng đồng ý của chủ giọng: danh tính, phạm vi sử dụng, mục đích thương mại, nền tảng, thời hạn, cách rút lại, tệp đồng ý và hash.
- Không nhân bản giọng người nổi tiếng hoặc bất kỳ ai không đồng ý, kể cả khi kỹ thuật cho phép.
- Giọng dựng sẵn cần hồ sơ quyền như asset, gồm ghi công nếu license yêu cầu.
- Đồng ý bị rút lại: chặn dùng mới và liệt kê các video đã dùng giọng đó để Chủ dự án quyết định.

## 8. Rights Gate (fail closed)

Rights Gate là một phần của QG5, **chạy lại ngay trước Tesla** theo đúng checksum gói xuất bản. Đây không phải Agent mới.

### Ranh giới bắt buộc của xuất bản

**Gói xuất bản** là bất biến: `package_manifest.json` liệt kê video, thumbnail, metadata và mọi asset đã dùng theo `asset_id`, `asset_version`, `asset_sha256`. `package_sha256` là hash của manifest này. Có một phiên bản gói cho mỗi thay đổi.

Dòng `publications` ở `queued` **chỉ được tạo** qua đúng một dịch vụ `enqueue_publication`, trong một transaction, khi đủ cả năm điều kiện:

| # | Điều kiện | Kiểm tra |
|---|---|---|
| 1 | Phê duyệt của con người còn hiệu lực | Có `approvals` mới nhất là chấp thuận, chưa bị thu hồi |
| 2 | Rights Gate đạt | Có `rights_reviews` đạt, không còn điều kiện chặn nào |
| 3 | Phê duyệt gắn đúng gói | `approvals.package_sha256` bằng `package_sha256` đang xuất bản |
| 4 | Quyền gắn đúng asset và phiên bản | Mọi asset trong manifest có hồ sơ quyền đúng `asset_version` và `asset_sha256` |
| 5 | Có ý định và đồng ý theo nền tảng | `publish_intents` hợp lệ cùng gói, theo yêu cầu của adapter |

**Kiểm tra lại ngay trước khi gửi.** Trong transaction `queued → uploading`, trước byte mạng đầu tiên, chạy lại cả năm điều kiện và tính lại hash tệp thực tế, cộng với: license chưa hết hạn, đồng ý giọng chưa bị rút, yêu cầu nền tảng chưa đổi. Không đạt thì chuyển `failed` với lý do `revalidation_failed`, run `BLOCKED`, không gửi gì.

**Không có đường vòng:**

- Adapter chỉ nhận `PublishGrant`, đối tượng chỉ `enqueue_publication` và bước kiểm tra lại tạo ra, gắn với `publication_id` và `package_sha256`. Adapter từ chối mọi lời gọi không có grant hợp lệ.
- API không có endpoint gọi trực tiếp adapter. Không có lệnh CLI, cờ debug hay biến môi trường để bỏ qua.
- Trigger SQLite từ chối dòng `publications` thiếu các khóa tham chiếu, như lớp thứ hai.
- Mã bên ngoài Tesla không import adapter; kiểm tra bằng test kiến trúc.
- Đăng lại có chủ đích cũng đi qua `enqueue_publication`.

**Thiếu hoặc không rõ đồng nghĩa với chặn.**

### Điều kiện chặn

Chặn xuất bản khi có bất kỳ điều kiện nào:

- Asset thiếu hồ sơ, thiếu trường bắt buộc, sai phiên bản, hoặc hash không khớp.
- `commercial_use` là `unknown`, hoặc là `no` với kênh có mục đích thương mại.
- `derivatives_allowed` là `unknown` hoặc `no` khi asset đã bị biến đổi.
- Yêu cầu ghi công nhưng metadata không có ghi công.
- License hết hạn.
- Giọng nhân bản thiếu đồng ý hợp lệ.
- Thiếu người duyệt quyền.

**Thiếu hoặc không rõ đồng nghĩa với chặn.** Phê duyệt của con người không vượt qua được Rights Gate; muốn đi tiếp phải bổ sung hồ sơ hoặc thay asset. Kết luận tự động chỉ nói hồ sơ đầy đủ, không phải ý kiến pháp lý.

## 9. Checklist phê duyệt của con người

Trước khi duyệt, người xem xác nhận: nội dung đúng sự thật; không vi phạm quyền; ghi công đúng; đã đặt nhãn nội dung AI theo chính sách hiện hành của nền tảng; đúng thiết lập đối tượng khán giả; đúng tài khoản đích.

## 10. Tiêu chí nghiệm thu

| Mã | Tiêu chí | Phase |
|---|---|---|
| AC-S1 | Yêu cầu sai Host, sai Origin hoặc thiếu token bị từ chối | 2 |
| AC-S2 | Ứng dụng từ chối bind ngoài loopback | 2 |
| AC-S3 | Quét canary không tìm thấy secret | 2, 15 |
| AC-S4 | Sai, thiếu hoặc dùng lại `state` bị từ chối | 15 |
| AC-S5 | Không có token ngoài Keychain | 15 |
| AC-S6 | Ngắt kết nối gọi thu hồi và xóa token | 15 |
| AC-S7 | Thiếu scope bắt buộc thì tính năng tắt, không gọi API | 15 |
| AC-S8 | Không có token trong phản hồi API, trạng thái dashboard hay HTML | 15 |
| AC-S9 | Bảo mật không phụ thuộc tính bí mật của `client_secret` | 15 |
| AC-R1 | Mỗi điều kiện ở mục 8 đều chặn được xuất bản, có test riêng | 13 |
| AC-R2 | Sửa asset sau khi duyệt làm mất hiệu lực phê duyệt | 13 |
| AC-R3 | Không có đường nào vượt qua Rights Gate | 13 |
| AC-R4 | Không thể tạo `queued` khi thiếu một trong năm điều kiện, có test cho từng điều kiện | 13 |
| AC-R5 | Phê duyệt gói phiên bản cũ không xuất bản được gói phiên bản mới | 13 |
| AC-R6 | Kiểm tra lại phát hiện asset đổi, license hết hạn, đồng ý bị rút sau khi `queued` và không gửi byte nào | 15 |
| AC-R7 | Gọi adapter không có `PublishGrant` hợp lệ bị từ chối | 15 |
| AC-R8 | Chèn trực tiếp dòng `publications` thiếu tham chiếu bị trigger từ chối | 13 |
