"""Pilot 2 bán hiện thực: SDXL + ControlNet Union (canny) img2img, denoise cao (0,75–0,85) để đổi chất liệu mạnh
nhưng khoá nét viền/tư thế của sprite đã duyệt. Sprite được tách nền bằng rembg → PNG alpha dùng được trong engine.
Đầu vào: output/_semireal_pilot2/inputs/*.png (đã xuất sẵn, không chữ). Đầu ra: output/_semireal_pilot2/*.png + pilot_log.json."""
import json, os, time, urllib.request, uuid, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WS = os.path.join(ROOT, "workspace", "comfyui")
INP = os.path.join(WS, "ComfyUI", "input")
DIR = os.path.join(ROOT, "output", "_semireal_pilot2")
API = "http://127.0.0.1:8188"

STYLE = ("semi-realistic 3D animated film still, soft subsurface skin, realistic hair strands, fabric texture, "
         "warm cinematic lighting, shallow depth of field, high detail, cute and wholesome")
NEG = ("flat cartoon, thick black outlines, cel shading, text, watermark, logo, deformed hands, extra fingers, "
       "distorted face, asymmetric eyes, blurry, lowres, extra limbs, nsfw")

JOBS = [  # (tên, mô tả, kích thước, [denoise], sprite?)
    ("ngang_home_angry", "young Vietnamese woman, very messy unwashed long wavy black hair, lavender pajamas, pouting annoyed, "
     "holding white coffee mug, plain grey background", (832, 1216), (0.75, 0.85), True),
    ("ti_home_joy", "young Vietnamese man, short messy black hair, sage green pajamas, warm closed-eye smile, holding coffee mug, "
     "plain grey background", (832, 1216), (0.75, 0.85), True),
    ("mimi_sit", "brown tabby cat with green eyes sitting, judging look, plain grey background", (1024, 1024), (0.75, 0.85), True),
    ("ti_phone", "young Vietnamese man sitting cross-legged holding a smartphone with both hands, eyes glued to the screen, "
     "red football jersey number 10, jeans, plain grey background", (832, 1216), (0.8,), True),
    ("ngang_gala", "young Vietnamese woman with long wavy black hair in elegant champagne evening gown, smiling, plain grey background",
     (832, 1216), (0.8,), True),
    ("scene_f04", "close-up of young Vietnamese woman with very messy long hair in lavender pajamas, pouting annoyed, holding coffee mug, "
     "pink sunburst background", (768, 1344), (0.8,), False),
    ("scene_f05", "young Vietnamese couple in pajamas holding coffee mugs in a pastel pink living room, woman with messy hair laughing "
     "and blushing, man smiling, tabby cat peeking from pink sofa behind them", (768, 1344), (0.8,), False),
]


def call(path, data=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def graph(img, pos, w, h, den, seed=1107):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img}},
        "3": {"class_type": "ImageScale", "inputs": {"image": ["2", 0], "upscale_method": "lanczos", "width": w, "height": h, "crop": "center"}},
        "4": {"class_type": "VAEEncode", "inputs": {"pixels": ["3", 0], "vae": ["1", 2]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "10": {"class_type": "Canny", "inputs": {"image": ["3", 0], "low_threshold": 0.15, "high_threshold": 0.4}},
        "11": {"class_type": "ControlNetLoader", "inputs": {"control_net_name": "controlnet-union-sdxl-1.0.safetensors"}},
        "12": {"class_type": "SetUnionControlNetType", "inputs": {"control_net": ["11", 0], "type": "canny/lineart/anime_lineart/mlsd"}},
        "13": {"class_type": "ControlNetApplyAdvanced", "inputs": {"positive": ["5", 0], "negative": ["6", 0], "control_net": ["12", 0],
                                                                    "image": ["10", 0], "strength": 0.7, "start_percent": 0.0,
                                                                    "end_percent": 0.8, "vae": ["1", 2]}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["13", 0], "negative": ["13", 1], "latent_image": ["4", 0],
                                                    "seed": seed, "steps": 28, "cfg": 6.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
                                                    "denoise": den}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": "avf_semireal2"}},
    }


def cutout(src, dst):
    from rembg import remove, new_session
    from PIL import Image
    global _sess
    try:
        _sess
    except NameError:
        _sess = new_session("u2net")
    remove(Image.open(src), session=_sess).save(dst)


def main():
    os.makedirs(INP, exist_ok=True)
    log = []
    for name, desc, (w, h), dens, sprite in JOBS:
        src = os.path.join(DIR, "inputs", name + ".png")
        if not os.path.exists(src):
            print("thiếu", src); continue
        fn = "avf2_%s.png" % name
        shutil.copy(src, os.path.join(INP, fn))
        for den in dens:
            t0 = time.time()
            pid = call("/prompt", {"prompt": graph(fn, desc + ", " + STYLE, w, h, den), "client_id": str(uuid.uuid4())})["prompt_id"]
            while True:
                hist = call("/history/" + pid)
                if pid in hist and hist[pid].get("outputs"):
                    break
                if pid in hist and hist[pid].get("status", {}).get("status_str") == "error":
                    raise SystemExit("ComfyUI lỗi: " + json.dumps(hist[pid]["status"])[:1200])
                time.sleep(2)
            o = hist[pid]["outputs"]["9"]["images"][0]
            out = os.path.join(DIR, "%s_d%02d.png" % (name, int(den * 100)))
            shutil.copy(os.path.join(WS, "ComfyUI", "output", o.get("subfolder", ""), o["filename"]), out)
            rec = {"name": name, "denoise": den, "size": [w, h], "seconds": round(time.time() - t0, 1), "file": os.path.basename(out),
                   "controlnet": "xinsir/controlnet-union-sdxl-1.0 canny s0.7 end0.8", "seed": 1107, "steps": 28, "cfg": 6.0}
            if sprite:
                t1 = time.time()
                cut = out.replace(".png", "_alpha.png")
                cutout(out, cut)
                rec["alpha_file"] = os.path.basename(cut); rec["rembg_seconds"] = round(time.time() - t1, 1)
            log.append(rec); print(json.dumps(rec, ensure_ascii=False), flush=True)
            json.dump(log, open(os.path.join(DIR, "pilot_log.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
