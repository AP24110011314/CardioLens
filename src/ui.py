"""CardioLens — UI components: CSS, gauge, badge, reusable widgets."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from src.config import DISCLAIMER

# High-contrast light palette for badges: accessible pastel bg + dark text
BADGE_STYLES: dict[str, dict[str, str]] = {
    "Low": {
        "bg": "#DCFCE7",  # Emerald 100
        "text": "#15803D",  # Emerald 700 (5.4:1 contrast)
        "border": "#86EFAC",  # Emerald 300
    },
    "Moderate": {
        "bg": "#FEF3C7",  # Amber 100
        "text": "#92400E",  # Amber 800 (5.8:1 contrast)
        "border": "#FCD34D",  # Amber 300
    },
    "High": {
        "bg": "#FEE2E2",  # Red 100
        "text": "#991B1B",  # Red 800 (6.5:1 contrast)
        "border": "#FCA5A5",  # Red 300
    },
}


def inject_custom_css() -> None:
    """Inject custom CSS for readable cards, badges, and layout polish."""
    st.html("""
    <style>
    /* Card containers - distinct white surface on soft slate bg */
    div[data-testid="stContainer"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05);
    }

    /* Badge pill */
    .risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }

    /* Disclaimer banner */
    .disclaimer {
        font-size: 0.85rem;
        color: #78350F;
        background-color: #FEF3C7;
        border: 1px solid #FDE68A;
        border-left: 4px solid #D97706;
        border-radius: 8px;
        padding: 0.65rem 0.85rem;
        margin-top: 1rem;
        line-height: 1.45;
    }

    /* Form submit button hover & focus refinement */
    div[data-testid="stFormSubmitButton"] > button {
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }

    /* Streamlit top header bar matching light background */
    header[data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.95) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }

    /* Mobile responsive adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 5rem !important;
            padding-bottom: 2.5rem !important;
        }

        h1,
        .stHeading h1,
        div[data-testid="stHeadingWithActionElements"] h1,
        [data-testid="stMarkdownContainer"] h1 {
            font-size: 1.65rem !important;
            line-height: 1.25 !important;
            padding-top: 0.25rem !important;
            padding-bottom: 0.4rem !important;
        }
        h2,
        .stHeading h2,
        div[data-testid="stHeadingWithActionElements"] h2 {
            font-size: 1.35rem !important;
        }
        h3, h4, h5,
        .stHeading h3,
        div[data-testid="stHeadingWithActionElements"] h3 {
            font-size: 1.15rem !important;
        }

        /* Touch-friendly full-width action buttons */
        div[data-testid="stFormSubmitButton"] > button,
        div[data-testid="stDownloadButton"] > button,
        div.stButton > button {
            width: 100% !important;
            min-height: 44px !important;
        }

        /* Compact cards on mobile */
        div[data-testid="stContainer"] {
            padding: 0.75rem !important;
            margin-bottom: 0.75rem !important;
        }

        /* Metric card readability on small screens */
        div[data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }

        .js-plotly-plot, .plot-container {
            max-width: 100% !important;
        }
    }

    /* Footer styling */
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.82rem;
        padding: 2.5rem 0 1.5rem 0;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
    }
    </style>
    """)


def render_gauge(probability: float, band: str, colour: str) -> go.Figure:
    """Create a high-contrast Plotly gauge chart for light mode."""
    steps = [
        {"range": [0, 30], "color": "rgba(34, 197, 94, 0.20)"},
        {"range": [30, 60], "color": "rgba(245, 158, 11, 0.22)"},
        {"range": [60, 100], "color": "rgba(239, 68, 68, 0.20)"},
    ]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={
                "suffix": "%",
                "font": {
                    "size": 42,
                    "color": "#0F172A",
                    "family": "system-ui, -apple-system, sans-serif",
                },
            },
            title={
                "text": f"<b>{band} Risk</b>",
                "font": {
                    "size": 20,
                    "color": colour,
                    "family": "system-ui, -apple-system, sans-serif",
                },
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1.5,
                    "tickcolor": "#94A3B8",
                    "tickfont": {"color": "#475569", "size": 12},
                },
                "bar": {"color": colour, "thickness": 0.28},
                "bgcolor": "#F1F5F9",
                "borderwidth": 1,
                "bordercolor": "#E2E8F0",
                "steps": steps,
                "threshold": {
                    "line": {"color": colour, "width": 4},
                    "thickness": 0.8,
                    "value": probability * 100,
                },
            },
        )
    )
    fig.update_layout(
        autosize=True,
        height=240,
        margin={"t": 35, "b": 10, "l": 20, "r": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#0F172A"},
    )
    return fig


def render_badge(band: str, colour: str) -> None:
    """Render a high-contrast, easily readable risk badge pill."""
    style = BADGE_STYLES.get(
        band, {"bg": "#F1F5F9", "text": "#1E293B", "border": "#CBD5E1"}
    )
    st.markdown(
        f'<div class="risk-badge" style="background-color:{style["bg"]}; color:{style["text"]}; border:1px solid {style["border"]}">'
        f"● {band} Risk</div>",
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render the educational disclaimer with clear high-contrast callout."""
    st.markdown(
        f'<div class="disclaimer">{DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the app footer with credits."""
    st.markdown(
        '<div class="footer">Built by Aman · CardioLens · Educational project</div>',
        unsafe_allow_html=True,
    )
