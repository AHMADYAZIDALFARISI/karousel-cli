# Architecture — karousel-cli v0.1.0

```text
slides.md --parse--> [Slide] --render--> slide_01.png … slide_NN.png
              parser.py        render.py (Pillow)
                    \            /
                     fonts.py (resolution chain)
```

## Modules

- `karousel/parser.py` — pure text parsing, no I/O except `parse_file`.
  Separator `---` (ignored inside ``` fences). Slide types: cover, list,
  quote, closing, text. Raises `ValueError` on empty input.
- `karousel/fonts.py` — resolution chain: `--font-dir` →
  `KAROUSEL_FONT_DIR` → `./fonts` → system DejaVu → Pillow built-in.
  Accepts canonical names (`Poppins-Regular.ttf`) and Google-Fonts-style
  names (`poppins-v24-latin-700.ttf`). Never raises.
- `karousel/render.py` — Pillow drawing. Canvas 1080×1350, margin 80px,
  content column 920px, footer band reserved for the slide number so body
  text can never overlap it. Text wraps by measured pixel width; fonts
  shrink in 5% steps from 100% to a 30% floor. No network, no threads.
- `karousel/cli.py` — argparse only; maps errors to exit codes
  (2 = bad input, 1 = render failure, 0 = success).

## Invariants

- Output is always RGB PNG, exactly 1080×1350.
- Filenames and displayed numbers both follow `--start`.
- Rendering never crashes on long text (shrink floor) or missing fonts
  (fallback chain); it fails only on unreadable input or unwritable output.
- No dependency besides Pillow. No config files in v0.1.
