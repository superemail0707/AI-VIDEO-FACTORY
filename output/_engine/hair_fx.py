"""Hiệu ứng tóc cho sprite đã duyệt. Dùng Pillow + numpy (miễn phí, chạy local).

bedhead(): tóc rối "mới ngủ dậy" theo mẫu thư viện NGANG_DAILY_001 (messy_hair, Owner đã duyệt hình):
  - tóc PHỒNG to ra hai bên và đỉnh, không đều, một bên xẹp hơn (bên nằm gối);
  - vài sợi mảnh dựng lên trên đỉnh, có sợi cong vòng như ăng-ten;
  - lông tơ xù ngắn dọc viền ngoài; vài lọn rời ở hai bên.
Không dùng chỏm nhọn hình tam giác (bản cũ bị Owner nhận xét "chưa chân thực").
Ảnh trả về ở độ phân giải x ss, có lề trên/hai bên để sợi tóc không bị cắt; số px lề trên ghi ở thuộc tính
`pad_top_px` của kết quả để engine giữ đúng chiều cao thân nhân vật."""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HAIR_FILL = (58, 42, 38, 255)
HAIR_MID = (78, 58, 50, 255)
HAIR_LINE = (34, 25, 23, 255)


def _hair_mask(a):
    al = a[..., 3]
    return (al > 200) & (a[..., 0] < 110) & (a[..., 1] < 90) & (a[..., 2] < 85)


def _taper(d, pts, w0, w1, col):
    n = len(pts) - 1
    for i in range(n):
        w = w0 + (w1 - w0) * i / max(1, n - 1)
        d.line([pts[i], pts[i + 1]], fill=col, width=max(1, int(round(w))))


def _curve(p0, ang, L, bend, curl=0.0, n=24):
    """Đường cong mềm đi ra theo góc ang, uốn dần (bend) và có thể cuộn lại ở cuối (curl)."""
    pts, x, y, a = [p0], p0[0], p0[1], ang
    step = L / n
    for i in range(n):
        a += bend / n + curl * (i / n) ** 2 / n * 6
        x += step * math.cos(a)
        y += step * math.sin(a)
        pts.append((x, y))
    return pts


def _lock_poly(pts, w0, w1=0.0):
    """Đa giác một lọn tóc thon dần theo đường tâm pts."""
    L, R = [], []
    n = len(pts)
    for i, (x, y) in enumerate(pts):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        dx, dy = pts[j1][0] - pts[j0][0], pts[j1][1] - pts[j0][1]
        nn = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / nn, dx / nn
        t = i / (n - 1)
        w = w1 + (w0 - w1) * (1 - t) ** 0.8
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    return L + R[::-1]


def bedhead(im, seed=7, ss=3, chin_frac=0.42, volume=1.0, flat_side=+1, locks=24, flyaways=7, strands=12):
    """Tóc rối mới ngủ dậy: các LỌN tóc dày, uốn, bung ra ngoài (không phải mảng phẳng hay chỏm nhọn),
    vài sợi dài dựng trên đỉnh, đường sợi rối bên trong. Một bên xẹp hơn (bên nằm gối)."""
    rnd = random.Random(seed)
    k = ss * im.width / 200.0
    pad = int(42 * k)
    big = im.resize((im.width * ss, im.height * ss), Image.LANCZOS)
    W, H = big.width + 2 * pad, big.height + pad
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(big, (pad, pad))
    a = np.asarray(canvas).astype(int)
    hair = _hair_mask(a)
    lim = int(pad + big.height * chin_frac)
    yy, xx = np.mgrid[0:H, 0:W]
    ys, xs = np.where(hair[:lim])
    if len(xs) == 0:
        canvas.info["pad_top_px"] = pad
        return canvas
    top = ys.min()
    cx, cy = xs.mean(), top + 0.45 * (lim - top)
    solid = a[..., 3] > 200
    other = solid & ~hair                                   # mặt, cổ, áo: không vẽ đè lên
    other_d = np.asarray(Image.fromarray((other * 255).astype("uint8")).filter(ImageFilter.MaxFilter(int(2 * ss) | 1))) > 127
    er = np.asarray(Image.fromarray((hair * 255).astype("uint8")).filter(ImageFilter.MinFilter(3))) > 127
    edge = hair & ~er & (yy < lim)
    ey, ex = np.where(edge)
    pts_edge = [(x, y) for x, y in zip(ex.tolist(), ey.tolist())
                if not other_d[y, x] and 0 <= x < W and 0 <= y < H]
    rnd.shuffle(pts_edge)

    def pick(cond, n, mind):
        got = []
        for x, y in pts_edge:
            g = math.atan2(y - cy, x - cx)
            if cond(g, y) and all((x - gx) ** 2 + (y - gy) ** 2 > mind ** 2 for gx, gy, _ in got):
                got.append((x, y, g))
                if len(got) >= n:
                    break
        return got

    def side_k(g):
        return 1.0 - 0.45 * max(0.0, flat_side * math.cos(g))

    def down_k(y):
        return max(0.35, min(1.0, (lim - y) / max(1.0, lim - top) * 1.5))

    back_o = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    back_f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    do, dfi = ImageDraw.Draw(back_o), ImageDraw.Draw(back_f)
    ow = max(2, int(1.25 * k))
    tex = []
    # 1) LỌN phồng: bắt đầu bên trong mép tóc, uốn ra ngoài
    for x, y, g in pick(lambda g, y: True, locks, 5 * k):
        sk, dk = side_k(g), down_k(y)
        L = rnd.uniform(9, 17) * k * volume * sk * dk * (1.3 if -2.4 < g < -0.7 else 1.0)
        a2 = g + rnd.uniform(-0.45, 0.45)
        start = (x - math.cos(a2) * 9 * k, y - math.sin(a2) * 9 * k)
        cl = _curve(start, a2, L + 9 * k, rnd.choice([-1, 1]) * rnd.uniform(0.6, 1.4),
                    curl=rnd.choice([-1, 1]) * rnd.uniform(0.8, 1.8), n=30)       # đuôi lọn quặp lại như sóng xoăn
        w0 = rnd.uniform(7.0, 11.0) * k * (0.65 + 0.35 * dk)
        poly = _lock_poly(cl, w0, 1.6 * k)
        do.polygon(poly, fill=HAIR_LINE, outline=HAIR_LINE, width=ow * 2)
        dfi.polygon(poly, fill=HAIR_FILL)
        tex.append(cl)
    back = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    back.alpha_composite(back_o)
    back.alpha_composite(back_f)
    db = ImageDraw.Draw(back)
    for cl in tex:                                         # đường sợi giữa lọn cho có khối
        if rnd.random() < 0.7:
            _taper(db, cl[3:-3], 0.9 * k, 0.3 * k, HAIR_LINE if rnd.random() < 0.5 else HAIR_MID)

    # 2) sợi dài dựng trên đỉnh, một số cuộn như ăng-ten (giống mẫu NGANG_DAILY_001)
    fly = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dfl = ImageDraw.Draw(fly)
    for j, (x, y, g) in enumerate(pick(lambda g, y: -2.6 < g < -0.55, flyaways, 10 * k)):
        a2 = g + rnd.uniform(-0.4, 0.4)
        curl = rnd.choice([-1, 1]) * (2.2 if j % 3 == 0 else rnd.uniform(0.3, 0.9))
        cl = _curve((x - math.cos(a2) * 4 * k, y - math.sin(a2) * 4 * k), a2, rnd.uniform(22, 34) * k * side_k(g),
                    rnd.uniform(-1.1, 1.1), curl=curl, n=40)
        _taper(dfl, cl, 2.1 * k, 0.5 * k, HAIR_LINE)

    # 3) lọn rối PHÍA TRƯỚC mép tóc gốc (che đường viền gọn gàng cũ), không đè lên mặt/áo
    front = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fo, ff = ImageDraw.Draw(front), Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dff = ImageDraw.Draw(ff)
    for x, y, g in pick(lambda g, y: -2.8 < g < -0.35, 8, 12 * k):
        a2 = g + rnd.uniform(-0.6, 0.6)
        cl = _curve((x - math.cos(a2) * 10 * k, y - math.sin(a2) * 10 * k), a2, rnd.uniform(14, 20) * k * side_k(g),
                    rnd.choice([-1, 1]) * rnd.uniform(1.0, 1.8), curl=rnd.choice([-1, 1]) * 1.2, n=30)
        poly = _lock_poly(cl, rnd.uniform(4.0, 6.0) * k, 1.0 * k)
        fo.polygon(poly, fill=HAIR_LINE, outline=HAIR_LINE, width=ow * 2)
        dff.polygon(poly, fill=HAIR_MID if rnd.random() < 0.4 else HAIR_FILL)
    front.alpha_composite(ff)
    # 4) đường sợi rối bên trong mái tóc (dài, mảnh, chồng chéo)
    dfr = ImageDraw.Draw(front)
    hy, hx = np.where(hair & (yy < lim) & ~other_d)
    for _ in range(strands if len(hx) else 0):
        i = rnd.randrange(len(hx))
        cl = _curve((hx[i], hy[i]), rnd.uniform(0, 6.28), rnd.uniform(14, 26) * k, rnd.choice([-1, 1]) * rnd.uniform(1.5, 3.2), n=30)
        _taper(dfr, cl, 1.0 * k, 0.3 * k, HAIR_LINE)
    clip = (~other_d).astype("uint8") * 255
    front.putalpha(Image.fromarray(np.minimum(np.asarray(front.getchannel("A")), clip)))
    fly.putalpha(Image.fromarray(np.minimum(np.asarray(fly.getchannel("A")), clip)))

    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(back)
    out.alpha_composite(fly)
    out.alpha_composite(canvas)
    out.alpha_composite(front)
    bb = out.getchannel("A").getbbox()
    out = out.crop((bb[0], bb[1], bb[2], H))
    out.info["pad_top_px"] = max(0, pad - bb[1])
    return out
