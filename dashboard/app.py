from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
DEMO_MODE = "--demo" in sys.argv

COLORS = {
    "green": "#0f8b6f",
    "blue": "#2457c5",
    "orange": "#f28c28",
    "gold": "#d9a441",
    "red": "#c2415d",
    "ink": "#0d1726",
    "muted": "#6b7a90",
    "line": "#d7e0ea",
}

I18N = {
    "English": {
        "title": "Sports Sponsorship Intelligence Platform",
        "caption": "Discover -> Explain -> Predict -> Simulate -> Recommend: sponsorship ROI, fan attention, uncertainty, and business decision support.",
        "guide_title": "How to use this dashboard",
        "guide_body": "Start with Discover to choose a market context, use Explain/Predict to inspect evidence, then use Simulate/Recommend to choose a sponsor strategy.",
        "filters": "Filters",
        "language": "Language",
        "strategy_templates": "Strategy templates",
        "conservative": "Conservative",
        "balanced": "Balanced",
        "aggressive": "Aggressive",
        "all": "All",
        "team": "Team",
        "sponsor": "Sponsor",
        "stage": "Match stage",
        "year": "Year / round timeline",
        "avg_roi": "Avg Sponsor ROI",
        "avg_fanscore": "Avg FanScore",
        "momentum": "Commercial Momentum",
        "roi_spend": "ROI / $M Spend",
        "discover": "Discover",
        "explain": "Explain",
        "predict": "Predict",
        "simulate": "Simulate",
        "recommend": "Recommend",
        "network": "Network",
        "recommend_title": "Recommend: Scenario Ranking and Sponsor Strategy",
        "strategy_compare": "Strategy Template Comparison: Lift vs Risk",
        "template_hint": "Use the template buttons to filter the recommendation table and compare conservative, balanced, and aggressive strategies.",
        "demo": "Demo mode is active: the app is using committed local artifacts and does not require external APIs.",
    },
    "中文": {
        "title": "体育赞助 ROI 智能决策平台",
        "caption": "发现 -> 解释 -> 预测 -> 模拟 -> 推荐：把粉丝注意力、赞助 ROI、不确定性和商业行动连成闭环。",
        "guide_title": "使用引导",
        "guide_body": "先在 Discover 选择球队、赞助商和阶段，再在 Explain 与 Predict 查看证据，最后用 Simulate 与 Recommend 选择赞助策略。",
        "filters": "筛选器",
        "language": "语言",
        "strategy_templates": "策略模板",
        "conservative": "保守",
        "balanced": "平衡",
        "aggressive": "激进",
        "all": "全部",
        "team": "球队",
        "sponsor": "赞助商",
        "stage": "比赛阶段",
        "year": "年份/时间线",
        "avg_roi": "平均赞助 ROI",
        "avg_fanscore": "平均 FanScore",
        "momentum": "商业动量",
        "roi_spend": "每百万投入 ROI",
        "discover": "发现",
        "explain": "解释",
        "predict": "预测",
        "simulate": "模拟",
        "recommend": "推荐",
        "network": "网络",
        "recommend_title": "推荐：场景排序与赞助策略",
        "strategy_compare": "策略模板对比：收益提升 vs 风险",
        "template_hint": "使用策略按钮筛选推荐表，并对比保守、平衡、激进三类策略。",
        "demo": "Demo 模式已开启：应用使用仓库内本地成果文件，不依赖外部 API。",
    },
}


def tr(key: str) -> str:
    return I18N[st.session_state.get("language", "English")].get(key, key)


def simple_pdf_bytes(title: str, markdown: str) -> bytes:
    lines = [title, ""] + markdown.replace("|", " ").splitlines()
    content_lines = ["BT", "/F1 16 Tf", "50 780 Td"]
    for idx, line in enumerate(lines[:34]):
        size = 16 if idx == 0 else 9
        escaped = line[:96].replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content_lines.extend([f"/F1 {size} Tf", f"({escaped}) Tj", "0 -19 Td"])
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
    return bytes(pdf)


def markdown_table(df: pd.DataFrame, max_rows: int = 120) -> str:
    view = df.head(max_rows)
    headers = list(view.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def download_module(label: str, df: pd.DataFrame, key: str, max_rows: int = 120) -> None:
    export_df = df.head(max_rows).copy()
    md = f"# {label}\n\n" + markdown_table(export_df, max_rows=max_rows)
    cols = st.columns(3)
    cols[0].download_button(
        f"{label} CSV",
        export_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{key}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    cols[1].download_button(
        f"{label} Markdown",
        md.encode("utf-8"),
        file_name=f"{key}.md",
        mime="text/markdown",
        use_container_width=True,
    )
    cols[2].download_button(
        f"{label} PDF",
        simple_pdf_bytes(label, md),
        file_name=f"{key}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


def polish(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=28, r=24, t=58, b=34),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Segoe UI, Arial", color=COLORS["ink"], size=12),
        title_font=dict(size=18, color=COLORS["ink"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor=COLORS["ink"], bordercolor=COLORS["gold"], font=dict(color="#ffffff", size=12)),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(215,224,234,.55)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(215,224,234,.55)", zeroline=False)
    return fig


@st.cache_data
def load_data():
    roi_path = DATA_DIR / "roi_predictions.csv"
    panel_path = DATA_DIR / "panel_dataset.csv"
    roi = pd.read_csv(roi_path) if roi_path.exists() else pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    if "predicted_roi" not in roi and "sponsor_roi" in roi:
        roi["predicted_roi"] = roi["sponsor_roi"]
    panel = pd.read_csv(panel_path) if panel_path.exists() else roi.copy()
    ab = pd.read_csv(REPORT_DIR / "ab_simulation_results.csv") if (REPORT_DIR / "ab_simulation_results.csv").exists() else None
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv") if (DATA_DIR / "roi_uncertainty.csv").exists() else None
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv") if (DATA_DIR / "scenario_recommendations.csv").exists() else None
    network = pd.read_csv(REPORT_DIR / "sponsor_influence_scores.csv") if (REPORT_DIR / "sponsor_influence_scores.csv").exists() else None
    future_roi = pd.read_csv(REPORT_DIR / "future_roi_forecast.csv") if (REPORT_DIR / "future_roi_forecast.csv").exists() else None
    sentiment_events = pd.read_csv(REPORT_DIR / "sentiment_event_roi_impact.csv") if (REPORT_DIR / "sentiment_event_roi_impact.csv").exists() else None
    resource_mix = pd.read_csv(REPORT_DIR / "resource_optimization_top_budget_mix.csv") if (REPORT_DIR / "resource_optimization_top_budget_mix.csv").exists() else None
    graph_attention = pd.read_csv(REPORT_DIR / "graph_attention_roi_contributions.csv") if (REPORT_DIR / "graph_attention_roi_contributions.csv").exists() else None
    extreme = pd.read_csv(REPORT_DIR / "extreme_scenario_roi_risk.csv") if (REPORT_DIR / "extreme_scenario_roi_risk.csv").exists() else None
    commercial = pd.read_csv(DATA_DIR / "commercial_decision_metrics.csv") if (DATA_DIR / "commercial_decision_metrics.csv").exists() else None
    return roi, panel, ab, uncertainty, scenarios, network, future_roi, sentiment_events, resource_mix, graph_attention, extreme, commercial


st.set_page_config(page_title="Sports Sponsorship Intelligence", page_icon="ROI", layout="wide")
(
    roi_df,
    panel_df,
    ab_df,
    uncertainty_df,
    scenarios_df,
    network_df,
    future_roi_df,
    sentiment_events_df,
    resource_mix_df,
    graph_attention_df,
    extreme_df,
    commercial_df,
) = load_data()

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #07140f 0%, #0c1a2a 34%, #f6f8fb 34%); }
    .block-container { padding-top: 1.2rem; }
    h1, h2, h3 { letter-spacing: 0 !important; }
    div[data-testid="stMetric"] {
      background: rgba(255,255,255,.96);
      border: 1px solid rgba(215,224,234,.9);
      border-radius: 14px;
      padding: 14px;
      box-shadow: 0 12px 32px rgba(15, 23, 42, .08);
    }
    div[data-testid="stPlotlyChart"] {
      background: rgba(255,255,255,.97);
      border: 1px solid rgba(215,224,234,.9);
      border-radius: 16px;
      padding: 10px;
      box-shadow: 0 14px 36px rgba(15, 23, 42, .08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.session_state["language"] = st.selectbox("Language / 语言", ["English", "中文"], index=0)

st.title(tr("title"))
st.caption(tr("caption"))
if DEMO_MODE:
    st.success(tr("demo"))
with st.expander(tr("guide_title"), expanded=False):
    st.write(tr("guide_body"))

teams = sorted(panel_df["team"].dropna().unique())
sponsors = sorted(panel_df["sponsor"].dropna().unique())
stages = sorted(panel_df["stage"].dropna().unique())

with st.sidebar:
    st.header(tr("filters"))
    selected_team = st.selectbox(tr("team"), [tr("all")] + teams)
    selected_sponsor = st.selectbox(tr("sponsor"), [tr("all")] + sponsors)
    selected_stage = st.multiselect(tr("stage"), stages, default=stages)
    year_min, year_max = int(panel_df["year"].min()), int(panel_df["year"].max())
    selected_year = st.slider(tr("year"), year_min, year_max, (year_min, year_max), step=4)
    st.subheader(tr("strategy_templates"))
    c1, c2, c3 = st.columns(3)
    if c1.button(tr("conservative"), use_container_width=True):
        st.session_state["strategy_template"] = "conservative"
    if c2.button(tr("balanced"), use_container_width=True):
        st.session_state["strategy_template"] = "balanced"
    if c3.button(tr("aggressive"), use_container_width=True):
        st.session_state["strategy_template"] = "aggressive"
    strategy_template = st.session_state.get("strategy_template", "balanced")

view = panel_df[panel_df["stage"].isin(selected_stage) & panel_df["year"].between(selected_year[0], selected_year[1])].copy()
if selected_team != tr("all"):
    view = view[view["team"].eq(selected_team)]
if selected_sponsor != tr("all"):
    view = view[view["sponsor"].eq(selected_sponsor)]
if view.empty:
    st.warning("No rows match the selected filters. Reset filters to continue.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric(tr("avg_roi"), f"{view['predicted_roi'].mean():.2f}x")
k2.metric(tr("avg_fanscore"), f"{view['fan_score_panel'].mean():.2f}")
k3.metric(tr("momentum"), f"{view['commercial_momentum'].mean():.2f}")
k4.metric(tr("roi_spend"), f"{view['roi_per_million_spend'].mean():.2f}")
with st.expander("KPI export / KPI 导出"):
    kpi_df = pd.DataFrame(
        [
            {"metric": "avg_sponsor_roi", "value": round(view["predicted_roi"].mean(), 4)},
            {"metric": "avg_fanscore", "value": round(view["fan_score_panel"].mean(), 4)},
            {"metric": "commercial_momentum", "value": round(view["commercial_momentum"].mean(), 4)},
            {"metric": "roi_per_million_spend", "value": round(view["roi_per_million_spend"].mean(), 4)},
        ]
    )
    download_module("KPI", kpi_df, "worldcuproi_kpi")

tabs = st.tabs([tr("discover"), tr("explain"), tr("predict"), tr("simulate"), tr("recommend")])

with tabs[0]:
    st.subheader("Discover: Match Context and Win / Draw / Loss Probability")
    match_view = roi_df[roi_df["stage"].isin(selected_stage)].copy()
    if selected_team != tr("all"):
        match_view = match_view[(match_view["team_a"].eq(selected_team)) | (match_view["team_b"].eq(selected_team))]
    match_view["p_team_a_win"] = (1 / (1 + pow(2.71828, -match_view["elo_diff"] / 260))).clip(0.08, 0.84)
    match_view["p_draw"] = (0.30 - (match_view["p_team_a_win"] - 0.5).abs() * 0.28).clip(0.10, 0.34)
    match_view["p_team_b_win"] = (1 - match_view["p_team_a_win"] - match_view["p_draw"]).clip(0.04, 0.84)
    prob_long = match_view.head(24).melt(
        id_vars=["match_id", "team_a", "team_b", "stage"],
        value_vars=["p_team_a_win", "p_draw", "p_team_b_win"],
        var_name="outcome",
        value_name="probability",
    )
    fig = px.bar(
        prob_long,
        x="match_id",
        y="probability",
        color="outcome",
        hover_data=["team_a", "team_b", "stage"],
        color_discrete_map={"p_team_a_win": COLORS["green"], "p_draw": COLORS["orange"], "p_team_b_win": COLORS["blue"]},
        title="Win / Draw / Loss Probability by Match",
    )
    fig.update_layout(barmode="stack", yaxis_tickformat=".0%")
    st.plotly_chart(polish(fig), use_container_width=True)

with tabs[1]:
    st.subheader("Explain: Sponsor ROI, Fan Attention, and Commercial Momentum")
    col_a, col_b = st.columns([1.25, 0.75])
    roi_scatter = px.scatter(
        view,
        x="fan_score_panel",
        y="predicted_roi",
        color="sponsor",
        size="event_attention_m",
        hover_data=["team", "opponent", "stage", "roi_per_million_spend"],
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Sponsor ROI Map: Attention vs Return",
    )
    roi_scatter.update_traces(marker=dict(opacity=0.82, line=dict(width=1.2, color="white")))
    col_a.plotly_chart(polish(roi_scatter), use_container_width=True)
    top_sponsor = view.groupby("sponsor", as_index=False).agg(avg_roi=("predicted_roi", "mean")).sort_values("avg_roi", ascending=False).head(10)
    bar = px.bar(top_sponsor, x="avg_roi", y="sponsor", orientation="h", color="avg_roi", color_continuous_scale=["#56B4E9", "#009E73"], title="Top Sponsor ROI Ranking")
    col_b.plotly_chart(polish(bar), use_container_width=True)

with tabs[2]:
    st.subheader("Predict: FanScore, Player Influence, and ROI Confidence")
    radar_values = [
        view["player_followers_m"].mean(),
        view["event_attention_m"].mean(),
        view["media_reposts_k"].mean() / 10,
        view["fan_score_panel"].mean() * 100,
        view["commercial_momentum"].mean() * 100,
    ]
    radar_labels = ["Player followers", "Event attention", "Media reposts", "FanScore", "Momentum"]
    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(r=radar_values + [radar_values[0]], theta=radar_labels + [radar_labels[0]], fill="toself", name="Fan influence profile", line=dict(color=COLORS["green"], width=4)))
    radar.update_layout(title="Fan Influence Radar", polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(polish(radar), use_container_width=True)
    if uncertainty_df is not None:
        interval = uncertainty_df.head(60)
        interval_fig = go.Figure()
        interval_fig.add_trace(go.Scatter(x=interval["match_id"], y=interval["roi_ci_high"], mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
        interval_fig.add_trace(go.Scatter(x=interval["match_id"], y=interval["roi_ci_low"], mode="lines", fill="tonexty", fillcolor="rgba(36,87,197,.20)", line=dict(width=0), name="ROI interval"))
        interval_fig.add_trace(go.Scatter(x=interval["match_id"], y=interval["roi_mean"], mode="lines+markers", line=dict(color=COLORS["blue"], width=3), marker=dict(color=COLORS["orange"], size=7), name="ROI mean"))
        interval_fig.update_layout(title="Conformal-Style ROI Prediction Interval")
        st.plotly_chart(polish(interval_fig), use_container_width=True)
        with st.expander("Risk export / 风险导出"):
            download_module("Risk", uncertainty_df, "worldcuproi_risk")

    col_future, col_sentiment = st.columns(2)
    if future_roi_df is not None and not future_roi_df.empty:
        future_fig = px.line(
            future_roi_df,
            x="cycle",
            y="forecast_roi",
            markers=True,
            title="Future World Cup Cycle ROI Forecast",
            hover_data=["trend_slope_per_cycle", "forecast_note"],
        )
        future_fig.update_traces(line=dict(color=COLORS["green"], width=4), marker=dict(size=10, color=COLORS["orange"]))
        col_future.plotly_chart(polish(future_fig), use_container_width=True)
        with col_future.expander("Future ROI export"):
            download_module("Future ROI Trend", future_roi_df, "worldcuproi_future_roi")
    if sentiment_events_df is not None and not sentiment_events_df.empty:
        sentiment_fig = px.bar(
            sentiment_events_df,
            x="event_type",
            y="avg_roi_delta",
            color="avg_roi_delta",
            color_continuous_scale=[COLORS["red"], COLORS["gold"], COLORS["green"]],
            hover_data=["stage", "avg_attention_sentiment", "avg_conversion", "samples"],
            title="Key Event Sentiment Impact on ROI",
        )
        col_sentiment.plotly_chart(polish(sentiment_fig), use_container_width=True)
        with col_sentiment.expander("Sentiment event export"):
            download_module("Sentiment Event Impact", sentiment_events_df, "worldcuproi_sentiment_events")

with tabs[3]:
    st.subheader("Simulate: Weather, Venue, and Stage Impact")
    heat = view.groupby(["weather", "stage"], as_index=False).agg(avg_roi=("predicted_roi", "mean"), avg_momentum=("commercial_momentum", "mean"), matches=("match_id", "count"))
    heatmap = px.density_heatmap(
        heat,
        x="stage",
        y="weather",
        z="avg_roi",
        histfunc="avg",
        color_continuous_scale=["#f8fbff", "#bce7d1", COLORS["green"], COLORS["orange"]],
        hover_data=["matches", "avg_momentum"],
        title="Weather x Stage ROI Heatmap",
    )
    heatmap.update_traces(xgap=3, ygap=3)
    st.plotly_chart(polish(heatmap), use_container_width=True)
    weather_scatter = px.scatter(view, x="temperature_c", y="predicted_roi", color="result_for_team", size="sponsor_power_index", hover_data=["team", "opponent", "weather", "stage"], title="Temperature, Venue Context, and Sponsor ROI")
    st.plotly_chart(polish(weather_scatter), use_container_width=True)
    col_budget, col_extreme = st.columns(2)
    if resource_mix_df is not None and not resource_mix_df.empty:
        budget_fig = px.scatter(
            resource_mix_df,
            x="budget_m",
            y="risk_adjusted_roi",
            size="media_multiplier",
            color="sponsor",
            hover_data=["expected_roi", "risk_penalty", "recommendation"],
            title="Budget x Media Optimization: Risk-Adjusted ROI",
        )
        col_budget.plotly_chart(polish(budget_fig), use_container_width=True)
        with col_budget.expander("Resource optimization export"):
            download_module("Resource Optimization", resource_mix_df, "worldcuproi_resource_mix")
    if extreme_df is not None and not extreme_df.empty:
        extreme_top = extreme_df.sort_values("scenario_roi", ascending=False).head(160)
        extreme_fig = px.box(
            extreme_top,
            x="extreme_scenario",
            y="scenario_roi",
            color="extreme_scenario",
            points=False,
            title="Extreme Scenario ROI Stress Test",
        )
        col_extreme.plotly_chart(polish(extreme_fig), use_container_width=True)
        with col_extreme.expander("Extreme scenario export"):
            download_module("Extreme Scenario", extreme_df, "worldcuproi_extreme_scenarios")

with tabs[4]:
    st.subheader(tr("recommend_title"))
    st.info(tr("template_hint"))
    if scenarios_df is not None:
        scenarios_view = scenarios_df[scenarios_df["strategy_type"].eq(strategy_template)].copy() if "strategy_type" in scenarios_df else scenarios_df.copy()
        compare = scenarios_df.groupby("strategy_type", as_index=False).agg(avg_roi_lift=("roi_lift", "mean"), avg_risk=("risk_score", "mean"), avg_scenario_roi=("scenario_roi", "mean"))
        lift_risk = px.scatter(compare, x="avg_risk", y="avg_roi_lift", size="avg_scenario_roi", color="strategy_type", color_discrete_map={"conservative": COLORS["blue"], "balanced": COLORS["green"], "aggressive": COLORS["orange"]}, title=tr("strategy_compare"))
        st.plotly_chart(polish(lift_risk), use_container_width=True)
        roi_compare = px.bar(compare, x="strategy_type", y=["avg_roi_lift", "avg_risk"], barmode="group", title="Strategy Comparison: Lift and Risk")
        st.plotly_chart(polish(roi_compare), use_container_width=True)
        scenario_summary = scenarios_df.groupby("scenario", as_index=False).agg(avg_roi_lift=("roi_lift", "mean"), avg_scenario_roi=("scenario_roi", "mean"))
        scenario_fig = px.bar(scenario_summary, x="scenario", y="avg_roi_lift", color="avg_roi_lift", color_continuous_scale=[COLORS["red"], COLORS["orange"], COLORS["green"]], hover_data=["avg_scenario_roi"], title="Scenario Ranking: ROI Lift by Strategy")
        st.plotly_chart(polish(scenario_fig), use_container_width=True)
        st.dataframe(scenarios_view.sort_values(["scenario_rank", "roi_lift"], ascending=[True, False]).head(80), use_container_width=True)
        with st.expander("Scenario export / 场景导出"):
            download_module("Scenario", scenarios_view, "worldcuproi_scenario")
    elif ab_df is not None:
        st.dataframe(ab_df.sort_values("predicted_roi", ascending=False).head(80), use_container_width=True)
        download_module("Scenario", ab_df, "worldcuproi_ab_scenario")
    else:
        st.info("Run `python src/scenario_engine.py` or `python src/ab_simulation.py` to generate scenario results.")

    st.divider()
    st.subheader("Network: Sponsor-Team-Player Influence")
    if network_df is not None:
        network_view = network_df.copy()
        network_view["sponsor"] = network_view["source"].str.replace("sponsor:", "", regex=False)
        bubble = px.scatter(
            network_view,
            x="pagerank",
            y="sponsor_influence",
            size="connected_nodes",
            color="avg_edge_weight",
            hover_data=["sponsor", "betweenness", "closeness"],
            color_continuous_scale=["#56B4E9", "#009E73", "#E69F00"],
            title="Sponsor Influence: Centrality vs Commercial Strength",
        )
        st.plotly_chart(polish(bubble), use_container_width=True)
        st.dataframe(network_view.sort_values("sponsor_influence", ascending=False), use_container_width=True)
        with st.expander("Network export / 网络导出"):
            download_module("Network", network_view, "worldcuproi_network")
    else:
        st.info("Run `python src/graph_analysis.py` to generate network outputs.")
    st.divider()
    st.subheader("Deep Decision Layer: Commercial Score and Graph Attention")
    col_score, col_attention = st.columns(2)
    if commercial_df is not None and not commercial_df.empty:
        commercial_view = commercial_df.sort_values("commercial_decision_score", ascending=False).head(20).copy()
        commercial_view["pair"] = commercial_view["team"].astype(str) + " x " + commercial_view["sponsor"].astype(str)
        score_fig = px.bar(
            commercial_view,
            x="commercial_decision_score",
            y="pair",
            orientation="h",
            color="commercial_decision_score",
            color_continuous_scale=[COLORS["blue"], COLORS["green"], COLORS["orange"]],
            title="Integrated Commercial Decision Score",
            hover_data=["media_value_index", "fan_conversion_rate", "social_spread_index", "brand_influence_score"],
        )
        col_score.plotly_chart(polish(score_fig), use_container_width=True)
        with col_score.expander("Commercial score export"):
            download_module("Commercial Decision Score", commercial_df, "worldcuproi_commercial_score")
    if graph_attention_df is not None and not graph_attention_df.empty:
        attention_view = graph_attention_df.sort_values("attention_roi_contribution", ascending=False).head(18).copy()
        attention_view["node_label"] = attention_view["node"].astype(str).str.replace("sponsor:", "", regex=False)
        attention_fig = px.bar(
            attention_view,
            x="attention_roi_contribution",
            y="node_label",
            orientation="h",
            color="attention_roi_contribution",
            color_continuous_scale=[COLORS["blue"], COLORS["green"], COLORS["orange"]],
            title="Graph Attention ROI Contribution",
            hover_data=["gat_attention_score", "node_importance_score", "avg_roi"],
        )
        col_attention.plotly_chart(polish(attention_fig), use_container_width=True)
        with col_attention.expander("Graph attention export"):
            download_module("Graph Attention", graph_attention_df, "worldcuproi_graph_attention")
