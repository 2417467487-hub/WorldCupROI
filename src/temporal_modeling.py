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


def rolling_forecast(panel: pd.DataFrame) -> pd.DataFrame:
    yearly = (
        panel.groupby(["year", "stage"], as_index=False)
        .agg(
            avg_roi=("predicted_roi", "mean"),
            avg_attention=("event_attention_m", "mean"),
            avg_player_rating=("core_player_rating", "mean"),
            samples=("match_id", "count"),
        )
        .sort_values(["stage", "year"])
    )
    frames = []
    for stage, group in yearly.groupby("stage"):
        g = group.sort_values("year").copy()
        g["ewm_roi"] = g["avg_roi"].ewm(alpha=0.45, adjust=False).mean()
        g["temporal_attention_score"] = (
            0.55 * (g["avg_attention"] / max(float(g["avg_attention"].max()), 1.0))
            + 0.45 * (g["avg_player_rating"] / max(float(g["avg_player_rating"].max()), 1.0))
        )
        if len(g) >= 2:
            slope = np.polyfit(g["year"], g["avg_roi"], deg=1)[0]
        else:
            slope = 0.0
        future_years = [2026, 2030, 2034]
        last_roi = float(g["ewm_roi"].iloc[-1])
        for year in future_years:
            g.loc[len(g)] = {
                "year": year,
                "stage": stage,
                "avg_roi": np.nan,
                "avg_attention": np.nan,
                "avg_player_rating": np.nan,
                "samples": 0,
                "ewm_roi": round(last_roi + slope * (year - int(g["year"].dropna().max())), 4),
                "temporal_attention_score": round(float(g["temporal_attention_score"].dropna().mean()), 4),
            }
        frames.append(g)
    out = pd.concat(frames, ignore_index=True)
    out["model_family"] = "temporal_ewm_with_transformer_attention_proxy"
    return out.round(4)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    temporal = rolling_forecast(panel)
    temporal.to_csv(REPORT_DIR / "temporal_roi_forecast.csv", index=False)

    future = temporal[temporal["samples"].eq(0)].sort_values(["year", "stage"])
    lines = [
        "# Temporal Modeling Report",
        "",
        "## Scope",
        "",
        "Model ROI as a time-aware sponsorship signal across World Cup cycles, stages, player strength, and attention context.",
        "",
        "## Current Baseline",
        "",
        "- Time-aware baseline: stage-level exponential weighted ROI trend.",
        "- Transformer proxy: attention-weighted temporal score that blends event attention and player quality.",
        "- Upgrade path: replace proxy with sequence Transformer or Time-aware GNN over match/team/sponsor histories.",
        "",
        "## Future ROI Forecast",
        "",
        markdown_table(future, max_rows=20),
    ]
    (REPORT_DIR / "temporal_modeling_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"temporal_rows": len(temporal), "future_rows": len(future)})


if __name__ == "__main__":
    main()
