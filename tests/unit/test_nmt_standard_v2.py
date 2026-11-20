"""Quy trình chuẩn NMT v2 (Owner duyệt 18/11/2026): phụ đề theo từng từ, thumbnail, giảm âm outro."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[2] / "output" / "_engine"
sys.path.insert(0, str(ENGINE))
import cute_engine as E  # noqa: E402
import scene_kit as K  # noqa: E402
from PIL import Image  # noqa: E402


class WordCaptionTests(unittest.TestCase):
    def test_card_dark_background_and_yellow_keyword(self):
        card = K.word_card("Quà của anh nè", ("quà",))
        px = [card.getpixel((x, card.height // 2)) for x in range(card.width)]
        self.assertTrue(any(p[:3] == K.WORD_KEY[:3] for p in px), "từ khoá phải màu vàng")
        corner = card.getpixel((30, 6))
        self.assertLess(sum(corner[:3]), 90)            # nền đen
        self.assertGreater(corner[3], 200)

    def test_chunks_of_at_most_four_words_one_line(self):
        """Owner 19/11/2026 (tối): mỗi lúc chỉ 3–4 chữ trên 1 dòng, cụm sau thay cụm trước theo giọng."""
        text = "Đàn ông đích thực phải biết rửa bát cả đời luôn đó!"
        chunks = K.word_chunks(text)
        self.assertEqual([w for c in chunks for w in c], text.split())
        self.assertTrue(all(1 <= len(c) <= 4 for c in chunks))
        one = K.word_card(text, (), 1)
        self.assertEqual(one.height, K.word_card("Quà", (), 1).height)   # luôn 1 dòng
        self.assertEqual(one.size, K.word_card(text, (), 4).size)        # cả cụm 1 hiện cùng lúc
        self.assertNotEqual(one.tobytes(), K.word_card(text, (), 5).tobytes())   # chữ thứ 5 -> cụm mới thay cụm cũ

    def test_chunk_breaks_prefer_punctuation_and_keep_names(self):
        self.assertEqual(K.word_chunks("Còn một phút! Chốt đơn thôi!"), (("Còn", "một", "phút!"), ("Chốt", "đơn", "thôi!")))
        joined = [" ".join(c) for c in K.word_chunks("Anh ơi, giỏ hàng Black Friday của em nè!")]
        self.assertTrue(any("Black Friday" in c for c in joined))
        self.assertFalse(any(c[-1].lower() in ("của", "cây", "vì") for c in K.word_chunks("Boss Mimi đang chấm bài của anh đó nha!")))
        self.assertEqual(K.word_chunks("Quà của anh nè"), (("Quà", "của", "anh", "nè"),))

    def test_breaks_follow_voice_pauses(self):
        """Ngắt ở chỗ giọng ngừng; chỗ ngừng ước lượng lệch 1 chữ được dời về dấu câu (bài học EP29 V3)."""
        wl = [{"word": w, "start": a, "end": b} for w, a, b in
              [("Mua", 0, .2), ("luôn!", .2, .4), ("Thẻ", .4, .6), ("anh", .97, 1.1), ("lưu", 1.1, 1.3),
               ("vào", 1.3, 1.4), ("máy", 1.4, 1.5), ("em", 1.5, 1.6), ("nè!", 1.6, 1.8)]]
        gaps = K.voice_gaps(wl)
        self.assertGreater(gaps[1], 0.3)            # dời về sau 'luôn!'
        self.assertEqual(gaps[2], 0.0)
        chunks = K.word_chunks("Mua luôn! Thẻ anh lưu vào máy em nè!", 4, gaps)
        self.assertEqual(chunks[0], ("Mua", "luôn!"))
        short = K.word_chunks("Khoan! Đừng bấm!", 4, (0.34, 0.0))
        self.assertEqual(short, (("Khoan!",), ("Đừng", "bấm!")))   # câu ngắn có chỗ ngừng dài vẫn tách theo giọng

    def test_manual_breaks_win_and_are_checked(self):
        text = "Em xoá vì thanh toán hết rồi đó anh!"
        m = "Em xoá | vì thanh toán hết | rồi đó anh!"
        self.assertEqual(K.word_chunks(text, 4, None, m)[1], ("vì", "thanh", "toán", "hết"))
        with self.assertRaises(SystemExit):
            K.word_chunks(text, 4, None, "Em xoá | vì thanh toán")          # thiếu chữ
        with self.assertRaises(SystemExit):
            K.word_chunks(text, 4, None, "Em xoá vì thanh toán | hết rồi đó anh!")   # cụm 5 chữ

    def test_keyword_larger_than_normal_words(self):
        plain = K.word_card("Quà của anh nè", ())
        hot = K.word_card("Quà của anh nè", ("quà",))
        self.assertGreater(hot.width, plain.width)
        self.assertGreaterEqual(K.WORD_KEY_SCALE, 1.15)

    def test_card_fits_subtitle_band(self):
        card = K.word_card("Đàn ông đích thực phải biết rửa bát cả đời luôn đó!", ())
        self.assertLessEqual(card.width, 800)
        self.assertLessEqual(K.WORD_SUB_Y + card.height / 2, 1680)
        self.assertGreaterEqual(K.WORD_SUB_Y - card.height / 2, 1480)


class OutroGainTests(unittest.TestCase):
    def test_outro_sfx_half_volume(self):
        full = K.subscribe_sfx("F20")
        half = K.subscribe_sfx("F20", gain=K.OUTRO_SFX_GAIN)
        self.assertEqual(len(full), len(half))
        for a, b in zip(full, half):
            self.assertAlmostEqual(b[4], a[4] * 0.5, places=4)
            self.assertEqual(a[:4], b[:4])


class ThumbnailTests(unittest.TestCase):
    def test_thumbnail_size_and_text_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "a.png")
            Image.new("RGB", (941, 1672), (200, 120, 160)).save(src)
            p = K.make_thumbnail(src, "QUÀ 19/11", "LÀ… EM?!", tmp, zoom=1.2)
            im = Image.open(p)
            self.assertEqual(im.size, (1080, 1920))
            self.assertTrue(os.path.exists(os.path.join(tmp, "cover.jpg")))
            self.assertLess(sum(im.getpixel((140, 200))[:3]), 120)      # khối đen chữ ở 1/3 trên
            self.assertGreater(sum(im.getpixel((540, 1500))[:3]), 300)  # phần dưới là tranh


if __name__ == "__main__":
    unittest.main()


class ThumbnailV2Tests(unittest.TestCase):
    """prompts/thumbnail_designer_v1.md: chữ trong vùng an toàn 80 % × 70 %, có bản 1/6 và bản che mép."""

    def test_two_by_three_art_extended_and_text_inside_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "t.png")
            Image.new("RGB", (1024, 1536), (40, 30, 90)).save(src)
            r = K.make_thumbnail_v2(src, ["TƯỞNG QUÀ", "MÁY GAME…", "HÓA RA LÀ?!"], "HÓA RA LÀ?!", tmp)
            self.assertTrue(r["inside_safe"])
            im = Image.open(r["path"])
            self.assertEqual(im.size, (1080, 1920))
            self.assertTrue(os.path.exists(os.path.join(tmp, "_qa", "thumb_small.png")))
            self.assertEqual(Image.open(os.path.join(tmp, "_qa", "thumb_small.png")).size, (180, 320))
            self.assertTrue(os.path.exists(os.path.join(tmp, "_qa", "thumb_safe.png")))
            lime = sum(1 for p in im.crop(r["text_box"]).getdata() if p[1] > 230 and p[0] > 190 and p[2] < 90)
            self.assertGreater(lime, 500)                        # từ khoá vàng chanh có mặt

    def test_text_outside_safe_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "t.png")
            Image.new("RGB", (1080, 1920), (40, 30, 90)).save(src)
            with self.assertRaises(SystemExit):
                K.make_thumbnail_v2(src, ["A B C", "D E F"], "D", tmp, text_top=60)
