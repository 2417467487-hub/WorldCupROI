from __future__ import annotations

import math
from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

INK = "#111827"
MUTED = "#4b5563"
GRID = "#d1d5db"
PAPER = "#ffffff"
PANEL = "#ffffff"
GREEN = "#009E73"
BLUE = "#0072B2"
CYAN = "#56B4E9"
ORANGE = "#E69F00"
PURPLE = "#7B61FF"
RED = "#D55E00"


def svg(name: str, body: str, width: int = 1600, height: int = 940) -> None:
    (ASSET_DIR / name).write_text(
        f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="{PAPER}"/>
  <line x1="72" y1="136" x2="{width-72}" y2="136" stroke="{GRID}" stroke-width="1"/>
  <style>
    .title {{ font: 700 42px Arial, Helvetica, sans-serif; fill: {INK}; }}
    .subtitle {{ font: 400 20px Arial, Helvetica, sans-serif; fill: {MUTED}; }}
    .h {{ font: 700 23px Arial, Helvetica, sans-serif; fill: {INK}; }}
    .label {{ font: 600 17px Arial, Helvetica, sans-serif; fill: {INK}; }}
    .small {{ font: 400 15px Arial, Helvetica, sans-serif; fill: {MUTED}; }}
    .tiny {{ font: 400 12px Arial, Helvetica, sans-serif; fill: {MUTED}; }}
    .white {{ fill: #ffffff; }}
  </style>
  {body}
</svg>""",
        encoding="utf-8",
    )


def title(text: str, subtitle: str) -> str:
    return f"""
  <text x="76" y="82" class="title">{escape(text)}</text>
  <text x="78" y="122" class="subtitle">{escape(subtitle)}</text>
"""


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = "#7c8da3") -> str:
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return f"""
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
  <path d="M{x2},{y2} l-14,-8 l0,16 z" fill="{color}" transform="rotate({angle} {x2} {y2})"/>
"""


def architecture() -> None:
    rows = [
        ("Data Sources", [("Matches", GREEN), ("Sponsors", BLUE), ("Players", CYAN), ("Text", ORANGE), ("Weather", PURPLE)]),
        ("Feature Store", [("FanScore", GREEN), ("Sponsor Power", BLUE), ("Media Exposure", ORANGE), ("Momentum", PURPLE)]),
        ("Model Layer", [("Match Model", GREEN), ("ROI Model", BLUE), ("GNN Layer", PURPLE), ("Scenario Engine", ORANGE)]),
        ("Reliability Layer", [("SHAP", GREEN), ("Conformal", BLUE), ("Monte Carlo", RED), ("Risk Score", PURPLE)]),
        ("Decision Output", [("Dashboard", GREEN), ("Reports", BLUE), ("Ranking", ORANGE), ("Recommendation", RED)]),
    ]
    parts = [title("Platform Architecture", "Data Sources -> Features -> ML/DL/GNN -> Reliability -> Business Decision Support")]
    y = 178
    for idx, (lane, chips) in enumerate(rows):
        parts.append(f'<text x="86" y="{y+38}" class="h">{lane}</text>')
        parts.append(f'<rect x="310" y="{y}" width="1040" height="76" rx="18" fill="{PANEL}" stroke="{GRID}"/>')
        x = 342
        for chip, color in chips:
            parts.append(f'<rect x="{x}" y="{y+18}" width="180" height="40" rx="20" fill="{color}" opacity="0.92"/>')
            parts.append(f'<text x="{x+90}" y="{y+44}" text-anchor="middle" class="label white">{escape(chip)}</text>')
            x += 210
        if idx < len(rows) - 1:
            parts.append(arrow(830, y + 80, 830, y + 122))
        y += 128
    parts.append(f'<rect x="76" y="828" width="1350" height="56" rx="14" fill="#edf5f2" stroke="{GRID}"/>')
    parts.append(f'<text x="104" y="864" class="label">Key point: match prediction is an upstream signal; the final decision target is sponsor ROI under uncertainty.</text>')
    svg("architecture.svg", "".join(parts), 1480, 920)


def data_flow() -> None:
    parts = [title("Multi-Source Data Flow", "Tabular sports data, real-source text, time-series attention, and graph relationships share one feature store")]
    lanes = [
        ("Historical/Public", "international_results.csv\nWorld Cup history\n2026 schedule", GREEN),
        ("Commercial Proxy", "sponsor spend\nad exposure\nbrand heat", BLUE),
        ("Real Text", "GDELT metadata\nWikimedia text\n5,450 text units", ORANGE),
        ("Context", "weather\nstage premium\nhome/away", PURPLE),
    ]
    x = 80
    for name, desc, color in lanes:
        parts.append(f'<rect x="{x}" y="185" width="285" height="300" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
        parts.append(f'<rect x="{x}" y="185" width="285" height="68" rx="22" fill="{color}"/>')
        parts.append(f'<text x="{x+28}" y="228" class="h white">{escape(name)}</text>')
        for i, line in enumerate(desc.splitlines()):
            parts.append(f'<text x="{x+28}" y="{300+i*42}" class="label">{escape(line)}</text>')
        parts.append(arrow(x + 142, 495, 740, 580, "#9aa8b8"))
        x += 350
    parts.append(f'<rect x="520" y="590" width="460" height="116" rx="24" fill="#eef7f3" stroke="{GREEN}" stroke-width="3"/>')
    parts.append(f'<text x="750" y="637" text-anchor="middle" class="h">Unified Modeling Dataset</text>')
    parts.append(f'<text x="750" y="674" text-anchor="middle" class="small">FanScore, Sponsor Power, Text Signal, Risk Features</text>')
    parts.append(arrow(750, 712, 750, 788, GREEN))
    parts.append(f'<rect x="518" y="798" width="464" height="66" rx="18" fill="{INK}"/>')
    parts.append(f'<text x="750" y="839" text-anchor="middle" class="h white">ROI Dashboard + Research Reports</text>')
    svg("data_flow.svg", "".join(parts), 1480, 930)


def model_pipeline() -> None:
    parts = [title("Model Architecture", "Separate predictive tasks, shared features, and risk-aware business outputs")]
    cols = [
        ("Shared Features", ["team strength", "fan score", "media heat", "weather", "stage premium"], GREEN),
        ("Predictive Models", ["match classifier", "ROI regressor", "model registry", "scenario engine"], BLUE),
        ("Interpretability", ["SHAP-style drivers", "feature importance", "GNN influence"], ORANGE),
        ("Reliability", ["conformal sets", "ROI intervals", "Monte Carlo risk"], PURPLE),
        ("Actions", ["ROI ranking", "scenario lift", "risk warning"], RED),
    ]
    x = 72
    for idx, (header, items, color) in enumerate(cols):
        parts.append(f'<rect x="{x}" y="192" width="252" height="500" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
        parts.append(f'<rect x="{x}" y="192" width="252" height="76" rx="22" fill="{color}"/>')
        parts.append(f'<text x="{x+126}" y="240" text-anchor="middle" class="h white">{escape(header)}</text>')
        y = 310
        for item in items:
            parts.append(f'<circle cx="{x+36}" cy="{y-5}" r="7" fill="{color}"/>')
            parts.append(f'<text x="{x+58}" y="{y}" class="label">{escape(item)}</text>')
            y += 58
        if idx < len(cols) - 1:
            parts.append(arrow(x + 262, 440, x + 326, 440))
        x += 292
    parts.append(f'<rect x="132" y="780" width="1180" height="70" rx="16" fill="#eef2ff" stroke="{GRID}"/>')
    parts.append(f'<text x="722" y="823" text-anchor="middle" class="label">Interpretation: the platform is not one black-box model; it is a decision chain that turns evidence into strategy.</text>')
    svg("model_pipeline.svg", "".join(parts), 1500, 900)


def shap_importance() -> None:
    df = pd.read_csv(ROOT / "reports" / "roi_feature_importance.csv").head(12).iloc[::-1]
    max_val = max(df["importance"].max(), 1e-9)
    parts = [title("SHAP-Style ROI Driver Explanation", "Feature contribution ranking aligned with common ML explainability reports")]
    x0, y0, w, h = 480, 182, 900, 540
    parts.append(f'<rect x="72" y="158" width="1358" height="650" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="{INK}" stroke-width="2"/>')
    parts.append(f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="{INK}" stroke-width="2"/>')
    for i in range(6):
        gx = x0 + i * w / 5
        parts.append(f'<line x1="{gx}" y1="{y0}" x2="{gx}" y2="{y0+h}" stroke="{GRID}" stroke-width="1"/>')
    y = y0 + 32
    for _, row in df.iterrows():
        name = str(row["feature"]).replace("_", " ")
        value = float(row["importance"])
        bw = w * value / max_val * 0.86
        color = GREEN if value >= df["importance"].median() else BLUE
        parts.append(f'<text x="{x0-28}" y="{y+8}" text-anchor="end" class="label">{escape(name)}</text>')
        parts.append(f'<rect x="{x0}" y="{y-16}" width="{bw:.1f}" height="28" rx="14" fill="{color}" opacity="0.92"/>')
        parts.append(f'<text x="{x0+bw+12:.1f}" y="{y+7}" class="small">{value:.3f}</text>')
        y += 42
    parts.append(f'<text x="{x0+w/2}" y="{y0+h+54}" text-anchor="middle" class="label">mean absolute contribution to predicted sponsor ROI</text>')
    parts.append(f'<text x="92" y="764" class="small">Reading: higher bars indicate stronger model influence. Brand heat and team strength dominate, which means ROI is driven by attention quality and sporting context together.</text>')
    svg("roi_feature_importance.svg", "".join(parts), 1500, 850)


def uncertainty_intervals() -> None:
    df = pd.read_csv(ROOT / "data" / "roi_uncertainty.csv").head(42)
    ymin = float(df["roi_ci_low"].min())
    ymax = float(df["roi_ci_high"].max())
    span = max(ymax - ymin, 1e-9)
    parts = [title("ROI Prediction Intervals", "Expected ROI with uncertainty bands for risk-aware sponsor decisions")]
    x0, y0, w, h = 108, 176, 1240, 520
    parts.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
    for i in range(5):
        yy = y0 + 50 + i * (h - 100) / 4
        parts.append(f'<line x1="{x0+60}" y1="{yy}" x2="{x0+w-40}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
    for idx, row in df.iterrows():
        x = x0 + 70 + idx * (w - 130) / max(len(df) - 1, 1)
        low = y0 + h - 60 - (float(row["roi_ci_low"]) - ymin) / span * (h - 120)
        high = y0 + h - 60 - (float(row["roi_ci_high"]) - ymin) / span * (h - 120)
        mean = y0 + h - 60 - (float(row["roi_mean"]) - ymin) / span * (h - 120)
        parts.append(f'<line x1="{x:.1f}" y1="{high:.1f}" x2="{x:.1f}" y2="{low:.1f}" stroke="{BLUE}" stroke-width="5" opacity=".28"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{mean:.1f}" r="5.5" fill="{ORANGE}"/>')
    parts.append(f'<text x="{x0+60}" y="{y0+h+48}" class="label">Blue ranges = ROI intervals; orange dots = expected ROI. Wider intervals signal decisions that need more caution.</text>')
    svg("roi_uncertainty_intervals.svg", "".join(parts), 1480, 820)


def scenario_ranking() -> None:
    df = pd.read_csv(ROOT / "data" / "scenario_recommendations.csv")
    summary = df.groupby("scenario", as_index=False).agg(avg_lift=("roi_lift", "mean")).sort_values("avg_lift", ascending=True)
    max_abs = max(summary["avg_lift"].abs().max(), 1e-9)
    parts = [title("Scenario ROI Lift", "Counterfactual sponsor strategies ranked by average ROI movement")]
    x0, y0, w = 720, 198, 520
    parts.append(f'<rect x="84" y="165" width="1320" height="566" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
    parts.append(f'<line x1="{x0}" y1="210" x2="{x0}" y2="660" stroke="{INK}" stroke-width="2"/>')
    y = 248
    for _, row in summary.iterrows():
        val = float(row["avg_lift"])
        bw = abs(val) / max_abs * w
        color = GREEN if val >= 0 else RED
        x = x0 if val >= 0 else x0 - bw
        label = str(row["scenario"]).replace("_", " ")
        parts.append(f'<text x="150" y="{y+7}" class="label">{escape(label)}</text>')
        parts.append(f'<rect x="{x:.1f}" y="{y-18}" width="{bw:.1f}" height="34" rx="17" fill="{color}" opacity=".94"/>')
        parts.append(f'<text x="{1260}" y="{y+7}" text-anchor="end" class="label">{val:+.3f}</text>')
        y += 82
    parts.append(f'<text x="150" y="690" class="small">Reading: negative lift scenarios expose fragile sponsor conditions, especially player absence or media cooling.</text>')
    svg("scenario_ranking.svg", "".join(parts), 1480, 780)


def text_embedding_map() -> None:
    df = pd.read_csv(ROOT / "data" / "text_embeddings_reduced.csv").sample(n=520, random_state=42)
    parts = [title("Text Signal Projection", "Real-source news and reference text reduced into a sponsor-attention map")]
    x0, y0, w, h = 110, 166, 1110, 560
    parts.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="22" fill="{PANEL}" stroke="{GRID}"/>')
    colors = {
        "GDELT": ORANGE,
        "Wikimedia": BLUE,
        "Wikimedia_chunk": GREEN,
        "real_match_record_fact": PURPLE,
        "real_text_window": RED,
    }
    for _, row in df.iterrows():
        x = x0 + 52 + float(row["text_x"]) * (w - 104)
        y = y0 + 52 + (1 - float(row["text_y"])) * (h - 104)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.8" fill="{colors.get(str(row["source"]), MUTED)}" opacity=".62"/>')
    lx = 110
    for label, color in colors.items():
        parts.append(f'<circle cx="{lx}" cy="785" r="8" fill="{color}"/>')
        parts.append(f'<text x="{lx+16}" y="791" class="small">{escape(label)}</text>')
        lx += 250
    svg("text_embedding_map.svg", "".join(parts), 1480, 840)


def gnn_explainer() -> None:
    parts = [title("GNN Relationship Explanation", "How Team-Player-Sponsor-Match edges become commercial influence signals")]
    parts.append(f'<rect x="96" y="162" width="1280" height="590" rx="24" fill="{PANEL}" stroke="{GRID}"/>')
    layers = [
        ("Sponsors", 210, [(210, 280, "Adidas", BLUE), (210, 430, "Hyundai", BLUE), (210, 580, "Visa", BLUE)]),
        ("Teams", 520, [(520, 280, "Argentina", GREEN), (520, 430, "Brazil", GREEN), (520, 580, "Spain", GREEN)]),
        ("Players", 830, [(830, 280, "Core player", ORANGE), (830, 430, "Attack unit", ORANGE), (830, 580, "Defense unit", ORANGE)]),
        ("Matches", 1130, [(1130, 355, "Stage", PURPLE), (1130, 505, "Venue", PURPLE)]),
    ]
    edges = [
        ((210, 280), (520, 280), 7),
        ((210, 430), (520, 430), 9),
        ((210, 580), (520, 580), 5),
        ((520, 280), (830, 280), 8),
        ((520, 430), (830, 430), 7),
        ((520, 580), (830, 580), 6),
        ((830, 280), (1130, 355), 6),
        ((830, 430), (1130, 355), 5),
        ((830, 580), (1130, 505), 4),
        ((210, 430), (830, 430), 4),
    ]
    for (x1, y1), (x2, y2), width in edges:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8aa3b4" stroke-width="{width}" opacity=".38"/>')
    for layer, x, nodes in layers:
        parts.append(f'<text x="{x}" y="214" text-anchor="middle" class="h">{layer}</text>')
        for nx, ny, label, color in nodes:
            parts.append(f'<circle cx="{nx}" cy="{ny}" r="54" fill="{color}" opacity=".95"/>')
            parts.append(f'<text x="{nx}" y="{ny+6}" text-anchor="middle" class="label white">{escape(label)}</text>')
    parts.append(f'<rect x="214" y="675" width="1030" height="48" rx="14" fill="#eef7f3" stroke="{GRID}"/>')
    parts.append(f'<text x="730" y="706" text-anchor="middle" class="label">GNN reading: message passing aggregates sponsor fit, player influence, and match context into node-level commercial influence.</text>')
    svg("gnn_relationship_explainer.svg", "".join(parts), 1480, 820)


def dashboard_gallery() -> None:
    cards = [
        ("Discover", "KPI cards + sponsor ranking", GREEN),
        ("Explain", "SHAP drivers + text signals", BLUE),
        ("Predict", "match probability + ROI", ORANGE),
        ("Simulate", "counterfactual ROI lift", PURPLE),
        ("Recommend", "risk-aware strategy", RED),
    ]
    parts = [title("Dashboard Decision Gallery", "The interface follows one sponsor-planning path instead of a loose chart wall")]
    x, y = 90, 210
    for idx, (name, desc, color) in enumerate(cards):
        parts.append(f'<rect x="{x}" y="{y}" width="245" height="310" rx="24" fill="{PANEL}" stroke="{GRID}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="245" height="74" rx="24" fill="{color}"/>')
        parts.append(f'<text x="{x+122}" y="{y+47}" text-anchor="middle" class="h white">{name}</text>')
        parts.append(f'<text x="{x+28}" y="{y+126}" class="label">{escape(desc)}</text>')
        parts.append(f'<polyline points="{x+34},{y+242} {x+82},{y+214} {x+128},{y+232} {x+172},{y+184} {x+214},{y+202}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>')
        if idx < len(cards) - 1:
            parts.append(arrow(x + 252, y + 156, x + 302, y + 156))
        x += 282
    parts.append(f'<text x="100" y="640" class="label">Business interpretation: every page asks one question, then pushes the user toward the next sponsor decision.</text>')
    svg("dashboard_gallery.svg", "".join(parts), 1530, 760)


def main() -> None:
    architecture()
    data_flow()
    model_pipeline()
    shap_importance()
    uncertainty_intervals()
    scenario_ranking()
    text_embedding_map()
    gnn_explainer()
    dashboard_gallery()
    print(f"Generated model visuals in {ASSET_DIR}")


if __name__ == "__main__":
    main()
