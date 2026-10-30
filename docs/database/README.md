# Lược đồ dữ liệu khái niệm

**[Đề xuất]** Bản khái niệm, chưa phải DDL. Chốt ở Phase 2 bằng migration có phiên bản.

| Bảng | Mục đích | Trường chính |
|---|---|---|
| `projects` | Chương trình, kênh, cấu hình mặc định | `id`, `name`, `language`, `style` |
| `runs` | Một lần sản xuất video | `id`, `project_id`, `state`, `brief`, thời gian |
| `scenes` | Cảnh trong run | `id`, `run_id`, `index`, `state`, `duration_ms` |
| `jobs` | Hàng đợi | `id`, `run_id`, `scene_id`, `kind`, `state`, `lease_generation`, `lease_owner`, `lease_expires_at`, `failure_count`, `max_failures`, `recovery_count`, `max_recoveries`, `next_run_at`, `idempotency_key` |
| `job_attempts` | Một dòng cho mỗi lần chạy | `job_id`, `generation` (khóa duy nhất), `outcome`, `pgid`, `process_started_at`, `executable`, `attempt_token`, `started_at`, `finished_at`, `error`, `metrics` |
| `artifacts` | Artifact đã commit, bất biến | `id`, `run_id`, `job_id`, `generation`, `kind`, `path`, `sha256`, `schema_version` |
| `artifact_heads` | Con trỏ artifact hiện hành | `run_id`, `slot` (ví dụ cảnh), `artifact_id` |
| `gate_results` | Kết quả Quality Gate | `run_id`, `gate`, `passed`, `details` |
| `packages` | Gói xuất bản bất biến | `id`, `run_id`, `version`, `package_sha256`, `manifest_path` |
| `approvals` | Phê duyệt của người | `run_id`, `type`, `package_sha256`, `decision`, `decided_at`, `revoked_at` |
| `rights_reviews` | Kết quả Rights Gate | `package_sha256`, `passed`, `reviewed_by`, `reviewed_at`, `details` |
| `assets` | Asset và hồ sơ quyền | Thêm `asset_version`. Xem [security-and-rights.md](../architecture/security-and-rights.md) mục 6 |
| `publish_intents` | Lựa chọn và đồng ý theo nền tảng | `package_sha256`, `platform`, `destination`, `options`, `requirements_snapshot`, `consented_by`, `consented_at` |
| `voice_consents` | Đồng ý nhân bản giọng | `voice_id`, `subject`, `scope`, `expires_at`, `revoked_at`, `evidence_sha256` |
| `publications` | Một dòng cho mỗi nền tảng và đích | `run_id`, `platform`, `destination`, `package_sha256`, `video_sha256`, `approval_id`, `rights_review_id`, `publish_intent_id`, `state`, `review_required`, `platform_status`, `external_id`, `idempotency_key` |
| `publication_events` | Bằng chứng, chỉ ghi thêm | `publication_id`, `at`, `from_state`, `to_state`, `request_id`, `http_status`, `redacted_excerpt`, `actor` |
| `metrics` | Số liệu nền tảng | `publication_id`, `name`, `value`, `collected_at` |
| `audit_log` | Sự kiện quan trọng, chỉ ghi thêm; `event_id` duy nhất chống ghi trùng từ nhật ký | `seq`, `event_id`, `at`, `actor`, `action`, `details` |

**Quy ước:** khóa chính dạng UUID; thời gian UTC ISO 8601; bật `foreign_keys`; dùng WAL với `synchronous=FULL` và `fullfsync=ON` (đo chi phí ở Phase 2); không lưu nhị phân trong DB; không lưu secret; xóa mềm cho dữ liệu quan trọng.

**Ràng buộc bắt buộc:**

- `job_attempts`: duy nhất `(job_id, generation)`.
- `publications`: unique index một phần trên `(video_sha256, platform, destination)` với các trạng thái `queued`, `uploading`, `unknown`, `confirmed`.
- Mọi ghi của worker vào `jobs`, `runs`, `scenes`, `artifacts`, `artifact_heads` đều qua kiểm tra fencing theo [queue-safety.md](../architecture/queue-safety.md) mục 5. Thu hồi và hủy do API/supervisor thực hiện trong transaction riêng.
- Không có đường tự động nào đưa `publications.state` từ `unknown` sang `queued`, xem [publishing-reliability.md](../architecture/publishing-reliability.md).
- Dòng `publications` chỉ được tạo khi có `approval_id`, `rights_review_id`, `publish_intent_id` hiện hành cùng `package_sha256`. Trigger SQLite là lớp bảo vệ thứ hai, bên cạnh kiểm tra ở lớp dịch vụ.
- Ghi vào DB khi tranh chấp theo [queue-safety.md](../architecture/queue-safety.md) mục 10. Tệp `pending` và nhật ký chỉ là ý định; **DB vẫn là nguồn sự thật**.
