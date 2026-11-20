"""TTS VieNeu v3 Turbo dùng chung. python3 tts_vieneu.py <episode_dir> [ID ...]  (đọc <ep>/render/lines.json -> <ep>/audio/voice/ID.wav)"""
import os, sys, json, time
import numpy as np
def _model_dir():
    """Thứ tự: biến môi trường AVF_VIENEU_MODEL -> <repo>/workspace/vieneu-model -> đường dẫn máy ảo cũ (tương thích).
    Sửa lỗi EP16: bản cũ chỉ trỏ ~/mnt/... nên 7 tập phải chép render/tts_local.py."""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.environ.get("AVF_VIENEU_MODEL", ""),
             os.path.join(here, "..", "..", "workspace", "vieneu-model"),
             os.path.expanduser("~/mnt/AI-VIDEO-FACTORY/workspace/vieneu-model")]
    for c in cands:
        if c and os.path.isdir(os.path.join(c, "onnx_update")) and os.path.isdir(os.path.join(c, "codec")):
            return os.path.abspath(c)
    raise SystemExit("Không tìm thấy model VieNeu (cần onnx_update/ và codec/). Đã thử: " + ", ".join(c for c in cands if c))


M = _model_dir()
from vieneu.v3turbo import V3TurboVieNeuTTS
import vieneu._v3_turbo_engine.onnx_runtime_lite as lite
_o = lite.OnnxV3LiteEngine.__init__
def _p(self, *a, **k):
    k.setdefault("codec_dir", os.path.join(M, "codec")); return _o(self, *a, **k)
lite.OnnxV3LiteEngine.__init__ = _p
ep = os.path.abspath(sys.argv[1])
only = set(sys.argv[2:])
out = os.path.join(ep, "audio", "voice"); os.makedirs(out, exist_ok=True)
lines = json.load(open(os.path.join(ep, "render", "lines.json"), encoding="utf-8"))
import re


def spoken(text):
    """Bài học EP27 (19/11/2026): bộ chuẩn hoá VieNeu đọc '20/11' thành 'hai mươi trên mười một'.
    Ngày dd/mm -> 'dd tháng mm' (chỉ cho giọng; phụ đề vẫn giữ chữ số)."""
    return re.sub(r"\b(\d{1,2})/(\d{1,2})\b", lambda m: "%s tháng %s" % (m.group(1), m.group(2)), text)


t0 = time.time()
tts = V3TurboVieNeuTTS(onnx_dir=os.path.join(M, "onnx_update"), codec_dir=os.path.join(M, "codec"), backend="onnx", precision="fp32")
for L in lines:
    if only and L["id"] not in only: continue
    t = time.time()
    a = tts.infer(spoken(L["text"]), voice=L["voice"], temperature=0.7)
    tts.save(a, os.path.join(out, L["id"] + ".wav"))
    print(json.dumps({"id": L["id"], "voice": L["voice"], "sec": round(len(np.asarray(a).reshape(-1)) / tts.sample_rate, 2), "infer_s": round(time.time() - t, 1)}, ensure_ascii=False), flush=True)
print("total_s", round(time.time() - t0, 1))
