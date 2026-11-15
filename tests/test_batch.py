"""Tests for batch CSV validation in src/preprocessing.py"""

from __future__ import annotations

import pandas as pd
import pytest

from src.config import FEATURE_ORDER


class TestBatchValidation:
    """Test batch CSV validation logic."""

    def test_missing_column_detected(self) -> None:
        from src.preprocessing import prepare_batch
        from src.model_loader import load_artifacts

        _, scaler, model_columns, scaler_columns = load_artifacts()
        df = pd.DataFrame({"Age": [50]})  # Missing most columns
        _, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) > 0
        assert any("Missing columns" in e for e in errors)

    def test_valid_single_row(self) -> None:
        from src.preprocessing import prepare_batch
        from src.model_loader import load_artifacts

        _, scaler, model_columns, scaler_columns = load_artifacts()
        row = {
            "Age": [50], "Sex": [1], "ChestPainType": [3],
            "RestingBP": [130], "Cholesterol": [250], "FastingBS": [0],
            "RestingECG": [1], "MaxHR": [160], "ExerciseAngina": [0],
            "Oldpeak": [1.5], "ST_Slope": [1],
        }
        df = pd.DataFrame(row)
        result, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) == 0
        assert len(result) == 1
