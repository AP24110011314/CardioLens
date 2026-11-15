"""CardioLens — Data preprocessing.

Builds, encodes, imputes, and scales a DataFrame for the model.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config import ENCODINGS, FEATURE_ORDER
from src.model_loader import get_cholesterol_median

KAGGLE_ALIASES: dict[str, dict[str, str]] = {
    "Sex": {"M": "Male", "F": "Female"},
    "ChestPainType": {
        "TA": "Typical angina",
        "ATA": "Atypical angina",
        "NAP": "Non-anginal pain",
        "ASY": "No symptoms (asymptomatic)",
    },
    "RestingECG": {
        "LVH": "Left ventricular hypertrophy",
        "Normal": "Normal",
        "ST": "ST-T wave abnormality",
    },
    "ExerciseAngina": {"N": "No", "Y": "Yes"},
    "ST_Slope": {"Down": "Downsloping", "Flat": "Flat", "Up": "Upsloping"},
}


def encode_value(feature: str, label: Any) -> int:
    """Encode a friendly label, Kaggle code, or integer to the integer the model expects.

    Raises ValueError if the label is not found in the encoding map.
    """
    mapping = ENCODINGS.get(feature)
    if mapping is None:
        raise ValueError(f"No encoding map for feature '{feature}'.")

    # If already an integer or integer-like matching valid codes
    try:
        val_int = int(label)
        if val_int in mapping.values():
            return val_int
    except (ValueError, TypeError):
        pass

    # Direct label lookup
    if label in mapping:
        return mapping[label]

    # Check Kaggle aliases
    str_val = str(label).strip()
    alias = KAGGLE_ALIASES.get(feature, {}).get(str_val)
    if alias and alias in mapping:
        return mapping[alias]

    raise ValueError(
        f"Unknown label '{label}' for feature '{feature}'. "
        f"Valid labels: {list(mapping.keys())}"
    )


def decode_value(feature: str, code: int) -> str:
    """Decode an integer code back to the friendly label."""
    from src.config import DECODINGS

    mapping = DECODINGS.get(feature)
    if mapping is None:
        raise ValueError(f"No decoding map for feature '{feature}'.")
    if code not in mapping:
        raise ValueError(f"Unknown code '{code}' for feature '{feature}'.")
    return mapping[code]


def build_frame(inputs: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame from user inputs.

    Parameters
    ----------
    inputs : dict
        Keys are feature names (Age, Sex, …) with friendly-label values
        for categorical features (e.g. "Male", "Typical angina").

    Returns
    -------
    pd.DataFrame
        One row with integer-encoded categoricals, in FEATURE_ORDER.
    """
    row: dict[str, Any] = {}
    for feature in FEATURE_ORDER:
        raw = inputs[feature]
        if feature in ENCODINGS and isinstance(raw, str):
            row[feature] = encode_value(feature, raw)
        else:
            row[feature] = raw

    df = pd.DataFrame([row], columns=FEATURE_ORDER)
    return df


def impute_cholesterol(df: pd.DataFrame) -> pd.DataFrame:
    """Replace Cholesterol == 0 (meaning 'unknown') with the training median."""
    df = df.copy()
    median = get_cholesterol_median()
    df["Cholesterol"] = df["Cholesterol"].replace(0, median)
    return df


def prepare(
    df: pd.DataFrame,
    model_columns: list[str],
    scaler: Any,
    scaler_columns: list[str],
) -> pd.DataFrame:
    """Apply imputation, column selection, and scaling.

    Parameters
    ----------
    df : pd.DataFrame
        Output of build_frame().
    model_columns : list[str]
        model.feature_names_in_ — defines column order.
    scaler : StandardScaler
        Fitted scaler.
    scaler_columns : list[str]
        scaler.feature_names_in_ — columns the scaler was fitted on.

    Returns
    -------
    pd.DataFrame
        Ready for model.predict / model.predict_proba.
    """
    df = impute_cholesterol(df)
    df = df[model_columns].copy()
    df[scaler_columns] = scaler.transform(df[scaler_columns])
    return df


def build_and_prepare(
    inputs: dict[str, Any],
    model_columns: list[str],
    scaler: Any,
    scaler_columns: list[str],
) -> pd.DataFrame:
    """Convenience: build_frame + prepare in one call."""
    df = build_frame(inputs)
    return prepare(df, model_columns, scaler, scaler_columns)


def prepare_batch(
    df: pd.DataFrame,
    model_columns: list[str],
    scaler: Any,
    scaler_columns: list[str],
) -> tuple[pd.DataFrame, list[str]]:
    """Validate and prepare a batch DataFrame for prediction.

    Supports friendly labels, Kaggle shorthand codes, or raw integer codes.
    Returns (prepared_df, errors) where errors is a list of issue descriptions.
    """
    errors: list[str] = []
    df = df.copy()

    # Check required columns
    missing = [c for c in FEATURE_ORDER if c not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return df, errors

    # Encode categorical columns
    for col in ENCODINGS:
        if col in df.columns:
            encoded_vals: list[int] = []
            col_has_err = False
            for idx, val in enumerate(df[col]):
                try:
                    encoded_vals.append(encode_value(col, val))
                except (ValueError, TypeError):
                    errors.append(
                        f"Row {idx + 1}: Invalid value '{val}' in column '{col}'."
                    )
                    col_has_err = True
                    break
            if not col_has_err:
                df[col] = encoded_vals

    # Coerce numeric types
    numeric_cols = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Check for NaN after coercion
    nan_counts = df[FEATURE_ORDER].isna().sum()
    for col, count in nan_counts.items():
        if count > 0:
            errors.append(f"Column '{col}' has {count} invalid/missing value(s).")

    if errors:
        return df, errors

    # Integer-typed columns
    int_cols = [
        "Age",
        "Sex",
        "ChestPainType",
        "RestingBP",
        "Cholesterol",
        "FastingBS",
        "RestingECG",
        "ExerciseAngina",
        "ST_Slope",
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)

    df = impute_cholesterol(df)
    df_prepared = df[model_columns].copy()
    df_prepared[scaler_columns] = scaler.transform(df_prepared[scaler_columns])
    return df_prepared, errors
