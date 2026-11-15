"""CardioLens — Explainability: sensitivity, what-if, neighbours.

Provides key-factor analysis, what-if comparisons, and similar-patient lookup.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config import DECODINGS, ENCODINGS, FEATURE_ORDER, FEATURES, REFERENCE_VALUES
from src.model_loader import load_artifacts, load_reference_data
from src.predict import predict_single


def sensitivity_analysis(
    inputs: dict[str, Any],
    base_proba: float,
) -> pd.DataFrame:
    """One-at-a-time sensitivity: swap each input with a reference value.

    Returns a DataFrame sorted by absolute change descending, with columns:
        Feature, Reference_Value, Delta, Direction
    """
    rows: list[dict[str, Any]] = []
    for feature in FEATURE_ORDER:
        ref_value = REFERENCE_VALUES.get(feature)
        if ref_value is None or inputs.get(feature) == ref_value:
            continue

        modified = dict(inputs)
        modified[feature] = ref_value
        result = predict_single(modified)
        delta = result["proba"] - base_proba

        feature_label = FEATURES.get(feature, {}).get("label", feature)
        rows.append({
            "Feature": feature_label,
            "Your value": _display_value(feature, inputs[feature]),
            "Reference value": _display_value(feature, ref_value),
            "Δ Risk": round(delta, 4),
            "Direction": "↓ lower risk" if delta < 0 else "↑ higher risk",
        })

    df = pd.DataFrame(rows)
    if len(df) > 0:
        df = df.sort_values("Δ Risk", key=abs, ascending=False).reset_index(drop=True)
    return df


def _display_value(feature: str, value: Any) -> str:
    """Convert a value to its display string."""
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def what_if(
    inputs: dict[str, Any],
    changes: dict[str, Any],
) -> dict[str, Any]:
    """Predict with one or more input changes applied.

    Parameters
    ----------
    inputs : dict  — original inputs
    changes : dict — feature name → new value overrides

    Returns
    -------
    dict with original result, modified result, and delta.
    """
    original = predict_single(inputs)
    modified_inputs = {**inputs, **changes}
    modified = predict_single(modified_inputs)

    return {
        "original_proba": original["proba"],
        "modified_proba": modified["proba"],
        "delta": modified["proba"] - original["proba"],
        "original_band": original["band"],
        "modified_band": modified["band"],
    }


def find_neighbours(
    inputs: dict[str, Any],
    k: int = 5,
) -> pd.DataFrame | None:
    """Find the k nearest neighbours in the reference dataset.

    Uses the model's kneighbors method on the scaled input.
    Requires data/heart_reference.csv.

    Returns a DataFrame of the k nearest reference rows with their
    true outcome and distance, or None if reference data is unavailable.
    """
    ref_df = load_reference_data()
    if ref_df is None:
        return None

    model, scaler, model_columns, scaler_columns = load_artifacts()

    from src.preprocessing import build_and_prepare, build_frame, prepare

    # Prepare the user input
    user_prepared = build_and_prepare(inputs, model_columns, scaler, scaler_columns)

    # Prepare the reference dataset
    ref_features = ref_df[model_columns].copy()
    # Impute cholesterol in reference data
    from src.model_loader import get_cholesterol_median
    chol_median = get_cholesterol_median()
    ref_features["Cholesterol"] = ref_features["Cholesterol"].replace(0, chol_median)
    ref_features[scaler_columns] = scaler.transform(ref_features[scaler_columns])

    # Find nearest neighbours
    distances, indices = model.kneighbors(user_prepared, n_neighbors=min(k, len(ref_features)))

    neighbour_rows = ref_df.iloc[indices[0]].copy()
    neighbour_rows = neighbour_rows.reset_index(drop=True)
    neighbour_rows["Distance"] = np.round(distances[0], 4)

    # Decode categorical columns for display
    for col in ENCODINGS:
        if col in neighbour_rows.columns and col in DECODINGS:
            neighbour_rows[col] = neighbour_rows[col].map(
                lambda x, c=col: DECODINGS[c].get(int(x), str(x))
            )

    # Rename HeartDisease for clarity
    if "HeartDisease" in neighbour_rows.columns:
        neighbour_rows["HeartDisease"] = neighbour_rows["HeartDisease"].map(
            {0: "No", 1: "Yes"}
        )

    return neighbour_rows
