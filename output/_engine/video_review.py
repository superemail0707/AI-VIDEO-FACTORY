"""Review video độc lập trước khi hỏi Owner duyệt video cuối (rule Owner 13/11/2026).

Luồng (sau `--mux`, trước khi gửi Owner):
  python3 output/_engine/video_review.py prepare <thư mục tập>
      -> render/video_review/vNN/: lưới khung hình (mỗi 2 s), số đo kỹ thuật + âm thanh, phụ đề, kết quả QA,
         và prompt giám khảo `prompt.md`.
  Giám khảo ĐỘC LẬP (subagent mới, không lịch sử hội thoại) đọc prompt + ảnh, trả JSON.
  python3 output/_engine/video_review.py record <thư mục tập> <file.json> --judge claude-subagent
      -> code tự cộng điểm; ĐẠT khi tổng ≥ 8/10 và không còn lỗi chặn (blocking).
  Chưa đạt: sửa, render lại, `prepare` lại (lần mới). Tối đa 3 lần; sau đó vẫn gửi Owner kèm điểm và lỗi còn lại.
  python3 output/_engine/video_review.py status <thư mục tập>
Mỗi lần chấm được ghi vào sổ `video_review_findings.jsonl` để cải tiến các tập sau.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
FINDINGS_FILE = ENGINE / "video_review_findings.jsonl"
THRESHOLD = 8.0
MAX_ATTEMPTS = 3
RUBRIC = [("visual", 3, "Hình ảnh: biểu cảm cường điệu đúng chỗ, nhân vật đúng nhận diện & liền mạch, không lỗi tranh, không cắt mặt, không khung tĩnh quá lâu"),
          ("comedy_brand", 2, "Hài & nhận diện kênh: tắt tiếng vẫn hiểu và buồn cười, có dấu hiệu thương hiệu (Chuyện nhỏ!, khung nguệch ngoạc, Mimi phán xét, cảnh kết tai mèo)"),
          ("audio", 2, "Âm thanh: giọng rõ, nhạc nền hợp và không át giọng, SFX đúng nhịp, không im lặng bất thường, độ to ổn định"),
          ("subtitles", 2, "Phụ đề & chữ: chỉ phụ đề thoại thật, đúng chính tả tiếng Việt, không thừa, không che nhân vật/watermark, chữ trên hình dễ đọc"),
          ("technical", 1, "Kỹ thuật: 1080×1920, 60 fps, thời lượng ≥ 60 s gồm outro 7,8 s (Owner 18/11/2026, D-032), không giật/hỏng khung")]


class ReviewError(SystemExit):
    pass


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _run(args):
    return subprocess.run(args, capture_output=True, text=True)


def probe(video):
    r = _run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration",
              "-of", "json", str(video)])
    j = json.loads(r.stdout or "{}")
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    num, den = (v.get("r_frame_rate") or "0/1").split("/")
    return {"width": v.get("width"), "height": v.get("height"), "fps": round(float(num) / float(den or 1), 2),
            "video_codec": v.get("codec_name"), "audio_codec": a.get("codec_name"),
            "duration_s": round(float(j.get("format", {}).get("duration", 0)), 2)}


def loudness(video):
    r = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-af", "ebur128=peak=true,silencedetect=n=-45dB:d=1.5",
              "-f", "null", "-"])
    err = r.stderr
    out = {}
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    if m:
        out["integrated_lufs"] = float(m[-1])
    m = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    if m:
        out["true_peak_dbfs"] = float(m[-1])
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", err)]
    out["silences"] = [[round(s, 2), round(e, 2)] for s, e in zip(starts, ends)]
    return out


def frame_sheets(video, out_dir, every=2.0, cols=6, rows=3):
    """Lưới khung hình (mỗi `every` giây), mỗi tấm cols×rows ô 270×480, có mốc giây trên từng ô."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pat = str(out_dir / "sheet_%02d.jpg")
    vf = ("fps=1/%g,scale=270:480,drawtext=text='%%{pts\\:hms}':x=6:y=6:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6,"
          "tile=%dx%d" % (every, cols, rows))
    r = _run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", vf, "-q:v", "4", pat])
    if r.returncode != 0:      # ffmpeg không có drawtext (thiếu freetype) -> bỏ nhãn giây
        vf = "fps=1/%g,scale=270:480,tile=%dx%d" % (every, cols, rows)
        _run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", vf, "-q:v", "4", pat])
    return sorted(str(p) for p in out_dir.glob("sheet_*.jpg"))


def srt_mids(srt):
    """Điểm giữa mỗi câu trong subtitle.srt (giây)."""
    import re
    out = []
    for a, b in re.findall(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", Path(srt).read_text(encoding="utf-8")):
        f = lambda s: sum(float(x) * m for x, m in zip(s.replace(",", ".").split(":"), (3600, 60, 1)))
        out.append(round((f(a) + f(b)) / 2, 2))
    return out


def subtitle_sheet(video, srt, out_dir, cols=6):
    """EP28 (19/11/2026): lưới cố định mỗi 2 s có thể rơi đúng lúc thẻ phụ đề (chạy theo giọng) đã tắt -> giám khảo
    báo nhầm 'mất phụ đề'. Thêm 1 tấm lấy đúng điểm giữa từng câu thoại để kiểm phụ đề."""
    from PIL import Image, ImageDraw
    mids = srt_mids(srt) if Path(srt).exists() else []
    if not mids:
        return None
    rows = (len(mids) + cols - 1) // cols
    sheet = Image.new("RGB", (270 * cols, 480 * rows), "black")
    tmp = Path(out_dir) / "_mid.png"
    for i, t in enumerate(mids):
        _run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % t, "-i", str(video), "-frames:v", "1", "-vf", "scale=270:480", str(tmp)])
        if tmp.exists():
            im = Image.open(tmp).convert("RGB")
            ImageDraw.Draw(im).text((6, 6), "%.1fs câu %d" % (t, i + 1), fill=(255, 230, 0))
            sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
    tmp.unlink(missing_ok=True)
    p = Path(out_dir) / "subs_mid.jpg"
    sheet.save(p, quality=85)
    return str(p)


def _qa(ep):
    out = {}
    for name in ("qa_subtitles_master", "qa_sync", "qa_transitions"):
        p = Path(ep) / "render" / (name + ".json")
        if p.exists():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                out[name] = {"pass": d.get("pass"), "errors": d.get("errors", [])[:5] if isinstance(d.get("errors"), list) else d.get("errors")}
            except ValueError:
                out[name] = "không đọc được"
    return out


def _state_path(ep):
    return Path(ep) / "render" / "video_review.json"


def load_state(ep):
    p = _state_path(ep)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"threshold": THRESHOLD, "max_attempts": MAX_ATTEMPTS, "status": "pending", "attempts": [], "packets": []}


def save_state(ep, st):
    _state_path(ep).write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def rubric_text():
    return "\n".join("- %s (tối đa %g): %s" % (k, mx, d) for k, mx, d in RUBRIC)


def build_prompt(ep, packet):
    ep = Path(ep)
    script = (ep / "render" / "script.md")
    srt = (ep / "subtitle.srt")
    sheets = "\n".join("- " + s for s in packet["sheets"])
    subs_line = ("- Phụ đề theo câu (mỗi ô là ĐIỂM GIỮA một câu thoại; thẻ phụ đề chạy theo giọng nên có thể không hiện ở ô lưới 2 s — "
                 "kiểm phụ đề bằng tấm này): %s\n" % packet["subs_sheet"]) if packet.get("subs_sheet") else ""
    example = "{" + ", ".join('"%s": <0–%g>' % (k, mx) for k, mx, _ in RUBRIC) + "}"
    return f"""Bạn là biên tập viên kiểm duyệt video ĐỘC LẬP cho kênh hoạt hình ngắn "Ngang Một Tí" (Tí, Ngang và mèo Mimi).
Nhiệm vụ: xem video cuối qua lưới khung hình + số đo, chấm điểm và chỉ ra lỗi CỤ THỂ (mốc giây, cảnh) trước khi gửi chủ kênh duyệt.
Chấm khắt khe: 8/10 = đủ tốt để đăng ngay. Không dự đoán viral.

Đọc (dùng công cụ đọc ảnh/tệp):
- Lưới khung hình (mỗi ô cách nhau {packet['every_s']} giây, nhãn vàng góc trên là mốc giây nếu có):
{sheets}
{subs_line}- Kịch bản đã duyệt: {script}
- Phụ đề: {srt}
- Bộ nhận diện kênh: {ENGINE.parent.parent / 'docs' / 'marketing' / 'BRAND_NMT.md'}

Số đo kỹ thuật (máy đo):
{json.dumps(packet['probe'], ensure_ascii=False)}
Âm thanh (ebur128 + đoạn im lặng < -45 dB dài ≥ 1,5 s):
{json.dumps(packet['loudness'], ensure_ascii=False)}
(Đây là bản gốc. Bước xuất 3 nền tảng (platform_export) tự chuẩn hoá loudnorm 2 lượt về -14 LUFS, TP -1,5 dBTP —
 KHÔNG trừ điểm vì độ to tổng của bản gốc; chỉ chấm cân bằng giọng/nhạc/SFX và im lặng bất thường.)
Kiểm tra tự động của engine:
{json.dumps(packet['qa'], ensure_ascii=False)}

Lưu ý: bạn không nghe được âm thanh — chấm mục audio dựa trên số đo, đoạn im lặng (có hợp với kịch bản không) và kịch bản SFX/nhạc.

Thang chấm (cho phép nửa điểm):
{rubric_text()}

"blocking": lỗi PHẢI sửa trước khi đăng (ví dụ: mặt bị cắt ở mép, nhân vật sai nhận diện, phụ đề sai chính tả/che mặt, im lặng
bất thường giữa thoại, sai độ phân giải/thời lượng, khung đen/hỏng). Không có thì để [].

Trả lời DUY NHẤT một object JSON (không thêm chữ ngoài JSON):
{{"criteria": {example}, "blocking": ["<lỗi chặn kèm mốc giây>"], "issues": ["<lỗi nhỏ kèm mốc giây>"], "fixes": ["<cách sửa cụ thể>"]}}
"""


def prepare(ep):
    ep = Path(ep).resolve()
    video = ep / "final_video.mp4"
    if not video.exists():
        raise ReviewError("Chưa có final_video.mp4 — chạy --mux trước.")
    st = load_state(ep)
    if st["status"] in ("passed", "needs_owner"):
        # Video đã đổi sau khi đạt/gửi Owner (vd. Owner yêu cầu sửa): mở vòng review mới, lại tối đa MAX_ATTEMPTS lần.
        last = st["packets"][-1]["video_sha256"] if st["packets"] else None
        if last and _sha(video) != last:
            st["round"] = st.get("round", 1) + 1
            st["status"] = "pending"
            st.pop("reason", None)
        else:
            raise ReviewError("Review video đã ở trạng thái '%s'." % st["status"])
    n = len(st["packets"]) + 1
    out = ep / "render" / "video_review" / ("v%02d" % n)
    sheets = frame_sheets(video, out)
    packet = {"n": n, "at": _now(), "video_sha256": _sha(video), "every_s": 2.0, "sheets": sheets,
              "subs_sheet": subtitle_sheet(video, ep / "subtitle.srt", out),
              "probe": probe(video), "loudness": loudness(video), "qa": _qa(ep)}
    (out / "prompt.md").write_text(build_prompt(ep, packet), encoding="utf-8")
    packet["prompt"] = str(out / "prompt.md")
    st["packets"].append(packet)
    save_state(ep, st)
    return packet


def _sha(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def parse(obj):
    if not isinstance(obj, dict) or not isinstance(obj.get("criteria"), dict):
        raise ValueError("thiếu 'criteria'")
    want = {k: mx for k, mx, _ in RUBRIC}
    if set(obj["criteria"]) != set(want):
        raise ValueError("mục chấm không khớp: %s" % sorted(set(obj["criteria"]) ^ set(want)))
    crit = {}
    for k, mx in want.items():
        v = obj["criteria"][k]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= mx or v * 2 != int(v * 2):
            raise ValueError("điểm '%s'=%r không hợp lệ" % (k, v))
        crit[k] = float(v)
    lists = {k: [str(x) for x in (obj.get(k) or [])] for k in ("blocking", "issues", "fixes")}
    return {"criteria": crit, "total": round(sum(crit.values()), 2), **lists}


def record(ep, obj, judge="claude-subagent", ledger=None):
    ep = Path(ep).resolve()
    st = load_state(ep)
    if st["status"] in ("passed", "needs_owner"):
        raise ReviewError("Review video đã ở trạng thái '%s'." % st["status"])
    if not st["packets"]:
        raise ReviewError("Chạy `prepare` trước.")
    pk = st["packets"][-1]
    if any(a["packet"] == pk["n"] for a in st["attempts"]):
        raise ReviewError("Gói review lần %d đã được chấm; sửa video rồi `prepare` lại." % pk["n"])
    if _sha(ep / "final_video.mp4") != pk["video_sha256"]:
        raise ReviewError("final_video.mp4 đã đổi sau khi `prepare`; chạy `prepare` lại.")
    res = parse(obj)
    rnd = st.get("round", 1)
    rec = {"n": len(st["attempts"]) + 1, "round": rnd, "packet": pk["n"], "at": _now(), "judge": judge, **res,
           "passed": res["total"] >= THRESHOLD and not res["blocking"]}
    st["attempts"].append(rec)
    in_round = [a for a in st["attempts"] if a.get("round", 1) == rnd]
    if rec["passed"]:
        st["status"] = "passed"
    elif len(in_round) >= MAX_ATTEMPTS:
        st["status"] = "needs_owner"
        st["reason"] = "%d lần review chưa đạt; gửi Owner kèm điểm và lỗi còn lại" % MAX_ATTEMPTS
    save_state(ep, st)
    row = {"at": rec["at"], "episode": ep.name, "attempt": rec["n"], "total": rec["total"], "passed": rec["passed"],
           "lost": {k: round(mx - rec["criteria"][k], 2) for k, mx, _ in RUBRIC if rec["criteria"][k] < mx},
           "blocking": rec["blocking"], "issues": rec["issues"], "fixes": rec["fixes"], "judge": judge}
    with open(ledger or FINDINGS_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return st, rec


def summary(st):
    out = ["Review video: %s" % st["status"]]
    for a in st["attempts"]:
        out.append("  Lần %d (%s): %.1f/10 %s" % (a["n"], a["judge"], a["total"], "ĐẠT" if a["passed"] else "CHƯA ĐẠT"))
        for b in a["blocking"]:
            out.append("     ⛔ " + b)
        for i in a["issues"]:
            out.append("     • " + i)
    if st.get("reason"):
        out.append("  " + st["reason"])
    return "\n".join(out)


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if len(args) < 2 or args[0] not in ("prepare", "record", "status"):
        print(__doc__)
        return
    cmd, ep = args[0], args[1]
    if cmd == "prepare":
        pk = prepare(ep)
        print(json.dumps({"lan": pk["n"], "prompt": pk["prompt"], "sheets": len(pk["sheets"]), "probe": pk["probe"],
                          "loudness": {k: v for k, v in pk["loudness"].items() if k != "silences"},
                          "silences": pk["loudness"].get("silences")}, ensure_ascii=False))
    elif cmd == "record":
        judge = args[args.index("--judge") + 1] if "--judge" in args else "claude-subagent"
        obj = json.loads(Path(args[2]).read_text(encoding="utf-8"))
        st, rec = record(ep, obj, judge)
        print(summary(st))
    else:
        print(summary(load_state(ep)))


if __name__ == "__main__":
    main()
