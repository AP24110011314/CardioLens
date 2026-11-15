"""CardioLens — PDF report generation with ReportLab."""

from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config import DISCLAIMER, FEATURES


def generate_pdf_report(
    inputs: dict[str, Any],
    result: dict[str, Any],
    sensitivity_df: Any | None = None,
) -> bytes:
    """Generate a one-page PDF report.

    Parameters
    ----------
    inputs : dict
        User inputs (friendly labels).
    result : dict
        Prediction result from predict_single().
    sensitivity_df : pd.DataFrame | None
        Top factors from sensitivity analysis.

    Returns
    -------
    bytes
        PDF file content.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=12,
        textColor=colors.HexColor("#E5484D"),
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor("#E5484D"),
    )
    body_style = styles["Normal"]
    caption_style = ParagraphStyle(
        "Caption",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
    )

    elements: list[Any] = []

    # Title
    elements.append(Paragraph("❤️ CardioLens — Risk Assessment Report", title_style))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            caption_style,
        )
    )
    elements.append(Spacer(1, 0.5 * cm))

    # Result summary
    elements.append(Paragraph("Result summary", heading_style))
    band_color = result.get("colour", "#E5484D")
    elements.append(
        Paragraph(
            f"<b>Risk probability:</b> {result['proba'] * 100:.1f}% "
            f"&nbsp;&nbsp; <b>Risk band:</b> <font color='{band_color}'><b>{result['band']}</b></font>",
            body_style,
        )
    )
    elements.append(Paragraph(result["message"], body_style))
    elements.append(Spacer(1, 0.5 * cm))

    # Input values table
    elements.append(Paragraph("Your inputs", heading_style))
    table_data = [["Parameter", "Value"]]
    for feature, value in inputs.items():
        label = FEATURES.get(feature, {}).get("label", feature)
        display_val = str(value)
        if feature == "Cholesterol" and value == 0:
            display_val = "Unknown (imputed)"
        table_data.append([label, display_val])

    table = Table(table_data, colWidths=[8 * cm, 8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#161B22")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2A313C")),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.HexColor("#0E1117"), colors.HexColor("#161B22")],
                ),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#E6EDF3")),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 0.5 * cm))

    # Top factors (if available)
    if sensitivity_df is not None and len(sensitivity_df) > 0:
        elements.append(Paragraph("Key factors", heading_style))
        factor_data = [["Factor", "Your value", "Δ Risk"]]
        for _, row in sensitivity_df.head(5).iterrows():
            factor_data.append(
                [
                    str(row["Feature"]),
                    str(row["Your value"]),
                    f"{row['Δ Risk']:+.1%}",
                ]
            )
        factor_table = Table(factor_data, colWidths=[6 * cm, 5 * cm, 5 * cm])
        factor_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#161B22")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#2A313C")),
                    ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#E6EDF3")),
                ]
            )
        )
        elements.append(factor_table)
        elements.append(Spacer(1, 0.5 * cm))

    # Disclaimer
    elements.append(Spacer(1, 0.5 * cm))
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=body_style,
        fontSize=8,
        textColor=colors.HexColor("#F5A524"),
        borderWidth=1,
        borderColor=colors.HexColor("#F5A524"),
        borderPadding=6,
    )
    elements.append(Paragraph(DISCLAIMER, disclaimer_style))

    doc.build(elements)
    return buffer.getvalue()
