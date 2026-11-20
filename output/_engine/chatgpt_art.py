"""Tạo tranh qua ChatGPT web bằng Playwright — cách TẠM THỜI khi Codex hết lượt (Owner 13/11/2026).

Engine không tự lái trình duyệt. Script này sinh một file JavaScript cho công cụ Playwright MCP
`browser_run_code_unsafe` (hồ sơ Chrome Playwright có sẵn đăng nhập ChatGPT của Owner):

    python3 output/_engine/chatgpt_art.py <thư mục tập> A01,A02,A03 [--new] [--prompts art/PROMPTS_v01.md] [--out art/v01]

rồi chạy `browser_run_code_unsafe` với `filename` = đường dẫn in ra. JS sẽ, với từng cảnh:
  - (--new) mở cuộc trò chuyện mới, đính kèm 3 master reference Tí/Ngang/Mimi;
  - dán prompt cảnh từ PROMPTS_vNN.md, bấm gửi, chờ ảnh mới (ảnh ≥ 600 px không thuộc tin nhắn người dùng) và hết nút Stop;
  - tải ảnh gốc bằng thẻ <a download> trên blob rồi `download.saveAs(<out>/<CẢNH>.png)`.
Mỗi lô ≤ 6 cảnh (~45 s/cảnh). Không ghi đè: cảnh đã có file thì bỏ qua (đổi tên bản cũ `_superseded` nếu muốn tạo lại).
Sau khi tải: `--check-art`, xem overlay, ghi `safe_annotations.json` như tranh --art-auto.
Không đăng nhập thay Owner; không dùng tính năng trả phí ngoài gói ChatGPT Owner đang dùng.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
ROOT = ENGINE.parent.parent
sys.path.insert(0, str(ENGINE))
import art_auto as AA  # noqa: E402

LIB = ROOT / "character_library"
REFS = [str(LIB / "ti" / "TI_MASTER_REFERENCE.png"), str(LIB / "ngang" / "NGANG_MASTER_REFERENCE.png"),
        str(LIB / "mimi" / "MIMI_MASTER_REFERENCE.png")]
JS_DIR = ROOT / ".playwright-mcp"          # thư mục Playwright MCP được phép đọc file
H_FIRST = ("The 3 attached images are the master character references (Ti, Ngang, Mimi). For every request in this chat, "
           "generate exactly ONE new image with your image generation tool, tall portrait 9:16, reply with the image only, "
           "no questions.\n\n")
H_NEXT = ("Generate exactly ONE new image with your image generation tool, tall portrait 9:16. "
          "Reply with the image only, no questions.\n\n")
# Owner 19/11/2026 (bài học EP29: A08 vẽ Ngang ngủ, A15 thêm Ngang sát mép, A13 đầu chạm đỉnh): khung chặt hơn, ghép
# vào cuối MỌI prompt để bớt phải tạo lại.
STRICT = ("STRICT FRAME CHECK before you draw (mandatory): draw ONLY the characters listed in CAST (no extra Ti, Ngang or Mimi); "
          "keep each character's exact state from ACTION (awake/asleep, holding/not holding, standing/sitting); every face fully "
          "inside the image and at least 12% away from the left and right edges; the top of every head (and cat ears) at least "
          "13% below the top edge; the lowest feet or body above 72% of the image height; the bottom 28% is empty floor/ground.")

JS = r'''async (page) => {
  const ATTACHED = %(attached)s;
  const NEW = %(new)s, JOBS = %(jobs)s, REFS = %(refs)s, TOK = %(tok)s, OUT = %(out)s;
  for (const J of JOBS) { let t = J.t; for (const k of Object.keys(TOK)) t = t.split(k).join(TOK[k]); J.text = t; J.target = OUT + J.o; }
  // 20/11/2026: ChatGPT có 2 ô "Ask ChatGPT" (1 ô ẩn 0×0) -> strict mode violation; chỉ lấy ô đang hiển thị
  const box = '[contenteditable=true][aria-label="Ask ChatGPT"] >> visible=true';
  const bigImgs = () => page.evaluate(() => [...document.querySelectorAll('main img')].filter(i => i.naturalWidth >= 600 && !i.closest('[data-message-author-role="user"]') && i.alt !== 'User attachment').map(i => i.src));
  const out = [];
  if (NEW && !ATTACHED) { await page.goto('https://chatgpt.com/'); await page.waitForSelector(box, {timeout: 30000}); }
  for (let k = 0; k < JOBS.length; k++) {
    const J = JOBS[k];
    const before = new Set(await bigImgs());
    if (NEW && k === 0 && !ATTACHED) {
      const upload = async () => { const fi = page.locator('input[type=file][aria-label="Attach photos or videos"]'); await (await fi.count() ? fi : page.locator('input[type=file][aria-label="Attach photos"]')).setInputFiles(REFS); };  // ChatGPT đổi tên ô tải ảnh (19/11/2026)
      // chờ đủ ảnh mẫu hiện trong ô soạn tin (bài học 13/11: chờ cố định 4 s -> gửi đi 0 ảnh)
      const thumbs = () => page.evaluate(() => { const f = document.querySelector('form') || document; return [...f.querySelectorAll('img')].filter(i => !i.closest('[data-message-author-role]')).length; });
      // EP28 19/11: tải ngay sau goto đôi khi không nhận (trang chưa hydrate) -> 0/3; chờ 3 s, sau 20 s vẫn 0 thì tải lại 1 lần
      await page.waitForTimeout(3000); await upload();
      let n = 0; for (let i = 0; i < 60 && (n = await thumbs()) < REFS.length; i++) { if (i === 20 && n === 0) await upload(); await page.waitForTimeout(1000); }
      if (n < REFS.length) return {out: [{scene: J.scene, ok: false, msg: 'ảnh mẫu chưa tải lên đủ: ' + n + '/' + REFS.length}], url: page.url()};
      await page.waitForTimeout(1500);
    }
    await page.locator(box).fill(J.text);
    const send = page.getByRole('button', {name: 'Send', exact: true});
    await send.waitFor({timeout: 60000});
    for (let i = 0; i < 60 && await send.isDisabled(); i++) await page.waitForTimeout(1000);
    await send.click();
    if (NEW && k === 0) {
      await page.waitForTimeout(3000);
      let sent = 0; for (let i = 0; i < 10 && sent < REFS.length; i++) { sent = await page.evaluate(() => [...document.querySelectorAll('main img')].filter(i => i.alt === 'User attachment').length); if (sent < REFS.length) await page.waitForTimeout(1000); }
      if (sent < REFS.length) return {out: [{scene: J.scene, ok: false, msg: 'tin nhắn đầu chỉ có ' + sent + ' ảnh mẫu — dừng, không tạo ảnh thiếu mẫu'}], url: page.url()};
    }
    const t0 = Date.now(); let src = null;
    while (Date.now() - t0 < 240000) {
      await page.waitForTimeout(5000);
      const fresh = (await bigImgs()).filter(u => !before.has(u));
      const stop = await page.getByRole('button', {name: /^Stop/}).count();
      if (fresh.length && stop === 0) { await page.waitForTimeout(3000); const f2 = (await bigImgs()).filter(u => !before.has(u)); src = f2[f2.length - 1]; break; }
    }
    if (!src) { const msg = await page.evaluate(() => { const a = [...document.querySelectorAll('[data-message-author-role="assistant"]')]; return a.length ? a[a.length-1].innerText.slice(0, 300) : ''; }); out.push({scene: J.scene, ok: false, msg}); break; }
    const dl = page.waitForEvent('download', {timeout: 60000});
    await page.evaluate(async (u) => { const b = await (await fetch(u)).blob(); const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'gen.png'; document.body.appendChild(a); a.click(); a.remove(); }, src);
    const d = await dl; await d.saveAs(J.target);
    out.push({scene: J.scene, ok: true, secs: Math.round((Date.now() - t0) / 1000)});
  }
  return {out, url: page.url()};
}'''


def common_lines(prompts):
    """Dòng xuất hiện trong mọi prompt (khoá nhân vật, bố cục, negative) -> token ngắn để file JS gọn."""
    sets = [set(p.splitlines()) for p in prompts]
    return sorted(set.intersection(*sets), key=len, reverse=True) if sets else []


def build(ep, scenes, new=False, prompts_path=None, out_dir=None, fix=None, attached=False):
    ep = Path(ep).resolve()
    P = AA.parse_prompts(str(Path(prompts_path) if prompts_path else ep / "art" / "PROMPTS_v01.md"))
    missing = [s for s in scenes if s not in P]
    if missing:
        raise SystemExit("Không có prompt cho: " + ", ".join(missing))
    # Bài học EP26: Playwright MCP chạy JS từ gốc repo -> đường dẫn tương đối lưu nhầm chỗ; luôn dùng đường dẫn tuyệt đối
    out = Path(out_dir).resolve() if out_dir else ep / "art" / "v01"
    out.mkdir(parents=True, exist_ok=True)
    todo = [s for s in scenes if not (out / (s + ".png")).exists()]
    skipped = [s for s in scenes if s not in todo]
    tok = {"@H": H_NEXT, "@0": H_FIRST, "@S": STRICT}
    for i, line in enumerate(l for l in common_lines(list(P.values())) if len(l) > 40):
        tok["@%d" % (i + 1)] = line
    jobs = []
    for i, s in enumerate(todo):
        t = (H_FIRST if (new and i == 0) else H_NEXT) + P[s] + "\n" + STRICT
        if "CAST:" not in P[s]:
            print("CẢNH BÁO %s: prompt thiếu dòng 'CAST: <tên nhân vật trong khung>' (Owner 19/11/2026)" % s, file=sys.stderr)
        if fix:
            t += "\nFIX FROM THE PREVIOUS ATTEMPT (mandatory): " + fix
        for k, v in sorted(tok.items(), key=lambda kv: -len(kv[1])):
            t = t.replace(v, k)
        jobs.append({"t": t, "o": s + ".png", "scene": s})
    js = JS % {"attached": "true" if attached else "false", "new": "true" if new else "false", "jobs": json.dumps(jobs, ensure_ascii=False),
               "refs": json.dumps(REFS), "tok": json.dumps(tok, ensure_ascii=False), "out": json.dumps(str(out) + "/")}
    JS_DIR.mkdir(exist_ok=True)
    path = JS_DIR / ("chatgpt_art_%s_%s.js" % (ep.name.split("_")[0], todo[0] if todo else "none"))
    path.write_text(js, encoding="utf-8")
    return path, todo, skipped


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ep")
    ap.add_argument("scenes", help="A01,A02,… (≤ 6 cảnh mỗi lô)")
    ap.add_argument("--new", action="store_true", help="mở cuộc trò chuyện mới và đính kèm 3 master reference")
    ap.add_argument("--prompts")
    ap.add_argument("--out")
    ap.add_argument("--attached", action="store_true", help="ảnh mẫu đã được đính kèm sẵn bằng tay (nút + → chọn file); không mở trang mới")
    ap.add_argument("--fix", help="mô tả lỗi lần trước, nối vào cuối prompt (như --art-auto --fix)")
    a = ap.parse_args(argv)
    path, todo, skipped = build(a.ep, [s.strip() for s in a.scenes.split(",") if s.strip()], a.new, a.prompts, a.out, a.fix, a.attached)
    print(json.dumps({"js": str(path), "scenes": todo, "skipped_existing": skipped}, ensure_ascii=False))


if __name__ == "__main__":
    main()
