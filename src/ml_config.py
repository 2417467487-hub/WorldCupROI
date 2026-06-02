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
    "engagement_rate",
    "news_sentiment_score",
    "time_decay_attention",
    "a_core_player_rating",
    "a_core_market_value_m",
    "a_player_followers_m",
    "a_avg_injury_risk",
    "a_avg_availability_score",
    "availability_diff",
    "injury_risk_diff",
]


ROI_FEATURES = [
    "fan_score",
    "a_sponsor_power_index",
    "a_sponsor_spend_m",
    "a_ad_exposure_m",
    "a_brand_heat_index",
    "a_paid_media_share",
    "a_brand_fit",
    "a_activation_quality",
    "a_historical_sports_presence",
    "team_a_strength",
    "event_attention_m",
    "media_reposts_k",
    "engagement_rate",
    "fan_growth_7d_pct",
    "news_sentiment_score",
    "text_signal_score",
    "time_decay_attention",
    "a_player_followers_m",
    "a_player_fan_growth_30d_pct",
    "a_player_sentiment_score",
    "a_core_market_value_m",
    "a_core_player_rating",
    "a_avg_injury_risk",
    "a_avg_availability_score",
    "elo_diff",
    "host_advantage_a",
    "media_exposure_index",
    "commercial_momentum_score",
    "injury_risk_score",
    "sponsor_team_fit_score",
    "weather_impact_score",
    "stage_premium_score",
]


FEATURE_GROUPS = {
    "team_strength": ["elo_diff", "market_value_diff_m", "recent_goal_diff_delta", "team_a_strength"],
    "player_influence": [
        "core_rating_diff",
        "a_core_player_rating",
        "a_core_market_value_m",
        "a_player_followers_m",
        "a_player_fan_growth_30d_pct",
        "a_player_sentiment_score",
    ],
    "injury_availability": ["a_avg_injury_risk", "a_avg_availability_score", "availability_diff", "injury_risk_diff"],
    "coach_context": ["coach_exp_diff"],
    "venue_weather": ["host_advantage_a", "stadium_capacity_k", "temperature_c", "humidity"],
    "media_attention": [
        "event_attention_m",
        "media_reposts_k",
        "engagement_rate",
        "fan_growth_7d_pct",
        "time_decay_attention",
        "fan_score",
    ],
    "text_sentiment": ["news_sentiment_score", "text_signal_score"],
    "sponsor_activation": [
        "a_sponsor_power_index",
        "a_sponsor_spend_m",
        "a_ad_exposure_m",
        "a_brand_heat_index",
        "a_paid_media_share",
        "a_brand_fit",
        "a_activation_quality",
        "a_historical_sports_presence",
    ],
    "business_intelligence_indices": [
        "media_exposure_index",
        "commercial_momentum_score",
        "injury_risk_score",
        "sponsor_team_fit_score",
        "weather_impact_score",
        "stage_premium_score",
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
