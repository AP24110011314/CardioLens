"""Tests for src/ui.py"""

from __future__ import annotations

import plotly.graph_objects as go

from src.ui import render_gauge


class TestUI:
    """Verify UI components."""

    def test_render_gauge_returns_figure(self) -> None:
        fig = render_gauge(0.45, "Moderate", "#F5A524")
        assert isinstance(fig, go.Figure)
        assert fig.data[0].type == "indicator"
        assert fig.data[0].value == 45.0
