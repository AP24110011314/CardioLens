"""CardioLens — Central configuration.

All encoding maps, feature specs, ranges, labels, and risk bands live here.
Nothing else in the codebase should hardcode these values.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Encoding maps — must match the Colab training LabelEncoder / manual maps
# ---------------------------------------------------------------------------

ENCODINGS: dict[str, dict[str, int]] = {
    "Sex": {"Male": 1, "Female": 0},
    "ChestPainType": {
        "Typical angina": 0,       # TA
        "Atypical angina": 1,      # ATA
        "Non-anginal pain": 2,     # NAP
        "No symptoms (asymptomatic)": 3,  # ASY
    },
    "RestingECG": {
        "Left ventricular hypertrophy": 0,  # LVH
        "Normal": 1,
        "ST-T wave abnormality": 2,         # ST
    },
    "ST_Slope": {
        "Downsloping": 0,   # Down
        "Flat": 1,
        "Upsloping": 2,     # Up
    },
    "ExerciseAngina": {"No": 0, "Yes": 1},
    "FastingBS": {"≤ 120 mg/dL": 0, "> 120 mg/dL": 1},
}

# Reverse maps: internal code → friendly label (for display)
DECODINGS: dict[str, dict[int, str]] = {
    feature: {v: k for k, v in mapping.items()}
    for feature, mapping in ENCODINGS.items()
}

# ---------------------------------------------------------------------------
# Feature specifications — order matches model.feature_names_in_
# ---------------------------------------------------------------------------

FEATURE_ORDER: list[str] = [
    "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol",
    "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak",
    "ST_Slope",
]

# Groups for the input form (section → list of feature names)
FEATURE_GROUPS: dict[str, list[str]] = {
    "Personal": ["Age", "Sex"],
    "Vitals": ["RestingBP", "Cholesterol", "FastingBS", "MaxHR"],
    "Cardiac tests": ["ChestPainType", "RestingECG", "ExerciseAngina", "Oldpeak", "ST_Slope"],
}

# Per-feature metadata
FEATURES: dict[str, dict] = {
    "Age": {
        "label": "Age",
        "type": "slider",
        "min": 18,
        "max": 100,
        "default": 40,
        "help": "Patient's age in years.",
    },
    "Sex": {
        "label": "Sex",
        "type": "select",
        "options": list(ENCODINGS["Sex"].keys()),
        "default": "Male",
        "help": "Biological sex.",
    },
    "ChestPainType": {
        "label": "Chest pain type",
        "type": "select",
        "options": list(ENCODINGS["ChestPainType"].keys()),
        "default": "No symptoms (asymptomatic)",
        "help": "Type of chest pain experienced.",
    },
    "RestingBP": {
        "label": "Resting blood pressure (mm Hg)",
        "type": "number",
        "min": 0,
        "max": 250,
        "default": 120,
        "help": "Systolic blood pressure at rest.",
    },
    "Cholesterol": {
        "label": "Serum cholesterol (mg/dL)",
        "type": "number",
        "min": 0,
        "max": 700,
        "default": 200,
        "help": "Serum cholesterol level. Check 'I don't know' if unavailable.",
        "has_unknown": True,
    },
    "FastingBS": {
        "label": "Fasting blood sugar",
        "type": "select",
        "options": list(ENCODINGS["FastingBS"].keys()),
        "default": "≤ 120 mg/dL",
        "help": "Whether fasting blood sugar is above 120 mg/dL.",
    },
    "RestingECG": {
        "label": "Resting ECG",
        "type": "select",
        "options": list(ENCODINGS["RestingECG"].keys()),
        "default": "Normal",
        "help": "Resting electrocardiogram results.",
    },
    "MaxHR": {
        "label": "Maximum heart rate (bpm)",
        "type": "number",
        "min": 50,
        "max": 220,
        "default": 150,
        "help": "Highest heart rate reached during exercise test.",
    },
    "ExerciseAngina": {
        "label": "Exercise-induced angina",
        "type": "select",
        "options": list(ENCODINGS["ExerciseAngina"].keys()),
        "default": "No",
        "help": "Whether exercise induced chest pain (angina).",
    },
    "Oldpeak": {
        "label": "ST depression (mm)",
        "type": "number",
        "min": -3.0,
        "max": 7.0,
        "default": 1.0,
        "step": 0.1,
        "help": "ST depression induced by exercise relative to rest.",
    },
    "ST_Slope": {
        "label": "ST slope",
        "type": "select",
        "options": list(ENCODINGS["ST_Slope"].keys()),
        "default": "Flat",
        "help": "Slope of the peak exercise ST segment.",
    },
}

# ---------------------------------------------------------------------------
# Risk bands — (upper_bound_exclusive, label, colour hex, message)
# ---------------------------------------------------------------------------

RISK_BANDS: list[tuple[float, str, str, str]] = [
    (
        0.30,
        "Low",
        "#2BB673",
        "Your inputs are similar to patients without heart disease in our reference data.",
    ),
    (
        0.60,
        "Moderate",
        "#F5A524",
        "Some inputs resemble patients with heart disease. Consider a routine check-up.",
    ),
    (
        1.01,
        "High",
        "#E5484D",
        "Your inputs resemble patients with heart disease. Please consult a doctor.",
    ),
]

DISCLAIMER: str = "⚠️ This is an educational estimate, not a medical diagnosis. Always consult a qualified doctor."

# ---------------------------------------------------------------------------
# Cholesterol imputation — training-set median of non-zero values
# Fallback value from the well-known Kaggle Heart Failure dataset.
# Will be overridden by data/model_metrics.json if available.
# ---------------------------------------------------------------------------

CHOLESTEROL_MEDIAN_FALLBACK: float = 223.0

# ---------------------------------------------------------------------------
# Colour tokens (for CSS / Plotly)
# ---------------------------------------------------------------------------

COLORS: dict[str, str] = {
    "primary": "#E5484D",
    "low": "#2BB673",
    "moderate": "#F5A524",
    "high": "#E5484D",
    "surface": "#161B22",
    "muted": "#8B949E",
    "bg": "#0E1117",
    "text": "#E6EDF3",
}

# ---------------------------------------------------------------------------
# Reference healthy/typical values for sensitivity analysis (what-if)
# ---------------------------------------------------------------------------

REFERENCE_VALUES: dict[str, int | float | str] = {
    "Age": 40,
    "Sex": "Male",
    "ChestPainType": "No symptoms (asymptomatic)",
    "RestingBP": 120,
    "Cholesterol": 200,
    "FastingBS": "≤ 120 mg/dL",
    "RestingECG": "Normal",
    "MaxHR": 150,
    "ExerciseAngina": "No",
    "Oldpeak": 0.0,
    "ST_Slope": "Upsloping",
}

# ---------------------------------------------------------------------------
# Model artefact paths (relative to repo root)
# ---------------------------------------------------------------------------

MODEL_DIR: str = "models"
MODEL_PATH: str = f"{MODEL_DIR}/KNN_heart.pkl"
SCALER_PATH: str = f"{MODEL_DIR}/scaler.pkl"
COLUMNS_PATH: str = f"{MODEL_DIR}/columns.pkl"

DATA_DIR: str = "data"
REFERENCE_CSV: str = f"{DATA_DIR}/heart_reference.csv"
METRICS_JSON: str = f"{DATA_DIR}/model_metrics.json"
