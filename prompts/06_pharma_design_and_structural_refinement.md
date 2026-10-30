# 06 · Executive pharma design system, interactive flowchart, PDF references and slide refinements

**Date:** 2026-10-30

## Prompt (verbatim)

```
# System Task: Executive Pharma/Medical Design System Overhaul, Interactive Flowchart, PDF References Generator & Slide Refinements

We are executing a high-precision design and structural iteration on our Schizophrenia capstone
presentation. The goal is to elevate the visual identity to the level of an executive pharmaceutical/biotech
launch presentation (clean, bright, medical-grade luxury, composed by senior graphic designers).

Implement every requirement below systematically, save this prompt in
`/prompts/06_pharma_design_and_structural_refinement.md`, update the Change Log in `README.md` before every
commit, and push incremental commits to GitHub (`https://github.com/OmriAbel6/schizophrenia-vibe-project.git`).

---

## 1. Executive Medical & Biotech Color Palette & Design System (`web/style.css`)
- **Replace the cream palette** with a crisp, bright, high-end Pharmaceutical / Clinical Design System:
  - **Primary Canvas Background**: Clinical Pure Alabaster / Ice White (`#F8FAFC` to `#FFFFFF` subtle
    radial/linear gradient) with crisp, airy breathing room.
  - **Surface / Card Containers**: Pure Translucent White (`rgba(255, 255, 255, 0.92)`) with ultra-refined
    hairline borders (`1px solid #E2E8F0`) and multi-layered ambient shadows
    (`0 10px 30px -10px rgba(15, 23, 42, 0.06)`).
  - **Primary Medical Accent**: Deep Biotech Navy (`#0F172A`) for authoritative headings and Clinical
    Cobalt / Cerulean (`#0284C7` & `#0EA5E9`) for primary interactive accents.
  - **Secondary Pharma Accents**: Surgical Teal / Cyan (`#0D9488`) for biological mechanisms, Soft Emerald
    (`#10B981`) for positive symptom/recovery indicators, and Clinical Coral/Rose (`#E11D48`) for
    negative/risk indicators.
  - **Typography & Hierarchy**: Crisp, agency-grade Hebrew typography (`Rubik` for bold geometric titles,
    `Assistant` for clean clinical body copy), balanced contrast (`#0F172A` headings, `#334155` body,
    `#64748B` captions), and strict zero-overflow slide fitting (`100vh` without vertical scrolling).

---

## 2. Specific Slide Modifications (`web/index.html`, `web/style.css`, `web/app.js`)

### A. Slide 1 (Title Slide Overhaul):
- **Remove**: Completely remove the words `"פרויקט גמר"` (or `"פרוייקט גמר"`).
- **Main Title**: Set the primary headline to:
  `סכיזופרניה: צלילה למוחו של חולה סכיזופרניה`
- **Academic & Course Metadata Badges**: Display prominently in a sleek, executive header/metadata bar:
  - קורס: **VIBE CODING וסוכני AI**
  - מוסד אקדמי: **אוניברסיטת חיפה – חטיבת AI**
- **Presenters & Lecturer**: Keep **עומרי אבל**, **אלה אדרי**, and **ד״ר יורם ראובן סגל** styled in a clean
  executive layout.

### B. Slide 5 (Horizontal Interactive Flowchart Below Text):
- **Layout Restructure**: Move the explanatory chain/process so it sits **horizontally balanced directly
  BELOW the main text block**, rather than beside it in a cramped side-by-side column.
- **Interactive Horizontal Flowchart**:
  - Build a wide, horizontal RTL process flow (`display: flex; flex-direction: row; align-items: stretch;
    justify-content: space-between;`) with connected directional arrows/nodes flowing right-to-left.
  - Make each node interactive: hovering or clicking a step in the biological/clinical chain highlights the
    node, animates the connecting line, and reveals a crisp, concise clinical insight badge.

### C. Slide 13 (Standardized Font Scale, Concise Copy & Zero Scrolling):
- **Fix Oversized Typography**: Scale down the exaggerated font size from the previous iteration to a
  balanced, standard presentation scale (`1.05rem–1.15rem` body, `1.35rem` card titles) so the entire slide
  fits comfortably within the viewport **with zero vertical scrolling**.
- **Summarize & Declutter Text**: Condense and tighten the Hebrew clinical text on Slide 13 into sharp,
  scannable bullet points and concise executive takeaways so the slide looks airy, structured, and
  effortless on the eyes.

### D. Slide 20 (Summary, Q&A, Thank You & Downloadable References PDF):
- **Remove Raw Bibliography List**: Remove the dense wall of raw academic citations from Slide 20.
- **Generate Official References PDF (`web/references.pdf`)**:
  - Write a clean helper script in `python/generate_references_pdf.py` (or integrate into `python/main.py`
    using pure Python standard library / minimal PDF structure so no external heavy dependencies break)
    that generates a valid, nicely formatted PDF file at `web/references.pdf` containing all the academic
    references cited in the presentation (DSM-5-TR, Kapur 2003, Howes & Kapur 2009, Stahl's Essential
    Psychopharmacology, Leucht et al., Andreasen et al.).
  - Place a sleek, high-visibility medical-styled button/link on Slide 20: **"לצפייה והורדת רשימת המקורות
    המלאה (PDF)"** pointing to `references.pdf` (`target="_blank"`).
- **Executive Summary, Q&A & Closing**:
  - Include a concise, impactful 3-point **סיכום קצר** synthesizing the presentation's core message
    (neurobiology, subjective patient experience, and targeted treatment).
  - Keep the dedicated **שאלות ודיון (Q&A)** prompt section.
  - Add a prominent, warm closing headline: **"תודה על ההקשבה!"** alongside the presenters' names.

---

## 3. Prompt Logging & Incremental GitHub Workflow
Follow the mandatory course Git workflow—do NOT combine everything into one commit:

1. **Save Prompt Log**:
   - Save this full prompt and execution summary into `prompts/06_pharma_design_and_structural_refinement.md`.

2. **Commit & Push Stage 1 (Executive Pharma Design System & Slide 1 / Slide 13 Refinements)**:
   - Update the Change Log table in `README.md` (Date: `2026-10-30`, Author: `עומרי אבל & אלה אדרי`,
     Description: `"שדרוג לעיצוב רפואי/פארמה יוקרתי ובהיר, עדכון שקופית פתיחה (אוניברסיטת חיפה חטיבת AI
     וקורס VIBE CODING וסוכני AI), ואיזון גודל הטקסט ותמצות שקופית 13"`).
   - Run:
     git add web/style.css web/index.html README.md prompts/
     git commit -m "style(web): apply executive pharma design system and refine slides 1 and 13"
     git push origin main

3. **Commit & Push Stage 2 (Slide 5 Horizontal Interactive Flowchart & Slide 20 PDF References)**:
   - Run the Python script to generate `web/references.pdf`.
   - Update the Change Log table in `README.md` with a new row: `"בניית תרשים זרימה אופקי ואינטראקטיבי
     בשקופית 5, יצירת קובץ PDF למקורות האקדמיים ועדכון שקופית הסיום (סיכום, שאלות ותודה על ההקשבה)"`.
   - Run:
     git add web/ python/ README.md
     git commit -m "feat(web): add horizontal interactive flowchart on slide 5 and PDF bibliography on slide 20"
     git push origin main

4. **Verification**:
   - Run `git log -2 --stat` to verify both commits are pushed to `origin/main` and open `web/index.html` in
     the browser to inspect Slides 1, 5, 13, and 20.
```

## Execution summary

### Stage 1 – design system, slide 1, slide 13

- Palette check before writing: emerald `#10B981` measures 2.42:1 on `#F8FAFC`, below the 3:1 floor for
  strokes and text, so it is used for **fills and badges** while `#059669` (same hue, one step darker)
  carries chart strokes and text; `#059669 / #0284C7 / #E11D48` pass every validator check on the alabaster
  surface (worst adjacent CVD ΔE 16.1, normal-vision 16.9, contrast ≥ 3:1).
- `:root` tokens rewritten: canvas `#F8FAFC → #FFFFFF` linear gradient with cobalt/teal radial washes,
  surfaces `rgba(255,255,255,0.92)` + `1px #E2E8F0` + layered ambient shadow, navy headings, `#334155`
  body, `#64748B` captions, cobalt/cerulean interactive accents, teal for mechanism chips and the H2 rule.
- Zero-overflow: base font scale reduced (`clamp(15px, 0.95vw + 8px, 19px)`), slide padding tightened,
  `.slide { overflow: hidden }`; every slide screenshotted at 1440×900 and adjusted until it fits.
- Slide 1: "פרויקט גמר" removed; new headline "סכיזופרניה: צלילה למוחו של חולה סכיזופרניה"; metadata bar
  with course (VIBE CODING וסוכני AI) and institution (אוניברסיטת חיפה – חטיבת AI) badges; presenters and
  lecturer in executive cards.
- Slide 13: the oversized table replaced by two concise generation cards (title 1.35rem, body
  1.05–1.15rem, three bullets each) and a row of three executive takeaways (CATIE, LAI, treatment duration).

### Stage 2 – slide 5 flowchart, references PDF, slide 20

- **Slide 5**: the four explanatory bullets now sit in a two-column text block; below it an `<ol
  class="flowchart">` lays the four nodes out with `display: flex; flex-direction: row; align-items:
  stretch; justify-content: space-between` (first node at the right, flow right-to-left). Connectors are
  CSS pseudo-elements (track + arrow head); each node holds a `.flow-line` span that grows to full width
  when the node is hovered, focused or clicked, while the step badge switches to the cobalt→teal gradient
  and the hidden `.flow-node__insight` badge expands (max-height/opacity transition). Clicking keeps the
  node active and lights every earlier connector (`is-lit`); keyboard users can tab to nodes and press
  Enter/Space.
- **`python/generate_references_pdf.py`**: a standard-library PDF 1.4 writer (catalog, page tree, pages,
  Helvetica / Helvetica-Bold with WinAnsi encoding, content streams, xref table and trailer) with real
  Helvetica AFM widths for word wrapping. It renders 24 references in five sections (diagnosis,
  neurobiology, cognition, pharmacology/measurement, digital health), with a title block, section rules
  and page footers. Output: `web/references.pdf`, two pages. Headings are in English because the base-14
  fonts carry no Hebrew glyphs; all citations are Latin-script anyway.
- **Slide 20**: the raw bibliography was removed. The slide now has a three-point "סיכום קצר"
  (neurobiology, subjective experience, targeted treatment), a cobalt PDF button
  ("לצפייה והורדת רשימת המקורות המלאה (PDF)", `target="_blank"`), the "שאלות ודיון (Q&A)" card and a
  gradient "תודה על ההקשבה!" panel with the presenters' names, course, institution and lecturer.
- `app.js`: chart colour constants moved to the new system (emerald `#059669` strokes, cobalt `#0284C7`,
  rose `#E11D48`, teal for functioning); the flowchart interaction was added as `initFlowchart()`.
- Verified with headless-Chrome screenshots of slides 5 (node 3 clicked), 17 and 20, and a Quick Look
  render of `references.pdf`.
