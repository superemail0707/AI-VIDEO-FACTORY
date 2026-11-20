# -*- coding: utf-8 -*-
"""Quy tắc phụ đề không đè nhân vật (Owner 08/11/2026) — nmt-engine (output/_engine/cute_engine.py).
Chạy: python3 -m unittest tests.unit.test_subtitle_layout"""
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[2] / "output" / "_engine"
sys.path.insert(0, str(ENGINE))

import cute_engine as E  # noqa: E402
import platform_export as PX  # noqa: E402
import safe_frame as SF  # noqa: E402
from PIL import Image  # noqa: E402

SPRITE = "TI_Y3_HOME_SLEEPY"   # sprite approved (visual_rebuild_v01)


LONG = "Năm ba rồi mà anh vẫn thương em nhiều như ngày đầu tiên luôn"


def _episode(fn, text="Năm ba, anh yêu cả lúc em chưa gội đầu."):
    """Một cảnh 1 s, một câu phụ đề suốt cảnh."""
    E.SCENES[:] = [("S1", 1.0, "test", "cut", 0.0)]
    E.STARTS.clear()
    E.STARTS["S1"] = 0.0
    E.FUNCS.clear()
    E.FUNCS["S1"] = fn
    E.CUES[:] = [(0.0, 1.0, text)]


def _bg():
    return Image.new("RGBA", (E.W, E.H), E.CREAM + (255,))


class PanelLayoutTests(unittest.TestCase):
    def tearDown(self):
        E.PLATFORM = None
        E.SAFE916 = True

    def test_content_top_three_quarters_subtitle_band_quarter(self):
        self.assertAlmostEqual(E.CONTENT_FRAC, 0.75)
        self.assertEqual(E.tray_top(), 1440)               # 1920 × 3/4
        self.assertLessEqual(E.band_frac(), 1 / 3)

    def test_band_over_one_third_is_blocked(self):
        old = E.CONTENT_FRAC
        try:
            E.CONTENT_FRAC = 0.80                            # dải 20%: hợp lệ (tuỳ nội dung)
            self.assertEqual(E.tray_top(), 1536)
            E.CONTENT_FRAC = 0.60                            # dải 40% > 1/3: chặn
            with self.assertRaises(SystemExit):
                E.tray_top()
        finally:
            E.CONTENT_FRAC = old

    def test_bottom_panel_stays_above_subtitle_band_even_when_zoomed(self):
        for plat in [None] + PX.ORDER:
            E.PLATFORM = plat
            pos, k = E.panel_layout()
            bottom = pos[1][1] + E.PANEL_H * k
            self.assertLessEqual(bottom * E.PANEL_ZOOM_MAX, E.tray_top() - 12 + 1e-6, plat)
            self.assertGreaterEqual(pos[0][1], 150, plat)   # tránh tab trên cùng của app

    def test_subtitle_inside_band_for_every_version(self):
        _episode(lambda t: (lambda im: (E.subtitle(im, t, y=1690), im)[1])(_bg()))
        for plat in [None] + PX.ORDER:
            rep = E.check_subs(step=30, plat=plat)
            self.assertEqual(rep["outside_band"], [], plat)
            self.assertEqual(rep["band_top"], SF.CONTENT_BOTTOM)   # khung an toàn: dải bắt đầu 1460
            self.assertEqual(rep["safe_frame_violations"], [], plat)
        E.SAFE916 = False                                           # bố cục cũ vẫn giữ quy tắc 3/4–1/4
        rep = E.check_subs(step=30)
        self.assertEqual((rep["outside_band"], rep["band_top"]), ([], 1440))


class CheckSubsTests(unittest.TestCase):
    """Các kiểm tra phát hiện lỗi chạy trên bố cục cũ (SAFE916=False): ở khung an toàn, phần cảnh dưới tray_top()
    bị cắt bỏ nên nhân vật không thể xuống dải phụ đề và phụ đề không thể chạm hàng watermark."""
    def setUp(self):
        E.SAFE916 = False

    def tearDown(self):
        E.PLATFORM = None
        E.HIDE_SPRITES, E.DRAW_SUB = False, True
        E.SAFE916 = True

    def test_detects_character_under_subtitle(self):
        def scene(t):
            im = _bg()
            E.place(im, SPRITE, 540, 1900, h=1500, shadow=False)   # thân nhân vật kéo tới đáy khung
            E.subtitle(im, t, y=1610, tray=False)   # cảnh quên dải nền: nhân vật lộ dưới phụ đề
            return im
        _episode(scene)
        rep = E.check_subs(step=30)
        self.assertFalse(rep["pass"])
        self.assertGreater(rep["worst_by_scene"]["S1"], 0.05)

    def test_passes_when_character_above_tray(self):
        def scene(t):
            im = _bg()
            E.place(im, SPRITE, 540, E.tray_top() + 40, h=E.tray_top() - 300, shadow=False)
            E.sub_tray(im)
            E.subtitle(im, t, y=E.sub_y_bottom())
            return im
        _episode(scene)
        for plat in [None] + PX.ORDER:
            rep = E.check_subs(step=30, plat=plat)
            self.assertTrue(rep["pass"], (plat, rep["violations"][:2]))
            self.assertGreater(rep["frames_checked"], 0)

    def _pushed_down(self, dodge):
        """Ép phụ đề xuống ngang hàng watermark (đệm trên lớn); dodge=False tắt né watermark."""
        old_pad, old_wm = E.SUB_TOP_PAD, E._wm_for_layout
        E.SUB_TOP_PAD = E.wm_box("tiktok")[1] - E.tray_top() - 40
        if not dodge:
            E._wm_for_layout = lambda: None
        try:
            _episode(lambda t: (lambda im: (E.subtitle(im, t, y=1690), im)[1])(_bg()), text=LONG)
            return [E.check_subs(step=30, plat=p) for p in PX.ORDER]
        finally:
            E.SUB_TOP_PAD, E._wm_for_layout = old_pad, old_wm

    def test_detects_subtitle_touching_watermark(self):
        for rep in self._pushed_down(dodge=False):
            self.assertTrue(rep["watermark_violations"], rep["platform"])
            self.assertFalse(rep["pass"], rep["platform"])

    def test_subtitle_dodges_watermark_when_low(self):
        for rep in self._pushed_down(dodge=True):
            self.assertEqual(rep["watermark_violations"], [], rep["platform"])

    def test_platform_subtitle_clear_of_watermark(self):
        _episode(lambda t: (lambda im: (E.sub_tray(im), E.subtitle(im, t, y=E.sub_y_bottom()), im)[2])(_bg()))
        for plat in PX.ORDER:
            rep = E.check_subs(step=30, plat=plat)
            self.assertEqual(rep["watermark_violations"], [], plat)
            wm = rep["watermark_box"]
            self.assertEqual(len(wm), 4)

    def test_flags_restored_after_check(self):
        _episode(lambda t: _bg())
        E.check_subs(step=30, plat="tiktok")
        self.assertFalse(E.HIDE_SPRITES)
        self.assertTrue(E.DRAW_SUB)
        self.assertIsNone(E.PLATFORM)



class SafeFrameTests(unittest.TestCase):
    """NMT-SAFE-916 v1 (Owner 08/11/2026): TikTok/Shorts cắt hai bên và đè đỉnh/đáy; ba nền tảng dùng chung khung."""
    def tearDown(self):
        E.PLATFORM = None
        E.HIDE_SPRITES, E.DRAW_SUB = False, True

    def test_character_kept_out_of_band_and_inside_safe_zone(self):
        def scene(t):
            im = _bg()
            E.place(im, SPRITE, 540, 1900, h=1500, shadow=False)   # lấn xuống đáy ở bố cục cũ
            E.subtitle(im, t, y=1610)
            return im
        _episode(scene, text=LONG)
        for plat in [None] + PX.ORDER:
            rep = E.check_subs(step=30, plat=plat)
            self.assertTrue(rep["pass"], (plat, rep["violations"][:1], rep["safe_frame_violations"][:1]))
            self.assertEqual(rep["safe_frame"], "NMT-SAFE-916 v1")

    def test_subtitle_box_in_safe_band_same_for_all_platforms(self):
        _episode(lambda t: (lambda im: (E.subtitle(im, t, y=1690), im)[1])(_bg()), text=LONG)
        boxes = []
        for plat in [None] + PX.ORDER:
            E.PLATFORM = plat
            E.SUB_BOX = None
            E.frame(0.6)
            boxes.append(tuple(round(v) for v in E.SUB_BOX))
            self.assertEqual(SF.check_box(E.SUB_BOX, "subtitle"), [], plat)
            self.assertGreaterEqual(E.SUB_BOX[1], SF.SUB_TOP - 20)
        self.assertEqual(len(set(boxes)), 1)

    def test_content_panel_inside_safe_zone_plain_surround(self):
        def scene(t):
            return Image.new("RGBA", (E.W, E.H), (40, 120, 200, 255))   # nội dung xanh tới sát mép
        _episode(scene)
        fr = E.frame(0.2).convert("RGB")
        self.assertEqual(fr.size, (1080, 1920))
        self.assertEqual(fr.getpixel((540, 800)), (40, 120, 200))       # nội dung ở giữa
        for xy in [(540, 100), (50, 800), (1030, 800), (540, 1800)]:     # xung quanh: màu trơn, không mờ
            self.assertEqual(fr.getpixel(xy), E.CREAM, xy)
        a = __import__("numpy").asarray(fr)
        blue = (a[:, :, 2] > 150) & (a[:, :, 0] < 80)
        ys, xs = blue.nonzero()
        self.assertGreaterEqual(xs.min(), SF.CROP_X)
        self.assertLessEqual(xs.max(), SF.W - SF.CROP_X)
        self.assertGreaterEqual(ys.min(), SF.CONTENT_TOP)
        self.assertLessEqual(ys.max(), SF.CONTENT_BOTTOM)

    def test_watermark_inside_crop_safe_zone(self):
        for plat in PX.ORDER:
            wm = E.wm_box(plat)
            self.assertEqual(SF.check_box(wm, "watermark")[:1] and
                             [m for m in SF.check_box(wm, "watermark") if "ngang" in m], [], plat)
            self.assertLessEqual(wm[2], SF.W - SF.CROP_X)

    def test_subtitle_border_always_centered(self):
        for text in ["Ừ", "Năm ba, anh yêu cả lúc em chưa gội đầu.", LONG]:
            _episode(lambda t: (lambda im: (E.subtitle(im, t, y=1690), im)[1])(_bg()), text=text)
            for plat in [None] + PX.ORDER:
                E.PLATFORM = plat
                for t in (0.05, 0.6):                  # lúc trượt vào và lúc đứng yên
                    E.SUB_BOX = None
                    E.frame(t)
                    if E.SUB_BOX:
                        self.assertAlmostEqual((E.SUB_BOX[0] + E.SUB_BOX[2]) / 2, E.W / 2, delta=SF.SUB_CENTER_TOL, msg=(text, plat, t))

    def test_check_box_flags_off_center_subtitle(self):
        self.assertTrue(SF.check_box((140, 1480, 880, 1600), "subtitle"))     # tâm 510 như EP10 v06
        self.assertEqual(SF.check_box((140, 1480, 940, 1600), "subtitle"), [])

    def test_check_box_flags_old_wide_subtitle(self):
        self.assertTrue(SF.check_box((75, 1460, 1005, 1575), "subtitle"))     # viên phụ đề EP10 v04


if __name__ == "__main__":
    unittest.main()
