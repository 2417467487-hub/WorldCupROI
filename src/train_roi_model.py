from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models"


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


class RidgeROIModel:
    """Dependency-free ridge regression for reproducible portfolio demos."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "RidgeROIModel":
        self.features = list(X.columns)
        self.mean = X.mean()
        self.std = X.std().replace(0, 1)
        Xz = ((X - self.mean) / self.std).to_numpy()
        design = np.column_stack([np.ones(len(Xz)), Xz])
        penalty = np.eye(design.shape[1]) * self.alpha
        penalty[0, 0] = 0
        self.coef = np.linalg.solve(design.T @ design + penalty, design.T @ y.to_numpy())
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        Xz = ((X[self.features] - self.mean) / self.std).to_numpy()
        design = np.column_stack([np.ones(len(Xz)), Xz])
        return design @ self.coef

    def importance(self) -> pd.DataFrame:
        return pd.DataFrame({"feature": self.features, "importance": np.abs(self.coef[1:])}).sort_values(
            "importance", ascending=False
        )

    def to_artifact(self) -> dict:
        return {
            "features": self.features,
            "mean": self.mean.to_dict(),
            "std": self.std.to_dict(),
            "coef": self.coef.tolist(),
        }


def ensure_dataset() -> None:
    if not (DATA_DIR / "modeling_dataset.csv").exists():
        from feature_builder import main as build_features

        build_features()


def train_test_split(df: pd.DataFrame, test_size: float = 0.22) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(42)
    idx = rng.permutation(len(df))
    test_n = int(len(df) * test_size)
    return df.iloc[idx[test_n:]].copy(), df.iloc[idx[:test_n]].copy()


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    ensure_dataset()
    REPORT_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    train_df, test_df = train_test_split(df)
    model = RidgeROIModel(alpha=1.5).fit(train_df[ROI_FEATURES], train_df["sponsor_roi"])
    pred = model.predict(test_df[ROI_FEATURES])
    mae = float(np.abs(pred - test_df["sponsor_roi"].to_numpy()).mean())
    ss_res = float(((test_df["sponsor_roi"].to_numpy() - pred) ** 2).sum())
    ss_tot = float(((test_df["sponsor_roi"].to_numpy() - test_df["sponsor_roi"].mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    importance_df = model.importance()

    scored = df.copy()
    scored["predicted_roi"] = model.predict(df[ROI_FEATURES]).round(3)
    scored["roi_lift_vs_spend"] = (scored["predicted_roi"] / scored["a_sponsor_spend_m"]).round(3)

    with open(MODEL_DIR / "sponsor_roi_model.pkl", "wb") as f:
        pickle.dump(model.to_artifact(), f)
    importance_df.to_csv(REPORT_DIR / "roi_feature_importance.csv", index=False)
    scored.to_csv(DATA_DIR / "roi_predictions.csv", index=False)

    metrics_md = [
        "# Sponsor ROI Model Metrics",
        "",
        f"- MAE: {mae:.4f}",
        f"- R2: {r2:.4f}",
        "- Model: dependency-free ridge regression fallback",
        "",
        "## Top ROI Drivers",
        "",
        markdown_table(importance_df.head(10)),
        "",
        "## Interpretation",
        "",
        "The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.",
    ]
    (REPORT_DIR / "roi_model_metrics.md").write_text("\n".join(metrics_md), encoding="utf-8")
    print({"mae": round(mae, 4), "r2": round(r2, 4)})


if __name__ == "__main__":
    main()
