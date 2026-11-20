"""art_measure: tấm QA đo tranh độ phân giải thấp (Owner 19/11/2026)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "output" / "_engine"))


class ArtMeasureTests(unittest.TestCase):
    def test_sheet_and_write_template(self):
        import art_measure as M
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            art = Path(d) / "art" / "v01"
            art.mkdir(parents=True)
            for n in ("A01", "A02"):
                Image.new("RGB", (941, 1672), (200, 180, 160)).save(art / ("%s.png" % n))
            (art / "safe_annotations.json").write_text(json.dumps({"A01": {"char_bottom_y": 1300, "head_top_y": 300, "face_x": [200, 800]}}))
            M.main([d, "--write"])
            ann = json.loads((art / "safe_annotations.json").read_text())
            self.assertEqual(ann["A01"]["char_bottom_y"], 1300)
            self.assertEqual(ann["A02"], {"subtitles": True})
            self.assertTrue((art / "_qa" / "measure_sheet.jpg").exists())


if __name__ == "__main__":
    unittest.main()
