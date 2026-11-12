"""Thử phong cách BÁN HIỆN THỰC bằng ComfyUI + SDXL Base 1.0 (img2img, chạy cục bộ trên Mac, miễn phí).
Đầu vào: ảnh mẫu nhân vật đã duyệt + khung hình tập 8 do nmt-engine dựng → giữ bố cục/nhận diện, đổi chất liệu.
Đầu ra: output/_semireal_pilot/<tên>_<denoise>.png + pilot_log.json. Không gửi ảnh ra ngoài."""
import json, os, sys, time, urllib.request, uuid, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WS = os.path.join(ROOT, "workspace", "comfyui")
INP = os.path.join(WS, "ComfyUI", "input")
OUT = os.path.join(ROOT, "output", "_semireal_pilot")
API = "http://127.0.0.1:8188"

STYLE = ("semi-realistic digital illustration, soft cinematic lighting, detailed skin and hair texture, "
         "gentle film color grading, cozy, high quality, consistent character design")
NEG = "text, watermark, logo, extra fingers, deformed hands, distorted face, blurry, lowres, extra limbs, nsfw"

JOBS = [  # (tên, ảnh nguồn, mô tả, kích thước SDXL, các mức denoise)
    ("ti_ref", "character_library/ti/TI_MASTER_REFERENCE.png",
     "young Vietnamese man, short messy black hair, kind smile, navy t-shirt, jeans, full body, plain light background", (832, 1216), (0.45, 0.6)),
    ("ngang_ref", "character_library/ngang/NGANG_MASTER_REFERENCE.png",
     "young Vietnamese woman, long wavy black hair, cute friendly smile, rust shirt, full body, plain light background", (832, 1216), (0.45, 0.6)),
    ("mimi_ref", "character_library/mimi/MIMI_MASTER_REFERENCE.png",
     "brown tabby cat with green eyes sitting, full body, plain light background", (1024, 1024), (0.45, 0.6)),
    ("ep08_f05", "output/ep08_ngay_dau_vs_nam_ba/render/stills/F05.png",
     "young Vietnamese couple in pajamas holding coffee mugs in a pink living room, woman with very messy unwashed long hair "
     "laughing and blushing, man smiling, tabby cat peeking from sofa", (768, 1344), (0.5,)),
    ("ep08_f04", "output/ep08_ngay_dau_vs_nam_ba/render/stills/F04.png",
     "close-up of young Vietnamese woman with very messy long hair in lavender pajamas, pouting annoyed, holding coffee mug, "
     "pink background", (768, 1344), (0.5,)),
]


def post(path, data):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def get(path):
    return json.loads(urllib.request.urlopen(API + path, timeout=30).read())


def graph(img, pos, w, h, den, seed):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "LoadImage", "inputs": {"image": img}},
        "3": {"class_type": "ImageScale", "inputs": {"image": ["2", 0], "upscale_method": "lanczos", "width": w, "height": h, "crop": "center"}},
        "4": {"class_type": "VAEEncode", "inputs": {"pixels": ["3", 0], "vae": ["1", 2]}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["5", 0], "negative": ["6", 0], "latent_image": ["4", 0],
                                                    "seed": seed, "steps": 26, "cfg": 6.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
                                                    "denoise": den}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["1", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": "avf_semireal"}},
    }


def flatten(src, dst):
    im = Image.open(src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (246, 242, 236, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(dst)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(INP, exist_ok=True)
    log = []
    for name, src, desc, (w, h), dens in JOBS:
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            print("bỏ qua (thiếu):", src); continue
        fn = "avf_%s.png" % name
        flatten(p, os.path.join(INP, fn))
        for den in dens:
            t0 = time.time()
            pid = post("/prompt", {"prompt": graph(fn, desc + ", " + STYLE, w, h, den, 1107), "client_id": str(uuid.uuid4())})["prompt_id"]
            while True:
                hist = get("/history/" + pid)
                if pid in hist and hist[pid].get("outputs"):
                    break
                if pid in hist and hist[pid].get("status", {}).get("status_str") == "error":
                    raise SystemExit("ComfyUI lỗi: " + json.dumps(hist[pid]["status"])[:800])
                time.sleep(2)
            o = hist[pid]["outputs"]["9"]["images"][0]
            srcp = os.path.join(WS, "ComfyUI", "output", o.get("subfolder", ""), o["filename"])
            dst = os.path.join(OUT, "%s_d%02d.png" % (name, int(den * 100)))
            shutil.copy(srcp, dst)
            rec = {"name": name, "source": src, "denoise": den, "size": [w, h], "seconds": round(time.time() - t0, 1), "file": os.path.basename(dst),
                   "model": "sd_xl_base_1.0.safetensors", "seed": 1107, "steps": 26, "cfg": 6.0}
            log.append(rec); print(json.dumps(rec, ensure_ascii=False), flush=True)
            json.dump(log, open(os.path.join(OUT, "pilot_log.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
