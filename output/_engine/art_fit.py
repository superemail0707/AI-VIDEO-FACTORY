"""Thu nhỏ tranh vào giữa khung để kéo mặt sát mép / chân sát phụ đề vào vùng an toàn (13/11/2026).

Bài học EP23/EP24: image_gen (ChatGPT web) vẫn đặt Mimi sát mép trái và vẽ cả bàn chân xuống dải phụ đề
dù prompt ghi "central 70%", tạo lại nhiều lần vẫn lệch. Thay vì tạo lại lần 3–4, thu nhỏ tranh theo hệ số s
(neo mép trên, canh giữa ngang), phần lề trống lấp bằng ảnh phản chiếu (mirror) làm mờ nhẹ — lề này nằm trong
vùng cắt TikTok (x < 108 / > 972) và dưới dải phụ đề nên gần như không thấy.

    python3 output/_engine/art_fit.py <thư mục art/v01> A01=0.85 A06=0.9 …

Bản gốc giữ ở _superseded/<CẢNH>_raw.png (chạy lại luôn đọc từ bản gốc, không thu nhỏ chồng).
Hệ số ghi vào art_fit.json. Toạ độ đổi: x' = 540 + (x − 540)·s, y' = y·s → dùng `map_xy` khi ghi safe_annotations.
"""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps

W, H = 1080, 1920


def map_xy(x, y, s):
    return 540 + (x - 540) * s, y * s


def fit(im, s, blur=6):
    """Ảnh 1080×1920: tranh thu nhỏ hệ số s neo mép trên, lề phản chiếu làm mờ."""
    base = ImageOps.fit(im.convert("RGB"), (W, H), Image.Resampling.LANCZOS)
    if s >= 0.999:
        return base
    w, h = round(W * s), round(H * s)
    x0 = (W - w) // 2
    small = base.resize((w, h), Image.Resampling.LANCZOS)
    arr = np.asarray(small)
    # đáy: phản chiếu (sàn/mặt bàn liền mạch); hai bên: kéo dài cột mép (phản chiếu hai bên sinh "mặt ma" ở lề)
    pad = np.pad(arr, ((0, H - h), (0, 0), (0, 0)), mode="symmetric")
    pad = np.pad(pad, ((0, 0), (x0, W - w - x0), (0, 0)), mode="edge")
    padded = Image.fromarray(pad)
    border = np.concatenate([arr[:, :4].reshape(-1, 3), arr[:, -4:].reshape(-1, 3), arr[-4:].reshape(-1, 3)])
    if border.mean() > 235:            # khung nguệch ngoạc nền giấy trắng: lề trắng phẳng, không kéo vệt màu
        out = Image.new("RGB", (W, H), tuple(int(v) for v in np.median(border, axis=0)))
    else:
        out = padded.filter(ImageFilter.GaussianBlur(blur * 2))
        side = padded.filter(ImageFilter.GaussianBlur(blur * 7))   # lề hai bên mờ mạnh: không thấy vệt kéo
        out.paste(side.crop((0, 0, x0, H)), (0, 0))
        out.paste(side.crop((x0 + w, 0, W, H)), (x0 + w, 0))
    out.paste(small, (x0, 0))
    return out


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2:
        raise SystemExit(__doc__)
    d = Path(argv[0])
    sup = d / "_superseded"
    sup.mkdir(exist_ok=True)
    rec_p = d / "art_fit.json"
    rec = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.exists() else {}
    for item in argv[1:]:
        name, s = item.split("=")
        s = float(s)
        if not 0.7 <= s <= 1.0:
            raise SystemExit("hệ số %s ngoài 0.7–1.0" % s)
        raw = sup / (name + "_raw.png")
        if not raw.exists():
            shutil.copy2(d / (name + ".png"), raw)
        fit(Image.open(raw), s).save(d / (name + ".png"))
        rec[name] = s
        print("%s: s=%.2f" % (name, s))
    rec_p.write_text(json.dumps(rec, indent=1, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()


def fit_wide(raw, s2=1.0, blur=9):
    """Bài học EP26 (18/11/2026): tranh ChatGPT khổ 2:3 (1024×1536) — KHÔNG cắt hai bên rồi thu nhỏ (lề kéo giãn thành vệt).
    Giữ nguyên bề ngang: resize 1080×1620, đáy 300 px = phản chiếu sàn làm mờ, nhạt dần về màu sàn; rồi mới thu thêm s2
    (thường ≥ 0,94) nếu mặt còn sát lề. Toạ độ từ khung cover-fit (x_c, y_c): x_w = (x_c + 100)·0,84375, y_w = y_c·0,84375;
    sau s2: x' = 540 + (x_w − 540)·s2, y' = y_w·s2."""
    w0, h0 = raw.size
    hh = round(W * h0 / w0)
    a = np.asarray(raw.convert("RGB").resize((W, hh), Image.Resampling.LANCZOS))
    img = Image.fromarray(np.pad(a, ((0, max(0, H - hh)), (0, 0), (0, 0)), mode="symmetric")[:H])
    if hh < H:
        band = img.crop((0, hh, W, H)).filter(ImageFilter.GaussianBlur(blur))
        floor = np.asarray(img.crop((0, hh - 60, W, hh))).reshape(-1, 3).mean(0)
        b = np.asarray(band).astype(float)
        g = np.linspace(0.25, 0.75, b.shape[0])[:, None, None]
        img.paste(Image.fromarray((b * (1 - g) + floor * g).clip(0, 255).astype("uint8")), (0, hh))
        img.paste(img.crop((0, hh - 20, W, hh + 20)).filter(ImageFilter.GaussianBlur(3)), (0, hh - 20))
    if s2 < 0.999:
        w, h = round(W * s2), round(H * s2)
        x0 = (W - w) // 2
        small = np.asarray(img.resize((w, h), Image.Resampling.LANCZOS))
        img = Image.fromarray(np.pad(small, ((0, H - h), (x0, W - w - x0), (0, 0)), mode="edge"))
    return img


def fit_down(raw, s=0.86, blur=14):
    """Bài học EP27 (19/11/2026): tranh ChatGPT 9:16 đặt nhân vật thấp và rộng (chân vào dải phụ đề, mặt sát lề).
    Cover-fit 1080×1920 rồi thu s, neo MÉP TRÊN + giữa ngang; hai bên và đáy lấp bằng phản chiếu làm mờ (không kéo giãn).
    Toạ độ: x' = 540 + (x − 540)·s, y' = y·s."""
    from PIL import ImageOps
    base = ImageOps.fit(raw.convert("RGB"), (W, H), Image.Resampling.LANCZOS)
    w, h = round(W * s), round(H * s)
    x0 = (W - w) // 2
    small = np.asarray(base.resize((w, h), Image.Resampling.LANCZOS))
    full = Image.fromarray(np.pad(small, ((0, H - h), (x0, W - w - x0), (0, 0)), mode="symmetric"))
    soft = full.filter(ImageFilter.GaussianBlur(blur))
    mask = Image.new("L", (W, H), 255)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rectangle((x0 + 6, 0, x0 + w - 7, h - 7), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    return Image.composite(soft, full, mask)
