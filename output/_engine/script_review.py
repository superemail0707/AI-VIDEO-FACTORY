"""Chấm kịch bản tự động (D-029, Giai đoạn A2).

Luồng mỗi lần thử (`epNN.py --script-review`):
  luật cứng (code) -> giám khảo độc lập chấm JSON thang 10 -> code tự cộng -> ≥ 8 thì tự duyệt cổng kịch bản.
Tối đa 3 lần thử; không được chấm lại cùng một bản kịch bản (phải sửa trước). Sau 3 lần chưa đạt -> Owner duyệt.
Cổng tự động hiệu lực khi giám khảo đã qua hiệu chỉnh (`calibrate`) với đúng phiên bản prompt, HOẶC khi tổng điểm
> 9,0/10 (> 90/100, rule Owner 13/11/2026) với bất kỳ giám khảo độc lập nào.
Mọi lần chấm (điểm mất theo mục, góp ý, lỗi luật cứng) được ghi vào sổ `script_review_findings.jsonl` (rule Owner
13/11/2026: lỗi tìm thấy phải được ghi nhận để cải tiến). Trước khi viết kịch bản mới: `python3 script_review.py findings`.
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
PROMPT_FILE = ENGINE / "prompts" / "script_judge_v2.md"   # v2 = chuẩn Viral Storyboard Agent V2.0 (D-030); v1 giữ làm lịch sử
CALIB_FILE = ENGINE / "calibration" / "script_judge_calibration.json"
THRESHOLD = 9.0                  # Quy trình chuẩn NMT v2 (Owner duyệt 18/11/2026): kịch bản chỉ qua khi ≥ 9/10
CALIB_THRESHOLD = 8.0            # ranh giới tốt/kém của bộ mẫu hiệu chỉnh (mẫu dựng theo mốc 8 cũ; không đổi theo THRESHOLD)
VIEWER_PROMPT_FILE = ENGINE / "prompts" / "viewer_panel_v1.md"
VIEWER_MIN = 20                  # hội đồng người xem: ≥ 20/24 "có" …
VIEWER_MUST = (1, 3, 5)          # … và câu 1 (hiểu topic 3 s), 3 (tắt tiếng vẫn hiểu), 5 (twist hợp lý) "có" ở cả 3 vai
OWNER_AUTO_ABOVE = 9.0           # rule Owner 13/11/2026: điểm > 90/100 thì mặc định được duyệt (kể cả giám khảo chưa hiệu chỉnh)
FINDINGS_FILE = ENGINE / "script_review_findings.jsonl"
MAX_ATTEMPTS = 3
CALIB_MIN_ACCURACY = 0.9
MAX_CHARS = 45
SPEAKERS = {"ti", "ngang"}
LABEL_RE = re.compile(r"(?<!\w)(twist|hook|cliffhanger|outro|end card|cảnh\s*\d+|khung\s*\d+|nhịp\s*\d+)(?!\w)", re.I)
DURATION_TOL = 0.15              # dung sai thời lượng ước tính trước khi có giọng thật
CONCEPT_TYPES = {"A", "B", "C"}  # Relatable / Absurd meme / Cinematic parody (Agent V2.0 mục III)
VISUAL_STYLES = set("ABCDEFG")   # Style A–G (Agent V2.0 mục VII)
COMEDY_MECHANISMS = {"expectation_vs_reality", "rule_of_three", "escalation", "visual_absurdity", "deadpan",
                     "role_reversal", "callback"}

# Thang 10 = thang 100 điểm chọn concept của Agent V2.0 chia 10 (hook 15, hình 20, twist 20, nhịp 15, đồng cảm 10, nhân vật 10, sản xuất 10)
RUBRIC_V2 = [("hook", 1.5, "Hook gây tò mò trong 3 giây đầu"),
             ("visual_comedy", 2, "Gây cười bằng hình ảnh, hiểu được khi tắt tiếng"),
             ("twist", 2, "Twist bất ngờ, hợp lý, được gieo chi tiết từ trước"),
             ("escalation", 1.5, "Giữ nhịp, 3 bước leo thang khác nhau, không lời dẫn thừa"),
             ("relatable", 1, "Đồng cảm, dễ chia sẻ, kết thúc đáng nhớ"),
             ("character_brief", 1, "Đúng tính cách/cơ chế hài từng nhân vật, Mimi không nói, giữ đúng brief"),
             ("producible", 1, "Mỗi cảnh một khoảnh khắc, khả thi tạo ảnh và dựng key pose, hợp thời lượng")]
RUBRICS = {"dialogue": RUBRIC_V2, "nondialogue": RUBRIC_V2}
FORMAT_LABEL = {"dialogue": "có thoại (hài/hội thoại)", "nondialogue": "không thoại (chill, theo nhạc, phim ngắn)"}


class ReviewError(SystemExit):
    pass


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def sha_files(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(os.path.basename(p).encode())
        with open(p, "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def prompt_version():
    return hashlib.sha256(PROMPT_FILE.read_bytes()).hexdigest()[:16]


def fmt_of(meta):
    f = (meta or {}).get("format", "dialogue")
    if f not in RUBRICS:
        raise ReviewError("META['format'] phải là dialogue hoặc nondialogue")
    return f


# ------------------------------------------------------------------ luật cứng
def hard_rules(meta, voice, scenes, starts):
    """Trả danh sách lỗi (rỗng = đạt). voice: [(vid, sid, lt, speaker, text)]; scenes: [(sid, dur, title, tr, td)]."""
    meta = meta or {}
    errs = []
    fmt = meta.get("format", "dialogue")
    for vid, sid, lt, spk, text in voice:
        if spk not in SPEAKERS:
            errs.append("%s: người nói '%s' không hợp lệ (Mimi không nói; chỉ ti/ngang)" % (vid, spk))
        if len(text.strip()) > MAX_CHARS:
            errs.append("%s: %d ký tự > %d" % (vid, len(text.strip()), MAX_CHARS))
        m = LABEL_RE.search(text)
        if m:
            errs.append("%s: đọc nhãn cấu trúc '%s' thành lời (bài học EP19)" % (vid, m.group(0)))
        if "TODO" in text:
            errs.append("%s: còn TODO" % vid)
    blob = json.dumps(meta, ensure_ascii=False)
    if "TODO" in blob:
        errs.append("META còn TODO")
    if not str(meta.get("brief") or meta.get("logline") or "").strip():
        errs.append("thiếu META['brief'] (giám khảo cần brief của Owner)")
    total = sum(s[1] for s in scenes)
    rng = meta.get("duration_s")   # D-030: thời lượng theo topic, Claude đề xuất trong brief
    if isinstance(rng, (int, float)) or (isinstance(rng, (list, tuple)) and len(rng) == 2
                                          and all(isinstance(x, (int, float)) for x in rng)):
        lo, hi = (rng, rng) if isinstance(rng, (int, float)) else rng
        lo, hi = lo * (1 - DURATION_TOL), hi * (1 + DURATION_TOL)
        if not lo <= total <= hi:
            errs.append("thời lượng ước tính %.1f s ngoài khoảng %.0f–%.0f s đã khai" % (total, lo, hi))
    else:
        errs.append("chưa khai META['duration_s'] hợp lệ (số giây hoặc [min, max], theo topic, ví dụ [55, 70])")
    errs += ideation_rules(meta)
    if scenes:
        first = scenes[0][0]
        notes = (meta.get("notes") or {}).get(first, "")
        first_lines = [v for v in voice if v[1] == first]
        opens_with_voice = first_lines and starts.get(first, 0.0) + first_lines[0][2] <= 2.0
        if not opens_with_voice and not str(notes).strip():
            errs.append("không có hook trong 2 giây đầu: cảnh %s chưa có câu mở ≤ 2 s cũng chưa mô tả hook hình" % first)
    for a in meta.get("assets", []) or []:
        if isinstance(a, dict) and not a.get("license"):
            errs.append("tài sản '%s' chưa ghi giấy phép" % a.get("name", "?"))
    return errs


def ideation_rules(meta):
    """Agent V2.0 mục III, V, VII: đủ 3 concept khác cơ chế, có điểm, chọn đúng; cơ chế hài; gieo twist; style."""
    errs = []
    ide = meta.get("ideation")
    if not isinstance(ide, dict):
        return ["thiếu META['ideation'] (3 concept A/B/C có điểm /100 và concept được chọn)"]
    cs = ide.get("concepts")
    if not isinstance(cs, list) or len(cs) != 3:
        return ["META['ideation']['concepts'] phải có đúng 3 concept"]
    names = [str(c.get("name", "")).strip() for c in cs]
    types = {str(c.get("type", "")).strip().upper() for c in cs}
    if len(set(names)) != 3 or not all(names):
        errs.append("3 concept phải có tên khác nhau")
    if types != CONCEPT_TYPES:
        errs.append("3 concept phải là A (relatable), B (absurd meme), C (cinematic parody)")
    scores = []
    for c in cs:
        sc = c.get("score")
        if isinstance(sc, bool) or not isinstance(sc, (int, float)) or not 0 <= sc <= 100:
            errs.append("concept '%s': điểm /100 không hợp lệ" % c.get("name"))
        else:
            scores.append(sc)
        for k in ("logline", "hook", "twist"):
            if not str(c.get(k, "")).strip():
                errs.append("concept '%s' thiếu %s" % (c.get("name"), k))
    chosen = str(ide.get("chosen", "")).strip()
    if chosen not in names:
        errs.append("META['ideation']['chosen'] phải là tên một trong 3 concept")
    elif len(scores) == 3 and cs[names.index(chosen)].get("score") != max(scores) and not ide.get("combined"):
        errs.append("không chọn concept điểm cao nhất mà không ghi 'combined': true và lý do")
    if not str(ide.get("reason", "")).strip():
        errs.append("thiếu lý do chọn concept")
    com = meta.get("comedy") or {}
    if com.get("main") not in COMEDY_MECHANISMS:
        errs.append("META['comedy']['main'] phải là một trong: " + ", ".join(sorted(COMEDY_MECHANISMS)))
    sup = com.get("support", [])
    if not isinstance(sup, list) or len(sup) > 2 or any(x not in COMEDY_MECHANISMS for x in sup):
        errs.append("META['comedy']['support'] tối đa 2 cơ chế hợp lệ")
    if not str(meta.get("twist_seed", "")).strip():
        errs.append("thiếu META['twist_seed'] (chi tiết gieo ở đầu làm cơ sở cho twist)")
    st = meta.get("visual_styles", [])
    if not isinstance(st, list) or not 1 <= len(st) <= 3 or any(str(x).upper() not in VISUAL_STYLES for x in st):
        errs.append("META['visual_styles'] 1–3 style trong A–G")
    return errs


# ------------------------------------------------------------------ giám khảo
def rubric_text(fmt):
    return "\n".join("- %s (tối đa %g): %s" % (k, mx, d) for k, mx, d in RUBRICS[fmt])


def build_prompt(fmt, brief, script):
    example = "{" + ", ".join('"%s": <0–%g>' % (k, mx) for k, mx, _ in RUBRICS[fmt]) + "}"
    return PROMPT_FILE.read_text(encoding="utf-8").format(
        format_label=FORMAT_LABEL[fmt], brief=brief.strip(), script=script.strip(),
        rubric=rubric_text(fmt), criteria_example=example)


def parse_judgement(obj, fmt):
    """Kiểm schema, tự cộng điểm. Sai -> ValueError."""
    if not isinstance(obj, dict) or not isinstance(obj.get("criteria"), dict):
        raise ValueError("thiếu 'criteria'")
    crit = obj["criteria"]
    want = {k: mx for k, mx, _ in RUBRICS[fmt]}
    if set(crit) != set(want):
        raise ValueError("mục chấm không khớp thang: %s" % sorted(set(crit) ^ set(want)))
    clean = {}
    for k, mx in want.items():
        v = crit[k]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= mx or (v * 2) != int(v * 2):
            raise ValueError("điểm '%s'=%r không hợp lệ (0–%g, bước 0,5)" % (k, v, mx))
        clean[k] = float(v)
    fixes = obj.get("fixes", [])
    if not isinstance(fixes, list):
        raise ValueError("'fixes' phải là danh sách")
    return {"criteria": clean, "total": round(sum(clean.values()), 2),
            "reasons": obj.get("reasons", {}) if isinstance(obj.get("reasons"), dict) else {},
            "fixes": [str(x) for x in fixes][:5]}


def codex_judge(prompt):
    import codex_client as C
    res = C.ask(prompt, mode="read-only", timeout=300)
    return {"judge": "codex", "thread_id": res.get("thread_id"), "raw": res["answer"],
            "obj": C.extract_json(res["answer"]), "seconds": res.get("seconds")}


# ------------------------------------------------------------------ hiệu chỉnh
def calibrated(judge):
    if not CALIB_FILE.exists():
        return False
    c = json.loads(CALIB_FILE.read_text(encoding="utf-8"))
    j = c.get("judges", {}).get(judge, {})
    return bool(j.get("pass")) and j.get("prompt_version") == prompt_version()


def calibrate(samples, judge_fn=None, judge="codex", write=True):
    """samples: [{"name","expected": "good"|"bad","format","brief","script"}]. Trả báo cáo; pass khi đúng ≥ 90 %."""
    judge_fn = judge_fn or codex_judge
    rows = []
    for s in samples:
        fmt = s.get("format", "dialogue")
        try:
            j = judge_fn(build_prompt(fmt, s["brief"], s["script"]))
            res = parse_judgement(j["obj"], fmt)
            ok = (res["total"] >= CALIB_THRESHOLD) == (s["expected"] == "good")
            rows.append({"name": s["name"], "expected": s["expected"], "total": res["total"], "correct": ok,
                         "criteria": res["criteria"], "fixes": res["fixes"], "thread_id": j.get("thread_id")})
        except Exception as exc:   # noqa: BLE001 — ghi lỗi từng mẫu, không dừng cả đợt
            if type(exc).__name__ == "CodexUnavailable":
                raise   # hết lượt / mất kết nối: dừng ngay, không ghi kết quả hiệu chỉnh sai lệch
            rows.append({"name": s["name"], "expected": s["expected"], "error": str(exc), "correct": False})
    acc = sum(r["correct"] for r in rows) / float(len(rows) or 1)
    rep = {"at": _now(), "judge": judge, "prompt_version": prompt_version(), "threshold": CALIB_THRESHOLD,
           "samples": len(rows), "accuracy": round(acc, 3), "pass": acc >= CALIB_MIN_ACCURACY and len(rows) >= 6,
           "rows": rows}
    if write:
        CALIB_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(CALIB_FILE.read_text(encoding="utf-8")) if CALIB_FILE.exists() else {"judges": {}}
        data["judges"][judge] = {k: rep[k] for k in ("at", "prompt_version", "accuracy", "pass", "samples")}
        data.setdefault("history", []).append(rep)
        CALIB_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


# ------------------------------------------------------------------ một lần thử
def _state_path(ep):
    return os.path.join(ep, "render", "script_review.json")


def load_state(ep):
    p = _state_path(ep)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    return {"threshold": THRESHOLD, "max_attempts": MAX_ATTEMPTS, "status": "pending", "attempts": []}


def save_state(ep, st):
    os.makedirs(os.path.join(ep, "render"), exist_ok=True)
    with open(_state_path(ep), "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=1)


def attempt(ep, gate_files, meta, voice, scenes, starts, judge_fn=None, judge_name="codex", external=None):
    """Chạy một lần thử. external: kết quả giám khảo ngoài đã có ({"judge","raw","obj","thread_id"}) — subagent Claude.
    Trả (state, attempt_record). Không tự ghi cổng; gọi gates.auto_approve khi record['passed'] và ['auto_gate_ok']."""
    st = load_state(ep)
    if st["status"] in ("passed", "needs_owner"):
        raise ReviewError("Kịch bản đã ở trạng thái '%s' (render/script_review.json)." % st["status"])
    missing = [p for p in gate_files if not os.path.exists(p)]
    if missing:
        raise ReviewError("Chạy --script trước: thiếu " + ", ".join(os.path.basename(m) for m in missing))
    sha = sha_files(gate_files)
    if any(a["sha256"] == sha for a in st["attempts"]):
        raise ReviewError("Bản kịch bản này đã được chấm; phải sửa theo góp ý rồi chạy --script lại trước khi chấm tiếp.")
    n = len(st["attempts"]) + 1
    fmt = fmt_of(meta)
    rec = {"n": n, "at": _now(), "sha256": sha, "format": fmt, "prompt_version": prompt_version()}
    errs = hard_rules(meta, voice, scenes, starts)
    rec["hard_errors"] = errs
    if errs:
        rec.update(passed=False, total=None, judge=None)
    else:
        script = open(gate_files[0], encoding="utf-8").read()
        brief = str(meta.get("brief") or meta.get("logline") or "")
        j = external or (judge_fn or codex_judge)(build_prompt(fmt, brief, script))
        res = parse_judgement(j["obj"], fmt)
        rec.update(judge=j.get("judge", judge_name), thread_id=j.get("thread_id"), raw=j.get("raw"),
                   criteria=res["criteria"], total=res["total"], reasons=res["reasons"], fixes=res["fixes"],
                   passed=res["total"] >= THRESHOLD, judge_seconds=j.get("seconds"))
    is_cal = bool(rec["passed"]) and calibrated(rec.get("judge") or "")
    above = rec.get("total") is not None and rec["total"] > OWNER_AUTO_ABOVE
    if viewer_required(meta):             # quy trình v2: rubric ≥ 9 VÀ hội đồng người xem đạt cho đúng bản này
        v = (st.get("viewer") or {}).get(sha)
        rec["viewer"] = {k: v[k] for k in ("score", "pass", "judge")} if v else None
        if rec["passed"] and not (v and v["pass"]):
            rec["passed"] = False
            rec["viewer_block"] = "hội đồng người xem chưa đạt" if v else "chưa có kết quả hội đồng người xem (--script-review viewer)"
    rec["auto_gate_ok"] = bool(rec["passed"]) and (is_cal or above)
    rec["gate_rule"] = "calibrated" if is_cal else ("owner_above_9" if rec["auto_gate_ok"] else None)
    st["attempts"].append(rec)
    record_findings(ep, rec)
    if rec["passed"] and rec["auto_gate_ok"]:
        st["status"] = "passed"
    elif rec["passed"]:
        st["status"] = "needs_owner"          # đạt điểm nhưng giám khảo chưa hiệu chỉnh -> Owner duyệt
        st["reason"] = "giám khảo '%s' chưa qua hiệu chỉnh với prompt %s" % (rec["judge"], rec["prompt_version"])
    elif n >= MAX_ATTEMPTS:
        st["status"] = "needs_owner"
        st["reason"] = "3 lần chưa đạt %g/10%s" % (THRESHOLD, " + hội đồng người xem" if viewer_required(meta) else "")
        best = max((a for a in st["attempts"] if a.get("total") is not None), key=lambda a: a["total"], default=None)
        st["best_attempt"] = best["n"] if best else None
    save_state(ep, st)
    return st, rec


# ------------------------------------------------------------------ hội đồng người xem (quy trình v2)
def viewer_required(meta):
    """Tập theo quy trình chuẩn v2 (META['process'] = 'nmt_v2') phải qua cả hội đồng người xem."""
    return (meta or {}).get("process") == "nmt_v2"


def viewer_prompt_for_subagent(ep, gate_files):
    p = os.path.join(ep, "render", "viewer_panel_prompt.md")
    script = open(gate_files[0], encoding="utf-8").read().strip()
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(VIEWER_PROMPT_FILE.read_text(encoding="utf-8").replace("[[SCRIPT]]", script))
    return p


def parse_viewer(obj):
    """Tự tính điểm/đạt từ answers (không tin 'score'/'pass' do giám khảo tự khai). Sai dạng -> ValueError."""
    roles = (obj or {}).get("roles")
    if not isinstance(roles, list) or len(roles) != 3:
        raise ValueError("cần đúng 3 vai trong 'roles'")
    yes, must_ok = 0, True
    for r in roles:
        ans = {a.get("q"): a for a in r.get("answers", []) if isinstance(a, dict)}
        if sorted(ans) != list(range(1, 9)):
            raise ValueError("vai '%s' phải trả lời đủ câu 1–8" % r.get("role"))
        for q, a in ans.items():
            if not isinstance(a.get("yes"), bool):
                raise ValueError("câu %s của vai '%s' thiếu yes true/false" % (q, r.get("role")))
            yes += a["yes"]
            if q in VIEWER_MUST and not a["yes"]:
                must_ok = False
    return {"score": yes, "max": 24, "pass": must_ok and yes >= VIEWER_MIN,
            "weakest": [str(x) for x in obj.get("weakest_scenes", [])][:5], "fixes": [str(x) for x in obj.get("fixes", [])][:5],
            "roles": roles}


def record_viewer(ep, gate_files, obj, judge="claude-subagent"):
    """Ghi kết quả hội đồng người xem cho bản kịch bản hiện tại (theo SHA). Chạy TRƯỚC lần chấm rubric cùng bản."""
    missing = [p for p in gate_files if not os.path.exists(p)]
    if missing:
        raise ReviewError("Chạy --script trước: thiếu " + ", ".join(os.path.basename(m) for m in missing))
    sha = sha_files(gate_files)
    res = parse_viewer(obj)
    res.update(at=_now(), judge=judge, sha256=sha)
    st = load_state(ep)
    st.setdefault("viewer", {})[sha] = res
    save_state(ep, st)
    return res


# ------------------------------------------------------------------ sổ lỗi (cải tiến liên tục)
def _maxes():
    return {k: mx for k, mx, _ in RUBRIC_V2}


def findings_row(ep, rec):
    """Một dòng sổ lỗi từ một lần chấm: điểm mất theo từng mục, góp ý, lỗi luật cứng."""
    crit = rec.get("criteria") or {}
    lost = {k: round(mx - crit[k], 2) for k, mx in _maxes().items() if k in crit and crit[k] < mx}
    return {"at": rec.get("at") or _now(), "episode": os.path.basename(os.path.normpath(str(ep))), "attempt": rec.get("n"),
            "sha256": rec.get("sha256"), "judge": rec.get("judge"), "total": rec.get("total"),
            "passed": bool(rec.get("passed")), "auto_gate_ok": bool(rec.get("auto_gate_ok")),
            "lost": lost, "reasons": {k: (rec.get("reasons") or {}).get(k) for k in lost},
            "fixes": rec.get("fixes") or [], "hard_errors": rec.get("hard_errors") or []}


def record_findings(ep, rec, path=None):
    """Ghi (append) một lần chấm vào sổ; bỏ qua nếu cùng tập + cùng sha đã có."""
    path = Path(path or FINDINGS_FILE)
    row = findings_row(ep, rec)
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                old = json.loads(line)
            except ValueError:
                continue
            if old.get("episode") == row["episode"] and old.get("sha256") == row["sha256"]:
                return False
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return True


def backfill_findings(output_dir, path=None):
    """Nạp các lần chấm cũ từ output/ep*/render/script_review.json vào sổ (không trùng)."""
    n = 0
    for st_p in sorted(Path(output_dir).glob("ep*/render/script_review*.json")):
        try:
            st = json.loads(st_p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for rec in st.get("attempts", []):
            n += record_findings(st_p.parents[1], rec, path)
    return n


def findings_summary(path=None, last=None):
    """Tổng hợp sổ lỗi: mục mất điểm nhiều nhất (tổng, số lần), góp ý gần nhất. Đọc trước khi viết kịch bản mới."""
    path = Path(path or FINDINGS_FILE)
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    if last:
        rows = rows[-last:]
    agg = {}
    for r in rows:
        for k, v in (r.get("lost") or {}).items():
            a = agg.setdefault(k, [0.0, 0])
            a[0] += v
            a[1] += 1
    order = sorted(agg.items(), key=lambda kv: -kv[1][0])
    out = ["Sổ lỗi chấm kịch bản: %d lần chấm" % len(rows)]
    for k, (tot, cnt) in order:
        out.append("  %-16s mất %.1f điểm qua %d lần" % (k, tot, cnt))
    hard = [e for r in rows for e in r.get("hard_errors", [])]
    if hard:
        out.append("  Lỗi luật cứng: %d (gần nhất: %s)" % (len(hard), hard[-1]))
    out.append("Góp ý gần nhất:")
    for r in rows[-4:]:
        for f in r.get("fixes", [])[:3]:
            out.append("  [%s lần %s] %s" % (r.get("episode"), r.get("attempt"), f))
    return "\n".join(out)


def judge_prompt_for_subagent(ep, gate_files, meta):
    """Ghi prompt giám khảo ra file để subagent Claude KHÔNG có ngữ cảnh chấm khi Codex không dùng được."""
    fmt = fmt_of(meta)
    p = os.path.join(ep, "render", "script_review_prompt.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(build_prompt(fmt, str(meta.get("brief") or meta.get("logline") or ""),
                              open(gate_files[0], encoding="utf-8").read()))
    return p


def summary_text(st):
    out = ["Trạng thái chấm: %s" % st["status"]]
    for a in st["attempts"]:
        if a["hard_errors"]:
            out.append("  Lần %d: LUẬT CỨNG — %s" % (a["n"], "; ".join(a["hard_errors"])))
        else:
            out.append("  Lần %d: %s %.1f/10 (%s)%s%s" % (a["n"], a["judge"], a["total"],
                       ", ".join("%s %g" % kv for kv in a["criteria"].items()),
                       "" if a["auto_gate_ok"] or not a["passed"] else " — chưa hiệu chỉnh",
                       (" · người xem %s/24" % a["viewer"]["score"]) if a.get("viewer") else ""))
            if a.get("viewer_block"):
                out.append("     ⛔ " + a["viewer_block"])
            for f in a.get("fixes", []):
                out.append("     • " + f)
    if st.get("reason"):
        out.append("  Lý do chuyển Owner: " + st["reason"])
    return "\n".join(out)


def main(argv=None):
    """python3 script_review.py calibrate [samples.json] — chấm bộ mẫu bằng Codex (TIÊU LƯỢT CODEX, ~15 lần gọi).
python3 script_review.py findings [N]   — tổng hợp sổ lỗi (N lần chấm gần nhất); đọc trước khi viết kịch bản mới.
python3 script_review.py backfill       — nạp các lần chấm cũ của output/ep*/ vào sổ lỗi."""
    import sys
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] == "findings":
        print(findings_summary(last=int(args[1]) if len(args) > 1 else None))
        return
    if args and args[0] == "backfill":
        print("Đã nạp %d lần chấm vào %s" % (backfill_findings(ENGINE.parent), FINDINGS_FILE))
        return
    if not args or args[0] != "calibrate":
        print(main.__doc__)
        return
    src = args[1] if len(args) > 1 else str(ENGINE / "calibration" / "script_judge_samples.json")
    with open(src, encoding="utf-8") as fh:
        samples = json.load(fh)
    import codex_client as C
    try:
        rep = calibrate(samples)
    except C.CodexUnavailable as exc:
        raise SystemExit("DỪNG hiệu chỉnh: Codex không dùng được (%s). Không ghi kết quả." % str(exc)[:300])
    for r in rep["rows"]:
        print("%-24s %-4s %-5s %s" % (r["name"], r["expected"], r.get("total", "LỖI"), "ĐÚNG" if r["correct"] else "SAI " + r.get("error", "")))
    print(json.dumps({k: rep[k] for k in ("judge", "prompt_version", "accuracy", "pass", "samples")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
