"""nmt-engine — Ngang Một Tí: dựng video hoạt hình 2D Tí · Ngang · Mimi
(9:16, 1080×1920, 60 fps), có cổng duyệt kịch bản, hình và video cuối.

Lệnh:
  python3 output/_engine/nmt_engine.py new "<chủ đề>"   tạo thư mục tập mới output/epNN_<slug>/ từ khuôn mẫu
  python3 output/_engine/nmt_engine.py list             liệt kê các tập và trạng thái cổng duyệt
Sau khi tạo, mọi bước chạy bằng file tập: render/epNN.py --script | --tts | --storyboard | <cảnh> | --audio | --mux | --export ...
Xem output/_engine/NMT_ENGINE.md."""
import json
import os
import re
import sys

ENGINE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)
from platform_export import slug  # noqa: E402

TEMPLATE = '''"""Tập {n} (nmt-engine, quy trình có cổng duyệt) — "{title}".
  --script -> [Owner duyệt kịch bản] -> --tts, --storyboard -> [Owner duyệt hình] -> render, --audio, --mux -> [duyệt video]
  -> --export <tiktok|youtube_shorts|facebook_reels> ... -> --export-finish  (videos-post/, không tự đăng)"""
import os, sys, wave
EP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EP_DIR, "..", "_engine"))
import cute_engine as E  # noqa: E402
from cute_engine import *  # noqa: F401,F403,E402

META = {{
    "title": "{title}",
    "logline": "TODO: một câu tóm tắt tình huống + cú twist",
    "notes": {{
        "F01": "TODO: mô tả hình/góc máy cảnh mở (hook trong 2 giây đầu)",
    }},
    "end": "TODO: câu hỏi tương tác / Tag người ấy vào xem!",
}}

# (cảnh, [(mã câu, "ti"|"ngang", lời thoại ≤ 45 ký tự)], đuôi giây, tên cảnh, chuyển cảnh cut|fade|whip|flash, thời lượng chuyển)
PLAN = [
    ("F01", [("V1", "ngang", "TODO")], 1.0, "Mở đầu", "cut", 0.0),
]
VDIR_ = os.path.join(EP_DIR, "audio", "voice")


def _dur(vid):
    p = os.path.join(VDIR_, vid + ".wav")
    if not os.path.exists(p):
        return 1.6
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()


SCENES, VOICE, T = [], [], {{}}
for sid, lines, tail, title, tr, td in PLAN:
    t = 0.35
    for vid, who, text in lines:
        VOICE.append((vid, sid, round(t, 3), who, text))
        T[vid] = (t, _dur(vid))
        t += _dur(vid) + 0.45
    SCENES.append((sid, round(max(2.4, t - 0.45 + tail), 3), title, tr, td))
SCENES.append(("F%02d" % (len(PLAN) + 1), 3.2, "End card", "iris", 0.55))

FUNCS = {{}}   # cảnh viết ở bước 2 trong ep{n}_scenes.py (sau khi kịch bản được duyệt)
SFX, MUSIC = [], []
PICKS, THUMB = [], None
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep{n}_scenes.py")):
    from ep{n}_scenes import FUNCS, SFX, MUSIC, PICKS, THUMB  # noqa: E402,F811

E.configure(EP_DIR, SCENES, VOICE, FUNCS)
if __name__ == "__main__":
    E.main(PICKS, thumb=THUMB, title="{title_up}", sfx=SFX, music=MUSIC, meta=META)
'''


def episodes():
    out = []
    for d in sorted(os.listdir(OUTPUT)):
        m = re.match(r"ep(\d+)_", d)
        if m and os.path.isdir(os.path.join(OUTPUT, d)):
            out.append((int(m.group(1)), d))
    return out


def new(topic):
    n = max([k for k, _ in episodes()] or [0]) + 1
    s = slug(topic)[:40].strip("-")
    ep = "ep%02d_%s" % (n, s.replace("-", "_"))
    d = os.path.join(OUTPUT, ep)
    if os.path.exists(d):
        raise SystemExit("Đã tồn tại: " + d)
    os.makedirs(os.path.join(d, "render"))
    py = os.path.join(d, "render", "ep%02d.py" % n)
    with open(py, "w", encoding="utf-8") as fh:
        fh.write(TEMPLATE.format(n="%02d" % n, title=topic, title_up=topic.upper()))
    post = {"topic_slug": s, "brand": "ngang-mot-ti",  # kênh Ngang Một Tí → bắt buộc watermark NMT khi xuất
            "tiktok": {"caption": "TODO", "hashtags": ["#capdoi", "#hoathinh", "#TiNgangMimi"]},
            "youtube_shorts": {"title": topic + " #Shorts", "caption": "TODO", "hashtags": ["#Shorts", "#capdoi", "#TiNgangMimi"]},
            "facebook_reels": {"caption": "TODO", "hashtags": ["#capdoi", "#TiNgangMimi"]}}
    with open(os.path.join(d, "post.json"), "w", encoding="utf-8") as fh:
        json.dump(post, fh, ensure_ascii=False, indent=1)
    from generated_art import POLICY
    with open(os.path.join(d, 'art_pipeline.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(POLICY, episode=ep, subject=topic), fh, ensure_ascii=False, indent=2)
    print(json.dumps({"episode": ep, "file": py, "post": os.path.join(d, "post.json"), "videos_post": "videos-post/" + s}, ensure_ascii=False))


def status():
    for n, d in episodes():
        wf = os.path.join(OUTPUT, d, "workflow.json")
        st = json.load(open(wf)).get("state", "?") if os.path.exists(wf) else "chưa có cổng duyệt (tập cũ)"
        print("%-40s %s" % (d, st))


def main(argv=None):
    """CLI chính của NMT-engine; tên cũ dùng chung entry point này."""
    args = sys.argv[1:] if argv is None else list(argv)
    if len(args) >= 2 and args[0] == "new":
        new(" ".join(args[1:]))
    elif args and args[0] in ("list", "status"):
        status()
    elif args and args[0] in ('art-add', 'art-import', 'art-review', 'references'):
        from generated_art import main as art_main
        art_main(args)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
