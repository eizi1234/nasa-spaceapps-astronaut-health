"""Aturan sederhana (tanpa ML): readiness gate + rekomendasi tindakan."""
from typing import List

from app.schemas import Circadian, CognitiveStress, ReadinessGate, WearableFeatures


def readiness_gate(readiness_score: float) -> ReadinessGate:
    if readiness_score >= 70:
        return ReadinessGate.GO
    if readiness_score >= 40:
        return ReadinessGate.CAUTION
    return ReadinessGate.HOLD


def recommend(f: WearableFeatures, stress: CognitiveStress, circ: Circadian) -> List[str]:
    actions: List[str] = []
    if f.sleep_debt_hours > 2:
        actions.append(f"Sleep debt {f.sleep_debt_hours:.1f} jam: jadwalkan tidur pemulihan 60-90 menit lebih awal.")
    if abs(circ.phase_shift_hours) >= 1:
        arah = "mundur" if circ.phase_shift_hours > 0 else "maju"
        actions.append(f"Ritme sirkadian bergeser {arah} {abs(circ.phase_shift_hours):.1f} jam: geser jadwal tidur bertahap 30 menit/hari dan atur pencahayaan.")
    if f.workload_hours > 10:
        actions.append("Beban kerja tinggi: kurangi persiapan EVA/tugas kritis ~20% atau bagi ke anggota kru lain.")
    if stress.risk_level.value == "HIGH":
        actions.append("Tunda aktivitas kritis sampai readiness membaik dan konsultasikan dengan flight surgeon.")
    return actions or ["Kondisi stabil: pertahankan rutinitas saat ini."]
