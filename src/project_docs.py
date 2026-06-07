from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
REPORT_DIR = ROOT / "reports"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def markdown_table(df: pd.DataFrame, max_rows: int = 12) -> str:
    view = df.head(max_rows)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, lines: list[str]) -> None:
    content_lines = ["BT", "/F1 17 Tf", "50 780 Td"]
    for i, line in enumerate(lines[:34]):
        size = 18 if i == 0 else 10
        content_lines.append(f"/F1 {size} Tf")
        content_lines.append(f"({pdf_escape(line[:92])}) Tj")
        content_lines.append("0 -21 Td")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for off in offsets:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    path.write_bytes(pdf)


def data_inventory() -> pd.DataFrame:
    rows = []
    for path in sorted(DATA_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".csv", ".json"}:
            origin = "proxy/mock commercial data"
            confidence = "medium-low"
            replacement = "Replace with licensed sponsor CRM, sales, broadcast, or social platform data."
            if "raw" in path.parts or path.name in {"historical_matches.csv", "real_text_articles.csv", "media_text_corpus.csv"}:
                origin = "real historical/text source"
                confidence = "medium-high"
                replacement = "Refresh from source APIs and pin source snapshots with data versioning."
            if path.name in {"social_media.csv", "sponsors.csv", "players.csv", "weather.csv"}:
                origin = "proxy/mock commercial enrichment"
                confidence = "medium-low"
            size_kb = round(path.stat().st_size / 1024, 1)
            shape = ""
            if path.suffix.lower() == ".csv":
                try:
                    df = pd.read_csv(path, nrows=5)
                    total = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore")) - 1
                    shape = f"{max(total, 0)} rows x {len(df.columns)} columns"
                except Exception:
                    shape = "unreadable csv"
            rows.append(
                {
                    "dataset": path.relative_to(ROOT).as_posix(),
                    "origin_type": origin,
                    "trust_level": confidence,
                    "shape": shape,
                    "size_kb": size_kb,
                    "future_replacement_path": replacement,
                }
            )
    return pd.DataFrame(rows)


def write_data_card(inventory: pd.DataFrame) -> None:
    lines = [
        "# Data Card",
        "",
        "## Scope",
        "",
        "WorldCupROI combines real historical football data, real-source text/news context, and proxy/mock commercial variables to support reproducible sponsor ROI analysis.",
        "",
        "## Data Boundary",
        "",
        "| Category | Examples | Current Use | Trust Level | Replacement Path |",
        "| --- | --- | --- | --- | --- |",
        "| Real historical data | international match results, World Cup history | Match context, labels, team history | Medium-high | Pin source snapshots, add official FIFA/provider feeds |",
        "| Real text data | Wikipedia/GDELT style article snapshots, media text corpus | Narrative and text-signal features | Medium | Add source freshness checks, use licensed media API |",
        "| Proxy/mock commercial data | sponsor spend, activation quality, player social proxy, conversion proxy | ROI labels, sponsor strategy, dashboard demo | Medium-low | Replace with sponsor CRM, campaign spend, social API, sales/ticketing conversion |",
        "",
        "## Dataset Inventory",
        "",
        markdown_table(inventory, max_rows=40),
        "",
        "## Limitations",
        "",
        "- `sponsor_roi` is a constructed proxy label, not audited sponsor revenue.",
        "- Sponsor spend, activation quality, and conversion fields are demo/proxy variables.",
        "- Text signals are lightweight source-derived features; they are not a substitute for production NLP monitoring.",
        "- Historical match outcomes are real-source oriented, but commercial activation is not historically verified.",
        "",
        "## Future Replacement Path",
        "",
        "1. Connect licensed sponsorship spend and media value datasets.",
        "2. Replace proxy conversion with CRM, sales, search lift, app installs, ticketing, or merch revenue.",
        "3. Add source versioning with DVC or a data warehouse snapshot table.",
        "4. Add automated freshness and drift checks before model retraining.",
    ]
    (DOCS_DIR / "data_card.md").write_text("\n".join(lines), encoding="utf-8")


def write_data_quality_report(inventory: pd.DataFrame) -> None:
    quality = pd.read_csv(REPORT_DIR / "data_quality_summary.csv") if (REPORT_DIR / "data_quality_summary.csv").exists() else pd.DataFrame()
    rows = []
    for _, item in inventory.iterrows():
        if not item["dataset"].endswith(".csv"):
            continue
        path = ROOT / item["dataset"]
        try:
            df = pd.read_csv(path)
            rows.append(
                {
                    "dataset": item["dataset"],
                    "rows": len(df),
                    "columns": len(df.columns),
                    "missing_cells": int(df.isna().sum().sum()),
                    "duplicate_rows": int(df.duplicated().sum()),
                    "origin_type": item["origin_type"],
                    "trust_level": item["trust_level"],
                }
            )
        except Exception:
            continue
    summary = pd.DataFrame(rows).sort_values(["missing_cells", "duplicate_rows"], ascending=False)
    lines = [
        "# Data Quality Report",
        "",
        "## Quality Principles",
        "",
        "- Separate real-source analytical facts from proxy/mock commercial variables.",
        "- Keep demo mode runnable without external APIs.",
        "- Treat proxy labels as decision-support signals, not truth claims.",
        "",
        "## Automated Checks",
        "",
        markdown_table(summary, max_rows=40),
        "",
        "## Existing Pipeline Quality Summary",
        "",
        markdown_table(quality, max_rows=40) if not quality.empty else "No `reports/data_quality_summary.csv` was found.",
        "",
        "## Highest-Risk Fields",
        "",
        "- `sponsor_roi`: proxy label with potential circularity against sponsor features.",
        "- `sponsor_spend_m`: proxy spend; should be replaced by campaign finance data.",
        "- `ad_exposure_m`, `brand_heat_index`, `activation_quality`: modeled commercial assumptions.",
        "- `predicted_roi`: model output; must not be used as a future training label.",
    ]
    (DOCS_DIR / "data_quality_report.md").write_text("\n".join(lines), encoding="utf-8")


def metric_line(text: str, label: str) -> str:
    for line in text.splitlines():
        if line.lower().startswith(f"- {label.lower()}"):
            return line
    return "- Not available"


def write_model_card() -> None:
    match_metrics = read_text(REPORT_DIR / "match_model_metrics.md")
    roi_metrics = read_text(REPORT_DIR / "roi_model_metrics.md")
    match_features = pd.read_csv(REPORT_DIR / "match_feature_group_importance.csv") if (REPORT_DIR / "match_feature_group_importance.csv").exists() else pd.DataFrame()
    roi_features = pd.read_csv(REPORT_DIR / "roi_feature_group_importance.csv") if (REPORT_DIR / "roi_feature_group_importance.csv").exists() else pd.DataFrame()
    lines = [
        "# Model Card",
        "",
        "## Match Outcome Model",
        "",
        "- Task: classify match result as `A_win`, `draw`, or `B_win`.",
        "- Inputs: Elo difference, market value difference, coach experience, player availability, injury risk, weather, stage, and attention context.",
        "- Label construction: historical `result` from match score data.",
        "- Training split: deterministic split defined in `algorithm_strategy.deterministic_split`; current pipeline uses a reproducible holdout split.",
        f"{metric_line(match_metrics, 'Accuracy')}",
        f"{metric_line(match_metrics, 'Log loss')}",
        "",
        "### Match Feature Groups",
        "",
        markdown_table(match_features) if not match_features.empty else "Feature group summary unavailable.",
        "",
        "## Sponsor ROI Model",
        "",
        "- Task: regress sponsor ROI proxy.",
        "- Inputs: media exposure, sponsor power, brand fit, activation quality, team strength, stage premium, weather impact, injury risk, text/social momentum.",
        "- Label construction: `sponsor_roi` is a constructed proxy, not audited revenue.",
        "- Training split: same deterministic reproducible holdout split.",
        f"{metric_line(roi_metrics, 'MAE')}",
        f"{metric_line(roi_metrics, 'RMSE')}",
        f"{metric_line(roi_metrics, 'R2')}",
        "",
        "### ROI Feature Groups",
        "",
        markdown_table(roi_features) if not roi_features.empty else "Feature group summary unavailable.",
        "",
        "## Limitations",
        "",
        "- ROI accuracy is bounded by proxy commercial labels.",
        "- Historical match data may not represent 2026 sponsor behavior.",
        "- Lightweight text features do not capture full narrative causality.",
        "- Current models are interpretable fallbacks; production should compare calibrated tree/boosting and causal uplift models.",
        "",
        "## Potential Data Leakage Risks",
        "",
        "- Post-match engagement or result-derived variables can leak future information if used for pre-match prediction.",
        "- `commercial_momentum_score` may blend variables close to the ROI label construction.",
        "- Generated `predicted_roi` must never be fed back as a training label.",
        "- Scenario outputs should remain downstream decision artifacts, not supervised labels.",
    ]
    (REPORT_DIR / "model_card.md").write_text("\n".join(lines), encoding="utf-8")


def write_business_insights() -> list[str]:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    funnel = pd.read_csv(REPORT_DIR / "attention_funnel.csv") if (REPORT_DIR / "attention_funnel.csv").exists() else pd.DataFrame()
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv") if (DATA_DIR / "scenario_recommendations.csv").exists() else pd.DataFrame()
    graph = pd.read_csv(REPORT_DIR / "sponsor_influence_scores.csv") if (REPORT_DIR / "sponsor_influence_scores.csv").exists() else pd.DataFrame()
    top_rows = panel.sort_values("predicted_roi", ascending=False).head(6)
    scenario_summary = (
        scenarios.groupby("strategy_type", as_index=False)
        .agg(avg_roi=("scenario_roi", "mean"), avg_lift=("roi_lift", "mean"), avg_risk=("risk_score", "mean"))
        .round(3)
        if not scenarios.empty and "strategy_type" in scenarios
        else pd.DataFrame()
    )
    lines = [
        "# Business Insights",
        "",
        "## Executive Takeaway",
        "",
        "WorldCupROI is now positioned as a decision platform: discover audience signals, explain ROI drivers, predict outcomes, simulate sponsor strategies, and recommend business actions.",
        "",
        "## Best Current Opportunities",
        "",
        markdown_table(top_rows[["team", "opponent", "stage", "sponsor", "predicted_roi", "fan_score_panel", "commercial_momentum", "roi_per_million_spend"]]),
        "",
        "## Attention Funnel",
        "",
        markdown_table(funnel) if not funnel.empty else "Run `make pipeline` to generate funnel output.",
        "",
        "## Strategy Summary",
        "",
        markdown_table(scenario_summary) if not scenario_summary.empty else "Run scenario engine to generate strategy output.",
        "",
        "## Sponsor Influence",
        "",
        markdown_table(graph.head(10)) if not graph.empty else "Run graph analysis to generate sponsor influence output.",
        "",
        "## Landing Recommendation",
        "",
        "- Use conservative strategy when risk is high or conversion proxy is weak.",
        "- Use balanced activation as the default commercial package.",
        "- Use aggressive media surge only when attention, stage premium, and player availability align.",
    ]
    (REPORT_DIR / "business_insights.md").write_text("\n".join(lines), encoding="utf-8")
    return [line.replace("#", "").strip() for line in lines if line and not line.startswith("|")][:28]


def write_deployment_docs() -> None:
    lines = [
        "# Deployment Guide",
        "",
        "## One-Command Local Run",
        "",
        "```powershell",
        "make demo",
        "make dashboard",
        "```",
        "",
        "## Streamlit Cloud",
        "",
        "1. Push the repository to GitHub.",
        "2. Create a Streamlit Cloud app from `dashboard/app.py`.",
        "3. Set Python dependencies from `requirements.txt`.",
        "4. Run `make demo` locally before each release to refresh committed demo artifacts.",
        "",
        "## GitHub Pages",
        "",
        "1. Run `make assets` and `make pipeline`.",
        "2. Publish `index.html`, `dashboard/panel_dashboard.html`, `assets/`, `docs/`, and selected `reports/` files.",
        "3. Use GitHub Pages branch settings to serve from the repository root.",
        "",
        "## Docker",
        "",
        "```powershell",
        "docker build -t worldcuproi .",
        "docker run --rm -p 8501:8501 worldcuproi",
        "```",
        "",
        "## Demo Mode Contract",
        "",
        "`--demo` uses local fallback/demo data and does not require external APIs. This keeps the project reproducible for reviewers, Streamlit Cloud, and offline portfolio demos.",
    ]
    (DOCS_DIR / "deployment.md").write_text("\n".join(lines), encoding="utf-8")


def write_executive_summary(pdf_lines: list[str]) -> None:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    lines = [
        "WorldCupROI Executive Summary",
        f"Panel rows: {len(panel):,}",
        f"Teams: {panel['team'].nunique()}",
        f"Sponsors: {panel['sponsor'].nunique()}",
        f"Average predicted ROI: {panel['predicted_roi'].mean():.3f}x",
        f"Average FanScore: {panel['fan_score_panel'].mean():.3f}",
        "",
        "Decision Workflow:",
        "1. Discover audience and match context.",
        "2. Explain ROI drivers and data boundaries.",
        "3. Predict match and sponsor ROI outcomes.",
        "4. Simulate conservative, balanced, and aggressive strategies.",
        "5. Recommend sponsor actions with risk and confidence intervals.",
        "",
        "Deliverables:",
        "business_insights.md, model_card.md, data_card.md, user_research_brief.md, executive_summary.pdf",
        "",
        *pdf_lines[:14],
    ]
    write_simple_pdf(REPORT_DIR / "executive_summary.pdf", lines)


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = data_inventory()
    write_data_card(inventory)
    write_data_quality_report(inventory)
    write_model_card()
    insight_lines = write_business_insights()
    write_deployment_docs()
    write_executive_summary(insight_lines)
    print("Saved data card, quality report, model card, business insights, deployment guide, and executive summary.")


if __name__ == "__main__":
    main()
