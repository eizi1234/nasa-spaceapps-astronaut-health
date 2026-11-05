# File ini disiapkan khusus untuk Aneeth yaaaa
# Tempat memuat model LightGBM/XGBoost dan melakukan inferensi
#
# Selama model .pkl belum ada, service memakai HEURISTIK PLACEHOLDER di bawah
# supaya frontend bisa dikembangkan. Aneeth: ganti isi `_heuristic_*` dengan
# model.predict(...) + SHAP, tapi JANGAN ubah bentuk return value-nya.
import os

from app.schemas import (
    Circadian, CognitiveStress, FeatureImpact, RiskLevel, WearableFeatures,
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")


class AstronautMLService:
    def __init__(self):
        self.stress_model = None
        self.circadian_model = None
        # TODO (Aneeth): aktifkan saat file model tersedia
        # import joblib
        # self.stress_model = joblib.load(os.path.join(MODEL_DIR, "lightgbm_stress.pkl"))
        # self.circadian_model = joblib.load(os.path.join(MODEL_DIR, "xgb_circadian.pkl"))

    @property
    def using_real_model(self) -> bool:
        return self.stress_model is not None

    def predict_cognitive_risk(self, f: WearableFeatures) -> CognitiveStress:
        # TODO (Aneeth): if self.stress_model: pakai model + SHAP untuk top_features
        contrib = [
            FeatureImpact(name="sleep_debt_hours", impact=round(0.07 * f.sleep_debt_hours, 3)),
            FeatureImpact(name="hrv_rmssd_ms", impact=round(0.004 * max(0, 50 - f.hrv_rmssd_ms), 3)),
            FeatureImpact(name="resting_hr_bpm", impact=round(0.002 * max(0, f.resting_hr_bpm - 65), 3)),
            FeatureImpact(name="schedule_shift_minutes", impact=round(0.001 * abs(f.schedule_shift_minutes), 3)),
        ]
        risk = min(1.0, max(0.0, 0.2 + sum(c.impact for c in contrib)))
        level = RiskLevel.LOW if risk < 0.35 else RiskLevel.MEDIUM if risk < 0.65 else RiskLevel.HIGH
        return CognitiveStress(
            risk_level=level,
            risk_score=round(risk, 3),
            readiness_score=round((1 - risk) * 100, 1),
            confidence=0.6,  # placeholder
            top_features=sorted(contrib, key=lambda c: c.impact, reverse=True),
        )

    def predict_circadian(self, f: WearableFeatures) -> Circadian:
        # TODO (Aneeth): if self.circadian_model: pakai model time-series/GBM
        shift_h = round(f.schedule_shift_minutes / 60, 1)
        if abs(shift_h) < 0.5:
            status = "ALIGNED"
        else:
            status = f"PHASE_{'DELAY' if shift_h > 0 else 'ADVANCE'}_{abs(shift_h)}H"
        sleep = max(3.0, 7.5 - 0.004 * abs(f.schedule_shift_minutes) - 0.2 * f.sleep_debt_hours)
        return Circadian(status=status, phase_shift_hours=shift_h, predicted_sleep_hours=round(sleep, 1))


ml_service = AstronautMLService()
