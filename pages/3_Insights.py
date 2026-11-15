"""CardioLens — Insights page.

Session history with trend chart and CSV export.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import COLORS
from src.ui import render_disclaimer

st.title("Insights & history")

# ---------------------------------------------------------------------------
# Session history
# ---------------------------------------------------------------------------
st.markdown("##### Prediction history")
st.caption("Your predictions from this session. Nothing is stored on the server.")

history = st.session_state.get("history", [])

if len(history) == 0:
    st.info(
        "No predictions yet. Go to the **Predict** page and submit a prediction to start building your history.",
        icon=":material/info:",
    )
else:
    history_df = pd.DataFrame(history)

    # Trend chart
    if len(history_df) > 1:
        st.markdown("##### Risk trend")
        # Parse probability back to float
        history_df["prob_float"] = (
            history_df["Probability"].str.replace("%", "").astype(float) / 100
        )
        fig = px.line(
            history_df,
            x="timestamp",
            y="prob_float",
            markers=True,
            labels={"timestamp": "Time", "prob_float": "Risk probability"},
            color_discrete_sequence=[COLORS["primary"]],
        )
        fig.update_layout(
            height=250,
            margin={"l": 10, "r": 10, "t": 10, "b": 10},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis={"range": [0, 1], "tickformat": ".0%"},
        )
        fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0")
        fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
        fig.add_hline(
            y=0.30,
            line_dash="dot",
            line_color=COLORS["low"],
            annotation_text="Low/Moderate",
            annotation_font_color="#15803D",
        )
        fig.add_hline(
            y=0.60,
            line_dash="dot",
            line_color=COLORS["moderate"],
            annotation_text="Moderate/High",
            annotation_font_color="#B45309",
        )
        st.plotly_chart(fig, key="history_trend", alt="Prediction history trend line")

    # Data table
    st.dataframe(
        history_df.drop(columns=["prob_float"], errors="ignore"), hide_index=True
    )

    # Export and clear
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        csv_export = history_df.drop(columns=["prob_float"], errors="ignore").to_csv(
            index=False
        )
        st.download_button(
            ":material/download: Export history CSV",
            data=csv_export,
            file_name="cardiolens_history.csv",
            mime="text/csv",
            key="history_export",
            width="stretch",
        )
    with action_col2:
        if st.button(
            "Clear history", key="clear_history", type="secondary", width="stretch"
        ):
            st.session_state["history"] = []
            st.session_state["last_inputs"] = None
            st.session_state["last_result"] = None
            st.rerun()

    render_disclaimer()
