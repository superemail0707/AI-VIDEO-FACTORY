"""Thư viện cảnh dùng chung cho các tập tranh full-bleed (Giai đoạn A, kế hoạch NMT_PIPELINE_UPGRADE_PLAN).

Gom các hàm phụ trợ đã chép tay ở EP11–EP19 (episode_safe_post, art, cam, mix, flash, pop, sparkle…).
Bản chuẩn = bản EP19 (mới nhất, đã duyệt). Biến thể của EP17/EP18 có tham số riêng.
Tập cũ KHÔNG đổi; chỉ tập mới import module này:

    import scene_kit as K
    K.install_post()                       # phụ đề hậu kỳ canh giữa 1480–1680, né watermark
    art = K.art_loader(ART_DIR)            # tranh image_gen phủ toàn khung 1080×1920
    out = K.cam(art('A01'), z=1.05)
"""
import math
import os
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

import cute_engine as E

W, H = E.W, E.H
GOLD = (255, 214, 92)
SWEAT = (150, 215, 255)
STAR_WHITE = (255, 250, 225)


# ---------------------------------------------------------------- phụ đề hậu kỳ (full-bleed)
def make_post(subtitles=True, pill_hook=None):
    """Trả về hàm safe_post cho tranh full-bleed (bản EP16/EP19).

    subtitles=False: bỏ phụ đề hoàn toàn (phim không thoại, như EP18).
    pill_hook(text, pim, s) -> (pim, s): đổi viên phụ đề cho câu đặc biệt (highlight EP17); gọi trước khi né watermark.
    """
    def episode_safe_post(im):
        if not subtitles:
            E._SUB_PENDING = None
            return im
        import safe_frame as SF
        from cute_engine import WM_PAD, DRAW_SUB, sub_pill, put, _wm_for_layout
        if im.size != (W, H):
            return im
        out = im.copy()
        pend, E._SUB_PENDING = E._SUB_PENDING, None
        if pend:
            pim, s, alpha, pin, text = pend
            if pill_hook is not None:
                pim, s = pill_hook(text, pim, s)
            x = SF.SUB_X_CENTER
            y = SF.SUB_TOP + pim.height / 2
            wm = _wm_for_layout()
            if wm and y + pim.height / 2 + 26 > wm[1] - WM_PAD and x + pim.width / 2 > wm[0] - WM_PAD:
                half = wm[0] - WM_PAD - x
                pim = sub_pill(text, maxw=max(300, int(2 * half) - 104))
                y = SF.SUB_TOP + pim.height / 2
            yy = y + 26 * (1 - pin)
            # Bài học EP20: viên 2 dòng đang trượt vào (pin < 1) lố đáy dải 1680 vài px → kẹp đáy trong dải
            yy = min(yy, SF.SUB_BOTTOM_MAX - pim.height * s / 2)
            if alpha > 0.05:
                E.SUB_BOX = (x - pim.width * s / 2, yy - pim.height * s / 2, x + pim.width * s / 2, yy + pim.height * s / 2)
            if DRAW_SUB:
                put(out, pim, x, yy, s=s, alpha=alpha)
        return out
    return episode_safe_post


def install_post(subtitles=True, pill_hook=None):
    """Gắn safe_post full-bleed vào engine (thay cho `E.safe_post = episode_safe_post` chép tay)."""
    E.safe_post = make_post(subtitles=subtitles, pill_hook=pill_hook)
    return E.safe_post


# ---------------------------------------------------------------- tranh
def art_loader(*dirs, aliases=None, cache=32):
    """Hàm art(name): mở <dir>/<name>.png, fit phủ kín 1080×1920 (LANCZOS), có cache.

    Nhiều thư mục: tìm lần lượt. aliases={'ep17_': '/đường/dẫn/EP17/art/v02'} cho tranh mượn tập khác (EP18).
    """
    dirs = [Path(d) for d in dirs]
    aliases = {k: Path(v) for k, v in (aliases or {}).items()}

    @lru_cache(maxsize=cache)
    def art(name):
        for pre, d in aliases.items():
            if name.startswith(pre):
                p = d / (name[len(pre):] + '.png')
                break
        else:
            p = next((d / (name + '.png') for d in dirs if (d / (name + '.png')).exists()), dirs[0] / (name + '.png'))
        return ImageOps.fit(Image.open(p).convert('RGBA'), (W, H), Image.Resampling.LANCZOS)
    return art


# ---------------------------------------------------------------- máy quay
def cam(im, z=1.0, **k):
    """E.cam nhưng không cho z < 1 (e_back vọt quá có thể kéo z xuống dưới 1 → lộ viền).
    EP31 20/11/2026: E.cam trả lại CHÍNH ảnh vào khi z = 1 và không lệch → cảnh vẽ chữ/lấp lánh lên ảnh đó làm bẩn
    tranh trong bộ nhớ đệm art_loader (bóng chữ mờ ở mọi khung sau). Luôn trả bản sao."""
    out = E.cam(im, z=max(1.0, z), **k)
    return out.copy() if out is im else out


def top_cam(im, z, cx, sx=0.0, sy=0.0):
    """Zoom neo mép trên: điểm y gốc → y·z. Dải phụ đề ứng với y gốc ≥ 1480/z."""
    return cam(im, z=z, cx=cx, cy=H / (2 * z), sx=sx, sy=sy)


def shaken(out, t, t0, d=0.3, a=10):
    sx, sy = E.shake(t, t0, d=d, a=a)
    return cam(out, z=1.02, sx=sx, sy=sy) if (sx or sy) else out


def jitter(t, a):
    """Run bần bật liên tục: (dx, dy)."""
    return a * math.sin(t * 91), a * 0.6 * math.cos(t * 73)


# ---------------------------------------------------------------- nhịp, chớp
def mix(a, b, p):
    return a + (b - a) * p


def flash(out, a=0.45, col=(255, 248, 220)):
    return Image.blend(out, Image.new('RGBA', (W, H), col + (255,)), max(0.0, min(1.0, a)))


def pop(t, t0, d=0.22):
    """Hệ số nảy 1 → 1,12 → 1 trong d giây kể từ t0."""
    if t < t0:
        return 0.0
    p = E.clamp((t - t0) / d)
    return 1.0 + 0.12 * math.sin(math.pi * p) if p < 1 else 1.0


# ---------------------------------------------------------------- thoại, phụ đề, mốc tiếng
def sub(im, sid, t):
    """Phụ đề dưới cùng (dải 1480–1680) cho cảnh sid ở thời điểm cục bộ t."""
    E.subtitle(im, E.STARTS.get(sid, 0.0) + t, y=E.sub_y_bottom(), tray=False)


def vt(vid, default):
    """(thời điểm bắt đầu trong cảnh, độ dài) của câu vid; default nếu chưa có giọng."""
    for v, sid, lt, *_ in E.VOICE:
        if v == vid:
            return lt, E.VDUR.get(vid, default[1])
    return default


def cut_at(vid, default=0.0):
    """Mốc cắt hình gắn với câu vid = đầu câu + onset tiếng thật đo trong WAV (bài học EP19: hình không đi trước tiếng)."""
    for v, sid, lt, *_ in E.VOICE:
        if v == vid:
            return lt + E.voice_onset(vid)
    return default


# ---------------------------------------------------------------- hiệu ứng vẽ
@lru_cache(maxsize=16)
def sparkle(size=70, col=STAR_WHITE, k=0.12, blur=0.0):
    """Sao 4 cánh. Bản EP19: k=0.12, không blur. Bản EP18: k=0.10, blur=0.6."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    c = size / 2
    ImageDraw.Draw(im).polygon([(c, 0), (c + size * k, c - size * k), (size, c), (c + size * k, c + size * k),
                                (c, size), (c - size * k, c + size * k), (0, c), (c - size * k, c - size * k)],
                               fill=col + (255,))
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im


def twinkles(out, t, pts, period=0.9, col=STAR_WHITE, size=70, thr=0.15, s0=0.4):
    """Sao lấp lánh tại các điểm pts, lệch pha. EP18: period=0.8, size=60, thr=0.2, s0=0.3."""
    for i, (x, y) in enumerate(pts):
        ph = (t / period + i * 0.37) % 1.0
        s = math.sin(ph * math.pi)
        if s > thr:
            E.put(out, sparkle(size, col), x, y, s=s0 + (1 - s0) * s, rot=ph * 90, alpha=s)


@lru_cache(maxsize=4)
def drop(size=46, col=SWEAT):
    im = Image.new('RGBA', (size, int(size * 1.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((4, size * 0.4, size - 4, size * 1.36), fill=col + (255,), outline=(40, 60, 90, 255), width=3)
    d.polygon([(size / 2, 2), (6, size * 0.8), (size - 6, size * 0.8)], fill=col + (255,))
    d.ellipse((size * 0.28, size * 0.75, size * 0.45, size * 0.95), fill=(255, 255, 255, 230))
    return im


def sweat_burst(out, t, t0, x, y, n=5, per=0.55):
    """Mồ hôi văng tỏa ra từ đầu, lặp mỗi `per` giây."""
    if t < t0:
        return
    ph = ((t - t0) / per) % 1.0
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * 0.55
        r = 70 + 190 * ph
        E.put(out, drop(), x + r * math.cos(a), y + r * math.sin(a) + 120 * ph ** 2, s=0.8,
              rot=-math.degrees(a + math.pi / 2), alpha=1 - ph)


def bubble(out, x, y, r, alpha=0.9):
    b = Image.new('RGBA', (int(2 * r + 8), int(2 * r + 8)), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(225, 245, 255, 140), outline=(90, 140, 190, 255), width=4)
    d.ellipse((r * 0.5, r * 0.45, r * 0.85, r * 0.8), fill=(255, 255, 255, 240))
    E.put(out, b, x, y, alpha=alpha)


def shock_lines(out, t, t0, x, y, n=7, r0=150, col=GOLD):
    if t < t0:
        return
    p = E.clamp((t - t0) / 0.18)
    d = ImageDraw.Draw(out)
    for i in range(n):
        a = -math.pi * (0.15 + 0.7 * i / (n - 1))
        r1, r2 = r0 * (0.9 + 0.2 * p), r0 * (0.9 + 0.2 * p) + 70 * p
        d.line([(x + r1 * math.cos(a), y + r1 * math.sin(a)), (x + r2 * math.cos(a), y + r2 * math.sin(a))],
               fill=col + (255,), width=12)


def zzz_bubbles(out, t, x, y):
    """Bong bóng ngủ bay lên (không chữ)."""
    for i in range(3):
        ph = (t / 1.6 + i / 3) % 1.0
        bubble(out, x + 40 * math.sin(ph * 6 + i), y - 260 * ph, 14 + 26 * ph, alpha=1 - ph ** 2)


def stars_orbit(out, t, x, y, rx=150, ry=40, col=GOLD):
    for i in range(4):
        a = t * 5 + i * math.pi / 2
        E.put(out, sparkle(56, col), x + rx * math.cos(a), y + ry * math.sin(a), s=0.8, rot=a * 40)


# ---------------------------------------------------------------- máy quay theo chú thích vùng an toàn (EP21, 13/11/2026)
FACE_X_MIN, FACE_X_MAX, CONTENT_BOTTOM, HEAD_MIN_Y = 108, 972, 1460, 200


def P_of(cx, cy, z):
    """Đổi toạ độ tranh gốc → khung sau cam(z, cx, cy) (cùng phép kẹp với E.cam)."""
    z = max(1.0, z)
    x0 = E.clamp(cx - W / z / 2, 0, W - W / z)
    y0 = E.clamp(cy - H / z / 2, 0, H - H / z)
    return lambda x, y: ((x - x0) * z, (y - y0) * z)


def load_annotations(art_dir):
    import json
    p = Path(art_dir) / 'safe_annotations.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def safe_z(ann, z, cx=W / 2, cy=H / 2, subs=True, step=0.005):
    """Giảm z (không dưới 1) tới khi mặt (face_x) vẫn trong 108–972 và, nếu có phụ đề, đáy nhân vật ≤ 1460.

    ann = mục của tranh trong safe_annotations.json. Bài học EP20/EP21: zoom làm mặt sát mép trôi vào lề cắt TikTok.
    """
    ann = ann or {}
    fx, bot = ann.get('face_x'), ann.get('char_bottom_y')
    z = max(1.0, z)
    while z > 1.0:
        P = P_of(cx, cy, z)
        ok = True
        if fx:
            ok &= P(fx[0], 0)[0] >= FACE_X_MIN and P(fx[1], 0)[0] <= FACE_X_MAX
        if subs and ann.get('subtitles', True) and bot is not None:
            ok &= P(0, bot)[1] <= CONTENT_BOTTOM
        if ok:
            return z
        z = max(1.0, z - step)
    return 1.0


def safe_cam(im, ann, z=1.0, cx=W / 2, cy=H / 2, sx=0.0, sy=0.0, subs=True):
    """cam() với z đã kẹp theo safe_z. Trả (ảnh, z thực dùng)."""
    zz = safe_z(ann, z, cx, cy, subs)
    return cam(im, z=zz, cx=cx, cy=cy, sx=sx, sy=sy), zz


def card(out, text, y=262, s=1.0, alpha=1.0, bg=(30, 30, 36, 235), fg=(255, 214, 92, 255), size=44):
    """Thẻ chữ nhỏ canh giữa ở đỉnh vùng an toàn (y ≥ 236): 'HỒ SƠ', '03:00', 'NGHI PHẠM #1'…"""
    lab = E.pill(text, size=size, bg=bg, fg=fg, outline=fg)
    E.put(out, lab, W / 2, y, s=s, alpha=alpha)
    return out


@lru_cache(maxsize=8)
def heart(size=64, col=(255, 110, 150)):
    """Trái tim vẽ bằng hình (không phụ thuộc font có ký tự ♥). Bản EP20."""
    im = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = size * 0.5
    d.ellipse((size * 0.5 - r, size * 0.6 - r, size * 0.5 + r, size * 0.6 + r), fill=col + (255,))
    d.ellipse((size * 1.5 - r, size * 0.6 - r, size * 1.5 + r, size * 0.6 + r), fill=col + (255,))
    d.polygon([(size * 0.04, size * 0.8), (size * 1.96, size * 0.8), (size, size * 1.9)], fill=col + (255,))
    return im


def float_hearts(out, t, pts, period=1.6, size=40):
    """Tim bay lên rồi mờ dần quanh các điểm pts (toạ độ khung)."""
    for i, (x, y) in enumerate(pts):
        ph = (t / period + i * 0.37) % 1.0
        E.put(out, heart(size), x + 18 * math.sin(ph * 6 + i), y - 160 * ph, s=0.6 + 0.5 * ph, alpha=1 - ph ** 2)
    return out


# ---------------------------------------------------------------- cảnh kết kêu gọi Like / Share / Subscribe (Owner 13/11/2026)
# Thiết kế (góp ý Owner lần 2): 3 nút tròn TAI MÈO trên MỘT hàng; chân mèo Mimi (trắng, đệm hồng) lần lượt bấm từng nút
# → nút lún xuống, đổi trạng thái, bung hạt; hạt/nền đổi theo chủ đề tập (theme): 'paws' dấu chân, 'snow' tuyết, 'stars' sao.
OUTRO_TITLE = 'Outro'          # tên cảnh: --check-transitions bắt buộc vào cảnh này bằng 'cut'
OUTRO_DUR = 3.6
OUTRO_Y = 1000                 # tâm hàng nút; mọi phần tử trong x 130–950, y 300–1400
OUTRO_X = (270, 540, 810)
OUTRO_TAPS = (1.0, 1.7, 2.4)  # mốc chân mèo bấm LIKE, SHARE, SUBSCRIBE (SFX của tập canh theo mốc này)
_PINK, _BLUE, _RED, _GREY = (255, 95, 130), (70, 160, 255), (235, 40, 50), (125, 125, 138)
_PAD = (255, 160, 180)


def _cat_button(col, size=230):
    """Nút tròn có hai tai mèo (tai cùng màu, lòng tai hồng), viền trắng."""
    pad = int(size * 0.28)
    im = Image.new('RGBA', (size, size + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for sx in (-1, 1):
        cx = size / 2 + sx * size * 0.3
        ear = [(cx - size * 0.16, pad + size * 0.18), (cx + sx * size * 0.06, 0), (cx + size * 0.16, pad + size * 0.18)]
        d.polygon(ear, fill=col + (255,), outline=(255, 255, 255, 255))
        inner = [(cx - size * 0.08, pad + size * 0.12), (cx + sx * size * 0.05, pad * 0.35), (cx + size * 0.08, pad + size * 0.12)]
        d.polygon(inner, fill=_PAD + (255,))
    d.ellipse((0, pad, size - 1, pad + size - 1), fill=col + (255,), outline=(255, 255, 255, 255), width=7)
    return im, pad


def _glyph_share(im, cx, cy, k, col=(255, 255, 255)):
    """Biểu tượng chia sẻ chuẩn: 3 nút tròn nối 2 nét (trái giữa → phải trên, phải dưới), vẽ khử răng cưa (x4 rồi thu nhỏ)."""
    S = 4
    r_node, w_line = 15 * k, 9 * k
    pts = [(-30 * k, 0), (28 * k, -30 * k), (28 * k, 30 * k)]
    size = int(140 * k)
    big = Image.new('RGBA', (size * S, size * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    o = size * S / 2
    P = [(o + x * S, o + y * S) for x, y in pts]
    for q in P[1:]:
        d.line([P[0], q], fill=col + (255,), width=int(w_line * S))
    for x, y in P:
        R = r_node * S
        d.ellipse((x - R, y - R, x + R, y + R), fill=col + (255,))
    small = big.resize((size, size), Image.Resampling.LANCZOS)
    im.alpha_composite(small, (int(cx - size / 2), int(cy - size / 2)))


def _button(kind, on):
    """kind: like|share|sub; on: đã bấm. Trả ảnh nút + toạ độ tâm hình tròn trong ảnh."""
    col = {'like': _PINK, 'share': _BLUE, 'sub': _GREY if on else _RED}[kind]
    if kind == 'like' and not on:
        col = (238, 150, 172)
    im, pad = _cat_button(col)
    c = (im.width / 2, pad + im.width / 2)
    if kind == 'like':
        E.put(im, heart(64 if on else 54, (255, 255, 255)), c[0], c[1] + 8)
    elif kind == 'share':
        _glyph_share(im, c[0], c[1], 1.4)
    else:
        E.put(im, _bell(104), c[0], c[1] + 2)
    return im, c


def _bell(size=56, col=(255, 255, 255)):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size
    d.pieslice((s * 0.18, s * 0.08, s * 0.82, s * 0.9), 180, 360, fill=col + (255,))
    d.rectangle((s * 0.18, s * 0.48, s * 0.82, s * 0.72), fill=col + (255,))
    d.polygon([(s * 0.08, s * 0.78), (s * 0.92, s * 0.78), (s * 0.82, s * 0.66), (s * 0.18, s * 0.66)], fill=col + (255,))
    d.ellipse((s * 0.4, s * 0.76, s * 0.6, s * 0.96), fill=col + (255,))
    return im


@lru_cache(maxsize=4)
def cat_paw(size=150):
    """Chân mèo Mimi làm 'con trỏ': cẳng sọc nâu, bàn chân trắng, 4 ngón + đệm hồng (nhìn từ dưới lên)."""
    s = size
    im = Image.new('RGBA', (s, int(s * 1.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * 0.22, s * 0.7, s * 0.78, s * 1.6), s * 0.2, fill=(150, 118, 88, 255), outline=(60, 45, 35, 255), width=4)
    for y in (0.95, 1.18, 1.41):
        d.line([(s * 0.26, s * y), (s * 0.74, s * (y - 0.06))], fill=(85, 62, 45, 255), width=int(s * 0.07))
    d.ellipse((s * 0.12, s * 0.28, s * 0.88, s * 0.98), fill=(255, 255, 255, 255), outline=(60, 45, 35, 255), width=4)
    d.ellipse((s * 0.3, s * 0.52, s * 0.7, s * 0.86), fill=_PAD + (255,))
    for x, y in ((0.14, 0.24), (0.34, 0.08), (0.56, 0.08), (0.76, 0.24)):
        d.ellipse((s * x, s * y, s * (x + 0.18), s * (y + 0.2)), fill=(255, 255, 255, 255), outline=(60, 45, 35, 255), width=3)
        d.ellipse((s * (x + 0.04), s * (y + 0.05), s * (x + 0.14), s * (y + 0.15)), fill=_PAD + (255,))
    return im


@lru_cache(maxsize=8)
def paw_print(size=44, col=(255, 160, 180)):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size
    d.ellipse((s * 0.25, s * 0.45, s * 0.75, s * 0.92), fill=col + (255,))
    for x, y in ((0.06, 0.32), (0.26, 0.1), (0.54, 0.1), (0.74, 0.32)):
        d.ellipse((s * x, s * y, s * (x + 0.2), s * (y + 0.24)), fill=col + (255,))
    return im


@lru_cache(maxsize=8)
def snowflake(size=40, col=(235, 245, 255)):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, r = size / 2, size * 0.46
    for k in range(6):
        a = math.pi * k / 3
        x, y = c + r * math.cos(a), c + r * math.sin(a)
        d.line([(c, c), (x, y)], fill=col + (255,), width=max(2, size // 12))
        for f in (0.55,):
            bx, by = c + r * f * math.cos(a), c + r * f * math.sin(a)
            for da in (-0.6, 0.6):
                d.line([(bx, by), (bx + r * 0.3 * math.cos(a + da), by + r * 0.3 * math.sin(a + da))], fill=col + (255,), width=max(2, size // 14))
    return im


def _particle(theme, size):
    if theme == 'paws':
        return paw_print(size)
    if theme == 'snow':
        return snowflake(size)
    if theme == 'hearts':
        return heart(size // 2 + 4)
    return sparkle(size, GOLD)


def burst(out, t, t0, x, y, theme, n=9, d=0.7, r1=190, size=40):
    """Bung hạt theo vòng tròn quanh (x, y) trong d giây kể từ t0."""
    if not (t0 <= t < t0 + d):
        return out
    p = (t - t0) / d
    e = 1 - (1 - p) ** 3
    for i in range(n):
        a = 2 * math.pi * i / n + 0.3
        rr = 40 + r1 * e
        E.put(out, _particle(theme, size), x + rr * math.cos(a), y + rr * math.sin(a) - 30 * p,
              s=0.6 + 0.6 * (1 - p), rot=40 * p * (1 if i % 2 else -1), alpha=1 - p ** 2)
    return out


def _ambient(out, t, theme):
    """Nền động nhẹ theo chủ đề: tuyết rơi / dấu chân bước ngang (callback tập thám tử) / sao lấp lánh."""
    if theme == 'snow':
        for i in range(16):
            x = (97 * i + 40 * math.sin(t * 1.3 + i)) % W
            y = (230 + (i * 113 + t * (90 + 7 * i)) % 1250)
            E.put(out, snowflake(26 + (i % 3) * 8), x, y, alpha=0.75)
    elif theme == 'paws':
        for k in range(8):
            tk = 0.15 + k * 0.32
            if t >= tk:
                x = 150 + k * 110
                y = 1330 + (24 if k % 2 else -24)
                E.put(out, paw_print(52, (255, 190, 205)), x, y, rot=-90, alpha=min(0.85, (t - tk) / 0.15))
    else:
        twinkles(out, t, [(200, 380), (880, 420), (180, 1280), (900, 1300)], 0.9, GOLD, size=46)
    return out


def outro_cta(t, bg, dur=OUTRO_DUR, title='Thích thì bấm nút nha!', theme='stars'):
    """Cảnh kết ~3,6 s: nền = tranh cảnh cuối tối 65 %; 3 nút tai mèo LIKE · SHARE · SUBSCRIBE trên một hàng;
    chân mèo bấm lần lượt (OUTRO_TAPS): nút lún 0,88, đổi trạng thái, bung hạt (like: tim; share: dấu chân; sub: theo theme)."""
    out = Image.blend(bg.convert('RGBA'), Image.new('RGBA', (W, H), (12, 14, 30, 255)), 0.62)
    _ambient(out, t, theme)
    panel = Image.new('RGBA', (W, H), (0, 0, 0, 0))   # thẻ kính mờ tối sau hàng nút cho dễ đọc trên nền rối
    ImageDraw.Draw(panel).rounded_rectangle((122, 540, 958, 1250), 60, fill=(14, 16, 34, int(150 * E.clamp(t / 0.25))))
    out.alpha_composite(panel)
    head = E.text_img(title, 76, fill=(255, 255, 255, 255), weight='ExtraBold', stroke=6, sfill=(30, 30, 40, 255))
    E.put(out, head, W / 2, 640, s=pop(t, 0.05, 0.3) or 1.0, alpha=E.clamp(t / 0.25))
    kinds = (('like', 'LIKE', 'hearts'), ('share', 'SHARE', 'paws'), ('sub', 'SUBSCRIBE', theme))
    for i, (kind, lab, part) in enumerate(kinds):
        t_in, tap, x = 0.2 + 0.12 * i, OUTRO_TAPS[i], OUTRO_X[i]
        if t < t_in:
            continue
        on = t >= tap + 0.06
        btn, c = _button(kind, on)
        s = pop(t, t_in, 0.3) or 1.0
        if tap <= t < tap + 0.14:
            s *= 0.88                                   # lún xuống khi bấm
        elif on:
            s *= pop(t, tap + 0.14, 0.25) or 1.0         # nảy lại
        rot = 0.0
        if kind == 'sub' and on:
            rot = 14 * math.sin((t - tap) * 28) * math.exp(-(t - tap) * 3)   # chuông rung
        yb = OUTRO_Y - c[1] + btn.height / 2
        E.put(out, btn, x, yb, s=s, rot=rot)
        if on:
            burst(out, t, tap, x, OUTRO_Y, part, n=8 if kind != 'sub' else 11, r1=150 if kind != 'sub' else 210,
                  size=42 if kind != 'sub' else 48)
        txt = 'ĐÃ ĐĂNG KÝ' if (kind == 'sub' and on) else lab
        col = (255, 214, 92, 255) if on else (255, 255, 255, 255)
        E.put(out, E.text_img(txt, 44, fill=col, weight='ExtraBold', stroke=5, sfill=(30, 30, 40, 255)),
              x, OUTRO_Y + 165, alpha=E.clamp((t - t_in) / 0.2))
    # chân mèo: vào từ dưới phải, chạm lần lượt 3 nút, rồi rút ra
    t_enter, t_out = OUTRO_TAPS[0] - 0.35, OUTRO_TAPS[-1] + 0.45
    if t_enter <= t < t_out + 0.35:
        path = [(OUTRO_X[0], OUTRO_TAPS[0]), (OUTRO_X[1], OUTRO_TAPS[1]), (OUTRO_X[2], OUTRO_TAPS[2])]
        if t < OUTRO_TAPS[0]:
            p = E.e_io(E.clamp((t - t_enter) / 0.35))
            px, py = mix(700, path[0][0], p), mix(1600, OUTRO_Y + 10, p)
        elif t < OUTRO_TAPS[-1]:
            j = 0 if t < OUTRO_TAPS[1] else 1
            p = E.e_io(E.clamp((t - path[j][1] - 0.18) / (path[j + 1][1] - path[j][1] - 0.18)))
            px, py = mix(path[j][0], path[j + 1][0], p), OUTRO_Y + 10 - 70 * math.sin(math.pi * p)
        else:
            p = E.e_io(E.clamp((t - t_out) / 0.35))
            px, py = mix(path[2][0], 960, p), mix(OUTRO_Y + 10, 1700, p)
        press = any(tp <= t < tp + 0.14 for tp in OUTRO_TAPS)
        paw = cat_paw(190)
        E.put(out, paw, px + 14, py + paw.height / 2 - 70, s=0.9 if press else 1.0, rot=-12)   # ngón chạm nửa dưới nút, không che chữ
    return out


# ---------------------------------------------------------------- dấu hiệu thương hiệu (docs/marketing/BRAND_NMT.md, 13/11/2026)
BRAND_YELLOW = (255, 212, 92)
BRAND_INK = (34, 30, 36)


def ep_tag(out, name, t, t0=0.0, x=130, y=236):
    """Nhãn tập ở góc trên trái (dấu hiệu 4): nền vàng chữ đen 'NGANG MỘT TÍ · <tên tập>'; trượt vào 0,25 s."""
    lab = E.pill('NGANG MỘT TÍ · ' + name.upper(), size=34, bg=BRAND_YELLOW + (255,), fg=BRAND_INK + (255,),
                 outline=BRAND_INK + (255,), padx=22, pady=10)
    p = E.e_io(E.clamp((t - t0) / 0.25))
    E.put(out, lab, x + lab.width / 2 - (1 - p) * 60, y + lab.height / 2, alpha=p)
    return out


def boom(out, text, x, y, t, t0, size=150, fill=BRAND_YELLOW, ink=BRAND_INK, rot=-8, d=0.18):
    """Chữ cảm thán đóng dấu trên hình (XÈO!, CHÁY!!, RẮC!…) thay phụ đề: phóng to từ 1,7 → 1 trong d giây rồi rung nhẹ."""
    if t < t0:
        return out
    p = E.clamp((t - t0) / d)
    s = 1.7 - 0.7 * E.e_out(p)
    wob = 2.5 * math.sin((t - t0) * 30) * math.exp(-(t - t0) * 2.5)
    im = E.text_img(text, size, fill=fill + (255,), weight='ExtraBold', stroke=max(6, size // 14), sfill=ink + (255,))
    E.put(out, im, x, y, s=s, rot=rot + wob, alpha=0.4 + 0.6 * p)
    return out


def judge(im, t, face, z1=1.9, d=0.12):
    """'Mimi phán xét' (dấu hiệu 3): zoom GIẬT vào mặt Mimi (face=(x, y) trên tranh) trong d giây, giữ yên, viền tối.
    Cảnh không phụ đề; mặt Mimi là tâm khung nên không cần kẹp face_x."""
    p = E.e_out(E.clamp(t / d))
    z = 1.0 + (z1 - 1.0) * p
    out = cam(im, z=z, cx=face[0], cy=face[1])
    vig = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(vig).ellipse((-260, 120, W + 260, H - 120), fill=(0, 0, 0, 0), outline=(0, 0, 0, 150), width=320)
    out.alpha_composite(vig.filter(ImageFilter.GaussianBlur(90)))
    return out.copy()


def phone_frame(out, inner, x0=250, y0=420, w=580, h=1000, t=0.0, label=None):
    """Khung điện thoại vẽ bằng code (gọi video / thông báo): viền đen bo tròn, tai thỏ; inner = ảnh RGBA đặt vào màn hình."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0 - 18, y0 - 18, x0 + w + 18, y0 + h + 18), 70, fill=(25, 25, 30, 255))
    lay.alpha_composite(ImageOps.fit(inner.convert('RGBA'), (w, h)), (x0, y0))
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((x0, y0, x0 + w, y0 + h), 54, fill=255)
    hole = Image.new('L', (W, H), 255)
    ImageDraw.Draw(hole).rectangle((x0, y0, x0 + w, y0 + h), fill=0)
    mask = Image.composite(Image.new('L', (W, H), 255), hole, m)
    lay.putalpha(Image.composite(lay.getchannel('A'), Image.new('L', (W, H), 0), mask))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0 + w / 2 - 70, y0 + 10, x0 + w / 2 + 70, y0 + 40), 15, fill=(25, 25, 30, 255))
    if label:
        E.put(lay, E.pill(label, size=34, bg=(255, 255, 255, 235), fg=BRAND_INK + (255,), outline=(255, 255, 255, 255),
                          padx=18, pady=8), x0 + w / 2, y0 + 90)
    out.alpha_composite(lay)
    return out


def big_tick(out, x, y, t, t0, r=170, col=(60, 200, 110)):
    """Dấu tick xanh to trong vòng tròn, nảy vào (thông báo 'Đã giao')."""
    if t < t0:
        return out
    s = pop(t, t0, 0.3) or 1.0
    lay = Image.new('RGBA', (2 * r + 20, 2 * r + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse((10, 10, 2 * r + 10, 2 * r + 10), fill=col + (255,), outline=(255, 255, 255, 255), width=12)
    d.line([(r * 0.55 + 10, r * 1.05 + 10), (r * 0.9 + 10, r * 1.4 + 10), (r * 1.5 + 10, r * 0.7 + 10)],
           fill=(255, 255, 255, 255), width=int(r * 0.22), joint='curve')
    E.put(out, lay, x, y, s=s * E.clamp((t - t0) / 0.12 + 0.3, 0, 1))
    return out


@lru_cache(maxsize=1)
def _ruled():
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(180, H, 64):
        d.line((0, y, W, y), fill=(120, 160, 230, 110), width=3)
    d.line((150, 0, 150, H), fill=(240, 110, 120, 120), width=4)     # lề đỏ vở học sinh
    return lay


def paper(out, thr=242):
    """Khung nguệch ngoạc vẽ trên giấy vở kẻ ngang: dòng kẻ xanh + lề đỏ chỉ hiện trên vùng gần trắng
    (review EP23 lần 1: nửa dưới khung nguệch ngoạc trắng trống trông như bố cục chưa xong)."""
    g = out.convert('L')
    mask = g.point(lambda v: 255 if v >= thr else 0).filter(ImageFilter.MinFilter(5))
    lines = _ruled()
    a = Image.composite(lines.getchannel('A'), Image.new('L', (W, H), 0), mask)
    lay = lines.copy()
    lay.putalpha(a)
    out.alpha_composite(lay)
    return out


# ---------------------------------------------------------------- outro "Đăng ký" kiểu lower-third (Owner 13/11/2026, theo clip mẫu
# avatar_banner/ScreenRecording_11-13-2026 20-55-26_1.mov): avatar bật ra + vòng viền, vệt khói trắng, thanh trắng kéo dài,
# 3 nút LIKE (xám→xanh) · ĐĂNG KÝ (đỏ→xám "ĐÃ ĐĂNG KÝ") · CHUÔNG (vàng → rung → xám), con trỏ chuột bấm lần lượt,
# rồi thanh thu vào avatar, avatar xoáy vòng trắng và biến mất. Chỉ đổi avatar thành avatar kênh.
SUB_DUR = 7.8
SUB_AVATAR = Path(__file__).resolve().parents[2] / 'avatar_banner' / 'nmt_channel_avatar.png'
SUB_CY, SUB_AX, SUB_R = 1250, 250, 122          # tâm avatar; thanh trắng x 250–930, cao 124
SUB_X1 = 930
SUB_THUMB_X, SUB_PILL_X, SUB_BELL_X = 452, 662, 868
# mốc (giây trong cảnh): vào · bấm like · bấm đăng ký · bấm chuông · thu thanh · biến mất
SUB_T = {'pop': 0.0, 'smoke': 0.3, 'bar': 0.6, 'icons': 1.15, 'like': 3.0, 'sub': 4.4, 'bell': 5.5, 'retract': 6.6, 'vanish': 7.05}
_RED, _GRAY, _BLUE, _YEL = (214, 32, 39), (160, 160, 165), (52, 92, 230), (247, 183, 24)


@lru_cache(maxsize=2)
def _avatar(r=SUB_R):
    im = Image.open(SUB_AVATAR).convert('RGBA')
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((4 * r, 4 * r), Image.LANCZOS)
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).ellipse((4, 4, 4 * r - 4, 4 * r - 4), fill=255)
    im.putalpha(m)
    out = Image.new('RGBA', (4 * r + 24, 4 * r + 24), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse((0, 0, 4 * r + 23, 4 * r + 23), fill=(255, 255, 255, 255))     # viền trắng mảnh
    out.alpha_composite(im, (12, 12))
    return out.resize((2 * r + 6, 2 * r + 6), Image.LANCZOS)


@lru_cache(maxsize=4)
def _thumb(col, size=74):
    k = 4
    S = size * k
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = col + (255,)
    d.rounded_rectangle((int(.02 * S), int(.42 * S), int(.22 * S), int(.98 * S)), int(.04 * S), fill=c)          # cổ tay áo
    d.rounded_rectangle((int(.28 * S), int(.40 * S), int(.96 * S), int(.98 * S)), int(.12 * S), fill=c)          # nắm tay
    d.polygon([(int(.30 * S), int(.44 * S)), (int(.44 * S), int(.06 * S)), (int(.58 * S), int(.08 * S)),
               (int(.60 * S), int(.42 * S))], fill=c)                                                              # ngón cái
    d.ellipse((int(.42 * S), int(.0 * S), int(.62 * S), int(.18 * S)), fill=c)
    for y in (.56, .70, .84):
        d.line((int(.66 * S), int(y * S), int(.96 * S), int(y * S)), fill=(255, 255, 255, 255), width=int(.035 * S))
    return im.resize((size, size), Image.LANCZOS)


@lru_cache(maxsize=4)
def _bell2(col, size=72):
    k = 4
    S = size * k
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = col + (255,)
    d.ellipse((int(.42 * S), int(.0 * S), int(.58 * S), int(.16 * S)), fill=c)
    d.pieslice((int(.16 * S), int(.08 * S), int(.84 * S), int(.80 * S)), 180, 360, fill=c)
    d.polygon([(int(.16 * S), int(.44 * S)), (int(.84 * S), int(.44 * S)), (int(.94 * S), int(.80 * S)), (int(.06 * S), int(.80 * S))], fill=c)
    d.rounded_rectangle((int(.02 * S), int(.74 * S), int(.98 * S), int(.84 * S)), int(.05 * S), fill=c)
    d.ellipse((int(.38 * S), int(.80 * S), int(.62 * S), int(1.0 * S) - 1), fill=c)
    return im.resize((size, size), Image.LANCZOS)


@lru_cache(maxsize=1)
def _cursor(size=64):
    k = 4
    S = size * k
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    pts = [(.08, .02), (.08, .80), (.28, .62), (.42, .96), (.56, .90), (.42, .56), (.70, .56)]
    P = [(int(x * S), int(y * S)) for x, y in pts]
    d = ImageDraw.Draw(im)
    d.polygon(P, fill=(255, 255, 255, 255), outline=(20, 20, 24, 255))
    d.line(P + [P[0]], fill=(20, 20, 24, 255), width=int(.05 * S), joint='curve')
    return im.resize((size, size), Image.LANCZOS)


def _pill(text, fill, fg, w=270, h=82):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=fill + (255,))
    ti = E.text_img(text, 38 if len(text) < 9 else 33, fill=fg + (255,), weight='ExtraBold')
    im.alpha_composite(ti, ((w - ti.width) // 2, (h - ti.height) // 2))
    return im


def _puffs(out, x, y, t, t0, n=6, spread=120, r0=26, dur=0.6, seed=0):
    """Cụm khói trắng tan dần (đầu vệt khói / khi thu thanh)."""
    if not (t0 <= t < t0 + dur):
        return
    p = (t - t0) / dur
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        ang = (i * 2.4 + seed) % (2 * math.pi)
        dx = math.cos(ang) * spread * (0.3 + p) * (0.6 + 0.4 * ((i * 37) % 5) / 4)
        dy = math.sin(ang) * spread * 0.45 * (0.3 + p)
        r = r0 * (1.2 - 0.9 * p) * (0.7 + 0.3 * (i % 3))
        d.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), fill=(255, 255, 255, int(240 * (1 - p))))
    out.alpha_composite(lay)


def _cursor_pos(t):
    """Đường đi con trỏ: vào từ dưới phải → like → đăng ký → chuông → ra dưới phải."""
    T = SUB_T
    keys = [(T['like'] - 1.4, (1010, 1560)), (T['like'] - 0.12, (SUB_THUMB_X + 18, SUB_CY + 14)),
            (T['like'] + 0.25, (SUB_THUMB_X + 18, SUB_CY + 14)), (T['sub'] - 0.12, (SUB_PILL_X + 30, SUB_CY + 16)),
            (T['sub'] + 0.25, (SUB_PILL_X + 30, SUB_CY + 16)), (T['bell'] - 0.12, (SUB_BELL_X + 12, SUB_CY + 16)),
            (T['bell'] + 0.45, (SUB_BELL_X + 12, SUB_CY + 16)), (T['retract'] - 0.05, (1010, 1560))]
    if t < keys[0][0] or t > keys[-1][0]:
        return None
    for (ta, a), (tb, b) in zip(keys, keys[1:]):
        if ta <= t <= tb:
            p = E.e_io(E.clamp((t - ta) / max(1e-3, tb - ta)))
            return mix(a[0], b[0], p), mix(a[1], b[1], p)
    return None


def subscribe_outro(t, bg, dim=0.18):
    """Cảnh kết ~7,8 s theo clip mẫu của Owner: nền = tranh cảnh cuối (đẩy chậm, tối nhẹ), lower-third avatar kênh +
    thanh LIKE · ĐĂNG KÝ · CHUÔNG, con trỏ bấm lần lượt, thu vào và biến mất. SFX của tập canh theo SUB_T."""
    T = SUB_T
    out = cam(bg.convert('RGBA'), z=1.0 + 0.05 * E.clamp(t / SUB_DUR))
    if dim:
        out = Image.blend(out, Image.new('RGBA', (W, H), (10, 12, 24, 255)), dim)
    cy, ax, R = SUB_CY, SUB_AX, SUB_R
    # --- avatar: bật ra (0 → 1,08 → 1), biến mất: co lại + vòng xoáy trắng
    if t < T['vanish']:
        sa = min(1.0, E.clamp(t / 0.32) * 1.08) if t < 0.32 else 1.0 + 0.08 * math.exp(-(t - 0.32) * 12) * math.cos((t - 0.32) * 30)
    else:
        sa = 1.0 - E.clamp((t - T['vanish']) / 0.42) ** 2          # co nhanh dần (ease-in)
    # --- thanh trắng: kéo dài sang phải (bar → bar+0,45), thu về (retract → retract+0,4)
    if t < T['bar']:
        bw = 0.0
    elif t < T['retract']:
        bw = E.e_out(E.clamp((t - T['bar']) / 0.45))
    else:
        bw = 1.0 - E.e_io(E.clamp((t - T['retract']) / 0.4))
    x_end = ax + (SUB_X1 - ax) * bw
    if x_end > ax + 30:          # thanh đủ dài để vẽ (bài học: bw nhỏ → x1 < x0 làm PIL lỗi)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        dd.rounded_rectangle((ax + 10, cy - 66, x_end + 4, cy + 66), 22, fill=(0, 0, 0, 50))           # bóng mờ
        dd.rounded_rectangle((ax, cy - 62, x_end, cy + 62), 20, fill=(255, 255, 255, 255))
        out.alpha_composite(lay)
        # icon (chỉ khi thanh đã mở hết; bị cắt theo mép phải của thanh khi thu)
        ia = E.clamp((t - T['icons']) / 0.35)
        if ia > 0:
            ic = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            liked, subbed, belled = t >= T['like'], t >= T['sub'], t >= T['bell'] + 0.55
            th = _thumb(_BLUE if liked else _GRAY)
            E.put(ic, th, SUB_THUMB_X, cy, s=(pop(t, T['like'], 0.25) or 1.0) if liked else 1.0, alpha=ia)
            pl = _pill('ĐÃ ĐĂNG KÝ' if subbed else 'ĐĂNG KÝ', _GRAY if subbed else _RED, (95, 95, 100) if subbed else (255, 255, 255))
            reveal = E.clamp((t - T['icons']) / 0.5)                              # chữ hiện dần trái → phải như clip
            if reveal < 1:
                m = Image.new('L', pl.size, 0)
                ImageDraw.Draw(m).rectangle((0, 0, int(pl.width * reveal), pl.height), fill=255)
                pl = pl.copy()
                pl.putalpha(Image.composite(pl.getchannel('A'), Image.new('L', pl.size, 0), m))
            E.put(ic, pl, SUB_PILL_X, cy, s=(pop(t, T['sub'], 0.25) or 1.0) if subbed else 1.0, alpha=ia)
            rot = 0.0
            if T['bell'] <= t < T['bell'] + 0.6:
                rot = 22 * math.sin((t - T['bell']) * 34) * (1 - (t - T['bell']) / 0.6)
            E.put(ic, _bell2(_GRAY if belled else _YEL), SUB_BELL_X, cy, rot=rot, alpha=ia)
            clip = Image.new('L', (W, H), 0)
            ImageDraw.Draw(clip).rectangle((ax + R * 0.6, 0, max(ax + R * 0.6, x_end - 8), H), fill=255)
            ic.putalpha(Image.composite(ic.getchannel('A'), Image.new('L', (W, H), 0), clip))
            out.alpha_composite(ic)
    # --- vệt khói trắng bắn sang phải trước khi thanh mở; cụm khói ở đầu thanh; chấm trắng khi thu
    if T['smoke'] <= t < T['bar'] + 0.25:
        p = E.clamp((t - T['smoke']) / 0.45)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        x0, x1 = ax + R * 0.8, ax + R * 0.8 + 560 * E.e_out(p)
        a = int(255 * (1 - E.clamp((t - T['bar'] - 0.05) / 0.2)))
        dd.polygon([(x0, cy - 10), (x1, cy - 22), (x1 + 30, cy), (x1, cy + 14), (x0, cy + 10)], fill=(255, 255, 255, a))
        out.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))
    _puffs(out, SUB_X1 + 20, cy, t, T['bar'] + 0.25, n=7, spread=110, r0=30, dur=0.65, seed=1)
    _puffs(out, ax + R + 30, cy, t, T['retract'] + 0.3, n=4, spread=70, r0=12, dur=0.45, seed=3)
    if sa > 0.01:
        av = _avatar()
        ring = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        rr = R * sa + 8
        ImageDraw.Draw(ring).ellipse((ax - rr, cy - rr, ax + rr, cy + rr), outline=(150, 40, 50, 230), width=5)
        if t < 0.5:                                                  # vòng viền loang ra khi bật
            r2 = R * (0.6 + 0.9 * E.clamp(t / 0.5))
            ImageDraw.Draw(ring).ellipse((ax - r2, cy - r2, ax + r2, cy + r2), outline=(150, 40, 50, int(200 * (1 - t / 0.5))), width=4)
        out.alpha_composite(ring)
        E.put(out, av, ax, cy, s=sa)
    if T['vanish'] - 0.1 <= t < T['vanish'] + 0.55:                   # vòng xoáy trắng khi biến mất
        p = E.clamp((t - T['vanish'] + 0.1) / 0.65)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        rr = R * (1.25 - 0.6 * p)
        a0 = 360 * p * 1.5
        for k, span in ((0, 110), (180, 70)):
            dd.arc((ax - rr, cy - rr, ax + rr, cy + rr), a0 + k, a0 + k + span, fill=(255, 255, 255, int(255 * (1 - p))), width=12)
        out.alpha_composite(lay)
    # --- con trỏ chuột; lúc bấm: co 0,85 + gợn tròn
    cp = _cursor_pos(t)
    if cp:
        press = any(T[k] <= t < T[k] + 0.12 for k in ('like', 'sub', 'bell'))
        cur = _cursor()
        E.put(out, cur, cp[0] + cur.width * 0.3, cp[1] + cur.height * 0.4, s=0.85 if press else 1.0)
        for k in ('like', 'sub', 'bell'):
            if T[k] <= t < T[k] + 0.3:
                p = (t - T[k]) / 0.3
                lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                r = 14 + 40 * p
                ImageDraw.Draw(lay).ellipse((cp[0] - r, cp[1] - r, cp[0] + r, cp[1] + r), outline=(255, 255, 255, int(220 * (1 - p))), width=5)
                out.alpha_composite(lay)
    return out


def subscribe_sfx(sid, gain=1.0, appear_vanish=None):
    """SFX đi kèm subscribe_outro (theo SUB_T): tách chuột + tiếng phản hồi ở 3 nút (Like · Đăng ký · Chuông).
    Owner 20/11/2026 (EP32): tiếng outro LÚC XUẤT HIỆN (pop, vút khói, phụt) và LÚC BIẾN MẤT (vút thu, vút biến, pop)
    gây khó chịu -> bỏ mặc định; hình xuất hiện/biến mất giữ nguyên. appear_vanish=True chỉ để tái lập tập cũ.
    gain: nhân âm lượng (quy trình v2: OUTRO_SFX_GAIN = 0,5 — outro nhỏ hơn thân video)."""
    T = SUB_T
    if appear_vanish is None:
        appear_vanish = OUTRO_APPEAR_VANISH_SFX
    raw = _subscribe_sfx_raw(sid, T) if appear_vanish else _subscribe_sfx_buttons(sid, T)
    return [(a, b, c, d, round(e * gain, 4)) for a, b, c, d, e in raw]


OUTRO_APPEAR_VANISH_SFX = False   # Owner 20/11/2026: không phát tiếng lúc outro xuất hiện/biến mất
OUTRO_SFX_GAIN = 0.5      # quy trình chuẩn v2 (Owner duyệt 18/11/2026): SFX outro 50 %
OUTRO_MUSIC_GAIN = 0.35   # nhạc nền trong outro 35 % mức thân video, rồi fade-out


def _subscribe_sfx_buttons(sid, T):
    """Chỉ tiếng ở 3 nút: tách chuột + ting like/tim, tách + ding đăng ký, tách + chuông."""
    return [(sid, T['like'], 'click', .1, .30), (sid, T['like'] + 0.02, 'pop', .15, .22), (sid, T['like'] + 0.05, 'heart', .5, .10),
            (sid, T['sub'], 'click', .1, .30), (sid, T['sub'] + 0.02, 'ding', .3, .22),
            (sid, T['bell'], 'click', .1, .30), (sid, T['bell'] + 0.02, 'chime', .8, .20)]


def _subscribe_sfx_raw(sid, T):
    return [(sid, 0.0, 'pop', .15, .20), (sid, T['smoke'], 'whoosh', .5, .22), (sid, T['bar'] + 0.25, 'huff', .4, .14),
            (sid, T['like'], 'click', .1, .30), (sid, T['like'] + 0.02, 'pop', .15, .22), (sid, T['like'] + 0.05, 'heart', .5, .10),
            (sid, T['sub'], 'click', .1, .30), (sid, T['sub'] + 0.02, 'ding', .3, .22),
            (sid, T['bell'], 'click', .1, .30), (sid, T['bell'] + 0.02, 'chime', .8, .20),
            (sid, T['retract'], 'whoosh', .4, .18), (sid, T['vanish'], 'whoosh', .5, .16), (sid, T['vanish'] + 0.35, 'pop', .15, .14)]


# ---------------------------------------------------------------- phụ đề theo từng từ (quy trình chuẩn v2)
# Chuẩn hoá từ EP25 (Owner duyệt): chữ trắng viền đen trên THẺ NỀN ĐEN, từ khoá vàng trên ô đen đậm, từ hiện dần theo
# mốc âm tiết của giọng thật, từ đang đọc nhấp lên 2 px, thẻ nảy nhẹ theo biên độ giọng. Tâm x = 540, dải 1480–1680.
WORD_SUB_Y = 1570
WORD_SUB_SIZE = 50                   # Owner 19/11/2026: kiểu D + font kiểu A (Be Vietnam Pro Bold 50, không viền chữ)
WORD_FONT_WEIGHT = 'Bold'
WORD_STROKE = 0                      # kiểu A không viền chữ; trước 19/11 là 2
WORD_SUB_MAXW = 710
WORD_BG = (12, 12, 16, 218)          # nền đen ~85 %
WORD_KEY = (255, 212, 92, 255)       # vàng thương hiệu #FFD45C
WORD_KEY_SCALE = 1.2                 # Owner 19/11/2026: từ khoá lớn hơn chữ thường 1 cỡ


_VI_DIGITS = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']


def _vi_number(n):
    """Âm tiết đọc số 0–999 (đủ để đếm âm tiết cho ước lượng mốc từ)."""
    if n < 10:
        return [_VI_DIGITS[n]]
    if n < 20:
        return ['mười'] + ([] if n == 10 else [_VI_DIGITS[n % 10]])
    if n < 100:
        return [_VI_DIGITS[n // 10], 'mươi'] + ([] if n % 10 == 0 else [_VI_DIGITS[n % 10]])
    return [_VI_DIGITS[n // 100], 'trăm'] + (_vi_number(n % 100) if n % 100 else [])


def _spoken_syllables(word):
    """Một từ phụ đề -> danh sách âm tiết thực đọc (dd/mm -> 'dd tháng mm'; số -> chữ). Từ thường giữ nguyên."""
    import re
    m = re.fullmatch(r"(\W*)(\d{1,2})/(\d{1,2})(\W*)", word)
    if m:
        return _vi_number(int(m.group(2))) + ['tháng'] + _vi_number(int(m.group(3)))
    m = re.fullmatch(r"(\W*)(\d{1,3})(\W*)", word)
    if m:
        return _vi_number(int(m.group(2)))
    return [word]


def build_word_timing(ep_dir, lines=None, fixes=None):
    """Ước lượng mốc từng từ từ WAV giọng (core.wordtime.estimate, không ASR). Khoá SHA từng file giọng.
    fixes = {'V08': {1: (0.59, 0.75)}} để chỉnh tay sau khi xem sóng âm. Ghi audio/word_timing.json."""
    import hashlib
    import json
    import sys
    import wave
    import numpy as np
    ep = Path(ep_dir).resolve()
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
    from ai_video_factory.core.wordtime import estimate
    lines = lines or json.loads((ep / 'render' / 'lines.json').read_text(encoding='utf-8'))
    rows = {}
    for line in lines:
        src = ep / 'audio' / 'voice' / (line['id'] + '.wav')
        with wave.open(str(src)) as w:
            rate, ch = w.getframerate(), w.getnchannels()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)
        x = x.reshape(-1, ch).mean(axis=1) / 32768
        words = line['text'].split()
        dur = len(x) / rate
        # Bài học EP27: chữ số đọc thành nhiều âm tiết ('20/11' = 'hai mươi tháng mười một') -> ước lượng trên âm tiết nói
        groups = [_spoken_syllables(wd) for wd in words]
        flat = [sy for g in groups for sy in g]
        spans = estimate(x, rate, flat, code='vi')
        cues, k = [], 0
        for wd, g in zip(words, groups):
            a, b = spans[k][0], spans[k + len(g) - 1][1]
            k += len(g)
            cues.append({'word': wd, 'start': a, 'end': min(dur, b)})
        for i, (a, b) in ((fixes or {}).get(line['id']) or {}).items():
            cues[i]['start'], cues[i]['end'] = a, b
        if not all(0 <= c['start'] < c['end'] <= dur + 1e-6 for c in cues):
            raise SystemExit('Mốc từ không hợp lệ ở %s' % line['id'])
        rows[line['id']] = {'text': line['text'], 'voice_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
                            'duration': dur, 'words': cues}
    out = {'method': 'core.wordtime acoustic syllable estimator; no ASR/forced alignment',
           'human_listening_verified': False, 'lines': rows}
    (ep / 'audio' / 'word_timing.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    return out


@lru_cache(maxsize=1)
def _word_rows(path):
    import hashlib
    import json
    rows = json.loads(Path(path).read_text(encoding='utf-8'))['lines']
    for vid, row in rows.items():
        wav = Path(path).parent / 'voice' / (vid + '.wav')
        if hashlib.sha256(wav.read_bytes()).hexdigest() != row['voice_sha256']:
            raise SystemExit('Giọng %s đã đổi: chạy lại build_word_timing' % vid)
    return rows


def _strip(w):
    return w.lower().strip('.,!?…:;"“”()')


WORD_REVEAL = True                   # Owner 20/11/2026 (EP31 'chữ chạy trước tiếng'): chữ hiện đúng lúc giọng đọc tới,
                                     # khung thẻ vẫn theo cả cụm nên không lệch tâm (bài học EP27)
WORD_HOLD = 0.4                      # giữ thẻ sau khi câu dứt để kịp đọc (trước: 0,12 s)
WORD_CHUNK_MAX = 4                   # Owner 19/11/2026 (tối): mỗi lúc chỉ 3–4 chữ, 1 dòng, cụm sau thay cụm trước
_PUNCT_END = ('…', ',', '!', '?', '.', ':', ';')
# chữ thường đứng TRƯỚC danh từ/động từ của nó — cụm không nên kết thúc bằng chúng ("cây | son", "của | anh")
_HEAD_WORDS = frozenset('cây cái con chiếc của là và vì để cho những các một mấy rất đang sẽ đã với từ ở bị được '
                        'phải cũng thì mà nhưng nên khi'.split())


SUB_BREAKS = {}      # ngắt tay theo nghĩa cho từng câu: {'V12': 'Em xoá | vì thanh toán hết | rồi đó anh!'} (tập tự khai báo)


@lru_cache(maxsize=512)
def word_chunks(text, size=WORD_CHUNK_MAX, gaps=None, manual=None):
    """Chia câu thành cụm ≤ size chữ (mỗi cụm 1 dòng). Quy hoạch động: ưu tiên ngắt sau dấu câu, cụm 3–4 chữ, tránh
    cụm 1 chữ (trừ thán từ có dấu câu như 'Ủa?'), không ngắt ngay sau chữ viết hoa giữa câu ('Boss / Mimi').
    gaps[i] = khoảng ngừng của giọng (giây) giữa chữ i và i+1 (từ word_timing): ngắt ở chỗ giọng ngừng, phạt cụm có
    chỗ ngừng dài bên trong — chữ chạy theo nhịp đọc. manual = 'a b | c d e' (SUB_BREAKS) thắng mọi luật nếu khớp câu.
    Trả tuple các tuple chữ, nối lại đúng bằng text.split()."""
    ws = text.split()
    n = len(ws)
    if manual:
        parts = tuple(tuple(p.split()) for p in manual.split('|') if p.split())
        if [w for p in parts for w in p] != ws:
            raise SystemExit('SUB_BREAKS không khớp câu thoại: %r ≠ %r' % (manual, text))
        if any(len(p) > size for p in parts):
            raise SystemExit('SUB_BREAKS có cụm quá %d chữ: %r' % (size, manual))
        return parts
    gaps = gaps or (0.0,) * (n - 1)
    if n <= size and max(gaps, default=0) < 0.25:
        return (tuple(ws),)

    def cost(i, j):                       # cụm ws[i:j]
        k, c = j - i, 0.3
        last = ws[j - 1]
        if j < n:
            if not last.endswith(_PUNCT_END):
                c += 2.0
                if last[:1].isupper() and ws[j][:1].isupper():      # tên riêng 2 chữ: 'Black / Friday'
                    c += 3.0
                if last.lower() in _HEAD_WORDS:
                    c += 1.5
        if k == 1:
            c += 1.0 if last.endswith(_PUNCT_END) else 4.0
        elif k == 2:
            c += 0.6
        c += 1.0 * sum(w.endswith(_PUNCT_END) for w in ws[i:j - 1])   # dấu câu nằm giữa cụm
        if j < n:
            c -= 5.0 * min(gaps[j - 1], 0.4)                            # giọng ngừng ở đây -> ngắt theo nhịp
        c += 5.0 * sum(min(g, 0.4) for g in gaps[i:j - 1] if g >= 0.15)  # cụm vắt qua chỗ ngừng dài
        return c

    best = [0.0] + [float('inf')] * n
    prev = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - size), j):
            v = best[i] + cost(i, j)
            if v < best[j]:
                best[j], prev[j] = v, i
    out, j = [], n
    while j:
        out.append(tuple(ws[prev[j]:j]))
        j = prev[j]
    return tuple(reversed(out))


def voice_gaps(wl):
    """Khoảng ngừng giữa các chữ từ mốc từ. Bộ ước lượng hay lệch 1 chữ ('Mua luôn! Thẻ[0.37] anh' — giọng thật ngừng
    sau 'luôn!'), nên chỗ ngừng ≥ 0,15 s nằm cạnh một dấu câu được dời về đúng dấu câu đó."""
    g = [round(max(0.0, b['start'] - a['end']), 2) for a, b in zip(wl, wl[1:])]
    punct = [w['word'].endswith(_PUNCT_END) for w in wl[:-1]]
    for i, v in enumerate(list(g)):
        if v >= 0.15 and not punct[i]:
            for j in (i - 1, i + 1):
                if 0 <= j < len(g) and punct[j]:
                    g[j], g[i] = max(g[j], v), 0.0
                    break
    return tuple(g)


def chunk_at(text, visible, gaps=None, manual=None):
    """(chỉ số cụm, chỉ số chữ đầu cụm) chứa chữ thứ `visible` (đếm từ 1) — cụm đang đọc."""
    first = 0
    chunks = word_chunks(text, WORD_CHUNK_MAX, gaps, manual)
    for ci, ch in enumerate(chunks):
        if visible <= first + len(ch):
            return ci, first
        first += len(ch)
    return len(chunks) - 1, first - len(chunks[-1])


@lru_cache(maxsize=256)
def word_card(text, keys=(), visible=None, active=-1, gaps=None, manual=None):
    """Thẻ phụ đề: nền đen bo góc, chữ trắng, từ khoá vàng to hơn WORD_KEY_SCALE (Owner 19/11: lớn hơn 1 cỡ) trên ô
    đen đậm. Owner 19/11/2026 (tối): CHỈ 1 DÒNG, mỗi lúc một cụm 3–4 chữ (`word_chunks`); cụm hiện cả khi giọng tới
    chữ đầu cụm, rồi được cụm sau thay thế. visible=None → cụm đầu. Chữ đang đọc (active, chỉ số trong cả câu) nhấp 2 px."""
    ci, first = chunk_at(text, visible or 1, gaps, manual)
    line = list(word_chunks(text, WORD_CHUNK_MAX, gaps, manual)[ci])
    size = WORD_SUB_SIZE
    while True:
        f = E.font(size, WORD_FONT_WEIGHT)
        fk = E.font(int(size * WORD_KEY_SCALE), WORD_FONT_WEIGHT)
        width = sum((fk if _strip(w) in keys else f).getlength(w) for w in line) + f.getlength(' ') * (len(line) - 1)
        if width <= WORD_SUB_MAXW or size <= 36:
            break
        size -= 1
    ks = int(size * WORD_KEY_SCALE)
    lh, padx, pady = ks + 14, 28, 12
    card = Image.new('RGBA', (int(width) + 2 * padx, lh + 2 * pady), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=WORD_BG)
    x = padx
    for i, wd in enumerate(line, start=first):
        hot = _strip(wd) in keys
        ff = fk if hot else f
        w = ff.getlength(wd)
        yy = pady + (0 if hot else (ks - size) * 0.8)            # chân chữ thẳng hàng
        if WORD_REVEAL and visible is not None and i >= visible:
            x += w + f.getlength(' ')                            # Owner 20/11 (EP31): chưa đọc tới -> giữ chỗ, chưa hiện
            continue
        if hot:
            d.rounded_rectangle((x - 6, yy + 2, x + w + 6, yy + ks + 12), 8, fill=(0, 0, 0, 255))
        d.text((x, yy - 2 if i == active else yy), wd, font=ff, fill=WORD_KEY if hot else (255, 255, 255, 255),
               stroke_width=WORD_STROKE, stroke_fill=(10, 10, 14, 255))
        x += w + f.getlength(' ')
    return card


def sub_chunk_report(ep_dir):
    """In cách chia cụm phụ đề của mọi câu (dùng mốc từ + SUB_BREAKS) để soát nghĩa/nhịp trước khi render."""
    import json
    ep = Path(ep_dir).resolve()
    rows = json.loads((ep / 'audio' / 'word_timing.json').read_text(encoding='utf-8'))['lines']
    out = {}
    for vid, row in rows.items():
        gaps = voice_gaps(row['words'])
        out[vid] = ' | '.join(' '.join(c) for c in word_chunks(row['text'], WORD_CHUNK_MAX, gaps, SUB_BREAKS.get(vid)))
    return out


def word_sub(out, sid, t, keywords=None, timing=None):
    """Vẽ phụ đề theo từng từ cho cảnh sid tại thời điểm cục bộ t (dùng với K.install_post(subtitles=False)).
    keywords = {'V3': {'quà'}}; timing = đường dẫn audio/word_timing.json (mặc định của tập). Ghi E.SUB_BOX cho --check-subs."""
    timing = timing or os.path.join(E.OUT, 'audio', 'word_timing.json')
    rows = _word_rows(timing) if os.path.exists(timing) else {}
    for vid, scene, start, who, text in E.VOICE:
        if scene != sid:
            continue
        if not (start + E.voice_onset(vid) <= t <= start + E.VDUR.get(vid, 0) + WORD_HOLD):
            continue
        keys = tuple(sorted((keywords or {}).get(vid, ())))
        if vid in rows:
            wl = rows[vid]['words']
            rel = t - start
            vis = sum(w['start'] <= rel for w in wl)
            act = next((i for i, w in enumerate(wl) if w['start'] <= rel < w['end']), -1)
            if not vis:
                continue
            gaps = voice_gaps(wl)
            card = word_card(text, keys, vis, act, gaps, SUB_BREAKS.get(vid))
        else:                                    # chưa có mốc từ: rải đều theo thời lượng giọng
            n = len(text.split())
            span = max(1e-3, E.VDUR.get(vid, 0) - E.voice_onset(vid))
            vis = min(n, 1 + int(n * (t - start - E.voice_onset(vid)) / span))
            card = word_card(text, keys, vis, -1, None, SUB_BREAKS.get(vid))
        sc = 1 + 0.035 * min(1.0, E.amp(E.STARTS[sid] + t, who) * 2)
        E.SUB_BOX = (540 - card.width * sc / 2, WORD_SUB_Y - card.height * sc / 2,
                     540 + card.width * sc / 2, WORD_SUB_Y + card.height * sc / 2)
        if E.DRAW_SUB:
            E.put(out, card, 540, WORD_SUB_Y, s=sc)
    return out


# ---------------------------------------------------------------- thumbnail (quy trình chuẩn v2)
THUMB_KEY = (255, 230, 0, 255)       # vàng tươi cho từ khoá thumbnail (Owner 18/11/2026)


def make_thumbnail(art_path, line1, line2, out_dir, focus=(0.5, 0.55), zoom=1.0, block_y=180, keys=(), key_scale=1.3):
    """Thumbnail 1080×1920 từ tranh thật của tập: khối đen bo góc đặt ở vùng KHÔNG có mặt (block_y), 2 dòng chữ
    ExtraBold viền đen 7 px. Owner 18/11/2026: từ cần nổi bật (keys, so khớp không phân biệt hoa thường) màu vàng tươi
    và to hơn chữ khác key_scale lần; chữ còn lại màu trắng. Không truyền keys: dòng 1 trắng, dòng 2 vàng (bản cũ).
    Ghi thumbnail.png + cover.jpg vào out_dir; trả đường dẫn thumbnail."""
    im = Image.open(art_path).convert('RGBA')
    if zoom > 1.0:
        w, h = im.width / zoom, im.height / zoom
        cx, cy = focus[0] * im.width, focus[1] * im.height
        x0 = min(max(0, cx - w / 2), im.width - w)
        y0 = min(max(0, cy - h / 2), im.height - h)
        im = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h)))
    cover = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS, centering=focus)
    d = ImageDraw.Draw(cover)
    keyset = {k.upper() for k in keys}

    def words(line, row):
        out = []
        for wd in line.split():
            hot = wd.upper().strip('.,!?…') in keyset if keyset else row == 1
            out.append((wd, hot))
        return out

    rows = [words(line1, 0), words(line2, 1)]
    base = 108
    while True:
        widths = []
        for r in rows:
            f = [E.font(int(base * (key_scale if hot and keyset else 1.0)), 'ExtraBold') for _, hot in r]
            widths.append(sum(ff.getlength(wd) for ff, (wd, _) in zip(f, r)) + E.font(base, 'ExtraBold').getlength(' ') * (len(r) - 1))
        if max(widths) <= 800 or base <= 60:
            break
        base -= 2
    heights = [int(base * (key_scale if any(h for _, h in r) and keyset else 1.0)) for r in rows]
    hgt = sum(heights) + 36 * len(rows) + 54
    d.rounded_rectangle((110, block_y, 970, block_y + hgt), 38, fill=(22, 20, 28, 240))
    y = block_y + 30
    for r, rh, rw in zip(rows, heights, widths):
        x = 540 - rw / 2
        for wd, hot in r:
            sz = int(base * (key_scale if hot and keyset else 1.0))
            col = THUMB_KEY if (hot and keyset) else (WORD_KEY if hot else (255, 255, 255, 255))
            t_img = E.text_img(wd, sz, fill=col, weight='ExtraBold', stroke=7, sfill=(10, 10, 14, 255))
            fnt = E.font(sz, 'ExtraBold')
            wlen = fnt.getlength(wd)
            base_in_img = fnt.getmetrics()[0] - fnt.getbbox(wd, stroke_width=7)[1] + 3   # đường chân chữ trong ảnh chữ
            top = y + rh - base_in_img + 4                                                # mọi từ chung một đường chân chữ
            E.put(cover, t_img, x + wlen / 2, top + t_img.height / 2)
            x += wlen + E.font(base, 'ExtraBold').getlength(' ')
        y += rh + 36
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, 'thumbnail.png')
    cover.convert('RGB').save(p)
    cover.convert('RGB').save(os.path.join(out_dir, 'cover.jpg'), quality=95)
    return p


# ---------------------------------------------------------------- thumbnail v2 (prompts/thumbnail_designer_v1.md, Owner 18/11/2026)
THUMB_SAFE = (108, 288, 972, 1632)        # vùng an toàn nội bộ: giữa 80 % rộng × 70 % cao (1080×1920)
THUMB_LIME = (214, 255, 28, 255)          # vàng chanh cho từ khoá
THUMB_INK = (28, 16, 56, 255)             # tím than cho viền + bóng cứng


def _to_916(im, extend='top'):
    """Ảnh không phải 9:16 (vd. 2:3 của image gen): giữ nguyên bề ngang, kéo dài phần nền đơn giản (mặc định phía trên)
    bằng phản chiếu + làm mờ — không cắt hai bên, không kéo giãn nhân vật."""
    import numpy as np
    from PIL import ImageFilter
    if abs(im.width / im.height - W / H) < 0.01:
        return ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS)
    hh = round(W * im.height / im.width)
    if hh >= H:
        return ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS, centering=(0.5, 1.0 if extend == 'top' else 0.0))
    a = np.asarray(im.convert('RGB').resize((W, hh), Image.Resampling.LANCZOS))
    pad = H - hh
    if extend == 'top':
        a = np.pad(a, ((pad, 0), (0, 0), (0, 0)), mode='symmetric')
        out = Image.fromarray(a)
        out.paste(out.crop((0, 0, W, pad + 30)).filter(ImageFilter.GaussianBlur(12)), (0, 0))
    else:
        a = np.pad(a, ((0, pad), (0, 0), (0, 0)), mode='symmetric')
        out = Image.fromarray(a)
        out.paste(out.crop((0, hh - 30, W, H)).filter(ImageFilter.GaussianBlur(12)), (0, hh - 30))
    return out.convert('RGBA')


THUMB_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'Oswald-VF.ttf')   # OFL, Owner cho tải 18/11/2026


@lru_cache(maxsize=64)
def _thumb_font(size):
    """Display sans siêu đậm, hơi hẹp, đủ dấu tiếng Việt: Oswald Bold (variable). Thiếu file -> Be Vietnam Pro ExtraBold."""
    from PIL import ImageFont
    if os.path.exists(THUMB_FONT):
        f = ImageFont.truetype(THUMB_FONT, size)
        f.set_variation_by_name('Bold')
        return f
    return E.font(size, 'ExtraBold')


def _thumb_word(word, size, fill, outline=THUMB_INK, stroke=10, shadow=(10, 12)):
    """Một từ: bóng cứng lệch (không làm mờ) + viền tối dày, lòng chữ không bị bít (stroke tính từ ngoài nét)."""
    f = _thumb_font(size)
    bb = f.getbbox(word, stroke_width=stroke)
    w, h = bb[2] - bb[0] + shadow[0] + 8, bb[3] - bb[1] + shadow[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ox, oy = 4 - bb[0], 4 - bb[1]
    d.text((ox + shadow[0], oy + shadow[1]), word, font=f, fill=outline, stroke_width=stroke, stroke_fill=outline)
    d.text((ox, oy), word, font=f, fill=fill, stroke_width=stroke, stroke_fill=outline)
    base = oy + f.getmetrics()[0]          # đường chân chữ trong ảnh
    return im, base, f.getlength(word) + 2 * stroke


def make_thumbnail_v2(art_path, lines, keyword, out_dir, key_scale=1.3, tilt=-3.0, extend='top', text_top=None,
                      text_height_frac=0.33, accent=THUMB_LIME, qa_dir=None, skew=0.0, zoom=1.0, zoom_center=(540, 960),
                      stroke=10, ribbon=None):
    """ribbon=(r,g,b,a): băng màu xiên viền tối sau dòng chứa từ khoá (phong cách mẫu references/thumbnail, Owner 19/11).
    Thumbnail theo prompts/thumbnail_designer_v1.md: tranh image gen không chữ + khối chữ display sans siêu đậm.
    lines: 2–3 dòng; keyword: cụm từ nhấn (màu accent, to hơn key_scale lần, tối đa 2 cấp cỡ chữ); chữ khác trắng;
    viền tím than + bóng cứng lệch; nghiêng nhẹ `tilt` độ. Khối chữ ở phần trên vùng an toàn, cao ~33 % vùng an toàn.
    Ghi thumbnail.png, cover.jpg; QA: _qa/thumb_small.png (1/6) và _qa/thumb_safe.png (che ngoài vùng an toàn).
    Trả dict {path, text_box, inside_safe}. Chặn (SystemExit) khi khối chữ ra ngoài vùng an toàn."""
    sx0, sy0, sx1, sy1 = THUMB_SAFE
    cover = _to_916(Image.open(art_path).convert('RGBA'), extend=extend)
    if zoom > 1.0:                               # phóng lớn biểu cảm (Owner 18/11) — kiểm lại bằng thumb_safe.png
        cover = E.cam(cover, z=zoom, cx=zoom_center[0], cy=zoom_center[1])
    kw = keyword.upper().split()
    rows = []
    for line in lines:
        ws = line.upper().split()
        hot = [False] * len(ws)
        for i in range(len(ws)):
            if ws[i:i + len(kw)] == kw:
                for j in range(i, i + len(kw)):
                    hot[j] = True
        rows.append(list(zip(ws, hot)))
    maxw = (sx1 - sx0) - 80                    # chừa khoảng thở hai bên
    maxh = (sy1 - sy0) * text_height_frac
    base = 150
    while base > 50:
        built = []
        for r in rows:
            parts = [(_thumb_word(w, int(base * (key_scale if h else 1.0)), accent if h else (255, 255, 255, 255), stroke=stroke), w)
                     for w, h in r]
            gap = _thumb_font(base).getlength(' ') * 0.8
            built.append((parts, sum(p[0][2] for p in parts) + gap * (len(parts) - 1), gap,
                           max(int(base * (key_scale if h else 1.0)) for _, h in r)))
        tot_h = sum(b[3] for b in built) * 1.08 + 20 * (len(built) - 1)
        if max(b[1] for b in built) <= maxw and tot_h <= maxh:
            break
        base -= 4
    blk_w = int(max(b[1] for b in built)) + 40
    blk_h = int(tot_h) + 60
    blk = Image.new('RGBA', (blk_w, blk_h), (0, 0, 0, 0))
    y = 10
    if ribbon:                                  # chừa chỗ cho băng nhô ra hai bên
        pad = 60
        big = Image.new('RGBA', (blk_w + 2 * pad, blk_h + 40), (0, 0, 0, 0))
        blk, blk_w = big, blk_w + 2 * pad
    hot_rows = [any(h for _, h in r) for r in rows]
    for ri, (parts, lw, gap, lh) in enumerate(built):
        x = (blk_w - lw) / 2
        if ribbon and hot_rows[ri]:
            d = ImageDraw.Draw(blk)
            x0r, x1r, y0r, y1r = x - 46, x + lw + 46, y + lh * 0.02, y + lh * 1.1
            k = (y1r - y0r) * 0.18
            poly = [(x0r + k, y0r), (x1r + k * 0.4, y0r - 6), (x1r - k, y1r), (x0r - k * 0.4, y1r + 6)]
            d.polygon([(px + 10, py + 12) for px, py in poly], fill=THUMB_INK)        # bóng cứng
            d.polygon(poly, fill=ribbon, outline=THUMB_INK, width=8)
        baseline = y + lh * 0.95
        for (img, bl, adv), _w in parts:
            blk.alpha_composite(img, (int(x), int(baseline - bl)))
            x += adv + gap
        y += lh * 1.08 + 20
    if skew:                                    # chữ nghiêng (italic giả bằng shear; Owner 18/11 yêu cầu "chữ nghiêng")
        sh = int(abs(skew) * blk.height)
        wide = Image.new('RGBA', (blk.width + sh, blk.height), (0, 0, 0, 0))
        wide.alpha_composite(blk, (sh if skew > 0 else 0, 0))
        blk = wide.transform(wide.size, Image.AFFINE, (1, skew, -skew * blk.height if skew > 0 else 0, 0, 1, 0),
                             resample=Image.Resampling.BICUBIC)
    if tilt:
        blk = blk.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=True)
    bb = blk.getbbox()
    blk = blk.crop(bb)
    top = text_top if text_top is not None else sy0 + 40
    left = int(540 - blk.width / 2)
    cover.alpha_composite(blk, (left, int(top)))
    box = (left, int(top), left + blk.width, int(top) + blk.height)
    inside = box[0] >= sx0 and box[1] >= sy0 and box[2] <= sx1 and box[3] <= sy1
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, 'thumbnail.png')
    cover.convert('RGB').save(p)
    cover.convert('RGB').save(os.path.join(out_dir, 'cover.jpg'), quality=95)
    qa = qa_dir or os.path.join(out_dir, '_qa')
    os.makedirs(qa, exist_ok=True)
    cover.convert('RGB').resize((W // 6, H // 6), Image.Resampling.LANCZOS).save(os.path.join(qa, 'thumb_small.png'))
    safe = cover.convert('RGB').copy()
    dark = Image.new('RGB', (W, H), (0, 0, 0))
    m = Image.new('L', (W, H), 175)
    ImageDraw.Draw(m).rectangle(THUMB_SAFE, fill=0)
    safe = Image.composite(dark, safe, m)
    ImageDraw.Draw(safe).rectangle(THUMB_SAFE, outline=(0, 255, 120), width=5)
    ImageDraw.Draw(safe).rectangle(box, outline=(255, 200, 0), width=4)
    safe.save(os.path.join(qa, 'thumb_safe.png'))
    if not inside:
        raise SystemExit('CHẶN thumbnail: khối chữ %s ra ngoài vùng an toàn %s' % (box, THUMB_SAFE))
    return {'path': p, 'text_box': box, 'inside_safe': inside, 'base_size': base}
