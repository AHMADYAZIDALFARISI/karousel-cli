"""Unit tests for karousel.parser."""

import unittest

from karousel.parser import parse_markdown


class TestParser(unittest.TestCase):
    def test_cover(self):
        slides = parse_markdown("# Belajar Python\nDasar-dasar untuk pemula")
        self.assertEqual(len(slides), 1)
        self.assertEqual(slides[0].type, "cover")
        self.assertEqual(slides[0].title, "Belajar Python")
        self.assertEqual(slides[0].extra, "Dasar-dasar untuk pemula")

    def test_list(self):
        slides = parse_markdown("## 3 Tips\n- Tidur cukup\n- Ulang materi\n- Latihan soal")
        self.assertEqual(slides[0].type, "list")
        self.assertEqual(slides[0].title, "3 Tips")
        self.assertEqual(slides[0].body,
                         ["Tidur cukup", "Ulang materi", "Latihan soal"])

    def test_quote(self):
        slides = parse_markdown('> "Konsisten mengalahkan motivasi."\n> — Penulis')
        self.assertEqual(slides[0].type, "quote")
        self.assertIn("Konsisten mengalahkan motivasi.", " ".join(slides[0].body))
        self.assertEqual(slides[0].extra, "Penulis")
        self.assertNotIn("Penulis", " ".join(slides[0].body))

    def test_separator_inside_fence_does_not_split(self):
        slides = parse_markdown("# A\n```\n---\n```\n\n---\n# B")
        self.assertEqual([s.title for s in slides], ["A", "B"])

    def test_closing(self):
        slides = parse_markdown("# Simpan untuk nanti\n@belajarbareng")
        self.assertEqual(slides[0].type, "closing")
        self.assertEqual(slides[0].extra, "@belajarbareng")

    def test_text_slide(self):
        slides = parse_markdown("Catatan penting\nIni paragraf isi.")
        self.assertEqual(slides[0].type, "text")
        self.assertEqual(slides[0].title, "Catatan penting")

    def test_separator_and_empty_chunks(self):
        slides = parse_markdown("# A\n\n---\n\n---\n# B")
        self.assertEqual([s.title for s in slides], ["A", "B"])

    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            parse_markdown("")
        with self.assertRaises(ValueError):
            parse_markdown("---\n---\n")


if __name__ == "__main__":
    unittest.main()
