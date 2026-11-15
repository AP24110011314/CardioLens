"""CardioLens — Cached model loading.

Loads the KNN model, scaler, and column list once per app session.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import streamlit as st

from src.config import (
    CHOLESTEROL_MEDIAN_FALLBACK,
    COLUMNS_PATH,
    METRICS_JSON,
    MODEL_PATH,
    REFERENCE_CSV,
    SCALER_PATH,
)


@st.cache_resource
def load_model() -> Any:
    """Load the KNN classifier. Cached across sessions."""
    path = Path(MODEL_PATH)
    if not path.exists():
        st.error(f"Model file not found: `{MODEL_PATH}`. Please ensure it exists.")
        st.stop()
    return joblib.load(path)


@st.cache_resource
def load_scaler() -> Any:
    """Load the StandardScaler. Cached across sessions."""
    path = Path(SCALER_PATH)
    if not path.exists():
        st.error(f"Scaler file not found: `{SCALER_PATH}`. Please ensure it exists.")
        st.stop()
    return joblib.load(path)


@st.cache_resource
def load_columns() -> list[str]:
    """Load the column list from training. Cached across sessions."""
    path = Path(COLUMNS_PATH)
    if not path.exists():
        st.error(f"Columns file not found: `{COLUMNS_PATH}`. Please ensure it exists.")
        st.stop()
    return list(joblib.load(path))


def load_artifacts() -> tuple[Any, Any, list[str], list[str]]:
    """Load all model artefacts and return (model, scaler, model_columns, scaler_columns)."""
    model = load_model()
    scaler = load_scaler()
    model_columns = list(model.feature_names_in_)
    scaler_columns = list(scaler.feature_names_in_)
    return model, scaler, model_columns, scaler_columns


@st.cache_data
def load_reference_data() -> pd.DataFrame | None:
    """Load the reference dataset if available."""
    path = Path(REFERENCE_CSV)
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data
def load_model_metrics() -> dict[str, Any] | None:
    """Load model metrics JSON if available."""
    path = Path(METRICS_JSON)
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def get_cholesterol_median() -> float:
    """Return the training-set median of non-zero cholesterol values.

    Tries model_metrics.json first, then heart_reference.csv, then the fallback.
    """
    metrics = load_model_metrics()
    if metrics and "chol_median" in metrics:
        return float(metrics["chol_median"])

    ref = load_reference_data()
    if ref is not None and "Cholesterol" in ref.columns:
        non_zero = ref.loc[ref["Cholesterol"] > 0, "Cholesterol"]
        if len(non_zero) > 0:
            return float(non_zero.median())

    return CHOLESTEROL_MEDIAN_FALLBACK
