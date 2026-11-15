"""CardioLens — Batch Prediction page.

Upload a CSV, validate, score all rows, download results.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import COLORS, FEATURE_ORDER, FEATURES
from src.model_loader import load_artifacts
from src.predict import predict_batch
from src.preprocessing import prepare_batch
from src.ui import render_disclaimer

st.title("Batch prediction")
st.caption("Upload a CSV with patient data to score multiple rows at once.")

# ---------------------------------------------------------------------------
# Template download
# ---------------------------------------------------------------------------
st.markdown("##### 1. Download the template")
st.caption(
    "Use this CSV template to ensure your file has the correct columns and format."
)

template_df = pd.DataFrame(
    {feat: [FEATURES[feat]["default"]] for feat in FEATURE_ORDER}
)
csv_template = template_df.to_csv(index=False)
st.download_button(
    ":material/download: Download CSV template",
    data=csv_template,
    file_name="cardiolens_template.csv",
    mime="text/csv",
    key="template_download",
)

st.markdown("**Expected columns:**")
col_descriptions = []
for feat in FEATURE_ORDER:
    spec = FEATURES[feat]
    label = spec["label"]
    if feat in (
        "Sex",
        "ChestPainType",
        "RestingECG",
        "ST_Slope",
        "ExerciseAngina",
        "FastingBS",
    ):
        col_descriptions.append(
            f"- `{feat}` — integer-encoded (see Model Info page for codes)"
        )
    elif "min" in spec and "max" in spec:
        col_descriptions.append(f"- `{feat}` — {spec['min']} to {spec['max']}")
    else:
        col_descriptions.append(f"- `{feat}`")

with st.expander("Column reference"):
    st.markdown("\n".join(col_descriptions))

# ---------------------------------------------------------------------------
# Upload and process
# ---------------------------------------------------------------------------
st.markdown("##### 2. Upload your CSV")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
    label_visibility="collapsed",
    key="batch_upload",
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except (ValueError, pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as e:
        st.error(f"Could not read file: {e}")
        st.stop()

    st.markdown(f"**Loaded {len(df)} rows.**")

    _, scaler, model_columns, scaler_columns = load_artifacts()

    with st.spinner("Validating and scoring..."):
        df_prepared, errors = prepare_batch(df, model_columns, scaler, scaler_columns)

    if errors:
        st.error("Validation errors found:", icon=":material/error:")
        for err in errors:
            st.markdown(f"- {err}")
        st.stop()

    results = predict_batch(df_prepared)

    # Combine original data with results
    output_df = pd.concat([df[FEATURE_ORDER].reset_index(drop=True), results], axis=1)

    # ---------------------------------------------------------------------------
    # Results display
    # ---------------------------------------------------------------------------
    st.markdown("##### 3. Results")

    # Summary metrics
    band_counts = results["Risk_Band"].value_counts()
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Total rows", len(results))
    with metric_cols[1]:
        st.metric("Low risk", int(band_counts.get("Low", 0)))
    with metric_cols[2]:
        st.metric("Moderate risk", int(band_counts.get("Moderate", 0)))
    with metric_cols[3]:
        st.metric("High risk", int(band_counts.get("High", 0)))

    # Histogram of probabilities
    fig = px.histogram(
        results,
        x="Probability",
        color="Risk_Band",
        color_discrete_map={
            "Low": COLORS["low"],
            "Moderate": COLORS["moderate"],
            "High": COLORS["high"],
        },
        nbins=20,
        labels={"Probability": "Predicted probability", "Risk_Band": "Risk band"},
    )
    fig.update_layout(
        height=300,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0")
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
    st.plotly_chart(
        fig,
        key="batch_histogram",
        alt="Batch prediction probability distribution",
        config={"responsive": True, "displayModeBar": False},
    )

    # Data table
    st.dataframe(
        output_df,
        hide_index=True,
        column_config={
            "Probability": st.column_config.ProgressColumn(
                "Probability",
                min_value=0.0,
                max_value=1.0,
                format="%.1%%",
            ),
            "Risk_Band": st.column_config.TextColumn("Risk band"),
        },
    )

    # Download results
    csv_result = output_df.to_csv(index=False)
    st.download_button(
        ":material/download: Download results CSV",
        data=csv_result,
        file_name="cardiolens_batch_results.csv",
        mime="text/csv",
        key="batch_result_download",
        width="stretch",
    )

    render_disclaimer()
