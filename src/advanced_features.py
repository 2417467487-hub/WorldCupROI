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


def stage_premium(stage: pd.Series) -> pd.Series:
    return stage.map(
        {
            "group": 0.10,
            "round_16": 0.32,
            "quarter_final": 0.48,
            "semi_final": 0.68,
            "final": 1.00,
            "knockout": 0.52,
        }
    ).fillna(0.20)


def build_advanced_indices(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["media_exposure_index"] = (
        0.34 * minmax(out["media_reposts_k"])
        + 0.26 * minmax(out["event_attention_m"])
        + 0.18 * minmax(out.get("engagement_rate", pd.Series(0, index=out.index)))
        + 0.14 * minmax(out.get("time_decay_attention", out["event_attention_m"]))
        + 0.08 * minmax(out.get("text_signal_score", pd.Series(0, index=out.index)))
    )
    out["injury_risk_score"] = (
        0.60 * out.get("a_avg_injury_risk", pd.Series(0, index=out.index))
        + 0.40 * (1 - out.get("a_avg_availability_score", pd.Series(1, index=out.index)))
    )
    out["sponsor_team_fit_score"] = (
        0.42 * out["a_brand_fit"]
        + 0.25 * out["a_activation_quality"]
        + 0.18 * out.get("a_brand_heat_index", pd.Series(0.5, index=out.index))
        + 0.15 * out.get("a_historical_sports_presence", pd.Series(0.5, index=out.index))
    )
    out["weather_impact_score"] = (
        0.45 * minmax(out["temperature_c"].sub(22).abs())
        + 0.35 * minmax(out["humidity"])
        + 0.20 * minmax(out.get("weather_severity", pd.Series(0.3, index=out.index)))
    )
    out["stage_premium_score"] = stage_premium(out["stage"])
    out["commercial_momentum_score"] = (
        0.28 * out["fan_score"]
        + 0.24 * out["a_sponsor_power_index"]
        + 0.20 * out["media_exposure_index"]
        + 0.14 * out["sponsor_team_fit_score"]
        + 0.08 * out["stage_premium_score"]
        - 0.06 * out["injury_risk_score"]
    ).clip(lower=0)
    return out


def main() -> None:
    path = DATA_DIR / "modeling_dataset.csv"
    df = pd.read_csv(path)
    if "weather_severity" not in df.columns and (DATA_DIR / "weather.csv").exists():
        weather = pd.read_csv(DATA_DIR / "weather.csv")[["match_id", "weather_severity"]]
        df = df.merge(weather, on="match_id", how="left")
    out = build_advanced_indices(df)
    out.to_csv(path, index=False)
    out[
        [
            "match_id",
            "media_exposure_index",
            "commercial_momentum_score",
            "injury_risk_score",
            "sponsor_team_fit_score",
            "weather_impact_score",
            "stage_premium_score",
        ]
    ].to_csv(DATA_DIR / "advanced_feature_outputs.csv", index=False)
    print(f"Saved advanced sponsorship intelligence features to {path}")


if __name__ == "__main__":
    main()
