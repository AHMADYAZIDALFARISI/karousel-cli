"""Parse a Markdown file into a list of carousel slides.

Slide format (v1)
------------------
Slides are separated by a line containing exactly ``---``.  The first
non-empty line of a chunk decides its type:

* ``# Title``            -> ``cover``   (a later ``#`` chunk that contains
  a line starting with ``@`` is a ``closing`` slide instead)
* ``## Title`` + bullets -> ``list``
* ``> text``             -> ``quote``
* anything else          -> ``text``

Empty chunks are skipped.  A document without any slide raises ValueError.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Slide:
    type: str  # cover | list | quote | closing | text
    title: str = ""
    body: list[str] = field(default_factory=list)
    extra: str = ""  # quote attribution, closing handle, cover subtitle


def _is_separator(line: str) -> bool:
    return line.strip() == "---"


def _parse_chunk(chunk: str) -> Slide | None:
    lines = [ln.rstrip() for ln in chunk.strip().splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    if not lines:
        return None

    first = lines[0].strip()

    # Quote: every content line starts with "> ".  A line like
    # "> — Author" (or a bare "— Author" line) becomes the attribution.
    if first.startswith(">"):
        text_lines = []
        attribution = ""
        for ln in lines:
            t = ln.strip()
            if t.startswith(">"):
                t = t[1:].strip()
            if t.startswith("—"):
                attribution = t[1:].strip()
            elif t.startswith("--"):
                attribution = t[2:].strip()
            elif t:
                text_lines.append(t)
        return Slide(type="quote", body=text_lines, extra=attribution)

    # List: "## Title" followed by "- item" / "* item" lines.
    # Non-bullet lines inside a list chunk are treated as items too
    # (lenient parsing; documented behaviour).
    if first.startswith("## "):
        title = first[3:].strip()
        items = []
        for ln in lines[1:]:
            t = ln.strip()
            if t.startswith("- "):
                items.append(t[2:].strip())
            elif t.startswith("* "):
                items.append(t[2:].strip())
            elif t:
                items.append(t)
        return Slide(type="list", title=title, body=items)

    # Cover / closing: "# Title".
    if first.startswith("# "):
        title = first[2:].strip()
        rest = [ln.strip() for ln in lines[1:] if ln.strip()]
        handle = ""
        subtitle_lines = []
        for ln in rest:
            if ln.startswith("@"):
                handle = ln.strip()
            else:
                subtitle_lines.append(ln)
        if handle:
            return Slide(type="closing", title=title, extra=handle)
        return Slide(type="cover", title=title,
                     extra=" ".join(subtitle_lines))

    # Plain text slide: first line is the title, the rest is the body.
    return Slide(type="text", title=first, body=[ln.strip() for ln in lines[1:]])


def parse_markdown(text: str) -> list[Slide]:
    """Split *text* into slides. Raises ValueError when no slide is found."""
    if not text or not text.strip():
        raise ValueError("input is empty: no slides found")
    chunks: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            current.append(line)
            continue
        if _is_separator(line) and not in_fence:
            chunks.append("\n".join(current))
            current = []
        else:
            current.append(line)
    chunks.append("\n".join(current))
    slides = []
    for chunk in chunks:
        slide = _parse_chunk(chunk)
        if slide is not None:
            slides.append(slide)
    if not slides:
        raise ValueError("input contains no slides (only separators/blank lines)")
    return slides


def parse_file(path: str) -> list[Slide]:
    with open(path, "r", encoding="utf-8") as f:
        return parse_markdown(f.read())
