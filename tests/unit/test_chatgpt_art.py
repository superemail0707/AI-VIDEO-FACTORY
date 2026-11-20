# -*- coding: utf-8 -*-
"""Tạo tranh qua ChatGPT web (Playwright) — cách tạm thời khi Codex hết lượt (Owner 13/11/2026)."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ENGINE = Path(__file__).resolve().parents[2] / "output" / "_engine"
sys.path.insert(0, str(ENGINE))
import chatgpt_art as CA  # noqa: E402

LOCK = "CHARACTER IDENTITY LOCK: Ti = navy T-shirt, Ngang = terracotta shirt, Mimi = brown tabby cat."
NEG = "NEGATIVE: no text, no letters, no numbers, no watermark, no logo, no panel border."
MD = "# P\n\n" + "".join("### %s — c\n\n```prompt\n%s\nSCENE: room %d.\n%s\n```\n\n" % (s, LOCK, i, NEG)
                          for i, s in enumerate(["A01", "A02", "A03"]))


class ChatgptArtTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ep = Path(self.tmp.name) / "ep99_thu"
        (self.ep / "art").mkdir(parents=True)
        (self.ep / "art" / "PROMPTS_v01.md").write_text(MD, encoding="utf-8")
        self.p = mock.patch.object(CA, "JS_DIR", Path(self.tmp.name) / "js")
        self.p.start()

    def tearDown(self):
        self.p.stop()
        self.tmp.cleanup()

    def jobs(self, path):
        js = path.read_text(encoding="utf-8")
        jobs = json.loads(re.search(r"JOBS = (\[.*?\]), REFS", js).group(1))
        tok = json.loads(re.search(r"TOK = (\{.*?\}), OUT", js).group(1))
        out = []
        for j in jobs:
            t = j["t"]
            for k in tok:          # cùng thứ tự với JS (Object.keys)
                t = tok[k].join(t.split(k))
            out.append((j["scene"], t))
        return out

    def test_tokens_restore_exact_prompt_and_first_header(self):
        path, todo, skipped = CA.build(self.ep, ["A01", "A02"], new=True)
        self.assertEqual((todo, skipped), (["A01", "A02"], []))
        got = dict(self.jobs(path))
        self.assertTrue(got["A01"].startswith(CA.H_FIRST))
        self.assertTrue(got["A02"].startswith(CA.H_NEXT))
        self.assertIn(LOCK + "\nSCENE: room 0.\n" + NEG, got["A01"])
        self.assertLess(len(path.read_text(encoding="utf-8").split("TOK =")[0]), len(MD))   # lời nhắc lặp được nén

    def test_existing_png_skipped_never_overwritten(self):
        (self.ep / "art" / "v01").mkdir()
        (self.ep / "art" / "v01" / "A02.png").write_bytes(b"x")
        path, todo, skipped = CA.build(self.ep, ["A01", "A02", "A03"])
        self.assertEqual((todo, skipped), (["A01", "A03"], ["A02"]))

    def test_unknown_scene_rejected(self):
        with self.assertRaises(SystemExit):
            CA.build(self.ep, ["A09"])


if __name__ == "__main__":
    unittest.main()


class SafeZoomTests(unittest.TestCase):
    """scene_kit.safe_z: zoom không đẩy mặt vào lề cắt 108/972, không kéo đáy nhân vật xuống dải phụ đề (EP21)."""

    def setUp(self):
        import scene_kit as K
        self.K = K

    def test_face_near_edge_limits_zoom(self):
        ann = {'face_x': [150, 960], 'char_bottom_y': 1200}
        z = self.K.safe_z(ann, 1.2)
        P = self.K.P_of(540, 960, z)
        self.assertLessEqual(P(960, 0)[0], 972)
        self.assertLess(z, 1.05)

    def test_bottom_limits_zoom_only_with_subtitles(self):
        ann = {'face_x': [400, 680], 'char_bottom_y': 1440}
        z = self.K.safe_z(ann, 1.2)
        self.assertLess(z, 1.2)
        self.assertLessEqual(self.K.P_of(540, 960, z)(0, 1440)[1], 1460)
        self.assertEqual(self.K.safe_z(ann, 1.2, subs=False), 1.2)
        self.assertEqual(self.K.safe_z(dict(ann, subtitles=False), 1.2), 1.2)

    def test_centered_face_keeps_zoom(self):
        self.assertEqual(self.K.safe_z({'face_x': [450, 630], 'char_bottom_y': 1000}, 1.15), 1.15)


class MusicReuseTests(unittest.TestCase):
    """qa_checks.music_reuse: chặn tập mới dùng lại nhạc nền của tập khác (Owner 13/11/2026)."""

    def setUp(self):
        import qa_checks as QA
        self.QA = QA
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def ep(self, name, sha=None, music_file=None):
        d = self.root / name
        (d / "audio" / "music").mkdir(parents=True)
        ev = [{"type": "music", "title": "T", "sha256": sha}] if sha else []
        (d / "audio" / "audio_events.json").write_text(json.dumps(ev), encoding="utf-8")
        if music_file:
            (d / "audio" / "music" / music_file[0]).write_bytes(music_file[1])
        return d

    def test_reuse_detected_via_events_and_files(self):
        import hashlib
        data = b"abc-music"
        sha = hashlib.sha256(data).hexdigest()
        self.ep("ep01_cu", music_file=("old.mp3", data))
        self.ep("ep02_cu", sha=sha)
        new = self.ep("ep03_moi", sha=sha)
        hits = self.QA.music_reuse(new)
        self.assertEqual(hits[0]["episodes"], ["ep01_cu", "ep02_cu"])

    def test_unique_music_passes_and_seg_ignored(self):
        self.ep("ep01_cu", music_file=("cute_seg0.wav", b"zzz"))
        import hashlib
        new = self.ep("ep02_moi", sha=hashlib.sha256(b"zzz").hexdigest())
        self.assertEqual(self.QA.music_reuse(new), [])

    def test_music_library_groups_by_sha(self):
        """Owner 19/11/2026: dùng lại nhạc có sẵn — kho nhạc gom theo SHA kèm các tập đã dùng."""
        self.ep("ep01_a", music_file=("song.mp3", b"same"))
        self.ep("ep02_b", music_file=("song_copy.mp3", b"same"))
        self.ep("ep03_c", music_file=("other.mp3", b"diff"))
        lib = {tuple(e["episodes"]) for e in self.QA.music_library(self.root)}
        self.assertEqual(lib, {("ep01_a", "ep02_b"), ("ep03_c",)})
