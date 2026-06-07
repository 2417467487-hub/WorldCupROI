from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def metric_line(report: str, label: str) -> str:
    for line in report.splitlines():
        if line.lower().startswith(f"- {label.lower()}"):
            return line
    return ""


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    roi_report = read_text(REPORT_DIR / "roi_model_metrics.md")
    match_report = read_text(REPORT_DIR / "match_model_metrics.md")
    uncertainty = read_text(REPORT_DIR / "uncertainty_summary.md")
    conformal = read_text(REPORT_DIR / "conformal_prediction_report.md")
    explainability = pd.read_csv(REPORT_DIR / "roi_driver_explanations.csv") if (REPORT_DIR / "roi_driver_explanations.csv").exists() else pd.DataFrame()
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv") if (DATA_DIR / "scenario_recommendations.csv").exists() else pd.DataFrame()
    top_drivers = ", ".join(explainability["feature"].head(6).tolist()) if not explainability.empty else "not available"
    top_scenarios = (
        scenarios.sort_values("roi_lift", ascending=False)[["scenario", "roi_lift", "risk_level", "strategy_recommendation"]].head(6)
        if not scenarios.empty
        else pd.DataFrame()
    )

    lines = [
        "# Sponsorship Intelligence Brief",
        "",
        "## Executive Summary",
        "",
        "WorldCupROI links match context, fan attention, media exposure, sponsor activation, and risk analysis into a repeatable sponsor decision workflow.",
        "",
        "## Model Signals",
        "",
        f"- Match model: {metric_line(match_report, 'Accuracy') or 'see match_model_metrics.md'}",
        f"- ROI model: {metric_line(roi_report, 'R2') or 'see roi_model_metrics.md'}",
        f"- Key ROI drivers: {top_drivers}",
        "",
        "## Risk and Uncertainty",
        "",
        uncertainty or "- Uncertainty report not available.",
        "",
        "## Conformal Prediction",
        "",
        conformal or "- Conformal report not available.",
        "",
        "## Scenario Recommendations",
        "",
    ]
    if not top_scenarios.empty:
        lines.extend(markdown_table(top_scenarios).splitlines())
    else:
        lines.append("- Scenario recommendations not available.")
    lines.extend(
        [
            "",
            "## Recommended Action",
            "",
            "Prioritize sponsor strategies with positive ROI lift and low or medium risk. Use high-risk scenarios as watchlist cases unless media exposure or player availability can be improved.",
            "",
            "## Analyst Notes",
            "",
            "- Exact sponsor spend remains replaceable with licensed commercial data.",
            "- Text signals are real-source but use lightweight sentiment scoring.",
            "- Production deployment should add SHAP for tree models and calibrated conformal coverage monitoring.",
        ]
    )
    (REPORT_DIR / "sponsorship_intelligence_brief.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved generative business brief to reports/sponsorship_intelligence_brief.md")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
