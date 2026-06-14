from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def markdown_table(df: pd.DataFrame, max_rows: int = 15) -> str:
    view = df.head(max_rows)
    lines = ["| " + " | ".join(view.columns) + " |", "| " + " | ".join(["---"] * len(view.columns)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[c]:.4f}" if isinstance(row[c], float) else str(row[c]) for c in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv") if (DATA_DIR / "roi_uncertainty.csv").exists() else pd.DataFrame()
    if uncertainty.empty:
        uncertainty = panel[["match_id", "predicted_roi"]].copy()
        uncertainty["roi_ci_low"] = uncertainty["predicted_roi"] - 0.35
        uncertainty["monte_carlo_std"] = 0.14

    uncertainty = uncertainty.assign(
        worst_case_input=lambda d: pd.to_numeric(d.get("roi_p05", d.get("roi_ci_low", d.get("bootstrap_ci_low", 0))), errors="coerce"),
        std_input=lambda d: pd.to_numeric(d.get("roi_std", d.get("monte_carlo_std", d.get("risk_score", 0.14))), errors="coerce").fillna(0.14),
    )
    risk = panel.merge(uncertainty[["match_id", "worst_case_input", "std_input"]], on="match_id", how="left")
    risk["tail_risk_score"] = (risk["std_input"].fillna(0.14) / risk["predicted_roi"].clip(lower=0.1)).round(4)
    risk["worst_case_roi"] = risk["worst_case_input"].fillna(risk["predicted_roi"] - 0.35).round(4)
    risk["risk_sensitive_roi"] = (risk["predicted_roi"] - 1.25 * risk["tail_risk_score"]).round(4)
    out = (
        risk.groupby(["team", "sponsor"], as_index=False)
        .agg(
            expected_roi=("predicted_roi", "mean"),
            worst_case_roi=("worst_case_roi", "min"),
            tail_risk_score=("tail_risk_score", "mean"),
            risk_sensitive_roi=("risk_sensitive_roi", "mean"),
            samples=("match_id", "count"),
        )
        .sort_values("risk_sensitive_roi", ascending=False)
        .round(4)
    )
    out.to_csv(REPORT_DIR / "tail_risk_decisions.csv", index=False)

    lines = [
        "# Tail Risk Analysis",
        "",
        "## Goal",
        "",
        "Move from average ROI to risk-sensitive decision making with worst-case ROI and tail-risk adjusted ranking.",
        "",
        "## Top Risk-Sensitive Opportunities",
        "",
        markdown_table(out.head(15)),
        "",
        "## Decision Rule",
        "",
        "Prefer opportunities with high risk-sensitive ROI and acceptable worst-case ROI, even if their average ROI is not the absolute highest.",
    ]
    (REPORT_DIR / "tail_risk_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"tail_risk_rows": len(out)})


if __name__ == "__main__":
    main()
