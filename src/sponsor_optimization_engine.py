from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def markdown_table(df: pd.DataFrame, max_rows: int = 12) -> str:
    view = df.head(max_rows)
    lines = ["| " + " | ".join(view.columns) + " |", "| " + " | ".join(["---"] * len(view.columns)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[c]:.4f}" if isinstance(row[c], float) else str(row[c]) for c in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def normalize(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce").fillna(0.0)
    lo, hi = float(s.min()), float(s.max())
    if hi <= lo:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - lo) / (hi - lo)


def portfolio_value(rows: pd.DataFrame, budget: float) -> dict:
    spend = float(rows["recommended_budget_m"].sum())
    roi = float(np.average(rows["expected_roi"], weights=rows["recommended_budget_m"]))
    risk = float(np.average(rows["risk_score"], weights=rows["recommended_budget_m"]))
    return {
        "budget_cap_m": budget,
        "allocated_budget_m": round(spend, 3),
        "expected_portfolio_roi": round(roi, 4),
        "risk_score": round(risk, 4),
        "risk_adjusted_roi": round(roi - 0.55 * risk, 4),
        "sponsor_count": int(rows["sponsor"].nunique()),
    }


def build_candidate_table(panel: pd.DataFrame) -> pd.DataFrame:
    uncertainty_path = DATA_DIR / "roi_uncertainty.csv"
    uncertainty = pd.read_csv(uncertainty_path) if uncertainty_path.exists() else pd.DataFrame()
    risk_by_match = (
        uncertainty.assign(
            risk_score=lambda d: pd.to_numeric(d.get("risk_score", d.get("monte_carlo_std", 0.12)), errors="coerce").fillna(0.12),
            downside_roi=lambda d: pd.to_numeric(d.get("roi_p05", d.get("roi_ci_low", d.get("bootstrap_ci_low", 0))), errors="coerce"),
        )
        .groupby("match_id", as_index=False)
        .agg(risk_score=("risk_score", "mean"), downside_roi=("downside_roi", "mean"))
        if not uncertainty.empty and "match_id" in uncertainty
        else pd.DataFrame()
    )
    candidates = panel.copy()
    if not risk_by_match.empty:
        candidates = candidates.merge(risk_by_match, on="match_id", how="left")
    else:
        candidates["risk_score"] = 0.12
        candidates["downside_roi"] = candidates["predicted_roi"] - 0.25

    grouped = (
        candidates.groupby(["team", "sponsor", "stage"], as_index=False)
        .agg(
            expected_roi=("predicted_roi", "mean"),
            avg_spend_m=("sponsor_spend_m", "mean"),
            fan_score=("fan_score_panel", "mean"),
            exposure=("exposure_score", "mean"),
            momentum=("commercial_momentum", "mean"),
            risk_score=("risk_score", "mean"),
            downside_roi=("downside_roi", "mean"),
            samples=("match_id", "count"),
        )
        .round(4)
    )
    grouped["ucb_score"] = (
        grouped["expected_roi"]
        + 0.18 * normalize(grouped["fan_score"])
        + 0.15 * normalize(grouped["momentum"])
        - 0.35 * normalize(grouped["risk_score"])
    ).round(4)
    grouped["rl_value_score"] = (
        grouped["expected_roi"] * (1 + 0.12 * normalize(grouped["exposure"]))
        - 0.5 * grouped["risk_score"]
        + 0.08 * normalize(grouped["samples"])
    ).round(4)
    grouped["optimizer_score"] = (0.55 * grouped["ucb_score"] + 0.45 * grouped["rl_value_score"]).round(4)
    grouped["min_budget_m"] = grouped["avg_spend_m"].clip(lower=5, upper=45).round(3)
    return grouped.sort_values("optimizer_score", ascending=False)


def greedy_allocate(candidates: pd.DataFrame, budget: float) -> pd.DataFrame:
    selected = []
    remaining = float(budget)
    seen_sponsors: set[str] = set()
    for _, row in candidates.iterrows():
        if remaining <= 4:
            break
        base = float(row["min_budget_m"])
        diversity_penalty = 0.75 if row["sponsor"] in seen_sponsors else 1.0
        allocation = min(base * diversity_penalty, remaining)
        if allocation < 4:
            continue
        item = row.to_dict()
        item["recommended_budget_m"] = round(allocation, 3)
        item["budget_cap_m"] = budget
        item["decision_rule"] = "bayesian_ucb_plus_rl_value"
        selected.append(item)
        remaining -= allocation
        seen_sponsors.add(str(row["sponsor"]))
    return pd.DataFrame(selected)


def optimize_portfolios(candidates: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    budgets = [25.0, 50.0, 100.0, 150.0]
    portfolios = []
    summaries = []
    for budget in budgets:
        selected = greedy_allocate(candidates, budget)
        if selected.empty:
            continue
        portfolios.append(selected)
        summaries.append(portfolio_value(selected, budget))
    return pd.concat(portfolios, ignore_index=True), pd.DataFrame(summaries)


def write_report(portfolio: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# Sponsor Optimization Engine",
        "",
        "## Objective",
        "",
        "Maximize sponsor ROI under explicit budget constraints while penalizing downside risk and rewarding fan attention, media exposure, and commercial momentum.",
        "",
        "## Optimization Methods",
        "",
        "- Bayesian optimization baseline: upper-confidence style acquisition score over sponsor-team-stage candidates.",
        "- Reinforcement learning baseline: contextual bandit value score that rewards ROI, exposure, and repeated evidence while penalizing risk.",
        "- Portfolio policy: greedy budget allocation with sponsor diversity control and risk-adjusted ROI ranking.",
        "",
        "## Portfolio Summary",
        "",
        markdown_table(summary),
        "",
        "## Top Recommended Allocations",
        "",
        markdown_table(
            portfolio[
                [
                    "budget_cap_m",
                    "team",
                    "sponsor",
                    "stage",
                    "recommended_budget_m",
                    "expected_roi",
                    "risk_score",
                    "optimizer_score",
                    "decision_rule",
                ]
            ].sort_values(["budget_cap_m", "optimizer_score"], ascending=[True, False]),
            max_rows=16,
        ),
        "",
        "## Decision Guardrails",
        "",
        "- Treat this as a decision baseline, not a binding media plan.",
        "- Replace proxy commercial variables with audited sponsor revenue data before production use.",
        "- Use causal and counterfactual reports before increasing budget materially.",
    ]
    (REPORT_DIR / "sponsor_optimization_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    candidates = build_candidate_table(panel)
    portfolio, summary = optimize_portfolios(candidates)
    candidates.to_csv(REPORT_DIR / "sponsor_optimization_candidates.csv", index=False)
    portfolio.to_csv(REPORT_DIR / "sponsor_optimization_portfolio.csv", index=False)
    summary.to_csv(REPORT_DIR / "sponsor_optimization_summary.csv", index=False)
    write_report(portfolio, summary)
    print({"optimization_candidates": len(candidates), "portfolio_rows": len(portfolio)})


if __name__ == "__main__":
    main()
