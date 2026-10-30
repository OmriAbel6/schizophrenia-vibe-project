# 04 · Submission preparation & Git history

**Date:** 2026-10-30

## Prompt (verbatim)

```
You need to finalize, structure, and push our academic schizophrenia project to GitHub according to the
strict course engineering guidelines.

Follow these steps sequentially using your terminal/file tools:

1. Verification & Directory Structure:
   - Ensure the project root contains:
     - `/web` with `index.html`, `style.css`, and `app.js` (fully functional, RTL-enabled, with the 3D
       Three.js hallucination slide and PANSS SVG charts).
     - `/python` with `schizophrenia_analysis.py`, `main.py`, `requirements.txt`, and generated
       `metrics.json` / `metrics.js`.
     - `/prompts` containing our full prompt interaction logs as `.md` files (e.g.,
       `01_project_scaffolding.md`, `02_frontend_development.md`, `03_python_orchestrator.md`).
     - `PRD.md` containing the complete Product Requirement Document for this project.
     - `README.md` populated with the required project template, student details, repository link
       (https://github.com/OmriAbel6/schizophrenia-vibe-project), execution instructions, and the Change
       Log table.

2. Git Initialization & Multi-Stage Commits:
   - Note: A single final push is strictly penalized by the course rubric. We must establish an
     incremental, modular commit history.
   - Run `git init` (if not already a git repository).
   - Configure remote origin:
     `git remote add origin https://github.com/OmriAbel6/schizophrenia-vibe-project.git` ||
     `git remote set-url origin https://github.com/OmriAbel6/schizophrenia-vibe-project.git`
   - Step A (Scaffolding & Prompts): Stage and commit initial structure, PRD, and prompt logs:
     `git add PRD.md prompts/ README.md`
     `git commit -m "docs: establish PRD, prompt history scaffolding, and project structure"`
   - Step B (Python Engine): Stage and commit the Python analysis module and generated data:
     `git add python/`
     `git commit -m "feat(python): implement PANSS trajectory simulation and JSON metrics exporter"`
   - Step C (Presentation & 3D Web): Stage and commit the web presentation and 3D visual component:
     `git add web/`
     `git commit -m "feat(web): build 20-slide RTL presentation with Three.js 3D hallucination simulation"`
   - Step D (Integration & Change Log): Update the Change Log table inside `README.md` with today's date
     and milestone notes, then stage and commit:
     `git add README.md`
     `git commit -m "chore: finalize README change log, verification checks, and submission prep"`

3. Branching & Push:
   - Rename current branch to `main`: `git branch -M main`
   - Push all commits and the main branch to the remote repository:
     `git push -u origin main`

Execute these commands, verify the status via `git status` and `git log --oneline`, and output the final
Git log summary to confirm success.
```

## Assistant actions

1. Confirmed the folder was not yet a git repository, that `gh` is authenticated as `OmriAbel6`, and that
   the remote repository exists and is empty.
2. Moved the generated-data default location to `python/` (per the directory guideline) with an automatic
   mirror into `web/` so the presentation keeps working.
3. Wrote `prompts/01–04`, `PRD.md`, `.gitignore`, and the templated `README.md`.
4. Executed the four-stage commit sequence exactly as specified (Step A also carried `.gitignore` as part
   of the project structure), renamed the branch to `main`, and pushed.
