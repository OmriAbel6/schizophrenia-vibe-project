"""Generate ``web/references.pdf`` – the presentation's bibliography.

The writer below emits a minimal but fully valid PDF 1.4 document using only
the standard library: a catalog, a page tree, one or more pages, two base-14
fonts (Helvetica / Helvetica-Bold with WinAnsi encoding) and per-page content
streams.  Text is word-wrapped with real Helvetica glyph widths so the layout
is clean without any third-party dependency.

Usage::

    python3 generate_references_pdf.py            # -> ../web/references.pdf
    python3 generate_references_pdf.py out.pdf    # custom path
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import sys
from typing import Dict, List, Sequence, Tuple

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE.parent / "web" / "references.pdf"

TITLE = "Schizophrenia: A Dive into the Mind of a Patient"
SUBTITLE = "Academic References Cited in the Presentation"
META_LINES = (
    "Course: VIBE CODING & AI Agents  |  University of Haifa, AI Division",
    "Presenters: Omri Abel & Ella Edri  |  Lecturer: Dr. Yoram Reuven Segal",
)

SECTIONS: Sequence[Tuple[str, Sequence[str]]] = (
    (
        "Diagnosis and clinical description",
        (
            "American Psychiatric Association. (2022). Diagnostic and statistical "
            "manual of mental disorders (5th ed., text rev.). American Psychiatric "
            "Publishing.",
            "Jauhar, S., Johnstone, M., & McKenna, P. J. (2022). Schizophrenia. "
            "The Lancet, 399(10323), 473-486.",
            "McCutcheon, R. A., Reis Marques, T., & Howes, O. D. (2020). "
            "Schizophrenia - An overview. JAMA Psychiatry, 77(2), 201-210.",
            "Jaaskelainen, E., Juola, P., Hirvonen, N., McGrath, J. J., Saha, S., "
            "Isohanni, M., Veijola, J., & Miettunen, J. (2013). A systematic review "
            "and meta-analysis of recovery in schizophrenia. Schizophrenia "
            "Bulletin, 39(6), 1296-1306.",
            "Hor, K., & Taylor, M. (2010). Suicide and schizophrenia: A systematic "
            "review of rates and risk factors. Journal of Psychopharmacology, "
            "24(4 Suppl), 81-90.",
        ),
    ),
    (
        "Neurobiology: dopamine, glutamate and the prefrontal cortex",
        (
            "Howes, O. D., & Kapur, S. (2009). The dopamine hypothesis of "
            "schizophrenia: Version III - The final common pathway. Schizophrenia "
            "Bulletin, 35(3), 549-562.",
            "Kapur, S. (2003). Psychosis as a state of aberrant salience: A "
            "framework linking biology, phenomenology, and pharmacology in "
            "schizophrenia. American Journal of Psychiatry, 160(1), 13-23.",
            "Kapur, S., & Seeman, P. (2001). Does fast dissociation from the "
            "dopamine D2 receptor explain the action of atypical antipsychotics? "
            "American Journal of Psychiatry, 158(3), 360-369.",
            "Kapur, S., Zipursky, R., Jones, C., Remington, G., & Houle, S. (2000). "
            "Relationship between dopamine D2 occupancy, clinical response, and "
            "side effects. American Journal of Psychiatry, 157(4), 514-520.",
            "Javitt, D. C., & Zukin, S. R. (1991). Recent advances in the "
            "phencyclidine model of schizophrenia. American Journal of "
            "Psychiatry, 148(10), 1301-1308.",
            "Weinberger, D. R., Berman, K. F., & Zec, R. F. (1986). Physiologic "
            "dysfunction of dorsolateral prefrontal cortex in schizophrenia. "
            "Archives of General Psychiatry, 43(2), 114-124.",
            "Feinberg, I. (1982). Schizophrenia: Caused by a fault in programmed "
            "synaptic elimination during adolescence? Journal of Psychiatric "
            "Research, 17(4), 319-334.",
            "Sekar, A., Bialas, A. R., de Rivera, H., et al. (2016). Schizophrenia "
            "risk from complex variation of complement component 4. Nature, 530, "
            "177-183.",
        ),
    ),
    (
        "Cognition and functional outcome",
        (
            "Green, M. F. (1996). What are the functional consequences of "
            "neurocognitive deficits in schizophrenia? American Journal of "
            "Psychiatry, 153(3), 321-330.",
            "Wykes, T., Huddy, V., Cellard, C., McGurk, S. R., & Czobor, P. (2011). "
            "A meta-analysis of cognitive remediation for schizophrenia. American "
            "Journal of Psychiatry, 168(5), 472-485.",
        ),
    ),
    (
        "Pharmacology, measurement and treatment",
        (
            "Stahl, S. M. (2021). Stahl's essential psychopharmacology: "
            "Neuroscientific basis and practical applications (5th ed.). "
            "Cambridge University Press.",
            "Lieberman, J. A., Stroup, T. S., McEvoy, J. P., et al. (2005). "
            "Effectiveness of antipsychotic drugs in patients with chronic "
            "schizophrenia (CATIE). New England Journal of Medicine, 353(12), "
            "1209-1223.",
            "Huhn, M., Nikolakopoulou, A., Schneider-Thoma, J., et al. (2019). "
            "Comparative efficacy and tolerability of 32 oral antipsychotics for "
            "the acute treatment of adults with multi-episode schizophrenia. The "
            "Lancet, 394(10202), 939-951.",
            "Kay, S. R., Fiszbein, A., & Opler, L. A. (1987). The Positive and "
            "Negative Syndrome Scale (PANSS) for schizophrenia. Schizophrenia "
            "Bulletin, 13(2), 261-276.",
            "Leucht, S., Kane, J. M., Kissling, W., Hamann, J., Etschel, E., & "
            "Engel, R. R. (2005). What does the PANSS mean? Schizophrenia "
            "Research, 79(2-3), 231-238.",
            "Andreasen, N. C., Carpenter, W. T., Kane, J. M., Lasser, R. A., "
            "Marder, S. R., & Weinberger, D. R. (2005). Remission in "
            "schizophrenia: Proposed criteria and rationale for consensus. "
            "American Journal of Psychiatry, 162(3), 441-449.",
        ),
    ),
    (
        "Digital health and technology",
        (
            "Craig, T. K. J., Rus-Calafell, M., Ward, T., et al. (2018). AVATAR "
            "therapy for auditory verbal hallucinations in people with psychosis: "
            "A single-blind, randomised controlled trial. The Lancet Psychiatry, "
            "5(1), 31-40.",
            "Freeman, D., Lambe, S., Kabir, T., et al. (2022). Automated virtual "
            "reality therapy to treat agoraphobic avoidance and distress in "
            "patients with psychosis (gameChange). The Lancet Psychiatry, 9(5), "
            "375-388.",
            "Ben-Zeev, D., Brian, R., Wang, R., et al. (2017). CrossCheck: "
            "Integrating self-report, behavioral sensing, and smartphone use to "
            "identify digital indicators of psychotic relapse. Psychiatric "
            "Rehabilitation Journal, 40(3), 266-275.",
        ),
    ),
)

# --------------------------------------------------------------------------- #
# Helvetica metrics (AFM widths, 1/1000 em) for word wrapping
# --------------------------------------------------------------------------- #

_HELVETICA_WIDTHS: Dict[str, int] = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667,
    "'": 191, "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333,
    ".": 278, "/": 278, "0": 556, "1": 556, "2": 556, "3": 556, "4": 556,
    "5": 556, "6": 556, "7": 556, "8": 556, "9": 556, ":": 278, ";": 278,
    "<": 584, "=": 584, ">": 584, "?": 556, "@": 1015, "A": 667, "B": 667,
    "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722, "I": 278,
    "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944,
    "X": 667, "Y": 667, "Z": 611, "[": 278, "\\": 278, "]": 278, "^": 469,
    "_": 556, "`": 333, "a": 556, "b": 556, "c": 500, "d": 556, "e": 556,
    "f": 278, "g": 556, "h": 556, "i": 222, "j": 222, "k": 500, "l": 222,
    "m": 833, "n": 556, "o": 556, "p": 556, "q": 556, "r": 333, "s": 500,
    "t": 278, "u": 556, "v": 500, "w": 722, "x": 500, "y": 500, "z": 500,
    "{": 334, "|": 260, "}": 334, "~": 584,
}


def text_width(text: str, size: float, bold: bool = False) -> float:
    scale = 1.05 if bold else 1.0
    units = sum(_HELVETICA_WIDTHS.get(ch, 556) for ch in text)
    return units * size * scale / 1000.0


def wrap(
    text: str, size: float, max_width: float, bold: bool = False
) -> List[str]:
    lines: List[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if text_width(candidate, size, bold) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# --------------------------------------------------------------------------- #
# Minimal PDF writer
# --------------------------------------------------------------------------- #

PAGE_W, PAGE_H = 595.28, 841.89  # A4 portrait, points
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 56.0, 64.0, 60.0
NAVY = (0.059, 0.090, 0.165)      # #0F172A
BODY = (0.200, 0.255, 0.333)      # #334155
COBALT = (0.008, 0.518, 0.780)    # #0284C7
SLATE = (0.392, 0.455, 0.545)     # #64748B
RULE = (0.886, 0.910, 0.941)      # #E2E8F0


def pdf_escape(text: str) -> str:
    encoded = text.encode("cp1252", errors="replace").decode("cp1252")
    return (
        encoded.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    )


class Page:
    """Accumulates content-stream operators for one page."""

    def __init__(self) -> None:
        self.ops: List[str] = []
        self.y = PAGE_H - MARGIN_TOP

    def text(
        self,
        x: float,
        y: float,
        text: str,
        size: float,
        font: str,
        rgb: Tuple[float, float, float],
    ) -> None:
        r, g, b = rgb
        self.ops.append(
            f"BT /{font} {size:.1f} Tf {r:.3f} {g:.3f} {b:.3f} rg "
            f"{x:.2f} {y:.2f} Td ({pdf_escape(text)}) Tj ET"
        )

    def rule(
        self,
        x1: float,
        x2: float,
        y: float,
        rgb: Tuple[float, float, float],
        width: float = 0.8,
    ) -> None:
        r, g, b = rgb
        self.ops.append(
            f"{r:.3f} {g:.3f} {b:.3f} RG {width:.2f} w "
            f"{x1:.2f} {y:.2f} m {x2:.2f} {y:.2f} l S"
        )

    def stream(self) -> bytes:
        return "\n".join(self.ops).encode("cp1252", errors="replace")


def build_pages() -> List[Page]:
    pages: List[Page] = [Page()]
    page = pages[0]
    width = PAGE_W - 2 * MARGIN_X

    def ensure(space: float) -> Page:
        nonlocal page
        if page.y - space < MARGIN_BOTTOM:
            page = Page()
            pages.append(page)
        return page

    # Title block
    page.text(MARGIN_X, page.y, TITLE, 20, "F2", NAVY)
    page.y -= 24
    page.text(MARGIN_X, page.y, SUBTITLE, 12.5, "F1", COBALT)
    page.y -= 20
    for line in META_LINES:
        page.text(MARGIN_X, page.y, line, 9.5, "F1", SLATE)
        page.y -= 13
    page.y -= 4
    page.rule(MARGIN_X, PAGE_W - MARGIN_X, page.y, COBALT, 1.4)
    page.y -= 26

    number = 1
    for heading, refs in SECTIONS:
        page = ensure(60)
        page.text(MARGIN_X, page.y, heading, 12.5, "F2", NAVY)
        page.y -= 6
        page.rule(MARGIN_X, PAGE_W - MARGIN_X, page.y, RULE)
        page.y -= 18
        for ref in refs:
            lines = wrap(ref, 10.5, width - 26)
            page = ensure(len(lines) * 14 + 8)
            page.text(MARGIN_X, page.y, f"{number}.", 10.5, "F2", COBALT)
            for i, line in enumerate(lines):
                page.text(MARGIN_X + 26, page.y, line, 10.5, "F1", BODY)
                page.y -= 14
            page.y -= 7
            number += 1
        page.y -= 10

    # Footer on every page
    stamp = _dt.date.today().isoformat()
    for index, p in enumerate(pages, 1):
        p.rule(MARGIN_X, PAGE_W - MARGIN_X, MARGIN_BOTTOM - 16, RULE)
        footer = f"Generated {stamp} by python/generate_references_pdf.py"
        p.text(MARGIN_X, MARGIN_BOTTOM - 30, footer, 8, "F1", SLATE)
        label = f"Page {index} of {len(pages)}"
        x_label = PAGE_W - MARGIN_X - text_width(label, 8)
        p.text(x_label, MARGIN_BOTTOM - 30, label, 8, "F1", SLATE)
    return pages


def write_pdf(pages: Sequence[Page], output: pathlib.Path) -> None:
    objects: List[bytes] = []

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font_regular = add(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        b"/Encoding /WinAnsiEncoding >>"
    )
    font_bold = add(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold "
        b"/Encoding /WinAnsiEncoding >>"
    )
    pages_id = len(objects) + 1 + 2 * len(pages)  # reserved after page/content pairs
    page_ids: List[int] = []
    for page in pages:
        stream = page.stream()
        content_id = add(
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
            + stream + b"\nendstream"
        )
        page_ids.append(
            add(
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] "
                f"/Resources << /Font << /F1 {font_regular} 0 R "
                f"/F2 {font_bold} 0 R >> >> /Contents {content_id} 0 R >>".encode()
            )
        )
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    tree = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"
    assert add(tree.encode()) == pages_id
    catalog_id = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())
    info_id = add(
        f"<< /Title ({pdf_escape(TITLE + ' - References')}) "
        f"/Author (Omri Abel & Ella Edri) /Producer (generate_references_pdf.py) "
        f"/CreationDate (D:{_dt.datetime.now():%Y%m%d%H%M%S}) >>".encode()
    )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: List[int] = []
    for index, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R "
        f"/Info {info_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    ).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(bytes(out))


def main(argv: List[str]) -> int:
    output = pathlib.Path(argv[0]) if argv else DEFAULT_OUTPUT
    pages = build_pages()
    write_pdf(pages, output)
    total = sum(len(refs) for _, refs in SECTIONS)
    print(f"wrote {output} ({len(pages)} page(s), {total} references)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
