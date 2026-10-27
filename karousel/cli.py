"""Command line interface for karousel-cli."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .parser import parse_file
from .render import THEMES, render_all


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="karousel",
        description="Turn a Markdown file into 1080x1350 Instagram "
                    "carousel PNGs, rendered offline with Pillow.")
    p.add_argument("input", help="Markdown file with slides separated by ---")
    p.add_argument("-o", "--output", default="./out",
                   help="output directory (default: ./out)")
    p.add_argument("--theme", choices=sorted(THEMES), default="dark",
                   help="color theme (default: dark)")
    p.add_argument("--font-dir",
                   help="directory with Poppins-Regular.ttf / Poppins-Bold.ttf "
                        "(also read from KAROUSEL_FONT_DIR; falls back to "
                        "system DejaVu)")
    p.add_argument("--start", type=int, default=1,
                   help="first displayed slide number (default: 1)")
    p.add_argument("--version", action="version",
                   version=f"karousel {__version__}")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        slides = parse_file(args.input)
    except FileNotFoundError:
        print(f"karousel: file not found: {args.input}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"karousel: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"karousel: cannot read {args.input}: {e}", file=sys.stderr)
        return 2
    try:
        paths = render_all(slides, args.output, args.theme,
                           args.font_dir, start=args.start)
    except Exception as e:  # noqa: BLE001 - CLI must not crash with traceback
        print(f"karousel: render failed: {e}", file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    print(f"karousel: {len(paths)} slides -> {args.output} "
          f"(theme={args.theme})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
