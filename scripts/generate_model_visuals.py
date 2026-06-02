from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
ASSET_DIR.mkdir(parents=True, exist_ok=True)


def write_svg(name: str, body: str, width: int = 1280, height: int = 720) -> None:
    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" fill="#f6f8fb"/>
  {body}
</svg>"""
    (ASSET_DIR / name).write_text(svg, encoding="utf-8")


def title(text: str, subtitle: str = "") -> str:
    safe_title = escape(text)
    safe_subtitle = escape(subtitle)
    return f"""
  <text x="64" y="78" font-family="Segoe UI, Arial" font-size="40" font-weight="700" fill="#0d1726">{safe_title}</text>
  <text x="64" y="116" font-family="Segoe UI, Arial" font-size="19" fill="#627085">{safe_subtitle}</text>
"""


def model_pipeline() -> None:
    steps = [
        ("Real sources", "match records, news, Wikimedia", "#0f8b6f"),
        ("Feature store", "FanScore, exposure, sponsor power", "#2457c5"),
        ("Models", "match probability + ROI regression", "#f28c28"),
        ("Risk layer", "intervals, negative ROI probability", "#6d5bd0"),
        ("Recommendations", "scenario ranking and actions", "#c2415d"),
    ]
    parts = [title("Modeling Pipeline", "From real-source signals to sponsor recommendations")]
    x = 58
    for idx, (name, desc, color) in enumerate(steps):
        parts.append(f'<rect x="{x}" y="216" width="210" height="164" rx="18" fill="{color}"/>')
        parts.append(f'<text x="{x+22}" y="274" font-family="Segoe UI, Arial" font-size="24" font-weight="700" fill="#fff">{escape(name)}</text>')
        parts.append(f'<text x="{x+22}" y="316" font-family="Segoe UI, Arial" font-size="15" fill="#eef6ff">{escape(desc)}</text>')
        if idx < len(steps) - 1:
            parts.append(f'<path d="M{x+222} 298H{x+274}" stroke="#0d1726" stroke-width="5"/>')
            parts.append(f'<path d="M{x+274} 298L{x+258} 288V308L{x+274} 298Z" fill="#0d1726"/>')
        x += 244
    parts.append('<rect x="64" y="470" width="1152" height="104" rx="18" fill="#ffffff" stroke="#d7e0ea"/>')
    parts.append('<text x="96" y="528" font-family="Segoe UI, Arial" font-size="24" font-weight="700" fill="#0d1726">Primary target: sponsor ROI. Match probability is used as business context, not the final product.</text>')
    write_svg("model_pipeline.svg", "".join(parts))


def feature_importance() -> None:
    df = pd.read_csv(ROOT / "reports" / "roi_feature_importance.csv").head(10)
    max_val = max(df["importance"].max(), 1e-9)
    parts = [title("ROI Feature Importance", "Top drivers from the current sponsor ROI model")]
    y = 166
    for _, row in df.iterrows():
        feature = str(row["feature"]).replace("_", " ")
        value = float(row["importance"])
        width = 760 * value / max_val
        parts.append(f'<text x="76" y="{y+22}" font-family="Segoe UI, Arial" font-size="17" fill="#0d1726">{escape(feature)}</text>')
        parts.append(f'<rect x="365" y="{y}" width="790" height="30" rx="15" fill="#e8eef5"/>')
        parts.append(f'<rect x="365" y="{y}" width="{width:.1f}" height="30" rx="15" fill="#0f8b6f"/>')
        parts.append(f'<text x="1172" y="{y+22}" font-family="Segoe UI, Arial" font-size="16" fill="#485568">{value:.3f}</text>')
        y += 46
    write_svg("roi_feature_importance.svg", "".join(parts))


def uncertainty_intervals() -> None:
    df = pd.read_csv(ROOT / "data" / "roi_uncertainty.csv").head(36)
    ymin = df["roi_ci_low"].min()
    ymax = df["roi_ci_high"].max()
    span = max(ymax - ymin, 1e-9)
    parts = [title("ROI Prediction Intervals", "Uncertainty layer for sponsor return estimates")]
    chart_x, chart_y, chart_w, chart_h = 82, 170, 1090, 430
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="18" fill="#ffffff" stroke="#d7e0ea"/>')
    for idx, row in df.iterrows():
        x = chart_x + 38 + idx * (chart_w - 86) / max(len(df) - 1, 1)
        low = chart_y + chart_h - 34 - (float(row["roi_ci_low"]) - ymin) / span * (chart_h - 80)
        high = chart_y + chart_h - 34 - (float(row["roi_ci_high"]) - ymin) / span * (chart_h - 80)
        mean = chart_y + chart_h - 34 - (float(row["roi_mean"]) - ymin) / span * (chart_h - 80)
        parts.append(f'<line x1="{x:.1f}" y1="{high:.1f}" x2="{x:.1f}" y2="{low:.1f}" stroke="#2457c5" stroke-width="4" opacity=".32"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{mean:.1f}" r="5" fill="#f28c28"/>')
    parts.append('<text x="92" y="640" font-family="Segoe UI, Arial" font-size="17" fill="#627085">Each vertical band shows the estimated ROI range; orange dots show expected ROI.</text>')
    write_svg("roi_uncertainty_intervals.svg", "".join(parts))


def text_embedding_map() -> None:
    df = pd.read_csv(ROOT / "data" / "text_embeddings_reduced.csv").sample(n=420, random_state=42)
    parts = [title("Text Signal Map", "5,450 real-source text units reduced to two display dimensions")]
    chart_x, chart_y, chart_w, chart_h = 82, 150, 1080, 500
    parts.append(f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="18" fill="#ffffff" stroke="#d7e0ea"/>')
    colors = {
        "GDELT": "#f28c28",
        "Wikimedia": "#2457c5",
        "Wikimedia_chunk": "#0f8b6f",
        "real_match_record_fact": "#6d5bd0",
        "real_text_window": "#c2415d",
    }
    for _, row in df.iterrows():
        x = chart_x + 42 + float(row["text_x"]) * (chart_w - 84)
        y = chart_y + 42 + (1 - float(row["text_y"])) * (chart_h - 84)
        color = colors.get(str(row["source"]), "#627085")
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="{color}" opacity=".58"/>')
    legend_y = 638
    lx = 96
    for label, color in list(colors.items())[:5]:
        parts.append(f'<circle cx="{lx}" cy="{legend_y}" r="7" fill="{color}"/>')
        parts.append(f'<text x="{lx+14}" y="{legend_y+6}" font-family="Segoe UI, Arial" font-size="14" fill="#485568">{escape(label)}</text>')
        lx += 216
    write_svg("text_embedding_map.svg", "".join(parts))


def scenario_ranking() -> None:
    df = pd.read_csv(ROOT / "data" / "scenario_recommendations.csv")
    summary = df.groupby("scenario", as_index=False).agg(avg_lift=("roi_lift", "mean")).sort_values("avg_lift", ascending=False)
    max_abs = max(summary["avg_lift"].abs().max(), 1e-9)
    parts = [title("Scenario Ranking", "Average ROI lift across sponsor strategy simulations")]
    y = 184
    zero_x = 640
    parts.append('<line x1="640" y1="150" x2="640" y2="590" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 8"/>')
    for _, row in summary.iterrows():
        val = float(row["avg_lift"])
        width = 420 * abs(val) / max_abs
        color = "#0f8b6f" if val >= 0 else "#c2415d"
        x = zero_x if val >= 0 else zero_x - width
        parts.append(f'<text x="90" y="{y+22}" font-family="Segoe UI, Arial" font-size="18" fill="#0d1726">{escape(str(row["scenario"]).replace("_", " "))}</text>')
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="30" rx="15" fill="{color}"/>')
        parts.append(f'<text x="1080" y="{y+22}" font-family="Segoe UI, Arial" font-size="17" fill="#485568">{val:+.3f}</text>')
        y += 58
    write_svg("scenario_ranking.svg", "".join(parts))


def data_flow() -> None:
    lanes = [
        ("Raw sources", "World Cup match records\\nGDELT article metadata\\nWikimedia text", "#0f8b6f"),
        ("Evidence tables", "match history\\ntext units\\nsponsor panel\\nweather context", "#2457c5"),
        ("Feature layer", "FanScore\\nSponsor Power\\nMedia Exposure\\nCommercial Momentum", "#f28c28"),
        ("Decision outputs", "ROI prediction\\nrisk intervals\\nscenario ranking\\ndashboard", "#6d5bd0"),
    ]
    parts = [title("Data Flow", "How raw sports, media, and business signals become decision-ready outputs")]
    x = 72
    for idx, (name, desc, color) in enumerate(lanes):
        parts.append(f'<rect x="{x}" y="172" width="246" height="326" rx="22" fill="{color}"/>')
        parts.append(f'<text x="{x+24}" y="230" font-family="Segoe UI, Arial" font-size="25" font-weight="700" fill="#fff">{escape(name)}</text>')
        for line_idx, line in enumerate(desc.split("\\n")):
            parts.append(f'<text x="{x+24}" y="{282 + line_idx * 38}" font-family="Segoe UI, Arial" font-size="18" fill="#eef6ff">{escape(line)}</text>')
        if idx < len(lanes) - 1:
            parts.append(f'<path d="M{x+258} 336H{x+302}" stroke="#0d1726" stroke-width="5"/>')
            parts.append(f'<path d="M{x+302} 336L{x+286} 326V346L{x+302} 336Z" fill="#0d1726"/>')
        x += 304
    write_svg("data_flow.svg", "".join(parts))


def decision_workflow() -> None:
    steps = [
        ("Discover", "market context"),
        ("Explain", "drivers"),
        ("Predict", "ROI"),
        ("Simulate", "strategy"),
        ("Recommend", "action"),
    ]
    parts = [title("Business Decision Workflow", "Dashboard logic designed for sponsor planning, not just chart browsing")]
    cx = 156
    for idx, (name, desc) in enumerate(steps):
        color = ["#0f8b6f", "#2457c5", "#f28c28", "#6d5bd0", "#c2415d"][idx]
        parts.append(f'<circle cx="{cx}" cy="310" r="72" fill="{color}"/>')
        parts.append(f'<text x="{cx}" y="302" font-family="Segoe UI, Arial" font-size="22" font-weight="700" text-anchor="middle" fill="#fff">{name}</text>')
        parts.append(f'<text x="{cx}" y="334" font-family="Segoe UI, Arial" font-size="15" text-anchor="middle" fill="#eef6ff">{desc}</text>')
        if idx < len(steps) - 1:
            parts.append(f'<path d="M{cx+82} 310H{cx+174}" stroke="#0d1726" stroke-width="5"/>')
            parts.append(f'<path d="M{cx+174} 310L{cx+158} 300V320L{cx+174} 310Z" fill="#0d1726"/>')
        cx += 240
    parts.append('<rect x="100" y="492" width="1080" height="88" rx="18" fill="#ffffff" stroke="#d7e0ea"/>')
    parts.append('<text x="132" y="544" font-family="Segoe UI, Arial" font-size="23" font-weight="700" fill="#0d1726">Output: scenario ranking, ROI lift, risk level, and sponsor strategy recommendation.</text>')
    write_svg("decision_workflow.svg", "".join(parts))


def dashboard_gallery() -> None:
    cards = [
        ("ROI Cockpit", "KPI cards, sponsor return, media exposure", "#0f8b6f"),
        ("Text Signals", "5,450 evidence units projected to 24 dims", "#2457c5"),
        ("Risk View", "Prediction intervals and negative ROI risk", "#f28c28"),
        ("Scenario Lab", "Investment, weather, player, stage changes", "#6d5bd0"),
    ]
    parts = [title("Dashboard Gallery", "Four views that turn model outputs into sponsor decisions")]
    coords = [(80, 164), (670, 164), (80, 430), (670, 430)]
    for (name, desc, color), (x, y) in zip(cards, coords):
        parts.append(f'<rect x="{x}" y="{y}" width="530" height="202" rx="22" fill="#fff" stroke="#d7e0ea"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="530" height="58" rx="22" fill="{color}"/>')
        parts.append(f'<text x="{x+28}" y="{y+39}" font-family="Segoe UI, Arial" font-size="23" font-weight="700" fill="#fff">{escape(name)}</text>')
        parts.append(f'<text x="{x+28}" y="{y+98}" font-family="Segoe UI, Arial" font-size="18" fill="#485568">{escape(desc)}</text>')
        parts.append(f'<polyline points="{x+32},{y+162} {x+130},{y+126} {x+226},{y+146} {x+324},{y+102} {x+432},{y+132}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/>')
    write_svg("dashboard_gallery.svg", "".join(parts))


def main() -> None:
    model_pipeline()
    data_flow()
    feature_importance()
    uncertainty_intervals()
    text_embedding_map()
    scenario_ranking()
    decision_workflow()
    dashboard_gallery()
    print(f"Generated model visuals in {ASSET_DIR}")


if __name__ == "__main__":
    main()
