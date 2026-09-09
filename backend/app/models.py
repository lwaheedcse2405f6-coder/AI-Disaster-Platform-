from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4


@dataclass
class ClimateIndicator:
    name: str
    value: float
    weight: float
    unit: str


@dataclass
class ImpactBreakdown:
    population_risk: float
    infrastructure_risk: float
    environmental_risk: float
    economic_risk: float


@dataclass
class AssessmentRecord:
    region: str
    hazard_type: str
    event_severity: float
    exposure_index: float
    vulnerability_index: float
    preparedness_index: float
    indicators: List[ClimateIndicator] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    overall_risk_score: float = 0.0
    impact_score: float = 0.0
    risk_level: str = "Unknown"
    impact_breakdown: ImpactBreakdown | None = None
    ai_summary: str = ""
    recommended_actions: List[str] = field(default_factory=list)


@dataclass
class IncidentRecord:
    title: str
    region: str
    hazard_type: str
    status: str
    affected_population: int
    severity: float
    updated_at: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid4()))
