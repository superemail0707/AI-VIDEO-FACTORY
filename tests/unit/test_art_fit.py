import sys
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "output" / "_engine"))
import art_fit as AF  # noqa: E402


class ArtFitTest(unittest.TestCase):
    def test_map_xy_pulls_edges_to_center(self):
        x, y = AF.map_xy(40, 1600, 0.85)
        self.assertGreaterEqual(x, 108)
        self.assertLessEqual(y, 1460)

    def test_fit_size_and_paper_fill(self):
        im = Image.new("RGB", (1024, 1820), (255, 255, 255))
        out = AF.fit(im, 0.85)
        self.assertEqual(out.size, (1080, 1920))
        self.assertEqual(out.getpixel((5, 1900)), (255, 255, 255))

    def test_scale_one_is_plain_fit(self):
        im = Image.new("RGB", (1080, 1920), (10, 20, 30))
        self.assertEqual(AF.fit(im, 1.0).getpixel((0, 0)), (10, 20, 30))


if __name__ == "__main__":
    unittest.main()
