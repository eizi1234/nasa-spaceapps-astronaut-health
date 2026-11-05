"""Kontrak JSON antara ML -> Backend -> Frontend.
Ubah file ini HANYA setelah disepakati dengan tim ML, lalu samakan
dengan frontend/src/types/astronaut.ts.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ReadinessGate(str, Enum):
    GO = "GO"
    CAUTION = "CAUTION"
    HOLD = "HOLD"


class FeatureImpact(BaseModel):
    name: str
    impact: float = Field(description="Kontribusi ke risiko (SHAP-like). + menaikkan risiko")


class WearableFeatures(BaseModel):
    """Input untuk model. Nama field = kesepakatan dengan tim ML."""
    hrv_rmssd_ms: float = 55
    resting_hr_bpm: float = 62
    sleep_hours: float = 7.0
    sleep_debt_hours: float = 0.5
    schedule_shift_minutes: float = 0  # + = jadwal mundur (delay), - = maju (advance)
    workload_hours: float = 8


class CognitiveStress(BaseModel):
    risk_level: RiskLevel
    risk_score: float = Field(ge=0, le=1)
    readiness_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    top_features: List[FeatureImpact]


class Circadian(BaseModel):
    status: str  # contoh: "ALIGNED", "PHASE_DELAY_1.5H"
    phase_shift_hours: float
    predicted_sleep_hours: float


class PredictionResponse(BaseModel):
    astronaut_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    scenario: str = "custom"
    is_simulated: bool = True
    cognitive_stress: CognitiveStress
    circadian: Circadian
    readiness_gate: ReadinessGate
    recommended_actions: List[str]
