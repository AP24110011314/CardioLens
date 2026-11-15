"""CardioLens — Heart Disease Risk Prediction App.

Entry point: page configuration and navigation setup.
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="CardioLens",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui import inject_custom_css, render_footer

inject_custom_css()

# --- Navigation ---
predict_page = st.Page(
    "pages/1_Predict.py", title="Predict", icon=":material/ecg_heart:"
)
batch_page = st.Page(
    "pages/2_Batch_Prediction.py",
    title="Batch prediction",
    icon=":material/table_chart:",
)
insights_page = st.Page(
    "pages/3_Insights.py", title="Insights", icon=":material/analytics:"
)
model_info_page = st.Page(
    "pages/4_Model_Info.py", title="Model info", icon=":material/info:"
)
about_page = st.Page("pages/5_About.py", title="About", icon=":material/help:")

nav = st.navigation(
    {
        "Prediction": [predict_page, batch_page],
        "Explore": [insights_page, model_info_page, about_page],
    }
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ❤️ CardioLens")
    st.caption("Heart disease risk estimation")

nav.run()

render_footer()
