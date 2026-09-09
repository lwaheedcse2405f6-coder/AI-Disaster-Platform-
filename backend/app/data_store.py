from __future__ import annotations

from statistics import mean
from typing import List

from .models import AssessmentRecord, ClimateIndicator, IncidentRecord
from .schemas import AssessmentCreate
from .services import score_assessment


class InMemoryStore:
    def __init__(self) -> None:
        self.assessments: List[AssessmentRecord] = []
        self.incidents: List[IncidentRecord] = self._seed_incidents()
        self._seed_assessments()

    def _seed_incidents(self) -> List[IncidentRecord]:
        return [
            IncidentRecord(
                title="Urban Flooding Alert",
                region="Chennai",
                hazard_type="Flood",
                status="Monitoring",
                affected_population=120000,
                severity=7.4,
            ),
            IncidentRecord(
                title="Coastal Cyclone Watch",
                region="Odisha Coast",
                hazard_type="Cyclone",
                status="Preparedness",
                affected_population=85000,
                severity=8.2,
            ),
        ]

    def _seed_assessments(self) -> None:
        starter_records = [
            AssessmentCreate(
                region="Assam",
                hazard_type="Flood",
                event_severity=8.1,
                exposure_index=0.76,
                vulnerability_index=0.69,
                preparedness_index=0.42,
                indicators=[
                    {"name": "Rainfall Anomaly", "value": 82, "weight": 0.4, "unit": "%"},
                    {"name": "River Stress", "value": 74, "weight": 0.35, "unit": "idx"},
                    {"name": "Soil Saturation", "value": 68, "weight": 0.25, "unit": "%"},
                ],
            ),
            AssessmentCreate(
                region="Rajasthan",
                hazard_type="Heatwave",
                event_severity=6.7,
                exposure_index=0.58,
                vulnerability_index=0.49,
                preparedness_index=0.63,
                indicators=[
                    {"name": "Temperature Anomaly", "value": 79, "weight": 0.5, "unit": "%"},
                    {"name": "Water Scarcity", "value": 72, "weight": 0.5, "unit": "idx"},
                ],
            ),
        ]
        for payload in starter_records:
            self.create_assessment(payload)

    def create_assessment(self, payload: AssessmentCreate) -> AssessmentRecord:
        record = AssessmentRecord(
            region=payload.region,
            hazard_type=payload.hazard_type,
            event_severity=payload.event_severity,
            exposure_index=payload.exposure_index,
            vulnerability_index=payload.vulnerability_index,
            preparedness_index=payload.preparedness_index,
            indicators=[ClimateIndicator(**indicator.model_dump()) for indicator in payload.indicators],
        )
        self.assessments.insert(0, score_assessment(record))
        return self.assessments[0]

    def get_assessments(self) -> List[AssessmentRecord]:
        return self.assessments

    def get_incidents(self) -> List[IncidentRecord]:
        return self.incidents

    def get_dashboard_metrics(self) -> dict:
        total = len(self.assessments)
        high_risk = len([item for item in self.assessments if item.risk_level in {"High", "Critical"}])
        avg_risk = round(mean([item.overall_risk_score for item in self.assessments]), 2) if self.assessments else 0.0
        return {
            "total_assessments": total,
            "high_risk_regions": high_risk,
            "active_incidents": len(self.incidents),
            "average_risk_score": avg_risk,
            "latest_assessments": self.assessments[:5],
            "incidents": self.incidents,
        }


store = InMemoryStore()
