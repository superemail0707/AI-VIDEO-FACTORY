import sys
import unittest
import importlib.util
import tempfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "output" / "_engine"))
import scene_kit as K  # noqa: E402


class SubscribeOutroTest(unittest.TestCase):
    def test_new_episode_defaults_to_subscribe_outro(self):
        import nmt_engine as N
        with tempfile.TemporaryDirectory() as tmp:
            previous = N.OUTPUT
            N.OUTPUT = tmp
            try:
                N.new('Outro default')
            finally:
                N.OUTPUT = previous
            episode_file = next(Path(tmp).glob('ep*/render/ep*.py'))
            spec = importlib.util.spec_from_file_location('outro_fixture', episode_file)
            episode = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(episode)
            sid, duration, title, transition, _ = episode.SCENES[-1]
            self.assertEqual((duration, title, transition), (7.8, 'Outro', 'cut'))
            self.assertIn(sid, episode.FUNCS)
            self.assertEqual([e for e in episode.SFX if e[0] == sid], K.subscribe_sfx(sid, gain=K.OUTRO_SFX_GAIN))  # quy trình v2: outro 50 %
            self.assertEqual(episode.META.get('process'), 'nmt_v2')
            Path(episode.ART_DIR).mkdir(parents=True)
            Image.new('RGB', (1080, 1920), (40, 60, 90)).save(Path(episode.ART_DIR) / 'A01.png')
            mid = episode.FUNCS[sid](2.2).getpixel((K.SUB_PILL_X + 120, K.SUB_CY - 50))
            end = episode.FUNCS[sid](K.SUB_DUR - 0.01).getpixel((K.SUB_PILL_X + 120, K.SUB_CY - 50))
            self.assertGreater(sum(mid[:3]), 700)
            self.assertLess(sum(end[:3]), 400)

    def setUp(self):
        self.bg = Image.new("RGBA", (1080, 1920), (40, 60, 90, 255))

    def test_frames_and_safe_zone(self):
        for t in (0.0, 1.0, 3.05, 4.45, 5.6, 7.3, K.SUB_DUR - 0.01):
            f = K.subscribe_outro(t, self.bg)
            self.assertEqual(f.size, (1080, 1920))
        self.assertGreaterEqual(K.SUB_AX - K.SUB_R, 108)
        self.assertLessEqual(K.SUB_X1, 972)
        self.assertLess(K.SUB_CY + 70, 1480)          # không chạm dải phụ đề

    def test_every_frame_renders(self):
        # bài học EP23: thanh rất ngắn khi mở/thu làm PIL lỗi x1 < x0 → render cảnh hỏng
        for i in range(0, int(K.SUB_DUR * 60), 3):
            K.subscribe_outro(i / 60.0, self.bg)

    def test_bar_visible_mid_and_gone_at_end(self):
        mid = K.subscribe_outro(2.2, self.bg).getpixel((K.SUB_PILL_X + 120, K.SUB_CY - 50))
        end = K.subscribe_outro(K.SUB_DUR - 0.01, self.bg).getpixel((K.SUB_PILL_X + 120, K.SUB_CY - 50))
        self.assertGreater(sum(mid[:3]), 700)          # thanh trắng
        self.assertLess(sum(end[:3]), 400)             # đã thu hết

    def test_sfx_times_inside_scene(self):
        for sid, t0, kind, d, g in K.subscribe_sfx("F99"):
            self.assertLess(t0 + d, K.SUB_DUR + 0.01)

    def test_no_appear_vanish_sfx_by_default(self):
        """Owner 20/11/2026 (EP32): chỉ còn tiếng ở 3 nút; không tiếng lúc outro xuất hiện/biến mất."""
        T = K.SUB_T
        sfx = K.subscribe_sfx("F99")
        self.assertEqual(sum(1 for e in sfx if e[2] == "click"), 3)
        self.assertNotIn("whoosh", [e[2] for e in sfx])
        self.assertNotIn("huff", [e[2] for e in sfx])
        self.assertGreaterEqual(min(e[1] for e in sfx), T['like'] - 1e-6)
        self.assertLessEqual(max(e[1] for e in sfx), T['bell'] + 0.05)
        self.assertGreater(len(K.subscribe_sfx("F99", appear_vanish=True)), len(sfx))   # tái lập tập cũ


if __name__ == "__main__":
    unittest.main()
