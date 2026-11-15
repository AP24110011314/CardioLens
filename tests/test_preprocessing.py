"""Tests for src/preprocessing.py"""

from __future__ import annotations

import pandas as pd
import pytest

from src.config import ENCODINGS, FEATURE_ORDER
from src.preprocessing import build_frame, encode_value, decode_value, impute_cholesterol


class TestEncodeValue:
    """Verify that encoding maps produce the expected integers."""

    def test_sex_male(self) -> None:
        assert encode_value("Sex", "Male") == 1

    def test_sex_female(self) -> None:
        assert encode_value("Sex", "Female") == 0

    def test_chest_pain_ta(self) -> None:
        assert encode_value("ChestPainType", "Typical angina") == 0

    def test_chest_pain_ata(self) -> None:
        assert encode_value("ChestPainType", "Atypical angina") == 1

    def test_chest_pain_nap(self) -> None:
        assert encode_value("ChestPainType", "Non-anginal pain") == 2

    def test_chest_pain_asy(self) -> None:
        assert encode_value("ChestPainType", "No symptoms (asymptomatic)") == 3

    def test_resting_ecg_lvh(self) -> None:
        assert encode_value("RestingECG", "Left ventricular hypertrophy") == 0

    def test_resting_ecg_normal(self) -> None:
        assert encode_value("RestingECG", "Normal") == 1

    def test_resting_ecg_st(self) -> None:
        assert encode_value("RestingECG", "ST-T wave abnormality") == 2

    def test_st_slope_down(self) -> None:
        assert encode_value("ST_Slope", "Downsloping") == 0

    def test_st_slope_flat(self) -> None:
        assert encode_value("ST_Slope", "Flat") == 1

    def test_st_slope_up(self) -> None:
        assert encode_value("ST_Slope", "Upsloping") == 2

    def test_exercise_angina_yes(self) -> None:
        assert encode_value("ExerciseAngina", "Yes") == 1

    def test_exercise_angina_no(self) -> None:
        assert encode_value("ExerciseAngina", "No") == 0

    def test_fasting_bs_low(self) -> None:
        assert encode_value("FastingBS", "≤ 120 mg/dL") == 0

    def test_fasting_bs_high(self) -> None:
        assert encode_value("FastingBS", "> 120 mg/dL") == 1

    def test_unknown_feature_raises(self) -> None:
        with pytest.raises(ValueError, match="No encoding map"):
            encode_value("FakeFeature", "anything")

    def test_unknown_label_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown label"):
            encode_value("Sex", "Other")


class TestDecodeValue:
    """Verify decoding from int back to label."""

    def test_sex_1_to_male(self) -> None:
        assert decode_value("Sex", 1) == "Male"

    def test_sex_0_to_female(self) -> None:
        assert decode_value("Sex", 0) == "Female"


class TestBuildFrame:
    """Test that build_frame produces a correct DataFrame."""

    @pytest.fixture
    def sample_inputs(self) -> dict:
        return {
            "Age": 50,
            "Sex": "Male",
            "ChestPainType": "No symptoms (asymptomatic)",
            "RestingBP": 130,
            "Cholesterol": 250,
            "FastingBS": "≤ 120 mg/dL",
            "RestingECG": "Normal",
            "MaxHR": 160,
            "ExerciseAngina": "No",
            "Oldpeak": 1.5,
            "ST_Slope": "Flat",
        }

    def test_column_order(self, sample_inputs: dict) -> None:
        df = build_frame(sample_inputs)
        assert list(df.columns) == FEATURE_ORDER

    def test_single_row(self, sample_inputs: dict) -> None:
        df = build_frame(sample_inputs)
        assert len(df) == 1

    def test_sex_encoded(self, sample_inputs: dict) -> None:
        df = build_frame(sample_inputs)
        assert df["Sex"].iloc[0] == 1

    def test_chest_pain_encoded(self, sample_inputs: dict) -> None:
        df = build_frame(sample_inputs)
        assert df["ChestPainType"].iloc[0] == 3  # ASY

    def test_numeric_passthrough(self, sample_inputs: dict) -> None:
        df = build_frame(sample_inputs)
        assert df["Age"].iloc[0] == 50
        assert df["RestingBP"].iloc[0] == 130
        assert df["Cholesterol"].iloc[0] == 250


class TestImputeCholesterol:
    """Test cholesterol imputation."""

    def test_zero_is_imputed(self) -> None:
        df = pd.DataFrame({"Cholesterol": [0], "Age": [50]})
        result = impute_cholesterol(df)
        assert result["Cholesterol"].iloc[0] > 0  # Should be median, not 0

    def test_nonzero_unchanged(self) -> None:
        df = pd.DataFrame({"Cholesterol": [200], "Age": [50]})
        result = impute_cholesterol(df)
        assert result["Cholesterol"].iloc[0] == 200
