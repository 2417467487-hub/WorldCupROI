from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ml_config import FEATURE_GROUPS, MATCH_FEATURES, RANDOM_SEED, ROI_FEATURES, TEST_SIZE


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"


@dataclass(frozen=True)
class AlgorithmLayer:
    name: str
    role: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    current_method: str
    upgrade_path: tuple[str, ...]


ALGORITHM_LAYERS = (
    AlgorithmLayer(
        name="Match Outcome Layer",
        role="Estimate win/draw/loss probability as one input to sponsorship value.",
        inputs=tuple(MATCH_FEATURES),
        outputs=("match probability", "feature importance", "conformal prediction set"),
        current_method="CentroidOutcomeModel fallback with deterministic split",
        upgrade_path=("calibrated logistic regression", "LightGBM multiclass", "XGBoost multi:softprob"),
    ),
    AlgorithmLayer(
        name="Sponsor ROI Layer",
        role="Predict commercial return from sponsor, attention, team, player, and context signals.",
        inputs=tuple(ROI_FEATURES),
        outputs=("predicted ROI", "ROI lift", "ROI driver ranking", "prediction interval"),
        current_method="RidgeROIModel fallback with standardized features",
        upgrade_path=("ElasticNet", "LightGBMRegressor", "XGBoostRegressor", "stacked tabular ensemble"),
    ),
    AlgorithmLayer(
        name="Risk And Recommendation Layer",
        role="Convert point forecasts into risk-aware scenario recommendations.",
        inputs=("predicted ROI", "scenario deltas", "conformal intervals", "Monte Carlo samples"),
        outputs=("negative ROI probability", "scenario ranking", "lift-risk recommendation"),
        current_method="bootstrap, Monte Carlo perturbation, conformal intervals",
        upgrade_path=("ensemble variance", "Bayesian optimization", "portfolio allocation policy"),
    ),
    AlgorithmLayer(
        name="Relationship Intelligence Layer",
        role="Measure sponsor-team-player-match network influence.",
        inputs=("sponsor edges", "team edges", "player edges", "match context"),
        outputs=("influence score", "centrality table", "graph explanation"),
        current_method="weighted heterogeneous graph centrality",
        upgrade_path=("GraphSAGE", "heterogeneous GNN", "temporal graph model"),
    ),
)


def deterministic_split(df: pd.DataFrame, test_size: float = TEST_SIZE) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    idx = rng.permutation(len(df))
    test_n = int(len(df) * test_size)
    return df.iloc[idx[test_n:]].copy(), df.iloc[idx[:test_n]].copy()


def regression_metrics(y_true: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    mae = float(np.abs(pred - y_true).mean())
    rmse = float(np.sqrt(((pred - y_true) ** 2).mean()))
    ss_res = float(((y_true - pred) ** 2).sum())
    ss_tot = float(((y_true - y_true.mean()) ** 2).sum())
    r2 = 1 - ss_res / max(ss_tot, 1e-12)
    return {"mae": mae, "rmse": rmse, "r2": r2}


def classification_metrics(y_true: pd.Series, pred: np.ndarray) -> dict[str, float]:
    return {"accuracy": float((pred == y_true.to_numpy()).mean())}


def feature_group_summary(feature_importance: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for group, features in FEATURE_GROUPS.items():
        group_features = feature_importance[feature_importance["feature"].isin(features)]
        if group_features.empty:
            continue
        rows.append(
            {
                "feature_group": group,
                "importance_sum": round(float(group_features["importance"].sum()), 6),
                "top_feature": str(group_features.iloc[0]["feature"]),
                "feature_count": int(len(group_features)),
            }
        )
    return pd.DataFrame(rows).sort_values("importance_sum", ascending=False)


def write_algorithm_manifest() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "random_seed": RANDOM_SEED,
        "test_size": TEST_SIZE,
        "layers": [asdict(layer) for layer in ALGORITHM_LAYERS],
        "feature_groups": FEATURE_GROUPS,
    }
    (REPORT_DIR / "algorithm_manifest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Algorithm Strategy",
        "",
        "WorldCupROI separates sports prediction from sponsorship decision intelligence.",
        "The current repository keeps dependency-free fallbacks runnable, while documenting production upgrade paths.",
        "",
        "| Layer | Role | Current method | Upgrade path |",
        "|---|---|---|---|",
    ]
    for layer in ALGORITHM_LAYERS:
        lines.append(
            f"| {layer.name} | {layer.role} | {layer.current_method} | {', '.join(layer.upgrade_path)} |"
        )
    lines.extend(
        [
            "",
            "## Feature Groups",
            "",
            "| Group | Features |",
            "|---|---|",
        ]
    )
    for group, features in FEATURE_GROUPS.items():
        lines.append(f"| {group} | {', '.join(features)} |")
    (REPORT_DIR / "algorithm_strategy.md").write_text("\n".join(lines), encoding="utf-8")


def write_model_card(
    *,
    task: str,
    model_name: str,
    target: str,
    features: list[str],
    metrics: dict[str, float],
    artifact_path: Path,
    report_path: Path,
    notes: str,
) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "task": task,
        "model_name": model_name,
        "target": target,
        "feature_count": len(features),
        "features": features,
        "metrics": {key: round(float(value), 6) for key, value in metrics.items()},
        "artifact_path": str(artifact_path.relative_to(ROOT)),
        "report_path": str(report_path.relative_to(ROOT)),
        "random_seed": RANDOM_SEED,
        "test_size": TEST_SIZE,
        "notes": notes,
    }
    card_json = REPORT_DIR / f"{task}_model_card.json"
    card_md = REPORT_DIR / f"{task}_model_card.md"
    card_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        f"# {task.replace('_', ' ').title()} Model Card",
        "",
        f"- Model: {model_name}",
        f"- Target: `{target}`",
        f"- Feature count: {len(features)}",
        f"- Artifact: `{payload['artifact_path']}`",
        f"- Report: `{payload['report_path']}`",
        f"- Random seed: {RANDOM_SEED}",
        f"- Test size: {TEST_SIZE}",
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in metrics.items():
        lines.append(f"| {key} | {value:.4f} |")
    lines.extend(["", "## Notes", "", notes])
    card_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_algorithm_manifest()
    print({"algorithm_layers": len(ALGORITHM_LAYERS), "manifest": "reports/algorithm_manifest.json"})


if __name__ == "__main__":
    main()
