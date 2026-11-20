"""Thống kê token Claude đã dùng cho từng tập NMT (Owner 19/11/2026: phân tích, tối ưu chi phí mà vẫn giữ chất lượng).

Đọc transcript Claude Code (~/.claude/projects/<dự án>/*.jsonl, kể cả subagents/*.jsonl), lấy `message.usage` của mỗi
lượt trả lời (khử trùng theo message.id), rồi gán lượt đó cho tập được nhắc gần nhất (đường dẫn `epNN_...` trong lời gọi
công cụ / kết quả). Subagent được gán theo tập xuất hiện trong prompt của nó. Không gọi mạng, không đọc secret.

    python3 output/_engine/token_report.py                # bảng theo tập
    python3 output/_engine/token_report.py --json out.json

Giới hạn: chỉ thấy transcript còn lưu trên máy (phiên đã xoá thì không tính); không tính token Codex/ChatGPT web;
lượt không nhắc tập nào gom vào "khác". Gán theo "tập được nhắc gần nhất" nên là ước lượng, sai số ở chỗ chuyển tập.
"""
import argparse
import glob
import json
import os
import re
from collections import defaultdict

PROJ = os.path.expanduser("~/.claude/projects/-Users-tthanhtaicntt-AI-Projects-AI-VIDEO-FACTORY")
EP_RE = re.compile(r"\b(ep\d{2}[a-z]?)_[a-z0-9_]+")
PHASES = (("script", re.compile(r"--script|script_review|viewer_panel|review_rubric|review_viewer")),
          ("art", re.compile(r"chatgpt_art|PROMPTS_v|--check-art|safe_annotations|art_fit|art/v0|THUMBNAIL|thumbnail")),
          ("render", re.compile(r"--storyboard|--render|--audio|--mux|_scenes\.py|--tts|contact_sheet")),
          ("review", re.compile(r"video_review|--metrics")),
          ("export", re.compile(r"--export|post\.json|library")))
KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def _texts(rec):
    m = rec.get("message") or {}
    c = m.get("content")
    if isinstance(c, str):
        yield c
    elif isinstance(c, list):
        for b in c:
            if b.get("type") == "text":
                yield b.get("text", "")
            elif b.get("type") == "tool_use":
                yield json.dumps(b.get("input", {}), ensure_ascii=False)
            elif b.get("type") == "tool_result":
                cc = b.get("content")
                yield cc if isinstance(cc, str) else json.dumps(cc, ensure_ascii=False)[:20000]


def _last_ep(text):
    hits = EP_RE.findall(text)
    return hits[-1] if hits else None


def scan_file(path, fixed_ep=None):
    """[(ep, phase, model, usage dict)] cho mỗi lượt trả lời (khử trùng message.id)."""
    out, seen, cur, phase = [], set(), fixed_ep, "khác"
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            txt = "\n".join(_texts(rec))
            if not fixed_ep:
                e = _last_ep(txt)
                if e:
                    cur = e
            for name, rx in PHASES:
                if rx.search(txt):
                    phase = name
            m = rec.get("message") or {}
            u = m.get("usage")
            if rec.get("type") != "assistant" or not u:
                continue
            mid = m.get("id") or rec.get("uuid")
            if mid in seen:
                continue
            seen.add(mid)
            out.append((cur or "khác", phase, m.get("model", "?"), {k: int(u.get(k) or 0) for k in KEYS}))
    return out


def _subagent_ep(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") == "user":
                return _last_ep("\n".join(_texts(rec)))
    return None


def report(proj=PROJ):
    rows = []
    for f in sorted(glob.glob(os.path.join(proj, "*.jsonl"))):
        rows += [r + ("main",) for r in scan_file(f)]
    for f in sorted(glob.glob(os.path.join(proj, "*", "subagents", "*.jsonl"))):
        rows += [r + ("subagent",) for r in scan_file(f, fixed_ep=_subagent_ep(f))]
    agg = defaultdict(lambda: defaultdict(int))
    for ep, phase, model, u, kind in rows:
        a = agg[ep]
        a["turns"] += 1
        a["subagent_turns"] += kind == "subagent"
        for k in KEYS:
            a[k] += u[k]
            a["%s:%s" % (phase, k)] += u[k]
        a["model:" + model] += 1
    return {ep: dict(v) for ep, v in sorted(agg.items())}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--proj", default=PROJ)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    rep = report(a.proj)
    if a.json:
        json.dump(rep, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%-8s %6s %6s %12s %12s %14s %10s" % ("tập", "lượt", "sub", "input", "cache_write", "cache_read", "output"))
    for ep, v in rep.items():
        print("%-8s %6d %6d %12d %12d %14d %10d" % (ep, v["turns"], v["subagent_turns"], v["input_tokens"],
              v["cache_creation_input_tokens"], v["cache_read_input_tokens"], v["output_tokens"]))


if __name__ == "__main__":
    main()
