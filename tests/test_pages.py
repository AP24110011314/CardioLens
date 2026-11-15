"""Smoke tests for Streamlit pages using AppTest."""

from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest


class TestAppPages:
    """Smoke tests: ensure each page loads without exceptions."""

    def test_main_app_loads(self) -> None:
        at = AppTest.from_file("app.py", default_timeout=30).run()
        assert not at.exception

    def test_predict_page_loads(self) -> None:
        at = AppTest.from_file("pages/1_Predict.py", default_timeout=30).run()
        assert not at.exception

    def test_batch_page_loads(self) -> None:
        at = AppTest.from_file("pages/2_Batch_Prediction.py", default_timeout=30).run()
        assert not at.exception

    def test_insights_page_loads(self) -> None:
        at = AppTest.from_file("pages/3_Insights.py", default_timeout=30).run()
        assert not at.exception

    def test_model_info_page_loads(self) -> None:
        at = AppTest.from_file("pages/4_Model_Info.py", default_timeout=30).run()
        assert not at.exception

    def test_about_page_loads(self) -> None:
        at = AppTest.from_file("pages/5_About.py", default_timeout=30).run()
        assert not at.exception
