# Contributing to karousel-cli

## Quick start

```bash
pip install Pillow
python -m unittest discover -s tests -v
```

## Rules

- Keep the runtime dependency list at one item (Pillow). New dependencies
  need a strong reason.
- Every new slide type or parser rule needs a unit test.
- Every rendering change needs a visual check: render `examples/sample.md`
  and look at the PNGs before submitting.
- No network calls in the render path. No secrets anywhere (see SECURITY.md).
- Write user-facing docs in the same PR as the feature.

## Reporting bugs

Include: input Markdown, command used, theme, font setup, and the broken
PNG (or a description of what looks wrong). A minimal failing case gets
fixed fastest.
