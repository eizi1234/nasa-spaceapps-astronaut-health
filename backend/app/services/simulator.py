"""Generator data wearable TIRUAN untuk demo/pengembangan UI.
Tampilkan label 'simulated' di UI dan presentasi.
"""
import numpy as np

from app.schemas import WearableFeatures

SCENARIOS = {
    "normal":           dict(hrv=55, rhr=62, sleep=7.3, debt=0.5, shift=0,   work=8),
    "sleep_deprived":   dict(hrv=32, rhr=74, sleep=4.5, debt=4.0, shift=30,  work=10),
    "chaotic_schedule": dict(hrv=28, rhr=78, sleep=5.0, debt=3.0, shift=180, work=12),
}


def generate(scenario: str = "normal", seed: int | None = None) -> WearableFeatures:
    base = SCENARIOS.get(scenario, SCENARIOS["normal"])
    rng = np.random.default_rng(seed)
    return WearableFeatures(
        hrv_rmssd_ms=round(float(base["hrv"] + rng.normal(0, 2)), 1),
        resting_hr_bpm=round(float(base["rhr"] + rng.normal(0, 1)), 1),
        sleep_hours=round(float(base["sleep"] + rng.normal(0, 0.2)), 1),
        sleep_debt_hours=round(float(max(0, base["debt"] + rng.normal(0, 0.2))), 1),
        schedule_shift_minutes=float(base["shift"]),
        workload_hours=float(base["work"]),
    )
