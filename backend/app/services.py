from __future__ import annotations

from typing import Iterable, List

from .models import AssessmentRecord, ClimateIndicator, ImpactBreakdown


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def compute_indicator_pressure(indicators: Iterable[ClimateIndicator]) -> float:
    weighted_total = sum(item.value * item.weight for item in indicators)
    total_weight = sum(item.weight for item in indicators)
    if total_weight == 0:
        return 0.0
    normalized = weighted_total / total_weight
    return clamp(normalized / 100.0, 0.0, 1.0)


def classify_risk(score: float) -> str:
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Moderate"
    return "Low"


def generate_actions(hazard_type: str, risk_level: str) -> List[str]:
    base_actions = [
        "Strengthen early warning communication across vulnerable communities.",
        "Prioritize shelters, evacuation routes, and backup power for essential services.",
        "Coordinate local agencies around a shared response and recovery checklist.",
    ]
    hazard_specific = {
        "flood": "Inspect drainage, river embankments, and low-lying settlements for pre-event mitigation.",
        "cyclone": "Pre-position emergency supplies and reinforce coastal evacuation logistics.",
        "heatwave": "Expand cooling centers, medical support, and water distribution coverage.",
        "wildfire": "Create defensible space near settlements and stage fire suppression equipment.",
        "drought": "Protect water storage assets and prepare agricultural relief support.",
    }
    if risk_level in {"High", "Critical"}:
        base_actions.insert(0, "Trigger high-alert coordination and accelerate district-level readiness reviews.")
    action = hazard_specific.get(hazard_type.lower(), "Review hazard-specific contingency plans with field teams.")
    return [action, *base_actions]


def build_summary(record: AssessmentRecord) -> str:
    return (
        f"{record.region} shows a {record.risk_level.lower()} climate disaster profile for "
        f"{record.hazard_type}. The combined risk score is {record.overall_risk_score:.1f}/100 "
        f"with impact pressure estimated at {record.impact_score:.1f}/100. "
        f"Exposure and vulnerability remain the strongest drivers, while preparedness "
        f"{'helps reduce downstream losses' if record.preparedness_index >= 0.5 else 'needs urgent improvement'}."
    )


def score_assessment(record: AssessmentRecord) -> AssessmentRecord:
    indicator_pressure = compute_indicator_pressure(record.indicators)
    hazard_index = clamp(((record.event_severity / 10.0) * 0.6) + (indicator_pressure * 0.4), 0.0, 1.0)
    exposure_index = clamp(record.exposure_index, 0.0, 1.0)
    vulnerability_index = clamp(record.vulnerability_index, 0.0, 1.0)
    preparedness_gap = clamp(1 - record.preparedness_index, 0.0, 1.0)

    # Academic-style composite formulation based on hazard, exposure, vulnerability, and capacity.
    risk_score = (
        (hazard_index * 0.30)
        + (exposure_index * 0.25)
        + (vulnerability_index * 0.25)
        + (preparedness_gap * 0.20)
    ) * 100

    impact_score = (
        (exposure_index * 0.35)
        + (vulnerability_index * 0.30)
        + (hazard_index * 0.20)
        + (preparedness_gap * 0.15)
    ) * 100

    record.overall_risk_score = round(clamp(risk_score, 0.0, 100.0), 2)
    record.impact_score = round(clamp(impact_score, 0.0, 100.0), 2)
    record.risk_level = classify_risk(record.overall_risk_score)
    record.impact_breakdown = ImpactBreakdown(
        population_risk=round(clamp((exposure_index * 0.5 + vulnerability_index * 0.5) * 100, 0.0, 100.0), 2),
        infrastructure_risk=round(clamp((hazard_index * 0.55 + exposure_index * 0.45) * 100, 0.0, 100.0), 2),
        environmental_risk=round(clamp((hazard_index * 0.6 + indicator_pressure * 0.4) * 100, 0.0, 100.0), 2),
        economic_risk=round(clamp((exposure_index * 0.4 + vulnerability_index * 0.3 + preparedness_gap * 0.3) * 100, 0.0, 100.0), 2),
    )
    record.recommended_actions = generate_actions(record.hazard_type, record.risk_level)
    record.ai_summary = build_summary(record)
    return record
