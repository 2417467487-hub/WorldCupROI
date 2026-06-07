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


def compute_fan_score(df: pd.DataFrame) -> pd.Series:
    """Fan influence score from player followers, event attention, and media reposts."""
    return (
        0.45 * minmax(df["player_followers_m"])
        + 0.35 * minmax(df["event_attention_m"])
        + 0.20 * minmax(df["media_reposts_k"])
    ).round(4)


def main() -> None:
    panel_path = DATA_DIR / "panel_dataset.csv"
    if not panel_path.exists():
        from build_panel_data import main as build_panel

        build_panel()
    panel = pd.read_csv(panel_path)
    panel["fan_score_module"] = compute_fan_score(panel)
    panel.to_csv(DATA_DIR / "panel_dataset.csv", index=False)
    panel[["panel_id", "team", "sponsor", "fan_score_module"]].to_csv(DATA_DIR / "fan_score_outputs.csv", index=False)
    print(f"Saved FanScore outputs to {DATA_DIR / 'fan_score_outputs.csv'}")


if __name__ == "__main__":
    main()

