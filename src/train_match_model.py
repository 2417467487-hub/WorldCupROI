from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from ml_config import MATCH_FEATURES, RANDOM_SEED, TEST_SIZE


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models"


FEATURES = MATCH_FEATURES


class CentroidOutcomeModel:
    """Small dependency-free classifier used when tree libraries are unavailable."""

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "CentroidOutcomeModel":
        self.features = list(X.columns)
        self.classes = sorted(y.unique())
        self.mean = X.mean()
        self.std = X.std().replace(0, 1)
        Xz = (X - self.mean) / self.std
        self.centroids = {label: Xz[y == label].mean().to_numpy() for label in self.classes}
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        Xz = ((X[self.features] - self.mean) / self.std).to_numpy()
        distances = np.column_stack([np.linalg.norm(Xz - self.centroids[label], axis=1) for label in self.classes])
        scores = -distances
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum(axis=1, keepdims=True)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return np.array(self.classes)[self.predict_proba(X).argmax(axis=1)]


def ensure_dataset() -> None:
    if not (DATA_DIR / "modeling_dataset.csv").exists():
        from feature_builder import main as build_features

        build_features()


def train_test_split(df: pd.DataFrame, test_size: float = TEST_SIZE) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    idx = rng.permutation(len(df))
    test_n = int(len(df) * test_size)
    return df.iloc[idx[test_n:]].copy(), df.iloc[idx[:test_n]].copy()


def log_loss(y_true: pd.Series, classes: list[str], proba: np.ndarray) -> float:
    class_to_idx = {label: i for i, label in enumerate(classes)}
    idx = np.array([class_to_idx[v] for v in y_true])
    chosen = np.clip(proba[np.arange(len(idx)), idx], 1e-9, 1)
    return float(-np.log(chosen).mean())


def centroid_importance(model: CentroidOutcomeModel) -> pd.DataFrame:
    centroid_matrix = np.vstack([model.centroids[label] for label in model.classes])
    spread = centroid_matrix.std(axis=0)
    return pd.DataFrame({"feature": model.features, "importance": spread}).sort_values("importance", ascending=False)


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
    model = CentroidOutcomeModel().fit(train_df[FEATURES], train_df["result"])
    pred = model.predict(test_df[FEATURES])
    proba = model.predict_proba(test_df[FEATURES])
    accuracy = float((pred == test_df["result"].to_numpy()).mean())
    loss = log_loss(test_df["result"], model.classes, proba)
    importance_df = centroid_importance(model)

    with open(MODEL_DIR / "match_outcome_model.pkl", "wb") as f:
        pickle.dump(model, f)
    importance_df.to_csv(REPORT_DIR / "match_feature_importance.csv", index=False)

    metrics_md = [
        "# Match Outcome Model Metrics",
        "",
        f"- Accuracy: {accuracy:.4f}",
        f"- Log loss: {loss:.4f}",
        "- Model: dependency-free centroid classifier fallback",
        "",
        "## Top Features",
        "",
        markdown_table(importance_df.head(10)),
    ]
    (REPORT_DIR / "match_model_metrics.md").write_text("\n".join(metrics_md), encoding="utf-8")
    print({"accuracy": round(accuracy, 4), "log_loss": round(loss, 4)})


if __name__ == "__main__":
    main()
