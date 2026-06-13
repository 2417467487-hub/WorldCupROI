from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "docs" / "assets"


def score_candidates(panel: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        panel.groupby(["sponsor", "team", "stage"], as_index=False)
        .agg(
            expected_roi=("predicted_roi", "mean"),
            avg_spend=("sponsor_spend_m", "mean"),
            momentum=("commercial_momentum", "mean"),
            fan_score=("fan_score_panel", "mean"),
            exposure=("exposure_score", "mean"),
        )
        .dropna()
    )
    grouped["risk_penalty"] = 1 / (1 + grouped["expected_roi"].clip(lower=0.1))
    grouped["utility"] = (
        grouped["expected_roi"] * 0.55
        + grouped["momentum"] * 0.18
        + grouped["fan_score"] * 0.14
        + grouped["exposure"] * 0.13
        - grouped["risk_penalty"] * 0.08
    )
    grouped["cost_m"] = grouped["avg_spend"].clip(lower=1.0)
    grouped["utility_per_m"] = grouped["utility"] / grouped["cost_m"]
    return grouped.sort_values("utility_per_m", ascending=False)


def greedy_budget_allocation(candidates: pd.DataFrame, budget_m: float = 120.0) -> pd.DataFrame:
    rows = []
    used = 0.0
    seen_sponsor_team: set[tuple[str, str]] = set()
    for _, row in candidates.iterrows():
        key = (str(row["sponsor"]), str(row["team"]))
        cost = float(row["cost_m"])
        if key in seen_sponsor_team or used + cost > budget_m:
            continue
        seen_sponsor_team.add(key)
        used += cost
        out = row.to_dict()
        out["allocated_budget_m"] = round(cost, 2)
        out["cumulative_budget_m"] = round(used, 2)
        rows.append(out)
        if used >= budget_m * 0.96:
            break
    allocation = pd.DataFrame(rows)
    if not allocation.empty:
        allocation["allocation_rank"] = np.arange(1, len(allocation) + 1)
    return allocation


def bandit_policy(candidates: pd.DataFrame) -> pd.DataFrame:
    arms = candidates.head(60).copy()
    arms["ucb_score"] = arms["utility"] + 0.12 * np.sqrt(np.log(len(arms) + 1) / (np.arange(len(arms)) + 1))
    return arms.sort_values("ucb_score", ascending=False).head(12)


def svg_allocation(allocation: pd.DataFrame) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    rows = ['<svg width="1280" height="620" viewBox="0 0 1280 620" xmlns="http://www.w3.org/2000/svg">', '<rect width="1280" height="620" fill="#ffffff"/>']
    rows.append('<text x="64" y="72" font-family="Arial" font-size="34" font-weight="700" fill="#111827">Budget-Constrained Sponsor Allocation</text>')
    rows.append('<text x="64" y="106" font-family="Arial" font-size="17" fill="#4b5563">Greedy portfolio baseline ranked by utility per million budget.</text>')
    if allocation.empty:
        rows.append('<text x="64" y="180" font-family="Arial" font-size="18">No allocation generated.</text>')
    else:
        max_budget = max(float(allocation["allocated_budget_m"].max()), 1)
        y = 160
        for _, row in allocation.head(8).iterrows():
            width = 680 * float(row["allocated_budget_m"]) / max_budget
            label = f'{row["sponsor"]} x {row["team"]}'
            rows.append(f'<text x="74" y="{y+21}" font-family="Arial" font-size="17" fill="#111827">{label}</text>')
            rows.append(f'<rect x="390" y="{y}" width="720" height="28" rx="14" fill="#eef0f3"/>')
            rows.append(f'<rect x="390" y="{y}" width="{width:.1f}" height="28" rx="14" fill="#0072B2"/>')
            rows.append(f'<text x="1128" y="{y+21}" font-family="Arial" font-size="15" fill="#4b5563">{row["allocated_budget_m"]:.1f}M</text>')
            y += 48
    rows.append("</svg>")
    (ASSET_DIR / "sponsor_allocation_optimization.svg").write_text("\n".join(rows), encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    candidates = score_candidates(panel)
    allocation = greedy_budget_allocation(candidates)
    bandit = bandit_policy(candidates)
    candidates.to_csv(REPORT_DIR / "sponsor_strategy_candidates.csv", index=False)
    allocation.to_csv(REPORT_DIR / "optimized_sponsor_allocation.csv", index=False)
    bandit.to_csv(REPORT_DIR / "bandit_sponsor_policy.csv", index=False)
    svg_allocation(allocation)
    lines = [
        "# Sponsor Strategy Optimization Report",
        "",
        "This module upgrades ROI prediction into budget-constrained sponsor allocation.",
        "",
        "## Optimized Allocation",
        "",
        markdown_table(allocation[["allocation_rank", "sponsor", "team", "stage", "allocated_budget_m", "expected_roi", "utility_per_m"]].round(4).head(10)) if not allocation.empty else "No allocation generated.",
        "",
        "## Multi-Armed Bandit Baseline",
        "",
        markdown_table(bandit[["sponsor", "team", "stage", "expected_roi", "ucb_score"]].round(4).head(10)),
        "",
        "## Upgrade Path",
        "",
        "- Bayesian Optimization: tune spend and exposure jointly under budget and risk constraints.",
        "- Contextual Bandit: learn sponsor allocation by team, stage, media heat and fan response.",
        "- Portfolio Optimization: add concentration limits and downside ROI probability constraints.",
    ]
    (REPORT_DIR / "sponsor_optimization_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Saved sponsor optimization outputs.")


if __name__ == "__main__":
    main()
