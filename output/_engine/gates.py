"""Quy trình chuẩn có cổng duyệt cho engine làm tay (Owner yêu cầu 07/11/2026).

  1. script   : Claude viết kịch bản  -> script.md + lines.json      -> CHỜ Owner duyệt kịch bản
  2. visual   : (đã duyệt 1) tạo giọng + khung hình mẫu từng cảnh   -> CHỜ Owner duyệt hình ảnh
  3. render   : (đã duyệt 1+2, file không đổi) render cảnh, âm thanh, ghép MP4
  4. final    : Owner duyệt bản MP4 cuối (trước khi đưa vào pipeline đăng)

Mỗi lần duyệt lưu SHA-256 của các file được duyệt. Sửa file sau khi duyệt -> cổng tự mở lại, phải duyệt lại.
"""
import hashlib
import json
import os
import time

ORDER = ["script", "visual", "final"]
LABEL = {"script": "kịch bản", "visual": "hình ảnh", "final": "video cuối"}


class GateBlocked(SystemExit):
    pass


def _wf_path(ep):
    return os.path.join(ep, "workflow.json")


def load(ep):
    p = _wf_path(ep)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return {"state": "drafting_script", "approvals": {}, "history": []}


def save(ep, wf):
    json.dump(wf, open(_wf_path(ep), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _sha(paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(os.path.basename(p).encode())
        h.update(open(p, "rb").read() if os.path.exists(p) else b"<missing>")
    return h.hexdigest()


def gated_files(ep, stage, episode_py):
    r = os.path.join(ep, "render")
    if stage == "script":
        return [os.path.join(r, "script.md"), os.path.join(r, "lines.json")]
    if stage == "visual":
        return [episode_py, os.path.join(ep, "contact_sheet.png")]
    if stage == "final":
        return [os.path.join(ep, "final_video.mp4")]
    raise ValueError(stage)


def log(ep, wf, event, **kw):
    wf["history"].append(dict(at=time.strftime("%Y-%m-%dT%H:%M:%S"), event=event, **kw))
    save(ep, wf)


def is_approved(ep, wf, stage, episode_py):
    a = wf["approvals"].get(stage)
    return bool(a and a.get("status") == "approved" and a.get("sha256") == _sha(gated_files(ep, stage, episode_py)))


def require(ep, stage, episode_py, action):
    """Chặn `action` nếu `stage` chưa được duyệt hoặc file đã đổi sau khi duyệt."""
    wf = load(ep)
    a = wf["approvals"].get(stage)
    if not a or a.get("status") != "approved":
        raise GateBlocked("CHẶN: '%s' cần Owner duyệt %s trước. Trạng thái: %s" % (action, LABEL[stage], wf["state"]))
    if a.get("sha256") != _sha(gated_files(ep, stage, episode_py)):
        raise GateBlocked("CHẶN: %s đã thay đổi sau khi duyệt (%s). Cần Owner duyệt lại." % (LABEL[stage], a.get("at")))


def submit(ep, stage, episode_py, next_state):
    wf = load(ep)
    wf["approvals"].pop(stage, None)
    for later in ORDER[ORDER.index(stage) + 1:]:   # duyệt sau bị vô hiệu khi bước trước đổi
        wf["approvals"].pop(later, None)
    wf["state"] = next_state
    log(ep, wf, "submitted", stage=stage, sha256=_sha(gated_files(ep, stage, episode_py)))


def decide(ep, stage, episode_py, decision, note="", by="owner"):
    wf = load(ep)
    if stage != ORDER[0]:
        prev = ORDER[ORDER.index(stage) - 1]
        if not is_approved(ep, wf, prev, episode_py):
            raise GateBlocked("CHẶN: chưa thể duyệt %s khi %s chưa được duyệt." % (LABEL[stage], LABEL[prev]))
    files = gated_files(ep, stage, episode_py)
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        raise GateBlocked("CHẶN: thiếu file để duyệt: %s" % ", ".join(os.path.basename(m) for m in missing))
    rec = {"status": decision, "sha256": _sha(files), "by": by, "note": note, "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "files": [os.path.relpath(f, ep) for f in files]}
    wf["approvals"][stage] = rec
    if decision == "approved":
        wf["state"] = {"script": "script_approved", "visual": "visual_approved", "final": "final_approved"}[stage]
    else:
        wf["state"] = {"script": "drafting_script", "visual": "revising_visual", "final": "revising_video"}[stage]
    log(ep, wf, decision, stage=stage, note=note, by=by)
    return wf
