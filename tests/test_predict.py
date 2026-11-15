"""Tests for src/predict.py"""

from __future__ import annotations

from src.predict import get_risk_band


class TestGetRiskBand:
    """Verify risk band thresholds."""

    def test_low_at_zero(self) -> None:
        label, _colour, _msg = get_risk_band(0.0)
        assert label == "Low"

    def test_low_at_boundary(self) -> None:
        label, _, _ = get_risk_band(0.29)
        assert label == "Low"

    def test_moderate_at_thirty(self) -> None:
        label, _, _ = get_risk_band(0.30)
        assert label == "Moderate"

    def test_moderate_at_fifty_nine(self) -> None:
        label, _, _ = get_risk_band(0.59)
        assert label == "Moderate"

    def test_high_at_sixty(self) -> None:
        label, _, _ = get_risk_band(0.60)
        assert label == "High"

    def test_high_at_one(self) -> None:
        label, _, _ = get_risk_band(1.0)
        assert label == "High"

    def test_low_colour_is_green(self) -> None:
        _, colour, _ = get_risk_band(0.1)
        assert colour == "#2BB673"

    def test_moderate_colour_is_amber(self) -> None:
        _, colour, _ = get_risk_band(0.45)
        assert colour == "#F5A524"

    def test_high_colour_is_red(self) -> None:
        _, colour, _ = get_risk_band(0.8)
        assert colour == "#E5484D"

    def test_each_band_has_message(self) -> None:
        for proba in [0.1, 0.4, 0.8]:
            _, _, msg = get_risk_band(proba)
            assert len(msg) > 0
