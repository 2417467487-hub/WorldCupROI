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
    )


def team_player_summary(players: pd.DataFrame) -> pd.DataFrame:
    grouped = players.groupby("team").agg(
        core_player_rating=("player_rating", "max"),
        core_market_value_m=("market_value_m", "max"),
        player_followers_m=("followers_m", "sum"),
    )
    return grouped.reset_index()


def attach_team_features(matches: pd.DataFrame, teams: pd.DataFrame, players: pd.DataFrame, sponsors: pd.DataFrame) -> pd.DataFrame:
    player_summary = team_player_summary(players)
    sponsor_features = sponsors.copy()
    sponsor_features["sponsor_power_index"] = sponsor_power_index(sponsor_features)
    team_features = teams.merge(player_summary, on="team", how="left").merge(sponsor_features, on="team", how="left")

    a = team_features.add_prefix("a_").rename(columns={"a_team": "team_a"})
    b = team_features.add_prefix("b_").rename(columns={"b_team": "team_b"})
    df = matches.merge(a, on="team_a", how="left").merge(b, on="team_b", how="left")
    df["elo_diff"] = df["a_elo"] - df["b_elo"]
    df["market_value_diff_m"] = df["a_squad_market_value_m"] - df["b_squad_market_value_m"]
    df["coach_exp_diff"] = df["a_coach_wc_matches"] - df["b_coach_wc_matches"]
    df["core_rating_diff"] = df["a_core_player_rating"] - df["b_core_player_rating"]
    df["recent_goal_diff_delta"] = df["a_recent_goal_diff"] - df["b_recent_goal_diff"]
    df["team_a_strength"] = (
        0.45 * minmax(df["a_elo"])
        + 0.25 * minmax(df["a_squad_market_value_m"])
        + 0.20 * minmax(df["a_core_player_rating"])
        + 0.10 * minmax(df["a_coach_wc_matches"])
    )
    df["fan_score"] = (
        0.45 * minmax(df["a_player_followers_m"])
        + 0.35 * minmax(df["event_attention_m"])
        + 0.20 * minmax(df["media_reposts_k"])
    )
    return df


def build_roi_target(df: pd.DataFrame) -> pd.DataFrame:
    stage_weight = df["stage"].map({"group": 0.0, "round_16": 0.12, "quarter_final": 0.2, "semi_final": 0.3, "final": 0.45}).fillna(0.08)
    result_boost = df["result"].map({"A_win": 0.16, "draw": 0.04, "B_win": -0.05})
    exposure_efficiency = np.log1p(df["media_reposts_k"]) * 0.11 + np.log1p(df["event_attention_m"]) * 0.16
    rng = np.random.default_rng(42)
    df["sponsor_roi"] = (
        0.75
        + 1.15 * df["fan_score"]
        + 0.90 * df["a_sponsor_power_index"]
        + 0.55 * df["team_a_strength"]
        + exposure_efficiency
        + stage_weight
        + result_boost
        - 0.035 * df["a_sponsor_spend_m"]
        + rng.normal(0, 0.12, len(df))
    ).round(3)
    df["sponsor_roi"] = df["sponsor_roi"].clip(lower=0.45)
    return df


def main() -> None:
    if not (DATA_DIR / "synthetic_matches.csv").exists():
        from preprocess import main as preprocess_main

        preprocess_main()

    matches = pd.read_csv(DATA_DIR / "synthetic_matches.csv")
    teams = pd.read_csv(DATA_DIR / "team_profile.csv")
    players = pd.read_csv(DATA_DIR / "synthetic_players.csv")
    sponsors = pd.read_csv(DATA_DIR / "synthetic_sponsors.csv")

    df = attach_team_features(matches, teams, players, sponsors)
    df = build_roi_target(df)
    out_path = DATA_DIR / "modeling_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved modeling dataset to {out_path}")


if __name__ == "__main__":
    main()

