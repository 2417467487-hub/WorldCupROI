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


def normalize(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce").fillna(0.0)
    lo, hi = float(x.min()), float(x.max())
    if hi <= lo:
        return pd.Series(np.zeros(len(x)), index=x.index)
    return (x - lo) / (hi - lo)


def build_link_predictions(panel: pd.DataFrame) -> pd.DataFrame:
    team_profile = (
        panel.groupby("team", as_index=False)
        .agg(team_roi=("predicted_roi", "mean"), team_attention=("fan_score_panel", "mean"), team_player=("core_player_rating", "mean"))
    )
    sponsor_profile = (
        panel.groupby("sponsor", as_index=False)
        .agg(sponsor_roi=("predicted_roi", "mean"), sponsor_power=("sponsor_power_index", "mean"), sponsor_fit=("brand_fit", "mean"))
    )
    existing = set(zip(panel["team"], panel["sponsor"]))
    rows = []
    for _, team in team_profile.iterrows():
        for _, sponsor in sponsor_profile.iterrows():
            pair = (team["team"], sponsor["sponsor"])
            score = (
                0.34 * team["team_roi"]
                + 0.32 * sponsor["sponsor_roi"]
                + 0.14 * team["team_attention"]
                + 0.10 * sponsor["sponsor_power"]
                + 0.10 * sponsor["sponsor_fit"]
            )
            rows.append(
                {
                    "team": team["team"],
                    "sponsor": sponsor["sponsor"],
                    "existing_edge": pair in existing,
                    "link_prediction_score": round(float(score), 4),
                    "future_sponsor_roi_prediction": round(float(score * (1.0 + 0.04 * sponsor["sponsor_power"])), 4),
                    "model_family": "HGT_GNN_compatible_link_prediction_baseline",
                }
            )
    out = pd.DataFrame(rows)
    out["rank"] = out["link_prediction_score"].rank(ascending=False, method="dense").astype(int)
    return out.sort_values("link_prediction_score", ascending=False)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    links = build_link_predictions(panel)
    links.to_csv(REPORT_DIR / "graph_learning_link_predictions.csv", index=False)

    lines = [
        "# Graph Learning Report",
        "",
        "## Upgrade",
        "",
        "Graph analysis is upgraded into graph learning with future sponsor-team link prediction and future sponsor ROI scoring.",
        "",
        "## Current Baseline",
        "",
        "- Heterogeneous graph schema: teams, sponsors, players, matches, and events.",
        "- Link prediction baseline: sponsor-team compatibility score from ROI, attention, sponsor power, and fit.",
        "- Upgrade path: HGT or GraphSAGE with typed nodes, temporal edges, and link-prediction loss.",
        "",
        "## Top Future Sponsor Links",
        "",
        markdown_table(links.head(15)),
    ]
    (REPORT_DIR / "graph_learning_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"link_predictions": len(links)})


if __name__ == "__main__":
    main()
