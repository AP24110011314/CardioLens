"""CardioLens — UI components: CSS, gauge, badge, reusable widgets."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from src.config import COLORS, DISCLAIMER


def inject_custom_css() -> None:
    """Inject custom CSS for cards, badges, and layout polish."""
    st.html("""
    <style>
    /* Card styling */
    div[data-testid="stVerticalBlock"] > div.stContainer {
        border-radius: 12px;
    }

    /* Badge pill */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #FFFFFF;
    }

    /* Disclaimer banner */
    .disclaimer {
        font-size: 0.85rem;
        color: #656D76;
        border-left: 3px solid #F5A524;
        padding-left: 0.75rem;
        margin-top: 1rem;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #656D76;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
    }
    </style>
    """)


def render_gauge(probability: float, band: str, colour: str) -> go.Figure:
    """Create a Plotly gauge chart for the risk probability.

    Parameters
    ----------
    probability : float
        Risk probability (0–1).
    band : str
        Risk band label ("Low", "Moderate", "High").
    colour : str
        Hex colour for the current band.

    Returns
    -------
    go.Figure
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 40, "color": COLORS["text"]}},
            title={"text": f"Risk: {band}", "font": {"size": 18, "color": colour}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": COLORS["muted"],
                    "tickfont": {"color": COLORS["muted"]},
                },
                "bar": {"color": colour, "thickness": 0.3},
                "bgcolor": COLORS["surface"],
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(43,182,115,0.15)"},
                    {"range": [30, 60], "color": "rgba(245,165,36,0.15)"},
                    {"range": [60, 100], "color": "rgba(229,72,77,0.15)"},
                ],
                "threshold": {
                    "line": {"color": colour, "width": 3},
                    "thickness": 0.8,
                    "value": probability * 100,
                },
            },
        )
    )
    fig.update_layout(
        height=250,
        margin={"t": 40, "b": 10, "l": 30, "r": 30},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": COLORS["text"]},
    )
    return fig


def render_badge(band: str, colour: str) -> None:
    """Render a coloured risk badge pill."""
    st.markdown(
        f'<span class="risk-badge" style="background-color:{colour}">{band} Risk</span>',
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render the educational disclaimer."""
    st.caption(DISCLAIMER)


def render_footer() -> None:
    """Render the app footer with credits."""
    st.markdown(
        '<div class="footer">Built by Aman · CardioLens · Educational project</div>',
        unsafe_allow_html=True,
    )
