# 05 · Neuro-Sim dopamine engine, first-person 3D POV and UI/UX overhaul

**Date:** 2026-10-30
**Note on numbering:** the prompt asked for `04_neuro_sim_and_ux_overhaul.md`; `04_submission_and_git.md`
already existed, so this log is numbered 05 to keep the sequence unambiguous.

## Prompt (verbatim)

```
# System Task: Comprehensive UI/UX Overhaul, First-Person 3D Hallucination POV, and Python Neuro-Sim Dopamine Engine

We are executing a major architectural and visual iteration on our Schizophrenia capstone project. You must
implement all requirements below systematically, log this prompt in `/prompts`, update the Change Log inside
`README.md` before every commit, and push incremental commits to GitHub
(`https://github.com/OmriAbel6/schizophrenia-vibe-project.git`).

---

## 1. Visual Theme, Accessible Color Palette & Modern Typography (`web/style.css`, `web/index.html`)
- **Strict Color Palette**: Replace the dark navy theme completely with an accessible, warm, pleasant light theme:
  - Primary Background: Warm Cream (`#FAF7F0` / `#F5F2EB`).
  - Typography & Subtitles: Strict combination of Deep Charcoal Black (`#1A1A1A`), Slate Grey (`#5A626A`),
    and Soft Sky/Light Blue (`#3B82F6` / `#60A5FA`). Use ONLY these colors across the general presentation
    (except where explicitly specified for positive/negative symptoms and neural pathway charts).
- **Modern, Approachable Hebrew Typography**:
  - Load and apply modern, friendly Hebrew fonts from Google Fonts: `Rubik` or `Fredoka` for headings,
    paired with `Assistant` or `Varela Round` for body text.
- **Editorial Flow (Fewer Boxes, More Flow)**:
  - Eliminate rigid, cluttered text boxes. Use open layouts, generous whitespace, flowing typography, and
    clean visual hierarchy.
- **Tactile Micro-Interactions & Smooth Transitions**:
  - Every interactive element, highlight block, or card must react smoothly on cursor hover
    (`transform: translateY(-6px) scale(1.015)`, subtle elevation shadow, and soft blue accent highlight)
    so the presentation feels alive.
  - Implement smooth CSS slide-to-slide transitions (cubic-bezier fade + gentle RTL horizontal glide).

---

## 2. Specific Slide Fixes & Content Updates (`web/index.html`)
- **Slide 1 (Title Slide Metadata)**:
  - Display the presenters and lecturer prominently:
    - מגישים: **עומרי אבל** ו**אלה אדרי**
    - מרצה: **ד״ר יורם ראובן סגל**
- **Slide 3 (RTL Number Overlap Fix & Symptom Color Coding)**:
  - Fix the layout bug where numbers overlap the Hebrew text by using proper Flexbox/Grid gap spacing
    (`gap: 1.25rem`) and isolated number badges.
  - Style **Positive Symptoms (תסמינים חיוביים)** with a soft, accessible Green background (`#DCFCE7`
    background, `#15803D` text/border) and **Negative Symptoms (תסמינים שליליים)** with a soft, accessible
    Red background (`#FEE2E2` background, `#B91C1C` text/border).
- **Slide 13 (Readability & Font Scaling)**:
  - Significantly enlarge the font size (`clamp(1.25rem, 2vw, 1.6rem)`), line-height (`1.75`), and visual
    spacing so the text is crisp, clear, and effortless to read.

---

## 3. Slide 8: First-Person (POV) Realistic 3D Hallucination Experience (`web/app.js`, `web/index.html`)
- Replace the abstract geometric scene with an **immersive First-Person Perspective (POV) 3D architectural
  simulation** using Three.js:
  - **The Scenario**: The viewer experiences looking through the eyes of a person with schizophrenia
    stepping toward and out the front door of their home into a hallway/street.
  - **Visual & Perceptual Distortions**: As the POV camera moves through the doorway, trigger realistic
    perceptual disturbances — walls subtly breathing/warping, shadows detaching and stretching, flickering
    overhead lights, chromatic aberration/vignette pulsing, and peripheral shadow silhouettes or intrusive
    visual fragments that vanish when looked at directly.
  - **Auditory Hallucinations & Anxiety Induction (Web Audio API)**:
    - Synthesize a realistic spatial audio environment conveying the patient's acute anxiety: a rising
      anxious heartbeat pulse (low-frequency thump), spatialized whispers panning sharply between left and
      right ears, muffled door creaks/footsteps, and a tense high-frequency ring.
  - **Interactive POV Controls**: Provide clear Hebrew buttons to "צעד אל מחוץ לדלת" (Advance POV through
    doorway), adjust "עוצמת ההזיה והחרדה" (Hallucination & Anxiety Intensity slider), toggle "שמע מרחבי"
    (Spatial Audio), and "הרגעה / איפוס" (Reset to calm baseline).

---

## 4. Python Component Replacement: Neuro-Sim Dopamine & Medication Engine (`python/` & Slides 16–18)
Replace the dry PANSS score calculator with **Option 2: A Neurobiological Dopamine & Antipsychotic
Medication Simulator (`schizophrenia_analysis.py` + `main.py`)**.

### A. Python Backend (`python/schizophrenia_analysis.py` & `python/main.py`):
- Model the two primary dopamine pathways in schizophrenia:
  1. **Mesolimbic Pathway (הנתיב המזולימבי)**: Hyperactivity (`>100%` dopamine signaling) driving Positive
     Symptoms (hallucinations, delusions).
  2. **Mesocortical Pathway (הנתיב המזוקורטיקלי)**: Hypoactivity (`<100%` dopamine signaling) driving
     Negative & Cognitive Symptoms (apathy, flat affect).
- Simulate 4 distinct clinical states across time and D2/5-HT2A receptor occupancy:
  1. `בריא (איזון נוירוכימי תקין)` – Balanced baseline (100% Mesolimbic, 100% Mesocortical).
  2. `התקף פסיכוטי (ללא טיפול)` – Dopamine storm in Mesolimbic (185%), deficit in Mesocortical (45%), high
     hallucinations, high anxiety.
  3. `תרופות דור 1 (חסימת D2 גורפת - למשל הלדול)` – Drops Mesolimbic dopamine effectively (reduces
     hallucinations), but further suppresses Mesocortical dopamine and spikes motor side-effects (EPS).
  4. `תרופות דור 2 (איזון סרוטונין-דופמין משולב)` – Brings Mesolimbic storm down to calm levels while
     preserving/boosting Mesocortical activity, minimizing side effects and restoring quality of life.
- Running `python3 python/main.py` must output clean, structured data into `web/metrics.json` and
  `web/metrics.js` (using standard library only, PEP 8 compliant). Update `PRD.md` and `README.md` to
  describe this Neuro-Sim Dopamine Engine as our Python component.

### B. Interactive Visualization on Slides 16–18 (NO Code Shown!):
- **Strictly NO Code on Slides**: Remove all Python code snippets, terminal outputs, or dense technical
  paragraphs from Slides 16–18.
- **Large, Accessible, Interactive Visuals**:
  - **Slide 16 (סערת הדופמין במוח: הנתיב המזולימבי מול המזוקורטיקלי)**: Large, animated side-by-side
    comparison gauges/bars with huge, clear Hebrew typography (`18px–22px` minimum labels) showing the stark
    contrast between a healthy brain and an untreated psychotic state.
  - **Slide 17 (סימולטור השפעת התרופות בזמן אמת)**: An interactive dashboard where clicking big, friendly
    buttons (`ללא טיפול`, `תרופות דור 1`, `תרופות דור 2`) dynamically animates the Python-generated
    graphs—showing how receptor blockade calms hallucinations vs. impacts side effects and negative symptoms.
  - **Slide 18 (איזון מוחי ואיכות חיים לאורך זמן)**: An interactive timeline curve showing symptom relief
    and daily functioning recovery, where hovering over milestones pops up a large, friendly single-sentence
    card explaining the clinical takeaway.

---

## 5. Prompt History Logging & Incremental GitHub Workflow
Follow the mandatory course Git methodology—do NOT push everything in a single commit:

1. **Log Prompt**:
   - Save this full prompt and an architectural execution log into `prompts/04_neuro_sim_and_ux_overhaul.md`.

2. **Commit & Push 1 (Python Neuro-Sim Dopamine Engine & PRD Update)**:
   - Run `python3 python/main.py` to generate the new `metrics.json` and `metrics.js`.
   - Update `PRD.md` and append a row to the Change Log table in `README.md` (Date: `2026-10-30`, Author:
     `עומרי אבל & אלה אדרי`, Description: `"שדרוג רכיב הפייתון לסימולטור נוירוביולוגי של נתיבי הדופמין
     והשפעת תרופות (Neuro-Sim) וייצוא נתונים חדשים"`).
   - Execute:
     git add python/ PRD.md README.md prompts/
     git commit -m "feat(python): replace PANSS script with Neuro-Sim dopamine and medication engine"
     git push origin main

3. **Commit & Push 2 (Cream Palette, Typography & Slide 1/3/13 Fixes)**:
   - Append a row to the Change Log table in `README.md`: `"מעבר לפלטת צבעי שמנת וכחול בהיר נגישה, הוספת
     שמות המגישים (עומרי אבל, אלה אדרי) והמרצה (ד״ר יורם ראובן סגל), תיקון שקופית 3 והגדלת כתב בשקופית 13"`.
   - Execute:
     git add web/style.css web/index.html README.md
     git commit -m "style(web): implement accessible cream/sky theme, modern typography, and slide 1/3/13 fixes"
     git push origin main

4. **Commit & Push 3 (First-Person 3D Hallucination POV & Interactive Dopamine Charts)**:
   - Append a row to the Change Log table in `README.md`: `"הטמעת סימולציית 3D מגוף ראשון (יציאה מהדלת
     והזיות שמיעתיות/ויזואליות) ועיצוב מחדש של שקופיות 16-18 לגרפים אינטראקטיביים ללא הצגת קוד"`.
   - Execute:
     git add web/ README.md
     git commit -m "feat(web): add 1st-person doorway hallucination 3D POV and interactive dopamine charts"
     git push origin main

5. **Verification**:
   - Run `git log -3 --stat` to confirm all 3 incremental commits were pushed cleanly to GitHub, and open
     `web/index.html` in the browser for inspection.
```

## Architectural execution log

### Commit 1 – Python Neuro-Sim engine

- `schizophrenia_analysis.py` rewritten around three concepts:
  - **Pathways** – mesolimbic and mesocortical signalling as % of healthy (100).
  - **Pharmacology** – `Drug` dataclass with D2 and 5-HT2A occupancy, onset half-life and metabolic burden.
    `effective_signaling = raw × (1 − D2 × 0.65)`, plus `5-HT2A × 60` cortical release for the mesocortical
    pathway. EPS follow a sigmoid centred on 80 % D2 occupancy (Kapur et al., 2000).
  - **Clinical states** – healthy (100/100), untreated psychosis (185/45), FGA haloperidol (D2 86 %, 5-HT2A
    5 %), SGA risperidone-like (D2 70 %, 5-HT2A 90 %).
- `symptom_profile` maps signalling to 0–100 scores (positive, hallucinations, delusions, anxiety, negative,
  cognitive, EPS, metabolic, functioning) with sigmoids, so the four states separate cleanly:

  | state | MesoL | MesoC | Pos | Neg | EPS | Func |
  |---|---|---|---|---|---|---|
  | healthy | 100 | 100 | 5 | 8 | 0 | 95 |
  | psychosis | 185 | 45 | 98 | 89 | 0 | 29 |
  | fga | 82 | 23 | 1 | 98 | 82 | 46 |
  | sga | 101 | 79 | 6 | 33 | 8 | 81 |

- `timeline` (12 weeks, half-week steps) lets occupancy build with a half-life and pathways adapt with a
  lag; `milestones` derives Hebrew one-sentence takeaways from threshold crossings; `occupancy_sweep`
  provides dose-response rows (0–100 % D2) for both generations.
- `main.py` keeps the `python/` → `web/` mirroring; `--seed` was dropped (the model is deterministic).
- Palette check for the pathway/symptom colours mandated in §2 (`#15803D`, `#B91C1C`, `#3B82F6`) on the
  cream surface: red↔green adjacent fails the CVD gate (ΔE 4.2), so charts never place them adjacent
  without blue between and always pair colour with labels/icons; the order green–blue–red passes all checks.
- PRD §1, §2, §5.1 F-12, §5.2, §7 and §8 updated; README Python section and change log updated.

### Commit 2 – Cream theme, typography, slide 1/3/13

- `style.css` rewritten (508 lines): tokens `--bg #FAF7F0`, `--bg-2 #F5F2EB`, `--ink #1A1A1A`, `--slate
  #5A626A`, `--sky #3B82F6`, `--sky-light #60A5FA`; green/red reserved for positive/negative symptoms and
  pathway charts. Rubik for headings, Assistant for body (Google Fonts).
- Editorial flow: `.card` blocks are borderless and transparent until hovered; every interactive block
  (`.card`, `.stat`, `.criterion`, `.chip`, `.btn`, `.pill`, timeline items, flow steps, gauges, panels,
  nav buttons) uses `transform: translateY(-6px) scale(1.015)` + elevation shadow + sky accent on hover.
  Slide transitions use `cubic-bezier(0.22, 1, 0.36, 1)` with a 56 px RTL glide.
- Slide 1: presenters עומרי אבל, אלה אדרי and lecturer ד״ר יורם ראובן סגל in prominent cards.
- Slide 3: criterion A list rebuilt as isolated number badges inside pill items with `gap: 1.25rem`;
  items 1–4 styled positive (`#DCFCE7`/`#15803D`), item 5 negative (`#FEE2E2`/`#B91C1C`); slide 4 cards
  re-skinned the same way.
- Slide 13: table font `clamp(1.25rem, 2vw, 1.6rem)`, line-height 1.75, wide container; padding tightened
  after a screenshot showed the table running past the viewport.
- Verified with headless-Chrome screenshots of slides 1, 3, 4, 5, 13.

### Commit 3 – First-person POV scene and slides 16–18

- **Slide 8** (`createPOVScene`): a 5×3×8 m hallway with rug, sideboard, picture and coat stand, a framed
  door that swings open as the camera approaches, and a night street beyond (pavement, asphalt, five
  buildings with lit windows, three street lamps). Seven waypoints carry the camera from inside the home,
  through the doorway, to the street. Distortion strength = intensity × (0.3 + 0.7 × door-proximity):
  simplex-noise breathing walls and ceiling, randomly flickering ceiling light, a detached floor shadow
  that drifts and stretches, six peripheral silhouettes that fade out within ~18° of the gaze direction,
  darting visual fragments, perceptual drift/roll/FOV pulsing, CSS vignette pulse and chromatic fringing
  (`drop-shadow` red/cyan offsets). Mouse-look over the stage. Controls: "צעד אל מחוץ לדלת" (step), "עוצמת
  ההזיה והחרדה" slider, "שמע מרחבי" toggle, "הרגעה / איפוס" (returns to the start, intensity 15, audio off).
  2D-canvas corridor fallback when Three.js is unavailable.
- **Audio** (`createPOVAudio`): heartbeat (double sine thump, 62–148 BPM with intensity), whispers
  (band-passed noise bursts hard-panned alternating ±0.85–1.0), muffled footsteps on each step, a door
  creak when crossing the threshold, a 7.6 kHz tremolo ring and a low street bed. Starts only from the
  toggle (user gesture); stops when leaving the slide.
- **Slides 16–18** are code-free. 16: two gauge columns (healthy vs. untreated) with 0–200 % tracks and a
  100 % baseline, labels ≥ 18 px, fills animate on slide entry; symptom tags. 17: three state buttons drive
  receptor dials (D2 / 5-HT2A), pathway bars, symptom/side-effect bars, a therapeutic-window chart from
  the occupancy sweep with a moving marker, and a one-paragraph summary. 18: functioning-over-time curves
  (untreated dashed red, FGA slate, SGA sky) with milestone circles; hover/focus/click shows a large
  one-sentence takeaway card.
- A section-replacement bug (replacing the *previous* section instead of the targeted one) was caught by
  listing slide titles after the edit; `index.html` was restored from HEAD and the replacement redone.
- Verified: POV harness clicked start + five steps → `STEPS=5` in the DOM dump and the camera advanced in
  the SwiftShader render; slides 16–18 screenshots fit the 1440×900 viewport after two compaction passes.
