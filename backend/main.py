from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PredictionResponse, WearableFeatures
from app.services import rules, simulator
from app.services.ml_service import ml_service

app = FastAPI(title="NASA Space Apps - Astronaut Health API")

# Setup CORS agar Next.js di localhost:3000 bisa mengakses FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Astronaut Cognitive & Circadian Risk API is running",
        "using_real_model": ml_service.using_real_model,
    }


def _build_response(astronaut_id: str, features: WearableFeatures, scenario: str) -> PredictionResponse:
    stress = ml_service.predict_cognitive_risk(features)
    circ = ml_service.predict_circadian(features)
    return PredictionResponse(
        astronaut_id=astronaut_id,
        scenario=scenario,
        is_simulated=True,  # ubah ke False saat memakai data wearable nyata
        cognitive_stress=stress,
        circadian=circ,
        readiness_gate=rules.readiness_gate(stress.readiness_score),
        recommended_actions=rules.recommend(features, stress, circ),
    )


@app.get("/api/v1/mock-prediction", response_model=PredictionResponse)
def get_mock_prediction():
    return _build_response("AST-01", simulator.generate("normal", seed=1), "normal")


@app.get("/api/v1/predict/{astronaut_id}", response_model=PredictionResponse)
def predict(
    astronaut_id: str,
    scenario: str = Query("normal", pattern="^(normal|sleep_deprived|chaotic_schedule)$"),
):
    return _build_response(astronaut_id, simulator.generate(scenario), scenario)


@app.post("/api/v1/predict/{astronaut_id}", response_model=PredictionResponse)
def predict_from_features(astronaut_id: str, features: WearableFeatures):
    """Dipakai nanti untuk data wearable asli / slider what-if dari frontend."""
    return _build_response(astronaut_id, features, "custom")
