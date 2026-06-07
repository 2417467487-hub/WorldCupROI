from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from algorithm_strategy import (
    deterministic_split,
    feature_group_summary,
    regression_metrics,
    write_algorithm_manifest,
    write_model_card,
)
from ml_config import RANDOM_SEED, ROI_FEATURES, TEST_SIZE


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models"


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
    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv", nrows=5)
    missing = [feature for feature in ROI_FEATURES if feature not in df.columns]
    if missing:
        from advanced_features import main as build_advanced_features

        build_advanced_features()


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    ensure_dataset()
    write_algorithm_manifest()
    REPORT_DIR.mkdir(exist_ok=True)
    MODEL_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    train_df, test_df = deterministic_split(df)
    model = RidgeROIModel(alpha=1.5).fit(train_df[ROI_FEATURES], train_df["sponsor_roi"])
    pred = model.predict(test_df[ROI_FEATURES])
    metrics = regression_metrics(test_df["sponsor_roi"].to_numpy(), pred)
    importance_df = model.importance()
    group_importance = feature_group_summary(importance_df)

    scored = df.copy()
    scored["predicted_roi"] = model.predict(df[ROI_FEATURES]).round(3)
    scored["roi_lift_vs_spend"] = (scored["predicted_roi"] / scored["a_sponsor_spend_m"]).round(3)

    artifact_path = MODEL_DIR / "sponsor_roi_model.pkl"
    report_path = REPORT_DIR / "roi_model_metrics.md"
    with open(artifact_path, "wb") as f:
        pickle.dump(model.to_artifact(), f)
    importance_df.to_csv(REPORT_DIR / "roi_feature_importance.csv", index=False)
    group_importance.to_csv(REPORT_DIR / "roi_feature_group_importance.csv", index=False)
    scored.to_csv(DATA_DIR / "roi_predictions.csv", index=False)
    write_model_card(
        task="sponsor_roi",
        model_name="RidgeROIModel",
        target="sponsor_roi",
        features=ROI_FEATURES,
        metrics=metrics,
        artifact_path=artifact_path,
        report_path=report_path,
        notes="Fallback ROI model uses standardized ridge regression so the platform remains reproducible without optional boosting libraries.",
    )

    metrics_md = [
        "# Sponsor ROI Model Metrics",
        "",
        f"- MAE: {metrics['mae']:.4f}",
        f"- RMSE: {metrics['rmse']:.4f}",
        f"- R2: {metrics['r2']:.4f}",
        "- Model: dependency-free ridge regression fallback",
        "- Model card: [sponsor_roi_model_card.md](sponsor_roi_model_card.md)",
        "",
        "## Top ROI Drivers",
        "",
        markdown_table(importance_df.head(10)),
        "",
        "## Feature Group Importance",
        "",
        markdown_table(group_importance.head(10)),
        "",
        "## Interpretation",
        "",
        "The ROI model tests whether attention variables, sponsor strength, and football performance jointly explain commercial conversion.",
    ]
    report_path.write_text("\n".join(metrics_md), encoding="utf-8")
    print({"mae": round(metrics["mae"], 4), "rmse": round(metrics["rmse"], 4), "r2": round(metrics["r2"], 4)})


if __name__ == "__main__":
    main()
