"""TTS VieNeu v3 Turbo dùng chung. python3 tts_vieneu.py <episode_dir> [ID ...]  (đọc <ep>/render/lines.json -> <ep>/audio/voice/ID.wav)"""
import os, sys, json, time
import numpy as np
M = os.path.expanduser("~/mnt/AI-VIDEO-FACTORY/workspace/vieneu-model")
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
t0 = time.time()
tts = V3TurboVieNeuTTS(onnx_dir=os.path.join(M, "onnx_update"), codec_dir=os.path.join(M, "codec"), backend="onnx", precision="fp32")
for L in lines:
    if only and L["id"] not in only: continue
    t = time.time()
    a = tts.infer(L["text"], voice=L["voice"], temperature=0.7)
    tts.save(a, os.path.join(out, L["id"] + ".wav"))
    print(json.dumps({"id": L["id"], "voice": L["voice"], "sec": round(len(np.asarray(a).reshape(-1)) / tts.sample_rate, 2), "infer_s": round(time.time() - t, 1)}, ensure_ascii=False), flush=True)
print("total_s", round(time.time() - t0, 1))
