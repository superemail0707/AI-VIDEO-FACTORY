# -*- coding: utf-8 -*-
"""Giai đoạn A (NMT_PIPELINE_UPGRADE_PLAN): qa_checks (tranh, chuyển cảnh, tiếng/hình), metrics, scene_kit, mẫu tập mới."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ENGINE = Path(__file__).resolve().parents[2] / "output" / "_engine"
sys.path.insert(0, str(ENGINE))

import cute_engine as E  # noqa: E402
import metrics as MX  # noqa: E402
import qa_checks as Q  # noqa: E402
import scene_kit as K  # noqa: E402


def _noise(w=1080, h=1920, seed=1):
    import numpy as np
    rng = np.random.default_rng(seed)
    return Image.fromarray(rng.integers(0, 255, (h, w, 3), dtype="uint8"), "RGB")


class ArtCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name) / "art" / "v01"
        self.d.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def _ann(self, data):
        (self.d / "safe_annotations.json").write_text(json.dumps(data), encoding="utf-8")

    def test_full_bleed_annotated_passes(self):
        _noise().save(self.d / "A01.png")
        self._ann({"A01": {"char_bottom_y": 1264, "subtitles": True}})
        rep = Q.check_art(str(self.d))
        self.assertTrue(rep["pass"], rep["items"][0]["errors"])
        self.assertGreaterEqual(rep["items"][0]["coverage"], 0.99)
        self.assertTrue((self.d / "_qa" / "A01_overlay.jpg").exists())
        self.assertTrue((self.d / "_qa" / "A01_band.jpg").exists())

    def test_cream_frame_fails_coverage(self):
        im = Image.new("RGB", (1080, 1920), (255, 246, 236))   # nền kem thừa (bài học 10/11)
        im.paste(_noise(900, 1500), (90, 210))
        im.save(self.d / "A01.png")
        self._ann({"A01": {"char_bottom_y": 1200}})
        rep = Q.check_art(str(self.d))
        self.assertFalse(rep["pass"])
        self.assertIn("độ phủ", rep["items"][0]["errors"][0])

    def test_face_in_crop_margin_fails(self):
        _noise().save(self.d / "A01.png")
        self._ann({"A01": {"char_bottom_y": 1200, "face_x": [780, 1040]}})   # Mimi sát mép phải (EP20 A14b v1)
        rep = Q.check_art(str(self.d))
        self.assertFalse(rep["pass"])
        self.assertIn("lề cắt", rep["items"][0]["errors"][0])
        self._ann({"A01": {"char_bottom_y": 1200, "face_x": [200, 900]}})
        self.assertTrue(Q.check_art(str(self.d))["pass"])

    def test_character_in_subtitle_band_fails_only_with_subtitles(self):
        _noise().save(self.d / "A01.png")
        self._ann({"A01": {"char_bottom_y": 1580, "subtitles": True}})   # giày Tí trong dải (EP17 F01 v01)
        self.assertFalse(Q.check_art(str(self.d))["pass"])
        self._ann({"A01": {"char_bottom_y": 1580, "subtitles": False}})  # cảnh không phụ đề: được phép
        self.assertTrue(Q.check_art(str(self.d))["pass"])

    def test_missing_annotation_blocks(self):
        _noise().save(self.d / "A01.png")
        rep = Q.check_art(str(self.d))
        self.assertFalse(rep["pass"])
        self.assertIn("chưa có chú thích", rep["items"][0]["errors"][0])
        self.assertTrue(Q.check_art(str(self.d), need_annotations=False)["pass"])

    def test_near_duplicate_and_superseded_skipped(self):
        a = _noise(seed=2)
        a.save(self.d / "A01.png")
        a.save(self.d / "A02.png")
        _noise(seed=3).save(self.d / "A03_v01_superseded.png")
        rep = Q.check_art(str(self.d), need_annotations=False)
        self.assertEqual(rep["images"], 2)
        self.assertEqual([(p["a"], p["b"]) for p in rep["possible_duplicates"]], [("A01", "A02")])


class TransitionTests(unittest.TestCase):
    def test_iris_into_end_card_fails(self):   # EP12/EP13
        sc = [("F01", 3.0, "Mở", "cut", 0.0), ("F02", 3.2, "End card", "iris", 0.55)]
        self.assertFalse(Q.check_transitions(sc)["pass"])
        sc[1] = ("F02", 3.2, "End card", "cut", 0.0)
        self.assertTrue(Q.check_transitions(sc)["pass"])

    def test_invalid_type_and_too_long(self):
        self.assertFalse(Q.check_transitions([("F01", 2, "a", "cut", 0), ("F02", 2, "b", "wipe", 0.2)])["pass"])
        self.assertFalse(Q.check_transitions([("F01", 0.3, "a", "cut", 0), ("F02", 2, "b", "fade", 0.5)])["pass"])
        self.assertTrue(Q.check_transitions([("F01", 2, "a", "cut", 0), ("F02", 2, "b", "whip", 0.2)])["pass"])


class SyncTests(unittest.TestCase):
    SC = [("F01", 3.0, "a", "cut", 0.0), ("F02", 3.0, "b", "cut", 0.0)]
    ST = {"F01": 0.0, "F02": 3.0}

    def _run(self, voice, vdur, onset=0.11):
        return Q.check_sync(self.SC, voice, self.ST, vdur, lambda v: onset)

    def test_opening_line_late_fails(self):   # EP19 v1: 0,35 + onset 0,11
        self.assertFalse(self._run([("V1", "F01", 0.35, "ti", "x")], {"V1": 1.0})["pass"])
        self.assertTrue(self._run([("V1", "F01", 0.05, "ti", "x")], {"V1": 1.0})["pass"])   # EP19 đã duyệt

    def test_overlap_and_past_end_fail(self):
        v = [("V1", "F01", 0.05, "ti", "x"), ("V2", "F01", 0.6, "ngang", "y")]
        self.assertFalse(self._run(v, {"V1": 1.5, "V2": 1.0})["pass"])
        self.assertFalse(self._run([("V1", "F02", 2.5, "ti", "x")], {"V1": 1.0})["pass"])

    def test_late_scene_lead_is_warning(self):
        rep = self._run([("V1", "F01", 0.05, "ti", "x"), ("V2", "F02", 0.8, "ti", "y")], {"V1": 1, "V2": 1})
        self.assertTrue(rep["pass"])
        self.assertEqual(len(rep["warnings"]), 1)


class MetricsTests(unittest.TestCase):
    def test_record_and_summary(self):
        with tempfile.TemporaryDirectory() as t:
            ep = Path(t) / "ep42_demo"
            (ep / "render").mkdir(parents=True)
            (ep / "render" / "ep42.py").write_text("a = 1\n# chú thích\n\nb = 2\n", encoding="utf-8")
            (ep / "render" / "render_log.jsonl").write_text('{"scene": "F01", "render_s": 12.5}\n', encoding="utf-8")
            (ep / "workflow.json").write_text(json.dumps({"history": [
                {"event": "submitted", "stage": "script"}, {"event": "rejected", "stage": "script"},
                {"event": "approved", "stage": "script", "by": "auto-review (codex, 8.5/10, lần 2)"}]}), encoding="utf-8")
            MX.record(str(ep), "tts", 3.21)
            MX.record(str(ep), "mux", 1.0, status="blocked")
            rep = MX.summary(str(ep))
            self.assertEqual(rep["code_lines_total"], 2)
            self.assertEqual(rep["steps"]["tts"]["runs"], 1)
            self.assertEqual(rep["steps"]["mux"]["failed"], 1)
            self.assertEqual(rep["render_seconds_logged"], 12.5)
            self.assertEqual(rep["revision_rounds"]["script"], 1)
            self.assertEqual(rep["gates"]["script"]["auto_approved"], 1)
            self.assertIsNone(rep["claude_tokens"])
            self.assertTrue((ep / "render" / "metrics.json").exists())


class SceneKitTests(unittest.TestCase):
    def test_cam_never_zooms_out(self):
        im = _noise(1080, 1920).convert("RGBA")
        self.assertEqual(K.cam(im, z=0.9).tobytes(), K.cam(im, z=1.0).tobytes())

    def test_pop_and_mix(self):
        self.assertEqual(K.pop(0.0, 1.0), 0.0)
        self.assertAlmostEqual(K.pop(1.11, 1.0), 1.12, places=2)
        self.assertEqual(K.mix(2, 4, 0.5), 3)

    def test_art_loader_fits_and_aliases(self):
        with tempfile.TemporaryDirectory() as t:
            a, b = Path(t) / "a", Path(t) / "b"
            a.mkdir(), b.mkdir()
            _noise(540, 960).save(a / "A01.png")
            _noise(800, 1200, seed=5).save(b / "F01.png")
            art = K.art_loader(a, aliases={"ep17_": b})
            self.assertEqual(art("A01").size, (1080, 1920))
            self.assertEqual(art("ep17_F01").size, (1080, 1920))

    def test_post_without_subtitles_clears_pending(self):
        post = K.make_post(subtitles=False)
        E._SUB_PENDING = ("x",)
        im = Image.new("RGBA", (1080, 1920))
        self.assertIs(post(im), im)
        self.assertIsNone(E._SUB_PENDING)

    def test_cut_at_adds_measured_onset(self):
        old_voice, old_on = list(E.VOICE), dict(E.VONSET)
        try:
            E.VOICE[:] = [("V9", "F01", 0.4, "ti", "x")]
            E.VONSET["V9"] = 0.09
            self.assertAlmostEqual(K.cut_at("V9"), 0.49)
            self.assertEqual(K.cut_at("NOPE", 1.5), 1.5)
        finally:
            E.VOICE[:] = old_voice
            E.VONSET.clear(); E.VONSET.update(old_on)


class TemplateTests(unittest.TestCase):
    def test_new_episode_template_defaults(self):
        import nmt_engine
        src = nmt_engine.TEMPLATE
        self.assertIn('"Outro", "cut", 0.0', src)
        self.assertIn("FIRST_LEAD = 0.05", src)
        self.assertIn("ART_CHECK = True", src)
        compile(src.format(n="42", title="Thử", title_up="THỬ", brief="Thử"), "ep42.py", "exec")


if __name__ == "__main__":
    unittest.main()
