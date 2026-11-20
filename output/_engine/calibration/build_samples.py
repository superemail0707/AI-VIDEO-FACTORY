"""Dựng bộ mẫu hiệu chỉnh giám khảo kịch bản (D-029).

GOOD: 9 kịch bản Owner đã duyệt (EP11–EP19, đọc nguyên văn render/script.md).
BAD : 6 bản kém — 2 bản dựng lại từ góp ý thật của Owner (EP19 v1 lời dẫn thừa + "Cú twist"; EP14 v02 mở đầu yếu),
      4 bản cố ý làm hỏng có kiểm soát (không twist, đảo nhịp/chốt trước, lời giải thích dài dòng, lạc brief).
Không cần mạng. Ghi calibration/script_judge_samples.json.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.abspath(os.path.join(HERE, "..", ".."))
NONDIALOGUE = {"ep14", "ep15", "ep18"}


def read(ep):
    p = glob.glob(os.path.join(OUTPUT, ep + "_*", "render", "script.md"))[0]
    return open(p, encoding="utf-8").read()


def brief_of(md):
    m = re.search(r"\*\*Ý tưởng:\*\*\s*(.+)", md)
    return m.group(1).strip() if m else ""


def good():
    out = []
    for n in range(11, 20):
        ep = "ep%d" % n
        md = read(ep)
        out.append({"name": ep + "_approved", "expected": "good", "brief": brief_of(md), "script": md,
                    "format": "nondialogue" if ep in NONDIALOGUE else "dialogue", "source": "Owner đã duyệt"})
    return out


def bad():
    ep19 = read("ep19")
    v1 = ep19.replace("## F02 — Ngang bắt chước", "## F02 — Ngang bắt chước").replace(
        "Âm: 'rrr' run, 'cót két', 'bịch', Tí cười (SFX).",
        "Âm: 'rrr' run, 'cót két', 'bịch', Tí cười (SFX).\n- **Ngang:** Ngang quyết tâm bắt chước đại sư.\n- **Ngang:** Ngang vắt chân lên đầu và lăn ra thảm.")
    v1 = v1.replace("whoosh mồ hôi, cười (SFX).",
                    "whoosh mồ hôi, cười (SFX).\n- **Ngang:** Đến lượt Tí thể hiện.\n- **Ngang:** Tí cũng rối như bánh quy.")
    v1 = v1.replace("- **Ngang:** Đại sư không tập.", "- **Ngang:** Cú twist: đại sư không tập.")
    v1 = v1.replace("bỏ 'Cú twist' theo Owner", "đọc nguyên chú thích khung")
    ep14 = read("ep14")
    weak = re.sub(r"## F00 — Đi dạo rồi giật bắn.*?\n\n## F01", (
        "## F00 — Một buổi sáng  (≈6.5 s, vào cảnh: fade)\n*Hình:* Toàn cảnh căn phòng buổi sáng, rèm cửa lay nhẹ. "
        "Mimi ngủ dậy, vươn vai, ngáp, đi ăn hạt, liếm lông. Không có gì bất thường xảy ra. Không thoại.\n\n"
        "## F00b — Đi dạo  (≈4.0 s, vào cảnh: fade)\n*Hình:* Mimi đi dạo quanh phòng, ngửi chân ghế, nhìn ra cửa sổ. "
        "Không thoại.\n\n## F01"), ep14, flags=re.S)
    return [
        {"name": "ep19_v1_reconstructed", "expected": "bad", "brief": brief_of(ep19), "script": v1, "format": "dialogue",
         "source": "Owner góp ý EP19 v1: lời dẫn thừa ở cảnh hình đã tự kể, đọc 'Cú twist' (IMPROVEMENT_LOG 12/11)"},
        {"name": "ep14_v02_weak_open", "expected": "bad", "brief": brief_of(ep14), "script": weak, "format": "nondialogue",
         "source": "Owner từ chối EP14 v02: cảnh mở yếu (workflow 11/11); dựng lại mở đầu chậm, không hook"},
        {"name": "ep12_no_twist", "expected": "bad", "format": "dialogue",
         "brief": "Tí mua ổ sang cho Mimi, nhưng Mimi chỉ chọn thùng carton cũ.",
         "script": """# Kịch bản — Ổ mới của Mimi

## F01 — Quà mới  (≈5.0 s, vào cảnh: fade)
*Hình:* Tí mở hộp, lấy ra ổ mèo mới màu hồng, đặt giữa phòng.
- **Tí:** Anh mua ổ mới cho Mimi nè.

## F02 — Mimi thử ổ  (≈6.0 s, vào cảnh: cut)
*Hình:* Mimi đi tới ổ mới, ngửi rồi nằm vào, ngủ ngon.
- **Ngang:** Mimi thích ổ mới quá.

## F03 — Vui vẻ  (≈6.0 s, vào cảnh: cut)
*Hình:* Tí và Ngang ngồi nhìn Mimi ngủ trong ổ mới.
- **Tí:** Ừ, mua đúng rồi.
- **Ngang:** Mai mua thêm cái nữa nha.

## F04 — End card  (≈3.2 s, vào cảnh: cut)

## Kết
Bạn đã mua ổ cho mèo chưa?
""", "source": "Cố ý làm hỏng: bỏ xung đột và twist (Mimi chọn ngay ổ mới)"},
        {"name": "ep16_shuffled", "expected": "bad", "format": "dialogue",
         "brief": brief_of(read("ep16")),
         "script": """# Kịch bản — Nhà tôi nuôi 2 con mèo

## F01 — Kết luận trước  (≈4.0 s, vào cảnh: cut)
*Hình:* Tí đứng giữa phòng nói thẳng kết luận với camera.
- **Tí:** Nuôi một con mèo, tặng kèm bà hoàng.

## F02 — Ngang ngủ  (≈5.0 s, vào cảnh: cut)
*Hình:* Ngang ngủ trên sofa. Mimi ngủ ở phòng khác, không cùng khung.
- **Tí:** Ngang đang ngủ.

## F03 — Ngang dậy  (≈5.0 s, vào cảnh: cut)
*Hình:* Ngang thức dậy, đi rửa mặt.
- **Ngang:** Anh nói gì đó?
- **Tí:** Không có gì đâu em.

## F04 — Mimi  (≈5.0 s, vào cảnh: cut)
*Hình:* Mimi ăn hạt.
- **Tí:** Mimi cũng dậy rồi.

## F05 — End card  (≈3.2 s, vào cảnh: cut)
""", "source": "Cố ý làm hỏng: chốt ở đầu, không leo thang, không đối chiếu Ngang–Mimi"},
        {"name": "ep17_wordy_explained", "expected": "bad", "format": "dialogue",
         "brief": brief_of(read("ep17")),
         "script": """# Kịch bản — Tổng tài ở nhà

## F01 — Giới thiệu  (≈8.0 s, vào cảnh: fade)
*Hình:* Tí đứng trong văn phòng, nói với camera.
- **Tí:** Xin chào, tôi là Tí, tôi là giám đốc một công ty lớn.
- **Tí:** Ở công ty ai cũng nghe lời tôi vì tôi là sếp.

## F02 — Về nhà  (≈8.0 s, vào cảnh: fade)
*Hình:* Tí về nhà, Ngang đang xem tivi.
- **Tí:** Nhưng khi về nhà thì tôi lại không phải là sếp nữa.
- **Ngang:** Anh ơi hôm nay đến lượt anh rửa chén đó anh nhớ chưa.

## F03 — Giải thích  (≈9.0 s, vào cảnh: cut)
*Hình:* Tí rửa chén, nói với camera.
- **Tí:** Đó là lý do vì sao tôi nói ở nhà tôi không có tiếng nói.
- **Tí:** Vì vợ tôi mới là người quyết định mọi thứ trong nhà này.

## F04 — End card  (≈3.2 s, vào cảnh: cut)
""", "source": "Cố ý làm hỏng: kể lể giải thích trò đùa, câu dài, không hình ảnh hài, không Mimi"},
        {"name": "ep13_offbrief", "expected": "bad", "format": "dialogue",
         "brief": brief_of(read("ep13")),
         "script": """# Kịch bản — Đi chợ

## F01 — Danh sách  (≈5.0 s, vào cảnh: cut)
*Hình:* Tí cầm tờ danh sách đi chợ trong bếp.
- **Tí:** Hôm nay mua thịt, rau với trứng.

## F02 — Siêu thị  (≈6.0 s, vào cảnh: cut)
*Hình:* Tí và Ngang đẩy xe trong siêu thị.
- **Ngang:** Anh lấy thêm sữa nha.

## F03 — Thanh toán  (≈6.0 s, vào cảnh: cut)
*Hình:* Hai người xếp hàng thanh toán.
- **Tí:** Hết bao nhiêu vậy em?
- **Ngang:** Năm trăm nghìn anh.

## F04 — End card  (≈3.2 s, vào cảnh: cut)
""", "source": "Cố ý làm hỏng: lạc brief (không Mimi, không cái ly, không trọng lực)"},
    ]


if __name__ == "__main__":
    samples = good() + bad()
    p = os.path.join(HERE, "script_judge_samples.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(samples, fh, ensure_ascii=False, indent=1)
    print(json.dumps({"file": p, "good": sum(s["expected"] == "good" for s in samples),
                      "bad": sum(s["expected"] == "bad" for s in samples)}, ensure_ascii=False))
