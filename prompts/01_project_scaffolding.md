# 01 · Project scaffolding – the founding prompt

**Date:** 2026-10-30
**Tool:** Claude Code (Claude Fable 5.1) running in VS Code, auto mode
**Outcome:** the complete project tree (`web/`, `python/`, `README.md`) was generated from this single
prompt in one session. Logs 02 and 03 document the frontend and Python sub-threads of that same session,
including the verification iterations that followed.

## Prompt (verbatim)

```
# System Context & Role
You are an expert full-stack web developer and Python software engineer. You are assisting a two-student
engineering team in developing an academic capstone web presentation on "Schizophrenia: Clinical,
Neurobiological, and Perceptual Dimensions".

# Constraints & Engineering Standards
1. Target Output: Single-page application (SPA) HTML5/CSS3/Vanilla JS presentation containing exactly 20
   structured, interactive slides.
2. Language & BiDi Support: Content must be fully in natural, academic Hebrew with strict bidirectional
   rendering:
   - Root document: `<html lang="he" dir="rtl">`.
   - Global CSS rule: `direction: rtl; text-align: right; unicode-bidi: isolate;`.
   - Clear CSS isolation for any embedded English/Latin terms or code tokens using `<bdi>` or
     `unicode-bidi: isolate`.
3. 3D Component (Schizophrenic Hallucination Simulation):
   - Embed a functional 3D media container representing visual and auditory hallucinations characteristic
     of schizophrenia (distorted perspective, surreal floating geometries, perceptual drift).
   - Implement either via Three.js (WebGL canvas) embedded directly, or an HTML5 `<video>` player embedding
     a seamless 3D spatial simulation with fallback interactive WebGL particle controls.
4. Python Component:
   - Provide a clean, modular Python module (`schizophrenia_analysis.py` + `main.py`).
   - Functionality: Acts as an academic data synthesizer/orchestrator (e.g., PANSS score calculator,
     Positive and Negative Syndrome Scale clinical trajectory simulator, or symptom progression visualizer
     that exports JSON data for the presentation to consume).
   - Must include `requirements.txt` and conform to PEP 8 standards.

---

# Deliverable 1: Presentation Structure & Content (20 Slides in Hebrew)
Please generate the comprehensive slide outline and layout structure covering:
- Slide 1: Title & Presenters (מבוא לסכיזופרניה: פסיכוביולוגיה, תפיסה וטכנולוגיה).
- Slides 2–4: Clinical definition, DSM-5 diagnostic criteria, positive vs. negative symptoms.
- Slides 5–7: Neurobiology (dopamine hypothesis, glutamate dysregulation, prefrontal cortex hypofunction).
- Slide 8: Interactive 3D Simulation Slide ("סימולציה תלת-ממדית: חוויית ההלוצינציה והעיוות התפיסתי")
  with controls.
- Slides 9–12: Cognitive impairments, affective symptoms, and functional decline.
- Slides 13–15: Contemporary treatments (first/second-gen antipsychotics, psychotherapy, digital health
  interventions).
- Slides 16–18: Python component integration — displaying computational metrics of symptom scoring and
  algorithmic assessment.
- Slide 19: Ethical considerations, destigmatization, and future clinical tech.
- Slide 20: Summary, Q&A, and Academic References.

---

# Deliverable 2: Frontend Implementation (`index.html`, `style.css`, `app.js`)
- UI/UX: Dark, clinical, modern aesthetic (deep navy/slate backgrounds `#0f172a`, subtle glowing accents
  `#38bdf8` and `#818cf8`, readable Hebrew typography using Google Fonts `Assistant` or `Heebo`).
- Keyboard & Click Navigation: Arrow keys (Left/Right respecting RTL orientation), progress bar, slide
  counter (`Slide X / 20`), and fullscreen toggle.
- 3D Hallucination Container: Complete inline WebGL / Three.js scene showing an eerie, fluidly morphing 3D
  geometry with subtle camera drift, illustrating perceptual distortion.

---

# Deliverable 3: Accompanying Python Software Tool (`analysis.py`)
- Provide the runnable Python script that generates the clinical scenario metrics (or acts as the local
  orchestrator), outputting clean `metrics.json` consumed by the HTML presentation.
```

## Assistant plan (as executed)

1. Loaded the data-visualisation guidance before writing any chart code, and validated the three-series
   chart palette (`#3987e5`, `#d95926`, `#199e70`) against both navy surfaces (`#0f172a`, `#1e293b`) with
   the palette validator – all six checks passed (lightness band, chroma floor, CVD separation,
   normal-vision floor, contrast).
2. Wrote the Python engine first (`schizophrenia_analysis.py`, `main.py`, `requirements.txt`) and ran it to
   produce `metrics.json` and a `metrics.js` twin, so the deck works both over HTTP (fetch) and from
   `file://` (script tag fallback).
3. Wrote `index.html` (20 slides), `style.css`, `app.js`.
4. Wrote `README.md` with the slide outline table.
5. Verified with headless Chrome screenshots (see logs 02 and 03).

## Decisions recorded

- Entry point named `main.py` (per the constraints section) rather than `analysis.py` (Deliverable 3
  heading); both names appeared in the prompt.
- Chart colours come from a validated categorical palette rather than the UI accents, because the UI
  accents (`#38bdf8`, `#818cf8`) are too close in hue to separate three series for colour-blind readers.
- All clinical numbers are synthetic and are labelled as such in the UI and in the JSON `meta.disclaimer_he`.
