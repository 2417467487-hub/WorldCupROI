from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
DASHBOARD_DIR = ROOT / "dashboard"
ASSETS_DIR = ROOT / "assets"


REQUIRED_FILES = {
    "modeling_dataset": DATA_DIR / "modeling_dataset.csv",
    "roi_predictions": DATA_DIR / "roi_predictions.csv",
    "panel_dataset": DATA_DIR / "panel_dataset.csv",
    "scenario_recommendations": DATA_DIR / "scenario_recommendations.csv",
    "roi_uncertainty": DATA_DIR / "roi_uncertainty.csv",
    "static_dashboard": DASHBOARD_DIR / "panel_dashboard.html",
    "streamlit_app": DASHBOARD_DIR / "app.py",
    "readme_hero": ASSETS_DIR / "images" / "readme_hero.png",
    "demo_video": ASSETS_DIR / "videos" / "worldcuproi_demo.mp4",
    "algorithm_strategy": REPORT_DIR / "algorithm_strategy.md",
    "roi_model_card": REPORT_DIR / "sponsor_roi_model_card.json",
    "match_model_card": REPORT_DIR / "match_outcome_model_card.json",
    "sponsor_optimization": REPORT_DIR / "sponsor_optimization_report.md",
    "causal_inference": REPORT_DIR / "causal_inference_report.md",
    "temporal_modeling": REPORT_DIR / "temporal_modeling_report.md",
    "funnel_behavior": REPORT_DIR / "funnel_behavior_modeling_report.md",
    "graph_learning": REPORT_DIR / "graph_learning_report.md",
    "counterfactual_engine": REPORT_DIR / "counterfactual_engine_report.md",
    "tail_risk": REPORT_DIR / "tail_risk_analysis_report.md",
    "decision_intelligence_brief": REPORT_DIR / "decision_intelligence_brief.md",
}


def row_count(path: Path) -> int | None:
    if not path.exists() or path.suffix.lower() != ".csv":
        return None
    try:
        return int(len(pd.read_csv(path)))
    except Exception:
        return None


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, path in REQUIRED_FILES.items():
        exists = path.exists()
        rows.append(
            {
                "artifact": name,
                "path": str(path.relative_to(ROOT)),
                "exists": exists,
                "size_kb": round(path.stat().st_size / 1024, 2) if exists else 0,
                "rows": row_count(path),
            }
        )
    health = pd.DataFrame(rows)
    health_score = round(float(health["exists"].mean() * 100), 2)
    status = "healthy" if health_score >= 90 else "needs_attention"
    health.to_csv(REPORT_DIR / "platform_health.csv", index=False)
    payload = {"health_score": health_score, "status": status, "artifacts": rows}
    (REPORT_DIR / "platform_health.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = [
        "# Platform Health Check",
        "",
        f"- Health score: {health_score:.2f} / 100",
        f"- Status: {status}",
        "",
        "| Artifact | Exists | Size KB | Rows | Path |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        md.append(
            f"| {row['artifact']} | {row['exists']} | {row['size_kb']} | {row['rows'] or ''} | `{row['path']}` |"
        )
    (REPORT_DIR / "platform_health.md").write_text("\n".join(md), encoding="utf-8")
    print({"health_score": health_score, "status": status})


if __name__ == "__main__":
    main()
