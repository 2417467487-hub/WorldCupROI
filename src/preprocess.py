from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RANDOM_SEED = 42


TEAMS = [
    "Argentina", "Brazil", "France", "Germany", "Spain", "England", "Portugal", "Netherlands",
    "Uruguay", "Croatia", "Belgium", "Italy", "Mexico", "USA", "Japan", "South Korea",
    "Morocco", "Nigeria", "Ghana", "Saudi Arabia", "Australia", "Canada", "Qatar", "Senegal",
]

SPONSORS = [
    "Adidas", "Nike", "Coca-Cola", "Visa", "Hyundai", "Qatar Airways", "Pepsi", "Sony",
    "Samsung", "Mastercard", "Puma", "Emirates",
]


def sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-x))


def build_team_profile(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for team in TEAMS:
        legacy = rng.normal(0, 1)
        rows.append(
            {
                "team": team,
                "elo": int(1500 + 145 * legacy + rng.normal(0, 55)),
                "coach_wc_matches": int(max(0, rng.normal(10 + 5 * legacy, 7))),
                "squad_market_value_m": round(max(80, rng.lognormal(2.35 + 0.18 * legacy, 0.45) * 90), 1),
                "recent_goal_diff": round(rng.normal(0.25 + 0.35 * legacy, 0.85), 2),
                "social_followers_m": round(max(1, rng.lognormal(2.2 + 0.25 * legacy, 0.75)), 2),
                "brand_globality": round(float(sigmoid(legacy + rng.normal(0, 0.6))), 3),
            }
        )
    return pd.DataFrame(rows)


def generate_players(team_profile: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for _, team in team_profile.iterrows():
        for role in ["core_forward", "core_midfielder", "core_defender"]:
            role_boost = {"core_forward": 1.25, "core_midfielder": 1.05, "core_defender": 0.9}[role]
            rows.append(
                {
                    "team": team["team"],
                    "player_role": role,
                    "player_rating": round(np.clip(rng.normal(74 + team["elo"] / 120, 4), 60, 97), 1),
                    "market_value_m": round(max(5, team["squad_market_value_m"] * rng.uniform(0.04, 0.12) * role_boost), 1),
                    "followers_m": round(max(0.2, team["social_followers_m"] * rng.uniform(0.05, 0.35) * role_boost), 2),
                }
            )
    return pd.DataFrame(rows)


def generate_sponsors(team_profile: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for team in team_profile["team"]:
        sponsor = rng.choice(SPONSORS)
        rows.append(
            {
                "team": team,
                "sponsor": sponsor,
                "sponsor_spend_m": round(float(rng.lognormal(2.2, 0.55)), 2),
                "brand_fit": round(float(rng.beta(5, 2)), 3),
                "activation_quality": round(float(rng.beta(4, 2.5)), 3),
                "historical_sports_presence": round(float(rng.beta(4.5, 2.2)), 3),
            }
        )
    return pd.DataFrame(rows)


def generate_coaches(team_profile: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for _, row in team_profile.iterrows():
        rows.append(
            {
                "team": row["team"],
                "coach_name": f"{row['team']} Head Coach",
                "coach_wc_matches": int(row["coach_wc_matches"]),
                "coach_win_rate": round(float(np.clip(0.36 + (row["elo"] - 1500) / 1100 + rng.normal(0, 0.06), 0.18, 0.78)), 3),
                "coach_tenure_years": round(float(np.clip(rng.normal(3.5, 1.6), 0.4, 9.5)), 1),
                "international_titles": int(max(0, rng.poisson(max(0.2, (row["elo"] - 1350) / 220)))),
            }
        )
    return pd.DataFrame(rows)


def generate_matches(team_profile: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    years = list(range(1930, 2023, 4))
    stages = ["group", "round_16", "quarter_final", "semi_final", "final"]
    weather_types = ["clear", "cloudy", "rain", "hot", "windy"]

    for match_id in range(1, 721):
        year = int(rng.choice(years))
        team_a, team_b = rng.choice(TEAMS, size=2, replace=False)
        a = team_profile.loc[team_profile["team"] == team_a].iloc[0]
        b = team_profile.loc[team_profile["team"] == team_b].iloc[0]
        stage = rng.choice(stages, p=[0.62, 0.16, 0.1, 0.08, 0.04])
        neutral = rng.random() > 0.12
        host_advantage = 0.18 if (not neutral and rng.random() > 0.5) else 0
        ability_gap = (a["elo"] - b["elo"]) / 260 + (a["recent_goal_diff"] - b["recent_goal_diff"]) * 0.25 + host_advantage
        p_a = float(sigmoid(ability_gap))
        draw_prob = float(np.clip(0.32 - abs(p_a - 0.5) * 0.32, 0.12, 0.34))
        win_a_prob = p_a * (1 - draw_prob)
        outcome = rng.choice(["A_win", "draw", "B_win"], p=[win_a_prob, draw_prob, 1 - win_a_prob - draw_prob])
        attention = (
            38
            + 0.015 * (a["elo"] + b["elo"] - 3000)
            + 8 * (stage != "group")
            + 18 * (stage == "final")
            + rng.normal(0, 7)
        )
        rows.append(
            {
                "match_id": match_id,
                "year": year,
                "team_a": team_a,
                "team_b": team_b,
                "stage": stage,
                "neutral_site": int(neutral),
                "host_advantage_a": round(host_advantage, 2),
                "stadium_capacity_k": round(float(rng.normal(58, 16)), 1),
                "temperature_c": round(float(rng.normal(24, 7)), 1),
                "humidity": round(float(np.clip(rng.normal(58, 18), 15, 95)), 1),
                "weather": rng.choice(weather_types, p=[0.42, 0.22, 0.16, 0.12, 0.08]),
                "event_attention_m": round(max(8, attention), 2),
                "media_reposts_k": round(max(1, attention * rng.lognormal(1.1, 0.35)), 2),
                "result": outcome,
            }
        )
    return pd.DataFrame(rows)


def split_weather_social(matches: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    weather = matches[
        [
            "match_id",
            "year",
            "temperature_c",
            "humidity",
            "weather",
            "stadium_capacity_k",
            "neutral_site",
            "host_advantage_a",
        ]
    ].copy()
    weather["venue_region"] = rng.choice(["North America", "Europe", "South America", "Asia", "Africa"], size=len(weather))
    weather["weather_severity"] = np.select(
        [weather["weather"].eq("clear"), weather["weather"].eq("cloudy"), weather["weather"].isin(["rain", "windy"]), weather["weather"].eq("hot")],
        [0.12, 0.22, 0.48, 0.62],
        default=0.30,
    )
    social = matches[["match_id", "year", "team_a", "team_b", "event_attention_m", "media_reposts_k", "stage"]].copy()
    social["hashtag_mentions_k"] = (social["event_attention_m"] * rng.lognormal(1.2, 0.28, len(social))).round(2)
    social["video_views_m"] = (social["event_attention_m"] * rng.uniform(0.8, 2.8, len(social))).round(2)
    social["sentiment_score"] = rng.normal(0.18, 0.28, len(social)).clip(-0.72, 0.91).round(3)
    return weather.round(3), social.round(3)


def generate_2026_schedule(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    host_cities = ["New York", "Los Angeles", "Dallas", "Miami", "Toronto", "Mexico City", "Vancouver"]
    for match_id in range(1001, 1065):
        team_a, team_b = rng.choice(TEAMS, size=2, replace=False)
        rows.append(
            {
                "match_id": match_id,
                "year": 2026,
                "team_a": team_a,
                "team_b": team_b,
                "stage": "group" if match_id < 1049 else "knockout",
                "host_city": rng.choice(host_cities),
                "scheduled_month": rng.choice(["June", "July"]),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    team_profile = build_team_profile(rng)
    players = generate_players(team_profile, rng)
    coaches = generate_coaches(team_profile, rng)
    sponsors = generate_sponsors(team_profile, rng)
    matches = generate_matches(team_profile, rng)
    weather, social = split_weather_social(matches, rng)
    schedule = generate_2026_schedule(rng)

    team_profile.to_csv(DATA_DIR / "team_profile.csv", index=False)
    players.to_csv(DATA_DIR / "synthetic_players.csv", index=False)
    players.to_csv(DATA_DIR / "players.csv", index=False)
    coaches.to_csv(DATA_DIR / "coaches.csv", index=False)
    sponsors.to_csv(DATA_DIR / "synthetic_sponsors.csv", index=False)
    sponsors.to_csv(DATA_DIR / "sponsors.csv", index=False)
    matches.to_csv(DATA_DIR / "synthetic_matches.csv", index=False)
    matches.to_csv(DATA_DIR / "historical_matches.csv", index=False)
    weather.to_csv(DATA_DIR / "weather.csv", index=False)
    social.to_csv(DATA_DIR / "social_media.csv", index=False)
    schedule.to_csv(DATA_DIR / "wc2026_schedule_mock.csv", index=False)
    schedule.to_csv(DATA_DIR / "schedule_2026.csv", index=False)
    print(f"Generated synthetic WorldCupROI data in {DATA_DIR}")


if __name__ == "__main__":
    main()
