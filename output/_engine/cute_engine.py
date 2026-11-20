"""Cute engine (dùng chung cho các tập Tí–Ngang–Mimi). Tách từ pilot 02 "Chỗ ấm nhất nhà".
Mỗi tập: import cute_engine as E; E.configure(out_dir, scenes, voice, funcs); E.main(stills_picks, thumb)
Tính năng: 60 fps, chuyển cảnh trong file (cut/fade/whip/flash/black_in/iris), hòa tan khi đổi sprite,
easing bậc 5 + spring, squash/stretch, vệt mờ chuyển động, camera trượt, bóng mềm, trang trí pastel."""
import os, sys, json, math, wave, subprocess, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(ENGINE, "..", ".."))
LIB = os.path.join(ROOT, "character_library")
FONTS = os.path.join(ENGINE, "fonts")
W, H, FPS = 1080, 1920, 60
OUT = HERE = SEG = VDIR = None
SCENES, VOICE, FUNCS, STARTS, SDUR = [], [], {}, {}, {}
TOTAL = 0.0
VOICE_NAME = {"ti": "Hải Đăng", "ngang": "Trúc Ly"}


PLATFORM = None   # đặt bởi --export <nền tảng>
# QA phụ đề (Owner 08/11/2026: phụ đề đặt ở dưới, KHÔNG đè lên nhân vật). Xem check_subs().
HIDE_SPRITES = False   # True: place() bỏ qua sprite (dựng khung "không nhân vật" để tách mặt nạ nhân vật)
DRAW_SUB = True        # False: subtitle() chỉ ghi vị trí, không vẽ
SUB_BOX = None         # hộp phụ đề của khung vừa dựng (x0, y0, x1, y1)
SUB_GAP = 115          # (cũ, giữ cho tương thích) nửa chiều cao phụ đề 2 dòng + lề
# Bố cục khung (Owner 08/11/2026): nội dung chiếm phần TRÊN (mặc định 3/4), phụ đề chỉ nằm trong dải DƯỚI.
# Tập có thể đổi CONTENT_FRAC tùy nội dung, nhưng dải phụ đề không bao giờ vượt SUB_BAND_MAX (1/3) chiều cao khung.
CONTENT_FRAC = 0.75
SUB_BAND_MAX = 1.0 / 3
SUB_TOP_PAD = 22       # khoảng cách từ mép trên dải tới mép trên viên phụ đề
# Khung an toàn NMT-SAFE-916 v1 (Owner 08/11/2026, xem safe_frame.py / NMT_ENGINE.md mục 3.2): cảnh vẫn vẽ theo bố cục cũ
# (nội dung 0…tray_top(), phụ đề trong dải dưới); mỗi khung được hậu kỳ: nội dung thành khung tranh x 108–972, y 200–1460, nền trơn,
# phụ đề dời xuống dải 1480–1680, viền LUÔN canh giữa màn hình (x 540), rộng ≤ 800 — giống nhau ở bản gốc và cả 3 nền tảng. Tắt: SAFE916 = False.
SAFE916 = True
_SUB_PENDING = None


def configure(out_dir, scenes, voice, funcs):
    global OUT, HERE, SEG, VDIR, SCENES, VOICE, FUNCS, TOTAL
    OUT = out_dir
    HERE = os.path.join(out_dir, "render")
    SEG = os.path.join(HERE, "segments")
    VDIR = os.path.join(out_dir, "audio", "voice")
    SCENES[:] = scenes
    VOICE[:] = voice
    FUNCS.clear(); FUNCS.update(funcs)
    STARTS.clear(); SDUR.clear()
    t = 0.0
    for s in scenes:
        STARTS[s[0]] = round(t, 3); SDUR[s[0]] = s[1]; t += s[1]
    TOTAL = round(t, 3)
# ---------------- màu pastel Style C ----------------
CH = (52, 44, 44)
CREAM = (255, 246, 236)
PINK = (253, 222, 222)
PINK2 = (247, 178, 178)
PEACH = (255, 228, 205)
MINT = (205, 236, 222)
LAV = (226, 214, 245)
SKYB = (204, 228, 246)
BUTTER = (255, 226, 140)
SOFA = (244, 170, 160)
SOFA_D = (222, 140, 132)
WOOD = (240, 214, 182)
WOOD_D = (222, 190, 152)
TI_BLUE = (52, 57, 73)
NG_RED = (166, 94, 72)
WHITE = (255, 255, 255)

# ---------------- asset ----------------
INDEX = {a["asset_id"]: a for a in json.load(open(os.path.join(LIB, "asset_index.json"), encoding="utf-8"))}
USED = {}
_raw, _cache = {}, {}


def raw(aid):
    if aid not in _raw:
        a = INDEX[aid]
        if a.get("approval_status") != "approved":
            raise SystemExit("not approved: " + aid)
        im = Image.open(os.path.join(LIB, a["image_path"])).convert("RGBA")
        _raw[aid] = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    return _raw[aid]


def spr(aid, h=None, scale=None, flip=False, sx=1.0, sy=1.0):
    r = raw(aid)
    # pad_top_px: lề trang trí phía trên (vd. sợi tóc rối bung ra) không tính vào chiều cao thân nhân vật
    pt = INDEX.get(aid, {}).get("pad_top_px", 0)
    k = scale if scale is not None else h / max(1, r.height - pt)
    w2, h2 = max(1, int(r.width * k * sx)), max(1, int(r.height * k * sy))
    key = (aid, w2, h2, flip)
    if key not in _cache:
        im = r.resize((w2, h2), Image.LANCZOS)
        if k > 1.2:
            im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=2))
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if len(_cache) > 600:
            _cache.clear()
        _cache[key] = im
    return _cache[key]


def paste(dst, im, x, y):
    x, y = int(round(x)), int(round(y))
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(dst.width, x + im.width), min(dst.height, y + im.height)
    if x1 > x0 and y1 > y0:
        dst.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


def with_alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * max(0.0, a))))
    return im


def place(dst, aid, x, y, h=None, scale=None, rot=0.0, alpha=1.0, flip=False, sx=1.0, sy=1.0, scene=None, shadow=True):
    """Neo giữa-đáy. squash/stretch bằng sx, sy (giữ chân chạm đất)."""
    if scene:
        USED.setdefault(aid, set()).add(scene)
    if HIDE_SPRITES:
        return
    im = spr(aid, h=h, scale=scale, flip=flip, sx=sx, sy=sy)
    if shadow and alpha > 0.05:
        soft_shadow(dst, x, y, im.width * 0.62, alpha)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    paste(dst, with_alpha(im, alpha), x - im.width / 2, y - im.height)


def place_x(dst, t, ts, a, b, d=0.14, ha=None, hb=None, **kw):
    """Đổi sprite mượt: hòa tan a->b trong d giây + nảy nhẹ khi b xuất hiện."""
    h = kw.pop("h", None)
    ha, hb = ha or h, hb or h
    if t < ts:
        place(dst, a, h=ha, **kw)
        return
    p = clamp((t - ts) / d)
    pop = 1.0 + 0.06 * math.sin(math.pi * clamp((t - ts) / 0.28))
    sy = kw.pop("sy", 1.0)
    sx = kw.pop("sx", 1.0)
    al = kw.pop("alpha", 1.0)
    sh = kw.pop("shadow", True)
    if p < 1:
        place(dst, a, h=ha, alpha=al * (1 - p), sx=sx, sy=sy, shadow=sh, **kw)
    place(dst, b, h=hb, alpha=al * p, sx=sx * (2 - pop), sy=sy * pop, shadow=sh and p >= 1, **kw)


_sh = {}


def soft_shadow(dst, x, y, w, alpha=1.0):
    w = int(max(20, w)) // 8 * 8
    if w not in _sh:
        im = Image.new("RGBA", (w + 60, 70), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((30, 20, w + 30, 50), fill=(120, 80, 80, 70))
        _sh[w] = im.filter(ImageFilter.GaussianBlur(10))
    s = _sh[w]
    paste(dst, with_alpha(s, alpha), x - s.width / 2, y - 38)


# ---------------- easing ----------------
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def prog(t, t0, d):
    return clamp((t - t0) / d) if d > 0 else float(t >= t0)


def e_out(p):
    return 1 - (1 - p) ** 3


def e_io(p):
    return p * p * (3 - 2 * p)


def e_io5(p):
    return p ** 3 * (p * (6 * p - 15) + 10)


def e_back(p, s=1.7):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def spring(t, t0, k=14.0, damp=5.5):
    """0->1 có vượt nhẹ rồi lắng, mượt hơn back-ease."""
    if t < t0:
        return 0.0
    x = t - t0
    return 1 - math.exp(-damp * x) * math.cos(k * x)


def breathe(t, ph=0.0, amp=0.014, per=2.2):
    return 1.0 + amp * math.sin(2 * math.pi * (t / per + ph))


def sway(t, ph=0.0, amp=1.2, per=3.0):
    return amp * math.sin(2 * math.pi * (t / per + ph))


def hop(t, per=0.36, amp=26):
    """Nhảy bước chân: y lệch + squash khi chạm đất."""
    ph = (t / per) % 1.0
    y = -amp * math.sin(math.pi * ph)
    land = max(0.0, 1 - ph / 0.18) if ph < 0.18 else 0.0
    return y, 1 - 0.08 * land, 1 + 0.08 * land


# ---------------- chữ ----------------
_fonts, _txt = {}, {}


def font(size, weight="ExtraBold"):
    k = (size, weight)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(os.path.join(FONTS, "BeVietnamPro-%s.ttf" % weight), size)
    return _fonts[k]


def text_img(text, size, fill=CH, weight="ExtraBold", stroke=0, sfill=WHITE):
    k = (text, size, fill, weight, stroke, sfill)
    if k not in _txt:
        f = font(size, weight)
        bb = f.getbbox(text, stroke_width=stroke)
        im = Image.new("RGBA", (bb[2] - bb[0] + 6, bb[3] - bb[1] + 6), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((3 - bb[0], 3 - bb[1]), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
        _txt[k] = im
    return _txt[k]


def pill(text, size=44, bg=WHITE, fg=CH, outline=PINK2, padx=34, pady=18, weight="ExtraBold"):
    k = ("pill", text, size, bg, fg, outline, weight)
    if k not in _txt:
        ti = text_img(text, size, fg, weight)
        w, h = ti.width + 2 * padx, ti.height + 2 * pady
        im = Image.new("RGBA", (w + 12, h + 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((6, 12, w + 6, h + 12), radius=h // 2, fill=tuple(max(0, c - 40) for c in outline))
        d.rounded_rectangle((6, 4, w + 6, h + 4), radius=h // 2, fill=bg, outline=outline, width=5)
        im.alpha_composite(ti, (6 + padx, 4 + pady))
        _txt[k] = im
    return _txt[k]


def put(dst, im, cx, cy, s=1.0, rot=0.0, alpha=1.0):
    if s <= 0.02 or alpha <= 0.01:
        return
    if abs(s - 1) > 0.004:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    paste(dst, with_alpha(im, alpha), cx - im.width / 2, cy - im.height / 2)


def pop_in(t, t0):
    return clamp(spring(t, t0, 16, 7), 0, 1.25)

_env, VDUR, VONSET = {}, {}, {}
ONSET_THR = 0.02   # biên độ (đã chuẩn hoá theo đỉnh) coi là bắt đầu có tiếng thật (~ -34 dB so với đỉnh)


def load_voice():
    for vid, *_ in VOICE:
        with wave.open(os.path.join(VDIR, vid + ".wav")) as w:
            sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
            a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
        if ch > 1:
            a = a.reshape(-1, ch).mean(1)
        a /= np.abs(a).max() + 1e-9
        hop_ = sr // FPS
        _env[vid] = np.array([np.sqrt(np.mean(a[i * hop_:(i + 1) * hop_] ** 2)) for i in range(len(a) // hop_)] + [0.0])
        VDUR[vid] = len(a) / sr
        nz_ = np.flatnonzero(np.abs(a) > ONSET_THR)
        VONSET[vid] = float(nz_[0]) / sr if len(nz_) else 0.0


def voice_onset(vid):
    """Giây im lặng ở đầu file giọng vid (tiếng thật bắt đầu sau đầu file bao lâu). Bài học EP19."""
    if vid not in VONSET and VDIR and os.path.exists(os.path.join(VDIR, vid + ".wav")):
        with wave.open(os.path.join(VDIR, vid + ".wav")) as w:
            sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
            a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32)
        if ch > 1:
            a = a.reshape(-1, ch).mean(1)
        a /= np.abs(a).max() + 1e-9
        nz_ = np.flatnonzero(np.abs(a) > ONSET_THR)
        VONSET[vid] = float(nz_[0]) / sr if len(nz_) else 0.0
    return VONSET.get(vid, 0.0)


def amp(tg, who):
    for vid, sid, lt, spk, _ in VOICE:
        if spk == who:
            t0 = STARTS[sid] + lt
            if t0 <= tg < t0 + VDUR[vid]:
                e = _env[vid]
                # làm mượt 3 khung
                i = int((tg - t0) * FPS)
                return float(np.mean(e[max(0, i - 1):i + 2]))
    return 0.0


def cues():
    out = []
    for vid, sid, lt, spk, text in VOICE:
        a = STARTS[sid] + lt
        out.append([a, a + VDUR[vid] + 0.45, text])
    for i in range(len(out) - 1):
        out[i][1] = min(out[i][1], out[i + 1][0] - 0.05)
    return out


CUES = []


def _wrap(text, size, maxw):
    f = font(size, "Bold")
    if f.getlength(text) <= maxw:
        return [text]
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        w = max(f.getlength(a), f.getlength(b))
        if best is None or w < best[0]:
            best = (w, [a, b])
    return best[1] if best else [text]


def sub_pill(text, size=50, maxw=900):
    """Phụ đề: tự xuống 2 dòng khi quá rộng, thu nhỏ chữ nếu vẫn tràn."""
    k = ("sub", text, maxw)
    if k in _txt:
        return _txt[k]
    lines = _wrap(text, size, maxw)
    while max(font(size, "Bold").getlength(l) for l in lines) > maxw and size > 34:
        size -= 2
        lines = _wrap(text, size, maxw)
    imgs = [text_img(l, size, CH, "Bold") for l in lines]
    gap = 8
    w = max(i.width for i in imgs) + 80
    h = sum(i.height for i in imgs) + gap * (len(imgs) - 1) + 44
    im = Image.new("RGBA", (w + 12, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = min(h // 2, 44)
    d.rounded_rectangle((6, 12, w + 6, h + 12), radius=r, fill=tuple(max(0, c - 40) for c in PINK2))
    d.rounded_rectangle((6, 4, w + 6, h + 4), radius=r, fill=WHITE, outline=PINK2, width=5)
    y = 4 + 22
    for i in imgs:
        im.alpha_composite(i, (6 + (w - i.width) // 2, y))
        y += i.height + gap
    _txt[k] = im
    return im


def band_frac():
    """Tỉ lệ chiều cao dành cho phụ đề. Chặn khi vượt SUB_BAND_MAX."""
    f = 1.0 - CONTENT_FRAC
    if f > SUB_BAND_MAX + 1e-9 or f <= 0:
        raise SystemExit("CHẶN: dải phụ đề %.0f%% khung, quy tắc Owner tối đa %.0f%% (CONTENT_FRAC=%.3f)"
                         % (100 * f, 100 * SUB_BAND_MAX, CONTENT_FRAC))
    return f


def tray_top(default=None):
    """Mép trên dải phụ đề = mép dưới vùng nội dung (H × CONTENT_FRAC). Nhân vật, khung, đạo cụ nằm phía trên."""
    band_frac()
    return int(round(H * CONTENT_FRAC))


def sub_y_bottom(default=None):
    """Tâm gần đúng của phụ đề 2 dòng trong dải (dùng khi cảnh cần biết vị trí; subtitle() tự canh lại)."""
    return tray_top() + SUB_TOP_PAD + 100


def sub_tray(dst, default=None, col=CREAM):
    """Dải nền phụ đề ở đáy khung: che mọi thứ của cảnh lấn xuống dưới vùng nội dung."""
    y0 = tray_top()
    d = ImageDraw.Draw(dst)
    d.rounded_rectangle((-30, y0, W + 30, H + 80), radius=56, fill=col + (255,), outline=PINK2, width=6)
    return y0


_WM_CACHE = {}


def _wm_for_layout():
    """Hộp watermark NMT dùng để né (bản gốc dùng hình học khung dọc mặc định, giống các nền tảng)."""
    k = PLATFORM or "tiktok"
    if k not in _WM_CACHE:
        try:
            _WM_CACHE[k] = wm_box(k)
        except Exception:   # thiếu file logo: kiểm tra chèn watermark sẽ chặn riêng
            _WM_CACHE[k] = None
    return _WM_CACHE[k]


def _call(sid, tau):
    """Dựng một khung của cảnh; khi SAFE916 bật thì hậu kỳ theo khung an toàn (mọi đường dựng đều qua frame())."""
    global _SUB_PENDING
    _SUB_PENDING = None
    im = FUNCS[sid](tau)
    return safe_post(im) if SAFE916 else im


def safe_post(im):
    """Hậu kỳ NMT-SAFE-916: thu nội dung thành khung tranh bo góc trong vùng an toàn (nền trơn, không làm mờ), vẽ dải và phụ đề ở vị trí mới."""
    global SUB_BOX, _SUB_PENDING
    import safe_frame as SF
    if im.size != (W, H):
        return im
    content = im.crop((0, 0, W, tray_top()))
    out = SF.reframe(content, band_col=CREAM)
    pend, _SUB_PENDING = _SUB_PENDING, None
    if pend:
        pim, s, alpha, pin, text = pend
        x = SF.SUB_X_CENTER          # luôn giữa màn hình; không dời ngang để né watermark
        y = SF.SUB_TOP + pim.height / 2
        wm = _wm_for_layout()
        if wm and y + pim.height / 2 + 26 > wm[1] - WM_PAD and x + pim.width / 2 > wm[0] - WM_PAD:
            # chạm hàng watermark: thu hẹp đối xứng quanh tâm (chữ xuống dòng), giữ tâm x
            half = wm[0] - WM_PAD - x
            pim = sub_pill(text, maxw=max(300, int(2 * half) - 104))
            y = SF.SUB_TOP + pim.height / 2
        yy = y + 26 * (1 - pin)
        if alpha > 0.05:
            SUB_BOX = (x - pim.width * s / 2, yy - pim.height * s / 2, x + pim.width * s / 2, yy + pim.height * s / 2)
        if DRAW_SUB:
            put(out, pim, x, yy, s=s, alpha=alpha)
    return out


def subtitle(dst, tg, y=1610, tray=True, tray_col=CREAM):
    """Phụ đề luôn nằm trong dải dưới (tray_top → đáy khung), canh mép trên dải; không đè nội dung, né watermark NMT.
    Tham số y cũ (vd. 1610, 1690) chỉ còn ý nghĩa với phụ đề trên (y < H/2, không dùng ở nmt-engine nữa)."""
    global SUB_BOX, _SUB_PENDING
    x, maxw = W / 2, 900
    if PLATFORM:
        import platform_export as PX
        x, y, maxw = PX.remap_sub(y, maxw)
    if y >= H / 2:
        if tray:
            sub_tray(dst, col=tray_col)
        top = tray_top() + SUB_TOP_PAD
    else:
        top = None
    for a, b, text in CUES:
        if a - 0.01 <= tg < b:
            if SAFE916 and top is not None:
                # khung an toàn: chỉ ghi lại, safe_post() vẽ ở dải mới (mọi bản giống nhau)
                import safe_frame as SF
                im = sub_pill(text, maxw=SF.SUB_MAX_W - 92)   # maxw là bề rộng chữ; viên phụ đề rộng thêm 92 px
                pin = e_out(prog(tg, a, 0.18))
                pout = 1 - e_io(prog(tg, b - 0.18, 0.18))
                _SUB_PENDING = (im, 0.92 + 0.08 * pin, min(pin, pout), pin, text)
                return
            im = sub_pill(text, maxw=maxw)
            if top is not None:
                y = top + im.height / 2
                wm = _wm_for_layout()
                if wm and y + im.height / 2 + 26 > wm[1] - WM_PAD and x + im.width / 2 > wm[0] - WM_PAD:
                    # phụ đề cao (nhiều dòng) chạm hàng watermark: thu hẹp và dời trái cho mép phải cách watermark
                    maxw2 = int(min(maxw, 2 * (wm[0] - WM_PAD - 40) - 80))
                    im = sub_pill(text, maxw=max(400, maxw2 - 92))
                    x = min(x, wm[0] - WM_PAD - im.width / 2)
            pin = e_out(prog(tg, a, 0.18))
            pout = 1 - e_io(prog(tg, b - 0.18, 0.18))
            s, yy = 0.92 + 0.08 * pin, y + 26 * (1 - pin)
            if min(pin, pout) > 0.05:
                SUB_BOX = (x - im.width * s / 2, yy - im.height * s / 2, x + im.width * s / 2, yy + im.height * s / 2)
            if DRAW_SUB:
                put(dst, im, x, yy, s=s, alpha=min(pin, pout))
            return


# ---------------- trang trí cute ----------------
def heart(d, cx, cy, r, col=PINK2, outline=CH):
    pts = []
    for i in range(40):
        a = 2 * math.pi * i / 40
        x = 16 * math.sin(a) ** 3
        y = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        pts.append((cx + x * r / 16, cy + y * r / 16))
    d.polygon(pts, fill=col, outline=outline)


def star(d, cx, cy, r, col=BUTTER):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.4
        a = math.pi / 4 * i - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=CH)


BOKEH = [(np.random.default_rng(3).uniform(0, W), np.random.default_rng(i).uniform(0, H), 12 + 22 * ((i * 37) % 7) / 7, i) for i in range(18)]


def bokeh(dst, t, col=WHITE, a=80):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x0, y0, r, i in BOKEH:
        x = (x0 + 37 * i + 20 * math.sin(t * 0.6 + i)) % W
        y = (y0 - 30 * t * (0.5 + (i % 3) * 0.3)) % H
        al = int(a * (0.5 + 0.5 * math.sin(t * 1.3 + i)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (al,))
    dst.alpha_composite(lay)


def floating_hearts(dst, t, t0, x, y, n=6, spread=160):
    if t < t0:
        return
    d = ImageDraw.Draw(dst)
    for i in range(n):
        ph = ((t - t0) * 0.55 + i / n) % 1.0
        if t - t0 < i / n / 0.55:
            continue
        hx = x + spread * math.sin(i * 2.3) * 0.6 + 18 * math.sin((t + i) * 3)
        hy = y - 300 * ph
        r = (18 + 8 * (i % 3)) * math.sin(math.pi * min(1, ph * 1.6)) ** 0.5
        if r > 2:
            heart(d, hx, hy, r, col=PINK2 if i % 2 else (255, 160, 190))


def sparkle_field(dst, t, pts, base=22):
    d = ImageDraw.Draw(dst)
    for i, (x, y) in enumerate(pts):
        r = base * (0.55 + 0.45 * math.sin(t * 4 + i * 1.7))
        if r > 4:
            star(d, x, y, r)


def speed_lines(col_a, col_b, t, cx=540, cy=900):
    """Nền 'hoành tráng': tia xoay chậm, vẽ mỗi khung (rẻ)."""
    im = Image.new("RGBA", (W, H), col_a + (255,))
    d = ImageDraw.Draw(im)
    n = 28
    rot = t * 0.12
    R = 2400
    for i in range(n):
        if i % 2:
            continue
        a0 = 2 * math.pi * i / n + rot
        a1 = 2 * math.pi * (i + 1) / n + rot
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=col_b + (255,))
    gk = ("glowmask", cx, cy)
    if gk not in _bg:
        g = Image.new("L", (W, H), 0)
        ImageDraw.Draw(g).ellipse((cx - 420, cy - 420, cx + 420, cy + 420), fill=255)
        _bg[gk] = g.filter(ImageFilter.GaussianBlur(120))
    g = _bg[gk]
    im.paste(Image.new("RGBA", (W, H), tuple(min(255, c + 30) for c in col_a) + (255,)), (0, 0), g)
    return im


_bg = {}


def room():
    """Phòng khách pastel: sofa + gối tròn + cửa sổ có vệt nắng."""
    if "room" in _bg:
        return _bg["room"]
    im = Image.new("RGBA", (W, H), PINK + (255,))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 90):  # giấy dán tường chấm bi
        for y in range(60, 1300, 110):
            ox = 45 if (y // 110) % 2 else 0
            d.ellipse((x + ox - 6, y - 6, x + ox + 6, y + 6), fill=(250, 208, 208))
    d.rectangle((0, 1300, W, H), fill=WOOD)
    d.line((0, 1300, W, 1300), fill=CH, width=6)
    for y in (1420, 1580, 1780):
        d.line((0, y, W, y), fill=WOOD_D, width=3)
    d.rounded_rectangle((640, 250, 960, 640), radius=24, fill=SKYB, outline=CH, width=7)
    d.line((800, 250, 800, 640), fill=CH, width=6)
    d.line((640, 445, 960, 445), fill=CH, width=6)
    d.ellipse((690, 300, 760, 340), fill=WHITE)
    # dây cờ ngôi sao
    pts = [(60 + i * 60, 170 + 28 * math.sin(i * 0.55)) for i in range(17)]
    d.line(pts, fill=CH, width=3)
    for i, (x, y) in enumerate(pts[1:-1:2]):
        d.polygon([(x - 18, y), (x + 18, y), (x, y + 34)], fill=[BUTTER, MINT, LAV, PINK2][i % 4], outline=CH)
    # sofa
    d.rounded_rectangle((150, 820, 930, 1110), radius=70, fill=SOFA, outline=CH, width=7)
    d.rounded_rectangle((110, 960, 260, 1250), radius=60, fill=SOFA, outline=CH, width=7)
    d.rounded_rectangle((820, 960, 970, 1250), radius=60, fill=SOFA, outline=CH, width=7)
    d.rounded_rectangle((220, 1040, 860, 1250), radius=40, fill=SOFA_D, outline=CH, width=7)
    d.rectangle((210, 1250, 240, 1300), fill=CH)
    d.rectangle((840, 1250, 870, 1300), fill=CH)
    # chậu cây
    d.rounded_rectangle((30, 1150, 130, 1300), radius=14, fill=MINT, outline=CH, width=6)
    for cx, cy, rx, ry in ((60, 1090, 34, 70), (105, 1080, 30, 80)):
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(150, 200, 150), outline=CH, width=5)
    _bg["room"] = im
    return im


CUSHION = (540, 1045)


def cushion(dst, t, glow=0.0):
    d = ImageDraw.Draw(dst)
    if glow > 0:
        if "glow" not in _bg:
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.polygon([(760, 300), (900, 300), (700, 1080), (360, 1080)], fill=(255, 240, 170, 55))
            ld.ellipse((CUSHION[0] - 230, CUSHION[1] - 90, CUSHION[0] + 230, CUSHION[1] + 70), fill=(255, 236, 160, 110))
            _bg["glow"] = lay.filter(ImageFilter.GaussianBlur(26))
        dst.alpha_composite(with_alpha(_bg["glow"], glow * (0.85 + 0.15 * math.sin(t * 5))))
    cx, cy = CUSHION
    d.ellipse((cx - 170, cy - 48, cx + 170, cy + 48), fill=BUTTER, outline=CH, width=6)
    d.arc((cx - 120, cy - 28, cx + 120, cy + 30), 200, 340, fill=(230, 190, 90), width=4)


def cam(im, z=1.0, cx=W / 2, cy=H / 2, sx=0.0, sy=0.0, rot=0.0):
    if z == 1.0 and not sx and not sy and not rot:
        return im
    w, h = W / z, H / z
    x0 = clamp(cx - w / 2 + sx, 0, W - w)
    y0 = clamp(cy - h / 2 + sy, 0, H - h)
    out = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
    if rot:
        out = out.rotate(rot, resample=Image.BICUBIC, fillcolor=tuple(im.getpixel((5, 5))))
    return out


def shake(t, t0, d=0.3, a=14):
    if not (t0 <= t < t0 + d):
        return 0.0, 0.0
    k = (1 - (t - t0) / d) ** 2
    return a * k * math.sin(t * 95), a * k * math.cos(t * 77)


def lightning(dst, t, p0, p1, seg=9, width=16):
    rng = np.random.default_rng(int(t * 20))
    pts = []
    for i in range(seg + 1):
        f = i / seg
        x = p0[0] + (p1[0] - p0[0]) * f
        y = p0[1] + (p1[1] - p0[1]) * f
        if 0 < i < seg:
            x += rng.uniform(-50, 50)
            y += rng.uniform(-30, 30)
        pts.append((x, y))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.line(pts, fill=(255, 240, 150, 200), width=width + 18)
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(lay)
    d.line(pts, fill=CH, width=width + 6)
    d.line(pts, fill=(255, 250, 200), width=width)
    dst.alpha_composite(lay)


def dust(dst, t, x, y, t0, n=4, dirx=1):
    if t < t0:
        return
    d = ImageDraw.Draw(dst)
    for i in range(n):
        p = prog(t, t0 + i * 0.05, 0.5)
        if 0 < p < 1:
            r = 16 + 30 * p
            cx = x - dirx * (30 + 70 * p) + 20 * i
            d.ellipse((cx - r, y - r - 20 * p, cx + r, y + r - 20 * p), fill=(255, 255, 255, int(200 * (1 - p))), outline=(200, 180, 170))


# ---------------- asset alias ----------------
TI_ANGRY, TI_ARGUE = "TI_EXP_LOCAL_ANGRY", "TI_DLG_LOCAL_ARGUING"
NG_ANGRY, NG_ARGUE = "NGANG_EXP_LOCAL_ANGRY", "NGANG_DLG_LOCAL_ARGUING"
TI_STOMP, TI_FLAIL, TI_DESPAIR, TI_SCARF, TI_PEEK = "TI_ACTING_011", "TI_ACTING_016", "TI_ACTING_019", "TI_ACTING_015", "TI_ACTING_012"
NG_STOMP, NG_HOP, NG_FACEPALM, NG_SCARF = "NGANG_ACTING_013", "NGANG_ACTING_012", "NGANG_ACTING_017", "NGANG_ACTING_014"
MI_CURL, MI_YAWN, MI_BELLY, MI_SLEEPY = "MIMI_ACTING_015", "MIMI_ACTING_019", "MIMI_ACTING_007", "MIMI_ACTING_011"
TI_WAVE, NG_WAVE, MI_PAW = "TI_BODY_SAMPLE_002_V01", "NGANG_BODY_SAMPLE_002_V01", "MIMI_BODY_SAMPLE_002_V01"


def talk_bust(dst, tg, who, closed, opened, x, y, scale, flip=False, sc=None, t=0.0):
    # Hai sprite đóng/mở lệch khung nên không chồng alpha (gây bóng ma): diễn thoại bằng nhún + gật theo biên độ giọng
    e = amp(tg, who)
    o = clamp((e - 0.04) / 0.3)
    sy = breathe(t, amp=0.008) * (1 + 0.025 * o)
    place(dst, closed, x, y, scale=scale, flip=flip, sy=sy, rot=2.0 * o * math.sin(t * 9), scene=sc, shadow=False)



def room_frame(t, glow=0.0, mimi=None):
    im = room().copy()
    bokeh(im, t, WHITE, 70)
    cushion(im, t, glow)
    if mimi:
        mimi(im)
    return im



def ghost(dst, aid, pos_fn, t, h, n=3, dt=0.025, flip=False, rot_fn=None, scene=None):
    """Vệt mờ chuyển động: vẽ lại các vị trí trước với alpha giảm dần."""
    for i in range(n, 0, -1):
        x, y = pos_fn(t - i * dt)
        place(dst, aid, x, y, h=h, flip=flip, alpha=0.18 * (n - i + 1) / n, rot=rot_fn(t - i * dt) if rot_fn else 0, shadow=False)
    x, y = pos_fn(t)
    place(dst, aid, x, y, h=h, flip=flip, rot=rot_fn(t) if rot_fn else 0, scene=scene)



def zzz(dst, x, y, t, s=1.0):
    for i in range(3):
        ph = (t * 0.6 + i / 3) % 1.0
        put(dst, text_img("z", int((34 + 14 * i) * s), (150, 130, 200), "ExtraBold", stroke=4), x + 28 * i * s + 10 * math.sin(ph * 6), y - 100 * ph * s, alpha=math.sin(math.pi * ph))



def hblur(im, k):
    if k < 2:
        return im
    return im.resize((max(1, W // k), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)


def frame(tg):
    i = max(j for j, s in enumerate(SCENES) if STARTS[s[0]] <= tg + 1e-9)
    sid, dur, _, tr, td = SCENES[i]
    tau = tg - STARTS[sid]
    B = _call(sid, tau)
    if i == 0 or tr == "cut" or tau >= td:
        return B
    psid = SCENES[i - 1][0]
    A = _call(psid, SCENES[i - 1][1] + tau)
    # bài học EP29 F17: cảnh trả khung RGB làm Image.blend lỗi 'images do not match' -> chuẩn hoá về RGBA
    A, B = (im if im.mode == "RGBA" else im.convert("RGBA") for im in (A, B))
    p = tau / td
    if tr == "fade":
        return Image.blend(A, B, e_io(p))
    if tr == "whip":
        q = e_io5(p)
        out = Image.new("RGBA", (W, H))
        out.paste(A, (int(-W * q), 0))
        out.paste(B, (int(W * (1 - q)), 0))
        return hblur(out, int(1 + 22 * math.sin(math.pi * p)))
    if tr == "flash":
        white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        return Image.blend(A, white, e_out(p / 0.5)) if p < 0.5 else Image.blend(white, B, e_io((p - 0.5) / 0.5))
    if tr == "black_in":
        return Image.blend(Image.new("RGBA", (W, H), (24, 20, 22, 255)), B, e_io(p))
    if tr == "iris":
        r = int(e_io5(p) * 1300)
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=255)
        out = A.copy()
        out.paste(B, (0, 0), m)
        return out
    return B


def check_subs(step=6, thr=0.004, plat=None):
    """QA tự động: phụ đề có đè lên nhân vật không (quy tắc Owner 08/11/2026).
    Mỗi khung mẫu được dựng 2 lần (có / không có sprite, cùng không vẽ phụ đề); điểm ảnh khác nhau = nhân vật (kể cả bóng).
    Tỉ lệ điểm nhân vật trong hộp phụ đề > thr là LỖI. Bỏ qua khung đang chuyển cảnh. Trả về báo cáo dict."""
    global HIDE_SPRITES, DRAW_SUB, SUB_BOX, PLATFORM
    old_p = PLATFORM
    PLATFORM = plat
    bad, n_checked, worst = [], 0, {}
    wm = wm_box(plat) if plat else None   # bản nền tảng mới gắn watermark NMT
    wm_bad, band_bad = [], []
    band = band_frac()                     # chặn ngay nếu dải phụ đề > 1/3 khung
    ttop = tray_top()
    crop_bad = []
    if SAFE916:
        import safe_frame as SF
        ttop = SF.CONTENT_BOTTOM
    try:
        DRAW_SUB = False
        for sid, dur, _t, tr, td in SCENES:
            for k in range(0, int(round(dur * FPS)), step):
                tau = k / FPS
                if tr != "cut" and tau < td and sid != SCENES[0][0]:
                    continue
                tg = STARTS[sid] + tau
                SUB_BOX = None
                HIDE_SPRITES = False
                A = np.asarray(frame(tg).convert("RGB")).astype(np.int16)
                box = SUB_BOX
                if box is None:
                    continue
                if SAFE916 and SF.check_box(box, "subtitle"):
                    crop_bad.append({"scene": sid, "t": round(tau, 3), "sub_box": [int(v) for v in box], "issues": SF.check_box(box, "subtitle")})
                if box[1] < ttop - 1 or box[3] > H:
                    band_bad.append({"scene": sid, "t": round(tau, 3), "sub_box": [int(v) for v in box], "band_top": ttop})
                if wm and box[0] < wm[2] + WM_PAD and wm[0] - WM_PAD < box[2] and box[1] < wm[3] + WM_PAD and wm[1] - WM_PAD < box[3]:
                    wm_bad.append({"scene": sid, "t": round(tau, 3), "sub_box": [int(v) for v in box], "wm_box": list(wm)})
                HIDE_SPRITES = True
                B = np.asarray(frame(tg).convert("RGB")).astype(np.int16)
                HIDE_SPRITES = False
                x0, y0 = max(0, int(box[0]) - 6), max(0, int(box[1]) - 6)
                x1, y1 = min(W, int(box[2]) + 6), min(H, int(box[3]) + 6)
                m = np.abs(A[y0:y1, x0:x1] - B[y0:y1, x0:x1]).max(-1) > 24
                r = float(m.mean()) if m.size else 0.0
                n_checked += 1
                worst[sid] = max(worst.get(sid, 0.0), r)
                if r > thr:
                    bad.append({"scene": sid, "t": round(tau, 3), "overlap": round(r, 4), "box": [x0, y0, x1, y1]})
    finally:
        HIDE_SPRITES, DRAW_SUB, SUB_BOX, PLATFORM = False, True, None, old_p
    return {"platform": plat or "master", "step_frames": step, "threshold": thr, "frames_checked": n_checked,
            "worst_by_scene": {k: round(v, 4) for k, v in worst.items()}, "violations": bad,
            "watermark_box": list(wm) if wm else None, "watermark_pad": WM_PAD, "watermark_violations": wm_bad,
            "content_frac": CONTENT_FRAC, "band_frac": round(band, 4), "band_top": ttop, "outside_band": band_bad,
            "safe_frame": "NMT-SAFE-916 v1" if SAFE916 else None, "safe_frame_violations": crop_bad,
            "pass": not bad and not wm_bad and not band_bad and not crop_bad}


WM_PAD = 24   # khoảng hở tối thiểu (px) giữa hộp phụ đề và watermark NMT


def wm_box(plat, brand="ngang-mot-ti"):
    """Hộp watermark NMT thật (x0, y0, x1, y1) trên khung dọc của nền tảng, tính bằng branding.geometry (cùng hàm lúc chèn).
    Áp dụng ghi đè output/<tập>/watermark.json nếu có."""
    root = os.path.abspath(os.path.join(ENGINE, "..", ".."))
    if os.path.join(root, "src") not in sys.path:
        sys.path.insert(0, os.path.join(root, "src"))
    from ai_video_factory.core import branding
    logo, _ = branding.load_master(brand)
    ov = {}
    p = os.path.join(OUT, "watermark.json") if OUT else ""
    if p and os.path.exists(p):
        j = json.load(open(p, encoding="utf-8"))
        ov = dict(j.get("default", {}), **j.get(plat, {}))
    if SAFE916:
        import safe_frame as SF
        ov = SF.wm_override(ov)
    g = branding.geometry(brand, W, H, plat, ov or None, logo.size)
    return (g["x"], g["y"], g["x"] + g["w"], g["y"] + g["h"])


def require_music_unique(meta=None):
    """Owner 19/11/2026 (thay rule 13/11): ĐƯỢC dùng lại nhạc nền có sẵn nếu hợp tập; chỉ tìm/tải nhạc mới khi kho không
    có bản phù hợp (vẫn xin Owner từng file). --mux chỉ báo bản nhạc đã dùng ở tập nào, không chặn.
    Muốn bắt buộc nhạc riêng cho một tập: META["music_unique"] = True."""
    sys.path.insert(0, ENGINE)
    import qa_checks as QA
    hits = QA.music_reuse(OUT)
    for h in hits:
        print("  NHẠC DÙNG LẠI: %s (%s…) đã dùng ở %s" % (h["title"], h["sha"][:10], ", ".join(h["episodes"])))
    if hits and (meta or {}).get("music_unique"):
        raise SystemExit("CHẶN --mux: tập này đặt META['music_unique'] nhưng nhạc nền đã dùng ở tập khác.")


def require_subs_ok(plat=None):
    """Chặn ghép/xuất khi phụ đề đè nhân vật. Ghi báo cáo render/qa_subtitles_<bản>.json."""
    rep = check_subs(plat=plat)
    with open(os.path.join(HERE, "qa_subtitles_%s.json" % (plat or "master")), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=1)
    if rep.get("safe_frame_violations"):
        v = rep["safe_frame_violations"]
        raise SystemExit("CHẶN [%s]: phụ đề ra ngoài khung an toàn NMT-SAFE-916 ở %d khung mẫu (vd. %s t=%.2fs, %s)"
                         % (rep["platform"], len(v), v[0]["scene"], v[0]["t"], v[0]["issues"]))
    if rep["outside_band"]:
        v = rep["outside_band"]
        raise SystemExit("CHẶN [%s]: phụ đề nằm ngoài dải dưới (mép trên dải y=%d) ở %d khung mẫu (vd. %s t=%.2fs, hộp %s)"
                         % (rep["platform"], rep["band_top"], len(v), v[0]["scene"], v[0]["t"], v[0]["sub_box"]))
    if rep["watermark_violations"]:
        v = rep["watermark_violations"]
        raise SystemExit("CHẶN [%s]: phụ đề chạm watermark NMT ở %d khung mẫu (vd. %s t=%.2fs, phụ đề %s, watermark %s). Báo cáo: qa_subtitles_%s.json"
                         % (rep["platform"], len(v), v[0]["scene"], v[0]["t"], v[0]["sub_box"], v[0]["wm_box"], rep["platform"]))
    if not rep["pass"]:
        v = rep["violations"]
        raise SystemExit("CHẶN [%s]: phụ đề đè nhân vật ở %d khung mẫu (vd. %s t=%.2fs, %.1f%% hộp phụ đề). Báo cáo: qa_subtitles_%s.json"
                         % (rep["platform"], len(v), v[0]["scene"], v[0]["t"], 100 * v[0]["overlap"], rep["platform"]))
    return rep


def render_scene(sid):
    os.makedirs(SEG, exist_ok=True)
    t0g = STARTS[sid]
    n = int(round(SDUR[sid] * FPS))
    final = os.path.join(SEG, sid + ".mp4")
    tmp = os.path.join(SEG, sid + ".part.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    st = time.time()
    for k in range(n):
        p.stdin.write(frame(t0g + k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    if p.returncode != 0:
        raise SystemExit("ffmpeg loi " + sid)
    os.replace(tmp, final)
    return {"scene": sid, "frames": n, "render_s": round(time.time() - st, 1)}



def stills(picks, thumb=None, title=None):
    os.makedirs(os.path.join(HERE, "stills"), exist_ok=True)
    tiles = []
    for sid, lt in picks:
        fr = frame(STARTS[sid] + lt).convert("RGB")
        fr.save(os.path.join(HERE, "stills", sid + ".png"))
        tiles.append((sid, fr))
    tw, th = 270, 480
    rows = (len(tiles) + 4) // 5
    sheet = Image.new("RGB", (tw * 5 + 60, (th + 50) * rows + 20), CREAM)
    dd = ImageDraw.Draw(sheet)
    for i, (sid, fr) in enumerate(tiles):
        x, y = 10 + (i % 5) * (tw + 10), 10 + (i // 5) * (th + 50)
        sheet.paste(fr.resize((tw, th), Image.LANCZOS), (x, y))
        dd.text((x, y + th + 6), "%s  %s" % (sid, [s[2] for s in SCENES if s[0] == sid][0]), font=font(17, "SemiBold"), fill=CH)
    sheet.save(os.path.join(OUT, "contact_sheet.png"))
    if thumb:
        th_im = frame(STARTS[thumb[0]] + thumb[1]).convert("RGBA")
        if title:
            put(th_im, pill(title, 80, BUTTER, CH, CH, padx=46, pady=26), W / 2, 230, rot=-3)
        th_im.convert("RGB").save(os.path.join(OUT, "thumbnail.png"))


def mux():
    lst = os.path.join(HERE, "concat.txt")
    # Bài học EP23 (13/11/2026): render một cảnh lỗi nhưng segment cũ vẫn còn → --mux ghép bản cũ (67 s) với tiếng mới (71 s)
    # mà không báo. Chặn khi độ dài segment lệch thời lượng cảnh > 0,1 s.
    bad = []
    for s in SCENES:
        seg = os.path.join(HERE, "segments", "%s.mp4" % s[0])
        if not os.path.exists(seg):
            bad.append("%s: thiếu" % s[0])
            continue
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", seg],
                                 capture_output=True, text=True).stdout.strip() or 0)
        if abs(d - s[1]) > 0.1:
            bad.append("%s: %.2f s ≠ %.2f s" % (s[0], d, s[1]))
    if bad:
        raise SystemExit("CHẶN --mux: segment không khớp thời lượng cảnh (render lại): " + "; ".join(bad))
    with open(lst, "w") as fh:
        for s in SCENES:
            fh.write("file 'segments/%s.mp4'\n" % s[0])
    tmp = os.path.join(OUT, "final_video.part.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(OUT, "audio", "master.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, os.path.join(OUT, "final_video.mp4"))
    print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,nb_frames",
                          "-of", "compact", os.path.join(OUT, "final_video.mp4")], capture_output=True, text=True).stdout)


def _creative_brief_md(meta):
    """Agent V2.0 mục III + VIII-A: bảng 3 concept và creative brief (chỉ khi META có)."""
    out = []
    ide = meta.get("ideation") or {}
    if ide.get("concepts"):
        out += ["## Chọn concept (Agent V2.0)", "", "| Concept | Loại | Điểm /100 | Logline | Hook | Twist |", "|---|---|---|---|---|---|"]
        for c in ide["concepts"]:
            out.append("| %s | %s | %s | %s | %s | %s |" % (c.get("name", ""), c.get("type", ""), c.get("score", ""),
                       c.get("logline", ""), c.get("hook", ""), c.get("twist", "")))
        out += ["", "**Chọn:** %s — %s" % (ide.get("chosen", ""), ide.get("reason", "")), ""]
    rows = [("Thời lượng", meta.get("duration_s")), ("Phong cách", ", ".join(map(str, meta.get("visual_styles", [])))),
            ("Cơ chế hài chính", (meta.get("comedy") or {}).get("main")),
            ("Cơ chế bổ trợ", ", ".join((meta.get("comedy") or {}).get("support", []))),
            ("Gieo twist", meta.get("twist_seed")), ("Khán giả", meta.get("audience"))]
    rows = [(k, v) for k, v in rows if v]
    if rows:
        out += ["## Creative brief", ""] + ["- **%s:** %s" % (k, v) for k, v in rows] + [""]
    return out


def write_script(meta=None):
    """Bước 1: kịch bản để Owner đọc (script.md) + lines.json cho TTS."""
    meta = meta or {}
    vn = {"ti": "Tí", "ngang": "Ngang"}
    out = ["# Kịch bản — %s" % meta.get("title", os.path.basename(OUT)), ""]
    if meta.get("logline"):
        out += ["**Ý tưởng:** " + meta["logline"], ""]
    out += _creative_brief_md(meta)
    out += ["Định dạng: 9:16 · 1080×1920 · 60 fps · khoảng %.0f giây · phụ đề không ghi tên nhân vật" % TOTAL, ""]
    notes = meta.get("notes", {})
    for sid, dur, title, tr, td in SCENES:
        out.append("## %s — %s  (≈%.1f s, vào cảnh: %s)" % (sid, title, dur, tr))
        if notes.get(sid):
            out.append("*Hình:* " + notes[sid])
        for vid, s2, lt, spk, text in VOICE:
            if s2 == sid:
                out.append("- **%s:** %s" % (vn.get(spk, spk), text))
        out.append("")
    if meta.get("end"):
        out += ["## Kết", meta["end"], ""]
    os.makedirs(HERE, exist_ok=True)
    open(os.path.join(HERE, "script.md"), "w", encoding="utf-8").write("\n".join(out))
    lines = [{"id": vid, "char": spk, "voice": VOICE_NAME[spk], "text": text} for vid, _, _, spk, text in VOICE]
    json.dump(lines, open(os.path.join(HERE, "lines.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return os.path.join(HERE, "script.md")


def run_tts():
    """Tạo giọng VieNeu từ lines.json đã duyệt (macOS: venv-vieneu; Linux VM: thư viện tạm)."""
    mac_py = os.path.join(ROOT, "workspace", "venv-vieneu", "bin", "python")
    env = dict(os.environ)
    env["HF_HOME"] = os.path.join(ROOT, "workspace", "hf-cache")
    env["HF_HUB_OFFLINE"] = "1"
    if sys.platform == "darwin" and os.path.exists(mac_py):
        py = mac_py
        env["PYTHONPATH"] = os.path.join(ROOT, "workspace", "shim")
    else:
        py = sys.executable
        env["PYTHONPATH"] = os.pathsep.join([os.path.expanduser("~/pyvn"), os.path.expanduser("~/vnpkg")])
    r = subprocess.run([py, os.path.join(ENGINE, "tts_vieneu.py"), OUT], env=env, capture_output=True, text=True)
    open(os.path.join(HERE, "tts_log.txt"), "w").write(r.stdout + r.stderr[-2000:])
    if r.returncode != 0:
        raise SystemExit("TTS lỗi:\n" + r.stderr[-800:])
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "tts ok")


def _arg(argv, flag, default=""):
    return argv[argv.index(flag) + 1] if flag in argv and argv.index(flag) + 1 < len(argv) else default


def _main_impl(picks, thumb=None, title=None, sfx=None, music=None, argv=None, meta=None):
    """Quy trình chuẩn (gates.py): --script -> duyệt kịch bản -> --tts, --storyboard -> duyệt hình -> render -> --audio -> --mux -> duyệt video."""
    sys.path.insert(0, ENGINE)
    import gates as G
    argv = sys.argv[1:] if argv is None else argv
    ep_py = os.path.abspath(sys.argv[0])
    if "--status" in argv:
        wf = G.load(OUT)
        print(json.dumps({"state": wf["state"], "approvals": {k: {x: v.get(x) for x in ("status", "at", "note")} for k, v in wf["approvals"].items()},
                          "script_ok": G.is_approved(OUT, wf, "script", ep_py), "visual_ok": G.is_approved(OUT, wf, "visual", ep_py)},
                         ensure_ascii=False, indent=1))
        return
    for flag, dec in (("--approve", "approved"), ("--reject", "rejected")):
        if flag in argv:
            stage = _arg(argv, flag)
            wf = G.decide(OUT, stage, ep_py, dec, note=_arg(argv, "--note"), by=_arg(argv, "--by", "owner"))
            print("Đã ghi: %s %s -> trạng thái %s" % (G.LABEL[stage], dec, wf["state"]))
            return
    if "--library-sync" in argv:
        # lưu sprite ghép/sửa của tập đã duyệt video cuối vào thư viện (library_sync.py)
        import library_sync as LS
        res, used = LS.sync(sys.modules[__name__], OUT, getattr(sys.modules.get("__main__"), "LIBRARY_OVERRIDES", None))
        print(json.dumps({"episode_assets": res, "library_assets_used": used}, ensure_ascii=False, indent=1))
        return
    if "--script" in argv:
        p = write_script(meta)
        G.submit(OUT, "script", ep_py, "awaiting_script_approval")
        if _script_gate_mode(meta, argv) == "owner":
            print("Bước 1 xong. Kịch bản: %s\nCHỜ Owner duyệt kịch bản." % p)
        else:
            print("Bước 1 xong. Kịch bản: %s\nTiếp: --script-review (quy trình v2: ≥ 9/10 + hội đồng người xem; tối đa 3 lần, sau đó Owner duyệt)." % p)
        return
    G.require(OUT, "script", ep_py, "tạo giọng / hình mẫu")
    if "--tts" in argv:
        run_tts()
        return
    load_voice()
    CUES[:] = cues()
    if "--storyboard" in argv or "--stills" in argv:
        require_art_ok()
        stills(picks, thumb, title)
        G.submit(OUT, "visual", ep_py, "awaiting_visual_approval")
        print("Bước 2 xong. Hình mẫu: %s\nCHỜ Owner duyệt hình ảnh." % os.path.join(OUT, "contact_sheet.png"))
        return
    G.require(OUT, "visual", ep_py, "render video")
    if "--audio" in argv:
        sys.path.insert(0, ENGINE)
        import audio_engine
        audio_engine.build(sys.modules[__name__], sfx or [], music or [])
        return
    if "--check-subs" in argv:
        plat = _arg(argv, "--check-subs") or None
        plat = plat if plat and not plat.startswith("--") else None
        rep = check_subs(plat=plat)
        with open(os.path.join(HERE, "qa_subtitles_%s.json" % (plat or "master")), "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
        print(json.dumps({k: rep[k] for k in ("platform", "frames_checked", "worst_by_scene", "watermark_box", "band_frac", "band_top", "pass")}, ensure_ascii=False))
        for v in rep["outside_band"][:12]:
            print("  NGOÀI DẢI:", json.dumps(v))
        for v in rep["violations"][:12]:
            print("  ĐÈ:", json.dumps(v))
        for v in rep["watermark_violations"][:12]:
            print("  CHẠM WATERMARK:", json.dumps(v))
        return
    if "--mux" in argv:
        require_subs_ok(None)
        require_timing_ok()
        require_music_unique(meta)
        mux()
        G.submit(OUT, "final", ep_py, "awaiting_final_approval")
        print("Bước 3 xong. CHỜ Owner duyệt video cuối.")
        return
    if "--export" in argv or "--export-finish" in argv:
        global PLATFORM, SEG
        import platform_export as PX
        G.require(OUT, "final", ep_py, "xuất đa nền tảng")
        if "--export-finish" in argv:
            for p_ in PX.ORDER:
                require_subs_ok(p_)
            tdir, made = PX.finish(sys.modules[__name__], meta or {}, G.load(OUT))
            for plat, vid, info in made:
                print(json.dumps({"platform": plat, "file": vid, "duration_s": info["duration_s"], "within_limit": info["within_length_limit"]}, ensure_ascii=False))
            print("Đã xuất vào: " + tdir)
            # Owner 12/11/2026: bất kỳ video cuối nào được tạo thì thêm hình vào thư viện
            import library_sync as LS
            res, used = LS.sync(sys.modules[__name__], OUT, getattr(sys.modules.get("__main__"), "LIBRARY_OVERRIDES", None))
            print("Đã thêm hình vào thư viện: " + json.dumps(res, ensure_ascii=False))
            return
        plat = _arg(argv, "--export")
        if plat not in PX.PLATFORMS:
            raise SystemExit("Nền tảng không hợp lệ: %s (chọn %s)" % (plat, ", ".join(PX.ORDER)))
        PLATFORM, SEG = plat, PX.seg_dir(sys.modules[__name__], plat)
        sids = [a for a in argv if not a.startswith("--") and a != plat] or [s[0] for s in SCENES]
        for sid in sids:
            r = render_scene(sid)
            r["platform"] = plat
            print(json.dumps(r), flush=True)
        return
    sids = [a for a in argv if not a.startswith("--")] or [s[0] for s in SCENES]
    for sid in sids:
        r = render_scene(sid)
        print(json.dumps(r), flush=True)
        with open(os.path.join(HERE, "render_log.jsonl"), "a") as fh:
            fh.write(json.dumps(r) + "\n")
    up = os.path.join(HERE, "used_assets.json")
    prev = json.load(open(up)) if os.path.exists(up) else {}
    for k, v in USED.items():
        prev[k] = sorted(set(prev.get(k, [])) | v)
    json.dump(prev, open(up, "w"), indent=1)

# ================= Quality Gate mới + đo đạc (Giai đoạn A, 12/11/2026) =================
def _episode_module():
    return sys.modules.get("__main__")


def art_dir_default():
    """ART_DIR của tập nếu khai báo; không thì art/v<mới nhất> có PNG."""
    m = _episode_module()
    d = getattr(m, "ART_DIR", None)
    if d:
        return str(d)
    root = os.path.join(OUT, "art")
    if not os.path.isdir(root):
        return None
    vs = sorted(x for x in os.listdir(root) if x.startswith("v") and os.path.isdir(os.path.join(root, x)))
    vs = [v for v in vs if any(f.lower().endswith(".png") for f in os.listdir(os.path.join(root, v)))]
    return os.path.join(root, vs[-1]) if vs else None


def run_check_art(art_dir=None):
    import qa_checks as Q
    d = art_dir or art_dir_default()
    if not d:
        raise SystemExit("Không tìm thấy thư mục tranh (đặt ART_DIR trong tập hoặc art/v01/*.png).")
    return Q.check_art(d, report_path=os.path.join(HERE, "qa_art.json"))


def run_check_timing():
    """Chuyển cảnh + tiếng/hình. Ghi qa_transitions.json, qa_sync.json."""
    import qa_checks as Q
    tr = Q.check_transitions(SCENES)
    if VOICE and not VDUR:
        load_voice()
    sy = Q.check_sync(SCENES, VOICE, STARTS, VDUR, voice_onset)
    os.makedirs(HERE, exist_ok=True)
    for name, rep in (("qa_transitions.json", tr), ("qa_sync.json", sy)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
    return tr, sy


def require_art_ok():
    """Tập khai báo ART_CHECK = True: chặn --storyboard khi tranh chưa qua check_art."""
    if not getattr(_episode_module(), "ART_CHECK", False):
        return
    rep = run_check_art()
    if not rep["pass"]:
        bad = [i for i in rep["items"] if not i["pass"]]
        raise SystemExit("CHẶN: %d/%d tranh chưa đạt --check-art (vd. %s: %s). Báo cáo: render/qa_art.json"
                         % (len(bad), rep["images"], bad[0]["name"], bad[0]["errors"][0]))


def require_timing_ok():
    tr, sy = run_check_timing()
    errs = tr["errors"] + sy["errors"]
    if errs:
        raise SystemExit("CHẶN (chuyển cảnh / tiếng-hình): " + " | ".join(errs[:4]))


def _script_gate_mode(meta, argv):
    if "--manual-script-gate" in argv or (meta or {}).get("script_gate") == "owner":
        return "owner"
    return "auto"


def run_script_review(argv, meta):
    """D-029: chấm kịch bản tự động. Dạng:
      --script-review                       chấm bằng Codex (lần thử kế tiếp)
      --script-review prompt                ghi prompt giám khảo cho subagent Claude (khi Codex không dùng được)
      --script-review record <file.json> [--judge claude-subagent]   ghi kết quả giám khảo ngoài
      --script-review viewer-prompt         (quy trình v2) ghi prompt hội đồng người xem cho subagent Claude mới
      --script-review viewer <file.json> [--judge claude-subagent]   ghi kết quả hội đồng người xem cho bản hiện tại
      --script-review status                xem trạng thái
      --script-review reset                 (Owner yêu cầu) lưu trạng thái cũ, bắt đầu vòng mới"""
    sys.path.insert(0, ENGINE)
    import gates as G
    import metrics as MX
    import script_review as SR
    meta = meta or {}
    ep_py = os.path.abspath(sys.argv[0])
    sub = _arg(argv, "--script-review")
    sub = sub if sub and not sub.startswith("--") else "run"
    files = G.gated_files(OUT, "script", ep_py)
    st = SR.load_state(OUT)
    if sub == "status":
        print(SR.summary_text(st))
        return
    if sub == "reset":
        p = os.path.join(HERE, "script_review.json")
        if os.path.exists(p):
            os.replace(p, os.path.join(HERE, "script_review_%s.json" % time.strftime("%Y%m%d_%H%M%S")))
        print("Đã lưu trạng thái cũ, bắt đầu vòng chấm mới.")
        return
    if _script_gate_mode(meta, argv) == "owner":
        raise SystemExit("Cổng kịch bản đang ở chế độ Owner duyệt (META script_gate='owner' hoặc --manual-script-gate).")
    if sub == "prompt":
        print("Prompt giám khảo cho subagent Claude (không đưa lịch sử hội thoại): " + SR.judge_prompt_for_subagent(OUT, files, meta))
        return
    if sub == "viewer-prompt":
        print("Prompt hội đồng người xem cho subagent Claude MỚI: " + SR.viewer_prompt_for_subagent(OUT, files))
        return
    if sub == "viewer":
        src = argv[argv.index("viewer") + 1] if argv.index("viewer") + 1 < len(argv) else ""
        if not src or not os.path.exists(src):
            raise SystemExit("Cần file JSON kết quả hội đồng người xem: --script-review viewer <file.json>")
        import codex_client as C
        res = SR.record_viewer(OUT, files, C.extract_json(open(src, encoding="utf-8").read()),
                               judge=_arg(argv, "--judge", "claude-subagent"))
        print("Hội đồng người xem: %d/24 — %s" % (res["score"], "ĐẠT" if res["pass"] else "CHƯA ĐẠT"))
        for f in res["fixes"]:
            print("     • " + f)
        return
    if st.get("status") == "passed" and os.path.exists(files[0]) and SR.sha_files(files) != st["attempts"][-1]["sha256"]:
        os.replace(os.path.join(HERE, "script_review.json"),
                   os.path.join(HERE, "script_review_%s.json" % time.strftime("%Y%m%d_%H%M%S")))
        print("Kịch bản đổi sau lần đạt trước: bắt đầu vòng chấm mới.")
    external = None
    if sub == "record":
        src = argv[argv.index("record") + 1] if "record" in argv and argv.index("record") + 1 < len(argv) else ""
        if not src or not os.path.exists(src):
            raise SystemExit("Cần file JSON kết quả giám khảo: --script-review record <file.json>")
        import codex_client as C
        raw = open(src, encoding="utf-8").read()
        external = {"judge": _arg(argv, "--judge", "claude-subagent"), "raw": raw, "obj": C.extract_json(raw),
                    "thread_id": None}
    t0 = time.time()
    try:
        st, rec = SR.attempt(OUT, files, meta, VOICE, SCENES, STARTS, external=external)
    except Exception as exc:
        import codex_client as C
        if isinstance(exc, C.CodexUnavailable):
            p = SR.judge_prompt_for_subagent(OUT, files, meta)
            MX.record(OUT, "script-review", time.time() - t0, status="judge_unavailable")
            raise SystemExit("Codex không chấm được (%s). Không tính lần thử. Dự phòng: subagent Claude mới chấm theo %s, "
                             "rồi --script-review record <file.json> --judge claude-subagent." % (exc, p))
        raise
    MX.record(OUT, "script-review", time.time() - t0, status="passed" if rec["passed"] else "failed",
              attempt=rec["n"], total=rec.get("total"), judge=rec.get("judge"))
    print(SR.summary_text(st))
    if st["status"] == "passed":
        rule = "rule Owner >9,0/10" if rec.get("gate_rule") == "owner_above_9" else "D-029"
        by = "auto-review (%s, %.1f/10, lần %d)" % (rec["judge"], rec["total"], rec["n"])
        wf = G.auto_approve(OUT, "script", ep_py, rec["sha256"], by, note="%s; render/script_review.json" % rule)
        print("ĐẠT: cổng kịch bản tự duyệt -> %s. Hiển thị đầy đủ kịch bản cho Owner xem (không chờ)." % wf["state"])
    elif st["status"] == "needs_owner":
        print("⛔ CHUYỂN OWNER DUYỆT KỊCH BẢN: %s. Gửi bản lần %s kèm điểm và góp ý." % (st.get("reason"), st.get("best_attempt", rec["n"])))
    else:
        print("CHƯA ĐẠT (lần %d/%d): sửa theo góp ý, chạy --script rồi --script-review." % (rec["n"], SR.MAX_ATTEMPTS))


def run_art_auto(argv):
    """D-029: --art-auto [CẢNH …] [--fix "lỗi"] [--prompts art/PROMPTS_v01.md]. Cần kịch bản đã duyệt."""
    sys.path.insert(0, ENGINE)
    import art_auto as AA
    import gates as G
    import metrics as MX
    ep_py = os.path.abspath(sys.argv[0])
    G.require(OUT, "script", ep_py, "tạo tranh tự động")
    m = _episode_module()
    art_dir = art_dir_default() if getattr(m, "ART_DIR", None) else os.path.join(OUT, "art", "v01")
    rev = os.path.basename(str(art_dir).rstrip("/"))
    prompts = _arg(argv, "--prompts") or os.path.join(OUT, "art", "PROMPTS_%s.md" % rev)
    refs = [str(p) for p in getattr(m, "ART_REFS", [])] or (
        [os.path.join(OUT, "refs", f) for f in sorted(os.listdir(os.path.join(OUT, "refs")))]
        if os.path.isdir(os.path.join(OUT, "refs")) else [])
    skip = {"--art-auto", "--fix", "--prompts", _arg(argv, "--fix"), _arg(argv, "--prompts")}
    scenes = [a for a in argv if a not in skip and not a.startswith("--")]
    t0 = time.time()
    rep = AA.run(OUT, os.path.basename(OUT), rev, prompts, scenes=scenes or None, refs=refs, fix_note=_arg(argv, "--fix"))
    MX.record(OUT, "art-auto", time.time() - t0, status="stopped" if rep["stopped"] else "ok",
              scenes=len(rep["scenes"]))
    for sid, r in rep["scenes"].items():
        print("%-6s %-16s lần %s  %s" % (sid, r.get("status"), r.get("attempt", "-"),
                                        "; ".join(r.get("machine_errors") or []) or r.get("reason", "")))
    used, cap = AA.budget(OUT, len(AA.parse_prompts(prompts)))
    print("Lượt image_gen đã dùng: %d/%d" % (used, cap))
    if rep["stopped"]:
        raise SystemExit("DỪNG: " + rep["stopped"] + ". Báo Owner: chờ có lượt lại hoặc tạo trên ChatGPT web (Owner tự đăng nhập).")
    print("Tiếp: --check-art, xem art/%s/_qa/*_overlay.jpg, ghi safe_annotations.json; cảnh lỗi bố cục: --art-auto CẢNH --fix \"…\"." % rev)


def _step_name(argv):
    for f in ("--script", "--tts", "--storyboard", "--stills", "--audio", "--check-subs", "--mux", "--export-finish",
              "--export", "--approve", "--reject", "--status", "--library-sync"):
        if f in argv:
            return f.lstrip("-")
    return "render"


def main(picks, thumb=None, title=None, sfx=None, music=None, argv=None, meta=None):
    """Bọc quy trình chuẩn: thêm --check-art/--check-transitions/--check-sync/--metrics và ghi thời gian mỗi bước."""
    sys.path.insert(0, ENGINE)
    import metrics as MX
    argv = sys.argv[1:] if argv is None else argv
    if "--metrics" in argv:
        print(json.dumps(MX.summary(OUT), ensure_ascii=False, indent=1))
        return
    if "--check-art" in argv:
        d = _arg(argv, "--check-art")
        rep = run_check_art(d if d and not d.startswith("--") else None)
        for it in rep["items"]:
            print("%-4s %-12s phủ %.1f%%  %s" % ("OK" if it["pass"] else "LỖI", it["name"], 100 * it["coverage"],
                                               "; ".join(it["errors"] + it["warnings"])))
        for dp in rep["possible_duplicates"]:
            print("  NGHI TRÙNG: %s ~ %s (sai khác %.1f)" % (dp["a"], dp["b"], dp["mean_diff"]))
        print(json.dumps({"pass": rep["pass"], "images": rep["images"], "overlays": rep["qa_dir"]}, ensure_ascii=False))
        return
    if "--script-review" in argv:
        return run_script_review(argv, meta)
    if "--art-auto" in argv:
        return run_art_auto(argv)
    if "--check-transitions" in argv or "--check-sync" in argv:
        tr, sy = run_check_timing()
        print(json.dumps({"transitions": tr, "sync": {k: sy[k] for k in ("total_s", "errors", "warnings", "pass")}},
                         ensure_ascii=False, indent=1))
        return
    step, t0, status = _step_name(argv), time.time(), "ok"
    try:
        return _main_impl(picks, thumb=thumb, title=title, sfx=sfx, music=music, argv=argv, meta=meta)
    except SystemExit as e:
        status = "blocked" if e.code not in (None, 0) else "ok"
        raise
    except Exception:
        status = "error"
        raise
    finally:
        if step not in ("status",):
            MX.record(OUT, step, time.time() - t0, status=status)


# ================= bổ sung cho các tập 3–5 =================
RED = (232, 96, 96)


def anticip(t, t0, d=0.18):
    """Nhún lấy đà trước khi bật: trả (sx, sy). Dùng ngay trước một cú nhảy tại t0+d."""
    if not (t0 <= t < t0 + d):
        return 1.0, 1.0
    k = math.sin(math.pi * (t - t0) / d)
    return 1 + 0.08 * k, 1 - 0.1 * k


def anger(dst, t, x, y, s=1.0, a=1.0):
    """Dấu giận: hai 'gân' đỏ nhấp nháy + làn hơi bốc lên."""
    if a <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    pulse = 1 + 0.15 * math.sin(t * 14)
    r = 26 * s * pulse
    for dx, dy in ((-r * 0.55, -r * 0.55), (r * 0.55, -r * 0.55), (-r * 0.55, r * 0.55), (r * 0.55, r * 0.55)):
        cx, cy = x + dx, y + dy
        d.arc((cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6), 0, 360, fill=RED + (int(255 * a),), width=int(7 * s))
    for i in range(3):
        ph = (t * 0.9 + i / 3) % 1.0
        px = x - 120 * s + i * 120 * s + 14 * math.sin(t * 3 + i)
        py = y + 60 * s - 160 * ph * s
        rr = (18 + 22 * ph) * s
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(255, 255, 255, int(170 * a * (1 - ph))), outline=(230, 200, 200, int(200 * a * (1 - ph))), width=3)
    dst.alpha_composite(lay)


def red_aura(dst, t, x, y, w, h, a=1.0):
    """Quầng đỏ mềm sau lưng nhân vật (đang giận)."""
    if a <= 0:
        return
    k = ("aura", int(w), int(h))
    if k not in _bg:
        m = Image.new("RGBA", (int(w) + 160, int(h) + 160), (0, 0, 0, 0))
        ImageDraw.Draw(m).ellipse((80, 80, w + 80, h + 80), fill=(255, 120, 120, 90))
        _bg[k] = m.filter(ImageFilter.GaussianBlur(40))
    im = _bg[k]
    put(dst, im, x, y, s=1 + 0.04 * math.sin(t * 6), alpha=a)


_signbox = {}


def sign_box(aid):
    """Tìm vùng bảng trắng trong sprite cầm bảng (theo pixel sáng ở giữa)."""
    if aid not in _signbox:
        r = np.asarray(raw(aid)).astype(int)
        hh, ww = r.shape[:2]
        bright = (r[..., 0] > 225) & (r[..., 1] > 220) & (r[..., 2] > 205) & (r[..., 3] > 200)
        bright[: int(hh * 0.3)] = False
        bright[int(hh * 0.78):] = False
        ys, xs = np.nonzero(bright)
        _signbox[aid] = (xs.min() / ww, ys.min() / hh, xs.max() / ww, ys.max() / hh)
    return _signbox[aid]


def place_sign(dst, aid, x, y, h, text, t=0.0, flip_t=None, text2=None, scene=None, size=40):
    """Nhân vật cầm bảng; chữ trên bảng có thể lật (co ngang về 0 rồi mở ra) tại flip_t."""
    place(dst, aid, x, y, h=h, sy=breathe(t, amp=0.01), scene=scene)
    r = raw(aid)
    k = h / r.height
    bx0, by0, bx1, by1 = sign_box(aid)
    sw, sh = (bx1 - bx0) * r.width * k, (by1 - by0) * r.height * k * breathe(t, amp=0.01)
    cx = x - r.width * k / 2 + (bx0 + bx1) / 2 * r.width * k
    cy = y - r.height * k * breathe(t, amp=0.01) + (by0 + by1) / 2 * r.height * k * breathe(t, amp=0.01)
    cur, sx = text, 1.0
    if flip_t is not None and t >= flip_t:
        p = prog(t, flip_t, 0.3)
        sx = abs(math.cos(math.pi * p))
        cur = text if p < 0.5 else (text2 or text)
    ti = text_img(cur, size, CH, "ExtraBold")
    fit = min(1.0, (sw * 0.86) / ti.width, (sh * 0.8) / ti.height)
    im = ti.resize((max(1, int(ti.width * fit * max(0.02, sx))), max(1, int(ti.height * fit))), Image.BICUBIC)
    paste(dst, im, cx - im.width / 2, cy - im.height / 2)


def translate_chip(dst, t, t0, text, cy=420, bg=BUTTER):
    """Chip 'PHIÊN DỊCH' rơi xuống, nảy và lắc nhẹ."""
    if t < t0:
        return
    s = pop_in(t, t0)
    put(dst, pill(text, 54, bg, CH, CH, padx=36, pady=20), W / 2, cy, s=s, rot=-2 + sway(t, 0, 1.2, 2.0))
    put(dst, pill("PHIÊN DỊCH", 30, CH, CREAM, CH, padx=22, pady=10), W / 2 - 150, cy - 78, s=s, rot=-5)


def stamp_x(dst, t, t0, cx, cy, size=150):
    """Dấu X đỏ đóng lên thẻ."""
    if t < t0:
        return
    p = prog(t, t0, 0.16)
    s = 1.6 - 0.6 * e_out(p)
    lay = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.line((20, 20, size + 20, size + 20), fill=RED, width=26)
    d.line((size + 20, 20, 20, size + 20), fill=RED, width=26)
    put(dst, lay, cx, cy, s=s, alpha=0.3 + 0.7 * p, rot=-8)


def food_card(kind, label):
    """Thẻ món ăn vẽ tay: pho / buncha / pizza / mi."""
    k = ("food", kind, label)
    if k in _bg:
        return _bg[k]
    im = Image.new("RGBA", (420, 470), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 18, 410, 460), radius=40, fill=(230, 190, 180))
    d.rounded_rectangle((10, 8, 410, 450), radius=40, fill=WHITE, outline=CH, width=6)
    cx, cy = 210, 190
    if kind in ("pho", "buncha", "mi"):
        d.chord((cx - 140, cy - 60, cx + 140, cy + 130), 0, 180, fill=(250, 230, 210), outline=CH, width=6)
        d.ellipse((cx - 140, cy - 40, cx + 140, cy + 40), fill=(245, 214, 160) if kind != "buncha" else (210, 150, 100), outline=CH, width=6)
        if kind in ("pho", "mi"):
            for i in range(-3, 4):
                d.arc((cx + i * 30 - 30, cy - 25, cx + i * 30 + 30, cy + 25), 200, 340, fill=(255, 250, 230), width=5)
        if kind == "pho":
            d.ellipse((cx - 60, cy - 18, cx - 10, cy + 8), fill=(200, 120, 110), outline=CH, width=3)
            d.ellipse((cx + 30, cy - 14, cx + 70, cy + 10), fill=(140, 200, 120), outline=CH, width=3)
        if kind == "buncha":
            for ox in (-70, -10, 50):
                d.ellipse((cx + ox - 26, cy - 20, cx + ox + 26, cy + 16), fill=(150, 90, 60), outline=CH, width=3)
        if kind == "mi":
            d.ellipse((cx - 30, cy - 20, cx + 30, cy + 20), fill=WHITE, outline=CH, width=3)
            d.ellipse((cx - 12, cy - 10, cx + 12, cy + 10), fill=BUTTER)
        for i in range(3):
            x = cx - 60 + i * 60
            d.arc((x - 16, cy - 140, x + 16, cy - 70), 90, 270, fill=(190, 170, 170), width=5)
    elif kind == "pizza":
        d.polygon([(cx, cy + 120), (cx - 140, cy - 90), (cx + 140, cy - 90)], fill=(255, 210, 120), outline=CH)
        d.line([(cx, cy + 120), (cx - 140, cy - 90), (cx + 140, cy - 90), (cx, cy + 120)], fill=CH, width=6)
        d.rounded_rectangle((cx - 150, cy - 110, cx + 150, cy - 74), radius=18, fill=(230, 160, 90), outline=CH, width=5)
        for ox, oy in ((-50, -40), (30, -30), (-10, 30), (50, -60)):
            d.ellipse((cx + ox - 18, cy + oy - 18, cx + ox + 18, cy + oy + 18), fill=(210, 80, 70), outline=CH, width=3)
    ti = text_img(label, 54, CH, "ExtraBold")
    im.alpha_composite(ti, (210 - ti.width // 2, 370 - ti.height // 2))
    _bg[k] = im
    return im


def clock_img(hh, mm, ring=0.0):
    im = Image.new("RGBA", (360, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for bx in (70, 290):
        d.ellipse((bx - 46, 10, bx + 46, 90), fill=BUTTER, outline=CH, width=6)
    d.line((90, 360, 60, 395), fill=CH, width=10)
    d.line((270, 360, 300, 395), fill=CH, width=10)
    d.ellipse((30, 40, 330, 370), fill=(255, 196, 196), outline=CH, width=8)
    d.ellipse((58, 70, 302, 340), fill=WHITE, outline=CH, width=5)
    cx, cy = 180, 205
    for i in range(12):
        a = math.pi * 2 * i / 12
        d.ellipse((cx + 100 * math.sin(a) - 5, cy - 100 * math.cos(a) - 5, cx + 100 * math.sin(a) + 5, cy - 100 * math.cos(a) + 5), fill=CH)
    am = math.pi * 2 * mm / 60
    ah = math.pi * 2 * ((hh % 12) + mm / 60) / 12
    d.line((cx, cy, cx + 85 * math.sin(am), cy - 85 * math.cos(am)), fill=CH, width=7)
    d.line((cx, cy, cx + 55 * math.sin(ah), cy - 55 * math.cos(ah)), fill=CH, width=11)
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=RED)
    return im


def ring_lines(dst, t, cx, cy, r=230):
    d = ImageDraw.Draw(dst)
    for side in (-1, 1):
        for i in range(3):
            a0 = -0.5 + i * 0.5
            L = 36 + 10 * math.sin(t * 40 + i)
            x0 = cx + side * (r + 10) * math.cos(a0)
            y0 = cy + (r * 0.6) * math.sin(a0)
            d.line((x0, y0, x0 + side * L * math.cos(a0), y0 + L * math.sin(a0)), fill=CH, width=8)


def bedroom():
    if "bedroom" in _bg:
        return _bg["bedroom"]
    im = Image.new("RGBA", (W, H), LAV + (255,))
    d = ImageDraw.Draw(im)
    for x in range(40, W, 120):
        for y in range(80, 1250, 130):
            star(d, x + (60 if (y // 130) % 2 else 0), y, 10, (246, 240, 255))
    d.rectangle((0, 1300, W, H), fill=(232, 212, 236))
    d.line((0, 1300, W, 1300), fill=CH, width=6)
    d.rounded_rectangle((640, 230, 960, 600), radius=24, fill=(255, 236, 200), outline=CH, width=7)
    d.line((800, 230, 800, 600), fill=CH, width=6)
    d.ellipse((820, 260, 900, 340), fill=(255, 210, 120))
    # giường
    d.rounded_rectangle((90, 860, 990, 1000), radius=40, fill=(205, 190, 235), outline=CH, width=7)
    d.rounded_rectangle((70, 980, 1010, 1260), radius=50, fill=(250, 250, 255), outline=CH, width=7)
    d.rounded_rectangle((70, 1080, 1010, 1260), radius=50, fill=(180, 210, 240), outline=CH, width=7)
    for x in range(140, 1000, 120):
        d.ellipse((x - 12, 1150, x + 12, 1174), fill=(220, 236, 250))
    d.rectangle((110, 1260, 140, 1300), fill=CH)
    d.rectangle((940, 1260, 970, 1300), fill=CH)
    d.rounded_rectangle((150, 930, 420, 1040), radius=45, fill=WHITE, outline=CH, width=6)
    _bg["bedroom"] = im
    return im


def kitchen():
    if "kitchen" in _bg:
        return _bg["kitchen"]
    im = Image.new("RGBA", (W, H), MINT + (255,))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 120):
        for y in range(0, 1300, 120):
            d.rectangle((x + 4, y + 4, x + 116, y + 116), outline=(190, 225, 210), width=3)
    d.rectangle((0, 1300, W, H), fill=WOOD)
    d.line((0, 1300, W, 1300), fill=CH, width=6)
    d.rounded_rectangle((60, 980, 1020, 1300), radius=20, fill=(255, 238, 220), outline=CH, width=7)
    d.rectangle((60, 960, 1020, 1000), fill=(240, 200, 170), outline=CH, width=6)
    for x in (300, 780):
        d.ellipse((x - 14, 1120, x + 14, 1148), fill=CH)
    d.rounded_rectangle((120, 260, 460, 560), radius=20, fill=SKYB, outline=CH, width=7)
    d.line((290, 260, 290, 560), fill=CH, width=6)
    for i, x in enumerate((640, 760, 880)):
        d.line((x, 200, x, 330), fill=CH, width=4)
        d.ellipse((x - 40, 330, x + 40, 410), fill=[BUTTER, PINK2, LAV][i], outline=CH, width=5)
    _bg["kitchen"] = im
    return im


def mi_bowl(full=True):
    im = Image.new("RGBA", (220, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.chord((10, -40, 210, 110), 0, 180, fill=(255, 190, 200), outline=CH, width=6)
    d.ellipse((10, 20, 210, 60), fill=(200, 140, 90) if full else (240, 220, 210), outline=CH, width=5)
    if full:
        for ox in (50, 90, 130, 165):
            d.ellipse((ox - 10, 30, ox + 10, 46), fill=(150, 95, 60))
    t = text_img("MIMI", 24, CH, "ExtraBold")
    im.alpha_composite(t, (110 - t.width // 2, 70))
    return im


# ================= màn hình chia đôi (so sánh A vs B) =================
PANEL_W, PANEL_H, PANEL_FLOOR = 1008, 600, 560
PANEL_POS = ((36, 250), (36, 872))
PANEL_ZOOM_MAX = 1.08   # mức đẩy máy tối đa vào một khung chia đôi mà bố cục nền tảng phải chừa chỗ
_pmask = None


def outdoor():
    """Ngoài phố pastel: trời, mây, nhà, cây, vỉa hè."""
    if "outdoor" in _bg:
        return _bg["outdoor"]
    im = Image.new("RGBA", (W, H), SKYB + (255,))
    d = ImageDraw.Draw(im)
    for cx, cy in ((220, 380), (760, 300), (520, 520)):
        for ox, r in ((-50, 46), (0, 62), (52, 44)):
            d.ellipse((cx + ox - r, cy - r, cx + ox + r, cy + r), fill=WHITE)
    d.ellipse((860, 140, 980, 260), fill=BUTTER, outline=CH, width=5)
    for i, (x, w, h, col) in enumerate(((40, 220, 520, PINK), (290, 200, 640, LAV), (520, 240, 460, MINT), (790, 230, 580, PEACH))):
        d.rounded_rectangle((x, 1300 - h, x + w, 1300), radius=18, fill=col, outline=CH, width=6)
        for yy in range(1300 - h + 50, 1240, 110):
            for xx in (x + 40, x + w - 90):
                d.rounded_rectangle((xx, yy, xx + 50, yy + 60), radius=8, fill=(255, 250, 230), outline=CH, width=4)
    d.rectangle((0, 1300, W, H), fill=(226, 222, 230))
    d.line((0, 1300, W, 1300), fill=CH, width=6)
    for x in range(0, W, 140):
        d.line((x, 1300, x - 60, H), fill=(200, 196, 210), width=4)
    for x in (140, 900):
        d.rectangle((x - 12, 1120, x + 12, 1300), fill=(170, 120, 90), outline=CH, width=4)
        d.ellipse((x - 90, 960, x + 90, 1150), fill=(150, 200, 150), outline=CH, width=6)
    _bg["outdoor"] = im
    return im


def _panel_bg(name):
    k = ("pbg", name)
    if k not in _bg:
        src = {"room": room, "kitchen": kitchen, "bedroom": bedroom, "outdoor": outdoor}[name]()
        _bg[k] = src.crop((0, 760, 1080, 760 + 643)).resize((PANEL_W, PANEL_H), Image.LANCZOS)
    return _bg[k]


def split_frame(t, top, bottom, label_top, label_bot, bg_top="room", bg_bot="outdoor", base=CREAM, slide=None,
                active=None):
    """top/bottom: hàm(canvas, t) vẽ trong khung PANEL (sàn ở y=PANEL_FLOOR). active: 0/1 làm nổi khung đang nói."""
    global _pmask
    if _pmask is None:
        _pmask = Image.new("L", (PANEL_W, PANEL_H), 0)
        ImageDraw.Draw(_pmask).rounded_rectangle((0, 0, PANEL_W - 1, PANEL_H - 1), radius=40, fill=255)
    im = Image.new("RGBA", (W, H), base + (255,))
    bokeh(im, t, WHITE, 90)
    for i, (fn, lab, bgn) in enumerate(((top, label_top, bg_top), (bottom, label_bot, bg_bot))):
        c = _panel_bg(bgn).copy()
        fn(c, t)
        lay = Image.new("RGBA", (PANEL_W, PANEL_H), (0, 0, 0, 0))
        lay.paste(c, (0, 0), _pmask)
        dd = ImageDraw.Draw(lay)
        hl = active == i
        dd.rounded_rectangle((3, 3, PANEL_W - 4, PANEL_H - 4), radius=40, outline=(PINK2 if hl else CH), width=10 if hl else 6)
        dx = 0
        if slide is not None:
            p = e_out(prog(t, slide + 0.08 * i, 0.4))
            dx = (-1 if i == 0 else 1) * W * (1 - p)
        pos, k = panel_layout()
        x, y = pos[i]
        s = (1.0 + (0.012 if hl else 0.0)) * k
        put(im, lay, x + PANEL_W * k / 2 + dx, y + PANEL_H * k / 2, s=s)
        put(im, pill(lab, 40, [BUTTER, LAV][i], CH, CH, padx=26, pady=12), x + (40 + 130) * k + dx, y + 8 * k,
            s=pop_in(t, (slide or 0) + 0.3) * max(0.85, k), rot=-3)
    return im


def panel_layout():
    """Vị trí 2 khung chia đôi: thu nhỏ để cả hai khung nằm trong vùng nội dung (trên tray_top()), kể cả khi đẩy máy
    tới PANEL_ZOOM_MAX. Áp dụng cho bản gốc lẫn bản nền tảng (Owner 08/11/2026: nội dung 3/4 trên, phụ đề 1/4 dưới)."""
    top, gap = 170, 22
    # chừa chỗ cho máy đẩy vào khung trên (zoom ≤ PANEL_ZOOM_MAX, cam() kẹp mép trên → y nhân z): khung dưới không trượt vào phụ đề
    k = min(1.0, ((tray_top() - 12) / PANEL_ZOOM_MAX - top) / (2 * PANEL_H + gap))
    x = (W - PANEL_W * k) / 2
    return ((x, top), (x, top + (PANEL_H + gap) * k)), k


def panel_center(i):
    """Tâm khung chia đôi i (0 trên, 1 dưới) theo bố cục hiện hành."""
    pos, k = panel_layout()
    return pos[i][0] + PANEL_W * k / 2, pos[i][1] + PANEL_H * k / 2


def p_place(c, aid, x, h, t, ph=0.0, a=0.0, scene=None, **kw):
    """Đặt nhân vật trong khung split (giữa-đáy tại sàn khung)."""
    place(c, aid, x, PANEL_FLOOR - 8 * a, h=h, sy=breathe(t, ph) * (1 + 0.02 * a), rot=kw.pop("rot", sway(t, ph, 1.0, 2.4)),
          scene=scene, **kw)
