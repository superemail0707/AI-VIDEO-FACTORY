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
  --script -> --script-review (D-029: ≥ 8/10 tự qua, tối đa 3 lần, sau đó Owner duyệt) -> --art-auto, --check-art
  -> --tts, --storyboard -> [Owner duyệt hình] -> render, --audio, --mux -> [Owner duyệt video]
  -> --export <tiktok|youtube_shorts|facebook_reels> ... -> --export-finish  (videos-post/unpost/, không tự đăng)"""
import os, sys, wave
EP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(EP_DIR, "..", "_engine"))
import cute_engine as E  # noqa: E402
import scene_kit as K  # noqa: E402
from cute_engine import *  # noqa: F401,F403,E402

META = {{
    "title": "{title}",
    "brief": {brief!r},   # nguyên văn brief của Owner — giám khảo chấm theo brief này
    "format": "dialogue",          # dialogue | nondialogue (chill, theo nhạc, phim ngắn)
    "duration_s": [60, 70],        # quy trình chuẩn v2 (Owner 18/11/2026): tổng ≥ 60 s gồm outro 7,8 s
    "process": "nmt_v2",           # _engine/NMT_STANDARD_PROCESS.md: rubric ≥ 9/10 + hội đồng người xem (--script-review viewer)
    # "script_gate": "owner",      # bật dòng này để Owner duyệt mọi kịch bản (tắt chấm tự động)
    # Chuẩn viết: _engine/prompts/viral_storyboard_agent_v2.md (Agent V2.0). Bảng concept hiện trong chat + script.md.
    "ideation": {{
        "concepts": [
            {{"name": "TODO", "type": "A", "score": 0, "logline": "TODO", "hook": "TODO", "conflict": "TODO",
             "escalation": ["E1", "E2", "E3"], "twist": "TODO", "styles": ["A"], "difficulty": "thấp|vừa|cao"}},
            {{"name": "TODO", "type": "B", "score": 0, "logline": "TODO", "hook": "TODO", "conflict": "TODO",
             "escalation": ["E1", "E2", "E3"], "twist": "TODO", "styles": ["B"], "difficulty": "thấp|vừa|cao"}},
            {{"name": "TODO", "type": "C", "score": 0, "logline": "TODO", "hook": "TODO", "conflict": "TODO",
             "escalation": ["E1", "E2", "E3"], "twist": "TODO", "styles": ["C"], "difficulty": "thấp|vừa|cao"}},
        ],
        "chosen": "TODO",          # concept điểm cao nhất (hoặc "combined": True kèm lý do)
        "reason": "TODO",
    }},
    "comedy": {{"main": "TODO", "support": []}},   # expectation_vs_reality | rule_of_three | escalation | visual_absurdity | deadpan | role_reversal | callback
    "twist_seed": "TODO: chi tiết nhỏ gieo ở đầu làm cơ sở cho twist",
    "visual_styles": ["A"],        # 1–3 trong A–G (Agent V2.0 mục VII), đặt trên master S1/S2/S3 đã duyệt
    "audience": "TODO",
    "logline": "TODO: một câu tóm tắt tình huống + cú twist",
    "notes": {{
        "F01": "TODO: mô tả hình/góc máy cảnh mở (hook trong 2 giây đầu)",
    }},
    "end": "TODO: câu hỏi tương tác / Tag người ấy vào xem!",
}}

# HSETL (Agent V2.0 mục IV): Hook 0–3 s → Setup → E1/E2/E3 → (khoảng lặng) Twist → Last laugh. Không thêm cảnh lặp để đủ giờ.
# notes[F..] ghi gọn các mục storyboard: mục đích, hình, biểu cảm, hành động, góc máy + chuyển máy, SFX, nhạc, continuity.
# Prompt ảnh (10 phần, tiếng Anh) -> art/PROMPTS_v01.md; prompt Image-to-Video (10 phần) -> art/I2V_PROMPTS_v01.md (kèm theo, engine vẫn tự dựng).
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
FIRST_LEAD = 0.05   # bài học EP19: câu mở vào ngay khung đầu, hình không đi trước tiếng (--check-sync chặn tiếng thật > 0,20 s)
for i_, (sid, lines, tail, title, tr, td) in enumerate(PLAN):
    t = FIRST_LEAD if i_ == 0 else 0.35
    for vid, who, text in lines:
        VOICE.append((vid, sid, round(t, 3), who, text))
        T[vid] = (t, _dur(vid))
        t += _dur(vid) + 0.45
    SCENES.append((sid, round(max(2.4, t - 0.45 + tail), 3), title, tr, td))
OUTRO_SID = "F%02d" % (len(PLAN) + 1)
SCENES.append((OUTRO_SID, K.SUB_DUR, "Outro", "cut", 0.0))  # Owner 18/11: avatar/thanh đăng ký xuất hiện rồi biến mất, 7,8 s

# Tranh image_gen: --check-art kiểm tranh trong ART_DIR; --storyboard bị chặn khi chưa đạt.
# Sau khi xem art/v01/_qa/*_overlay.jpg, ghi art/v01/safe_annotations.json:
#   {{"A01": {{"char_bottom_y": 1264, "head_top_y": 420, "subtitles": true}}}}
ART_DIR = os.path.join(EP_DIR, "art", "v01")
ART_CHECK = True
# --art-auto đọc art/PROMPTS_v01.md (khối "### A01 — …" + ```prompt```), tham chiếu nhân vật trong refs/ hoặc ART_REFS.
ART_REFS = []

OUTRO_ART = "A01"  # đổi sang mã tranh cảnh cuối khi hoàn tất storyboard
FUNCS = {{OUTRO_SID: lambda t: K.subscribe_outro(t, K.art_loader(ART_DIR)(OUTRO_ART))}}
SFX, MUSIC = K.subscribe_sfx(OUTRO_SID, gain=K.OUTRO_SFX_GAIN), []   # quy trình v2: SFX outro 50 %, nhạc outro K.OUTRO_MUSIC_GAIN
PICKS, THUMB = [], None
if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep{n}_scenes.py")):
    # Module cảnh giữ mặc định K.subscribe_outro + K.subscribe_sfx(gain=K.OUTRO_SFX_GAIN), không dùng outro tai mèo.
    # Quy trình v2: K.install_post(subtitles=False) + K.word_sub(out, sid, t, KEYWORDS) (chữ trắng nền đen, keyword vàng,
    # chạy theo giọng; K.build_word_timing(EP_DIR) sau --tts); K.make_thumbnail(...) cho thumbnail; không chữ tiêu đề đầu video.
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
        fh.write(TEMPLATE.format(n="%02d" % n, title=topic, title_up=topic.upper(), brief=topic))
    post = {"topic_slug": s, "brand": "ngang-mot-ti",  # kênh Ngang Một Tí → bắt buộc watermark NMT khi xuất
            "titles": {"curious": "TODO", "funny": "TODO", "short": "TODO"},   # Agent V2.0 mục XIII
            "thumbnail": {"description": "TODO: nhân vật, biểu cảm, góc máy, màu, chi tiết gây tò mò (không lộ hết twist)",
                          "prompt": "TODO"},
            "comment_question": "TODO: câu hỏi về trải nghiệm người xem (không kéo tương tác giả tạo)",
            "tiktok": {"caption": "TODO", "hashtags": ["#capdoi", "#hoathinh", "#TiNgangMimi"]},
            "youtube_shorts": {"title": topic + " #Shorts", "caption": "TODO", "hashtags": ["#Shorts", "#capdoi", "#TiNgangMimi"]},
            "facebook_reels": {"caption": "TODO", "hashtags": ["#capdoi", "#TiNgangMimi"]}}
    with open(os.path.join(d, "post.json"), "w", encoding="utf-8") as fh:
        json.dump(post, fh, ensure_ascii=False, indent=1)
    from generated_art import POLICY
    with open(os.path.join(d, 'art_pipeline.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(POLICY, episode=ep, subject=topic), fh, ensure_ascii=False, indent=2)
    print(json.dumps({"episode": ep, "file": py, "post": os.path.join(d, "post.json"), "videos_post": "videos-post/unpost/" + s}, ensure_ascii=False))


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
