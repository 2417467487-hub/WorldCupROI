from __future__ import annotations

from dataclasses import dataclass


RANDOM_SEED = 42
TEST_SIZE = 0.22


MATCH_FEATURES = [
    "elo_diff",
    "market_value_diff_m",
    "coach_exp_diff",
    "core_rating_diff",
    "recent_goal_diff_delta",
    "host_advantage_a",
    "stadium_capacity_k",
    "temperature_c",
    "humidity",
    "event_attention_m",
    "media_reposts_k",
    "a_core_player_rating",
    "a_core_market_value_m",
    "a_player_followers_m",
]


ROI_FEATURES = [
    "fan_score",
    "a_sponsor_power_index",
    "a_sponsor_spend_m",
    "a_brand_fit",
    "a_activation_quality",
    "a_historical_sports_presence",
    "team_a_strength",
    "event_attention_m",
    "media_reposts_k",
    "a_player_followers_m",
    "a_core_market_value_m",
    "a_core_player_rating",
    "elo_diff",
    "host_advantage_a",
]


FEATURE_GROUPS = {
    "team_strength": ["elo_diff", "market_value_diff_m", "recent_goal_diff_delta", "team_a_strength"],
    "player_influence": ["core_rating_diff", "a_core_player_rating", "a_core_market_value_m", "a_player_followers_m"],
    "coach_context": ["coach_exp_diff"],
    "venue_weather": ["host_advantage_a", "stadium_capacity_k", "temperature_c", "humidity"],
    "media_attention": ["event_attention_m", "media_reposts_k", "fan_score"],
    "sponsor_activation": [
        "a_sponsor_power_index",
        "a_sponsor_spend_m",
        "a_brand_fit",
        "a_activation_quality",
        "a_historical_sports_presence",
    ],
}


@dataclass(frozen=True)
class ModelSpec:
    task: str
    current_model: str
    production_candidates: tuple[str, ...]
    target: str
    primary_metrics: tuple[str, ...]
    interpretability: str


MODEL_REGISTRY = {
    "match_outcome": ModelSpec(
        task="multi-class classification",
        current_model="CentroidOutcomeModel fallback",
        production_candidates=("XGBoost multi:softprob", "LightGBM multiclass", "LSTM sequence model"),
        target="result",
        primary_metrics=("accuracy", "log_loss"),
        interpretability="permutation/centroid feature importance; upgrade path to SHAP",
    ),
    "sponsor_roi": ModelSpec(
        task="regression",
        current_model="RidgeROIModel fallback",
        production_candidates=("XGBoostRegressor", "LightGBMRegressor", "ElasticNet baseline"),
        target="sponsor_roi",
        primary_metrics=("MAE", "R2"),
        interpretability="absolute standardized coefficients; upgrade path to SHAP",
    ),
}


def describe_registry() -> list[dict[str, str]]:
    rows = []
    for name, spec in MODEL_REGISTRY.items():
        rows.append(
            {
                "module": name,
                "task": spec.task,
                "current_model": spec.current_model,
                "production_candidates": ", ".join(spec.production_candidates),
                "target": spec.target,
                "metrics": ", ".join(spec.primary_metrics),
                "interpretability": spec.interpretability,
            }
        )
    return rows

