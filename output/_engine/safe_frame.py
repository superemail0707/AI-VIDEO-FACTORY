"""Khung an toàn thống nhất cho video dọc 9:16 (Owner 08/11/2026) — NMT-SAFE-916 v1.

Vì sao cần: TikTok và YouTube Shorts hiển thị video 9:16 kiểu "lấp đầy" (aspect-fill) trên điện thoại
màn hình dài hơn 9:16 (19.5:9, 20:9): video bị phóng to theo chiều cao và cắt hai bên, đồng thời
thanh trạng thái/tab ở đỉnh và caption/nút ở đáy đè lên video. Facebook Reels thường hiển thị vừa khung,
nên ít lỗi hơn, nhưng vẫn dùng chung khung này để ba bản giống nhau.

Mọi số đo theo khung 1080×1920. Đây là ước lượng bảo thủ (giao diện app đổi theo phiên bản/máy);
luôn xem thử trên điện thoại trước khi đăng.

CLI:  python3 safe_frame.py preview <video.mp4> [giây ...] [-o out.png]
      → ghép khung hình có vẽ vùng cắt/vùng giao diện/vùng an toàn để kiểm tra bằng mắt.
"""
import os
import subprocess
import sys
import tempfile

W, H = 1080, 1920
SPEC = "NMT-SAFE-916 v1"

# Cắt hai bên khi app lấp đầy màn hình dài (20:9 → còn rộng 1920*9/20 = 864 px, mất 108 px mỗi bên).
CROP_X = 108
# Vùng giao diện app (hợp của TikTok, YouTube Shorts, Facebook Reels).
TOP_UI = 200            # thanh trạng thái + tab "Dành cho bạn"/tìm kiếm/camera
BOTTOM_UI = 300         # caption, tên kênh, nhạc, nút đăng ký (phần chắc chắn bị đè)
RIGHT_UI = 130          # cột nút tim/bình luận/chia sẻ (tính từ mép phải khung gốc)

# Bố cục chuẩn (dời xuống so với bố cục cũ 0–1440 / phụ đề tâm ~1518).
CONTENT_TOP = 200       # mép trên khung tranh; phía trên chỉ là màu nền trơn
HEAD_MIN_Y = 240        # đỉnh đầu nhân vật thấp nhất được phép
CONTENT_BOTTOM = 1460   # mép dưới vùng nội dung = mép trên dải phụ đề
SUB_TOP = 1480          # mép trên viên phụ đề
SUB_CENTER_Y = 1540     # tâm phụ đề 1 dòng
SUB_BOTTOM_MAX = 1680   # phụ đề 2 dòng không vượt quá (ưu tiên 1 dòng)
SUB_X_CENTER = W // 2   # Owner 08/11/2026: viền phụ đề LUÔN canh giữa màn hình (rộng ≤ 800 → x 140–940, vẫn né cột nút phải)
SUB_CENTER_TOL = 2      # sai lệch tâm cho phép (px)
SUB_MAX_W = 800
SAFE_X0, SAFE_X1 = CROP_X, W - RIGHT_UI   # 108 … 950: mặt, chữ, logo, viền khung phải nằm trong đây

# Watermark NMT phải nằm trong vùng không bị cắt: mép phải ≤ W - CROP_X - 12.
WM_MIN_MARGIN_X = CROP_X + 12   # 120 px


def check_box(box, kind="text"):
    """box = (x0, y0, x1, y1). Trả về danh sách vi phạm (rỗng = đạt)."""
    x0, y0, x1, y1 = box
    bad = []
    xr = W - CROP_X if kind == "watermark" else SAFE_X1
    if x0 < SAFE_X0 or x1 > xr:
        bad.append("ra ngoài vùng không bị cắt ngang (%d–%d)" % (SAFE_X0, xr))
    if y0 < (HEAD_MIN_Y if kind == "head" else CONTENT_TOP):
        bad.append("lấn vào vùng giao diện đỉnh (< %d)" % CONTENT_TOP)
    if kind == "subtitle" and (y0 < SUB_TOP - 20 or y1 > SUB_BOTTOM_MAX):
        bad.append("phụ đề ngoài dải %d–%d" % (SUB_TOP, SUB_BOTTOM_MAX))
    if kind == "subtitle" and abs((x0 + x1) / 2 - SUB_X_CENTER) > SUB_CENTER_TOL:
        bad.append("viền phụ đề không canh giữa màn hình (tâm x=%.0f, phải là %d)" % ((x0 + x1) / 2, SUB_X_CENTER))
    if kind in ("text", "head") and y1 > CONTENT_BOTTOM:
        bad.append("lấn xuống dải phụ đề (> %d)" % CONTENT_BOTTOM)
    return bad


def wm_override(ov=None):
    """Ghi đè watermark để logo nằm trong vùng không bị cắt (dùng cho cả lúc né phụ đề lẫn lúc chèn)."""
    ov = dict(ov or {})
    ov["margin_x"] = max(int(ov.get("margin_x", 0)), WM_MIN_MARGIN_X)
    return ov


_GRAD = {}


def reframe(content, band_col=(255, 246, 236), backdrop=None, radius=40, outline=(239, 193, 181), outline_w=4):
    """Đặt ảnh nội dung (bố cục cũ, vd. 1080×1440) thành một khung tranh gọn trong vùng an toàn
    x CROP_X…W-CROP_X, y CONTENT_TOP…CONTENT_BOTTOM: thu theo chiều cao, cắt bớt hai mép nền cho vừa bề rộng,
    bo góc. Xung quanh là màu trơn (Owner 08/11/2026: KHÔNG làm mờ phần xung quanh)."""
    from PIL import Image, ImageDraw
    content = content.convert("RGBA")
    cw, ch = content.size
    th = CONTENT_BOTTOM - CONTENT_TOP
    tw = W - 2 * CROP_X
    s = th / ch
    src_w = tw / s
    if src_w > cw:                      # nội dung hẹp hơn khung: giữ nguyên bề rộng
        src_w, tw = cw, round(cw * s)
    x0 = (cw - src_w) / 2
    panel = content.crop((round(x0), 0, round(x0 + src_w), ch)).resize((tw, th), Image.LANCZOS)
    out = Image.new("RGBA", (W, H), tuple(band_col) + (255,))
    if backdrop is not None:
        out.paste(tuple(backdrop) + (255,), (0, 0, W, CONTENT_BOTTOM))
    px = (W - tw) // 2
    m = _round_mask(tw, th, radius)
    out.paste(panel, (px, CONTENT_TOP), m)
    if outline_w:
        ImageDraw.Draw(out).rounded_rectangle((px, CONTENT_TOP, px + tw - 1, CONTENT_TOP + th - 1), radius,
                                              outline=tuple(outline) + (255,), width=outline_w)
    return out


def _round_mask(w, h, r):
    k = ("round", w, h, r)
    if k not in _GRAD:
        from PIL import Image, ImageDraw
        big = Image.new("L", (w * 2, h * 2), 0)
        ImageDraw.Draw(big).rounded_rectangle((0, 0, w * 2 - 1, h * 2 - 1), r * 2, fill=255)
        _GRAD[k] = big.resize((w, h), Image.LANCZOS)
    return _GRAD[k]


def map_point(x, y, src_w=1080, src_h=1440):
    """Toạ độ trong ảnh nội dung cũ → toạ độ trên khung đã reframe."""
    s = (CONTENT_BOTTOM - CONTENT_TOP) / src_h
    return W / 2 + (x - src_w / 2) * s, CONTENT_TOP + y * s


def _overlay_filter():
    """Vẽ vùng cắt (đỏ), vùng giao diện (cam), dải phụ đề (xanh) bằng drawbox của ffmpeg."""
    boxes = [
        (0, 0, CROP_X, H, "red@0.35"), (W - CROP_X, 0, CROP_X, H, "red@0.35"),
        (0, 0, W, TOP_UI, "orange@0.35"), (0, H - BOTTOM_UI, W, BOTTOM_UI, "orange@0.35"),
        (W - RIGHT_UI, 600, RIGHT_UI, 900, "orange@0.30"),
        (SUB_X_CENTER - SUB_MAX_W // 2, SUB_TOP, SUB_MAX_W, SUB_BOTTOM_MAX - SUB_TOP, "cyan@0.9:t=6"),
        (SAFE_X0, CONTENT_TOP, SAFE_X1 - SAFE_X0, CONTENT_BOTTOM - CONTENT_TOP, "lime@0.9:t=6"),
    ]
    out = []
    for x, y, w, h, c in boxes:
        col, _, t = c.partition(":t=")
        out.append("drawbox=x=%d:y=%d:w=%d:h=%d:color=%s:t=%s" % (x, y, w, h, col, t or "fill"))
    return ",".join(out)


def preview(video, times, out):
    tmp = tempfile.mkdtemp(prefix="safe_")
    pngs = []
    for i, t in enumerate(times):
        p = os.path.join(tmp, "f%02d.png" % i)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1",
                        "-vf", "scale=%d:%d,%s,scale=360:-1" % (W, H, _overlay_filter()), p], check=True)
        if not os.path.exists(p):
            raise SystemExit("Không lấy được khung tại %ss (vượt thời lượng video?)" % t)
        pngs.append(p)
    args = ["ffmpeg", "-v", "error", "-y"]
    for p in pngs:
        args += ["-i", p]
    args += ["-filter_complex", "hstack=inputs=%d" % len(pngs) if len(pngs) > 1 else "null", out]
    subprocess.run(args, check=True)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2 or a[0] != "preview":
        sys.exit(__doc__)
    out = "safe_preview.png"
    if "-o" in a:
        i = a.index("-o")
        out = a[i + 1]
        del a[i:i + 2]
    ts = [float(x) for x in a[2:]] or [2.0, 10.0, 20.0]
    print(preview(a[1], ts, out))
