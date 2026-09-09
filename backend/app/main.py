from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .data_store import store
from .schemas import (
    AssessmentCreate,
    AssessmentResponse,
    DashboardMetricsResponse,
    ImpactBreakdownResponse,
    IncidentResponse,
)

app = FastAPI(
    title="Climate Risk and Disaster Impact Assessment API",
    version="0.1.0",
    description="Backend API for AI-enabled climate risk scoring and disaster impact assessment.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    return {
        "message": "Climate Risk and Disaster Impact Assessment API is running.",
        "health": "/health",
        "dashboard": "/api/dashboard",
        "docs": "/docs",
    }


def _map_assessment(item) -> AssessmentResponse:
    return AssessmentResponse(
        id=item.id,
        region=item.region,
        hazard_type=item.hazard_type,
        event_severity=item.event_severity,
        exposure_index=item.exposure_index,
        vulnerability_index=item.vulnerability_index,
        preparedness_index=item.preparedness_index,
        overall_risk_score=item.overall_risk_score,
        impact_score=item.impact_score,
        risk_level=item.risk_level,
        ai_summary=item.ai_summary,
        recommended_actions=item.recommended_actions,
        impact_breakdown=ImpactBreakdownResponse(**asdict(item.impact_breakdown)),
        created_at=item.created_at,
    )


def _map_incident(item) -> IncidentResponse:
    return IncidentResponse(
        id=item.id,
        title=item.title,
        region=item.region,
        hazard_type=item.hazard_type,
        status=item.status,
        affected_population=item.affected_population,
        severity=item.severity,
        updated_at=item.updated_at,
    )


@app.get("/api/assessments", response_model=list[AssessmentResponse])
def list_assessments() -> list[AssessmentResponse]:
    return [_map_assessment(item) for item in store.get_assessments()]


@app.post("/api/assessments", response_model=AssessmentResponse, status_code=201)
def create_assessment(payload: AssessmentCreate) -> AssessmentResponse:
    return _map_assessment(store.create_assessment(payload))


@app.get("/api/incidents", response_model=list[IncidentResponse])
def list_incidents() -> list[IncidentResponse]:
    return [_map_incident(item) for item in store.get_incidents()]


@app.get("/api/dashboard", response_model=DashboardMetricsResponse)
def get_dashboard() -> DashboardMetricsResponse:
    metrics = store.get_dashboard_metrics()
    return DashboardMetricsResponse(
        total_assessments=metrics["total_assessments"],
        high_risk_regions=metrics["high_risk_regions"],
        active_incidents=metrics["active_incidents"],
        average_risk_score=metrics["average_risk_score"],
        latest_assessments=[_map_assessment(item) for item in metrics["latest_assessments"]],
        incidents=[_map_incident(item) for item in metrics["incidents"]],
    )
