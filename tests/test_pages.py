"""Smoke tests for Streamlit pages using AppTest."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent


class TestAppPages:
    """Smoke tests: ensure each page loads without exceptions."""

    def test_main_app_loads(self) -> None:
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        assert not at.exception

    def test_predict_page_loads(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/1_Predict.py"), default_timeout=30
        ).run()
        assert not at.exception

    def test_batch_page_loads(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/2_Batch_Prediction.py"), default_timeout=30
        ).run()
        assert not at.exception

    def test_insights_page_loads(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/3_Insights.py"), default_timeout=30
        ).run()
        assert not at.exception

    def test_model_info_page_loads(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/4_Model_Info.py"), default_timeout=30
        ).run()
        assert not at.exception

    def test_about_page_loads(self) -> None:
        at = AppTest.from_file(str(ROOT / "pages/5_About.py"), default_timeout=30).run()
        assert not at.exception

    def test_predict_example_button(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/1_Predict.py"), default_timeout=30
        ).run()
        assert not at.exception
        at.button(key="example_btn").click().run()
        assert not at.exception
        assert at.session_state["last_result"] is not None
        assert "proba" in at.session_state["last_result"]
        assert "band" in at.session_state["last_result"]

    def test_predict_form_submission(self) -> None:
        at = AppTest.from_file(
            str(ROOT / "pages/1_Predict.py"), default_timeout=30
        ).run()
        assert not at.exception
        # Click form submit button
        for b in at.button:
            if "Predict" in b.label:
                b.click().run()
                break
        assert not at.exception
        assert at.session_state["last_result"] is not None
        assert len(at.session_state["history"]) >= 1
