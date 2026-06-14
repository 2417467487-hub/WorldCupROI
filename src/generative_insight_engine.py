from __future__ import annotations

from pathlib import Path

import pandas as pd

from project_docs import write_simple_pdf


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def read_csv(name: str) -> pd.DataFrame:
    path = REPORT_DIR / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def bullet(label: str, value: str) -> str:
    return f"- **{label}:** {value}"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    opt = read_csv("sponsor_optimization_summary.csv")
    causal = read_csv("causal_effect_estimates.csv")
    cf = read_csv("counterfactual_summary.csv")
    risk = read_csv("tail_risk_decisions.csv")
    graph = read_csv("graph_learning_link_predictions.csv")
    funnel = read_csv("funnel_behavior_paths.csv")

    lines = [
        "# Causal + Decision Intelligence Brief",
        "",
        "## Executive Summary",
        "",
        "WorldCupROI has been upgraded from an ROI prediction workflow into a decision intelligence platform that connects optimization, causal evidence, temporal behavior, graph learning, counterfactual stress tests, and risk-sensitive sponsor recommendations.",
        "",
        "## Recommended Sponsor Investment Logic",
        "",
    ]
    if not opt.empty:
        top = opt.sort_values("risk_adjusted_roi", ascending=False).iloc[0]
        lines.append(bullet("Budget policy", f"under a {top['budget_cap_m']:.0f}M cap, expected portfolio ROI is {top['expected_portfolio_roi']:.2f}x with risk-adjusted ROI {top['risk_adjusted_roi']:.2f}x."))
    if not causal.empty:
        best = causal.reindex(causal["causal_effect_residualized"].abs().sort_values(ascending=False).index).iloc[0]
        lines.append(bullet("Causal evidence", f"{best['treatment']} has the strongest residualized effect signal ({best['causal_effect_residualized']:.4f}); treat as causal evidence, not proof."))
    if not cf.empty:
        worst = cf.sort_values("worst_case_roi").iloc[0]
        lines.append(bullet("Counterfactual risk", f"{worst['counterfactual']} has the lowest worst-case ROI ({worst['worst_case_roi']:.2f}x)."))
    if not risk.empty:
        safe = risk.sort_values("risk_sensitive_roi", ascending=False).iloc[0]
        lines.append(bullet("Risk-sensitive pick", f"{safe['team']} x {safe['sponsor']} leads after tail-risk adjustment."))
    if not graph.empty:
        link = graph.sort_values("future_sponsor_roi_prediction", ascending=False).iloc[0]
        lines.append(bullet("Future link", f"{link['team']} x {link['sponsor']} is the top graph-learning future sponsor link."))
    if not funnel.empty:
        path = funnel.sort_values("ROI", ascending=False).iloc[0]
        lines.append(bullet("Funnel path", f"{path['team']} x {path['sponsor']} has the strongest Exposure -> ROI path."))

    lines.extend(
        [
            "",
            "## Operating Guidance",
            "",
            "- Use optimization results to shortlist sponsor portfolios.",
            "- Use causal inference to check whether exposure and player signals are decision evidence or only correlations.",
            "- Use counterfactual and tail-risk outputs before scaling spend.",
            "- Use graph learning for future partnership discovery, not as a standalone investment decision.",
            "",
            "## Generated Artifacts",
            "",
            "- `reports/sponsor_optimization_report.md`",
            "- `reports/causal_inference_report.md`",
            "- `reports/temporal_modeling_report.md`",
            "- `reports/funnel_behavior_modeling_report.md`",
            "- `reports/graph_learning_report.md`",
            "- `reports/counterfactual_engine_report.md`",
            "- `reports/tail_risk_analysis_report.md`",
        ]
    )
    md = REPORT_DIR / "decision_intelligence_brief.md"
    md.write_text("\n".join(lines), encoding="utf-8")
    write_simple_pdf(REPORT_DIR / "decision_intelligence_brief.pdf", [line.replace("**", "") for line in lines if line.strip()][:34])
    print({"brief": str(md.relative_to(ROOT))})


if __name__ == "__main__":
    main()
