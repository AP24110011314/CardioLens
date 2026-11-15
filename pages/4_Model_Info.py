"""CardioLens — Model Info page.

Displays model metrics, confusion matrix, limitations, and technical details.
Degrades gracefully when data/model_metrics.json is not available.
"""

from __future__ import annotations

import numpy as np
import plotly.express as px
import streamlit as st

from src.config import ENCODINGS, FEATURES
from src.model_loader import load_artifacts, load_model_metrics, load_reference_data
from src.ui import render_disclaimer

st.title("Model information")

# ---------------------------------------------------------------------------
# Model overview
# ---------------------------------------------------------------------------
model, scaler, model_columns, scaler_columns = load_artifacts()

st.markdown("##### Model overview")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Algorithm", "K-Nearest Neighbours")
    with col2:
        params = model.get_params()
        st.metric("k (neighbours)", params.get("n_neighbors", "?"))
    with col3:
        st.metric("Weights", params.get("weights", "?").capitalize())

    st.caption(
        f"**Features:** {len(model_columns)} · "
        f"**Scaled features:** {', '.join(scaler_columns)} · "
        f"**Distance metric:** Minkowski (p={params.get('p', 2)}) = Euclidean"
    )

# ---------------------------------------------------------------------------
# Metrics from Colab (if available)
# ---------------------------------------------------------------------------
st.markdown("##### Performance metrics")

metrics = load_model_metrics()
if metrics is not None:
    report = metrics.get("report", {})

    metric_cols = st.columns(5)
    labels = ["accuracy", "precision", "recall", "f1-score"]
    display_names = ["Accuracy", "Precision", "Recall", "F1 Score"]

    for i, (key, name) in enumerate(zip(labels, display_names)):
        val = report.get(key) or report.get("weighted avg", {}).get(key)
        if val is not None:
            with metric_cols[i]:
                st.metric(name, f"{val:.3f}")

    roc_auc = metrics.get("roc_auc")
    if roc_auc is not None:
        with metric_cols[4]:
            st.metric("ROC-AUC", f"{roc_auc:.3f}")

    # Confusion matrix
    cm = metrics.get("confusion_matrix")
    if cm is not None:
        st.markdown("##### Confusion matrix")
        cm_array = np.array(cm)
        fig = px.imshow(
            cm_array,
            labels={"x": "Predicted", "y": "Actual", "color": "Count"},
            x=["No disease", "Heart disease"],
            y=["No disease", "Heart disease"],
            color_continuous_scale=[[0, "#EFF6FF"], [1, "#1D4ED8"]],
            text_auto=True,
        )
        fig.update_layout(
            height=350,
            margin={"l": 10, "r": 10, "t": 10, "b": 10},
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(
            fig,
            key="confusion_matrix",
            alt="Confusion matrix heatmap",
            config={"responsive": True, "displayModeBar": False},
        )

    # sklearn version
    sk_ver = metrics.get("sklearn")
    if sk_ver:
        st.caption(f"Model trained with scikit-learn {sk_ver}")
else:
    st.warning(
        "Model metrics not found. To enable this section, export "
        "`model_metrics.json` from your Colab notebook and place it in `data/`.",
        icon=":material/warning:",
    )
    st.markdown(
        "Expected file: `data/model_metrics.json` with keys: "
        "`sklearn`, `roc_auc`, `chol_median`, `report` (classification_report dict), "
        "`confusion_matrix` (2×2 list)."
    )

# ---------------------------------------------------------------------------
# Dataset info
# ---------------------------------------------------------------------------
st.markdown("##### Dataset")
ref_df = load_reference_data()
if ref_df is not None:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total records", len(ref_df))
    with col_b:
        if "HeartDisease" in ref_df.columns:
            st.metric("Positive (disease)", int(ref_df["HeartDisease"].sum()))
    with col_c:
        if "HeartDisease" in ref_df.columns:
            st.metric("Negative (no disease)", int((ref_df["HeartDisease"] == 0).sum()))
else:
    st.info(
        "Reference dataset not found. Expected: `data/heart_reference.csv` "
        "(918 rows from the Heart Failure Prediction Dataset).",
        icon=":material/info:",
    )

# ---------------------------------------------------------------------------
# Encoding reference
# ---------------------------------------------------------------------------
st.markdown("##### Feature encoding reference")
st.caption(
    "These are the internal integer codes used by the model for categorical features."
)

for feat_name, mapping in ENCODINGS.items():
    if feat_name == "FastingBS":
        continue
    with st.expander(f"{FEATURES.get(feat_name, {}).get('label', feat_name)}"):
        for label, code in mapping.items():
            st.markdown(f"- **{label}** → `{code}`")

# ---------------------------------------------------------------------------
# Limitations
# ---------------------------------------------------------------------------
st.markdown("##### Limitations")
st.markdown("""
- **Small, older, merged dataset** (918 rows): sources used different diagnostic practices.
- **Only 11 features**: no family history, smoking, lipid breakdown, BMI, etc.
- **Not clinically validated**: may be biased by the sex/age distribution of the training data.
- **KNN probabilities are coarse**: with k=5, possible values are only 0%, 20%, 40%, 60%, 80%, 100%.
- **Output is a statistical resemblance** to patients in the dataset, not a diagnosis.
""")

render_disclaimer()
