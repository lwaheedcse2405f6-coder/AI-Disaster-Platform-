from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ClimateIndicatorInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    value: float
    weight: float = Field(..., ge=0.0, le=1.0)
    unit: str = Field(..., min_length=1, max_length=20)


class AssessmentCreate(BaseModel):
    region: str = Field(..., min_length=2, max_length=120)
    hazard_type: str = Field(..., min_length=2, max_length=100)
    event_severity: float = Field(..., ge=0.0, le=10.0)
    exposure_index: float = Field(..., ge=0.0, le=1.0)
    vulnerability_index: float = Field(..., ge=0.0, le=1.0)
    preparedness_index: float = Field(..., ge=0.0, le=1.0)
    indicators: List[ClimateIndicatorInput] = Field(default_factory=list)


class ImpactBreakdownResponse(BaseModel):
    population_risk: float
    infrastructure_risk: float
    environmental_risk: float
    economic_risk: float


class AssessmentResponse(BaseModel):
    id: str
    region: str
    hazard_type: str
    event_severity: float
    exposure_index: float
    vulnerability_index: float
    preparedness_index: float
    overall_risk_score: float
    impact_score: float
    risk_level: str
    ai_summary: str
    recommended_actions: List[str]
    impact_breakdown: ImpactBreakdownResponse
    created_at: datetime


class IncidentResponse(BaseModel):
    id: str
    title: str
    region: str
    hazard_type: str
    status: str
    affected_population: int
    severity: float
    updated_at: datetime


class DashboardMetricsResponse(BaseModel):
    total_assessments: int
    high_risk_regions: int
    active_incidents: int
    average_risk_score: float
    latest_assessments: List[AssessmentResponse]
    incidents: List[IncidentResponse]
