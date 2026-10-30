# 07 · Layout distribution, slide 1 title fix, brain animation bridge (19→20) and medical micro-animations

**Date:** 2026-10-30
**Attachment:** a "Medical Infographic" template image (blue timeline with circular icon nodes, percent rings,
Montserrat typography) was supplied as visual inspiration, together with `Fonts.txt` naming Montserrat.

## Prompt (verbatim)

```
# System Task: Comprehensive Layout Distribution, Slide 1 Title Fix, Animated Brain GIF Surprise (Slides 19–20), Medical Infographics & Micro-Animations

We are executing the final structural and visual polish on our Schizophrenia capstone presentation. You must
implement all requirements below systematically, save this prompt in
`/prompts/07_layout_infographics_and_brain_gif.md`, update the Change Log inside `README.md` before every
commit, and push incremental commits to GitHub (`https://github.com/OmriAbel6/schizophrenia-vibe-project.git`).

---

## 1. Structural & Typography Refinements (`web/index.html`, `web/style.css`)
- **Slide 1 Title Restructure (No Colons)**:
  - Remove any colons from the title. Set it cleanly with a prominent main header and a subtitle:
    - Main Header (Large): **סכיזופרניה**
    - Subtitle (Secondary): **צלילה למוחו של חולה סכיזופרניה**
    - Metadata Badges: קורס **VIBE CODING וסוכני AI** | **אוניברסיטת חיפה – חטיבת AI** | מגישים: **עומרי אבל**
      & **אלה אדרי** | מרצה: **ד״ר יורם ראובן סגל**.
- **Vertical Layout Distribution & Centering**:
  - Audit all 20 slides to ensure content does not cluster exclusively at the top. Vertically distribute,
    space out, and center elements evenly across the viewport (`display: flex; flex-direction: column;
    justify-content: center; align-items: center; min-height: 100vh; padding: 2rem;`) to maintain a
    balanced, breathable executive presentation look.
- **Slides 19–20 Transition & Animated Brain GIF Surprise**:
  - At the end of Slide 19 leading into Slide 20, embed an engaging, high-quality animated GIF or CSS/canvas
    animation of a **pulsing/shaking brain (מוח רועד)** as a fascinating visual surprise/bridge before the
    final summary and Q&A.

---

## 2. Advanced Medical Infographics & Moving Objects (`web/style.css`, `web/app.js`)
- **Pharma-Grade Infographics & Micro-Animations**:
  - Inspired by clean medical design systems (featuring floating biological nodes, subtle pulsing
    heartbeat/waveform lines, rotating D2 receptor interactive rings, and smooth SVG data connectors),
    integrate floating/moving vector objects and interactive infographic cards.
  - Every chart, data pill, and clinical metric container must feature gentle, organic CSS animations
    (floating, pulsing glows, smooth fade-ins on scroll/slide entry) to make the data feel alive, modern,
    and professionally designed by senior medical UX experts.

---

## 3. Prompt History Logging & Incremental GitHub Workflow
Follow the mandatory course Git workflow—do NOT combine everything into one commit:

1. **Save Prompt Log**:
   - Save this full prompt and execution summary into `prompts/07_layout_infographics_and_brain_gif.md`.

2. **Commit & Push Stage 1 (Slide 1 Title Clean-up & Vertical Layout Distribution)**:
   - Update the Change Log table in `README.md` (Date: `2026-10-30`, Author: `עומרי אבל & אלה אדרי`,
     Description: `"סדור כותרת שקופית 1 ללא נקודתיים (סכיזופרניה / צלילה למוחו של חולה סכיזופרניה) ופיזור
     ומרכוז אנכי של המלל בכל השקופיות למילוי אחיד של העמוד"`).
   - Run:
     git add web/index.html web/style.css README.md prompts/
     git commit -m "style(web): clean slide 1 title hierarchy and apply balanced vertical layout distribution"
     git push origin main

3. **Commit & Push Stage 2 (Brain GIF Surprise on Slide 19-20 & Moving Medical Infographics)**:
   - Update the Change Log table in `README.md` with a new row: `"הוספת GIF של מוח רועד כהפתעה ויזואלית בין
     שקופית 19 ל-20, ושילוב אלמנטים אינפוגרפיים ואובייקטים זזים בעיצוב רפואי יוקרתי"`).
   - Run:
     git add web/ README.md
     git commit -m "feat(web): add pulsing brain GIF transition between slides 19-20 and interactive medical infographics"
     git push origin main

4. **Verification**:
   - Run `git log -2 --stat` to verify both incremental commits and pushes succeeded, and open
     `web/index.html` in the browser to inspect the layout, infographics, and brain GIF.
```

## Execution summary

### Stage 1 – slide 1 hierarchy and vertical distribution

- Slide 1: no colons – `h1.title--main` "סכיזופרניה" (gradient navy→cobalt, up to 6.6rem) over the
  `.title-sub` "צלילה למוחו של חולה סכיזופרניה"; metadata badges for course and institution above, and
  stronger badges for "מגישים: עומרי אבל & אלה אדרי" and "מרצה: ד״ר יורם ראובן סגל" below the lead.
- Every other slide's eyebrow + H2 were wrapped in `<header class="slide__head">` (19 slides) so the
  container can space its blocks evenly.
- `.slide` is now `display: flex; flex-direction: column; justify-content: center; align-items: center;
  min-height: 100vh; padding: 2rem …`; `.slide__inner` is a flex column with `justify-content: center`,
  `min-height: calc(100vh − 6.6rem)` and a viewport-relative gap, so content is centred and spread rather
  than clustered at the top. Per-slide "start" anchors from earlier iterations were removed.
- Twelve representative slides were screenshotted at 1440×900: all centred, none overflow.

### Stage 2 – brain bridge and medical micro-animations

- **Brain bridge (19 → 20)**: a full-screen overlay (`#brainBridge`) with a hand-drawn SVG brain
  (gradient hemispheres, white gyri, cerebellum, stem, glow filter) that beats (`brainBeat`, scale) and
  shakes (`brainShake`, translate/rotate), six sparkling synapse dots, a moving ECG trace, drifting nodes,
  the title "מוח רועד", a one-line caption, a progress bar and a skip hint. It is shown by the slide-20
  enter hook only when arriving from slide 19 (the hook now receives the previous slide number), runs for
  4.2 s and closes on click or any key. Slide 19 ends with a pulsing hint line. It is a CSS/SVG animation
  rather than a GIF file, which keeps it crisp at any resolution and respects `prefers-reduced-motion`.
- **Micro-animations** (all inside `@media (prefers-reduced-motion: no-preference)`):
  staggered `fadeUp` on every card, metric, pill, node and panel when its slide becomes active (`--i`
  indices set by `initDecorations()` on grid/flex children); gentle `floatY` on stat tiles, data pills,
  dials, chips and badges (uses the `translate` property so hover `transform` still works); `glowPulse`
  on values and the thank-you title; `barGlow` on gauge/bar fills and primary buttons; rotating dashed
  D2/5-HT2A receptor rings around the dials (`spin` / `spinBack`); SVG series lines draw in on slide entry
  (`pathLength="1"` + `stroke-dashoffset`), including the dashed untreated line which restores its dash
  pattern after drawing; an animated ECG waveform in the suicide-risk card; floating biological nodes
  with dashed halos and faint connectors injected behind slides 1, 5, 6, 7, 16, 17, 18 and 19.
- Montserrat (from the supplied inspiration) is loaded for numeric display values (stat, gauge, dial and
  bar values) to echo the infographic's percent rings.
- Fix found in review: the rotating rings orbited instead of spinning because the `rotate` property is
  applied before `transform: translateX(-50%)`; the rings are now positioned with `left: 0; width: 100%`.
