"""Tests for src/model_loader.py"""

from __future__ import annotations

from src.model_loader import (
    get_cholesterol_median,
    load_artifacts,
    load_columns,
    load_model,
    load_model_metrics,
    load_reference_data,
    load_scaler,
)
from src.config import CHOLESTEROL_MEDIAN_FALLBACK


class TestModelLoader:
    """Verify artefact loading."""

    def test_load_artifacts(self) -> None:
        model, scaler, model_columns, scaler_columns = load_artifacts()
        assert model is not None
        assert scaler is not None
        assert len(model_columns) == 11
        assert len(scaler_columns) == 4
        assert "Age" in model_columns
        assert "BMI" not in model_columns

    def test_load_columns(self) -> None:
        cols = load_columns()
        assert isinstance(cols, list)
        assert len(cols) == 11

    def test_cholesterol_median_fallback(self) -> None:
        # If no data files exist, should return fallback
        med = get_cholesterol_median()
        assert isinstance(med, float)
        assert med > 0

    def test_graceful_missing_data(self) -> None:
        # Reference data and metrics degrade gracefully to None
        ref = load_reference_data()
        metrics = load_model_metrics()
        # Either None or DataFrame/dict if files exist
        assert ref is None or hasattr(ref, "columns")
        assert metrics is None or isinstance(metrics, dict)
