"""Đo đạc mỗi tập (Giai đoạn A): thời gian từng bước, vòng duyệt, số dòng code Claude viết.

Mỗi lệnh epNN.py --<bước> ghi một dòng vào render/metrics.jsonl (tự động, trong cute_engine.main).
`epNN.py --metrics` tổng hợp ra render/metrics.json.
Token Claude KHÔNG đo được từ engine: để null, chỉ điền khi có số thật (ghi tay vào render/metrics_manual.json).
"""
import json
import os
import time


def record(out_dir, step, seconds, status="ok", **extra):
    if not out_dir:
        return
    p = os.path.join(out_dir, "render", "metrics.jsonl")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    row = dict(at=time.strftime("%Y-%m-%dT%H:%M:%S"), step=step, seconds=round(seconds, 2), status=status, **extra)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _lines(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if ln.strip() and not ln.strip().startswith("#"))
    except OSError:
        return 0


def _jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def summary(out_dir, write=True):
    r = os.path.join(out_dir, "render")
    ep = os.path.basename(os.path.abspath(out_dir))
    n = ep[2:4] if ep.startswith("ep") else ""
    code = {f: _lines(os.path.join(r, f)) for f in sorted(os.listdir(r))
            if f.endswith(".py") and f.startswith("ep%s" % n)} if os.path.isdir(r) else {}
    steps = {}
    for row in _jsonl(os.path.join(r, "metrics.jsonl")):
        s = steps.setdefault(row["step"], {"runs": 0, "seconds": 0.0, "failed": 0})
        s["runs"] += 1
        s["seconds"] = round(s["seconds"] + row.get("seconds", 0.0), 2)
        s["failed"] += row.get("status") not in ("ok", "passed")
    render = _jsonl(os.path.join(r, "render_log.jsonl"))
    wf_p = os.path.join(out_dir, "workflow.json")
    gates = {}
    if os.path.exists(wf_p):
        with open(wf_p, encoding="utf-8") as fh:
            hist = json.load(fh).get("history", [])
        for h in hist:
            st = h.get("stage")
            if not st:
                continue
            g = gates.setdefault(st, {"submitted": 0, "approved": 0, "rejected": 0, "auto_approved": 0})
            ev = h.get("event")
            if ev in g:
                g[ev] += 1
            if ev == "approved" and str(h.get("by", "")).startswith("auto-review"):
                g["auto_approved"] += 1
    sr_p = os.path.join(r, "script_review.json")
    script_review = None
    if os.path.exists(sr_p):
        with open(sr_p, encoding="utf-8") as fh:
            sr = json.load(fh)
        script_review = {"status": sr.get("status"), "attempts": len(sr.get("attempts", [])),
                         "scores": [a.get("total") for a in sr.get("attempts", [])],
                         "judges": sorted({a.get("judge") for a in sr.get("attempts", []) if a.get("judge")})}
    art_rows = _jsonl(os.path.join(r, "art_auto_log.jsonl"))
    art_auto = {"codex_calls": sum(1 for x in art_rows if x.get("called_codex")),
                "ok": sum(1 for x in art_rows if x.get("status") == "ok"),
                "by_status": {s: sum(1 for x in art_rows if x.get("status") == s) for s in {x.get("status") for x in art_rows}}}
    manual_p = os.path.join(r, "metrics_manual.json")
    manual = {}
    if os.path.exists(manual_p):
        with open(manual_p, encoding="utf-8") as fh:
            manual = json.load(fh)
    rep = {"episode": ep, "code_lines": code, "code_lines_total": sum(code.values()),
           "steps": steps, "render_seconds_logged": round(sum(x.get("render_s", 0) for x in render), 1),
           "gates": gates,
           "revision_rounds": {k: v["rejected"] for k, v in gates.items()},
           "script_review": script_review, "art_auto": art_auto,
           "claude_tokens": manual.get("claude_tokens"),
           "notes": "claude_tokens chỉ có khi ghi tay số đo thật vào render/metrics_manual.json"}
    if write:
        with open(os.path.join(r, "metrics.json"), "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
    return rep
