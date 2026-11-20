"""Xuất đa nền tảng sau khi Owner duyệt video cuối (cổng 'final').

Mỗi nền tảng được dựng lại từ cùng cảnh/âm thanh đã duyệt, chỉ khác:
- vị trí và bề rộng phụ đề để không bị giao diện ứng dụng che (vùng an toàn, ước lượng theo hướng dẫn công khai của nền tảng);
- âm lượng chuẩn hoá -14 LUFS (mức các nền tảng ngắn tự chuẩn hoá);
- ảnh bìa, caption + hashtag riêng.
Kết quả: <gốc dự án>/videos-post/unpost/<topic>/<nền tảng>/  (KHÔNG tự đăng lên đâu; đăng xong chuyển sang videos-post/posted/)."""
import hashlib
import json
import os
import shutil
import subprocess
import time
import unicodedata

PLATFORMS = {
    # sub_y: tâm phụ đề dưới; sub_top: tâm phụ đề trên tối thiểu; sub_x/maxw: tránh cột nút bên phải
    "tiktok": {"label": "TikTok", "sub_y": 1390, "sub_top": 300, "sub_x": 500, "maxw": 820, "max_s": 600,
               "ui": "đáy ~440 px (caption, nhạc), phải ~120 px (nút tim/bình luận), đỉnh ~150 px (tab)"},
    "youtube_shorts": {"label": "YouTube Shorts", "sub_y": 1440, "sub_top": 300, "sub_x": 505, "maxw": 840, "max_s": 180,
                       "ui": "đáy ~380 px (tiêu đề, kênh, nút đăng ký), phải ~110 px"},
    "facebook_reels": {"label": "Facebook Reels", "sub_y": 1300, "sub_top": 300, "sub_x": 505, "maxw": 840, "max_s": 90,
                       "ui": "đáy ~35% nên tránh chữ (caption mở rộng, nút), phải ~120 px; Reels > 90 s không được đề xuất rộng"},
}
ORDER = ["tiktok", "youtube_shorts", "facebook_reels"]


def slug(text):
    s = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    out = "".join(c if c.isalnum() else "-" for c in s)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def remap_sub(y, maxw=900):
    """Gọi từ cute_engine.subtitle khi đang xuất cho một nền tảng. Từ 08/11/2026 phụ đề dưới luôn nằm trong dải 1/4 dưới
    (cute_engine.tray_top), nên ở đây chỉ còn dùng sub_x, maxw (né cột nút bên phải); sub_y không còn quyết định vị trí."""
    import cute_engine as E
    p = PLATFORMS.get(E.PLATFORM or "")
    if not p:
        return E.W / 2, y, maxw
    if y >= 1000:
        y = min(y, p["sub_y"])
    else:
        y = max(y, p["sub_top"])
    return p["sub_x"], y, p["maxw"]


def seg_dir(E, plat):
    return os.path.join(E.HERE, "export", plat, "segments")


def topic_dir(E, meta, post):
    root = os.path.dirname(os.path.dirname(E.OUT))           # <gốc dự án>
    name = post.get("topic_slug") or slug(meta.get("title", os.path.basename(E.OUT)))
    return os.path.join(root, "videos-post", "unpost", name)


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _brand_mark(E, post, plat, clean, pdir, base):
    """Bước cuối của Spielberg: chèn watermark thương hiệu. Lỗi → CHẶN, không đưa bản sạch vào videos-post."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from ai_video_factory.core import branding
    brand = post.get("brand")
    rep_p = os.path.join(os.path.dirname(clean), "watermark_report.json")
    if not brand:
        raise SystemExit("CHẶN XUẤT: post.json thiếu 'brand'. Khai báo thương hiệu (vd. \"ngang-mot-ti\") để biết có phải chèn watermark không.")
    if brand not in branding.BRANDS:
        # thương hiệu khác: không chèn watermark NMT; bản xuất = bản sạch (ghi rõ trong manifest)
        vid = os.path.join(pdir, "%s_%s.mp4" % (base, plat))
        shutil.copyfile(clean, vid)
        return vid, {"status": "NOT_REQUIRED", "reason": "thương hiệu '%s' không có quy tắc watermark" % brand}
    ov_p = os.path.join(E.OUT, "watermark.json")
    ov = json.load(open(ov_p, encoding="utf-8")) if os.path.exists(ov_p) else {}
    override = dict(ov.get("default", {}), **ov.get(plat, {})) or None
    if getattr(E, "SAFE916", False):
        import safe_frame as SF
        override = SF.wm_override(override)   # logo không nằm trong lề bị app cắt
    vid = os.path.join(pdir, "%s_%s_nmt.mp4" % (base, plat))
    try:
        rep = branding.export(clean, vid, brand, platform=plat, override=override, report_path=rep_p)
    except branding.WatermarkError as e:
        with open(os.path.join(pdir, "BLOCKED.txt"), "w", encoding="utf-8") as fh:
            fh.write("CHẶN XUẤT BẢN %s: %s\nBáo cáo: %s\n" % (plat, e, rep_p))
        raise SystemExit("CHẶN XUẤT BẢN [%s] — watermark lỗi: %s" % (plat, e))
    blk = os.path.join(pdir, "BLOCKED.txt")
    if os.path.exists(blk):
        os.replace(blk, os.path.join(os.path.dirname(clean), "BLOCKED_resolved.txt"))
    g = rep["geometry"]
    return vid, {"status": "PASS", "master_sha256": rep["master"]["sha256"],
                 "box": [g["x"], g["y"], g["w"], g["h"]], "opacity": g["opacity"], "anchor": g["anchor"],
                 "checks": rep["verify"]["checks"], "busy_ratio": rep["busy"]["busy_ratio"],
                 "report": os.path.relpath(rep_p, ROOT)}


def finish(E, meta, workflow):
    post_p = os.path.join(E.OUT, "post.json")
    post = json.load(open(post_p, encoding="utf-8")) if os.path.exists(post_p) else {}
    tdir = topic_dir(E, meta, post)
    master = os.path.join(E.OUT, "audio", "master.wav")
    made = []
    for plat in ORDER:
        sd = seg_dir(E, plat)
        miss = [s[0] for s in E.SCENES if not os.path.exists(os.path.join(sd, s[0] + ".mp4"))]
        if miss:
            raise SystemExit("Chưa dựng xong %s: thiếu %s (chạy --export %s %s)" % (plat, miss, plat, " ".join(miss)))
        pdir = os.path.join(tdir, plat)
        os.makedirs(pdir, exist_ok=True)
        lst = os.path.join(os.path.dirname(sd), "concat.txt")
        with open(lst, "w") as fh:
            for s in E.SCENES:
                fh.write("file 'segments/%s.mp4'\n" % s[0])
        base = os.path.basename(tdir)
        # Bản SẠCH (không watermark) để chỉnh sửa/tái sử dụng: nằm trong render/export/<nền tảng>/, không bao giờ ghi đè.
        clean = os.path.join(os.path.dirname(sd), "%s_%s_clean.mp4" % (base, plat))
        srcs = [os.path.join(sd, s[0] + ".mp4") for s in E.SCENES] + [master]
        if os.path.exists(clean) and os.path.getmtime(clean) < max(os.path.getmtime(f) for f in srcs):
            # cảnh/âm thanh đã dựng lại sau bản sạch cũ: KHÔNG ghi đè bản cũ, tạo bản sạch mới có dấu thời gian
            clean = os.path.join(os.path.dirname(sd), "%s_%s_clean_%s.mp4" % (base, plat, time.strftime("%Y%m%d-%H%M%S")))
        if os.path.exists(clean):
            print("[%s] dùng lại bản sạch có sẵn (không ghi đè): %s" % (plat, clean))
        else:
            tmp = clean + ".part.mp4"
            # loudnorm 2 lượt: đo trước rồi chuẩn hoá tuyến tính để đạt đúng -14 LUFS
            m = subprocess.run(["ffmpeg", "-hide_banner", "-i", master, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                                "-f", "null", "-"], capture_output=True, text=True).stderr
            js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
            ln = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
                  % (js["input_i"], js["input_tp"], js["input_lra"], js["input_thresh"], js["target_offset"]))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", master,
                            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", ln,
                            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", "-f", "mp4", tmp], check=True)
            os.replace(tmp, clean)
        vid, wm = _brand_mark(E, post, plat, clean, pdir, base)
        # ảnh bìa = khung thumbnail đã duyệt
        thumb = os.path.join(E.OUT, "thumbnail.png")
        if os.path.exists(thumb):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", thumb, "-q:v", "2", os.path.join(pdir, "cover.jpg")], check=True)
        cap = post.get(plat, {})
        tags = " ".join(cap.get("hashtags", post.get("hashtags", [])))
        with open(os.path.join(pdir, "caption.txt"), "w", encoding="utf-8") as fh:
            fh.write((cap.get("title") + "\n\n" if cap.get("title") else "") + cap.get("caption", post.get("caption", meta.get("title", ""))) + "\n\n" + tags + "\n")
        probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate",
                                           "-of", "json", vid], capture_output=True, text=True).stdout)
        dur = float(probe["format"]["duration"])
        eb = subprocess.run(["ffmpeg", "-hide_banner", "-i", vid, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        lufs = float([l for l in eb.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        p = PLATFORMS[plat]
        info = {"platform": p["label"], "file": os.path.basename(vid), "duration_s": round(dur, 2), "size_bytes": int(probe["format"]["size"]),
                "video": "1080x1920 9:16 SAR 1:1 H.264 60fps", "audio": "AAC 48 kHz", "loudness_lufs_measured": lufs,
                "safe_frame": "NMT-SAFE-916 v1 (output/_engine/safe_frame.py); kiểm tra bằng safe_frame.py preview",
                "subtitle_safe_zone": {"y_bottom_center": p["sub_y"], "x_center": p["sub_x"], "max_width": p["maxw"], "ui_avoided": p["ui"]},
                "within_length_limit": dur <= p["max_s"], "sha256": _sha(vid),
                "brand": post.get("brand"), "watermark": wm,
                "clean_version": {"file": os.path.relpath(clean, ROOT), "sha256": _sha(clean), "note": "bản sạch để sửa/tái dùng, KHÔNG đăng"},
                "source_final_video_sha256": _sha(os.path.join(E.OUT, "final_video.mp4")),
                "approvals": {k: {"status": v.get("status"), "by": v.get("by"), "at": v.get("at")} for k, v in workflow["approvals"].items()},
                "published": False}
        json.dump(info, open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        made.append((plat, vid, info))
    with open(os.path.join(tdir, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# %s\n\nNguồn: `output/%s/final_video.mp4` (Owner đã duyệt video cuối).\n\n" % (meta.get("title", ""), os.path.basename(E.OUT)))
        fh.write("| Nền tảng | File | Thời lượng | Vùng phụ đề |\n|---|---|---|---|\n")
        for plat, vid, info in made:
            fh.write("| %s | `%s/%s` | %.1f s | tâm y=%d, rộng ≤ %d px |\n" % (info["platform"], plat, os.path.basename(vid), info["duration_s"],
                                                                         PLATFORMS[plat]["sub_y"], PLATFORMS[plat]["maxw"]))
        fh.write("\nMỗi thư mục có `cover.jpg`, `caption.txt`, `manifest.json`. File `*_nmt.mp4` đã chèn watermark NMT và qua kiểm tra. "
                 "Bản sạch (không watermark) nằm ở `output/%s/render/export/<nền tảng>/`, không dùng để đăng.\n" % os.path.basename(E.OUT))
        fh.write("\n**Chưa đăng.** Owner tự đăng thủ công. Không bật thêm watermark trong YouTube Studio (tránh 2 logo).\n")
    return tdir, made
