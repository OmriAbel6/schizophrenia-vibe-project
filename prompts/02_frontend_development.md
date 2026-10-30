# 02 · Frontend development – `web/index.html`, `web/style.css`, `web/app.js`

**Date:** 2026-10-30
**Source prompt:** Deliverables 1 & 2 of the founding prompt (see `01_project_scaffolding.md`).
Below are the requirement fragments that drove each decision, followed by the assistant's work log and the
verification loop.

## Requirement → implementation map

| Requirement (from prompt) | Implementation |
|---|---|
| Exactly 20 structured, interactive slides, SPA, vanilla JS | 20 `<section class="slide">` elements, one `app.js` IIFE, no frameworks |
| `<html lang="he" dir="rtl">`, global `direction: rtl; text-align: right; unicode-bidi: isolate;` | Set on `<html>` and on `html, body` in `style.css` |
| `<bdi>` / `unicode-bidi: isolate` for Latin terms and code | Every Latin term wrapped in `<bdi>`; `pre.code`, `.refs` are `dir="ltr"` blocks |
| Dark clinical aesthetic `#0f172a`, accents `#38bdf8` / `#818cf8`, Heebo | CSS custom properties, Google Fonts Heebo + JetBrains Mono |
| Arrow keys respecting RTL, progress bar, counter, fullscreen | `ArrowLeft` = forward, `ArrowRight` = back, Home/End, F, `#N` hash routing, swipe |
| Slide 8: Three.js scene, morphing geometry, camera drift, controls | Simplex-noise displaced icosahedron, wire shell, 30 floating geometries, 1 800 particles, FOV/roll oscillation; intensity slider, drift, wireframe, pause, reset |
| Auditory hallucination | Web Audio layer: detuned sawtooth drone, LFO-swept brown-noise bed, randomly panned band-passed whisper bursts (user-gesture gated) |
| Fallback if WebGL/CDN unavailable | 2D canvas particle field with the same control API |
| Slides 16–18 consume Python metrics | `fetch('metrics.json')` → fallback `window.SCHIZO_METRICS` from `metrics.js`; SVG grouped columns, line chart with crosshair tooltip and relapse markers, assessment cards |

## Assistant work log

1. **Palette validation** – ran the dataviz validator for `#3987e5,#d95926,#199e70` in dark mode against
   `#1e293b` and `#0f172a`: all checks PASS (worst adjacent CVD ΔE 9.4, normal-vision ΔE 26.5, contrast ≥ 3:1).
2. **Wrote `index.html`** – 636 lines; Hebrew academic copy for all 20 slides with citations inline.
3. **Wrote `style.css`** – 394 lines; theme tokens, slide transitions, card/criteria/timeline/table layouts,
   chart chrome, responsive breakpoint at 1000 px, reduced-motion support.
4. **Wrote `app.js`** – 784 lines; navigation, simplex noise, WebGL scene, 2D fallback, audio layer, SVG
   charts, table views, tooltip. `node --check` passed.
5. **Verification round 1** – served `web/` with `python3 -m http.server` and screenshotted slides
   1, 3, 5, 8, 12, 13, 16, 17, 18, 20 with headless Chrome at 1440×900. All layouts rendered; RTL
   correct; Hebrew typography legible.
6. **Verification round 2 (WebGL)** – created a temporary `_test.html` that auto-navigates to slide 8 and
   clicks "הפעלת הסימולציה", rendered with `--use-angle=swiftshader`. The morphing body, shell, floating
   torus knots/cubes and particles rendered. Temporary file deleted afterwards.
7. **Fix** – bar chart direct labels changed from "first series + all of the general group" to "tallest bar
   per group only" (selective labelling rule; tooltip and table carry the rest).
8. **Verification round 3** – re-screenshotted slides 16–18 after the Python re-tune (log 03): relapse
   markers visible, sustained-remission badge on the integrated-care card.
9. **File:// check** – opened `index.html` from disk in headless Chrome; the meta line on slide 16 reports
   `metrics.js (מוטמע)`, confirming the no-server fallback.

## Follow-up prompt

```
open the presention
```

Assistant ran `open web/index.html` (macOS default browser).
