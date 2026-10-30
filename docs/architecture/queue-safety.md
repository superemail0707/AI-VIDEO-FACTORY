# Đặc tả an toàn Job Queue

| Hạng mục | Trạng thái |
|---|---|
| Tài liệu đặc tả | Đã viết (Bản sửa 3) |
| Thiết kế | `Proposed` (D-011, D-018) |
| Duyệt của Chủ dự án | **Chờ, bắt buộc trước Phase 2** |
| Triển khai | Chưa làm |
| Kiểm thử | Chưa làm |

> **Chưa thể tuyên bố queue an toàn.** Tài liệu này mô tả điều phải đúng và cách kiểm tra. Tính an toàn chỉ được chứng minh sau khi triển khai và chạy các bài kiểm thử ở mục 13.
> Các giá trị thời gian là giá trị khởi điểm chưa đo, được hiệu chỉnh ở Phase 2.

## 1. Mục tiêu và mô hình lỗi

**Bất biến cần giữ:**

1. **Không ghi đè kết quả mới:** worker cũ hoặc bị thay thế không làm thay đổi trạng thái job, trạng thái run hay artifact hiện hành.
2. **Không mất kết quả đã commit:** job `succeeded` luôn trỏ đến artifact tồn tại và khớp checksum.
3. **Không lộ dữ liệu dở dang:** bên đọc chỉ thấy artifact đã commit hoàn chỉnh.
4. **Luôn phục hồi được:** mỗi job đi tới trạng thái kết thúc hoặc được chuyển cho người xử lý.
5. **Không chồng tác vụ nặng:** không tác vụ nặng mới nào bắt đầu khi tác vụ cũ, kể cả mồ côi, còn sống.

**Lỗi được tính đến:** tiến trình bị kill, tiến trình con mồ côi, tiến trình bị treo hoặc tạm dừng, máy ngủ, đồng hồ nhảy tiến hoặc lùi, đĩa đầy, `SQLITE_BUSY`, mất điện.

Hệ thống cung cấp **at-least-once execution, exactly-once commit**: một job có thể chạy nhiều lần, nhưng chỉ một lần chạy được commit. Thao tác có tác dụng phụ bên ngoài không thể bị fencing thu hồi, nên Tesla có quy tắc riêng ở mục 9.

## 2. Mô hình tiến trình

- **Một Worker duy nhất:** Worker giữ `flock` trên `workspace/run/worker.lock`. Tệp này mở với close-on-exec, nên tiến trình con không kế thừa. Không lấy được khóa thì Worker thoát.
- **Supervisor và tiến trình con:** supervisor giữ kết nối DB, heartbeat, watchdog và commit. Mỗi tác vụ chạy trong tiến trình con có session và process group riêng. Tiến trình con **không có quyền ghi DB**, chỉ ghi vào thư mục staging của mình.
- **Khóa tác vụ nặng:** `workspace/run/heavy.lock`, xem mục 11. Mọi tiến trình con của job đều giữ khóa này.
- Nhiều worker nằm ngoài phạm vi MVP. Fencing vẫn bắt buộc như lớp bảo vệ độc lập, phòng khi khóa singleton bị phá, ví dụ tệp khóa bị di chuyển.

## 3. Mô hình dữ liệu

| Trường của `jobs` | Ý nghĩa |
|---|---|
| `state` | `queued`, `running`, `succeeded`, `dead`, `cancelled` |
| `lease_generation` | Fencing token, tăng đơn điệu, không bao giờ giảm hoặc dùng lại |
| `lease_owner` | Mã phiên worker, chỉ phục vụ chẩn đoán, không dùng để phân quyền |
| `lease_expires_at` | Mốc hiển thị job có thể đã đình trệ; xem mục 7 |
| `failure_count` | Số lần thất bại do chính tác vụ, tính vào ngân sách retry |
| `recovery_count` | Số lần bị thu hồi do hạ tầng, có giới hạn riêng |
| `next_run_at` | Thời điểm sớm nhất được chạy lại |

`job_attempts` có một dòng cho mỗi lần chạy, khóa duy nhất `(job_id, generation)`, gồm `outcome` (`running`, `succeeded`, `failed`, `abandoned`, `superseded`, `cancelled`), `pgid`, thời điểm khởi động tiến trình, đường dẫn thực thi và `attempt_token`.

## 4. Nhận job

Trong một transaction `BEGIN IMMEDIATE`:

1. Chọn job có `state = 'queued'` và `next_run_at <= now`.
2. Đặt `state = 'running'`, `lease_generation = lease_generation + 1`, `lease_owner`, `lease_expires_at`.
3. Thêm dòng `job_attempts` với generation mới.

Điều kiện trước khi nhận: giữ được `heavy.lock` và hàng đợi không ở chế độ tạm dừng. **Mỗi lần chạy có generation riêng.** Generation chỉ tăng trong transaction này.

## 5. Quy tắc commit có điều kiện (fencing)

Mọi thao tác ghi của worker lên `jobs`, `runs`, `scenes`, `artifacts`, `artifact_heads` đều nằm trong transaction `BEGIN IMMEDIATE` có kiểm tra:

```sql
UPDATE jobs SET ... WHERE id = :job_id AND lease_generation = :g AND state = 'running';
-- 1 dòng: tiếp tục transaction.
-- 0 dòng: ROLLBACK, xem xử lý bên dưới.
```

- Kiểm tra và ghi nằm trong **cùng một transaction**. Kiểm tra trước rồi ghi sau là không hợp lệ.
- Luôn dùng `BEGIN IMMEDIATE` cho transaction ghi, không nâng cấp từ giao dịch đọc, để tránh lỗi snapshot.
- **Quyền lực nằm ở generation, không nằm ở đồng hồ.** Lease quá hạn nhưng generation còn khớp thì vẫn được commit.
- **Commit là idempotent.** Khi cập nhật ảnh hưởng 0 dòng, đọc `job_attempts(job_id, g)`: nếu `outcome` đã là kết quả cuối thì lần trước đã thành công, coi như xong. Nếu chưa thì generation đã mất quyền: đánh dấu `superseded`, không ghi gì thêm.
- Heartbeat dùng cùng điều kiện. Heartbeat ảnh hưởng 0 dòng nghĩa là đã mất quyền: dừng tiến trình con, không ghi gì thêm.
- Factory Manager cập nhật trạng thái run **trong cùng transaction** với commit job.

## 6. Staging và promote artifact

```text
workspace/runs/<run_id>/staging/<job_id>/g<generation>/     # chỉ attempt này ghi
workspace/runs/<run_id>/committed/<job_id>/g<generation>/   # bất biến sau khi promote
```

Trình tự commit:

1. Tiến trình con ghi toàn bộ đầu ra vào staging, gồm `manifest.json` có SHA-256 từng tệp.
2. Supervisor xác minh manifest, schema và checksum.
3. **Flush:** đẩy dữ liệu xuống đĩa bằng `F_FULLFSYNC`.
4. **Rename:** đổi tên thư mục staging sang `committed/<job_id>/g<generation>/`, rồi flush thư mục cha.
5. **Con trỏ DB:** transaction fencing thêm dòng `artifacts`, cập nhật `artifact_heads`, đặt job `succeeded`, cập nhật run.

**Điểm commit duy nhất là bước 5.** Rename ở bước 4 không ghi đè được kết quả mới vì đường dẫn chứa generation riêng. Crash trước bước 5 để lại dữ liệu mồ côi mà bên đọc không thấy.

**Quy tắc đọc:** artifact chỉ được tìm qua DB. Không suy đoán đường dẫn, không quét thư mục. Job sau xác minh checksum đầu vào.

**Điều kiện an toàn:**

- `rename` chỉ nguyên tử trên cùng một volume. Worker kiểm tra `staging/` và `committed/` cùng volume khi khởi động, nếu không thì từ chối chạy.
- SQLite bật `PRAGMA fullfsync=ON` và `synchronous=FULL`. Chi phí được đo ở Phase 2.
- Workspace và SQLite phải nằm trên volume APFS cục bộ.
- Artifact đã commit là bất biến. Render lại một cảnh tạo generation mới và đổi con trỏ.
- Nội dung đổi nghĩa là checksum đổi, nên phê duyệt cũ không còn hiệu lực.

**Dữ liệu mồ côi** không bị tự động xóa. Worker lập danh sách, dashboard hiển thị dung lượng, việc dọn cần người xác nhận theo D-016.

## 7. Lease, heartbeat, retry

| Tham số | Khởi điểm |
|---|---|
| Chu kỳ heartbeat | 15 giây |
| TTL lease | 120 giây |
| `max_failures` | 3 |
| `max_recoveries` | 3 |
| Backoff tác vụ | 30 giây × 2^n, tối đa 15 phút |
| `busy_timeout` SQLite | 5 giây |
| Ngân sách BUSY | 8 lần thử, backoff 250 ms × 2^n, tối đa 8 giây |
| Giới hạn tạm dừng do DB | 30 phút, thăm dò mỗi 30 giây |
| Hạn chờ orphan | 5 phút |
| Ngưỡng phát hiện đồng hồ lùi | 5 giây |

**Ý nghĩa của lease.** Vì MVP có một Worker, **việc thu hồi job chỉ xảy ra trong phục hồi lúc khởi động**, sau khi đã giữ `worker.lock`. Khi đang chạy, `lease_expires_at` không kích hoạt thu hồi. API dùng nó để suy ra trạng thái hiển thị `stalled` (`running` và quá hạn). Đây là giá trị suy ra, không phải trạng thái lưu.

**Heartbeat chứng minh supervisor còn sống, không chứng minh công việc đang chạy.** **Watchdog tiến độ** độc lập dừng process group khi quá thời gian không có tiến độ hoặc vượt `max_runtime`, tính là lỗi tạm thời. Watchdog dùng đồng hồ monotonic trong tiến trình, nên không bị ảnh hưởng khi đồng hồ hệ thống đổi.

| Phân loại kết quả | Hành động | Tính vào |
|---|---|---|
| Thành công | Commit | – |
| Lỗi tạm thời của tác vụ | `queued`, có backoff; hết ngân sách thì `dead` | `failure_count` |
| Đầu vào sai | `dead`, không retry | – |
| Tranh chấp DB | Mục 10 | Không tính |
| Hạ tầng (đĩa, thiếu bộ nhớ, DB hỏng) | Tạm dừng hàng đợi, thông báo | Không tính |
| Mất quyền | Attempt `superseded`, không ghi gì | – |
| Thu hồi lúc khởi động | `queued`, không backoff | `recovery_count` |

Hết `max_recoveries` nghĩa là job có thể đang làm chết worker: chuyển `dead`, run chuyển `BLOCKED`. Ngủ máy thông thường không làm cạn ngân sách retry của tác vụ.

## 8. Phục hồi

### Mac ngủ

Không dựa vào việc ngăn máy ngủ. Khi thức dậy:

1. Supervisor thấy khoảng trống heartbeat, ghi sự kiện `sleep_detected`.
2. Gửi heartbeat. Thành công thì tiếp tục. Tiến trình con kiểm tra lại kết nối Ollama; lỗi kết nối là lỗi tạm thời.
3. Heartbeat ảnh hưởng 0 dòng: dừng tiến trình con, attempt `superseded`, không ghi gì.

### Worker khởi động lại

1. Giữ `worker.lock`. Việc giữ được khóa chứng minh không còn supervisor nào khác sống, nên có thể xử lý ngay, không cần chờ TTL.
2. Xử lý tiến trình con cũ theo mục 11. **Chưa giữ được `heavy.lock` thì không làm gì với job.**
3. Xử lý `pending_outcome` theo mục 10.
4. Với job `running` còn lại: trong transaction, đánh dấu attempt `abandoned`, đặt `queued`, tăng `recovery_count`. Generation không đổi ở đây; điều kiện `state = 'running'` đã chặn worker cũ, và generation tăng ở lần nhận tiếp theo.
5. Gửi yêu cầu giải phóng model của Ollama, vì Ollama là daemon riêng và có thể vẫn giữ model trong RAM.
6. Chạy bước kẹp `next_run_at` (mục "Đồng hồ"), quét dữ liệu mồ côi, bắt đầu vòng lặp.

### Worker dừng có kiểm soát

Khi nhận SIGTERM: ngừng nhận job mới, dừng tiến trình con, trả job về `queued` không tính lỗi.

### Đồng hồ

- **Nhảy tiến:** lease hiển thị `stalled` sớm. Không ảnh hưởng an toàn vì không có thu hồi khi đang chạy.
- **Nhảy lùi:** `lease_expires_at` và `next_run_at` trở nên xa hơn thực tế. Heartbeat vẫn ghi đè `lease_expires_at`. Phục hồi lúc khởi động không dựa vào TTL. Thứ tự sự kiện dựa vào `audit_log.seq`, không dựa vào thời gian.

**Xử lý đồng hồ lùi khi Worker đang sống.** Vòng lặp supervisor chạy cả hai bước sau ở mỗi chu kỳ, **kể cả khi đang chạy job**, không cần khởi động lại:

1. **Phát hiện và dịch lịch.** So sánh mức tăng đồng hồ thực với mức tăng đồng hồ monotonic kể từ mốc gần nhất. Đồng hồ thực tăng ít hơn monotonic quá ngưỡng thì có đồng hồ lùi một khoảng `delta`. Trong một transaction: trừ `delta` khỏi `next_run_at` của mọi job `queued`, ghi `clock_regression`, rồi cập nhật mốc. Nhờ vậy thời gian chờ còn lại được giữ nguyên. Gặp BUSY thì **không cập nhật mốc**, nên chu kỳ sau thử lại đúng `delta`, và lịch không bị dịch hai lần.
2. **Kẹp không phụ thuộc phát hiện.** `next_run_at` lớn hơn `now + backoff tối đa` được đặt về mức đó. Bước này là lưới an toàn cho trường hợp không phát hiện được, ví dụ đồng hồ đổi khi máy đang ngủ, hoặc khi Worker chưa chạy. Lúc khởi động chỉ có bước này, vì chưa có mốc so sánh.

Kết quả: sau khi đồng hồ lùi, job không bao giờ chờ quá backoff tối đa, và trường hợp phát hiện được thì chỉ chờ phần còn lại.

### Mất điện

SQLite tự phục hồi WAL. Xử lý như worker crash. `flock` tự mất khi máy khởi động lại.

## 9. Ngoại lệ: tác dụng phụ bên ngoài

Fencing không thu hồi được một yêu cầu đã gửi tới nền tảng. Job Tesla **không bao giờ tự động chạy lại** sau khi mất quyền hoặc crash khi `uploading`; bản ghi xuất bản chuyển `unknown`. Xem [publishing-reliability.md](publishing-reliability.md).

## 10. Xử lý `SQLITE_BUSY`

### 10.1 Phân biệt tranh chấp DB với lỗi job

| Tín hiệu | Phân loại | Xử lý |
|---|---|---|
| Mã lỗi `SQLITE_BUSY`, `SQLITE_LOCKED` kể cả mã mở rộng | Tranh chấp DB | Mục này. **Không phải lỗi job** |
| `SQLITE_FULL`, `SQLITE_IOERR`, `SQLITE_CORRUPT`, `SQLITE_CANTOPEN` | Hạ tầng | Tạm dừng ngay, không retry tự động |
| Tiến trình con thoát lỗi hoặc xác minh thất bại | Lỗi tác vụ | `failure_count` |

Phân loại dựa trên **mã lỗi SQLite của kết nối supervisor**, không dựa vào chuỗi thông báo. Tiến trình con không chạm DB, nên kết quả tác vụ và tình trạng DB tách biệt hoàn toàn. `failure_count` không bao giờ tăng vì tranh chấp DB.

### 10.2 Hành vi theo loại thao tác

| Thao tác | Khi BUSY | Hết ngân sách |
|---|---|---|
| Nhận job | Bỏ qua, thử ở vòng sau | Không có gì thay đổi |
| Heartbeat | Thử ở chu kỳ sau. Tiến trình con tiếp tục, vì không ghi được không có nghĩa là mất quyền | Ghi nhật ký, tiếp tục; hàng đợi không nhận job mới |
| Commit hoặc báo lỗi tác vụ | Thử lại với ngân sách BUSY | Mục 10.3 |
| Yêu cầu API (hủy, phê duyệt) | Thử trong `busy_timeout` | Trả 503 kèm `Retry-After`; **không báo thành công** |

**Mỗi lần thử lại là một transaction mới từ đầu**, chạy lại toàn bộ kiểm tra fencing theo mục 5. Không được dùng lại kết quả kiểm tra của lần trước.

### 10.3 Khi hết ngân sách: dừng để phục hồi, không requeue

**Worker không requeue.** Requeue cần đúng khóa ghi đang bị chặn, nên không thể thực hiện, và sẽ bỏ phí công việc đã xong. Thứ tự xử lý:

1. Tiến trình con đã kết thúc; kết quả nằm trong `committed/.../g<generation>/`, hoặc là một lỗi đã phân loại.
2. Ghi nguyên tử và flush `workspace/run/pending/<job_id>.g<generation>.json` theo schema ở mục 10.4. Tệp này chỉ là **ý định, không phải sự thật**.
3. Chuyển sang chế độ **tạm dừng do DB:** không nhận job mới, ghi `workspace/run/worker-status.json` để API hiển thị, ghi sự kiện vào `workspace/run/journal.jsonl`.
4. Thăm dò DB theo chu kỳ. DB hoạt động lại thì chạy transaction commit đầy đủ, gồm fencing.
5. Hết giới hạn tạm dừng: Worker thoát với mã riêng. Job vẫn `running` trong DB, phần tiếp theo do Worker khởi động sau xử lý.

Sự kiện trong nhật ký được chuyển vào `audit_log` khi DB ghi được, có mã sự kiện duy nhất để không ghi trùng.

### 10.4 Phục hồi `pending_outcome` khi khởi động

**Schema của `pending_outcome`.** Mọi tệp có `job_id`, `generation`, `outcome_kind`, thời điểm. Hai loại có yêu cầu khác nhau:

| `outcome_kind` | Trường bắt buộc | Yêu cầu artifact |
|---|---|---|
| `success` | `manifest_sha256` | **Bắt buộc:** thư mục `committed/.../g<generation>/`, manifest và mọi checksum khớp |
| `failure` | `failure_class` (`transient` hoặc `invalid_input`), `error_code`, thông điệp đã che dữ liệu nhạy cảm | **Không yêu cầu.** Lỗi có thể xảy ra trước khi có manifest |

**Phục hồi.** Sau khi có `heavy.lock`, với mỗi tệp `pending`, kiểm tra theo thứ tự:

1. **Fencing (cả hai loại):** generation hiện hành và `state = 'running'`. Không khớp: không áp dụng; attempt `superseded` nếu chưa có kết quả cuối.
2. **Tính hợp lệ theo loại:**
   - `success`: như bảng trên. Đạt thì áp dụng T6.
   - `failure`: schema hợp lệ, `job_id` và `generation` khớp tên tệp, `failure_class` thuộc tập cho phép. Đạt thì áp dụng T11.
3. **Không hợp lệ** (tệp hỏng, thiếu trường, sai checksum): không áp dụng, đi theo luồng thu hồi T7.

**Quy tắc bắt buộc:**

- Tệp `failure` **không bao giờ** dẫn tới `succeeded`, kể cả khi có artifact trong staging.
- Tệp `success` không hợp lệ **không được diễn giải thành `failure`**, vì lỗi hạ tầng không phải lỗi tác vụ; nó đi theo T7.
- **Idempotent:** kết quả được áp dụng trong transaction fencing, cùng với `outcome` của attempt. Áp dụng lại khi attempt đã có kết quả cuối là thao tác rỗng, nên bộ đếm không tăng hai lần.

Tệp `pending` được đổi tên sang `processed/` sau khi xử lý, không xóa. Crash giữa lúc áp dụng và lúc đổi tên chỉ khiến tệp được xử lý lại như một thao tác rỗng.

### 10.5 Chuyển trạng thái và sự kiện audit

| # | Tình huống | `jobs.state` | `attempt.outcome` | Bộ đếm | Sự kiện |
|---|---|---|---|---|---|
| T1 | BUSY rồi commit được trong ngân sách | `running → succeeded` | `succeeded` | – | `db_busy_retry` (chỉ log), `job_committed` |
| T2 | Hết ngân sách | `running`, không đổi | `running` | – | `db_busy_exhausted`, `queue_paused` (nhật ký) |
| T3 | DB phục hồi, generation hiện hành | `running → succeeded` | `succeeded` | – | `queue_resumed`, `job_commit_delayed` |
| T4 | DB phục hồi, generation không hiện hành | Không đổi | `superseded` | – | `job_commit_rejected` |
| T5 | Hết giới hạn tạm dừng | `running`, không đổi | `running` | – | `worker_stopped_for_recovery` (nhật ký) |
| T6 | Khởi động, `pending` loại `success` hợp lệ | `running → succeeded` | `succeeded` | – | `pending_outcome_recovered` |
| T7 | Khởi động, `pending` không hợp lệ hoặc không có | `running → queued` | `abandoned` | `recovery_count + 1` | `pending_outcome_rejected` (nếu có tệp), `job_requeued_after_recovery` |
| T8 | Lỗi tác vụ được ghi muộn, **Worker vẫn sống** | `running → queued` hoặc `dead` | `failed` | `failure_count + 1`, đúng một lần | `job_failed`, `job_commit_delayed` |
| T9 | Hết `max_recoveries` | `running → dead`, run `BLOCKED` | `abandoned` | – | `job_dead_recovery_limit` |
| T10 | Lỗi hạ tầng DB | `running`, không đổi | `running` | – | `db_infrastructure_error`, `queue_paused` |
| T11a | Khởi động, `pending` loại `failure`, lớp `transient`, còn ngân sách | `running → queued`, có backoff | `failed` | `failure_count + 1`; `recovery_count` không đổi | `pending_outcome_recovered`, `job_failed` |
| T11b | Như T11a, hết ngân sách | `running → dead`, run `BLOCKED` | `failed` | `failure_count + 1` | `pending_outcome_recovered`, `job_failed`, `job_dead_failure_limit` |
| T11c | Khởi động, `pending` loại `failure`, lớp `invalid_input` | `running → dead`, run `BLOCKED` | `failed` | Không đổi | `pending_outcome_recovered`, `job_failed` |

**Không có đường nào đặt `succeeded` khi chưa có transaction commit thành công.** Tệp `pending` và thư mục `committed/` đều không đủ để coi là thành công.

### 10.6 Vì sao job không thể kẹt ở `running` vĩnh viễn

Job `running` chỉ có thể ở một trong ba tình huống:

| Tình huống | Điều gì kết thúc nó |
|---|---|
| Worker sống, tác vụ đang chạy | Hoàn tất, watchdog, hoặc `max_runtime` |
| Worker sống, tạm dừng do DB | DB phục hồi, hoặc hết giới hạn và Worker thoát |
| Không có Worker | Lần khởi động Worker tiếp theo, luôn xử lý mọi job `running`, kết thúc bằng T6, T7, T9 hoặc T11 |

**Giới hạn thật:** nếu không ai khởi động Worker, hoặc tiến trình ngoài giữ khóa DB vô thời hạn, job vẫn `running`. Hệ thống không tự sửa được hai trường hợp này. Nó hiển thị `stalled` và yêu cầu người xử lý. Việc tự khởi động Worker khi đăng nhập được xem xét ở Phase 2.

## 11. Tiến trình con mồ côi

### 11.1 Ba lớp bảo vệ

1. **Dây sinh tồn:** supervisor giữ đầu ghi của một pipe, tiến trình con giữ đầu đọc. Supervisor chết thì pipe đóng; tiến trình con dừng cả process group trong vài giây. Lớp này bao gồm cả trường hợp crash trước khi kịp ghi PID.
2. **`heavy.lock` là nguồn sự thật về tác vụ nặng:** tiến trình con giữ `flock` trên tệp này và truyền mô tả tệp cho mọi tiến trình cháu như FFmpeg. `flock` gắn với mô tả tệp mở, nên **khóa chỉ được nhả khi mọi tiến trình giữ nó đã thoát**. Vì vậy phát hiện orphan **không cần đoán theo PID**. Bắt buộc dùng `flock(2)`, không dùng khóa `fcntl` vì khóa đó không được kế thừa.
3. **Giới hạn đĩa:** `RLIMIT_FSIZE` theo loại job được đặt trên tiến trình con và được kế thừa; hết giới hạn thì lần ghi thất bại ở cấp hệ điều hành. Supervisor giám sát kích thước staging.

**Quy tắc cứng:** không giữ được `heavy.lock` thì không tác vụ nặng nào được chạy. **Không có tùy chọn bỏ qua khóa này.**

Tác vụ không phải tiến trình con, tức yêu cầu đang xử lý trong Ollama, không được lớp 2 bảo vệ. Vì vậy Worker gửi yêu cầu giải phóng model khi khởi động lại, và Phase 1 đo thêm việc này.

### 11.2 Nhận diện và dừng

Mỗi attempt ghi `pgid`, thời điểm khởi động tiến trình, đường dẫn thực thi và `attempt_token` trong tham số dòng lệnh.

Chỉ gửi tín hiệu khi **tất cả** đều khớp. PID có thể được hệ điều hành dùng lại, nên PID đơn lẻ không đủ. Trình tự: SIGTERM tới process group, chờ 10 giây, SIGKILL, chờ `heavy.lock` tối đa 30 giây.

### 11.3 Bảng quyết định lúc khởi động

| # | Tình huống | Hành động | Kết quả job | Phục hồi |
|---|---|---|---|---|
| O1 | `heavy.lock` lấy được ngay | Không có orphan | Theo mục 10.4 và 8 | Tự động |
| O2 | Khóa bị giữ, orphan nhận diện được, dừng thành công | Dừng, lấy khóa | `queued`, `recovery_count + 1` | Tự động |
| O3 | Khóa bị giữ, không nhận diện được hoặc không khớp đủ | **Không gửi tín hiệu.** Chờ hết hạn chờ orphan vì dây sinh tồn có thể tự giải quyết | Giữ `running`, hàng đợi tạm dừng | Tự động nếu orphan tự thoát |
| O4 | O3 hết hạn chờ | Thông báo cần can thiệp | Giữ `running`, run `BLOCKED` khi ghi được | **Thủ công** |
| O5 | Đã SIGKILL nhưng khóa vẫn bị giữ | Như O4 | Như O4 | **Thủ công** |
| O6 | Đĩa dưới ngưỡng khi còn orphan | Thông báo khẩn. Không xóa dữ liệu | Như O4 | **Thủ công** |

**Can thiệp thủ công:** dashboard hiển thị tiến trình đang giữ `heavy.lock`, lấy từ `lsof`, nếu xác định được. Người dùng dừng tiến trình đó hoặc khởi động lại máy, rồi bấm "Kiểm tra lại". Nút này **chỉ tiếp tục khi `heavy.lock` thực sự lấy được**; nó không có quyền bỏ qua kiểm tra. Khởi động lại máy luôn giải phóng khóa.

### 11.4 Tiếp tục, requeue hay can thiệp

| Quyết định | Điều kiện |
|---|---|
| **Tiếp tục** (chỉ ghi kết quả đã có, không chạy lại) | Có `pending_outcome` hợp lệ theo mục 10.4, generation hiện hành, có `heavy.lock` |
| **Requeue** | Có `heavy.lock`, generation hiện hành, không có kết quả hợp lệ, chưa hết `max_recoveries`, job không phải Tesla |
| **Can thiệp thủ công** | Không lấy được `heavy.lock` sau hạn chờ; hết `max_recoveries`; orphan khi đĩa dưới ngưỡng |
| **Không bao giờ requeue** | Job Tesla khi `uploading`: chuyển `unknown` |

Hệ thống **không bao giờ gắn lại** với tiến trình con cũ. "Tiếp tục" chỉ có nghĩa là commit một kết quả đã hoàn tất. Quyết định chỉ chạy sau khi có `heavy.lock`, nên requeue không thể tạo chồng tác vụ.

### 11.5 Chặn đĩa tăng không kiểm soát

- Dây sinh tồn chặn phần lớn trường hợp.
- `RLIMIT_FSIZE` giới hạn từng tệp, kể cả với orphan không nhận diện được.
- Khi phục hồi, thư mục staging của generation cũ chuyển sang chỉ đọc, chặn tạo tệp mới. Tệp đã mở vẫn ghi được cho tới giới hạn `RLIMIT_FSIZE`.
- Kiểm tra dung lượng trống mỗi chu kỳ trong khi còn orphan.

**Giới hạn thật:** orphan không nhận diện được bị giới hạn chứ không bị dừng. Khi đó cần người xử lý.

## 12. Tiêu chí nghiệm thu (Phase 2–3)

| Mã | Tiêu chí |
|---|---|
| AC-Q1 | `lease_generation` tăng nghiêm ngặt; không có hai attempt cùng generation |
| AC-Q2 | Mọi đường ghi của worker có điều kiện generation; rà soát code xác nhận không có ngoại lệ |
| AC-Q3 | Worker cũ không thể đổi job, run, scene, artifact hay con trỏ hiện hành |
| AC-Q4 | Bên đọc không bao giờ thấy artifact dở dang |
| AC-Q5 | Mọi job `succeeded` trỏ đến artifact tồn tại và đúng checksum |
| AC-Q6 | Chỉ một Worker chạy tại một thời điểm |
| AC-Q7 | Sau mọi lỗi ở mục 13, job kết thúc hoặc ở trạng thái chờ người có thông báo; không có job kẹt mà không hiển thị |
| AC-Q8 | Ngủ máy và tranh chấp DB không làm tăng `failure_count` |
| AC-Q9 | Không kịch bản phục hồi nào tự động xóa dữ liệu |
| AC-Q10 | Không có đường nào đặt `succeeded` ngoài transaction commit fencing |
| AC-Q11 | Mỗi lần thử lại sau BUSY chạy lại kiểm tra fencing |
| AC-Q12 | Mỗi chuyển trạng thái T1–T10 tạo đúng sự kiện audit, không trùng |
| AC-Q13 | Không bao giờ có hai tác vụ nặng chạy cùng lúc, kể cả khi có orphan |
| AC-Q14 | Không gửi tín hiệu tới tiến trình không khớp đủ nhận diện |
| AC-Q15 | Orphan không nhận diện được chặn hàng đợi và yêu cầu người xử lý |
| AC-Q16 | "Kiểm tra lại" không thể vượt qua `heavy.lock` |
| AC-Q17 | Một tệp của orphan không vượt quá `RLIMIT_FSIZE` |
| AC-Q18 | `pending` loại `failure` được áp dụng không cần artifact, không dẫn tới `succeeded`, tăng đúng bộ đếm đúng một lần |
| AC-Q19 | Sau khi đồng hồ lùi, job không chờ quá backoff tối đa; khi Worker sống, không cần khởi động lại |

## 13. Bộ kiểm thử fault injection

Chạy ở cấp tích hợp với SQLite thật và tác vụ giả có thể điều khiển. Điểm lỗi được cài qua hook kiểm thử. **"Bằng chứng" dưới đây là điều kiện kiểm tra, chưa phải kết quả đã đạt.** Mọi kiểm thử đều chưa chạy.

**Oracle kiểm tra sau mọi bài:**

| Mã | Điều kiện | Chống |
|---|---|---|
| OR1 | Mỗi job có tối đa một attempt `succeeded` | Commit trùng |
| OR2 | Mỗi vị trí `artifact_heads` trỏ đúng artifact của attempt `succeeded`, checksum khớp | Dữ liệu hỏng |
| OR3 | Mỗi job khi kết thúc bài ở trạng thái cuối, hoặc `queued`, hoặc `running` có thông báo chờ người | Kẹt không hiển thị |
| OR4 | Sau phục hồi, không job `running` nào không có chủ, trừ OR3 | Kẹt vĩnh viễn |
| OR5 | Bộ đếm và sự kiện audit đúng theo bảng T | Sai kế toán |
| OR6 | Không có tệp nào bị xóa; không có hai tác vụ nặng chồng nhau | Mất dữ liệu, chồng tải |

| Mã | Trạng thái đầu | Lỗi tiêm | Job cuối | Artifact cuối | Phục hồi | Bằng chứng riêng | Phase |
|---|---|---|---|---|---|---|---|
| FI-01 | A chạy g1, bị thu hồi, B xong g2 | A cố commit | `succeeded` (g2) | Head trỏ g2 | Tự động | Commit A 0 dòng, attempt g1 `superseded` | 2 |
| FI-02 | A g1 và B g2 cùng chạy | A xong sau B | `succeeded` (g2) | Head g2, g1 mồ côi | Tự động | Như FI-01 | 2 |
| FI-03 | A g1 đã bị thay | A heartbeat | Theo B | Không đổi | Tự động | 0 dòng, A dừng con | 2 |
| FI-04 | Một job `queued`, hai bên nhận, lặp 1.000 lần | Tranh nhận | `running`, một chủ | Không có | Tự động | Generation duy nhất | 2 |
| FI-05 | Worker chạy, không bị thu hồi | `SIGSTOP` quá TTL, `SIGCONT` | `succeeded` | Head trỏ g1 | Tự động | Late commit hợp lệ | 2 |
| FI-06 | Như FI-05 | Harness thu hồi trong lúc dừng | Theo attempt mới | Head không trỏ g1 | Tự động | A không ghi được | 2 |
| FI-07 | Job `running` | `SIGKILL` Worker, con đã thoát | `queued` rồi `succeeded` | Head trỏ g2 | Tự động | `recovery_count = 1`, attempt g1 `abandoned` | 2 |
| FI-08 | Job `running`, con sống | `SIGKILL` Worker | `queued` rồi `succeeded` | Head g2, staging g1 mồ côi | Tự động | Con tự dừng qua dây sinh tồn trước khi g2 bắt đầu | 2 |
| FI-09 | Con đang ghi staging | Crash | `queued` rồi `succeeded` | Head g2, staging g1 dở dang không hiển thị | Tự động | Không có dòng `artifacts` của g1 | 2 |
| FI-10 | Rename xong | **Crash sau rename, trước con trỏ DB** | `queued` rồi `succeeded` | Head g2, `committed/g1` mồ côi | Tự động | Không có dòng DB nào trỏ g1 | 2 |
| FI-11 | Transaction commit xong | **Crash sau con trỏ DB** | `succeeded` (g1) | Head g1 | Tự động | Không chạy lại, generation giữ nguyên | 2 |
| FI-12 | Worker đang chạy | Khởi động Worker thứ hai | Không đổi | Không đổi | Tự động | Worker 2 thoát, không chạm DB | 2 |
| FI-13 | Con treo, heartbeat chạy | Không có tiến độ | `queued`, `failure_count = 1` | Không có | Tự động | Watchdog dừng process group | 2 |
| FI-14 | Tác vụ luôn lỗi | Lỗi tạm thời lặp lại | `dead`, run `BLOCKED` | Không có | Thủ công | Đúng `max_failures` lần | 3 |
| FI-15 | Tác vụ luôn làm chết Worker | Crash lặp lại | `dead`, run `BLOCKED` | Không có | Thủ công | T9, không lặp vô hạn | 3 |
| FI-16 | Job `running` | Hủy khi đang chạy | `cancelled` | Không có head | Tự động | Commit worker 0 dòng | 3 |
| FI-17 | Đang ghi hoặc promote | Đĩa đầy | `running`, hàng đợi dừng | Không hiển thị dữ liệu dở | Thủ công | Thông báo; không xóa | 2 |
| FI-18 | Commit bị BUSY ngắn | Khóa giữ dưới ngân sách | `succeeded` | Head g1 | Tự động | T1, `failure_count = 0`, fencing chạy ở mỗi lần | 2 |
| FI-19 | Worker chạy | Đồng hồ nhảy tiến 1 giờ | `succeeded` | Head g1 | Tự động | Hiển thị `stalled`, không thu hồi | 2 |
| FI-20 | Artifact đầu vào sai checksum | Sửa tệp | `dead` hoặc run `BLOCKED` | Không có artifact mới | Thủ công | Không dùng dữ liệu hỏng | 3 |
| FI-21 | Run nhiều cảnh | 5 lần `SIGKILL` ngẫu nhiên | Mọi job `succeeded` | Đủ head | Tự động | Oracle sau mỗi lần kill | 3 |
| FI-22 | Commit và thu hồi cùng lúc | **Commit thắng cuộc đua** | `succeeded` (g1) | Head g1 | Tự động | Thu hồi thấy không còn `running`, bỏ qua | 2 |
| FI-23 | Commit và thu hồi cùng lúc | **Thu hồi thắng cuộc đua** | `queued` rồi `succeeded` (g2) | Head g2, g1 mồ côi | Tự động | Commit g1 0 dòng; `BEGIN IMMEDIATE` tuần tự hóa | 2 |
| FI-24 | Staging đủ, chưa flush | **Crash trước flush** | `queued` rồi `succeeded` | Head g2, g1 mồ côi | Tự động | Không có `pending`, không có DB trỏ g1 | 2 |
| FI-25 | Đã flush, chưa rename | **Crash sau flush, trước rename** | `queued` rồi `succeeded` | Head g2, staging g1 mồ côi | Tự động | Như FI-24 | 2 |
| FI-26 | Commit bị BUSY | **BUSY kéo dài**, hết ngân sách, hết trong giới hạn | `succeeded` | Head g1 | Tự động | T2, T3; không requeue, không chạy lại | 2 |
| FI-27 | Commit bị BUSY | **BUSY quá giới hạn tạm dừng** | `running`, Worker thoát | `committed/g1`, chưa có head | Tự động sau khi Worker khởi động | T5; không đặt `succeeded` | 2 |
| FI-28 | Sau FI-27 | Khởi động, DB hết khóa | `succeeded` (g1) | Head g1 | Tự động | T6; đúng một lần, không chạy lại | 2 |
| FI-29 | Sau FI-27, `pending` hoặc checksum hỏng | Khởi động | `queued` rồi `succeeded` (g2) | Head g2 | Tự động | T7; `pending` chuyển `processed/` | 2 |
| FI-30 | Tác vụ lỗi, ghi lỗi bị BUSY | Hết ngân sách, rồi DB hoạt động | `queued` có backoff | Không có | Tự động | T8; `failure_count` tăng đúng 1 | 2 |
| FI-31 | Tác vụ chạy | BUSY ở heartbeat dài hơn TTL | `succeeded` | Head g1 | Tự động | Tiến trình con không bị dừng oan | 2 |
| FI-32 | Worker **đang sống**, job `queued` chờ backoff 30 giây. **Cấm khởi động lại trong bài này.** Đồng hồ được tiêm qua hook, không đổi đồng hồ máy | **Đồng hồ lùi 1 giờ** | `succeeded` | Head g1 | Tự động | Một sự kiện `clock_regression`; job chạy sau phần chờ còn lại, không chờ thêm 1 giờ; không thu hồi | 2 |
| FI-33 | Orphan bỏ qua dây sinh tồn, nhận diện được | **Worker phục hồi với orphan** | `queued` rồi `succeeded` | Head g2 | Tự động | O2; g2 chỉ bắt đầu sau khi có khóa | 2 |
| FI-34 | Orphan giữ khóa, không khớp nhận diện | Khởi động | `running`, run `BLOCKED` | Không đổi | Thủ công | O3, O4; không có tín hiệu nào được gửi | 2 |
| FI-35 | Orphan không dừng sau SIGKILL (khóa do harness giữ) | Khởi động | `running`, run `BLOCKED` | Không đổi | Thủ công | O5 | 2 |
| FI-36 | Sau FI-34 | Bấm "Kiểm tra lại" khi orphan còn | Không đổi | Không đổi | Thủ công | Không vượt được khóa; AC-Q16 | 2 |
| FI-37 | Sau FI-34 | Orphan thoát | `queued` rồi `succeeded` | Head g2 | Tự động | Tiếp tục không cần sửa dữ liệu | 2 |
| FI-38 | PID ghi lại đã thuộc tiến trình khác | Khởi động | Theo trạng thái khóa | Không đổi | Tự động | Tiến trình vô can không nhận tín hiệu | 2 |
| FI-39 | Orphan còn sống | Thử nhận job nặng thứ hai | `queued`, không chạy | Không đổi | Tự động | Không chồng tải; đo bằng log khóa | 2 |
| FI-40 | Orphan ghi liên tục | Vượt `RLIMIT_FSIZE` | Theo O2 hoặc O4 | Tệp không vượt giới hạn | Tự động hoặc thủ công | AC-Q17; thông báo đĩa | 2 |
| FI-41 | Con vừa sinh, chưa ghi `pgid` | `SIGKILL` Worker | `queued` rồi `succeeded` | Head g2 | Tự động | `heavy.lock` phát hiện dù không có bản ghi | 2 |
| FI-42 | Orphan còn sống | Kiểm tra Worker mới | Theo O2 | Không đổi | Tự động | Orphan không giữ `worker.lock` | 2 |
| FI-43 | Worker crash khi Ollama giữ model | Khởi động | `queued` | Không đổi | Tự động | Đã gửi yêu cầu giải phóng model | 3 |
| FI-44 | Tác vụ lỗi `transient` **trước khi có manifest**, ghi lỗi hết ngân sách BUSY, `pending` loại `failure`, Worker thoát | Khởi động, DB hết khóa | `queued` có backoff | Không có | Tự động | T11a: `failure_count = 1`, `recovery_count` không đổi, không có `succeeded` | 2 |
| FI-45 | Như FI-44, lớp `invalid_input` | Khởi động | `dead`, run `BLOCKED` | Không có | Thủ công | T11c: không retry, bộ đếm không đổi | 2 |
| FI-46 | Như FI-44, hết `max_failures` | Khởi động | `dead`, run `BLOCKED` | Không có | Thủ công | T11b | 2 |
| FI-47 | `pending` loại `failure` bị hỏng | Khởi động | `queued` rồi chạy lại | Không có | Tự động | T7: `recovery_count + 1`, `failure_count` không đổi | 2 |
| FI-48 | `pending` đã áp dụng, chưa đổi sang `processed/` | Crash, khởi động lại, thử cả hai loại | Giữ kết quả lần trước | Không đổi | Tự động | Thao tác rỗng; bộ đếm và sự kiện không tăng hai lần | 2 |
| FI-49 | `pending` loại `success` thiếu manifest | Khởi động | `queued` rồi `succeeded` (g2) | Head g2 | Tự động | T7; không diễn giải thành `failure`, `failure_count` không đổi | 2 |
| FI-50 | Worker sống, job `queued` | Đồng hồ lùi trong lúc không phát hiện được (đổi khi máy ngủ) | `succeeded` | Head g1 | Tự động | Bước kẹp giữ chờ không quá backoff tối đa | 2 |
| FI-51 | Worker sống, phát hiện đồng hồ lùi | BUSY khi dịch `next_run_at`, rồi hết | `succeeded` | Head g1 | Tự động | Lịch chỉ bị dịch đúng một lần, một sự kiện `clock_regression` | 2 |
| MT-01 | Render thật | **Thủ công:** ngủ máy, thức sau hơn TTL | `succeeded` | Head đúng | Tự động | Có `sleep_detected` | 3 |
| MT-02 | Render thật | **Thủ công:** gập nắp | `succeeded` | Head đúng | Tự động | Như MT-01 | 3 |
| MT-03 | Render thật | **Thủ công:** ngắt nguồn, chỉ khi Chủ dự án đồng ý | Như worker crash | DB toàn vẹn | Tự động | `PRAGMA integrity_check` đạt | 14 |
