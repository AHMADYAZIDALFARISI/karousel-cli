# Changelog

## 0.1.0 — 2026-10-27

- Initial release.
- Markdown → 1080×1350 PNG carousel rendering with Pillow only.
- Slide types: cover, list, quote, closing, text.
- Dark/light themes, safe margins, text wrap + shrink-to-fit.
- Font resolution: `--font-dir` / `KAROUSEL_FONT_DIR` / `./fonts` /
  system DejaVu / Pillow built-in fallback.
- CLI: `karousel INPUT -o OUTPUT [--theme] [--font-dir] [--start]`.
- 16 unit/integration tests, GitHub Actions CI.
