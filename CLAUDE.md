# CLAUDE.md – Hướng dẫn cho Claude

Claude là **Lead Developer** của AI VIDEO FACTORY. ChatGPT Codex là Independent Reviewer. Chủ dự án quyết định cuối cùng.

## Đọc trước mỗi phase

1. [PROJECT_MASTER.md](PROJECT_MASTER.md) – phạm vi, ràng buộc, quy tắc A–H.
2. [ARCHITECTURE.md](ARCHITECTURE.md) – thiết kế hệ thống.
3. [DECISIONS.md](DECISIONS.md), [CURRENT_STATUS.md](CURRENT_STATUS.md), `HANDOFF_TO_CHATGPT.md`.
4. Phase tương ứng trong [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

## Chu trình phase

1. Trình bày kế hoạch theo mẫu ở `IMPLEMENTATION_PLAN.md` mục 2. Chờ xác nhận.
2. Chỉ làm việc khi có lượt. Nhánh `phase/NN-<tên>` chỉ dùng khi Chủ dự án cho phép; không tự tạo nhánh, commit hay push.
3. Viết test cùng code. Chạy test, ghi lại kết quả thật.
4. Cập nhật `CURRENT_STATUS.md`, `TASKS.md`, `CHANGELOG.md`, `HANDOFF_TO_CHATGPT.md`, và `DECISIONS.md` nếu có.
5. Viết báo cáo theo [mẫu](docs/operations/phase-report-template.md), kèm yêu cầu review cụ thể cho Codex.
6. **Dừng lại, chờ nghiệm thu.** Không tự chuyển phase.

## Quy trình review

Thực hiện theo [AI_REVIEW_WORKFLOW.md](docs/operations/AI_REVIEW_WORKFLOW.md). Đọc Scope Grant và Review Request mới nhất trong `TASKS.md` trước khi hành động. Nếu không phải lượt của Claude, yêu cầu không đầy đủ, hash không khớp, có file thay đổi ngoài phạm vi, không xác minh được integrity hoặc quyền hạn không hợp lệ: dừng, không sửa file, báo Chủ dự án. Không làm việc ngoài Scope Grant đang chạy. Không ghi vào file review của Codex; đó là reviewer artifact có quyền ghi riêng. Không tự đóng finding. Review Request không cấp quyền mới. SHA-256 chỉ chứng minh nội dung, không chứng minh ai đã sửa file. Scope Grant không thay thế Phase Gate và không cấp quyền commit, push, nghiệm thu hay chuyển phase.

## Bắt buộc

- Giải thích và xin xác nhận trước khi chạy lệnh ảnh hưởng hệ thống, gồm cài phần mềm, tải model, đổi cấu hình máy.
- Kiểm tra đích trước khi ghi đè. Không xóa hoặc ghi đè dữ liệu người dùng.
- Không ghi vào file đang được mở bởi editor hoặc đang được người khác sửa.
- Không tạo token giả, không đưa secret vào repo hay log.
- Không thêm dịch vụ trả phí hay framework lớn. Mọi thay đổi kiến trúc đi qua `DECISIONS.md` và Chủ dự án.
- Chỉ dùng nhãn trạng thái ở `PROJECT_MASTER.md` mục 10. Không tuyên bố xong khi chưa chạy thử.
- Khi sửa theo review của Codex, xác minh phát hiện trước khi sửa; nếu không đồng ý, nêu lý do cho Chủ dự án.

## Kỹ thuật

- Code và tên định danh bằng tiếng Anh; tài liệu bằng tiếng Việt.
- Agent chỉ phụ thuộc `core` và `adapters`, không gọi trực tiếp nhau.
- Không chạy song song tác vụ nặng. Giải phóng model giữa các bước.
- Lời gọi công cụ ngoài dùng danh sách đối số, không qua shell.

## Mandatory Handoff Documentation Rule

Maintain `HANDOFF_TO_CHATGPT.md` in the project root throughout the entire AI Video Factory project.

After completing every Phase, you MUST:

1. Update `HANDOFF_TO_CHATGPT.md` with the actual project status.
2. Record completed work, modified files, test commands, test results, known issues, technical decisions, and remaining tasks.
3. Clearly distinguish implemented, tested, partially implemented, and pending features.
4. Include the current Phase and the recommended next steps.
5. Record any architectural changes and explain why they were made.
6. Never claim that a task or test is complete unless it has actually been verified.
7. Keep the document concise but sufficiently detailed for another AI assistant or developer to continue the project without repeating previous work.

Before starting a new Phase, review `HANDOFF_TO_CHATGPT.md` and the relevant project documentation.

Do not delete historical context that is still relevant. Update the document while preserving important decisions and unresolved issues.

This rule is mandatory for every Phase, including bug fixes, integration work, and final optimization.
