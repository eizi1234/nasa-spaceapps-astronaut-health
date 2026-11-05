from pydantic import BaseModel
from typing import Literal

class AstronautPredictionResponse(BaseModel):
    astronaut_id: str
    cognitive_stress_risk: Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    readiness_score: float
    circadian_status: str
    recommended_action: str
