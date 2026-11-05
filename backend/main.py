from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        "message": "Astronaut Cognitive & Circadian Risk API is running"
    }

@app.get("/api/v1/mock-prediction")
def get_mock_prediction():
    return {
        "astronaut_id": "AST-01",
        "cognitive_stress_risk": "MEDIUM",
        "readiness_score": 78.5,
        "circadian_status": "PHASE_DELAY_1.5H",
        "recommended_action": "Reduce EVA preparation workload by 20%"
    }
