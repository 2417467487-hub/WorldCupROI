from __future__ import annotations

import argparse
import importlib
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineStep:
    name: str
    module: str
    description: str


PIPELINE_STEPS = [
    PipelineStep("preprocess", "real_data_ingestion", "ingest real-source data and prepare base tables"),
    PipelineStep("feature_builder", "feature_builder", "build modeling dataset and core sponsorship features"),
    PipelineStep("advanced_features", "advanced_features", "build business indices"),
    PipelineStep("text_dimensionality", "text_dimensionality", "reduce real-source text features"),
    PipelineStep("data_quality", "data_quality", "profile datasets and schema coverage"),
    PipelineStep("model_registry", "model_registry", "run model catalog and benchmark comparison"),
    PipelineStep("algorithm_strategy", "algorithm_strategy", "write algorithm manifest and upgrade map"),
    PipelineStep("train_match_model", "train_match_model", "train match outcome model"),
    PipelineStep("train_roi_model", "train_roi_model", "train sponsor ROI model"),
    PipelineStep("model_validation", "model_validation", "run cross-validation and generalization diagnostics"),
    PipelineStep("explainability", "explainability", "generate SHAP-style ROI driver explanations"),
    PipelineStep("uncertainty", "uncertainty", "run bootstrap and Monte Carlo ROI risk analysis"),
    PipelineStep("conformal_prediction", "conformal_prediction", "generate match sets and ROI intervals with coverage"),
    PipelineStep("build_panel_data", "build_panel_data", "build dashboard-ready panel data"),
    PipelineStep("user_behavior_analysis", "user_behavior_analysis", "build media-to-conversion user research funnel"),
    PipelineStep("graph_analysis", "graph_analysis", "build team-player-sponsor-match network metrics"),
    PipelineStep("ab_simulation", "ab_simulation", "run counterfactual A/B sponsor scenarios"),
    PipelineStep("scenario_engine", "scenario_engine", "rank sponsor strategy scenarios"),
    PipelineStep("risk_visuals", "risk_visuals", "write uncertainty heatmap and risk-benefit visuals"),
    PipelineStep("project_docs", "project_docs", "write data cards, model card, deployment notes, and executive summary"),
    PipelineStep("generative_report", "generative_report", "write commercial insight brief"),
    PipelineStep("report_generator", "report_generator", "write project report artifacts"),
    PipelineStep("build_dashboard", "build_plotly_dashboard", "build static Plotly dashboard"),
    PipelineStep("platform_health", "platform_health", "verify dashboard, report, model, and data artifacts"),
]


def load_main(module_name: str) -> Callable[[], None]:
    module = importlib.import_module(module_name)
    if not hasattr(module, "main"):
        raise AttributeError(f"{module_name} has no main() function")
    return module.main


def run_step(step: PipelineStep) -> None:
    print(f"\n==> {step.name}: {step.description}")
    load_main(step.module)()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the WorldCupROI reproducible analytics pipeline.")
    parser.add_argument(
        "--fallback",
        action="store_true",
        help="Use local fallback data generator instead of real-source ingestion for the preprocess step.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run fully offline with committed/local demo data. Equivalent to --fallback.",
    )
    parser.add_argument(
        "--skip-ingestion",
        action="store_true",
        help="Skip the preprocess/ingestion step and reuse existing data files.",
    )
    args = parser.parse_args()

    steps = list(PIPELINE_STEPS)
    if args.skip_ingestion:
        steps = [step for step in steps if step.name != "preprocess"]
    elif args.fallback or args.demo:
        steps = [
            PipelineStep("preprocess", "preprocess", "generate fallback local data tables")
            if step.name == "preprocess"
            else step
            for step in steps
        ]

    for step in steps:
        run_step(step)
    print("\nPipeline complete. Open dashboard/panel_dashboard.html or run `streamlit run dashboard/app.py`.")


if __name__ == "__main__":
    main()
