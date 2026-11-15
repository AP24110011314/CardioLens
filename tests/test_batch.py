"""Tests for batch CSV validation in src/preprocessing.py"""

from __future__ import annotations

import pandas as pd


class TestBatchValidation:
    """Test batch CSV validation logic."""

    def test_missing_column_detected(self) -> None:
        from src.model_loader import load_artifacts
        from src.preprocessing import prepare_batch

        _, scaler, model_columns, scaler_columns = load_artifacts()
        df = pd.DataFrame({"Age": [50]})  # Missing most columns
        _, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) > 0
        assert any("Missing columns" in e for e in errors)

    def test_valid_single_row(self) -> None:
        from src.model_loader import load_artifacts
        from src.preprocessing import prepare_batch

        _, scaler, model_columns, scaler_columns = load_artifacts()
        row = {
            "Age": [50],
            "Sex": [1],
            "ChestPainType": [3],
            "RestingBP": [130],
            "Cholesterol": [250],
            "FastingBS": [0],
            "RestingECG": [1],
            "MaxHR": [160],
            "ExerciseAngina": [0],
            "Oldpeak": [1.5],
            "ST_Slope": [1],
        }
        df = pd.DataFrame(row)
        result, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) == 0
        assert len(result) == 1

    def test_friendly_labels_batch(self) -> None:
        from src.model_loader import load_artifacts
        from src.preprocessing import prepare_batch

        _, scaler, model_columns, scaler_columns = load_artifacts()
        row = {
            "Age": [55],
            "Sex": ["Male"],
            "ChestPainType": ["Typical angina"],
            "RestingBP": [140],
            "Cholesterol": [240],
            "FastingBS": ["≤ 120 mg/dL"],
            "RestingECG": ["Normal"],
            "MaxHR": [150],
            "ExerciseAngina": ["No"],
            "Oldpeak": [1.0],
            "ST_Slope": ["Flat"],
        }
        df = pd.DataFrame(row)
        result, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) == 0
        assert len(result) == 1

    def test_kaggle_aliases_batch(self) -> None:
        from src.model_loader import load_artifacts
        from src.preprocessing import prepare_batch

        _, scaler, model_columns, scaler_columns = load_artifacts()
        row = {
            "Age": [60],
            "Sex": ["F"],
            "ChestPainType": ["ASY"],
            "RestingBP": [135],
            "Cholesterol": [220],
            "FastingBS": [0],
            "RestingECG": ["LVH"],
            "MaxHR": [140],
            "ExerciseAngina": ["Y"],
            "Oldpeak": [2.0],
            "ST_Slope": ["Down"],
        }
        df = pd.DataFrame(row)
        result, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) == 0
        assert len(result) == 1

    def test_invalid_categorical_detected(self) -> None:
        from src.model_loader import load_artifacts
        from src.preprocessing import prepare_batch

        _, scaler, model_columns, scaler_columns = load_artifacts()
        row = {
            "Age": [50],
            "Sex": ["InvalidSex"],
            "ChestPainType": [3],
            "RestingBP": [130],
            "Cholesterol": [250],
            "FastingBS": [0],
            "RestingECG": [1],
            "MaxHR": [160],
            "ExerciseAngina": [0],
            "Oldpeak": [1.5],
            "ST_Slope": [1],
        }
        df = pd.DataFrame(row)
        _, errors = prepare_batch(df, model_columns, scaler, scaler_columns)
        assert len(errors) > 0
        assert any("column 'Sex'" in e for e in errors)
