"""Bundle the presentation into ONE self-contained HTML file.

Lecture 2 asks for the deck "as a single HTML file".  Development keeps the
sources split (``index.html``, ``style.css``, ``app.js``, ``dialogue.js``) for
readability; this script inlines them into ``web/schizophrenia-deck.html``.
Only Google Fonts and the Three.js CDN remain external.

Usage::

    python3 build_single_file.py              # -> ../web/schizophrenia-deck.html
    python3 build_single_file.py out.html
"""

from __future__ import annotations

import pathlib
import re
import sys
from typing import List

HERE = pathlib.Path(__file__).resolve().parent
WEB = HERE.parent / "web"
DEFAULT_OUTPUT = WEB / "schizophrenia-deck.html"


def inline(html: str) -> str:
    css = (WEB / "style.css").read_text(encoding="utf-8")
    html = html.replace(
        '<link rel="stylesheet" href="style.css">',
        "<style>\n" + css + "\n</style>",
    )
    for name in ("dialogue.js", "app.js"):
        script = (WEB / name).read_text(encoding="utf-8")
        if "</script" in script:
            raise ValueError(f"{name} contains '</script', cannot be inlined safely")
        html = html.replace(
            f'<script src="{name}"></script>',
            f"<script>\n/* ---- {name} ---- */\n{script}\n</script>",
        )
    leftovers: List[str] = re.findall(r'(?:src|href)="(?!https?:|#|references\.pdf)[^"]+"', html)
    if leftovers:
        raise ValueError(f"unresolved local references: {leftovers}")
    return html


def main(argv: List[str]) -> int:
    output = pathlib.Path(argv[0]) if argv else DEFAULT_OUTPUT
    html = (WEB / "index.html").read_text(encoding="utf-8")
    bundled = inline(html)
    output.write_text(bundled, encoding="utf-8")
    size_kb = output.stat().st_size / 1024
    print(f"wrote {output} ({size_kb:.0f} KB, single self-contained HTML file)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
