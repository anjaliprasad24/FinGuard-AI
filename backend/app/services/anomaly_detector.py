"""Anomaly Detector using Z-Score and Isolation Forest."""

import numpy as np
from typing import List, Dict, Any, Tuple
try:
    from sklearn.ensemble import IsolationForest
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class AnomalyDetector:
    """Detects statistical financial anomalies using Z-score and Isolation Forest."""

    @classmethod
    def evaluate(
        cls,
        amount: float,
        historical_amounts: List[float]
    ) -> Tuple[bool, str, float, Dict[str, Any]]:
        """
        Returns:
            flagged (bool)
            risk_level ("LOW", "MEDIUM", "HIGH", "CRITICAL")
            anomaly_score (float 0.0 - 1.0)
            evidence_payload (dict)
        """
        if not historical_amounts or len(historical_amounts) < 3:
            # Baseline benchmark fallback when historical sample size is small
            historical_amounts = historical_amounts or [500.0, 1000.0, 1500.0, 2000.0]

        data = np.array(historical_amounts, dtype=float)
        mean_val = float(np.mean(data))
        std_val = float(np.std(data))

        if std_val < 1e-5:
            std_val = 1.0  # Prevent zero division

        z_score = (amount - mean_val) / std_val

        # Isolation Forest check
        iso_score = 0.0
        if HAS_SKLEARN and len(data) >= 4:
            X = data.reshape(-1, 1)
            clf = IsolationForest(contamination=0.1, random_state=42)
            clf.fit(X)
            # decision_function: lower = more anomalous
            raw_decision = clf.decision_function([[amount]])[0]
            iso_score = float(-raw_decision)
        else:
            iso_score = max(0.0, (z_score - 1.5) / 5.0)

        # Risk classification logic
        flagged = False
        risk_level = "LOW"
        
        if z_score >= 3.0 or iso_score > 0.35:
            flagged = True
            if z_score >= 5.0 or iso_score > 0.5:
                risk_level = "CRITICAL"
            else:
                risk_level = "HIGH"
        elif z_score >= 2.0 or iso_score > 0.2:
            risk_level = "MEDIUM"

        normalized_anomaly_score = round(min(1.0, max(0.0, (z_score / 6.0) if z_score > 0 else 0.0)), 4)

        evidence_payload = {
            "amount": float(amount),
            "historical_mean": round(mean_val, 2),
            "std_dev": round(std_val, 2),
            "z_score": round(float(z_score), 2),
            "anomaly_score": normalized_anomaly_score,
            "isolation_forest_raw_score": round(iso_score, 4),
            "flagged": flagged,
            "sample_size": len(historical_amounts)
        }

        return flagged, risk_level, normalized_anomaly_score, evidence_payload
