# NMT-engine — Ngang Một Tí

Phiên bản: **1.0.0** (12/11/2026, xem `VERSION` và `CHANGELOG.md`).

`nmt-engine` là bộ công cụ dựng video hoạt hình 2D cho thương hiệu **Ngang Một Tí**, với **Tí, Ngang và Mimi — thú cưng của Ngang**. Engine hỗ trợ triển khai brief thành kịch bản, storyboard, diễn xuất bằng sprite/key pose, giọng thoại hoặc nhạc do Owner cung cấp, phụ đề tiếng Việt, outro và video có watermark NMT cho TikTok, YouTube Shorts, Facebook Reels.

Phần dựng dùng Pillow/numpy và FFmpeg, có điều phối theo từng tập và cổng duyệt của Project Owner. Khổ mặc định 9:16, 1080×1920, 60 fps. Video thoại thường khoảng 25–35 giây; video theo nhạc lấy thời lượng từ đoạn nhạc Owner chọn. Mức hỗ trợ rig, lip-sync và tự động hóa phải đi kèm tài sản cùng kiểm chứng thực tế; các tập đã xuất bằng key pose không mặc định chứng minh đã có rig/lip-sync.

**Cách gọi chính:**

```text
/nmt-engine <chủ đề hoặc brief>
```

```bash
python3 output/_engine/nmt_engine.py list
python3 output/_engine/nmt_engine.py new "Tí và Ngang nấu ăn cùng Mimi"
```

Lệnh `/nmt-engine` được khai báo tại `.claude/commands/nmt-engine.md` cho Claude Code. Prompt dùng với ứng dụng/AI khác: [NMT_ENGINE_PROMPT.md](NMT_ENGINE_PROMPT.md). Việc đổi tên trong repo không tự cài hoặc đổi tên một skill độc lập trong Claude Desktop.

Tên cũ `couple-engine`, CLI `couple_engine.py` và hai đường dẫn tài liệu `COUPLE_ENGINE*.md` được giữ dưới dạng alias/chuyển hướng. Thư mục tập, ID nhân vật và video đã xuất giữ nguyên. Renderer nội bộ vẫn là `cute_engine.py`; đây là tên module kỹ thuật, không phải tên lệnh thương hiệu.

Thư mục engine: `output/_engine/`. Cập nhật lần cuối 08/11/2026.

**Cải tiến liên tục (Owner 08/11/2026):** mỗi lỗi Owner phát hiện phải được sửa, tìm nguyên nhân gốc, chặn tái diễn bằng kiểm tra tự động trong engine (hoặc checklist mục 4) và ghi vào [`IMPROVEMENT_LOG.md`](IMPROVEMENT_LOG.md). Đọc sổ này trước khi làm tập mới.

## 0. Nguyên tắc công cụ: chỉ dùng loại miễn phí 100% (Owner, 07/11/2026)

- Chỉ dùng công cụ, plugin, thư viện, model và mã nguồn GitHub **miễn phí 100%**, ưu tiên loại chạy cục bộ.
- **Thành phần trong các workflow hiện có (mức kiểm chứng xem báo cáo từng tập/model):**
  - Pillow, numpy, ffmpeg (dựng hình và âm thanh).
  - VieNeu TTS cục bộ (giọng).
  - ComfyUI (GPL-3.0), SDXL Base 1.0 (Open RAIL++-M), ControlNet Union SDXL (Apache-2.0) và rembg (MIT), có workflow tạo ảnh cục bộ/bán hiện thực riêng. Việc liệt kê không xác nhận mọi model đã tải hoặc đạt chất lượng cho mọi tập.
  - Font Be Vietnam Pro và Itim (OFL); chọn theo nội dung và mẫu Owner duyệt.
- **Không dùng:**
  - Dịch vụ tính credit hoặc trả phí, ví dụ Canva AI (generate-image).
  - API trả tiền.
  - Plugin hay connector có gói trả phí cho các bước sản xuất.
- Mỗi thành phần mới phải ghi rõ giấy phép và được Owner đồng ý trước khi cài hoặc tải.

## 1. Nhân vật và hình mẫu (chỉ dùng tài sản đã duyệt)

| Nhân vật | Vai | Giọng VieNeu |
|---|---|---|
| **Tí** | Bạn trai, hiền, hay "lỡ lời" | Hải Đăng |
| **Ngang** | Bạn gái, tóc dài, hay dỗi nhưng đáng yêu | Trúc Ly |
| **Mimi** | Mèo mướp, **không bao giờ nói**, chỉ phán xét bằng ánh mắt | — |

Mọi hình ảnh đều lấy từ `character_library/asset_index.json`, chỉ dùng mục có `approval_status = approved`. Engine tự chặn sprite chưa duyệt.

| Loại | Ví dụ ID | Ghi chú |
|---|---|---|
| Diễn xuất | `TI_ACTING_001…020`, `NGANG_ACTING_*`, `MIMI_ACTING_*` | Toàn thân, nhiều hành động |
| Biểu cảm cận mặt | `*_EXP_LOCAL_<DELIGHTED/ANGRY/SAD/SMUG/SLEEPY/...>` | Ảnh bán thân, cùng khung hình |
| Tư thế | `TI_POSE_002` (ngồi), `*_POSE_LOCAL_*` | |
| Trang phục | `*_WARDROBE_001…010` | ở nhà, công sở, mưa, thể thao, du lịch, vest, áo dài Tết, nấu ăn, cổ tích, dạ tiệc. Ảnh 2/3 thân, một nét mặt |

Ảnh ghép được phép làm, nhưng Owner phải xem chúng ở bước duyệt hình. Mẫu trong tập 8:
- `ep08_wardrobe.make()`: ghép đầu biểu cảm lên thân trang phục.
- `make_messy()`: tóc rối, "chưa gội đầu".
- `ep08_phone.build()`: lấy `TI_ACTING_013`, đổi cốc thành điện thoại và đổi áo thành áo đấu.

Hình vẽ tay hoàn toàn đã bị Owner chê là "giả". Phải **tìm trong thư viện trước**, chỉ ghép khi không có hình phù hợp.

## 2. Quy trình chuẩn: duyệt kịch bản, hình và video cuối

| Bước | Lệnh (chạy trong `output/epNN_<slug>/render/`) | Kết quả | Cổng |
|---|---|---|---|
| 0. Tạo tập | `python3 ../../_engine/nmt_engine.py new "<chủ đề>"` | `epNN.py`, `post.json` | — |
| 1. Kịch bản | Điền `META` và `PLAN`, rồi chạy `python3 epNN.py --script` | `script.md`, `lines.json` | **Owner duyệt kịch bản** |
| 2. Giọng và hình mẫu | `--tts`, viết `epNN_scenes.py`, rồi chạy `--storyboard` | Giọng, `contact_sheet.png`, `thumbnail.png` | **Owner duyệt hình** |
| 3. Video | `python3 epNN.py F01 F02 …` (chia nhỏ để mỗi lượt dưới 180 s), `--audio`, `--mux` | `final_video.mp4` | **Owner duyệt video cuối** |
| 4. Xuất đa nền tảng | `--export tiktok F01 …`, `--export youtube_shorts …`, `--export facebook_reels …`, rồi `--export-finish` | `videos-post/<slug>/<nền tảng>/` | Bản để đăng **thủ công** |

Ghi quyết định duyệt bằng `--approve <script|visual|final> --by "owner (chat)" --note "…"`. Từ chối thì dùng `--reject`.

**Cổng khoá bằng SHA-256.**
- Sửa kịch bản hoặc file cảnh sau khi đã duyệt thì bước sau bị chặn, phải duyệt lại.
- Xuất đa nền tảng bị chặn cho tới khi Owner duyệt video cuối. Đã thử và bị chặn đúng.

**Hỏi duyệt ngay trong chat.**
- **Kịch bản (Owner, 10/11/2026):** Toàn bộ kịch bản phải hiển thị trực tiếp trong chat, gồm từng cảnh, hành động/biểu cảm, lời thoại hoặc không thoại, âm thanh và outro. Gửi nội dung đầy đủ trước câu hỏi có hai lựa chọn Duyệt / Cần chỉnh; không chỉ gửi đường dẫn file hay thông báo đã sẵn sàng. Lời nhắc và câu trả lời duyệt phải chỉ rõ tập/phiên bản. Yêu cầu cập nhật quy trình hoặc góp ý không được tính là duyệt; chỉ ghi nhận duyệt khi Owner xác nhận rõ ràng.
- Đưa nội dung kịch bản, bảng hình, video lên chat kèm mô tả, rồi hỏi bằng câu hỏi lựa chọn.
- **Owner 09/11/2026:** mỗi lần hỏi duyệt phải hiển thị hai nút **Duyệt** và **Cần chỉnh** bằng công cụ hỏi có lựa chọn của ứng dụng (Codex: `request_user_input_async`, options `["Duyệt", "Cần chỉnh"]`). Gửi nội dung cần duyệt trước khi hiển thị nút. Nếu ứng dụng không hỗ trợ nút thì nêu rõ và đưa hai lựa chọn bằng chữ; không mô tả nút như thể đã hiển thị.
- Không bắt Owner phải mở file để đọc.
- Nếu Owner chọn "Cần sửa" mà không ghi nội dung, phải hỏi lại. Không tự đoán.

## 3. Xuất đa nền tảng: `videos-post/`

```
videos-post/
└── <slug chủ đề>/             vd. ngay-dau-yeu-vs-nam-thu-3
    ├── README.md
    ├── tiktok/            <slug>_tiktok_nmt.mp4, cover.jpg, caption.txt, manifest.json
    ├── youtube_shorts/    <slug>_youtube_shorts_nmt.mp4, cover.jpg, caption.txt, manifest.json
    └── facebook_reels/    <slug>_facebook_reels_nmt.mp4, cover.jpg, caption.txt, manifest.json
```

Cả ba bản đều có khổ 1080×1920 (9:16), H.264 60 fps, âm thanh AAC 48 kHz chuẩn hoá 2 lượt về mục tiêu −14 LUFS. Mục tiêu đỉnh −1,5 dBTP; số đo thực ghi trong `manifest.json`. Các bản dùng cảnh và âm thanh đã duyệt. Bố cục hiện tại đặt nội dung 3/4 trên, phụ đề 1/4 dưới; EP10 v04 dùng chung bố cục master cho cả ba bản. Bảng dưới là thông số/vùng giao diện tham khảo của bộ xuất, không xác nhận mọi tập đã được dựng lại riêng theo từng giao diện app:

| Nền tảng | Tâm phụ đề dưới (y) | Rộng tối đa | Vùng giao diện cần tránh (ước lượng) | Giới hạn độ dài đặt trong engine |
|---|---|---|---|---|
| TikTok | 1390 | 820 px (lệch trái, x=500) | Đáy khoảng 440 px, cột nút phải khoảng 120 px, đỉnh khoảng 150 px | 600 s |
| YouTube Shorts | 1440 | 840 px | Đáy khoảng 380 px, phải khoảng 110 px | 180 s |
| Facebook Reels | 1300 | 840 px | Đáy khoảng 35 %, phải khoảng 120 px | 90 s |

- Caption và hashtag lấy từ `output/epNN_<slug>/post.json`.
- `manifest.json` ghi SHA-256, lịch sử duyệt và `published: false`.
- **Engine không đăng lên nền tảng nào.**

Các số vùng an toàn là ước lượng theo hướng dẫn công khai của từng nền tảng. Giao diện app thay đổi theo phiên bản, nên trước khi đăng cần xem thử trên điện thoại.

### Cập nhật bố cục Owner 10/11/2026 — ưu tiên hơn khung tranh cũ

- Hình/bối cảnh phủ tối thiểu 95% màn hình; không thu tranh vào khung bo góc rồi để thừa nền trắng/kem xung quanh. Không dùng nền mờ hoặc kéo giãn hình.
- Nhân vật, biểu cảm và hành động quan trọng vẫn nằm trong vùng tập trung/an toàn đã định (x108–950, y200–1460 ở 1080×1920). Bối cảnh được phép phủ các vùng ngoại vi.
- Phụ đề giữ canh giữa, vùng1480–1680 và không đè nhân vật hoặc watermark. Bối cảnh tự nhiên tiếp tục phía sau phụ đề, không cần dải nền trắng chiếm cả đáy.
- EP13 áp dụng renderer riêng và tranh9:16 mới. Engine chung vẫn có hành vi đóng khung cũ cho các tập lịch sử; chưa tuyên bố đã thay đổi renderer chung hoặc các file đã xuất.

### 3.2 Khung an toàn thống nhất NMT-SAFE-916 v1 (bắt buộc, Owner 08/11/2026)

**Lỗi Owner thấy trên điện thoại:** TikTok và YouTube Shorts phóng to video, mất 4 góc; phần trên tràn lên vùng tab/thanh trạng thái. Facebook Reels hiển thị bình thường.

**Nguyên nhân:** file xuất đúng chuẩn (1080×1920, SAR 1:1, H.264 High, 60 fps). Lỗi do bố cục. TikTok/Shorts dùng chế độ *lấp đầy* trên màn hình dài hơn 9:16 (19,5:9; 20:9): video phóng theo chiều cao, cắt hai bên tới khoảng 108 px mỗi bên, rồi tab/trạng thái đè đỉnh và caption/nút đè đáy. Bố cục cũ đặt nội dung sát mép, từ y=0 tới 1440, có khung bo góc, nhãn chữ ("NĂM ĐẦU") và viên phụ đề rộng chạm mép, nên bị cắt hoặc bị đè. Facebook hiển thị vừa khung nên không lộ lỗi.

**Quy tắc:** một khung dùng chung cho cả 3 nền tảng, là giao của các vùng an toàn. Số đo trên khung 1080×1920, hằng số ở `output/_engine/safe_frame.py`.

| Vùng | Toạ độ | Được đặt gì |
|---|---|---|
| Lề cắt hai bên | x < 108 và x > 972 | Chỉ màu nền trơn. Không mặt, chữ, logo hay tranh |
| Cột nút phải | x > 950 (y 600–1500) | Không chữ, không mặt |
| Đỉnh (giao diện app) | y < 200 | Chỉ nền kéo dài. Đỉnh đầu nhân vật ≥ 240 |
| Nội dung chính | x 108–950, y 200–1460 | Nhân vật, đạo cụ, khung chia đôi, nhãn chữ |
| Dải phụ đề | mép trên 1480, tâm 1 dòng ≈ 1540, đáy ≤ 1680 (ưu tiên 1 dòng); rộng ≤ 800, **viền luôn canh giữa màn hình (tâm x = 540)** | Phụ đề. Dời xuống so với bản cũ (≈1460–1575) |
| Đáy (giao diện app) | y > 1680 | Nền và watermark. Không thoại |

- **Nội dung là một khung tranh bo góc nằm gọn trong x 108–972, y 200–1460**; xung quanh là màu nền trơn của tập (kem/hồng). **Không làm mờ hay kéo giãn tranh ra xung quanh** (Owner 08/11/2026, sau khi xem v05 nền mờ). Khi thu tranh, cắt bớt hai mép nền cho vừa bề rộng, không bóp méo.
- **Viền phụ đề luôn canh giữa màn hình** (Owner 08/11/2026, phát hiện ở EP10 v06 tâm x = 510): tâm hộp viền = 540 ± 2 px với mọi câu, mọi nền tảng, kể cả khi có icon hay chữ hiện dần. Không dời ngang để né watermark; nếu chạm thì thu hẹp đối xứng. `safe_frame.check_box(..., "subtitle")` báo lỗi khi lệch tâm; `check_subs()` và `--mux`/`--export-finish` chặn. Renderer riêng theo revision phải dùng `SF.SUB_X_CENTER` cho tâm viên phụ đề (icon/chữ canh bên trong viên).
- **Icon diễn đạt nằm trong viên phụ đề** (bên trái chữ), không đặt rời dưới phụ đề. **Hiệu ứng "đang phát nhạc"** đặt trên tranh (góc trên-trái khung tranh), không đặt ở dải dưới.
- Watermark NMT nằm trong vùng không bị cắt: `margin_x ≥ 120` (mặc định cũ 48 làm logo lấn vào lề cắt). Đổi mặc định trong `src/.../branding.py` cần Scope Grant; trước khi có quyền, đặt `watermark.json` của tập.
- Ba bản TikTok/Shorts/Reels dùng **cùng một bố cục và cùng file hình**; chỉ khác caption, độ dài và loudness. Không dựng bố cục riêng từng nền tảng.
- Thông số file giữ nguyên: 1080×1920, 9:16, SAR 1:1, H.264 High yuv420p, 60 fps, AAC 48 kHz. Không xuất 4K/khác tỉ lệ.
- **Kiểm tra trước khi hỏi duyệt video cuối:** `python3 output/_engine/safe_frame.py preview <mp4> 2 10 20 -o <ảnh>` vẽ vùng cắt (đỏ), giao diện (cam), nội dung (xanh lá), phụ đề (xanh dương). Mặt, chữ, góc khung phải nằm trong ô xanh lá; phụ đề trong ô xanh dương. Gửi ảnh này cùng video khi hỏi duyệt.
- **Tự động hoá trong engine (08/11/2026):** `cute_engine.SAFE916 = True` (mặc định). Cảnh vẫn vẽ theo bố cục cũ; `frame()` gọi `safe_post()` để thu nội dung `0…tray_top()` vào y 200–1460 (`safe_frame.reframe`: khung tranh bo góc, nền trơn), rồi vẽ dải và phụ đề ở 1480–1680, viền canh giữa màn hình (x 540), rộng ≤ 800, giống nhau ở bản gốc và 3 nền tảng. `check_subs()` báo `safe_frame_violations`; `--mux`/`--export-finish` chặn khi phụ đề ra ngoài khung. `wm_box()` và `platform_export` đặt watermark `margin_x ≥ 120`. Tắt (`SAFE916 = False`) chỉ để tái lập bản cũ.
- Renderer riêng theo revision (vd. EP10 dùng `engine_snapshot`) không tự nhận thay đổi; phải gọi `safe_frame.reframe` trong renderer revision mới (mẫu: `output/ep10_vi_anh_qua_dep_trai/revisions/v05/render/ep10_v05.py`).

### 3.0 Lưu hình đã duyệt vào thư viện (bắt buộc, Owner 07/11/2026)

- Sau khi Owner duyệt video cuối, chạy `python3 output/<tập>/render/<tập>.py --library-sync`. Lệnh này lưu mọi sprite ghép hoặc đã sửa của tập vào `character_library/episode_approved/<tập>/` và ghi vào `asset_index.json`.
- Khi Owner báo lỗi một hình và hình đó đã được sửa: lưu bản mới với trạng thái `pending_owner_review`. Bản cũ tự chuyển sang `superseded` và file cũ được dời vào `_superseded/`, không xoá. Sau khi Owner duyệt, đổi bản mới sang `approved`.
- **Mọi video cuối đều thêm hình vào thư viện (bắt buộc, Owner 12/11/2026).** `--export-finish` tự gọi `--library-sync` ngay sau khi xuất: lưu sprite ghép/sửa **và** mọi tranh cảnh full-bleed mà renderer dùng qua `art('<tên>')` (`asset_category: episode_scene_art`), kèm `contact_sheet.jpg` và mục `scene_art` trong `usage.json`. Khai báo `LIBRARY_ART = {'<tên tranh>': {'asset_id', 'character_id', 'character_name', 'outfit', 'scenes', 'context', 'style', 'generator'}}` trong `<tập>_scenes.py` để mục thư viện có mô tả đầy đủ; thiếu thì engine tự đặt mã `<EPnn>_SCENE_<tên>`. Tập có renderer riêng không đi qua `--export-finish` thì phải chạy `--library-sync` bằng tay sau khi Owner duyệt video cuối. Báo Owner số hình đã thêm khi kết thúc tập.
- Trước khi vẽ cảnh mới, xem `character_library/episode_approved/README.md` (bảng lỗi đã ghi nhận) để không lặp lại lỗi cũ.
- Tóc rối của Ngang: dùng `hair_fx.bedhead` (tóc mới ngủ dậy, mẫu `NGANG_DAILY_001`). Không dùng `messy_hair` (chỏm nhọn), vì Owner đã chê.

### 3.1 Watermark NMT (bắt buộc, Owner 07/11/2026)

- `--export-finish` dựng **bản sạch** `output/<tập>/render/export/<nền tảng>/<slug>_<nền tảng>_clean.mp4` (có rồi thì dùng lại, không ghi đè), rồi chèn watermark NMT bằng `src/ai_video_factory/core/branding.py`. Chỉ bản `_nmt.mp4` đã qua kiểm tra mới được đưa vào `videos-post/`.
- Vị trí mặc định: góc dưới-phải, rộng 190 px, độ mờ 0,85, cách mép 48 px (cả 3 nền tảng). Chỉnh theo tập bằng `output/<tập>/watermark.json`.
- `post.json` phải có `"brand": "ngang-mot-ti"` (tập mới tự có). Thiếu khoá → chặn xuất.
- Lỗi (thiếu file logo, logo đè phụ đề, chèn lỗi, kiểm tra hỏng) → **chặn**, ghi `BLOCKED.txt` trong thư mục nền tảng và `watermark_report.json` cạnh bản sạch. Không bao giờ đưa bản sạch đi đăng.
- Không bật watermark trong YouTube Studio (sẽ thành 2 logo).
- **Phụ đề không chạm watermark (Owner 08/11/2026):** `--check-subs <nền tảng>` tính hộp watermark thật bằng `branding.geometry` (cùng hàm lúc chèn, kể cả `watermark.json`) và đối chiếu với hộp phụ đề thật ở mọi khung mẫu, khoảng hở tối thiểu `WM_PAD` = 24 px. `--export-finish` chặn nếu chạm. Bổ sung cho kiểm tra vùng phụ đề ước lượng `SUBTITLE_ZONES` của `branding.py`.
- Đặc tả và bằng chứng: `docs/requirements/WATERMARK_NMT.md`.

## 4. Kiểm tra chất lượng trước mỗi lần hỏi duyệt (rút từ góp ý Owner)

**Hình và bố cục**
- Phụ đề **không ghi tên nhân vật**. Câu thoại tối đa khoảng 45 ký tự.
- **Khung an toàn NMT-SAFE-916 v1 (mục 3.2) được ưu tiên hơn quy tắc 3/4–1/4 bên dưới:** nội dung y 200–1460, x 108–950; phụ đề 1480–1680; khung tranh bo góc, nền trơn, không làm mờ.
- **Bố cục khung (Owner 08/11/2026): nội dung 3/4 trên, phụ đề 1/4 dưới** (`E.CONTENT_FRAC` = 0,75; tập được chỉnh tùy nội dung nhưng dải phụ đề không vượt 1/3, engine chặn). `subtitle()` tự vẽ dải và đặt phụ đề trong dải, giống nhau ở mọi bản; né watermark NMT.
- **Phụ đề ở dưới, không đè nhân vật, không chạm watermark** (Owner 08/11/2026), ở bản gốc và 3 bản nền tảng. Cảnh toàn khung: `E.sub_tray(im)` rồi `subtitle(im, tg, y=E.sub_y_bottom())`, nhân vật đặt phía trên `E.tray_top()`. Cảnh chia đôi: `E.panel_layout()` tự thu khung theo vùng an toàn nền tảng; dùng `E.panel_center(i)` khi đẩy máy, không vượt `E.PANEL_ZOOM_MAX`. Kiểm tra tự động: `python3 epNN.py --check-subs [nền tảng]`; `--mux` và `--export-finish` tự chặn.
- Đầu và tóc nhân vật **không bị cắt** ở mép khung, kể cả trong khung chia đôi.
- Sprite trang phục 2/3 thân: đẩy đáy xuống dưới mép khung để giấu đường cắt.
- Sinh vật "vô tri" (sâu, muỗi…) phải dễ thương và đúng giải phẫu. Hành động phải thật: bay vào, lơ lửng, đáp xuống, xếp cánh…
- Vật trang trí không được che nhân vật đang diễn. Ví dụ bong bóng suy nghĩ phải nằm cao hơn đầu.
- Phụ kiện bám theo đúng đầu và nhịp thở của nhân vật. Ví dụ vương miện của Mimi.
- Cảnh cuối không có câu thừa. Owner đã bỏ dòng "ai cũng thua mèo".

**Chuyển động và góc máy**
- Góc máy đa dạng: toàn, cận, chèn, góc thấp/cao, nghiêng khung, lia nhanh, đẩy hoặc kéo máy, khung chia đôi.
- Chuyển động sống: thở, dồn trọng tâm, lấy đà, nảy rồi lắng, nháy mắt.

**Âm thanh**
- Âm thanh trung bình khoảng −19 dB, đỉnh không vượt −1 dB.

**Đối chiếu sau khi dựng**
- Lưới khung hình cả video và `volumedetect`, đối chiếu lại với các mục trên.

## 5. Lưu ý vận hành

- Máy ảo không gọi được Ollama trên Mac. TTS chạy bằng VieNeu cục bộ (`tts_vieneu.py`).
- Mỗi lệnh trên máy ảo tối đa 180 s. Mỗi lượt render 2–3 cảnh.
- Sửa file trực tiếp trên thiết bị. Bản sao trên cloud có thể lệch, nên kiểm tra bằng `grep` trước khi render.
- Thư mục dự án chặn lệnh xoá. File tạm có tiền tố `_qa`, `_wardrobe_review/` để Owner tự dọn.

## 6. Tập đã làm bằng engine này

| Tập | Chủ đề | Trạng thái |
|---|---|---|
| ep07 | Nếu em là con sâu | final_approved (chưa xuất videos-post) |
| ep08 | Ngày đầu yêu vs năm thứ 3 | **v2 (08/11):** dựng lại bằng bộ hình Codex ImageGen `visual_rebuild_v01`, sửa phụ đề không đè nhân vật/watermark; final_approved, đã xuất lại `videos-post/ngay-dau-yeu-vs-nam-thu-3/` (3 nền tảng, watermark NMT). Bản v1 lưu ở `output/ep08_ngay_dau_vs_nam_ba/_superseded_v1_2d/`. Lịch sử v1: Style C, có watermark NMT từ 07/11; bản sạch ở `render/export/`. Bản 2 (sprite pilot 2) đang làm ở `ep08b_…`. Đã thử bán hiện thực (pilot 1, 2 trong `output/_semireal_pilot*/`). Owner không duyệt tải model cho pilot 3. |


## Mặc định hình ảnh — Owner 08/11/2026

Mốc hình ảnh mặc định là video đã duyệt trong videos-post/ngay-dau-yeu-vs-nam-thu-3/. Dùng comic Nhật theo cách thể hiện trong video đó, giữ danh tính Style C của Tí, Ngang và Mimi. Hình tham chiếu kiểm tra từ bản TikTok tại giây 2, 9, 16 và 23.

- Nền kem, hồng, tím và xanh pastel, nội thất và ngoại cảnh giản lược.
- Đường bao rõ, màu phẳng và bóng cel nhẹ, biểu cảm đọc tốt ở cỡ điện thoại.
- Dùng khung bo góc, cận mặt và nét nhấn phản ứng khi phù hợp nhịp truyện.
- Mimi là thú cưng của Ngang. Vị trí, tương tác và hành động phải thể hiện quan hệ này.
- Bối cảnh phục vụ nội dung bài hát hoặc kịch bản từng cảnh.
- Chữ tiếng Việt được dựng bằng font đã kiểm tra glyph và được Owner chọn. Kiểm tra lại chính tả từ nội dung nguồn trước khi xuất video.
- Font chọn theo nội dung và phê duyệt từng video. EP10 đã dùng **Itim** do Owner chọn; các tập khác có thể dùng Be Vietnam Pro. Kiểm tra dấu tiếng Việt và license OFL đi kèm font.


## 7. Video theo nhạc, revision và bài học đã áp dụng

- Dùng MP3 do Owner cung cấp và đoạn lời/đoạn nhạc đã chọn; thời lượng theo bản thu. Không chạy TTS chồng lên bài hát. Căn theo từ, kiểm tra cả khoảng nghỉ trước từ đầu; chỉ gọi là khớp sau khi có kiểm chứng phù hợp.
- Phụ đề có thể dùng word reveal/highlight và icon vector theo tình huống. Kiểm tra trên MP4 thực, cả trước và sau mốc câu, không chỉ dựa vào storyboard.
- Theo dõi trạng thái Mimi và đạo cụ giữa các shot; sprite có sẵn lồng/điện thoại phải được kiểm tra ở mọi lần tái sử dụng. Cảnh tương tác gần cần kiểm tra điểm tiếp xúc và silhouette; tránh tim che mặt hoặc dissolve tạo bóng đôi.
- Outro NMT và cú twist theo brief: không tiết lộ sớm so với nhạc/lời, đủ thời gian đọc phản ứng/câu chốt; logo không chèn hai lần.
- EP10 có renderer/timing/export riêng theo revision, không phải mọi bước đã được tích hợp vào template CLI chung. Bản cuối: `output/ep10_vi_anh_qua_dep_trai/revisions/v04/`, giao tại `videos-post/vi-anh-qua-dep-trai/` (ba nền tảng; chưa đăng).
- Khi tiếp tục một tập có `CURRENT_PREVIEW.json`, đọc revision đang hoạt động và xác minh hash/workflow tương ứng trước khi render, duyệt hoặc xuất. Giữ các phiên bản cũ và lịch sử phê duyệt, không xuất nhầm `final_video.mp4` cũ ở thư mục gốc tập.

## 8. Tên và phạm vi

Owner yêu cầu đổi tên từ `couple-engine` sang `nmt-engine` ngày 08/11/2026. Đây là thay đổi tên entry point, mô tả và tài liệu; giữ nguyên kiến trúc Factory Manager + 7 Agent, cổng duyệt, thư viện nhân vật và đầu ra đã xuất. Các tên cũ trong trích dẫn Owner, Scope Grant hoặc báo cáo lịch sử là dấu vết tại thời điểm đó, không phải lệnh chính mới.
