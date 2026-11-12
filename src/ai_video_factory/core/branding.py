"""Watermark thương hiệu, chèn ở BƯỚC XUẤT CUỐI của Spielberg (không chèn vào ảnh nguồn hay từng cảnh).

Quy tắc Owner 07/11/2026 cho thương hiệu "Ngang Một Tí" (NMT):
- Mọi video xuất bản của NMT bắt buộc có watermark NMT chèn trực tiếp vào file video.
- Nguồn: output/branding/ngang-mot-ti/watermark-master.png (PNG trong suốt). KHÔNG dùng bản 150×150 của YouTube Studio.
- Giữ tỉ lệ, không méo. Kích thước, độ mờ, khoảng cách mép cấu hình theo khung ngang/dọc và nền tảng.
- Vị trí mặc định do Owner chọn: góc DƯỚI-PHẢI (khung dọc: sát góc, cách mép 48 px).
- Tránh phụ đề: chồng lấn với vùng phụ đề thì CHẶN, trừ khi có watermark.json điều chỉnh vị trí trước khi xuất.
- Bản sạch giữ riêng, không ghi đè. Bản có watermark chỉ ra đích sau khi qua kiểm tra.
- Lỗi (thiếu file, chèn hỏng, kiểm tra đầu ra thất bại) → WatermarkError. Không bao giờ âm thầm dùng bản sạch.
- Chỉ áp dụng cho thương hiệu đã khai báo; thương hiệu khác không bị chèn NMT.
Chỉ dùng công nghệ đã duyệt: FFmpeg (overlay), Pillow, numpy."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image

from . import config

BRANDS = {
    "ngang-mot-ti": {
        "name": "Ngang Một Tí",
        "master": "output/branding/ngang-mot-ti/watermark-master.png",
        "min_master_width": 600,                     # chặn bản 150×150 dành cho YouTube Studio
        "alpha_floor": 16,                           # bỏ cặn alpha rất mờ quanh logo (chỉ trong bộ nhớ)
        "anchor": "bottom-right",
        "vertical": {"width": 190, "opacity": 0.85, "margin_x": 48, "margin_y": 48},
        "horizontal": {"width": 240, "opacity": 0.85, "margin_x": 40, "margin_y": 170},   # ngang: nằm TRÊN dải phụ đề (đo thật y 930–1060)
        "platforms": {                               # ghi đè theo nền tảng (khung dọc); để trống = dùng mặc định
            "tiktok": {}, "youtube_shorts": {}, "facebook_reels": {},
        },
    },
}

# Vùng phụ đề phải tránh (x0, y0, x1, y1). Khung dọc theo nmt-engine/platform_export; khung ngang theo phụ đề giữa-đáy.
SUBTITLE_ZONES = {
    # Tính từ code phụ đề thật: viên phụ đề được đặt theo TÂM y, cao tối đa ~200 px (2 dòng), trượt vào 26 px.
    # vertical None = engine MVP (src/.../comedy/engine.py, tâm y=1610). Bản gốc nmt-engine (tâm 1690) không được
    # gắn watermark trực tiếp: chỉ bản xuất theo nền tảng mới đi đăng.
    "vertical": {
        None: [(90, 1490, 990, 1750), (90, 190, 990, 430)],
        "tiktok": [(90, 1270, 910, 1530), (90, 190, 990, 430)],         # tâm 1390, x 500, rộng ≤ 820
        "youtube_shorts": [(85, 1320, 925, 1580), (90, 190, 990, 430)], # tâm 1440, x 505, rộng ≤ 840
        "facebook_reels": [(85, 1180, 925, 1440), (90, 190, 990, 430)], # tâm 1300
    },
    # Khung ngang: đo trên video ngang thật của dự án (workspace/deliver/a04, a09): hộp phụ đề tối x 82–1830, y ~945–1054.
    "horizontal": {None: [(60, 930, 1860, 1060)]},
}


class WatermarkError(RuntimeError):
    """Chặn xuất bản: thiếu file, chèn lỗi hoặc kiểm tra đầu ra thất bại."""


def project_root():
    return Path(os.environ.get("AVF_PROJECT_ROOT", str(config.ROOT)))


def profile(brand):
    if brand not in BRANDS:
        raise WatermarkError("Thương hiệu '%s' chưa có hồ sơ watermark" % brand)
    return BRANDS[brand]


def _sha(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_master(brand, path=None):
    """Kiểm tra và nạp PNG gốc. Trả (ảnh RGBA đã cắt theo khung logo, thông tin)."""
    pf = profile(brand)
    p = Path(path) if path else project_root() / pf["master"]
    if not p.exists():
        raise WatermarkError("Thiếu file watermark: %s" % p)
    if "150x150" in p.name:
        raise WatermarkError("Không dùng bản 150×150 của YouTube Studio làm nguồn render: %s" % p.name)
    try:
        im = Image.open(str(p))
        im.load()
    except Exception as e:  # noqa: BLE001
        raise WatermarkError("Không đọc được file watermark %s: %s" % (p, e))
    if im.format != "PNG":
        raise WatermarkError("Watermark phải là PNG, nhận %s" % im.format)
    if im.mode not in ("RGBA", "LA") and not (im.mode == "P" and "transparency" in im.info):
        raise WatermarkError("Watermark không có kênh trong suốt (mode %s)" % im.mode)
    if im.width < pf["min_master_width"]:
        raise WatermarkError("Watermark quá nhỏ (%d px < %d px), có thể là bản 150×150" % (im.width, pf["min_master_width"]))
    rgba = im.convert("RGBA")
    a = np.asarray(rgba).copy()
    if (a[..., 3] < 250).mean() < 0.05:
        raise WatermarkError("Watermark gần như không có vùng trong suốt")
    a[..., 3] = np.where(a[..., 3] < pf["alpha_floor"], 0, a[..., 3])
    trimmed = Image.fromarray(a)
    bbox = trimmed.getchannel("A").getbbox()
    if not bbox:
        raise WatermarkError("Watermark trống sau khi bỏ cặn alpha")
    trimmed = trimmed.crop(bbox)
    return trimmed, {"path": str(p), "sha256": _sha(p), "size": list(im.size), "logo_bbox": list(bbox),
                     "logo_size": list(trimmed.size)}


def orientation(w, h):
    return "vertical" if h > w else "horizontal"


def geometry(brand, frame_w, frame_h, platform=None, override=None, logo_size=None):
    """Vị trí và kích thước watermark trên khung (pixel nguyên, giữ tỉ lệ logo)."""
    pf = profile(brand)
    ori = orientation(frame_w, frame_h)
    g = dict(pf[ori])
    if ori == "vertical" and platform:
        g.update(pf["platforms"].get(platform, {}))
    anchor = pf["anchor"]
    if override:
        g.update({k: override[k] for k in ("width", "opacity", "margin_x", "margin_y") if k in override})
        anchor = override.get("anchor", anchor)
    lw, lh = logo_size
    w = int(round(g["width"] * frame_w / (1080 if ori == "vertical" else 1920)))
    h = int(round(w * lh / lw))
    mx = int(round(g["margin_x"] * frame_w / (1080 if ori == "vertical" else 1920)))
    my = int(round(g["margin_y"] * frame_h / (1920 if ori == "vertical" else 1080)))
    x = frame_w - mx - w if "right" in anchor else mx
    y = frame_h - my - h if "bottom" in anchor else my
    if override and "x" in override and "y" in override:
        x, y = int(override["x"]), int(override["y"])
    if not (0 <= x and 0 <= y and x + w <= frame_w and y + h <= frame_h):
        raise WatermarkError("Watermark nằm ngoài khung: %s" % [x, y, w, h])
    return {"x": x, "y": y, "w": w, "h": h, "opacity": float(g["opacity"]), "anchor": anchor, "orientation": ori,
            "platform": platform}


def subtitle_zones(frame_w, frame_h, platform=None):
    ori = orientation(frame_w, frame_h)
    z = SUBTITLE_ZONES[ori].get(platform) or SUBTITLE_ZONES[ori][None]
    sx, sy = frame_w / (1080 if ori == "vertical" else 1920), frame_h / (1920 if ori == "vertical" else 1080)
    return [(int(a * sx), int(b * sy), int(c * sx), int(d * sy)) for a, b, c, d in z]


def conflicts(geom, zones):
    x0, y0, x1, y1 = geom["x"], geom["y"], geom["x"] + geom["w"], geom["y"] + geom["h"]
    return [z for z in zones if x0 < z[2] and z[0] < x1 and y0 < z[3] and z[1] < y1]


def make_overlay(logo, geom, path):
    """PNG đúng kích thước, độ mờ đã nhân sẵn vào kênh alpha."""
    m = logo.resize((geom["w"], geom["h"]), Image.LANCZOS)
    a = np.asarray(m).copy()
    a[..., 3] = np.round(a[..., 3].astype(float) * geom["opacity"]).astype("uint8")
    Image.fromarray(a).save(str(path))
    return path


def probe(mp4):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(mp4)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise WatermarkError("ffprobe lỗi với %s: %s" % (mp4, r.stderr[-300:]))
    j = json.loads(r.stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"]
    if not v:
        raise WatermarkError("Không có luồng hình trong %s" % mp4)
    return {"duration": float(j["format"]["duration"]), "w": v[0]["width"], "h": v[0]["height"],
            "fps": v[0]["r_frame_rate"], "audio": any(s["codec_type"] == "audio" for s in j["streams"])}


def _frame(mp4, t, w, h):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", str(mp4), "-frames:v", "1", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True)
    if r.returncode != 0 or len(r.stdout) < w * h * 3:
        raise WatermarkError("Không trích được khung %.2fs từ %s" % (t, mp4))
    return np.frombuffer(r.stdout[: w * h * 3], dtype=np.uint8).reshape(h, w, 3).astype(float)


def apply(clean, out, geom, overlay_png, workdir=None):
    """Ghi ra file tạm trong thư mục tạm của hệ thống (không để file dở trong thư mục dự án/videos-post)."""
    tmp = Path(workdir or tempfile.mkdtemp(prefix="avf_wm_")) / (Path(out).stem + ".part.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(clean), "-i", str(overlay_png), "-filter_complex",
           "[0:v][1:v]overlay=%d:%d:format=auto:eof_action=repeat,format=yuv420p[v]" % (geom["x"], geom["y"]),
           "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "copy",
           "-movflags", "+faststart", str(tmp)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not tmp.exists():
        raise WatermarkError("FFmpeg không chèn được watermark: %s" % r.stderr[-400:])
    return tmp


def verify(clean, marked, geom, overlay_png):
    """Kiểm tra đầu ra: cùng thời lượng/khung/fps/âm thanh; watermark có mặt đúng chỗ ở đầu, giữa, cuối; ngoài vùng không đổi."""
    pc, pm = probe(clean), probe(marked)
    res = {"clean": pc, "marked": pm, "checks": []}
    if (pc["w"], pc["h"], pc["fps"], pc["audio"]) != (pm["w"], pm["h"], pm["fps"], pm["audio"]):
        raise WatermarkError("Bản watermark khác thông số bản sạch: %s vs %s" % (pm, pc))
    fps = eval(pc["fps"]) if "/" in pc["fps"] else float(pc["fps"])   # noqa: S307 — chuỗi từ ffprobe dạng "60/1"
    if abs(pc["duration"] - pm["duration"]) > 2.0 / max(fps, 1):
        raise WatermarkError("Lệch thời lượng: sạch %.3fs, watermark %.3fs" % (pc["duration"], pm["duration"]))
    ov = np.asarray(Image.open(str(overlay_png)).convert("RGBA")).astype(float)
    alpha = ov[..., 3:4] / 255.0
    x, y, w, h = geom["x"], geom["y"], geom["w"], geom["h"]
    W, H = pc["w"], pc["h"]
    D = pc["duration"]
    mask = np.zeros((H, W), bool)
    mask[y:y + h, x:x + w] = True
    for label, t in (("đầu", min(0.25, D * 0.05)), ("giữa", D / 2), ("cuối", max(0.0, D - 0.35))):
        fc, fm = _frame(clean, t, W, H), _frame(marked, t, W, H)
        reg_c, reg_m = fc[y:y + h, x:x + w], fm[y:y + h, x:x + w]
        expect = reg_c * (1 - alpha) + ov[..., :3] * alpha
        strong = alpha[..., 0] > 0.5
        err_expect = float(np.abs(reg_m - expect)[strong].mean())
        diff_clean_in = float(np.abs(reg_m - reg_c)[strong].mean())
        outside = float(np.abs(fm - fc)[~mask].mean())
        ok = err_expect < 14 and diff_clean_in > max(6.0, err_expect) and outside < 3.0
        res["checks"].append({"at": label, "t": round(t, 2), "err_vs_expected": round(err_expect, 2),
                              "diff_vs_clean_in_box": round(diff_clean_in, 2), "diff_outside_box": round(outside, 2), "ok": ok})
        if not ok:
            raise WatermarkError("Kiểm tra watermark thất bại ở %s (%.2fs): %s" % (label, t, res["checks"][-1]))
    return res


def busy_report(clean, geom, step=0.5):
    """Cảnh báo (không chặn): khung có nhiều nét/chi tiết dưới vị trí watermark (gợi ý có thể che nội dung)."""
    p = probe(clean)
    x, y, w, h = geom["x"], geom["y"], geom["w"], geom["h"]
    pad = 12
    vf = "fps=%g,crop=%d:%d:%d:%d,format=gray" % (1.0 / step, w + 2 * pad, h + 2 * pad, max(0, x - pad), max(0, y - pad))
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clean), "-vf", vf, "-f", "rawvideo", "-"], capture_output=True)
    fw, fh = w + 2 * pad, h + 2 * pad
    n = len(r.stdout) // (fw * fh)
    warn = []
    for i in range(n):
        g = np.frombuffer(r.stdout[i * fw * fh:(i + 1) * fw * fh], np.uint8).reshape(fh, fw).astype(float)
        edge = (np.abs(np.diff(g, axis=0)) > 40).mean() + (np.abs(np.diff(g, axis=1)) > 40).mean()
        if edge > 0.08:
            warn.append({"t": round(i * step, 1), "edge_density": round(float(edge), 3)})
    return {"samples": n, "busy_frames": warn, "busy_ratio": round(len(warn) / max(n, 1), 3), "duration": p["duration"]}


def export(clean, out_final, brand, platform=None, override=None, report_path=None, master=None):
    """Toàn bộ bước: kiểm tra nguồn → vị trí → xung đột phụ đề → chèn → kiểm tra → mới chuyển tới đích.
    Thất bại: ghi báo cáo BLOCKED, KHÔNG tạo out_final, ném WatermarkError."""
    clean, out_final = Path(clean), Path(out_final)
    rep = {"brand": brand, "platform": platform, "clean": str(clean), "status": "BLOCKED",
           "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    tmp = None
    work = None
    try:
        if not clean.exists():
            raise WatermarkError("Không có bản sạch: %s" % clean)
        clean_sha = _sha(clean)
        logo, minfo = load_master(brand, master)
        rep["master"] = minfo
        pc = probe(clean)
        geom = geometry(brand, pc["w"], pc["h"], platform, override, logo.size)
        rep["geometry"] = geom
        zones = subtitle_zones(pc["w"], pc["h"], platform)
        hit = conflicts(geom, zones)
        rep["subtitle_conflicts"] = hit
        if hit and not (override and override.get("accept_subtitle_overlap")):
            raise WatermarkError("Watermark chồng vùng phụ đề %s. Điều chỉnh vị trí trong watermark.json trước khi xuất." % hit)
        rep["busy"] = busy_report(clean, geom)
        work = Path(tempfile.mkdtemp(prefix="avf_wm_"))
        ovp = work / "overlay.png"
        out_final.parent.mkdir(parents=True, exist_ok=True)
        make_overlay(logo, geom, ovp)
        tmp = apply(clean, out_final, geom, ovp, work)
        rep["verify"] = verify(clean, tmp, geom, ovp)
        if _sha(clean) != clean_sha:
            raise WatermarkError("Bản sạch bị thay đổi trong lúc chèn watermark")
        rep["clean_sha256"] = clean_sha
        part = out_final.parent / (out_final.name + ".part")
        shutil.copyfile(str(tmp), str(part))           # chép vào cùng thư mục rồi đổi tên nguyên tử
        if _sha(part) != _sha(tmp):
            raise WatermarkError("Chép bản watermark ra đích bị lỗi")
        os.replace(str(part), str(out_final))
        rep.update({"status": "PASS", "output": str(out_final), "output_sha256": _sha(out_final)})
        return rep
    except WatermarkError as e:
        rep["error"] = str(e)
        raise
    finally:
        if work is not None:
            shutil.rmtree(str(work), ignore_errors=True)   # chỉ dọn thư mục tạm hệ thống, không đụng thư mục dự án
        if report_path:
            Path(report_path).parent.mkdir(parents=True, exist_ok=True)
            Path(report_path).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------- tích hợp pipeline (Spielberg bước cuối → Quality Gate → Tesla) ----------------
PUBLISH_NAME = "final_%s.mp4"     # spielberg/final_nmt.mp4 với thương hiệu ngang-mot-ti
BRAND_TAGS = {"ngang-mot-ti": "nmt"}


def brand_final(ctx, state, platform=None):
    """Gọi NGAY SAU khi Spielberg xuất spielberg/final.mp4 (bản sạch) và Quality Gate cơ bản đã qua.
    - Thương hiệu có quy tắc watermark → tạo spielberg/final_<tag>.mp4, ghi manager/watermark_report.json (PASS).
    - Không khai báo thương hiệu, hoặc thương hiệu không có quy tắc → báo cáo NOT_REQUIRED, file đăng = final.mp4.
    - Lỗi → báo cáo BLOCKED, state['publish_file'] = None, ném WatermarkError (caller biến thành GateFailed)."""
    brand = state.get("brand")
    clean = ctx.dir / "spielberg" / "final.mp4"
    rep_p = ctx.dir / "manager" / "watermark_report.json"
    if not brand or brand not in BRANDS:
        rep = {"status": "NOT_REQUIRED", "brand": brand, "reason": "thương hiệu không có quy tắc watermark",
               "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        rep_p.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
        state["publish_file"] = "spielberg/final.mp4"
        return clean
    out = ctx.dir / "spielberg" / (PUBLISH_NAME % BRAND_TAGS.get(brand, brand))
    try:
        export(clean, out, brand, platform=platform or state.get("platform"),
               override=state.get("watermark_override"), report_path=rep_p)
    except WatermarkError:
        state["publish_file"] = None
        raise
    state["publish_file"] = str(out.relative_to(ctx.dir))
    return out


def check_publishable(ctx, approved_rel, approved_sha):
    """Dùng ở Tesla. Trả None nếu hợp lệ, ngược lại chuỗi lý do từ chối."""
    state = json.loads((ctx.dir / "manager" / "run.json").read_text(encoding="utf-8")) \
        if (ctx.dir / "manager" / "run.json").exists() else {}
    brand = state.get("brand")
    rep_p = ctx.dir / "manager" / "watermark_report.json"
    if brand in BRANDS:
        if not rep_p.exists():
            return "thương hiệu %s bắt buộc watermark nhưng chưa có watermark_report.json" % brand
        rep = json.loads(rep_p.read_text(encoding="utf-8"))
        if rep.get("status") != "PASS" or rep.get("brand") != brand:
            return "watermark chưa qua kiểm tra (trạng thái %s)" % rep.get("status")
        want = PUBLISH_NAME % BRAND_TAGS.get(brand, brand)
        if Path(approved_rel).name != want:
            return "bản được duyệt (%s) không phải bản có watermark (%s)" % (approved_rel, want)
        if rep.get("output_sha256") != approved_sha:
            return "checksum bản duyệt khác bản watermark đã kiểm tra"
    elif rep_p.exists():
        rep = json.loads(rep_p.read_text(encoding="utf-8"))
        if rep.get("status") == "BLOCKED":
            return "watermark bị CHẶN: %s" % rep.get("error")
    return None
