from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def minmax(s: pd.Series) -> pd.Series:
    span = s.max() - s.min()
    if span == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / span


def sponsor_power_index(df: pd.DataFrame) -> pd.Series:
    return (
        0.40 * minmax(df["sponsor_spend_m"])
        + 0.25 * df["brand_fit"]
        + 0.20 * df["activation_quality"]
        + 0.15 * df["historical_sports_presence"]
    ).round(4)


def compute_roi_score(df: pd.DataFrame) -> pd.Series:
    return (
        0.95 * df["fan_score_panel"]
        + 0.90 * df["sponsor_power_index"]
        + 0.55 * df["exposure_score"]
        + 0.18 * df["match_points"]
        - 0.025 * df["sponsor_spend_m"]
        + 1.25
    ).clip(lower=0.45).round(4)


def main() -> None:
    panel_path = DATA_DIR / "panel_dataset.csv"
    if not panel_path.exists():
        from build_panel_data import main as build_panel

        build_panel()
    panel = pd.read_csv(panel_path)
    panel["roi_formula_score"] = compute_roi_score(panel)
    panel[["panel_id", "team", "sponsor", "predicted_roi", "roi_formula_score", "roi_per_million_spend"]].to_csv(
        DATA_DIR / "sponsor_roi_outputs.csv", index=False
    )
    print(f"Saved sponsor ROI outputs to {DATA_DIR / 'sponsor_roi_outputs.csv'}")


if __name__ == "__main__":
    main()

