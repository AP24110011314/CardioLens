"""Tests for src/explain.py"""

from __future__ import annotations

import pytest

from src.explain import sensitivity_analysis, what_if
from src.predict import predict_single


@pytest.fixture
def sample_inputs() -> dict:
    return {
        "Age": 55,
        "Sex": "Male",
        "ChestPainType": "Typical angina",
        "RestingBP": 140,
        "Cholesterol": 260,
        "FastingBS": "> 120 mg/dL",
        "RestingECG": "Normal",
        "MaxHR": 130,
        "ExerciseAngina": "Yes",
        "Oldpeak": 2.0,
        "ST_Slope": "Flat",
    }


class TestExplain:
    """Verify sensitivity analysis and what-if logic."""

    def test_sensitivity_returns_dataframe(self, sample_inputs: dict) -> None:
        result = predict_single(sample_inputs)
        sens_df = sensitivity_analysis(sample_inputs, result["proba"])
        assert hasattr(sens_df, "columns")
        assert "Feature" in sens_df.columns
        assert "Δ Risk" in sens_df.columns
        assert len(sens_df) > 0

    def test_what_if_calculates_delta(self, sample_inputs: dict) -> None:
        wi = what_if(sample_inputs, {"MaxHR": 180, "Oldpeak": 0.0})
        assert "original_proba" in wi
        assert "modified_proba" in wi
        assert "delta" in wi
        assert isinstance(wi["delta"], float)
        assert wi["delta"] == pytest.approx(wi["modified_proba"] - wi["original_proba"], abs=1e-5)
