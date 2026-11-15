"""Tests for src/report.py"""

from __future__ import annotations

from src.predict import predict_single
from src.report import generate_pdf_report


def test_generate_pdf_report() -> None:
    inputs = {
        "Age": 50,
        "Sex": "Male",
        "ChestPainType": "Typical angina",
        "RestingBP": 130,
        "Cholesterol": 220,
        "FastingBS": "≤ 120 mg/dL",
        "RestingECG": "Normal",
        "MaxHR": 150,
        "ExerciseAngina": "No",
        "Oldpeak": 1.0,
        "ST_Slope": "Flat",
    }
    result = predict_single(inputs)
    pdf_bytes = generate_pdf_report(inputs, result)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
    # PDF magic header
    assert pdf_bytes.startswith(b"%PDF")
