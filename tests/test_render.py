"""Tests for karousel.render: wrapping, themes, end-to-end rendering."""

import os
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageFont

from karousel.parser import parse_markdown
from karousel.render import CONTENT_W, THEMES, render_all, render_slide, wrap_text

SAMPLE = """# Belajar Python
Dasar-dasar untuk pemula

---
## 3 Tips Belajar
- Tidur cukup
- Ulang materi
- Latihan soal

---
> Konsisten mengalahkan motivasi.

---
# Simpan untuk nanti
@belajarbareng
"""


class TestWrap(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGB", (100, 100))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()

    def test_short_text_single_line(self):
        self.assertEqual(wrap_text(self.draw, self.font, "halo dunia", 1000),
                         ["halo dunia"])

    def test_long_text_wraps_within_width(self):
        font = self.font
        lines = wrap_text(self.draw, font,
                          "ini adalah kalimat yang cukup panjang untuk dibungkus",
                          100)
        self.assertGreater(len(lines), 1)
        for line in lines:
            self.assertLessEqual(self.draw.textlength(line, font=font), 100 + 1)

    def test_empty_text(self):
        self.assertEqual(wrap_text(self.draw, self.font, "", 100), [])


class TestFontGlob(unittest.TestCase):
    def test_google_fonts_style_name_resolves(self):
        import shutil
        from karousel import fonts as fonts_mod
        with tempfile.TemporaryDirectory() as tmp:
            src = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            dst = os.path.join(tmp, "poppins-v24-latin-700.ttf")
            shutil.copy(src, dst)
            found = fonts_mod.font_name_used("bold", tmp)
            self.assertEqual(found, dst)


class TestThemes(unittest.TestCase):
    def test_known_themes(self):
        self.assertIn("dark", THEMES)
        self.assertIn("light", THEMES)
        self.assertNotEqual(THEMES["dark"]["bg"], THEMES["light"]["bg"])


class TestRenderEndToEnd(unittest.TestCase):
    def test_render_sample(self):
        slides = parse_markdown(SAMPLE)
        self.assertEqual(len(slides), 4)
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_all(slides, tmp, "dark")
            self.assertEqual(len(paths), 4)
            for i, path in enumerate(paths, start=1):
                self.assertTrue(os.path.isfile(path))
                self.assertTrue(path.endswith(f"slide_{i:02d}.png"))
                with Image.open(path) as im:
                    self.assertEqual(im.size, (1080, 1350))
                    self.assertEqual(im.mode, "RGB")
                self.assertGreater(os.path.getsize(path), 1000)

    def test_render_light_theme(self):
        slides = parse_markdown("# Judul")
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_all(slides, tmp, "light")
            with Image.open(paths[0]) as im:
                self.assertEqual(im.getpixel((0, 0)), (255, 255, 255))

    def test_render_very_long_text_does_not_crash(self):
        slides = parse_markdown("# Judul\n" + ("kata " * 400))
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_all(slides, tmp, "dark")
            self.assertEqual(len(paths), 1)
            with Image.open(paths[0]) as im:
                self.assertEqual(im.size, (1080, 1350))

    def test_slide_numbering_with_start(self):
        slides = parse_markdown("# A\n\n---\n# B")
        img = render_slide(slides[1], 5, 2, "dark")
        self.assertEqual(img.size, (1080, 1350))

    def test_start_offsets_filenames(self):
        slides = parse_markdown("# A\n\n---\n# B")
        with tempfile.TemporaryDirectory() as tmp:
            paths = render_all(slides, tmp, "dark", start=5)
            self.assertEqual([os.path.basename(p) for p in paths],
                             ["slide_05.png", "slide_06.png"])


if __name__ == "__main__":
    unittest.main()
