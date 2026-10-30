"""Clinical data synthesizer for the schizophrenia capstone presentation.

The module models the Positive and Negative Syndrome Scale (PANSS; Kay,
Fiszbein & Opler, 1987), simulates symptom trajectories under different
treatment profiles, and derives rule-based clinical metrics (response,
remission, severity band) that the web presentation consumes as JSON.

Everything here is a *synthetic* educational model.  It is not a clinical
instrument and must not be used to assess real patients.
"""

from __future__ import annotations

import datetime as _dt
import math
import random
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

# --------------------------------------------------------------------------- #
# PANSS structure
# --------------------------------------------------------------------------- #

SCALE_MIN = 1
SCALE_MAX = 7

POSITIVE_ITEMS: Dict[str, str] = {
    "P1": "Delusions",
    "P2": "Conceptual disorganization",
    "P3": "Hallucinatory behavior",
    "P4": "Excitement",
    "P5": "Grandiosity",
    "P6": "Suspiciousness / persecution",
    "P7": "Hostility",
}

NEGATIVE_ITEMS: Dict[str, str] = {
    "N1": "Blunted affect",
    "N2": "Emotional withdrawal",
    "N3": "Poor rapport",
    "N4": "Passive / apathetic social withdrawal",
    "N5": "Difficulty in abstract thinking",
    "N6": "Lack of spontaneity and flow of conversation",
    "N7": "Stereotyped thinking",
}

GENERAL_ITEMS: Dict[str, str] = {
    "G1": "Somatic concern",
    "G2": "Anxiety",
    "G3": "Guilt feelings",
    "G4": "Tension",
    "G5": "Mannerisms and posturing",
    "G6": "Depression",
    "G7": "Motor retardation",
    "G8": "Uncooperativeness",
    "G9": "Unusual thought content",
    "G10": "Disorientation",
    "G11": "Poor attention",
    "G12": "Lack of judgment and insight",
    "G13": "Disturbance of volition",
    "G14": "Poor impulse control",
    "G15": "Preoccupation",
    "G16": "Active social avoidance",
}

ITEM_LABELS_HE: Dict[str, str] = {
    "P1": "מחשבות שווא",
    "P2": "חוסר ארגון מושגי",
    "P3": "התנהגות הזייתית",
    "P4": "התרגשות יתר",
    "P5": "גדלות",
    "P6": "חשדנות / רדיפה",
    "P7": "עוינות",
    "N1": "אפקט קהה",
    "N2": "נסיגה רגשית",
    "N3": "קשר דל",
    "N4": "נסיגה חברתית פסיבית",
    "N5": "קושי בחשיבה מופשטת",
    "N6": "חוסר ספונטניות בשיחה",
    "N7": "חשיבה סטריאוטיפית",
    "G1": "דאגה סומטית",
    "G2": "חרדה",
    "G3": "רגשות אשמה",
    "G4": "מתח",
    "G5": "מנייריזם ותנוחה",
    "G6": "דיכאון",
    "G7": "האטה מוטורית",
    "G8": "חוסר שיתוף פעולה",
    "G9": "תוכן מחשבה חריג",
    "G10": "חוסר התמצאות",
    "G11": "קשב ירוד",
    "G12": "חוסר שיפוט ותובנה",
    "G13": "הפרעה ברצייה",
    "G14": "שליטה ירודה בדחפים",
    "G15": "שקיעה במחשבות",
    "G16": "הימנעות חברתית פעילה",
}

DOMAIN_LABELS_HE: Dict[str, str] = {
    "positive": "תסמינים חיוביים",
    "negative": "תסמינים שליליים",
    "general": "פסיכופתולוגיה כללית",
}

# Symptomatic remission criteria (Andreasen et al., 2005): all eight items
# scored mild (3) or less for at least six months.
REMISSION_ITEMS: Sequence[str] = ("P1", "P2", "P3", "N1", "N4", "N6", "G5", "G9")
REMISSION_ITEM_MAX = 3
REMISSION_DURATION_WEEKS = 26

# PANSS total to Clinical Global Impression (CGI) severity anchors
# (Leucht et al., 2005): mildly ill ~58, moderately ill ~75,
# markedly ill ~95, severely ill ~116.
SEVERITY_BANDS: Sequence[tuple] = (
    (58, "minimal", "קל מאוד / ללא"),
    (75, "mild", "קל"),
    (95, "moderate", "בינוני"),
    (116, "marked", "ניכר"),
    (math.inf, "severe", "חמור"),
)

# Response thresholds as percentage reduction from the *adjusted* baseline
# (total minus 30, the scale minimum), per Leucht et al., 2009.
RESPONSE_MINIMAL = 20.0
RESPONSE_MUCH_IMPROVED = 50.0


# --------------------------------------------------------------------------- #
# Assessment
# --------------------------------------------------------------------------- #


def _validate_scores(scores: Mapping[str, int], expected: Iterable[str]) -> None:
    expected_keys = list(expected)
    missing = [key for key in expected_keys if key not in scores]
    if missing:
        raise ValueError(f"Missing PANSS items: {', '.join(missing)}")
    for key in expected_keys:
        value = scores[key]
        if not isinstance(value, int) or not SCALE_MIN <= value <= SCALE_MAX:
            raise ValueError(
                f"Item {key} must be an integer in [{SCALE_MIN}, {SCALE_MAX}], "
                f"got {value!r}"
            )


@dataclass
class PANSSAssessment:
    """A single PANSS rating (30 items) taken at a given week."""

    positive: Dict[str, int]
    negative: Dict[str, int]
    general: Dict[str, int]
    week: int = 0

    def __post_init__(self) -> None:
        _validate_scores(self.positive, POSITIVE_ITEMS)
        _validate_scores(self.negative, NEGATIVE_ITEMS)
        _validate_scores(self.general, GENERAL_ITEMS)

    # -- totals ------------------------------------------------------------- #
    @property
    def positive_total(self) -> int:
        return sum(self.positive.values())

    @property
    def negative_total(self) -> int:
        return sum(self.negative.values())

    @property
    def general_total(self) -> int:
        return sum(self.general.values())

    @property
    def total(self) -> int:
        return self.positive_total + self.negative_total + self.general_total

    @property
    def composite_index(self) -> int:
        """Positive minus negative subscale: >0 means positive-dominant."""
        return self.positive_total - self.negative_total

    # -- derived classifications ------------------------------------------- #
    def severity(self) -> Dict[str, str]:
        for upper, key, label_he in SEVERITY_BANDS:
            if self.total < upper:
                return {"key": key, "label_he": label_he}
        raise AssertionError("unreachable")  # pragma: no cover

    def item(self, code: str) -> int:
        for group in (self.positive, self.negative, self.general):
            if code in group:
                return group[code]
        raise KeyError(code)

    def meets_remission_threshold(self) -> bool:
        """Symptomatic criterion only (duration is checked on trajectories)."""
        return all(self.item(code) <= REMISSION_ITEM_MAX for code in REMISSION_ITEMS)

    def to_dict(self) -> Dict[str, object]:
        return {
            "week": self.week,
            "positive": self.positive_total,
            "negative": self.negative_total,
            "general": self.general_total,
            "total": self.total,
            "composite_index": self.composite_index,
            "remission_threshold": self.meets_remission_threshold(),
        }


# --------------------------------------------------------------------------- #
# Treatment profiles
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class TreatmentProfile:
    """Pharmacodynamic caricature of a treatment arm.

    ``efficacy`` is the fraction of the *excess* score (score - 1) that is
    removed at steady state for each domain.  ``half_life_weeks`` controls how
    fast the effect builds up.  ``relapse_hazard`` is the weekly probability
    of a relapse event once the acute phase has passed.
    """

    key: str
    name: str
    name_he: str
    drug_class: str
    efficacy: Mapping[str, float]
    half_life_weeks: float
    relapse_hazard: float
    adherence: float = 0.9

    def effect_at(self, week: int, domain: str) -> float:
        build_up = 1.0 - math.exp(-math.log(2.0) * week / self.half_life_weeks)
        return self.efficacy[domain] * self.adherence * build_up


DEFAULT_PROFILES: Dict[str, TreatmentProfile] = {
    "fga": TreatmentProfile(
        key="fga",
        name="First-generation antipsychotic (haloperidol)",
        name_he="אנטי-פסיכוטי דור ראשון (הלופרידול)",
        drug_class="FGA",
        efficacy={"positive": 0.60, "negative": 0.20, "general": 0.40},
        half_life_weeks=3.0,
        relapse_hazard=0.035,
        adherence=0.80,
    ),
    "sga": TreatmentProfile(
        key="sga",
        name="Second-generation antipsychotic (risperidone)",
        name_he="אנטי-פסיכוטי דור שני (ריספרידון)",
        drug_class="SGA",
        efficacy={"positive": 0.62, "negative": 0.32, "general": 0.45},
        half_life_weeks=3.0,
        relapse_hazard=0.022,
        adherence=0.88,
    ),
    "sga_plus_cbtp": TreatmentProfile(
        key="sga_plus_cbtp",
        name="SGA + CBTp + family intervention",
        name_he="דור שני + CBTp + התערבות משפחתית",
        drug_class="SGA + psychosocial",
        efficacy={"positive": 0.70, "negative": 0.50, "general": 0.60},
        half_life_weeks=3.5,
        relapse_hazard=0.008,
        adherence=0.94,
    ),
}


# --------------------------------------------------------------------------- #
# Baseline generation
# --------------------------------------------------------------------------- #


def _sample_domain(
    rng: random.Random, items: Iterable[str], mean: float, spread: float
) -> Dict[str, int]:
    scores = {}
    for code in items:
        raw = rng.gauss(mean, spread)
        scores[code] = int(max(SCALE_MIN, min(SCALE_MAX, round(raw))))
    return scores


def generate_baseline(
    rng: random.Random,
    positive_mean: float = 4.6,
    negative_mean: float = 4.0,
    general_mean: float = 3.6,
    spread: float = 1.0,
) -> PANSSAssessment:
    """Draw a plausible acute-phase baseline rating."""
    return PANSSAssessment(
        positive=_sample_domain(rng, POSITIVE_ITEMS, positive_mean, spread),
        negative=_sample_domain(rng, NEGATIVE_ITEMS, negative_mean, spread),
        general=_sample_domain(rng, GENERAL_ITEMS, general_mean, spread),
        week=0,
    )


# --------------------------------------------------------------------------- #
# Trajectory simulation
# --------------------------------------------------------------------------- #


@dataclass
class RelapseEvent:
    week: int
    magnitude: float
    duration_weeks: int


@dataclass
class TrajectoryResult:
    profile: TreatmentProfile
    baseline: PANSSAssessment
    assessments: List[PANSSAssessment]
    relapses: List[RelapseEvent] = field(default_factory=list)

    @property
    def endpoint(self) -> PANSSAssessment:
        return self.assessments[-1]


class TrajectorySimulator:
    """Simulate weekly PANSS ratings under a treatment profile.

    Each item decays from its baseline towards the scale floor following a
    first-order build-up of drug effect, with rater noise and stochastic
    relapse events that temporarily restore part of the baseline excess.
    """

    def __init__(
        self,
        baseline: PANSSAssessment,
        profile: TreatmentProfile,
        weeks: int = 52,
        seed: Optional[int] = None,
        noise_sd: float = 0.30,
    ) -> None:
        if weeks < 1:
            raise ValueError("weeks must be >= 1")
        self.baseline = baseline
        self.profile = profile
        self.weeks = weeks
        self.noise_sd = noise_sd
        self._rng = random.Random(seed)

    def _relapse_boost(self, week: int, relapses: List[RelapseEvent]) -> float:
        boost = 0.0
        for event in relapses:
            offset = week - event.week
            if 0 <= offset < event.duration_weeks:
                # Triangular pulse: rises then fades.
                shape = 1.0 - abs(offset - event.duration_weeks / 2) / (
                    event.duration_weeks / 2
                )
                boost = max(boost, event.magnitude * shape)
        return boost

    def _maybe_relapse(self, week: int, relapses: List[RelapseEvent]) -> None:
        acute_phase = week < 8
        if acute_phase or self._rng.random() >= self.profile.relapse_hazard:
            return
        relapses.append(
            RelapseEvent(
                week=week,
                magnitude=self._rng.uniform(0.35, 0.7),
                duration_weeks=self._rng.randint(4, 8),
            )
        )

    def _project_domain(
        self, baseline: Mapping[str, int], domain: str, week: int, boost: float
    ) -> Dict[str, int]:
        effect = self.profile.effect_at(week, domain)
        projected = {}
        for code, score in baseline.items():
            excess = score - SCALE_MIN
            remaining = excess * (1.0 - effect)
            remaining += excess * boost * (1.0 if domain == "positive" else 0.5)
            value = SCALE_MIN + remaining + self._rng.gauss(0.0, self.noise_sd)
            projected[code] = int(max(SCALE_MIN, min(SCALE_MAX, round(value))))
        return projected

    def run(self) -> TrajectoryResult:
        relapses: List[RelapseEvent] = []
        assessments: List[PANSSAssessment] = [self.baseline]
        for week in range(1, self.weeks + 1):
            self._maybe_relapse(week, relapses)
            boost = self._relapse_boost(week, relapses)
            assessments.append(
                PANSSAssessment(
                    positive=self._project_domain(
                        self.baseline.positive, "positive", week, boost
                    ),
                    negative=self._project_domain(
                        self.baseline.negative, "negative", week, boost
                    ),
                    general=self._project_domain(
                        self.baseline.general, "general", week, boost
                    ),
                    week=week,
                )
            )
        return TrajectoryResult(self.profile, self.baseline, assessments, relapses)


# --------------------------------------------------------------------------- #
# Clinical metrics
# --------------------------------------------------------------------------- #


def percent_reduction(baseline: PANSSAssessment, current: PANSSAssessment) -> float:
    """Percentage reduction of the adjusted PANSS total (total - 30)."""
    denominator = baseline.total - 30
    if denominator <= 0:
        return 0.0
    return 100.0 * (baseline.total - current.total) / denominator


def response_status(reduction: float) -> Dict[str, object]:
    return {
        "percent_reduction": round(reduction, 1),
        "responder_20": reduction >= RESPONSE_MINIMAL,
        "responder_50": reduction >= RESPONSE_MUCH_IMPROVED,
        "label_he": (
            "שיפור ניכר"
            if reduction >= RESPONSE_MUCH_IMPROVED
            else "תגובה מינימלית"
            if reduction >= RESPONSE_MINIMAL
            else "ללא תגובה"
        ),
    }


def remission_status(result: TrajectoryResult) -> Dict[str, object]:
    """Andreasen criteria: symptom threshold sustained for 26 weeks."""
    flags = [a.meets_remission_threshold() for a in result.assessments]
    longest = current = 0
    for flag in flags:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    sustained = current >= REMISSION_DURATION_WEEKS
    return {
        "symptomatic_at_endpoint": flags[-1],
        "consecutive_weeks_at_endpoint": current,
        "longest_streak_weeks": longest,
        "sustained_remission": sustained,
        "required_weeks": REMISSION_DURATION_WEEKS,
        "label_he": (
            "רמיסיה מלאה"
            if sustained
            else "סף תסמיני מושג (משך לא מספק)"
            if flags[-1]
            else "ללא רמיסיה"
        ),
    }


def dominant_dimension(assessment: PANSSAssessment) -> Dict[str, str]:
    composite = assessment.composite_index
    if composite >= 3:
        return {"key": "positive", "label_he": "תמונה חיובית-דומיננטית"}
    if composite <= -3:
        return {"key": "negative", "label_he": "תמונה שלילית-דומיננטית"}
    return {"key": "mixed", "label_he": "תמונה מעורבת"}


def algorithmic_assessment(result: TrajectoryResult) -> Dict[str, object]:
    """Rule-based clinical summary of a simulated trajectory.

    The rules mirror the decision logic a clinician applies at a review
    visit: severity band, treatment response, remission, dominant dimension,
    and flags that suggest a treatment adjustment.
    """
    baseline, endpoint = result.baseline, result.endpoint
    reduction = percent_reduction(baseline, endpoint)
    response = response_status(reduction)
    remission = remission_status(result)
    severity = endpoint.severity()
    dimension = dominant_dimension(endpoint)

    flags: List[Dict[str, str]] = []
    if not response["responder_20"]:
        flags.append(
            {
                "code": "non_response",
                "label_he": "העדר תגובה לאחר תקופת ניסיון – לשקול החלפת טיפול",
            }
        )
    if endpoint.negative_total >= 24:
        flags.append(
            {
                "code": "persistent_negative",
                "label_he": "תסמינים שליליים מתמשכים – לשקול שיקום קוגניטיבי",
            }
        )
    if len(result.relapses) >= 2:
        flags.append(
            {
                "code": "recurrent_relapse",
                "label_he": "הישנויות חוזרות – לבדוק היענות / טיפול בזריקה",
            }
        )
    if endpoint.item("G6") >= 4:
        flags.append(
            {
                "code": "depressive_symptoms",
                "label_he": "תסמיני דיכאון – הערכת סיכון אובדני",
            }
        )
    if not flags:
        flags.append({"code": "stable", "label_he": "מהלך יציב – המשך מעקב"})

    return {
        "severity": severity,
        "response": response,
        "remission": remission,
        "dominant_dimension": dimension,
        "relapse_count": len(result.relapses),
        "flags": flags,
    }


# --------------------------------------------------------------------------- #
# Scenario orchestration & export
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Scenario:
    key: str
    name: str
    name_he: str
    profile: TreatmentProfile
    baseline_means: Mapping[str, float]


DEFAULT_SCENARIOS: Sequence[Scenario] = (
    Scenario(
        key="first_episode_sga",
        name="First-episode psychosis, SGA monotherapy",
        name_he="אפיזודה ראשונה – דור שני בלבד",
        profile=DEFAULT_PROFILES["sga"],
        baseline_means={"positive": 4.8, "negative": 3.6, "general": 3.5},
    ),
    Scenario(
        key="chronic_fga",
        name="Chronic course, FGA monotherapy",
        name_he="מהלך כרוני – דור ראשון בלבד",
        profile=DEFAULT_PROFILES["fga"],
        baseline_means={"positive": 4.4, "negative": 4.6, "general": 3.8},
    ),
    Scenario(
        key="integrated_care",
        name="Integrated care: SGA + CBTp + family intervention",
        name_he="טיפול משולב – תרופה, CBTp ומשפחה",
        profile=DEFAULT_PROFILES["sga_plus_cbtp"],
        baseline_means={"positive": 4.7, "negative": 4.0, "general": 3.6},
    ),
)


def run_scenario(scenario: Scenario, weeks: int, seed: int) -> TrajectoryResult:
    rng = random.Random(seed)
    baseline = generate_baseline(
        rng,
        positive_mean=scenario.baseline_means["positive"],
        negative_mean=scenario.baseline_means["negative"],
        general_mean=scenario.baseline_means["general"],
    )
    simulator = TrajectorySimulator(baseline, scenario.profile, weeks, seed=seed + 1)
    return simulator.run()


def _domain_breakdown(assessment: PANSSAssessment) -> Dict[str, int]:
    return {
        "positive": assessment.positive_total,
        "negative": assessment.negative_total,
        "general": assessment.general_total,
        "total": assessment.total,
    }


def build_metrics(
    scenarios: Sequence[Scenario] = DEFAULT_SCENARIOS,
    weeks: int = 52,
    seed: int = 22,
) -> Dict[str, object]:
    """Run every scenario and assemble the JSON document for the front end."""
    exported = []
    for index, scenario in enumerate(scenarios):
        result = run_scenario(scenario, weeks, seed + index * 101)
        exported.append(
            {
                "key": scenario.key,
                "name": scenario.name,
                "name_he": scenario.name_he,
                "treatment": {
                    "key": result.profile.key,
                    "name": result.profile.name,
                    "name_he": result.profile.name_he,
                    "drug_class": result.profile.drug_class,
                    "efficacy": dict(result.profile.efficacy),
                    "adherence": result.profile.adherence,
                },
                "baseline": {
                    **_domain_breakdown(result.baseline),
                    "severity": result.baseline.severity(),
                    "items": {
                        **result.baseline.positive,
                        **result.baseline.negative,
                        **result.baseline.general,
                    },
                },
                "endpoint": {
                    **_domain_breakdown(result.endpoint),
                    "severity": result.endpoint.severity(),
                },
                "trajectory": [a.to_dict() for a in result.assessments],
                "relapses": [
                    {"week": r.week, "magnitude": round(r.magnitude, 2),
                     "duration_weeks": r.duration_weeks}
                    for r in result.relapses
                ],
                "assessment": algorithmic_assessment(result),
            }
        )

    return {
        "meta": {
            "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "generator": "schizophrenia_analysis.py",
            "weeks": weeks,
            "seed": seed,
            "disclaimer_he": (
                "נתונים סינתטיים להמחשה אקדמית בלבד – אינם מייצגים מטופלים "
                "אמיתיים ואינם כלי קליני."
            ),
            "scale": {
                "name": "PANSS",
                "items": 30,
                "item_range": [SCALE_MIN, SCALE_MAX],
                "total_range": [30 * SCALE_MIN, 30 * SCALE_MAX],
                "domains": {
                    "positive": len(POSITIVE_ITEMS),
                    "negative": len(NEGATIVE_ITEMS),
                    "general": len(GENERAL_ITEMS),
                },
                "domain_labels_he": dict(DOMAIN_LABELS_HE),
                "item_labels_en": {**POSITIVE_ITEMS, **NEGATIVE_ITEMS, **GENERAL_ITEMS},
                "item_labels_he": dict(ITEM_LABELS_HE),
            },
            "thresholds": {
                "response_minimal_pct": RESPONSE_MINIMAL,
                "response_much_improved_pct": RESPONSE_MUCH_IMPROVED,
                "remission_items": list(REMISSION_ITEMS),
                "remission_item_max": REMISSION_ITEM_MAX,
                "remission_duration_weeks": REMISSION_DURATION_WEEKS,
                "severity_bands": [
                    {"upper_exclusive": None if math.isinf(u) else u,
                     "key": k, "label_he": h}
                    for u, k, h in SEVERITY_BANDS
                ],
            },
            "references": [
                "Kay, S. R., Fiszbein, A., & Opler, L. A. (1987). Schizophrenia "
                "Bulletin, 13(2), 261-276.",
                "Leucht, S., et al. (2005). Neuropsychopharmacology, 30, 2318-2325.",
                "Andreasen, N. C., et al. (2005). American Journal of Psychiatry, "
                "162(3), 441-449.",
                "Leucht, S., et al. (2009). Neuropsychopharmacology, 34, 2318-2325.",
            ],
        },
        "scenarios": exported,
    }
