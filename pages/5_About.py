"""CardioLens — About page.

Explains each input in plain language, credits, and general health information.
"""

from __future__ import annotations

import streamlit as st

from src.config import FEATURES
from src.ui import render_disclaimer

st.title("About CardioLens")

# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------
st.markdown("""
**CardioLens** is an educational web app that estimates the likelihood of heart disease
based on 11 clinical inputs, using a K-Nearest Neighbours (KNN) model trained on a
publicly available dataset.

> ⚠️ **This is not a medical device.** CardioLens is a student/portfolio project.
> It does not provide diagnoses or treatment recommendations. Always consult a
> qualified healthcare professional for medical advice.
""")

# ---------------------------------------------------------------------------
# What do the inputs mean?
# ---------------------------------------------------------------------------
st.markdown("##### Understanding the inputs")
st.caption("A plain-language explanation of each clinical value used by the model.")

explanations = {
    "Age": ("Your age in years. Heart disease risk generally increases with age."),
    "Sex": (
        "Biological sex (Male / Female). The dataset shows different risk distributions by sex, "
        "but this reflects the training data, not a universal rule."
    ),
    "ChestPainType": (
        "The type of chest pain you experience:\n"
        "- **Typical angina** — classic chest pain triggered by exertion, relieved by rest\n"
        "- **Atypical angina** — chest discomfort that doesn't follow the typical pattern\n"
        "- **Non-anginal pain** — chest pain unlikely related to the heart\n"
        "- **No symptoms (asymptomatic)** — no chest pain reported"
    ),
    "RestingBP": (
        "Your systolic blood pressure (mm Hg) measured at rest. "
        "Normal is generally below 120 mm Hg. High blood pressure is a major risk factor."
    ),
    "Cholesterol": (
        "Serum cholesterol level (mg/dL). Desirable is below 200 mg/dL. "
        "High cholesterol can contribute to plaque buildup in arteries. "
        "If you don't know your level, the model uses a typical reference value."
    ),
    "FastingBS": (
        "Whether your fasting blood sugar is above 120 mg/dL. "
        "Elevated fasting blood sugar may indicate diabetes, which is a heart disease risk factor."
    ),
    "RestingECG": (
        "Results of a resting electrocardiogram:\n"
        "- **Normal** — no notable abnormalities\n"
        "- **ST-T wave abnormality** — changes in the T-wave or ST segment\n"
        "- **Left ventricular hypertrophy** — signs of enlarged heart chamber"
    ),
    "MaxHR": (
        "The highest heart rate (beats per minute) achieved during an exercise test. "
        "A lower max heart rate during exercise can be associated with higher risk."
    ),
    "ExerciseAngina": (
        "Whether exercise caused chest pain (angina). "
        "Exercise-induced angina suggests the heart may not be getting enough blood during exertion."
    ),
    "Oldpeak": (
        "The amount of ST segment depression (in mm) induced by exercise compared to rest. "
        "Higher values may indicate reduced blood flow to the heart muscle."
    ),
    "ST_Slope": (
        "The slope of the peak exercise ST segment:\n"
        "- **Upsloping** — generally normal\n"
        "- **Flat** — may indicate ischemia\n"
        "- **Downsloping** — more strongly associated with heart disease"
    ),
}

for feat_name, explanation in explanations.items():
    label = FEATURES.get(feat_name, {}).get("label", feat_name)
    with st.expander(label):
        st.markdown(explanation)

# ---------------------------------------------------------------------------
# Data credits
# ---------------------------------------------------------------------------
st.markdown("##### Data credits")
st.markdown("""
**Heart Failure Prediction Dataset**
fedesoriano. (September 2021). *Heart Failure Prediction Dataset.* Kaggle.

The dataset combines five public heart disease datasets:
- Cleveland Clinic Foundation (303 observations)
- Hungarian Institute of Cardiology (294)
- University Hospital, Zurich (123)
- Long Beach VA Medical Center (200)
- Statlog (Heart) dataset (270)

After removing 272 duplicates: **918 unique records**, 11 features + target.
""")

# ---------------------------------------------------------------------------
# Privacy
# ---------------------------------------------------------------------------
st.markdown("##### Privacy")
st.markdown("""
- **No data is stored or logged.** Your inputs stay in your browser session only.
- No cookies, no analytics, no external API calls.
- Prediction history is lost when you close the tab.
""")

# ---------------------------------------------------------------------------
# Built by
# ---------------------------------------------------------------------------
st.divider()
st.markdown(
    "**Built by Aman** as a portfolio project demonstrating applied machine learning with Streamlit."
)

render_disclaimer()
