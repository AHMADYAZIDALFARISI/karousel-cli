"""Font resolution for karousel-cli.

Resolution order for a requested weight (``regular`` or ``bold``):

1. ``--font-dir`` / ``KAROUSEL_FONT_DIR`` directory (files named
   ``Poppins-Regular.ttf`` / ``Poppins-Bold.ttf`` or any ``*.ttf`` whose
   name contains the weight).
2. ``./fonts`` next to the working directory.
3. System DejaVu (``/usr/share/fonts/truetype/dejavu/``), which ships on
   most Linux systems and on GitHub-hosted CI runners.
4. Pillow's built-in bitmap font (last resort; ugly but never crashes).

No font file is bundled in this repository: Poppins is SIL OFL licensed
and can be fetched with ``scripts/download-fonts.sh`` into ``fonts/``.
"""

from __future__ import annotations

import os
from PIL import ImageFont

_SYSTEM_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/TTF",
    os.path.expanduser("~/.fonts"),
)

_WEIGHT_FILES = {
    "regular": ("Poppins-Regular.ttf", "Poppins-regular.ttf",
                "DejaVuSans.ttf", "NotoSans-Regular.ttf"),
    "bold": ("Poppins-Bold.ttf", "Poppins-bold.ttf",
             "DejaVuSans-Bold.ttf", "NotoSans-Bold.ttf"),
}


def _glob_matches(directory: str, weight: str) -> list[str]:
    """Fallback matches for Google-Fonts-style names, e.g.
    ``poppins-v24-latin-700.ttf`` (bold) or ``poppins-v24-latin-regular.ttf``."""
    import glob
    out = []
    try:
        files = sorted(glob.glob(os.path.join(directory, "*.ttf")))
    except Exception:
        return out
    for path in files:
        low = os.path.basename(path).lower()
        if weight == "bold":
            if "bold" in low or "-700." in low or "-800." in low:
                out.append(path)
        else:
            if "regular" in low and "bold" not in low:
                out.append(path)
    return out


def _candidates(font_dir: str | None, weight: str) -> list[str]:
    dirs: list[str] = []
    if font_dir:
        dirs.append(font_dir)
    env_dir = os.environ.get("KAROUSEL_FONT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append(os.path.join(os.getcwd(), "fonts"))
    dirs.extend(_SYSTEM_DIRS)
    out = []
    for d in dirs:
        for name in _WEIGHT_FILES[weight]:
            out.append(os.path.join(d, name))
        out.extend(_glob_matches(d, weight))
    return out


def load_font(weight: str, size: int, font_dir: str | None = None):
    """Return a Pillow font for *weight* at *size* (never raises)."""
    for path in _candidates(font_dir, weight):
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def font_name_used(weight: str, font_dir: str | None = None) -> str:
    """Path of the font that would be used, or ``"<builtin>"``."""
    for path in _candidates(font_dir, weight):
        if os.path.isfile(path):
            return path
    return "<builtin>"
