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
        df.groupby(["validation_type", "task", "model", "metric"], as_index=False)
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


def add_metric_rows(
    rows: list[dict[str, float | str | int]],
    *,
    validation_type: str,
    task: str,
    model: str,
    fold: int,
    metrics: dict[str, float],
) -> None:
    for metric, value in metrics.items():
        rows.append(
            {
                "validation_type": validation_type,
                "task": task,
                "model": model,
                "fold": fold,
                "metric": metric,
                "value": value,
            }
        )


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def run_match_cv(df: pd.DataFrame, folds: list[np.ndarray], validation_type: str = "kfold") -> list[dict[str, float | str | int]]:
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
        add_metric_rows(
            rows,
            validation_type=validation_type,
            task="match_outcome",
            model="CentroidOutcomeModel",
            fold=fold_id,
            metrics=metrics,
        )
    return rows


def run_roi_cv(df: pd.DataFrame, folds: list[np.ndarray], validation_type: str = "kfold") -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    all_indices = np.arange(len(df))
    for fold_id, test_idx in enumerate(folds, start=1):
        train_idx = np.setdiff1d(all_indices, test_idx)
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        model = RidgeROIModel(alpha=1.5).fit(train[ROI_FEATURES], train["sponsor_roi"])
        pred = model.predict(test[ROI_FEATURES])
        metrics = regression_scores(test["sponsor_roi"].to_numpy(), pred)
        add_metric_rows(
            rows,
            validation_type=validation_type,
            task="sponsor_roi",
            model="RidgeROIModel",
            fold=fold_id,
            metrics=metrics,
        )
    return rows


def run_subsample_validation(df: pd.DataFrame) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    rng = np.random.default_rng(RANDOM_SEED + 17)
    n = len(df)
    all_idx = np.arange(n)
    sample_fracs = [0.55, 0.70, 0.85]
    for fold_id, frac in enumerate(sample_fracs, start=1):
        train_size = max(40, int(n * frac))
        train_idx = rng.choice(all_idx, size=train_size, replace=False)
        test_idx = np.setdiff1d(all_idx, train_idx)
        if len(test_idx) < 20:
            test_idx = rng.choice(train_idx, size=min(80, len(train_idx) // 3), replace=False)
            train_idx = np.setdiff1d(train_idx, test_idx)
        train, test = df.iloc[train_idx], df.iloc[test_idx]

        match_model = CentroidOutcomeModel().fit(train[MATCH_FEATURES], train["result"])
        match_pred = match_model.predict(test[MATCH_FEATURES])
        match_proba = match_model.predict_proba(test[MATCH_FEATURES])
        add_metric_rows(
            rows,
            validation_type=f"subsample_{int(frac * 100)}pct",
            task="match_outcome",
            model="CentroidOutcomeModel",
            fold=fold_id,
            metrics={
                "accuracy": accuracy(test["result"], match_pred),
                "log_loss": log_loss(test["result"], match_model.classes, match_proba),
            },
        )

        roi_model = RidgeROIModel(alpha=1.5).fit(train[ROI_FEATURES], train["sponsor_roi"])
        roi_pred = roi_model.predict(test[ROI_FEATURES])
        add_metric_rows(
            rows,
            validation_type=f"subsample_{int(frac * 100)}pct",
            task="sponsor_roi",
            model="RidgeROIModel",
            fold=fold_id,
            metrics=regression_scores(test["sponsor_roi"].to_numpy(), roi_pred),
        )
    return rows


def run_temporal_sliding_validation(df: pd.DataFrame) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    if "year" not in df.columns:
        return rows
    years = sorted(int(year) for year in df["year"].dropna().unique())
    if len(years) < 4:
        return rows
    fold_id = 0
    for cutoff in years[2:-1]:
        train = df[df["year"] <= cutoff]
        test = df[df["year"] == years[years.index(cutoff) + 1]]
        if len(train) < 40 or len(test) < 10:
            continue
        fold_id += 1

        match_model = CentroidOutcomeModel().fit(train[MATCH_FEATURES], train["result"])
        match_pred = match_model.predict(test[MATCH_FEATURES])
        match_proba = match_model.predict_proba(test[MATCH_FEATURES])
        add_metric_rows(
            rows,
            validation_type=f"temporal_train_to_{cutoff}_test_{int(test['year'].iloc[0])}",
            task="match_outcome",
            model="CentroidOutcomeModel",
            fold=fold_id,
            metrics={
                "accuracy": accuracy(test["result"], match_pred),
                "log_loss": log_loss(test["result"], match_model.classes, match_proba),
            },
        )

        roi_model = RidgeROIModel(alpha=1.5).fit(train[ROI_FEATURES], train["sponsor_roi"])
        roi_pred = roi_model.predict(test[ROI_FEATURES])
        add_metric_rows(
            rows,
            validation_type=f"temporal_train_to_{cutoff}_test_{int(test['year'].iloc[0])}",
            task="sponsor_roi",
            model="RidgeROIModel",
            fold=fold_id,
            metrics=regression_scores(test["sponsor_roi"].to_numpy(), roi_pred),
        )
    return rows


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    data_path = DATA_DIR / "modeling_dataset.csv"
    if not data_path.exists():
        from feature_builder import main as build_features

        build_features()
    df = pd.read_csv(data_path)
    folds = kfold_indices(len(df), n_splits=5)
    fold_rows = (
        run_match_cv(df, folds)
        + run_roi_cv(df, folds)
        + run_subsample_validation(df)
        + run_temporal_sliding_validation(df)
    )
    fold_df = pd.DataFrame(fold_rows).round(5)
    summary = summarize(fold_rows)
    fold_df.to_csv(REPORT_DIR / "cross_validation_folds.csv", index=False)
    summary.to_csv(REPORT_DIR / "cross_validation_summary.csv", index=False)
    lines = [
        "# Cross-Validation Generalization Report",
        "",
        "Cross-validation, sub-sample validation, and temporal sliding validation evaluate whether the current fallback models generalize beyond a single deterministic holdout split.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "- `kfold` estimates average generalization under random tournament-mixed splits.",
        "- `subsample_*` measures sample-size sensitivity and whether performance collapses when fewer rows are available.",
        "- `temporal_train_to_*` is the highest-risk diagnostic because it asks older tournaments to predict a later tournament.",
        "- Match outcome accuracy should be read as a directional baseline because football outcomes are noisy and class balance changes by tournament era.",
        "- Sponsor ROI R2 and MAE are bounded by proxy-label realism; temporal degradation is a signal to replace mock commercial variables.",
        "- Large fold-to-fold variance should trigger data leakage review, stronger temporal features, or calibrated model selection before production use.",
    ]
    (REPORT_DIR / "cross_validation_report.md").write_text("\n".join(lines), encoding="utf-8")
    print({"cv_rows": len(fold_df), "summary_rows": len(summary)})


if __name__ == "__main__":
    main()
