"""CardioLens — Predict page.

Grouped input form, risk gauge, sensitivity analysis, what-if, similar patients,
and compare-with-population tabs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import (
    COLORS,
    DISCLAIMER,
    ENCODINGS,
    FEATURE_GROUPS,
    FEATURE_ORDER,
    FEATURES,
    REFERENCE_VALUES,
)
from src.explain import find_neighbours, sensitivity_analysis, what_if
from src.model_loader import load_reference_data
from src.predict import predict_single
from src.report import generate_pdf_report
from src.ui import render_badge, render_disclaimer, render_gauge

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []
if "last_inputs" not in st.session_state:
    st.session_state["last_inputs"] = None
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

st.title("Heart disease risk prediction")
st.caption("Enter your clinical values below and click **Predict risk** to see your estimated risk.")

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
form_col, result_col = st.columns([3, 2], gap="large")

with form_col:
    with st.form("predict_form"):
        for group_name, features in FEATURE_GROUPS.items():
            st.markdown(f"**{group_name}**")
            with st.container(border=True):
                for feat_name in features:
                    spec = FEATURES[feat_name]

                    if feat_name == "Cholesterol":
                        # "I don't know" checkbox
                        chol_unknown = st.checkbox(
                            "I don't know my cholesterol",
                            value=False,
                            key="chol_unknown",
                            help="If checked, a typical value from the training data will be used.",
                        )
                        if chol_unknown:
                            st.info("A median reference value will be used in the prediction.", icon=":material/info:")
                            cholesterol_val: int | float = 0  # will be imputed
                        else:
                            cholesterol_val = st.number_input(
                                spec["label"],
                                min_value=spec["min"],
                                max_value=spec["max"],
                                value=spec["default"],
                                help=spec["help"],
                                key=f"input_{feat_name}",
                            )
                    elif spec["type"] == "slider":
                        st.slider(
                            spec["label"],
                            min_value=spec["min"],
                            max_value=spec["max"],
                            value=spec["default"],
                            help=spec["help"],
                            key=f"input_{feat_name}",
                        )
                    elif spec["type"] == "number":
                        kwargs: dict[str, Any] = {
                            "label": spec["label"],
                            "min_value": spec["min"],
                            "max_value": spec["max"],
                            "value": spec["default"],
                            "help": spec["help"],
                            "key": f"input_{feat_name}",
                        }
                        if "step" in spec:
                            kwargs["step"] = spec["step"]
                        st.number_input(**kwargs)
                    elif spec["type"] == "select":
                        st.selectbox(
                            spec["label"],
                            options=spec["options"],
                            index=spec["options"].index(spec["default"]) if spec["default"] in spec["options"] else 0,
                            help=spec["help"],
                            key=f"input_{feat_name}",
                        )

        submitted = st.form_submit_button("Predict risk", type="primary", width="stretch")

# ---------------------------------------------------------------------------
# Collect inputs and predict
# ---------------------------------------------------------------------------
if submitted:
    inputs: dict[str, Any] = {}
    for feat_name in FEATURE_ORDER:
        if feat_name == "Cholesterol":
            inputs[feat_name] = cholesterol_val  # type: ignore[possibly-undefined]
        else:
            inputs[feat_name] = st.session_state.get(f"input_{feat_name}", FEATURES[feat_name]["default"])

    with st.spinner("Predicting..."):
        try:
            result = predict_single(inputs)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

    st.session_state["last_inputs"] = inputs
    st.session_state["last_result"] = result

    # Add to history
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **{FEATURES.get(k, {}).get("label", k): v for k, v in inputs.items()},
        "Probability": f"{result['proba']:.1%}",
        "Risk band": result["band"],
    }
    st.session_state["history"].append(entry)

    st.toast(f"Prediction complete: {result['band']} risk ({result['proba']:.0%})", icon="❤️")

# ---------------------------------------------------------------------------
# Result panel
# ---------------------------------------------------------------------------
inputs = st.session_state.get("last_inputs")
result = st.session_state.get("last_result")

if result is not None and inputs is not None:
    with result_col:
        with st.container(border=True):
            gauge_fig = render_gauge(result["proba"], result["band"], result["colour"])
            st.plotly_chart(gauge_fig, key="gauge_chart", alt="Risk probability gauge")

            render_badge(result["band"], result["colour"])
            st.markdown(result["message"])

            st.caption(
                "ℹ️ KNN probabilities are coarse — they represent the fraction of the "
                "model's 5 nearest neighbours with heart disease."
            )
            render_disclaimer()

        # --- PDF download ---
        sens_df = sensitivity_analysis(inputs, result["proba"])
        pdf_bytes = generate_pdf_report(inputs, result, sens_df)
        st.download_button(
            label=":material/download: Download PDF report",
            data=pdf_bytes,
            file_name="cardiolens_report.pdf",
            mime="application/pdf",
            key="pdf_download",
            width="stretch",
        )

    # -----------------------------------------------------------------------
    # Tabs: key factors, what-if, similar patients, compare
    # -----------------------------------------------------------------------
    st.divider()
    tab_factors, tab_whatif, tab_similar, tab_compare = st.tabs([
        ":material/bar_chart: Key factors",
        ":material/swap_horiz: What-if",
        ":material/group: Similar patients",
        ":material/compare: Compare with population",
    ])

    # --- Tab: Key factors ---
    with tab_factors:
        if len(sens_df) > 0:
            st.markdown("##### Which inputs affect your risk the most?")
            st.caption(
                "Each bar shows how your risk would change if one input "
                "were replaced with a typical/healthy reference value."
            )
            top = sens_df.head(7).copy()
            top["Abs"] = top["Δ Risk"].abs()
            fig = px.bar(
                top,
                x="Δ Risk",
                y="Feature",
                orientation="h",
                color="Δ Risk",
                color_continuous_scale=["#2BB673", "#E6EDF3", "#E5484D"],
                color_continuous_midpoint=0,
            )
            fig.update_layout(
                height=300,
                margin={"l": 10, "r": 10, "t": 10, "b": 10},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis={"autorange": "reversed"},
                showlegend=False,
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig, key="factors_chart", alt="Key factors bar chart")
            render_disclaimer()
        else:
            st.info("Your inputs are already at the reference values — no sensitivity to show.")

    # --- Tab: What-if ---
    with tab_whatif:
        st.markdown("##### Adjust values and see how your risk changes")
        st.caption("Move the sliders to explore hypothetical changes.")

        whatif_cols = st.columns(3)
        changes: dict[str, Any] = {}

        with whatif_cols[0]:
            wi_maxhr = st.slider(
                "Max heart rate",
                min_value=50,
                max_value=220,
                value=int(inputs["MaxHR"]) if isinstance(inputs["MaxHR"], (int, float)) else 150,
                key="wi_maxhr",
            )
            if wi_maxhr != inputs["MaxHR"]:
                changes["MaxHR"] = wi_maxhr

        with whatif_cols[1]:
            wi_chol = st.slider(
                "Cholesterol",
                min_value=50,
                max_value=700,
                value=int(inputs["Cholesterol"]) if inputs["Cholesterol"] != 0 else 200,
                key="wi_chol",
            )
            chol_input = inputs["Cholesterol"]
            if chol_input == 0:
                changes["Cholesterol"] = wi_chol
            elif wi_chol != chol_input:
                changes["Cholesterol"] = wi_chol

        with whatif_cols[2]:
            wi_oldpeak = st.slider(
                "ST depression",
                min_value=-3.0,
                max_value=7.0,
                value=float(inputs["Oldpeak"]),
                step=0.1,
                key="wi_oldpeak",
            )
            if wi_oldpeak != inputs["Oldpeak"]:
                changes["Oldpeak"] = wi_oldpeak

        if changes:
            wi_result = what_if(inputs, changes)
            delta = wi_result["delta"]
            col_orig, col_arrow, col_new = st.columns([2, 1, 2])
            with col_orig:
                st.metric("Original risk", f"{wi_result['original_proba']:.0%}", help=wi_result["original_band"])
            with col_arrow:
                st.markdown(
                    f"<div style='text-align:center; font-size:2rem; padding-top:1rem;'>→</div>",
                    unsafe_allow_html=True,
                )
            with col_new:
                st.metric(
                    "Modified risk",
                    f"{wi_result['modified_proba']:.0%}",
                    delta=f"{delta:+.0%}",
                    delta_color="inverse",
                    help=wi_result["modified_band"],
                )
            render_disclaimer()
        else:
            st.info("Adjust a slider to see how your risk changes.")

    # --- Tab: Similar patients ---
    with tab_similar:
        st.markdown("##### Patients with similar clinical values")
        neighbours = find_neighbours(inputs, k=5)
        if neighbours is not None:
            has_disease = neighbours["HeartDisease"].value_counts()
            yes_count = has_disease.get("Yes", 0)
            total = len(neighbours)
            st.metric("Neighbours with heart disease", f"{yes_count} of {total}")

            display_cols = [c for c in neighbours.columns if c != "Distance"]
            st.dataframe(
                neighbours[display_cols],
                hide_index=True,
                column_config={
                    "HeartDisease": st.column_config.TextColumn("Heart disease"),
                },
            )
            st.caption(f"Showing {total} nearest neighbours from the reference dataset (Euclidean distance in scaled space).")
            render_disclaimer()
        else:
            st.warning(
                "Reference data not found. To enable this feature, export "
                "`heart_reference.csv` from your Colab notebook and place it in `data/`.",
                icon=":material/warning:",
            )

    # --- Tab: Compare with population ---
    with tab_compare:
        st.markdown("##### Your values vs. the reference dataset")
        ref_df = load_reference_data()
        if ref_df is not None:
            compare_features = ["Age", "MaxHR", "Cholesterol", "Oldpeak"]
            for feat in compare_features:
                if feat not in ref_df.columns:
                    continue
                user_val = inputs.get(feat)
                if user_val is None or (feat == "Cholesterol" and user_val == 0):
                    continue

                fig = px.histogram(
                    ref_df[ref_df[feat] > 0] if feat == "Cholesterol" else ref_df,
                    x=feat,
                    color=ref_df["HeartDisease"].map({0: "No disease", 1: "Heart disease"}),
                    barmode="overlay",
                    opacity=0.6,
                    color_discrete_map={"No disease": COLORS["low"], "Heart disease": COLORS["high"]},
                    labels={feat: FEATURES.get(feat, {}).get("label", feat)},
                )
                fig.add_vline(
                    x=float(user_val),
                    line_dash="dash",
                    line_color=COLORS["text"],
                    annotation_text="You",
                    annotation_font_color=COLORS["text"],
                )
                fig.update_layout(
                    height=250,
                    margin={"l": 10, "r": 10, "t": 30, "b": 10},
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend_title_text="",
                )
                st.plotly_chart(fig, key=f"compare_{feat}", alt=f"{feat} distribution comparison")
            render_disclaimer()
        else:
            st.warning(
                "Reference data not found. To enable population comparisons, export "
                "`heart_reference.csv` from your Colab notebook and place it in `data/`.",
                icon=":material/warning:",
            )

else:
    # Empty state — before first prediction
    with result_col:
        with st.container(border=True):
            st.markdown("#### Results will appear here")
            st.caption("Fill in the form and click **Predict risk** to see your estimated heart disease risk.")

            if st.button("Try an example", key="example_btn"):
                for feat_name, ref_val in REFERENCE_VALUES.items():
                    st.session_state[f"input_{feat_name}"] = ref_val
                st.rerun()
