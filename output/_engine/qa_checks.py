"""Quality Gate tự động mới (Giai đoạn A, kế hoạch NMT_PIPELINE_UPGRADE_PLAN) — biến checklist trong IMPROVEMENT_LOG thành kiểm tra máy.

  check_art         : tranh image_gen (EP16, EP17) — tỉ lệ 9:16, độ phủ ≥ 95 %, trùng tranh, đáy nhân vật/đỉnh đầu theo chú thích,
                      ảnh overlay 540×960 lưới 100 px + dải phụ đề 1:1 để kiểm bằng mắt.
  check_transitions : chuyển cảnh (EP13) — vào End card/Outro phải cắt thẳng; kiểu chuyển hợp lệ; thời lượng chuyển ≤ cảnh.
  check_sync        : tiếng/hình (EP19) — câu mở có tiếng thật ≤ 0,20 s; câu không chồng nhau; không vượt cuối video.

Không tuyên bố đo ngữ nghĩa ảnh: vị trí nhân vật lấy từ art/<bản>/safe_annotations.json do người kiểm ghi sau khi xem overlay.
"""
import itertools
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1920
COVER_MIN = 0.95
CONTENT_BOTTOM, HEAD_MIN_Y, SUB_TOP, SUB_BOTTOM, CROP_X = 1460, 240, 1480, 1680, 108
TRANSITIONS = {"cut", "fade", "whip", "flash", "black_in", "iris"}
OUTRO_WORDS = ("end card", "outro")
OPEN_MAX = 0.20       # câu mở video: tiếng thật phải bắt đầu trước mốc này (s). Hiệu chỉnh: EP19 đã duyệt = 0,16 s (đầu file 0,05 + onset 0,11)
LEAD_WARN = 0.6       # hình đi trước tiếng quá mức này ở đầu cảnh có thoại -> cảnh báo
FACE_X_MIN, FACE_X_MAX = 108, 972   # bài học EP20: mặt nhân vật trong vùng không bị cắt
DUP_DIFF = 20.0       # nghi trùng tranh. Hiệu chỉnh EP17: F07 v01 lặp F06 = 11,7; tranh khác cảnh ≥ 47


# ------------------------------------------------------------------ tranh
def _flat_run(arr, axis_rows, from_end):
    """Số hàng/cột liên tiếp từ mép là viền phẳng sáng hoặc trong suốt (khung bo/nền kem thừa)."""
    lines = arr if axis_rows else arr.transpose(1, 0, 2)
    rng = range(len(lines) - 1, -1, -1) if from_end else range(len(lines))
    n = 0
    for i in rng:
        ln = lines[i]
        rgb, a = ln[:, :3].astype(np.float32), ln[:, 3]
        transparent = (a < 10).mean() > 0.9
        flat_light = rgb.std(axis=0).max() < 4 and rgb.mean() > 225   # phẳng theo từng kênh (nền kem không xám)
        if transparent or flat_light:
            n += 1
        else:
            break
    return n


def coverage(im):
    """Tỉ lệ khung 1080×1920 có hình thật sau khi fit (bỏ viền phẳng sáng/trong suốt ở 4 mép)."""
    arr = np.asarray(im.convert("RGBA"))
    t, b = _flat_run(arr, True, False), _flat_run(arr, True, True)
    l, r = _flat_run(arr, False, False), _flat_run(arr, False, True)
    return max(0, W - l - r) * max(0, H - t - b) / float(W * H), {"top": t, "bottom": b, "left": l, "right": r}


def _font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def overlay(im, name, ann=None):
    """Ảnh kiểm 540×960: lưới 100 px (toạ độ khung 1080×1920), vạch vùng an toàn, nhãn toạ độ."""
    o = im.convert("RGB").copy()
    d = ImageDraw.Draw(o, "RGBA")
    f = _font(26)
    for y in range(100, H, 100):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 70), width=2)
        d.text((6, y - 30), str(y), fill=(255, 255, 255, 230), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
    for x in range(100, W, 100):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 50), width=2)
    d.rectangle([CROP_X, SUB_TOP, W - CROP_X, SUB_BOTTOM], fill=(255, 0, 0, 55), outline=(255, 40, 40, 255), width=5)
    for y, col in ((200, (0, 200, 255)), (HEAD_MIN_Y, (0, 255, 120)), (CONTENT_BOTTOM, (255, 200, 0))):
        d.line([(0, y), (W, y)], fill=col + (255,), width=5)
    for x in (CROP_X, W - CROP_X):
        d.line([(x, 0), (x, H)], fill=(255, 0, 255, 200), width=4)
    if ann:
        for k, col in (("char_bottom_y", (255, 120, 0)), ("head_top_y", (0, 255, 120))):
            if isinstance(ann.get(k), (int, float)):
                d.line([(0, ann[k]), (W, ann[k])], fill=col + (255,), width=9)
    d.text((14, 14), name, fill=(255, 255, 0, 255), font=_font(44), stroke_width=3, stroke_fill=(0, 0, 0))
    return o.resize((540, 960), Image.Resampling.LANCZOS)


def list_art(art_dir):
    return sorted(f for f in os.listdir(art_dir)
                  if f.lower().endswith(".png") and not f.startswith("_") and "superseded" not in f.lower())


def check_art(art_dir, report_path=None, qa_dir=None, need_annotations=True):
    """Kiểm mọi tranh trong art_dir. Trả dict báo cáo; 'pass' False nếu có lỗi chặn."""
    qa_dir = qa_dir or os.path.join(art_dir, "_qa")
    os.makedirs(qa_dir, exist_ok=True)
    ann_path = os.path.join(art_dir, "safe_annotations.json")
    anns = json.load(open(ann_path, encoding="utf-8")) if os.path.exists(ann_path) else {}
    items, thumbs = [], {}
    for fn in list_art(art_dir):
        name = fn[:-4]
        src = Image.open(os.path.join(art_dir, fn))
        sw, sh = src.size
        fit = ImageOps.fit(src.convert("RGBA"), (W, H), Image.Resampling.LANCZOS)
        cov, margins = coverage(fit)
        ratio = sw / float(sh)
        crop_loss = 1 - min(ratio, W / H) / max(ratio, W / H)
        ann = anns.get(name)
        errors, warns = [], []
        if cov < COVER_MIN:
            # Khung nguệch ngoạc (BRAND_NMT): nền giấy trắng là chủ đích — người kiểm ghi "paper_bg": "<lý do>" → chỉ cảnh báo
            (warns if (ann or {}).get("paper_bg") else errors).append("độ phủ %.1f%% < 95%% (viền phẳng %s)" % (100 * cov, margins))
        if crop_loss > 0.12:
            warns.append("tỉ lệ gốc %dx%d lệch 9:16, fit cắt mất %.0f%%" % (sw, sh, 100 * crop_loss))
        if sw < 720 or sh < 1280:
            warns.append("độ phân giải thấp %dx%d" % (sw, sh))
        if ann is None:
            (errors if need_annotations else warns).append(
                "chưa có chú thích vị trí nhân vật trong safe_annotations.json (xem _qa/%s_overlay.jpg)" % name)
        else:
            if ann.get("subtitles", True) and isinstance(ann.get("char_bottom_y"), (int, float)) \
                    and ann["char_bottom_y"] > CONTENT_BOTTOM:
                errors.append("đáy nhân vật y=%d > %d nhưng tranh có phụ đề (đè dải 1480–1680)"
                              % (ann["char_bottom_y"], CONTENT_BOTTOM))
            if isinstance(ann.get("head_top_y"), (int, float)) and ann["head_top_y"] < HEAD_MIN_Y:
                warns.append("đỉnh đầu y=%d < %d (sát thanh trạng thái)" % (ann["head_top_y"], HEAD_MIN_Y))
            # Bài học EP20: image_gen đặt nhân vật sát mép phải/trái dù prompt ghi "central 80%" → mặt vào lề cắt TikTok
            fx = ann.get("face_x")
            if isinstance(fx, (list, tuple)) and len(fx) == 2:
                if fx[0] < FACE_X_MIN or fx[1] > FACE_X_MAX:
                    errors.append("mặt nhân vật x=%d–%d ra ngoài %d–%d (lề cắt TikTok/Shorts, cột nút phải)"
                                  % (fx[0], fx[1], FACE_X_MIN, FACE_X_MAX))
            elif ann.get("char_bottom_y") is not None:
                warns.append("chưa ghi face_x [x trái, x phải] của các mặt nhân vật (bài học EP20)")
        overlay(fit, name, ann).save(os.path.join(qa_dir, name + "_overlay.jpg"), quality=88)
        fit.convert("RGB").crop((0, SUB_TOP - 100, W, SUB_BOTTOM + 40)).save(
            os.path.join(qa_dir, name + "_band.jpg"), quality=90)
        thumbs[name] = np.asarray(fit.convert("L").resize((108, 192)), dtype=np.float32)
        items.append({"name": name, "source_size": [sw, sh], "coverage": round(cov, 4), "margins": margins,
                      "crop_loss": round(crop_loss, 3), "annotation": ann, "errors": errors, "warnings": warns,
                      "pass": not errors})
    dups = []
    for a, b in itertools.combinations(thumbs, 2):
        diff = float(np.abs(thumbs[a] - thumbs[b]).mean())
        if diff < DUP_DIFF:
            dups.append({"a": a, "b": b, "mean_diff": round(diff, 2)})
    rep = {"art_dir": os.path.abspath(art_dir), "images": len(items), "items": items, "possible_duplicates": dups,
           "rules": {"coverage_min": COVER_MIN, "content_bottom": CONTENT_BOTTOM, "head_min_y": HEAD_MIN_Y,
                     "subtitle_band": [SUB_TOP, SUB_BOTTOM], "dup_mean_diff": DUP_DIFF},
           "qa_dir": os.path.abspath(qa_dir), "pass": bool(items) and all(i["pass"] for i in items)}
    if report_path:
        with open(report_path, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
    return rep


# ------------------------------------------------------------------ chuyển cảnh
def check_transitions(scenes):
    """scenes: [(sid, dur, title, transition, trans_dur)] như E.SCENES."""
    errors, warns = [], []
    for i, (sid, dur, title, tr, td) in enumerate(scenes):
        if tr not in TRANSITIONS:
            errors.append("%s: kiểu chuyển '%s' không hợp lệ (frame() sẽ bỏ qua)" % (sid, tr))
            continue
        if i == 0:
            if tr != "cut":
                warns.append("%s: cảnh đầu không có cảnh trước, '%s' không có tác dụng" % (sid, tr))
            continue
        if tr != "cut" and td <= 0:
            errors.append("%s: chuyển '%s' nhưng thời lượng chuyển = %s" % (sid, tr, td))
        if tr != "cut" and (td > dur or td > scenes[i - 1][1]):
            errors.append("%s: thời lượng chuyển %.2f s dài hơn cảnh (%.2f / %.2f s)" % (sid, td, dur, scenes[i - 1][1]))
        if any(w in str(title).lower() for w in OUTRO_WORDS) and tr != "cut":
            errors.append("%s (%s): vào outro bằng '%s' — phải 'cut' để không lồng hai hình (bài học EP13)" % (sid, title, tr))
    return {"scenes": len(scenes), "errors": errors, "warnings": warns, "pass": not errors}


# ------------------------------------------------------------------ tiếng / hình
def check_sync(scenes, voice, starts, vdur, onset):
    """voice: [(vid, sid, lt, speaker, text)]; starts/vdur: dict; onset(vid) -> giây im lặng đầu file."""
    errors, warns, lines = [], [], []
    total = sum(s[1] for s in scenes)
    for vid, sid, lt, spk, text in voice:
        a = starts[sid] + lt
        on = onset(vid)
        lines.append({"vid": vid, "scene": sid, "file_start": round(a, 3), "speech_start": round(a + on, 3),
                      "end": round(a + vdur.get(vid, 0.0), 3), "onset": round(on, 3)})
    if voice and scenes and voice[0][1] == scenes[0][0]:
        first = lines[0]
        if first["speech_start"] > OPEN_MAX:
            errors.append("câu mở %s: tiếng thật bắt đầu ở %.2f s > %.2f s — hình đi trước tiếng (bài học EP19)"
                          % (first["vid"], first["speech_start"], OPEN_MAX))
    seen = set()
    for L in lines:
        if L["scene"] in seen:
            continue
        seen.add(L["scene"])
        lead = L["speech_start"] - starts[L["scene"]]
        if L is not lines[0] and lead > LEAD_WARN:
            warns.append("%s: hình vào trước tiếng %.2f s ở câu đầu cảnh (%s)" % (L["scene"], lead, L["vid"]))
    for a, b in zip(lines, lines[1:]):
        if b["speech_start"] < a["end"] - 0.02:
            errors.append("%s chồng lên %s (%.2f s < %.2f s)" % (b["vid"], a["vid"], b["speech_start"], a["end"]))
    for L in lines:
        if L["end"] > total + 0.01:
            errors.append("%s kết thúc %.2f s sau cuối video %.2f s" % (L["vid"], L["end"], total))
    return {"total_s": round(total, 3), "lines": lines, "errors": errors, "warnings": warns, "pass": not errors}


# ------------------------------------------------------------------ nhạc nền không lặp giữa các tập (Owner 13/11/2026)
def _sha_file(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def music_shas(ep_dir):
    """SHA-256 các bản nhạc nền của một tập: từ audio/audio_events.json (type=music) + file gốc trong audio/music
    (bỏ đoạn cắt tạm *_seg*.wav)."""
    import glob
    import json
    ep_dir = str(ep_dir)
    out = {}
    p = os.path.join(ep_dir, "audio", "audio_events.json")
    if os.path.exists(p):
        try:
            for e in json.load(open(p, encoding="utf-8")):
                if e.get("type") == "music" and e.get("sha256"):
                    out[e["sha256"]] = e.get("title") or e.get("file") or "?"
        except ValueError:
            pass
    for f in glob.glob(os.path.join(ep_dir, "audio", "music", "*")):
        if f.lower().endswith((".mp3", ".wav", ".m4a", ".ogg", ".flac")) and "_seg" not in os.path.basename(f):
            out.setdefault(_sha_file(f), os.path.basename(f))
    return out


def music_reuse(ep_dir, root=None):
    """Bản nhạc nền của tập này đã dùng ở tập khác chưa? Trả [{"sha","title","episodes"}] (rỗng = đạt)."""
    import glob
    ep_dir = os.path.abspath(str(ep_dir))
    root = root or os.path.dirname(ep_dir)
    mine = {}
    p = os.path.join(ep_dir, "audio", "audio_events.json")
    import json
    if os.path.exists(p):
        for e in json.load(open(p, encoding="utf-8")):
            if e.get("type") == "music" and e.get("sha256"):
                mine[e["sha256"]] = e.get("title") or e.get("file") or "?"
    hits = []
    others = [d for d in sorted(glob.glob(os.path.join(root, "ep*"))) if os.path.isdir(d) and os.path.abspath(d) != ep_dir]
    other_sh = {d: music_shas(d) for d in others}
    for sha, title in mine.items():
        eps = [os.path.basename(d) for d, sh in other_sh.items() if sha in sh]
        if eps:
            hits.append({"sha": sha, "title": title, "episodes": eps})
    return hits


def music_library(root):
    """Kho nhạc nền đã tải (Owner 19/11/2026: ưu tiên dùng lại). Trả [{"sha","file","episodes","credits"}] theo SHA,
    episodes = các tập có file/sự kiện nhạc này; credits = dòng đầu audio/CREDITS.md của tập đầu tiên (tên bài, tác giả, link)."""
    import glob
    lib = {}
    for d in sorted(glob.glob(os.path.join(str(root), "ep*"))):
        if not os.path.isdir(d):
            continue
        for sha, name in music_shas(d).items():
            e = lib.setdefault(sha, {"sha": sha, "file": os.path.join(os.path.basename(d), "audio", "music", name),
                                     "episodes": [], "credits": ""})
            e["episodes"].append(os.path.basename(d))
            c = os.path.join(d, "audio", "CREDITS.md")
            if not e["credits"] and os.path.exists(c):
                for line in open(c, encoding="utf-8"):
                    if "freesound.org" in line or "Nhạc" in line or "nhạc" in line:
                        e["credits"] = line.strip()[:200]
                        break
    return list(lib.values())

