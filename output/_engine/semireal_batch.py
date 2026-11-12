"""Tạo bộ sprite chất liệu minh hoạ 3D mềm (cấu hình pilot 2 đã được Owner chọn: SDXL Base + ControlNet Union canny,
denoise 0,75) cho một tập nmt-engine, rồi tách nền bằng rembg. Có thể chạy lại: ảnh đã xong sẽ bỏ qua.
Dùng: semireal_batch.py <thư mục tập>  (đọc <tập>/semireal_jobs.json, ảnh vào <tập>/semireal_inputs/, ra <tập>/semireal_assets/)"""
import json, os, time, urllib.request, uuid, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WS = os.path.join(ROOT, "workspace", "comfyui")
INP = os.path.join(WS, "ComfyUI", "input")
API = "http://127.0.0.1:8188"

STYLE = ("semi-realistic 3D animated film still, soft subsurface skin, realistic hair strands, fabric texture, "
         "warm cinematic lighting, high detail, cute and wholesome, plain grey background")
NEG = ("flat cartoon, thick black outlines, cel shading, text, watermark, logo, deformed hands, extra fingers, "
       "distorted face, asymmetric eyes, blurry, lowres, extra limbs, nsfw")
DEN, STEPS = 0.75, 22


def call(path, data=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def graph(img, pos, w, h, den, seed=1107, cn=0.7):
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
                                                                    "image": ["10", 0], "strength": cn, "start_percent": 0.0,
                                                                    "end_percent": 0.8, "vae": ["1", 2]}},
        "7": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["13", 0], "negative": ["13", 1], "latent_image": ["4", 0],
                                                    "seed": seed, "steps": STEPS, "cfg": 6.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
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
    import sys
    ep = os.path.abspath(sys.argv[1])
    jobs = json.load(open(os.path.join(ep, "semireal_jobs.json"), encoding="utf-8"))
    dst_dir = os.path.join(ep, "semireal_assets")
    os.makedirs(dst_dir, exist_ok=True)
    os.makedirs(INP, exist_ok=True)
    logp = os.path.join(dst_dir, "batch_log.json")
    log = json.load(open(logp)) if os.path.exists(logp) else []
    for k, job in enumerate(jobs):
        name = job["name"]
        alpha = os.path.join(dst_dir, name + ".png")
        if os.path.exists(alpha):
            print("đã có, bỏ qua:", name); continue
        fn = "avfb_%s.png" % name
        shutil.copy(os.path.join(ep, "semireal_inputs", name + ".png"), os.path.join(INP, fn))
        t0 = time.time()
        pid = call("/prompt", {"prompt": graph(fn, job["desc"] + ", " + STYLE, 832, 1216, job.get("denoise", DEN), cn=job.get("canny_strength", 0.7)), "client_id": str(uuid.uuid4())})["prompt_id"]
        while True:
            hist = call("/history/" + pid)
            if pid in hist and hist[pid].get("outputs"):
                break
            if pid in hist and hist[pid].get("status", {}).get("status_str") == "error":
                raise SystemExit("ComfyUI lỗi: " + json.dumps(hist[pid]["status"])[:1200])
            time.sleep(2)
        o = hist[pid]["outputs"]["9"]["images"][0]
        raw = os.path.join(dst_dir, name + "_raw.png")
        shutil.copy(os.path.join(WS, "ComfyUI", "output", o.get("subfolder", ""), o["filename"]), raw)
        cutout(raw, alpha)
        rec = {"name": name, "sprite": job["sprite"], "denoise": job.get("denoise", DEN), "canny_strength": job.get("canny_strength", 0.7), "steps": STEPS, "seed": 1107, "seconds": round(time.time() - t0, 1),
               "model": "sd_xl_base_1.0 + xinsir controlnet-union canny s0.7 end0.8", "file": os.path.basename(alpha)}
        log.append(rec)
        json.dump(log, open(logp, "w"), ensure_ascii=False, indent=1)
        print("[%d/%d] %s" % (k + 1, len(jobs), json.dumps(rec, ensure_ascii=False)), flush=True)


if __name__ == "__main__":
    main()
