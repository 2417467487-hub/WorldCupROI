from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

from ml_config import MATCH_FEATURES, RANDOM_SEED, ROI_FEATURES, TEST_SIZE
from train_match_model import CentroidOutcomeModel, log_loss
from train_roi_model import RidgeROIModel


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


MODEL_CATALOG = [
    {"model": "Logistic Regression", "package": "sklearn", "task": "match classification", "status": "optional"},
    {"model": "Random Forest", "package": "sklearn", "task": "match classification + ROI regression", "status": "optional"},
    {"model": "XGBoost", "package": "xgboost", "task": "tabular classification + regression", "status": "optional"},
    {"model": "LightGBM", "package": "lightgbm", "task": "tabular classification + regression", "status": "optional"},
    {"model": "CatBoost", "package": "catboost", "task": "categorical tabular modeling", "status": "optional"},
    {"model": "MLP", "package": "sklearn", "task": "dense neural baseline", "status": "optional"},
    {"model": "Centroid classifier", "package": "built-in", "task": "match classification fallback", "status": "available"},
    {"model": "Ridge regression", "package": "built-in", "task": "ROI regression fallback", "status": "available"},
]


def package_available(package: str) -> bool:
    return package == "built-in" or importlib.util.find_spec(package) is not None


def split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    idx = rng.permutation(len(df))
    test_n = int(len(df) * TEST_SIZE)
    return df.iloc[idx[test_n:]].copy(), df.iloc[idx[:test_n]].copy()


def r2_score(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return 1 - ss_res / max(ss_tot, 1e-12)


def evaluate_builtin_models(df: pd.DataFrame) -> list[dict[str, object]]:
    train_df, test_df = split(df)
    match_model = CentroidOutcomeModel().fit(train_df[MATCH_FEATURES], train_df["result"])
    match_proba = match_model.predict_proba(test_df[MATCH_FEATURES])
    match_pred = match_model.predict(test_df[MATCH_FEATURES])
    roi_model = RidgeROIModel(alpha=1.5).fit(train_df[ROI_FEATURES], train_df["sponsor_roi"])
    roi_pred = roi_model.predict(test_df[ROI_FEATURES])

    return [
        {
            "task": "match_outcome",
            "model": "Centroid classifier",
            "status": "trained",
            "primary_metric": "accuracy",
            "score": round(float((match_pred == test_df["result"].to_numpy()).mean()), 4),
            "secondary_metric": "log_loss",
            "secondary_score": round(log_loss(test_df["result"], match_model.classes, match_proba), 4),
            "notes": "dependency-free baseline",
        },
        {
            "task": "sponsor_roi",
            "model": "Ridge regression",
            "status": "trained",
            "primary_metric": "r2",
            "score": round(r2_score(test_df["sponsor_roi"].to_numpy(), roi_pred), 4),
            "secondary_metric": "mae",
            "secondary_score": round(float(np.abs(roi_pred - test_df["sponsor_roi"].to_numpy()).mean()), 4),
            "notes": "dependency-free baseline",
        },
    ]


def sklearn_benchmarks(df: pd.DataFrame) -> list[dict[str, object]]:
    if not package_available("sklearn"):
        return []

    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.linear_model import LogisticRegression
    from sklearn.neural_network import MLPClassifier, MLPRegressor

    train_df, test_df = split(df)
    rows: list[dict[str, object]] = []
    classifiers = [
        ("Logistic Regression", LogisticRegression(max_iter=800, random_state=RANDOM_SEED)),
        ("Random Forest", RandomForestClassifier(n_estimators=120, random_state=RANDOM_SEED)),
        ("MLP", MLPClassifier(hidden_layer_sizes=(48,), max_iter=500, random_state=RANDOM_SEED)),
    ]
    for name, model in classifiers:
        model.fit(train_df[MATCH_FEATURES], train_df["result"])
        pred = model.predict(test_df[MATCH_FEATURES])
        rows.append(
            {
                "task": "match_outcome",
                "model": name,
                "status": "trained",
                "primary_metric": "accuracy",
                "score": round(float((pred == test_df["result"].to_numpy()).mean()), 4),
                "secondary_metric": "package",
                "secondary_score": "sklearn",
                "notes": "optional benchmark",
            }
        )

    regressors = [
        ("Random Forest", RandomForestRegressor(n_estimators=160, random_state=RANDOM_SEED)),
        ("MLP", MLPRegressor(hidden_layer_sizes=(64,), max_iter=500, random_state=RANDOM_SEED)),
    ]
    for name, model in regressors:
        model.fit(train_df[ROI_FEATURES], train_df["sponsor_roi"])
        pred = model.predict(test_df[ROI_FEATURES])
        rows.append(
            {
                "task": "sponsor_roi",
                "model": name,
                "status": "trained",
                "primary_metric": "r2",
                "score": round(r2_score(test_df["sponsor_roi"].to_numpy(), pred), 4),
                "secondary_metric": "mae",
                "secondary_score": round(float(np.abs(pred - test_df["sponsor_roi"].to_numpy()).mean()), 4),
                "notes": "optional benchmark",
            }
        )
    return rows


def optional_model_rows() -> list[dict[str, object]]:
    rows = []
    for spec in MODEL_CATALOG:
        if spec["package"] in {"built-in", "sklearn"}:
            continue
        available = package_available(str(spec["package"]))
        rows.append(
            {
                "task": str(spec["task"]),
                "model": str(spec["model"]),
                "status": "available" if available else "not_installed",
                "primary_metric": "",
                "score": "",
                "secondary_metric": "",
                "secondary_score": "",
                "notes": f"install `{spec['package']}` to enable full benchmark",
            }
        )
    return rows


def markdown_table(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    catalog = pd.DataFrame(
        [
            {**spec, "available": package_available(str(spec["package"]))}
            for spec in MODEL_CATALOG
        ]
    )
    results = pd.DataFrame(evaluate_builtin_models(df) + sklearn_benchmarks(df) + optional_model_rows())
    catalog.to_csv(REPORT_DIR / "model_registry_catalog.csv", index=False)
    results.to_csv(REPORT_DIR / "model_registry_comparison.csv", index=False)
    md = [
        "# Model Registry",
        "",
        "The platform keeps dependency-free fallback models runnable while documenting optional production models.",
        "",
        "## Benchmark Results",
        "",
        markdown_table(results),
        "",
        "## Model Catalog",
        "",
        markdown_table(catalog),
    ]
    (REPORT_DIR / "model_registry_comparison.md").write_text("\n".join(md), encoding="utf-8")
    print({"registry_models": len(catalog), "benchmark_rows": len(results)})


if __name__ == "__main__":
    main()
