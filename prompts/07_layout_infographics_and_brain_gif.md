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

(appended after execution)

### Stage 2 – brain bridge and medical micro-animations

(appended after execution)
