"""Lưu hình đã được Owner duyệt trong video vào thư viện nhân vật để tham khảo và dùng lại (quy tắc Owner 07/11/2026):
  "Tất cả ảnh duyệt trong video thì cần lưu vào thư viện để tham khảo sau này tránh lỗi.
   Nếu có lỗi hình ảnh và fix thì cần cập nhật lại hình."

- sync(E, OUT): chạy sau khi tập đã được duyệt video cuối. Lưu mọi sprite GHÉP/SỬA trong tập (không có sẵn trong thư viện)
  vào character_library/episode_approved/<tập>/<asset_id>.png và thêm/ cập nhật mục trong asset_index.json.
  Ghi usage.json: sprite gốc của thư viện được dùng ở tập nào.
- register(...): ghi một phiên bản (approved / pending_owner_review / superseded) với ghi chú lỗi.
- Khi hình đổi (sha khác): bản cũ được CHUYỂN vào _superseded/<id>__v<n>.png, mục cũ đổi trạng thái 'superseded'
  (engine không cho dùng), bản mới tăng version. Không xoá file nào.
- sync_scene_art(out_dir): (quy tắc Owner 12/11/2026 "bất kỳ video cuối nào được tạo thì thêm hình vào thư viện")
  lưu mọi tranh cảnh full-bleed mà renderer của tập dùng qua art('<tên>') vào episode_approved/<tập>/ với
  asset_category 'episode_scene_art', kèm contact_sheet.jpg và mục 'scene_art' trong usage.json.
  Siêu dữ liệu lấy từ LIBRARY_ART trong <tập>_scenes.py nếu có; thiếu thì tự đặt mã <EPnn>_SCENE_<tên>.
- Engine tự gọi sync() (gồm sync_scene_art) ngay sau --export-finish, nên tập nào xuất xong cũng có hình trong thư viện.
Dùng tay: python3 output/<tập>/render/<tập>.py --library-sync"""
import datetime
import hashlib
import json
import os
import re
import shutil

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.abspath(os.path.join(HERE, "..", "..", "character_library"))
INDEX_P = os.path.join(LIB, "asset_index.json")


def _now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _sha_img(im):
    return hashlib.sha256(np.asarray(im.convert("RGBA")).tobytes()).hexdigest()


def _load():
    return json.load(open(INDEX_P, encoding="utf-8"))


def _save(idx):
    bak = os.path.join(LIB, "metadata_backups")
    os.makedirs(bak, exist_ok=True)
    b = os.path.join(bak, "asset_index.%s.json" % datetime.date.today().isoformat())
    if not os.path.exists(b):
        shutil.copyfile(INDEX_P, b)
    tmp = INDEX_P + ".part"
    json.dump(idx, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, INDEX_P)


def register(idx, asset_id, im, episode, status, note, base_entry=None, extra=None):
    """Thêm hoặc cập nhật một hình. Trả 'new' | 'same' | 'updated'."""
    d = os.path.join(LIB, "episode_approved", episode)
    os.makedirs(d, exist_ok=True)
    rel = os.path.relpath(os.path.join(d, asset_id + ".png"), LIB)
    sha = _sha_img(im)
    cur = [a for a in idx if a["asset_id"] == asset_id]
    if cur and cur[0].get("pixel_sha256") == sha:
        if cur[0].get("approval_status") != status or cur[0].get("note") != note:
            cur[0].update({"approval_status": status, "note": note, "updated_at": _now()})
            return "status"
        return "same"
    ver = 1
    if cur:
        old = cur[0]
        ver = int(old.get("version", 1)) + 1
        sd = os.path.join(d, "_superseded")
        os.makedirs(sd, exist_ok=True)
        src = os.path.join(LIB, old["image_path"])
        dst_rel = os.path.relpath(os.path.join(sd, "%s__v%d.png" % (asset_id, old.get("version", 1))), LIB)
        if os.path.exists(src) and old["image_path"].startswith("episode_approved/"):
            shutil.move(src, os.path.join(LIB, dst_rel))
        hist = dict(old, asset_id="%s__v%d" % (asset_id, old.get("version", 1)), image_path=dst_rel,
                    approval_status="superseded", superseded_at=_now(), superseded_by="%s v%d" % (asset_id, ver))
        idx[idx.index(old)] = hist
    im.save(os.path.join(LIB, rel))
    b = base_entry or {}
    e = {"asset_id": asset_id, "character_id": b.get("character_id"), "character_name": b.get("character_name"),
         "asset_category": "episode_composite", "outfit": b.get("outfit"), "story_context": b.get("story_context"),
         "intended_use": ["storyboard", "compositing_preview", "reference"], "style_version": b.get("style_version", "Style C"),
         "image_path": rel, "background_type": "transparent", "approval_status": status,
         "consistency_check": "owner_final_video_approved" if status == "approved" else status,
         "source_episode": episode, "derived_from": b.get("asset_id"), "version": ver, "note": note,
         "created_at": _now(), "pixel_size": list(im.size), "pixel_sha256": sha}
    if extra:
        e.update(extra)
    idx.append(e)
    return "updated" if ver > 1 else "new"


def sync(E, out_dir, overrides=None):
    """overrides: {asset_id: {"status": ..., "note": ..., "image": PIL (tuỳ chọn, thay ảnh đang dựng)}}"""
    import gates as G
    episode = os.path.basename(out_dir.rstrip("/"))
    wf = G.load(out_dir)
    if wf.get("approvals", {}).get("final", {}).get("status") != "approved":
        raise SystemExit("Tập %s chưa được duyệt video cuối: chưa lưu hình vào thư viện." % episode)
    idx = _load()
    lib_ids = {a["asset_id"] for a in idx if not a.get("source_episode")}
    overrides = overrides or {}
    res = {}
    for k in sorted(E.INDEX):
        if k in lib_ids or k not in E._raw:
            continue
        ov = overrides.get(k, {})
        im = ov.get("image", E._raw[k])
        base = E.INDEX[k]
        st = ov.get("status", "approved")
        note = ov.get("note", base.get("note") or "sprite ghép trong tập %s, Owner duyệt video cuối" % episode)
        extra = {"pad_top_px": im.info.get("pad_top_px", base.get("pad_top_px", 0))}
        res[k] = register(idx, k, im, episode, st, note, base, extra)
    _save(idx)
    # sprite gốc của thư viện được dùng trong tập
    src = "".join(open(os.path.join(out_dir, "render", f), encoding="utf-8").read()
                  for f in os.listdir(os.path.join(out_dir, "render")) if f.endswith(".py"))
    used = sorted({m for m in re.findall(r"\b(?:TI|NGANG|MIMI|NG)_[A-Z_]+_\d{3}\b|\b(?:TI|NGANG|MIMI)_[A-Z]+_LOCAL_[A-Z_]+\b", src)
                   if m in lib_ids} | {k for k in E._raw if k in lib_ids})
    d = os.path.join(LIB, "episode_approved", episode)
    os.makedirs(d, exist_ok=True)
    up = os.path.join(d, "usage.json")
    prev = json.load(open(up, encoding="utf-8")) if os.path.exists(up) else {}
    scene = sync_scene_art(out_dir, wf)
    usage = dict(prev, episode=episode, final_approved_at=wf["approvals"]["final"].get("at"),
                 library_assets_used=sorted(set(used) | set(prev.get("library_assets_used", []))),
                 episode_assets=dict(prev.get("episode_assets", {}), **res), synced_at=_now())
    if scene:
        usage["scene_art"] = scene
    json.dump(usage, open(up, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return dict(res, **{k: v["result"] for k, v in scene.items()}), used


def _scenes_meta(out_dir):
    """(thư mục tranh, [tên tranh dùng qua art('...')], LIBRARY_ART) đọc từ *_scenes.py của tập (không import)."""
    rd = os.path.join(out_dir, "render")
    srcs = [open(os.path.join(rd, f), encoding="utf-8").read() for f in sorted(os.listdir(rd)) if f.endswith("_scenes.py")]
    src = "\n".join(srcs)
    m = re.search(r"ART\s*=\s*EP\s*/\s*'art'\s*/\s*'([\w.-]+)'", src)
    art_dir = os.path.join(out_dir, "art", m.group(1) if m else "v01")
    names = sorted(set(re.findall(r"\bart\(\s*'([\w.-]+)'\s*\)", src)))
    meta = {}
    # Bài học EP27: tìm phép gán bằng ast (không phụ thuộc '}' đứng đầu dòng như regex cũ)
    import ast
    expr = None
    for one in srcs:
        try:
            tree = ast.parse(one)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "LIBRARY_ART" for t in node.targets):
                expr = ast.get_source_segment(one, node.value)
    if expr is None:
        m2 = re.search(r"^LIBRARY_ART\s*=\s*(\{.*?^\})", src, re.S | re.M)
        expr = m2.group(1) if m2 else None
    if expr:
        meta = _literal_with_consts(expr, src)
    # tranh gọi qua biến (vd. ô montage EP20: art(name)) không khớp regex → lấy thêm theo khai báo LIBRARY_ART
    names = sorted(set(names) | {k for k in meta if os.path.exists(os.path.join(art_dir, k + ".png"))})
    return art_dir, names, meta


def _literal_with_consts(expr, src):
    """literal_eval cho LIBRARY_ART, cho phép tên hằng khai báo ở đầu file (vd. _G = '...'; bài học EP20)."""
    import ast
    consts = {}
    for chunk in src.split("\n"):
        m = re.match(r"^([A-Za-z_]\w*)\s*=\s*(['\"].*['\"])\s*$", chunk)
        if m:
            try:
                consts[m.group(1)] = ast.literal_eval(m.group(2))
            except (ValueError, SyntaxError):
                pass
    tree = ast.parse(expr.strip(), mode="eval")

    class _Sub(ast.NodeTransformer):
        def visit_Name(self, node):
            if node.id in consts:
                return ast.copy_location(ast.Constant(consts[node.id]), node)
            raise ValueError("LIBRARY_ART dùng tên '%s' không phải hằng chuỗi ở đầu file" % node.id)
    return ast.literal_eval(ast.fix_missing_locations(_Sub().visit(tree)))


def _contact_sheet(paths, dst):
    from PIL import Image, ImageDraw
    if not paths:
        return
    W_, H_, n = 270, 480, len(paths)
    cols = min(n, 6)
    rows = (n + cols - 1) // cols
    sh = Image.new("RGB", (cols * W_, rows * (H_ + 28)), "white")
    d = ImageDraw.Draw(sh)
    for i, (label, p) in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((W_, H_))
        x, y = (i % cols) * W_, (i // cols) * (H_ + 28)
        sh.paste(im, (x, y))
        d.text((x + 6, y + H_ + 6), label[:42], fill=(40, 40, 40))
    sh.save(dst, quality=85)


def sync_scene_art(out_dir, wf=None):
    """Đăng tranh cảnh full-bleed của tập (đã duyệt video cuối) vào thư viện. Trả {asset_id: {...}}."""
    from PIL import Image, ImageOps
    import gates as G
    episode = os.path.basename(out_dir.rstrip("/"))
    wf = wf or G.load(out_dir)
    if wf.get("approvals", {}).get("final", {}).get("status") != "approved":
        raise SystemExit("Tập %s chưa được duyệt video cuối: chưa lưu tranh vào thư viện." % episode)
    art_dir, names, meta = _scenes_meta(out_dir)
    if not names:
        return {}
    ep_tag = episode.split("_")[0].upper()
    refs = sorted(os.listdir(os.path.join(out_dir, "refs"))) if os.path.isdir(os.path.join(out_dir, "refs")) else []
    idx = _load()
    out, sheet = {}, []
    for name in names:
        p = os.path.join(art_dir, name + ".png")
        if not os.path.exists(p):
            continue
        mm = meta.get(name, {})
        aid = mm.get("asset_id") or "%s_SCENE_%s" % (ep_tag, re.sub(r"\W", "_", name).upper())
        raw = Image.open(p).convert("RGB")
        im = ImageOps.fit(raw, (1080, 1920), Image.Resampling.LANCZOS)
        base = {"character_id": mm.get("character_id"), "character_name": mm.get("character_name"),
                "outfit": mm.get("outfit"), "story_context": "%s %s — %s" % (ep_tag, mm.get("scenes", ""), mm.get("context", name)),
                "style_version": mm.get("style", "tranh cảnh image_gen")}
        extra = {"asset_category": "episode_scene_art", "background_type": "full_scene_9x16",
                 "intended_use": ["reference", "scene_background_reuse", "image_gen_reference"],
                 "scenes": mm.get("scenes"), "generator": mm.get("generator", "chatgpt_image_gen"),
                 "raw_path": os.path.relpath(p, LIB),
                 "raw_file_sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(),
                 "reference_image": os.path.relpath(os.path.join(out_dir, "refs", refs[0]), LIB) if refs else None}
        note = "Tranh cảnh full-bleed 9:16 trong video %s, Owner duyệt video cuối %s" % (
            episode, (wf["approvals"]["final"].get("at") or "")[:10])
        r = register(idx, aid, im, episode, "approved", note, base, extra)
        out[aid] = {"result": r, "source": name}
        sheet.append((aid, os.path.join(LIB, "episode_approved", episode, aid + ".png")))
    _save(idx)
    _contact_sheet(sheet, os.path.join(LIB, "episode_approved", episode, "contact_sheet.jpg"))
    return out
