"""CardioLens — Prediction logic.

Wraps model.predict_proba and maps to risk bands.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.config import RISK_BANDS
from src.model_loader import load_artifacts
from src.preprocessing import build_and_prepare


def get_risk_band(probability: float) -> tuple[str, str, str]:
    """Map a probability to (band_label, colour_hex, message).

    Parameters
    ----------
    probability : float
        Probability of heart disease (0.0 – 1.0).

    Returns
    -------
    tuple[str, str, str]
        (label, colour, message) from RISK_BANDS.
    """
    for upper, label, colour, message in RISK_BANDS:
        if probability < upper:
            return label, colour, message
    # Fallback (should not happen)
    _, label, colour, message = RISK_BANDS[-1]
    return label, colour, message


def predict_single(inputs: dict[str, Any]) -> dict[str, Any]:
    """Run prediction for a single set of inputs.

    Parameters
    ----------
    inputs : dict
        Feature name → friendly-label value.

    Returns
    -------
    dict with keys:
        proba : float  — probability of heart disease (0–1)
        label : int    — 0 or 1
        band  : str    — "Low" / "Moderate" / "High"
        colour: str    — hex colour for the band
        message: str   — human-readable summary
    """
    model, scaler, model_columns, scaler_columns = load_artifacts()
    df = build_and_prepare(inputs, model_columns, scaler, scaler_columns)

    proba = float(model.predict_proba(df)[0, 1])
    label = int(model.predict(df)[0])
    band, colour, message = get_risk_band(proba)

    return {
        "proba": proba,
        "label": label,
        "band": band,
        "colour": colour,
        "message": message,
    }


def predict_batch(df_prepared: pd.DataFrame) -> pd.DataFrame:
    """Run prediction on a prepared batch DataFrame.

    Returns a DataFrame with Probability, Label, and Risk_Band columns.
    """
    model, *_ = load_artifacts()
    probas = model.predict_proba(df_prepared)[:, 1]
    labels = model.predict(df_prepared)

    results = pd.DataFrame(
        {
            "Probability": np.round(probas, 4),
            "Label": labels.astype(int),
        }
    )
    results["Risk_Band"] = results["Probability"].apply(lambda p: get_risk_band(p)[0])
    return results
