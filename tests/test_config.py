"""Tests for src/config.py — encoding map consistency."""

from __future__ import annotations

from src.config import DECODINGS, ENCODINGS, FEATURE_ORDER, FEATURES, RISK_BANDS


class TestEncodingMaps:
    """Verify encoding/decoding consistency."""

    def test_all_categorical_features_have_encodings(self) -> None:
        categorical = ["Sex", "ChestPainType", "RestingECG", "ST_Slope", "ExerciseAngina", "FastingBS"]
        for feat in categorical:
            assert feat in ENCODINGS, f"Missing encoding for {feat}"

    def test_decodings_are_inverse(self) -> None:
        for feat, mapping in ENCODINGS.items():
            for label, code in mapping.items():
                assert DECODINGS[feat][code] == label

    def test_feature_order_has_11_features(self) -> None:
        assert len(FEATURE_ORDER) == 11

    def test_all_features_have_specs(self) -> None:
        for feat in FEATURE_ORDER:
            assert feat in FEATURES, f"Missing spec for {feat}"


class TestRiskBands:
    """Verify risk band configuration."""

    def test_bands_cover_full_range(self) -> None:
        upper_bounds = [b[0] for b in RISK_BANDS]
        assert upper_bounds[-1] > 1.0  # Should cover up to and including 1.0

    def test_bands_are_ordered(self) -> None:
        upper_bounds = [b[0] for b in RISK_BANDS]
        assert upper_bounds == sorted(upper_bounds)

    def test_three_bands(self) -> None:
        assert len(RISK_BANDS) == 3
