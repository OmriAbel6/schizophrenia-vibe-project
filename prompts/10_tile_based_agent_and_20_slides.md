# 10 · Tile-based interactive patient agent and 20-slide restoration

**Date:** 2026-11-06

## Prompt (verbatim)

```
# System Task: Tile-Based Interactive Patient Agent, 20-Slide Restoration, and Continuous Git Workflow

We are executing a critical refinement for our capstone project to ensure robust functionality without
external API key dependencies, and restoring the strict 20-slide requirement.

Implement all requirements below systematically, save this prompt in
`prompts/10_tile_based_agent_and_20_slides.md`, update the Change Log inside `README.md` before every commit,
and push incremental commits to GitHub (https://github.com/OmriAbel6/schizophrenia-vibe-project.git).

## 1. Python Backend & Frontend: Tile-Based Interactive Patient Simulation
- **Remove Free-Text Input**: To avoid API token exhaustion and ensure a 100% reliable offline presentation
  demo, remove the free-text input field from the chat interface on the AI Simulation slide.
- **Interactive Question Tiles**: Replace the text input with a sleek Liquid Glass grid of predefined,
  clickable question tiles (e.g., "איך אתה ישן בלילה?", "האם אתה שומע משהו עכשיו?", "איך הקשר שלך עם
  המשפחה?").
- **Contextual Backend Logic (python/main.py)**: Update the FastAPI backend to route these specific tile
  clicks. The Python server must return distinct, highly accurate psychiatric responses depending on BOTH
  the specific question asked AND the active toggle state ("untreated" vs. "treated").
  - *Untreated Response Style*: Active psychosis, paranoia, responding to internal stimuli
    (hallucinations), loose associations.
  - *Treated Response Style*: Coherent, reality-tested, acknowledging past symptoms but demonstrating clear
    negative symptoms (flat affect, low motivation, social withdrawal).

## 2. Restoring the 20-Slide Structure
- The presentation currently dropped to 18 slides. You must expand it back to exactly 20 slides by
  injecting two deep-dive infographic slides after the initial clinical definition slides.
- **New Slide (Positive Symptoms Deep-Dive)**: Create a dedicated slide focusing entirely on Positive
  Symptoms (Hallucinations, Delusions, Paranoia). Use Liquid Glass infographics to visually explain how
  these actively disrupt the patient's daily life and perception of reality.
- **New Slide (Negative Symptoms Deep-Dive)**: Create a dedicated slide focusing entirely on Negative
  Symptoms (Avolition, Anhedonia, Flat Affect, Alogia). Use contrasting Liquid Glass visuals to map how
  these lead to social isolation and severe functional decline.
- Re-number the slide routing in `app.js` and ensure the slide counter (`Slide X / 20`) accurately reflects
  the full 20 slides.

## 3. Strict Incremental GitHub Workflow
Execute these commands sequentially using your terminal capabilities. Do NOT combine them into one commit:

1. Save this exact prompt to `prompts/10_tile_based_agent_and_20_slides.md`.
2. In `README.md`, append a new row to the Change Log (Date: 2026-11-06, Author: עומרי אבל & אלה אדרי,
   Description: "שדרוג סוכן ה-AI לממשק משבצות שיח מבוססות הקשר (ללא תלות בטוקנים חיצוניים), והחזרת
   המצגת ל-20 שקופיות עם צלילת עומק לתסמינים חיוביים ושליליים").
3. Run in terminal:
   git add python/ PRD.md README.md prompts/
   git commit -m "feat(python): implement tile-based interactive patient simulation backend"
   git push origin main

4. In `README.md`, append another row to the Change Log: "הטמעת משבצות שאלות אינטראקטיביות בממשק
   ה-Liquid Glass, והוספת 2 שקופיות אינפוגרפיקה חדשות להשלמת 20 שקופיות".
5. Run in terminal:
   git add web/ README.md
   git commit -m "feat(web): add interactive chat tiles and restore 20-slide structure with deep-dive symptom slides"
   git push origin main
```

## Execution summary

### Commit 1 – tile-routed backend

- New `python/dialogue.py`: the single source of truth for the interview. Ten tiles (sleep, hearing
  voices now, family, a typical day, medication, friends, feeling right now, safety, the coming year, how it
  began), each with two answer variants per clinical state – 40 answers. Untreated answers respond to
  internal stimuli (bracketed stage directions such as "[מפנה את הראש הצידה]"), carry persecutory and
  referential ideas and loosening of associations; treated answers are reality-tested and insightful while
  showing flat affect ("בסדר", "[טון אחיד]"), avolition, alogia-like brevity and social withdrawal.
  `python3 dialogue.py --export ../web/dialogue.js` writes the same bank as a browser global.
- `python/main.py`: `ChatRequest` now takes `question_id` (routed to the bank, rotating through variants
  per question × state) or `message` (free text → LLM when a key exists, scripted demo otherwise);
  `GET /api/questions` lists the tiles and `GET /api/dialogue` returns the full bank; `/api/health`
  reports the tile count. The treated system prompt now spells out the negative-symptom cluster.
- Verified with `curl`: 10 tiles listed; the sleep tile gives different answers in each state and rotates
  on a second click; unknown tile → 404; empty request → 422; free text still answered in demo mode;
  `/api/dialogue` matches the exported `web/dialogue.js` (loaded and parsed with Node: 10 tiles).
- PRD and README updated for the tile contract and the 20-slide outline.

### Commit 2 – tiles UI and the two deep-dive slides

- **Slide 5 – positive symptoms deep dive**: three glass cards (הזיות, מחשבות שווא, פרנויה), each with a
  definition, an inline SVG motif (animated voice waveform, a belief network with a glowing core, a
  sweeping paranoia radar with blips) and impact pills; below, a "מד השיבוש" with four life domains
  (sleep, study/work, trust in relatives, reality testing) whose emerald fills animate on slide entry.
- **Slide 6 – negative symptoms deep dive**: four rose-edged glass cards (אבוליציה, אנהדוניה, השטחה
  רגשית, אלוגיה) with declining mini bar motifs; below, shrinking concentric social circles (community →
  work → friends → family, outer rings fading in turn) beside a four-step cascade (symptoms → withdrawal →
  isolation → functional decline) built with the flowchart component in a rose variant; a one-line footnote
  on treatment response and Green (1996).
- **Chat slide (now 18)**: the free-text form and quick suggestions are gone; a 5×2 liquid-glass tile grid
  renders the ten questions (from `GET /api/questions` when the server answers, otherwise from
  `window.PATIENT_DIALOGUE` in `web/dialogue.js`). A click posts `{question_id, clinical_state}`; the reply
  is labelled "מהשרת" or "מאגר מקומי"; tiles already asked in the current state get a subtle mark; repeated
  clicks rotate variants on both paths. Status: green "מחובר לשרת · 10 שאלות" or amber "ללא שרת · מאגר
  מקומי זהה".
- `app.js`: `TOTAL = 20`, POV slide 10, chat 18, finale 20 (brain bridge on 19→20), floating nodes on
  1/7/8/9/18/19, stagger indices for the new grids.
- Verified with headless Chrome: 20 titles in order; slides 5, 6, 10, 20 fit at 1440×900; served from the
  backend, the "voices" tile answered in the untreated state, the toggle switched and the same tile gave
  the treated answer; with the server stopped and the page opened from `file://`, the medication tile
  answered from the local bank and the status showed the amber "ללא שרת" state.
