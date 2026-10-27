"""Render slides to 1080x1350 PNG images with Pillow only.

No browser, no network, no paid API: everything happens locally.
Text that does not fit is shrunk step by step down to a 30% floor;
content beyond that is drawn dense rather than crashing — split such
slides instead of relying on the floor.
"""

from __future__ import annotations

import os

from PIL import Image, ImageDraw

from .fonts import load_font
from .parser import Slide

WIDTH = 1080
HEIGHT = 1350
MARGIN = 80
NUMBER_SIZE = 36
FOOTER_GAP = 16
CONTENT_W = WIDTH - 2 * MARGIN
# Content box ends above the slide-number footer band, so body text can
# never overlap the "N / total" label.
CONTENT_H = HEIGHT - 2 * MARGIN - NUMBER_SIZE - FOOTER_GAP

THEMES = {
    "dark": {"bg": (17, 17, 17), "fg": (255, 255, 255),
             "muted": (170, 170, 170), "accent": (255, 77, 109)},
    "light": {"bg": (255, 255, 255), "fg": (17, 17, 17),
              "muted": (110, 110, 110), "accent": (255, 77, 109)},
}

TITLE_SIZE = 96
LIST_TITLE_SIZE = 72
BODY_SIZE = 52
QUOTE_SIZE = 64
LINE_GAP = 18


def wrap_text(draw: ImageDraw.ImageDraw, font, text: str,
              max_width: int) -> list[str]:
    """Word-wrap *text* to lines no wider than *max_width* pixels."""
    max_width = max(1, max_width)
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = ""
    for word in words:
        # Split a single overlong word character by character.
        while draw.textlength(word, font=font) > max_width:
            cut = len(word)
            while cut > 1 and draw.textlength(word[:cut], font=font) > max_width:
                cut -= 1
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:cut])
            word = word[cut:]
            if not word:
                break
        if not word:
            continue
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _block_height(draw, lines_with_fonts) -> int:
    total = 0
    for i, (lines, font) in enumerate(lines_with_fonts):
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            total += (bbox[3] - bbox[1]) + LINE_GAP
        if i < len(lines_with_fonts) - 1:
            total += LINE_GAP * 2
    return max(total - LINE_GAP, 0)


def _draw_block(draw, x, y, lines_with_fonts, fill, align="center"):
    """Draw (lines, font) groups; returns the y after the block.

    Callers always pass ``x == MARGIN``; centering is computed against
    the full content column starting there.  ``align`` is ``"center"``,
    ``"left"``, or ``"right"``.
    """
    for gi, (lines, font) in enumerate(lines_with_fonts):
        for line in lines:
            w = draw.textlength(line, font=font)
            if align == "center":
                lx = x + (CONTENT_W - w) / 2
            elif align == "right":
                lx = x + CONTENT_W - w
            else:
                lx = x
            draw.text((lx, y), line, font=font, fill=fill)
            bbox = draw.textbbox((0, 0), line, font=font)
            y += (bbox[3] - bbox[1]) + LINE_GAP
        if gi < len(lines_with_fonts) - 1:
            y += LINE_GAP * 2
    return y - LINE_GAP  # drop the trailing gap so the return matches height


def _fit_and_draw(draw, groups, theme, font_dir, align="center"):
    """Shrink fonts until the block fits CONTENT_H, then draw centered.

    *groups* is a list of (text, weight, base_size) tuples.  Fonts shrink
    from 100% down to a 30% floor in integer steps; content that still
    does not fit at the floor is drawn anyway (dense, but never a crash)
    — split such slides.
    """
    groups = [(t, w, s) for (t, w, s) in groups if t and t.strip()]
    built = []
    for step in range(15):  # 1.00, 0.95, ..., 0.30 — deterministic, no floats
        scale = 1.0 - step * 0.05
        built = []
        for text, weight, size in groups:
            font = load_font(weight, max(10, int(size * scale)), font_dir)
            built.append((wrap_text(draw, font, text, CONTENT_W), font))
        if _block_height(draw, built) <= CONTENT_H:
            break
    total_h = _block_height(draw, built)
    y = MARGIN + max(0, (CONTENT_H - total_h) / 2)
    _draw_block(draw, MARGIN, y, built, theme["fg"], align=align)


def render_slide(slide: Slide, index: int, total: int,
                 theme_name: str = "dark",
                 font_dir: str | None = None) -> Image.Image:
    """Render one slide. *index* is 1-based (display number)."""
    theme = THEMES.get(theme_name, THEMES["dark"])
    img = Image.new("RGB", (WIDTH, HEIGHT), theme["bg"])
    draw = ImageDraw.Draw(img)
    # Accent bar at the top.
    draw.rectangle([MARGIN, 56, MARGIN + 120, 68], fill=theme["accent"])

    if slide.type == "cover":
        groups = [(slide.title, "bold", TITLE_SIZE)]
        if slide.extra:
            groups.append((slide.extra, "regular", BODY_SIZE))
        _fit_and_draw(draw, groups, theme, font_dir)
    elif slide.type == "list":
        title_font = load_font("bold", LIST_TITLE_SIZE, font_dir)
        title_lines = wrap_text(draw, title_font, slide.title, CONTENT_W)
        items = []
        for item in (slide.body or []):
            items.append("•  " + item)
        body_font = load_font("regular", BODY_SIZE, font_dir)
        body_lines = []
        for item in items:
            body_lines.extend(wrap_text(draw, body_font, item, CONTENT_W))
        groups = [(title_lines, title_font), (body_lines, body_font)]
        total_h = _block_height(draw, groups)
        y = MARGIN + max(0, (CONTENT_H - total_h) / 2)
        _draw_block(draw, MARGIN, y, groups, theme["fg"], align="left")
    elif slide.type == "quote":
        groups = [(" ".join(slide.body or []), "bold", QUOTE_SIZE)]
        if slide.extra:
            groups.append(("— " + slide.extra, "regular", BODY_SIZE))
        _fit_and_draw(draw, groups, theme, font_dir)
    elif slide.type == "closing":
        groups = [(slide.title, "bold", TITLE_SIZE)]
        if slide.extra:
            groups.append((slide.extra, "bold", BODY_SIZE))
        _fit_and_draw(draw, groups, theme, font_dir)
    else:  # text
        groups = [(slide.title, "bold", LIST_TITLE_SIZE)]
        for para in (slide.body or []):
            groups.append((para, "regular", BODY_SIZE))
        _fit_and_draw(draw, groups, theme, font_dir)

    # Slide number, bottom-right, muted.
    num_font = load_font("regular", NUMBER_SIZE, font_dir)
    label = f"{index} / {total}"
    w = draw.textlength(label, font=num_font)
    draw.text((WIDTH - MARGIN - w, HEIGHT - MARGIN - NUMBER_SIZE),
              label, font=num_font, fill=theme["muted"])
    return img


def render_all(slides: list[Slide], out_dir: str, theme_name: str = "dark",
               font_dir: str | None = None, start: int = 1) -> list[str]:
    """Render every slide to ``slide_NN.png`` in *out_dir*.

    Filenames and the displayed ``N / total`` label both follow *start*,
    so ``start=5`` with 3 slides writes ``slide_05..07.png`` labelled
    ``5 / 7`` … ``7 / 7``.
    """
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    total = start + len(slides) - 1
    for i, slide in enumerate(slides):
        num = start + i
        img = render_slide(slide, num, total, theme_name, font_dir)
        path = os.path.join(out_dir, f"slide_{num:02d}.png")
        img.save(path)
        paths.append(path)
    return paths
