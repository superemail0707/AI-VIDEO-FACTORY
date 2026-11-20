"""Tạo tranh cảnh tự động bằng image_gen qua Codex (D-029, Giai đoạn A2).

`epNN.py --art-auto [CẢNH …] [--fix "mô tả lỗi"]`:
  đọc art/PROMPTS_vNN.md (khối `### <CẢNH> — …` + ```prompt```) -> mỗi cảnh một phiên Codex workspace-write mới
  -> nhận PNG tại art/vNN/<CẢNH>.png -> kiểm giải mã, SHA mới, không ghi file lạ -> generated_art.archive
  -> kiểm máy (độ phủ, tỉ lệ, trùng cảnh khác) -> lỗi thì tạo lại kèm mô tả lỗi, tối đa 3 lần/cảnh.
Ngân sách mỗi tập: 3 × số cảnh + 3 lượt. Hết lượt / Codex lỗi -> dừng và báo (không dịch vụ trả phí, không đăng nhập thay Owner).
Bản cũ không bị ghi đè: đổi tên <CẢNH>_aNN_superseded.png trước khi tạo lại.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageOps

ENGINE = Path(__file__).resolve().parent
ROOT = ENGINE.parents[1]
TEMPLATE = ENGINE / "prompts" / "art_scene_v1.md"
CODEX_IMAGES = Path(os.path.expanduser("~/.codex/generated_images"))
MAX_PER_SCENE = 3
LIBRARY = Path(os.environ.get("AVF_ART_LIBRARY", str(ROOT / "character_library")))   # thử nghiệm: trỏ thư mục tạm
BLOCK_RE = re.compile(r"^###\s+([A-Za-z0-9_.-]+)[^\n]*\n+```[a-z]*\n(.*?)\n```", re.M | re.S)


class ArtStop(SystemExit):
    pass


def parse_prompts(path):
    """{cảnh: prompt} theo thứ tự trong file."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for sid, body in BLOCK_RE.findall(text):
        out[sid] = body.strip()
    if not out:
        raise ArtStop("Không đọc được khối prompt nào trong %s (cần '### A01 — …' + khối ```)." % path)
    return out


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _log_path(ep):
    return Path(ep) / "render" / "art_auto_log.jsonl"


def read_log(ep):
    p = _log_path(ep)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def _log(ep, row):
    p = _log_path(ep)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(dict(at=time.strftime("%Y-%m-%dT%H:%M:%S"), **row), ensure_ascii=False) + "\n")


def budget(ep, n_scenes):
    used = sum(1 for r in read_log(ep) if r.get("called_codex"))
    return used, 3 * n_scenes + 3


def scene_attempts(ep, sid, revision):
    return sum(1 for r in read_log(ep) if r.get("scene") == sid and r.get("revision") == revision and r.get("called_codex"))


def _git_dirty():
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT), capture_output=True, text=True, timeout=60)
        return set(r.stdout.splitlines())
    except (OSError, subprocess.SubprocessError):
        return set()


def _codex_images():
    return {p: p.stat().st_mtime for p in CODEX_IMAGES.rglob("*.png")} if CODEX_IMAGES.exists() else {}


def machine_check(png, others):
    """Kiểm phần máy đo được (không cần chú thích): độ phủ, tỉ lệ, trùng cảnh khác. Trả danh sách lỗi."""
    import numpy as np
    import qa_checks as Q
    src = Image.open(png)
    sw, sh = src.size
    fit = ImageOps.fit(src.convert("RGBA"), (Q.W, Q.H), Image.Resampling.LANCZOS)
    errs = []
    cov, margins = Q.coverage(fit)
    if cov < Q.COVER_MIN:
        errs.append("image has blank/cream margins (coverage %.0f%%, margins %s): make it full-bleed" % (100 * cov, margins))
    ratio = sw / float(sh)
    if ratio > 0.70:
        errs.append("image is not portrait enough (%dx%d): generate a tall portrait image" % (sw, sh))
    me = np.asarray(fit.convert("L").resize((108, 192)), dtype=np.float32)
    for name, path in others.items():
        o = np.asarray(ImageOps.fit(Image.open(path).convert("L"), (108, 192)), dtype=np.float32)
        if float(np.abs(me - o).mean()) < Q.DUP_DIFF:
            errs.append("image repeats scene %s: compose a clearly different, new scene" % name)
    return errs


def generate_scene(ep, episode, revision, sid, scene_prompt, refs, fix_note="", ask=None):
    """Một lượt tạo cho một cảnh. Trả record log. ask: thay codex_client.ask (test)."""
    import codex_client as C
    ask = ask or C.ask
    art_dir = Path(ep) / "art" / revision
    art_dir.mkdir(parents=True, exist_ok=True)
    target = art_dir / (sid + ".png")
    n = scene_attempts(ep, sid, revision) + 1
    if target.exists():
        keep = art_dir / ("%s_a%02d_superseded.png" % (sid, n - 1 if n > 1 else 0))
        i = 0
        while keep.exists():
            i += 1
            keep = art_dir / ("%s_a%02d_superseded_%d.png" % (sid, n - 1, i))
        target.rename(keep)
    prompt = TEMPLATE.read_text(encoding="utf-8").format(
        references="\n".join("   - %s" % r for r in refs) or "   - (none: follow the character descriptions in the scene prompt)",
        target=str(target), scene_prompt=scene_prompt,
        fix_note=("\nFIX FROM PREVIOUS ATTEMPT (mandatory): " + fix_note + "\n") if fix_note else "")
    before_git, before_img = _git_dirty(), _codex_images()
    rec = {"episode": episode, "revision": revision, "scene": sid, "attempt": n, "called_codex": True,
           "fix_note": fix_note or None}
    try:
        res = ask(prompt, mode="workspace-write", timeout=600)
    except C.CodexUnavailable as exc:
        rec.update(status="codex_unavailable", error=str(exc))
        _log(ep, rec)
        return rec
    rec.update(thread_id=res.get("thread_id"), seconds=res.get("seconds"))
    if not target.exists():   # Codex tạo ảnh nhưng không chép: lấy ảnh mới nhất trong ~/.codex/generated_images
        new = [p for p, m in _codex_images().items() if p not in before_img or m > before_img[p]]
        if new:
            src = max(new, key=lambda p: p.stat().st_mtime)
            shutil.copyfile(src, target)
            rec["copied_from"] = str(src)
    if not target.exists():
        rec.update(status="no_image", answer=str(res.get("answer"))[:500])
        _log(ep, rec)
        return rec
    try:
        with Image.open(target) as im:
            fmt, size = im.format, im.size
            im.verify()
        if fmt != "PNG":
            orig = target.with_suffix(".orig." + (fmt or "img").lower())
            target.rename(orig)
            Image.open(orig).save(target, "PNG")
            rec["converted_from"] = str(orig.name)
    except Exception as exc:  # noqa: BLE001
        rec.update(status="bad_image", error=str(exc))
        _log(ep, rec)
        return rec
    stray = sorted(x for x in (_git_dirty() - before_git) if str(art_dir.relative_to(ROOT)) not in x
                   and "render/art_auto_log" not in x)
    rec.update(size=list(size), sha256=_sha(target), stray_changes=stray)
    others = {p.stem: p for p in art_dir.glob("*.png") if p.stem != sid and "superseded" not in p.stem
              and not p.stem.startswith("_")}
    errs = machine_check(target, others)
    rec.update(machine_errors=errs, status="ok" if not errs and not stray else ("stray_files" if stray else "check_failed"))
    try:
        import generated_art as GA
        a = GA.archive(library=LIBRARY, episode=episode, revision=revision, scene=sid, image=target, prompt=scene_prompt,
                       tool="image_gen (codex app-server)", references=[str(r) for r in refs],
                       characters=["ti", "ngang", "mimi"])
        rec["archive_id"] = a["asset_id"]
    except Exception as exc:  # noqa: BLE001 — lưu trữ lỗi không làm mất ảnh
        rec["archive_error"] = str(exc)
    _log(ep, rec)
    return rec


def run(ep, episode, revision, prompts_file, scenes=None, refs=(), fix_note="", ask=None):
    """Tạo các cảnh (mặc định: cảnh chưa có ảnh). Tự tạo lại khi máy kiểm lỗi, tối đa 3 lượt/cảnh. Trả báo cáo."""
    prompts = parse_prompts(prompts_file)
    todo = list(scenes) if scenes else [s for s in prompts if not (Path(ep) / "art" / revision / (s + ".png")).exists()]
    unknown = [s for s in todo if s not in prompts]
    if unknown:
        raise ArtStop("Cảnh không có trong %s: %s" % (prompts_file, ", ".join(unknown)))
    report = {"scenes": {}, "stopped": None}
    for sid in todo:
        note = fix_note
        while True:
            used, cap = budget(ep, len(prompts))
            if used >= cap:
                report["stopped"] = "hết ngân sách %d/%d lượt image_gen của tập" % (used, cap)
                return report
            if scene_attempts(ep, sid, revision) >= MAX_PER_SCENE:
                report["scenes"][sid] = {"status": "needs_owner", "reason": "3 lượt chưa đạt"}
                break
            rec = generate_scene(ep, episode, revision, sid, prompts[sid], refs, fix_note=note, ask=ask)
            report["scenes"][sid] = rec
            if rec["status"] == "codex_unavailable":
                report["stopped"] = "Codex không dùng được: %s" % rec.get("error")
                return report
            if rec["status"] in ("ok", "stray_files"):
                break
            note = "; ".join(rec.get("machine_errors") or [rec["status"]])
    return report
