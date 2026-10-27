# karousel-cli

Turn a Markdown file into **1080×1350 Instagram carousel PNGs**, rendered
100% offline with Pillow. No browser, no paid API, no account.

```bash
pip install karousel-cli
karousel examples/sample.md -o out/
# out/slide_01.png … out/slide_04.png (1080x1350, RGB)
```

## The problem

Indonesian student creators and small teams make carousel posts by hand in
design tools: slow, repetitive, and hard to version. Existing open-source
carousel generators either need a headless browser (heavy download, slow
startup), live inside an AI-coding-assistant skill, or generate captions and
AI images instead of rendering real slides. `karousel-cli` fills the gap: a
deterministic, scriptable Markdown → PNG pipeline that runs anywhere Python
runs, including CI and low-spec machines.

## Features

- Markdown in, PNG slides out — one command, no GUI.
- Slide types: `cover`, `list`, `quote`, `closing`, `text`.
- Dark and light themes, 80px safe margins, automatic text wrapping and
  font shrinking so long text never overflows.
- Slide numbering (`1 / 4`) and accent bar on every slide.
- Font resolution: `--font-dir` / `KAROUSEL_FONT_DIR` / `./fonts` / system
  DejaVu / Pillow built-in fallback. Poppins (SIL OFL) recommended — fetch
  it free with `scripts/download-fonts.sh`.
- Fully offline rendering. No data leaves your machine.

## Requirements

- Python 3.9+
- Pillow >= 10.0 (`pip install Pillow`)

## Installation

```bash
pip install karousel-cli
# or from source:
pip install .
```

Fonts (one-time, free, SIL OFL):

```bash
bash scripts/download-fonts.sh   # downloads Poppins Regular + Bold into fonts/
# or point at your own fonts:
karousel slides.md -o out/ --font-dir /path/to/fonts
```

Without Poppins, the tool falls back to system DejaVu, then to Pillow's
built-in font. Rendering always succeeds.

## Quick start

Write `slides.md`:

```markdown
# Belajar Python
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
```

Then:

```bash
karousel slides.md -o out/ --theme dark
karousel slides.md -o out/ --theme light --start 5   # numbering starts at 5
```

### Slide rules

Slides are separated by a line containing exactly `---`.

| First line | Slide type |
|---|---|
| `# Title` (+ subtitle lines) | `cover` |
| `## Title` + `- item` lines | `list` |
| `> text` | `quote` (a `— name` line becomes the attribution) |
| `# Title` + `@handle` line | `closing` |
| anything else | `text` (first line = title) |

Empty chunks are skipped. A file with no slides is an error (exit code 2).

### CLI reference

```text
karousel INPUT -o OUTPUT [--theme dark|light] [--font-dir DIR] [--start N]
```

- `INPUT`: Markdown file (UTF-8).
- `-o, --output`: output directory (default `./out`).
- `--theme`: `dark` (default) or `light`.
- `--font-dir`: directory with `Poppins-Regular.ttf` / `Poppins-Bold.ttf`
  (also accepts Google-Fonts-style names like `poppins-v24-latin-700.ttf`).
- `--start`: first displayed slide number (default 1). Filenames follow
  the displayed numbering, so `--start 5` writes `slide_05.png` onward
  and labels slides `5 / 7`, `6 / 7`, …

## Testing

```bash
python -m unittest discover -s tests -v
```

18 tests: parser (all slide types, separators, fenced code blocks, empty input), text wrapping,
themes, end-to-end rendering (dimensions, filenames, file sizes), long-text
shrink, and font-name resolution. CI runs the same suite on every push
(see `.github/workflows/ci.yml`).

## Known limitations

- Text only: no images, emoji rendering depends on the chosen font
  (DejaVu covers most Latin text; color emoji are not supported by Pillow
  text rendering).
- One layout per slide type; no per-slide custom layout in v0.1.
- PNG output only (no PDF/video export).
- Very long slides shrink text down to 30% of base size; beyond that, text
  is still drawn but may look dense — split the slide instead.
- Fenced code blocks (```) do not split slides, but they are not rendered
  specially — fence lines appear as literal text.

## Security and privacy

- Rendering is fully local: no network calls, no telemetry, no data upload.
- The tool reads only the Markdown file you pass and writes only to the
  output directory you choose. It never executes Markdown content.
- No secrets are required or accepted. See `SECURITY.md` for reporting.

## Roadmap

- More slide layouts (comparison, timeline, checklist).
- Theme config file (custom colors + accent).
- Per-slide background colors.
- Optional image strip on cover slides.
- `karousel init` starter template.

## Contributing

See `CONTRIBUTING.md`. Bug reports and small PRs are welcome; please
include a failing test case when reporting a rendering bug.

## License

MIT for code (see `LICENSE`). Poppins font, when downloaded via
`scripts/download-fonts.sh`, is under the SIL Open Font License 1.1 by
Indian Type Foundry — see the license file shipped with the font.

## Attribution

- Built with [Pillow](https://python-pillow.org/).
- Research notes and competitor comparison: `docs/RESEARCH.md`.
- Project 1 of the Ayasi Open Source Intelligence daily factory
  (27 October 2026). Research, novelty, and architecture inputs came from
  WusRouter free-tier models (see `docs/RESEARCH.md` for exactly which
  models were called and what they returned).
