"""Unit tests for Anomaly Detector."""

from app.services.anomaly_detector import AnomalyDetector


def test_anomaly_detector_normal():
    history = [100.0, 110.0, 95.0, 105.0, 100.0]
    flagged, risk, score, evidence = AnomalyDetector.evaluate(102.0, history)
    assert not flagged
    assert risk in ["LOW", "MEDIUM"]
    assert evidence["z_score"] < 2.0


def test_anomaly_detector_high_risk():
    history = [100.0, 110.0, 95.0, 105.0, 100.0]
    flagged, risk, score, evidence = AnomalyDetector.evaluate(18499.0, history)
    assert flagged
    assert risk in ["HIGH", "CRITICAL"]
    assert evidence["z_score"] > 3.0
