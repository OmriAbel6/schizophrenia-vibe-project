"""Neuro-Sim: dopamine pathway and antipsychotic medication simulator.

Educational model for the schizophrenia capstone presentation.  It describes
the two dopamine pathways most implicated in schizophrenia and how receptor
blockade by first- and second-generation antipsychotics changes their
signalling, the resulting symptom domains, side effects and daily
functioning.

The model is a *caricature* built from textbook pharmacology (Kapur &
Seeman, 2001; Howes & Kapur, 2009; Stahl, 2021).  All numbers are synthetic
and must not be read as patient data or dosing guidance.
"""

from __future__ import annotations

import datetime as _dt
import math
from dataclasses import dataclass
from typing import Dict, List, Mapping, Sequence

# --------------------------------------------------------------------------- #
# Pathways
# --------------------------------------------------------------------------- #

PATHWAYS: Dict[str, Dict[str, str]] = {
    "mesolimbic": {
        "name_he": "הנתיב המזולימבי",
        "origin_he": "VTA ← גרעין האקומבנס / סטריאטום",
        "drives_he": "תסמינים חיוביים: הזיות ומחשבות שווא",
        "pathology_he": "פעילות יתר (מעל 100%) – סערת דופמין",
    },
    "mesocortical": {
        "name_he": "הנתיב המזוקורטיקלי",
        "origin_he": "VTA ← קורטקס פרה-פרונטלי",
        "drives_he": "תסמינים שליליים וקוגניטיביים: אפתיה, השטחה, קשב",
        "pathology_he": "תת-פעילות (מתחת ל-100%) – חסר דופמין",
    },
}

HEALTHY_SIGNALING = 100.0


# --------------------------------------------------------------------------- #
# Pharmacology
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Drug:
    """Receptor-occupancy caricature of an antipsychotic."""

    key: str
    name: str
    name_he: str
    generation: int
    d2_occupancy: float
    ht2a_occupancy: float
    onset_half_life_weeks: float
    metabolic_burden: float  # 0-100 weight gain / metabolic risk

    def occupancy_at(self, week: float, receptor: str) -> float:
        target = self.d2_occupancy if receptor == "d2" else self.ht2a_occupancy
        build_up = 1.0 - math.exp(-math.log(2.0) * week / self.onset_half_life_weeks)
        return target * build_up


NO_DRUG = Drug("none", "No treatment", "ללא טיפול", 0, 0.0, 0.0, 1.0, 0.0)

DRUGS: Dict[str, Drug] = {
    "fga": Drug(
        key="fga",
        name="Haloperidol (first generation)",
        name_he="הלופרידול (דור ראשון)",
        generation=1,
        d2_occupancy=0.86,
        ht2a_occupancy=0.05,
        onset_half_life_weeks=1.2,
        metabolic_burden=12.0,
    ),
    "sga": Drug(
        key="sga",
        name="Risperidone-like (second generation)",
        name_he="ריספרידון (דור שני)",
        generation=2,
        d2_occupancy=0.70,
        ht2a_occupancy=0.90,
        onset_half_life_weeks=1.5,
        metabolic_burden=38.0,
    ),
}

# Fraction of pathway signalling removed at full D2 blockade.
D2_BLOCKADE_GAIN = 0.65
# Cortical dopamine released (in % of healthy) by full 5-HT2A antagonism:
# blocking 5-HT2A on cortical neurons disinhibits dopamine release.
HT2A_CORTICAL_GAIN = 60.0
# Extrapyramidal symptoms appear once striatal D2 occupancy exceeds ~80 %.
EPS_THRESHOLD = 0.80
EPS_WIDTH = 0.04


def effective_signaling(raw: float, pathway: str, d2: float, ht2a: float) -> float:
    """Dopamine signalling (% of healthy) after receptor blockade."""
    value = raw * (1.0 - d2 * D2_BLOCKADE_GAIN)
    if pathway == "mesocortical":
        value += ht2a * HT2A_CORTICAL_GAIN
    return max(0.0, value)


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def symptom_profile(
    mesolimbic: float, mesocortical: float, d2: float, metabolic: float
) -> Dict[str, float]:
    """Map pathway signalling and occupancy to 0-100 symptom scores."""
    positive = 100.0 * _sigmoid((mesolimbic - 135.0) / 12.0)
    negative = 100.0 * _sigmoid((70.0 - mesocortical) / 12.0)
    cognitive = 100.0 * _sigmoid((65.0 - mesocortical) / 15.0)
    eps = 100.0 * _sigmoid((d2 - EPS_THRESHOLD) / EPS_WIDTH) if d2 > 0 else 0.0
    anxiety = 8.0 + 0.72 * positive + 0.2 * eps
    hallucinations = positive * 0.95
    delusions = positive * 0.9 + 2.0
    burden = (
        0.35 * positive
        + 0.30 * negative
        + 0.12 * cognitive
        + 0.15 * eps
        + 0.08 * metabolic
    )
    functioning = max(0.0, 100.0 - burden)
    return {
        "positive": round(positive, 1),
        "hallucinations": round(hallucinations, 1),
        "delusions": round(min(100.0, delusions), 1),
        "anxiety": round(min(100.0, anxiety), 1),
        "negative": round(negative, 1),
        "cognitive": round(cognitive, 1),
        "eps": round(eps, 1),
        "metabolic": round(metabolic, 1),
        "functioning": round(functioning, 1),
    }


# --------------------------------------------------------------------------- #
# Clinical states
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ClinicalState:
    key: str
    name_he: str
    summary_he: str
    raw_mesolimbic: float
    raw_mesocortical: float
    drug: Drug


STATES: Sequence[ClinicalState] = (
    ClinicalState(
        key="healthy",
        name_he="בריא (איזון נוירוכימי תקין)",
        summary_he="שני הנתיבים מאוזנים סביב 100% – תפיסה ותפקוד תקינים.",
        raw_mesolimbic=100.0,
        raw_mesocortical=100.0,
        drug=NO_DRUG,
    ),
    ClinicalState(
        key="psychosis",
        name_he="התקף פסיכוטי (ללא טיפול)",
        summary_he=(
            "סערת דופמין בנתיב המזולימבי (185%) לצד חסר מזוקורטיקלי (45%) – "
            "הזיות, מחשבות שווא וחרדה גבוהה."
        ),
        raw_mesolimbic=185.0,
        raw_mesocortical=45.0,
        drug=NO_DRUG,
    ),
    ClinicalState(
        key="fga",
        name_he="תרופות דור 1 (חסימת D2 גורפת – למשל הלדול)",
        summary_he=(
            "חסימה גורפת של D2 מרגיעה את הסערה המזולימבית, אך מדכאת עוד יותר "
            "את הנתיב המזוקורטיקלי ומזניקה תופעות לוואי מוטוריות (EPS)."
        ),
        raw_mesolimbic=185.0,
        raw_mesocortical=45.0,
        drug=DRUGS["fga"],
    ),
    ClinicalState(
        key="sga",
        name_he="תרופות דור 2 (איזון סרוטונין-דופמין משולב)",
        summary_he=(
            "חסימת D2 מתונה עם חסימת 5-HT2A: הסערה המזולימבית נרגעת, "
            "הפעילות המזוקורטיקלית נשמרת ואף משתפרת, ותופעות הלוואי המוטוריות "
            "מזעריות."
        ),
        raw_mesolimbic=185.0,
        raw_mesocortical=45.0,
        drug=DRUGS["sga"],
    ),
)


def steady_state(state: ClinicalState) -> Dict[str, object]:
    d2, ht2a = state.drug.d2_occupancy, state.drug.ht2a_occupancy
    mesolimbic = effective_signaling(state.raw_mesolimbic, "mesolimbic", d2, ht2a)
    mesocortical = effective_signaling(
        state.raw_mesocortical, "mesocortical", d2, ht2a
    )
    return {
        "mesolimbic": round(mesolimbic, 1),
        "mesocortical": round(mesocortical, 1),
        "d2_occupancy": round(d2 * 100),
        "ht2a_occupancy": round(ht2a * 100),
        "symptoms": symptom_profile(
            mesolimbic, mesocortical, d2, state.drug.metabolic_burden
        ),
    }


# --------------------------------------------------------------------------- #
# Time course
# --------------------------------------------------------------------------- #

PATHWAY_ADAPTATION_WEEKS = 2.5  # dopamine systems lag behind receptor occupancy


def timeline(
    state: ClinicalState, weeks: int, step: float = 0.5
) -> List[Dict[str, float]]:
    """Weekly course from the start of treatment (week 0 = acute state)."""
    points: List[Dict[str, float]] = []
    n_steps = int(round(weeks / step))
    for index in range(n_steps + 1):
        week = index * step
        d2 = state.drug.occupancy_at(week, "d2")
        ht2a = state.drug.occupancy_at(week, "ht2a")
        # Pathway signalling follows occupancy with a lag.
        lag = 1.0 - math.exp(-week / PATHWAY_ADAPTATION_WEEKS)
        target_ml = effective_signaling(state.raw_mesolimbic, "mesolimbic", d2, ht2a)
        target_mc = effective_signaling(
            state.raw_mesocortical, "mesocortical", d2, ht2a
        )
        mesolimbic = state.raw_mesolimbic + (target_ml - state.raw_mesolimbic) * lag
        mesocortical = state.raw_mesocortical + (
            target_mc - state.raw_mesocortical
        ) * lag
        metabolic = state.drug.metabolic_burden * min(1.0, week / max(weeks, 1))
        symptoms = symptom_profile(mesolimbic, mesocortical, d2, metabolic)
        points.append(
            {
                "week": week,
                "mesolimbic": round(mesolimbic, 1),
                "mesocortical": round(mesocortical, 1),
                "d2_occupancy": round(d2 * 100, 1),
                "ht2a_occupancy": round(ht2a * 100, 1),
                **symptoms,
            }
        )
    return points


def _milestone(week: float, title_he: str, takeaway_he: str) -> Dict[str, object]:
    return {"week": week, "title_he": title_he, "takeaway_he": takeaway_he}


def _first_week(
    course: Sequence[Mapping[str, float]], key: str, value: float, above: bool
) -> float:
    for point in course:
        if (point[key] >= value) if above else (point[key] <= value):
            return point["week"]
    return course[-1]["week"]


def milestones(
    state: ClinicalState, course: Sequence[Mapping[str, float]]
) -> List[Dict[str, object]]:
    """Clinically meaningful moments along the course, one-sentence takeaways."""
    last_week = course[-1]["week"]
    if state.key == "healthy":
        return [
            _milestone(0, "איזון", "שני הנתיבים ב-100% – אין תסמינים."),
            _milestone(
                last_week, "יציבות", "ללא שינוי לאורך זמן – קו הייחוס להשוואה."
            ),
        ]
    if state.drug is NO_DRUG:
        return [
            _milestone(0, "התקף חריף", "הזיות וחרדה בשיא; התפקוד היומיומי קורס."),
            _milestone(
                4, "ללא טיפול", "סערת הדופמין אינה שוככת מעצמה – התפקוד נותר נמוך."
            ),
            _milestone(
                last_week,
                "מהלך מתמשך",
                "ככל שהפסיכוזה אינה מטופלת זמן רב יותר, ההחלמה קשה יותר.",
            ),
        ]

    items = [
        _milestone(
            0, "תחילת טיפול", "התרופה מתחילה לתפוס קולטני D2; המוח עדיין בסערה."
        ),
        _milestone(
            _first_week(course, "anxiety", 45, above=False),
            "החרדה יורדת",
            "ההרגעה מורגשת עוד לפני שההזיות נעלמות.",
        ),
        _milestone(
            _first_week(course, "positive", 25, above=False),
            "ההזיות שוככות",
            "חסימת D2 מורידה את הסערה המזולימבית מתחת לסף ההזיה.",
        ),
    ]
    if state.drug.generation == 1:
        items.append(
            _milestone(
                _first_week(course, "eps", 50, above=True),
                "תופעות לוואי מוטוריות",
                "תפיסה של יותר מ-80% מקולטני D2 מביאה לנוקשות ולרעד (EPS).",
            )
        )
        items.append(
            _milestone(
                last_week,
                "תפקוד חלקי",
                "ההזיות נעלמו, אך האפתיה ותופעות הלוואי מגבילות את איכות החיים.",
            )
        )
    else:
        items.append(
            _milestone(
                _first_week(course, "mesocortical", 65, above=True),
                "הנתיב המזוקורטיקלי מתאושש",
                "חסימת 5-HT2A משחררת דופמין בקורטקס – האפתיה פוחתת.",
            )
        )
        items.append(
            _milestone(
                _first_week(course, "functioning", 78, above=True),
                "חזרה לתפקוד",
                "איזון בין שני הנתיבים מחזיר את היכולת לעבוד, ללמוד ולהתחבר.",
            )
        )
    items.sort(key=lambda m: m["week"])
    return items


# --------------------------------------------------------------------------- #
# Occupancy sweep (dose-response) for the interactive simulator
# --------------------------------------------------------------------------- #


def occupancy_sweep(step: int = 5) -> List[Dict[str, object]]:
    """Symptoms vs. D2 occupancy for each generation at the acute baseline."""
    psychosis = STATES[1]
    rows = []
    for occupancy in range(0, 101, step):
        d2 = occupancy / 100.0
        row: Dict[str, object] = {"d2_occupancy": occupancy}
        for drug in DRUGS.values():
            # 5-HT2A occupancy scales with the drug's own D2:5-HT2A ratio.
            ratio = (
                drug.ht2a_occupancy / drug.d2_occupancy if drug.d2_occupancy else 0.0
            )
            ht2a = min(1.0, d2 * ratio)
            ml = effective_signaling(psychosis.raw_mesolimbic, "mesolimbic", d2, ht2a)
            mc = effective_signaling(
                psychosis.raw_mesocortical, "mesocortical", d2, ht2a
            )
            symptoms = symptom_profile(ml, mc, d2, drug.metabolic_burden)
            row[drug.key] = {
                "mesolimbic": round(ml, 1),
                "mesocortical": round(mc, 1),
                "positive": symptoms["positive"],
                "negative": symptoms["negative"],
                "eps": symptoms["eps"],
                "functioning": symptoms["functioning"],
            }
        rows.append(row)
    return rows


# --------------------------------------------------------------------------- #
# Export
# --------------------------------------------------------------------------- #

SYMPTOM_LABELS_HE: Dict[str, str] = {
    "positive": "תסמינים חיוביים",
    "hallucinations": "הזיות",
    "delusions": "מחשבות שווא",
    "anxiety": "חרדה",
    "negative": "תסמינים שליליים",
    "cognitive": "ליקוי קוגניטיבי",
    "eps": "תופעות לוואי מוטוריות (EPS)",
    "metabolic": "עומס מטבולי",
    "functioning": "תפקוד יומיומי",
}


def build_metrics(weeks: int = 12) -> Dict[str, object]:
    """Assemble the JSON document consumed by the presentation."""
    states = []
    for state in STATES:
        course = timeline(state, weeks)
        states.append(
            {
                "key": state.key,
                "name_he": state.name_he,
                "summary_he": state.summary_he,
                "drug": {
                    "key": state.drug.key,
                    "name": state.drug.name,
                    "name_he": state.drug.name_he,
                    "generation": state.drug.generation,
                    "d2_occupancy": round(state.drug.d2_occupancy * 100),
                    "ht2a_occupancy": round(state.drug.ht2a_occupancy * 100),
                    "metabolic_burden": state.drug.metabolic_burden,
                },
                "raw": {
                    "mesolimbic": state.raw_mesolimbic,
                    "mesocortical": state.raw_mesocortical,
                },
                "steady": steady_state(state),
                "timeline": course,
                "milestones": milestones(state, course),
            }
        )
    return {
        "meta": {
            "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "generator": "schizophrenia_analysis.py (Neuro-Sim dopamine engine)",
            "weeks": weeks,
            "healthy_signaling": HEALTHY_SIGNALING,
            "disclaimer_he": (
                "מודל חינוכי מפושט של נתיבי הדופמין והשפעת תרופות – אינו מייצג "
                "מטופלים אמיתיים ואינו הנחיית מינון."
            ),
            "model": {
                "d2_blockade_gain": D2_BLOCKADE_GAIN,
                "ht2a_cortical_gain": HT2A_CORTICAL_GAIN,
                "eps_threshold_occupancy": EPS_THRESHOLD,
                "pathway_adaptation_weeks": PATHWAY_ADAPTATION_WEEKS,
            },
            "pathways": PATHWAYS,
            "symptom_labels_he": SYMPTOM_LABELS_HE,
            "references": [
                "Howes, O. D., & Kapur, S. (2009). Schizophrenia Bulletin, "
                "35(3), 549-562.",
                "Kapur, S., & Seeman, P. (2001). American Journal of Psychiatry, "
                "158(3), 360-369.",
                "Kapur, S., Zipursky, R., et al. (2000). American Journal of "
                "Psychiatry, 157(4), 514-520.",
                "Stahl, S. M. (2021). Stahl's Essential Psychopharmacology (5th ed.).",
            ],
        },
        "states": states,
        "occupancy_sweep": occupancy_sweep(),
    }
