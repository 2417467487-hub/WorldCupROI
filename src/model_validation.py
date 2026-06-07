from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from ml_config import MATCH_FEATURES, RANDOM_SEED, ROI_FEATURES
from train_match_model import CentroidOutcomeModel, log_loss
from train_roi_model import RidgeROIModel


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def kfold_indices(n_rows: int, n_splits: int = 5) -> list[np.ndarray]:
    rng = np.random.default_rng(RANDOM_SEED)
    indices = np.arange(n_rows)
    rng.shuffle(indices)
    return [fold for fold in np.array_split(indices, n_splits) if len(fold)]


def accuracy(y_true: pd.Series, y_pred: np.ndarray) -> float:
    return float((y_true.to_numpy() == y_pred).mean())


def regression_scores(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    residual = y_true - y_pred
    mae = float(np.mean(np.abs(residual)))
    rmse = float(np.sqrt(np.mean(residual**2)))
    denom = float(np.sum((y_true - y_true.mean()) ** 2))
    r2 = 1 - float(np.sum(residual**2)) / denom if denom else 0.0
    return {"mae": mae, "rmse": rmse, "r2": r2}


def summarize(rows: list[dict[str, float | str | int]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    summary = (
        df.groupby(["task", "model", "metric"], as_index=False)
        .agg(
            folds=("fold", "count"),
            mean=("value", "mean"),
            std=("value", "std"),
            min=("value", "min"),
            max=("value", "max"),
        )
        .round(4)
    )
    summary["std"] = summary["std"].fillna(0)
    return summary


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def run_match_cv(df: pd.DataFrame, folds: list[np.ndarray]) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    all_indices = np.arange(len(df))
    for fold_id, test_idx in enumerate(folds, start=1):
        train_idx = np.setdiff1d(all_indices, test_idx)
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        model = CentroidOutcomeModel().fit(train[MATCH_FEATURES], train["result"])
        pred = model.predict(test[MATCH_FEATURES])
        proba = model.predict_proba(test[MATCH_FEATURES])
        metrics = {
            "accuracy": accuracy(test["result"], pred),
            "log_loss": log_loss(test["result"], model.classes, proba),
        }
        for metric, value in metrics.items():
            rows.append({"task": "match_outcome", "model": "CentroidOutcomeModel", "fold": fold_id, "metric": metric, "value": value})
    return rows


def run_roi_cv(df: pd.DataFrame, folds: list[np.ndarray]) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    all_indices = np.arange(len(df))
    for fold_id, test_idx in enumerate(folds, start=1):
        train_idx = np.setdiff1d(all_indices, test_idx)
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        model = RidgeROIModel(alpha=1.5).fit(train[ROI_FEATURES], train["sponsor_roi"])
        pred = model.predict(test[ROI_FEATURES])
        metrics = regression_scores(test["sponsor_roi"].to_numpy(), pred)
        for metric, value in metrics.items():
            rows.append({"task": "sponsor_roi", "model": "RidgeROIModel", "fold": fold_id, "metric": metric, "value": value})
    return rows


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data_path = DATA_DIR / "modeling_dataset.csv"
    if not data_path.exists():
        from feature_builder import main as build_features

        build_features()
    df = pd.read_csv(data_path)
    folds = kfold_indices(len(df), n_splits=5)
    fold_rows = run_match_cv(df, folds) + run_roi_cv(df, folds)
    fold_df = pd.DataFrame(fold_rows).round(5)
    summary = summarize(fold_rows)
    fold_df.to_csv(REPORT_DIR / "cross_validation_folds.csv", index=False)
    summary.to_csv(REPORT_DIR / "cross_validation_summary.csv", index=False)
    lines = [
        "# Cross-Validation Generalization Report",
        "",
        "Five-fold cross-validation evaluates whether the current fallback models generalize beyond a single deterministic holdout split.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "- Match outcome accuracy should be read as a directional baseline because football outcomes are noisy and class balance changes by tournament era.",
        "- Sponsor ROI R2 and MAE are more stable when commercial proxy features are internally consistent, but they remain bounded by proxy-label realism.",
        "- Large fold-to-fold variance should trigger data leakage review, stronger temporal splits, or calibrated model selection before production use.",
    ]
    (REPORT_DIR / "cross_validation_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"cv_rows": len(fold_df), "summary_rows": len(summary)})


if __name__ == "__main__":
    main()
