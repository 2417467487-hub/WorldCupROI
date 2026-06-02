from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


st.set_page_config(page_title="Sports Sponsorship Intelligence", page_icon="ROI", layout="wide")

WORLD_CUP_COLORS = {
    "green": "#0f8b6f",
    "blue": "#2457c5",
    "orange": "#f28c28",
    "gold": "#d9a441",
    "red": "#c2415d",
    "ink": "#0d1726",
    "muted": "#6b7a90",
    "card": "#ffffff",
    "line": "#d7e0ea",
}


def polish(fig: go.Figure, height: int = 430) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=28, r=24, t=58, b=34),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter, Segoe UI, Arial", color=WORLD_CUP_COLORS["ink"], size=12),
        title_font=dict(size=18, color=WORLD_CUP_COLORS["ink"]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,.72)",
            bordercolor="rgba(215,224,234,.8)",
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor="#0d1726",
            bordercolor="#d9a441",
            font=dict(color="#ffffff", size=12),
        ),
        transition_duration=550,
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(215,224,234,.55)",
        zeroline=False,
        linecolor="rgba(13,23,38,.25)",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(215,224,234,.55)",
        zeroline=False,
        linecolor="rgba(13,23,38,.25)",
    )
    return fig


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None]:
    roi_path = DATA_DIR / "roi_predictions.csv"
    panel_path = DATA_DIR / "panel_dataset.csv"
    if roi_path.exists():
        roi = pd.read_csv(roi_path)
    else:
        roi = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
        roi["predicted_roi"] = roi["sponsor_roi"]
    if panel_path.exists():
        panel = pd.read_csv(panel_path)
    else:
        panel = roi.copy()
    ab_path = REPORT_DIR / "ab_simulation_results.csv"
    ab = pd.read_csv(ab_path) if ab_path.exists() else None
    uncertainty_path = DATA_DIR / "roi_uncertainty.csv"
    scenarios_path = DATA_DIR / "scenario_recommendations.csv"
    uncertainty = pd.read_csv(uncertainty_path) if uncertainty_path.exists() else None
    scenarios = pd.read_csv(scenarios_path) if scenarios_path.exists() else None
    return roi, panel, ab, uncertainty, scenarios


roi_df, panel_df, ab, uncertainty, scenarios = load_data()

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #07140f 0%, #0c1a2a 34%, #f6f8fb 34%); }
    .block-container { padding-top: 1.2rem; }
    h1, h2, h3 { letter-spacing: 0 !important; }
    div[data-testid="stVerticalBlock"] > div {
      transition: transform .18s ease, box-shadow .18s ease;
    }
    div[data-testid="stMetric"] {
      background: rgba(255,255,255,.96);
      border: 1px solid rgba(215,224,234,.9);
      border-radius: 14px;
      padding: 14px;
      box-shadow: 0 12px 32px rgba(15, 23, 42, .08);
    }
    div[data-testid="stMetric"]:hover {
      transform: translateY(-2px);
      box-shadow: 0 16px 40px rgba(15, 23, 42, .13);
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

st.title("Sports Sponsorship Intelligence Platform")
st.caption("Discover -> Explain -> Predict -> Simulate -> Recommend: sponsorship ROI, fan attention, uncertainty, and business decision support.")

teams = sorted(panel_df["team"].unique()) if "team" in panel_df else sorted(roi_df["team_a"].unique())
sponsors = sorted(panel_df["sponsor"].unique()) if "sponsor" in panel_df else sorted(roi_df["a_sponsor"].unique())
stages = sorted(panel_df["stage"].unique())
players = sorted(panel_df["team"].unique())

with st.sidebar:
    st.header("Filters")
    selected_team = st.selectbox("Team", ["All"] + teams)
    selected_sponsor = st.selectbox("Sponsor", ["All"] + sponsors)
    selected_player_proxy = st.selectbox("Player / team proxy", ["All"] + players)
    selected_stage = st.multiselect("Match stage", stages, default=stages)
    year_min, year_max = int(panel_df["year"].min()), int(panel_df["year"].max())
    selected_year = st.slider("Year / round timeline", year_min, year_max, (year_min, year_max), step=4)

view = panel_df[
    panel_df["stage"].isin(selected_stage)
    & panel_df["year"].between(selected_year[0], selected_year[1])
].copy()
if selected_team != "All":
    view = view[view["team"] == selected_team]
if selected_sponsor != "All":
    view = view[view["sponsor"] == selected_sponsor]
if selected_player_proxy != "All":
    view = view[view["team"] == selected_player_proxy]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Avg Sponsor ROI", f"{view['predicted_roi'].mean():.2f}x")
k2.metric("Avg FanScore", f"{view['fan_score_panel'].mean():.2f}")
k3.metric("Commercial Momentum", f"{view['commercial_momentum'].mean():.2f}")
k4.metric("ROI / $M Spend", f"{view['roi_per_million_spend'].mean():.2f}")

tab_match, tab_roi, tab_fan, tab_weather, tab_ab = st.tabs(
    ["Discover", "Explain", "Predict", "Simulate", "Recommend"]
)

with tab_match:
    st.subheader("Discover: Match Context and Win / Draw / Loss Probability")
    match_view = roi_df.copy()
    if selected_stage:
        match_view = match_view[match_view["stage"].isin(selected_stage)]
    if selected_team != "All":
        match_view = match_view[(match_view["team_a"] == selected_team) | (match_view["team_b"] == selected_team)]
    match_view = match_view.assign(
        p_team_a_win=(1 / (1 + pow(2.71828, -match_view["elo_diff"] / 260))).clip(0.08, 0.84),
    )
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
        color_discrete_map={"p_team_a_win": "#0f8b6f", "p_draw": "#f28c28", "p_team_b_win": "#2457c5"},
        title="Win / Draw / Loss Probability by Match",
    )
    fig.update_traces(marker_line_color="rgba(255,255,255,.75)", marker_line_width=1.4)
    fig.update_layout(barmode="stack", yaxis_tickformat=".0%")
    st.plotly_chart(polish(fig), use_container_width=True)

with tab_roi:
    st.subheader("Explain: Sponsor ROI, Fan Attention, and Commercial Momentum")
    c1, c2 = st.columns([1.25, 0.75])
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
    c1.plotly_chart(polish(roi_scatter), use_container_width=True)
    roi_value = min(100, max(0, view["predicted_roi"].mean() / 4.2 * 100))
    ring = go.Figure(
        go.Pie(
            values=[roi_value, 100 - roi_value],
            hole=0.72,
            labels=["ROI progress", "Remaining"],
            marker_colors=["#f28c28", "#e8eef5"],
            textinfo="none",
            hoverinfo="label+percent",
            sort=False,
            direction="clockwise",
        )
    )
    ring.update_layout(
        title="Sponsor ROI Progress",
        annotations=[dict(text=f"{roi_value:.0f}%", showarrow=False, font_size=28, font_color=WORLD_CUP_COLORS["ink"])],
        showlegend=False,
    )
    c2.plotly_chart(polish(ring), use_container_width=True)

with tab_fan:
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
    radar.add_trace(
        go.Scatterpolar(
            r=radar_values + [radar_values[0]],
            theta=radar_labels + [radar_labels[0]],
            fill="toself",
            name="Fan influence profile",
            line=dict(color="#0f8b6f", width=4),
            fillcolor="rgba(15,139,111,.24)",
            marker=dict(size=8, color="#f28c28", line=dict(width=2, color="#ffffff")),
        )
    )
    radar.update_layout(
        title="Fan Influence Radar",
        polar=dict(
            bgcolor="rgba(15,139,111,.04)",
            radialaxis=dict(visible=True, gridcolor="rgba(13,23,38,.16)", linecolor="rgba(13,23,38,.20)"),
            angularaxis=dict(gridcolor="rgba(13,23,38,.12)"),
        ),
        showlegend=False,
    )
    st.plotly_chart(polish(radar), use_container_width=True)
    if uncertainty is not None:
        interval = uncertainty.head(60)
        interval_fig = go.Figure()
        interval_fig.add_trace(
            go.Scatter(
                x=interval["match_id"],
                y=interval["roi_ci_high"],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        interval_fig.add_trace(
            go.Scatter(
                x=interval["match_id"],
                y=interval["roi_ci_low"],
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(36,87,197,.20)",
                line=dict(width=0),
                name="ROI interval",
            )
        )
        interval_fig.add_trace(
            go.Scatter(
                x=interval["match_id"],
                y=interval["roi_mean"],
                mode="lines+markers",
                line=dict(color="#2457c5", width=3),
                marker=dict(color="#f28c28", size=7),
                name="ROI mean",
            )
        )
        interval_fig.update_layout(title="Conformal-Style ROI Prediction Interval")
        st.plotly_chart(polish(interval_fig), use_container_width=True)

with tab_weather:
    st.subheader("Simulate: Weather, Venue, and Stage Impact")
    heat = (
        view.groupby(["weather", "stage"], as_index=False)
        .agg(avg_roi=("predicted_roi", "mean"), avg_momentum=("commercial_momentum", "mean"), matches=("match_id", "count"))
    )
    heatmap = px.density_heatmap(
        heat,
        x="stage",
        y="weather",
        z="avg_roi",
        histfunc="avg",
        color_continuous_scale=["#f8fbff", "#bce7d1", "#0f8b6f", "#f28c28"],
        hover_data=["matches", "avg_momentum"],
        title="Weather x Stage ROI Heatmap",
    )
    heatmap.update_traces(xgap=3, ygap=3)
    st.plotly_chart(polish(heatmap), use_container_width=True)
    weather_scatter = px.scatter(
            view,
            x="temperature_c",
            y="predicted_roi",
            color="result_for_team",
            size="sponsor_power_index",
            hover_data=["team", "opponent", "weather", "stage"],
            color_discrete_sequence=["#0f8b6f", "#f28c28", "#2457c5"],
            title="Temperature, Venue Context, and Sponsor ROI",
        )
    weather_scatter.update_traces(marker=dict(opacity=0.78, line=dict(width=1, color="#ffffff")))
    st.plotly_chart(polish(weather_scatter), use_container_width=True)

with tab_ab:
    st.subheader("Recommend: Scenario Ranking and Sponsor Strategy")
    if scenarios is not None:
        scenario_summary = scenarios.groupby("scenario", as_index=False).agg(
            avg_roi_lift=("roi_lift", "mean"),
            avg_scenario_roi=("scenario_roi", "mean"),
        )
        scenario_fig = px.bar(
            scenario_summary,
            x="scenario",
            y="avg_roi_lift",
            color="avg_roi_lift",
            color_continuous_scale=["#c2415d", "#f28c28", "#0f8b6f"],
            hover_data=["avg_scenario_roi"],
            title="Scenario Ranking: ROI Lift by Strategy",
        )
        st.plotly_chart(polish(scenario_fig), use_container_width=True)
        st.dataframe(
            scenarios.sort_values(["scenario_rank", "roi_lift"], ascending=[True, False]).head(80),
            use_container_width=True,
        )
    elif ab is None:
        st.info("Run `python src/scenario_engine.py` or `python src/ab_simulation.py` to generate scenario results.")
    else:
        summary = ab.groupby("scenario", as_index=False).agg(
            avg_predicted_roi=("predicted_roi", "mean"),
            avg_roi_lift_pct=("roi_lift_pct", "mean"),
        )
        fig = px.bar(
            summary,
            x="scenario",
            y="avg_roi_lift_pct",
            color="avg_roi_lift_pct",
            color_continuous_scale=["#c2415d", "#f28c28", "#0f8b6f"],
            hover_data=["avg_predicted_roi"],
            title="Counterfactual ROI Lift by Scenario",
        )
        fig.update_traces(marker_line_color="rgba(255,255,255,.82)", marker_line_width=1.5)
        st.plotly_chart(polish(fig), use_container_width=True)
        st.dataframe(ab.sort_values("predicted_roi", ascending=False).head(80), use_container_width=True)
