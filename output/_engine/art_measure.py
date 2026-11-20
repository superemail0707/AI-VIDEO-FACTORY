"""Tấm QA đo tranh 9:16 độ phân giải thấp (Owner 19/11/2026: giảm token khâu tranh).

    python3 output/_engine/art_measure.py <thư mục tập> [A01,A02,...] [--write]

Thay cho 3–4 lượt xem ảnh lớn: một lệnh dựng `art/v01/_qa/measure_sheet*.jpg` (8 tranh/tấm, ¼ độ phân giải, thước
120 px có số, lề mặt 108/972, dải phụ đề 1480–1680, khung chú thích hiện có nếu đã có) — Claude xem MỘT tấm, đọc số theo
thước rồi ghi `safe_annotations.json`. `--write` chỉ thêm khung trống {"subtitles": true} cho tranh chưa có chú thích.

Đã thử đo tự động theo màu da (19/11/2026, EP29): KHÔNG tin cậy — màu da hoạt hình trùng tường/sàn kem → khung sai
hoàn toàn trên 16/16 tranh. Nhận diện mặt thật cần OpenCV + cascade anime (chưa cài, cần Owner cho phép).
"""
import argparse
import glob
import json
import os
import sys

from PIL import Image, ImageDraw, ImageOps

W, H = 1080, 1920


def load(path):
    return ImageOps.fit(Image.open(path).convert('RGB'), (W, H), Image.Resampling.LANCZOS)


def sheet(items, out_path, cols=4, cw=270):
    ch = int(cw * H / W)
    rows = (len(items) + cols - 1) // cols
    sh = Image.new('RGB', (cols * cw, rows * (ch + 18)), 'white')
    d0 = ImageDraw.Draw(sh)
    for i, (name, im, m) in enumerate(items):
        im = im.copy()
        d = ImageDraw.Draw(im)
        for y in range(0, H, 120):
            d.line([0, y, W, y], fill=(255, 0, 0), width=3)
            d.text((6, y + 4), str(y), fill=(255, 0, 0))
        d.line([108, 0, 108, H], fill=(0, 140, 255), width=4)
        d.line([972, 0, 972, H], fill=(0, 140, 255), width=4)
        d.rectangle([0, 1480, W, 1680], outline=(0, 220, 0), width=8)
        if 'face_x' in m and 'head_top_y' in m and 'char_bottom_y' in m:
            d.rectangle([m['face_x'][0], m['head_top_y'], m['face_x'][1], m['char_bottom_y']], outline=(255, 0, 255), width=8)
        x, y = (i % cols) * cw, (i // cols) * (ch + 18)
        sh.paste(im.resize((cw, ch)), (x, y + 18))
        d0.text((x + 4, y + 3), '%s %s' % (name, {k: m[k] for k in ('face_x', 'head_top_y', 'char_bottom_y') if k in m}), fill='black')
    sh.save(out_path, quality=80)
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('ep')
    ap.add_argument('scenes', nargs='?')
    ap.add_argument('--art', default='art/v01')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args(argv)
    art = os.path.join(os.path.abspath(a.ep), a.art)
    names = [s.strip() for s in a.scenes.split(',')] if a.scenes else \
        sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(art, 'A*.png')))
    p = os.path.join(art, 'safe_annotations.json')
    ann = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    items, res = [], {}
    for n in names:
        im = load(os.path.join(art, n + '.png'))
        res[n] = ann.get(n, {})
        items.append((n, im, res[n]))
    os.makedirs(os.path.join(art, '_qa'), exist_ok=True)
    sheets = [sheet(items[i:i + 8], os.path.join(art, '_qa', 'measure_sheet%s.jpg' % ('' if i == 0 else i // 8 + 1)))
              for i in range(0, len(items), 8)]
    if a.write:
        for n in names:
            ann.setdefault(n, {}).setdefault('subtitles', True)
        json.dump(ann, open(p, 'w', encoding='utf-8'), indent=1)
    print(json.dumps({'missing': [n for n in names if 'char_bottom_y' not in res[n]], 'sheets': sheets}, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())
