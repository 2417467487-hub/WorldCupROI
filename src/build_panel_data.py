from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DASHBOARD_DIR = ROOT / "dashboard"
REPORT_DIR = ROOT / "reports"


def ensure_predictions() -> None:
    if not (DATA_DIR / "roi_predictions.csv").exists():
        from train_roi_model import main as train_roi

        train_roi()


def normalized(s: pd.Series) -> pd.Series:
    span = s.max() - s.min()
    if span == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / span


def result_for_team(row: pd.Series) -> str:
    if row["result"] == "draw":
        return "draw"
    if row["team_side"] == "A" and row["result"] == "A_win":
        return "win"
    if row["team_side"] == "B" and row["result"] == "B_win":
        return "win"
    return "loss"


def build_team_panel(df: pd.DataFrame) -> pd.DataFrame:
    a_cols = {
        "team_a": "team",
        "team_b": "opponent",
        "a_sponsor": "sponsor",
        "a_sponsor_spend_m": "sponsor_spend_m",
        "a_sponsor_power_index": "sponsor_power_index",
        "a_brand_fit": "brand_fit",
        "a_activation_quality": "activation_quality",
        "a_historical_sports_presence": "historical_sports_presence",
        "a_player_followers_m": "player_followers_m",
        "a_core_player_rating": "core_player_rating",
        "a_core_market_value_m": "core_market_value_m",
        "a_elo": "team_elo",
    }
    b_cols = {
        "team_b": "team",
        "team_a": "opponent",
        "b_sponsor": "sponsor",
        "b_sponsor_spend_m": "sponsor_spend_m",
        "b_sponsor_power_index": "sponsor_power_index",
        "b_brand_fit": "brand_fit",
        "b_activation_quality": "activation_quality",
        "b_historical_sports_presence": "historical_sports_presence",
        "b_player_followers_m": "player_followers_m",
        "b_core_player_rating": "core_player_rating",
        "b_core_market_value_m": "core_market_value_m",
        "b_elo": "team_elo",
    }
    shared = [
        "match_id",
        "year",
        "stage",
        "stadium_capacity_k",
        "temperature_c",
        "humidity",
        "weather",
        "event_attention_m",
        "media_reposts_k",
        "result",
        "predicted_roi",
    ]
    panel_a = df[shared + list(a_cols.keys())].rename(columns=a_cols)
    panel_a["team_side"] = "A"
    panel_b = df[shared + list(b_cols.keys())].rename(columns=b_cols)
    panel_b["team_side"] = "B"
    panel = pd.concat([panel_a, panel_b], ignore_index=True)

    panel["result_for_team"] = panel.apply(result_for_team, axis=1)
    panel["match_points"] = panel["result_for_team"].map({"win": 3, "draw": 1, "loss": 0})
    panel["exposure_score"] = (
        0.55 * normalized(panel["event_attention_m"])
        + 0.30 * normalized(panel["media_reposts_k"])
        + 0.15 * normalized(panel["stadium_capacity_k"])
    )
    panel["fan_score_panel"] = (
        0.50 * normalized(panel["player_followers_m"])
        + 0.30 * normalized(panel["event_attention_m"])
        + 0.20 * normalized(panel["media_reposts_k"])
    )
    panel["commercial_momentum"] = (
        0.38 * panel["fan_score_panel"]
        + 0.34 * panel["sponsor_power_index"]
        + 0.18 * panel["exposure_score"]
        + 0.10 * normalized(panel["match_points"])
    )
    panel["roi_per_million_spend"] = (panel["predicted_roi"] / panel["sponsor_spend_m"]).round(3)
    panel["attention_segment"] = pd.cut(
        panel["fan_score_panel"],
        bins=[-0.01, 0.33, 0.66, 1.01],
        labels=["Low attention", "Mid attention", "High attention"],
    ).astype(str)
    panel["commercial_segment"] = pd.cut(
        panel["commercial_momentum"],
        bins=[-0.01, 0.38, 0.62, 1.01],
        labels=["Watchlist", "Scalable", "Premium"],
    ).astype(str)
    panel["panel_id"] = (
        panel["year"].astype(str)
        + "_"
        + panel["match_id"].astype(str)
        + "_"
        + panel["team"].str.replace(" ", "_", regex=False)
    )

    ordered_cols = [
        "panel_id",
        "year",
        "match_id",
        "team",
        "opponent",
        "team_side",
        "stage",
        "sponsor",
        "result_for_team",
        "match_points",
        "team_elo",
        "core_player_rating",
        "core_market_value_m",
        "player_followers_m",
        "event_attention_m",
        "media_reposts_k",
        "exposure_score",
        "fan_score_panel",
        "sponsor_spend_m",
        "sponsor_power_index",
        "brand_fit",
        "activation_quality",
        "commercial_momentum",
        "predicted_roi",
        "roi_per_million_spend",
        "attention_segment",
        "commercial_segment",
        "weather",
        "temperature_c",
        "humidity",
    ]
    return panel[ordered_cols].round(3)


def aggregate_panel(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    team_year = (
        panel.groupby(["year", "team", "sponsor"], as_index=False)
        .agg(
            matches=("match_id", "count"),
            avg_roi=("predicted_roi", "mean"),
            avg_fan_score=("fan_score_panel", "mean"),
            avg_sponsor_power=("sponsor_power_index", "mean"),
            avg_commercial_momentum=("commercial_momentum", "mean"),
            total_media_reposts_k=("media_reposts_k", "sum"),
            total_event_attention_m=("event_attention_m", "sum"),
            points=("match_points", "sum"),
        )
        .round(3)
    )
    sponsor_summary = (
        panel.groupby("sponsor", as_index=False)
        .agg(
            teams=("team", "nunique"),
            exposure_events=("panel_id", "count"),
            avg_roi=("predicted_roi", "mean"),
            avg_roi_per_million_spend=("roi_per_million_spend", "mean"),
            avg_commercial_momentum=("commercial_momentum", "mean"),
            high_attention_share=("attention_segment", lambda x: round((x == "High attention").mean(), 3)),
        )
        .sort_values("avg_roi", ascending=False)
        .round(3)
    )
    return team_year, sponsor_summary


def build_html(panel: pd.DataFrame, sponsor_summary: pd.DataFrame) -> str:
    payload = {
        "panel": panel.to_dict(orient="records"),
        "sponsors": sponsor_summary.to_dict(orient="records"),
        "teams": sorted(panel["team"].unique().tolist()),
        "sponsorNames": sorted(panel["sponsor"].unique().tolist()),
        "stages": sorted(panel["stage"].unique().tolist()),
        "segments": ["Watchlist", "Scalable", "Premium"],
    }
    payload_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WorldCupROI Intelligence Platform</title>
  <style>
    :root {{
      --ink: #0d1726;
      --muted: #6b7a90;
      --line: #d7e0ea;
      --surface: rgba(255, 255, 255, .96);
      --bg: #07140f;
      --green: #0f8b6f;
      --pitch: #0e7a4f;
      --blue: #2457c5;
      --gold: #d9a441;
      --rose: #c2415d;
      --violet: #6d5bd0;
      --grass2: #0b5f3f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background:
        radial-gradient(circle at 18% 0%, rgba(217,164,65,.24), transparent 28%),
        radial-gradient(circle at 82% 8%, rgba(15,139,111,.25), transparent 30%),
        linear-gradient(180deg, #07140f 0%, #0c1a2a 52%, #f4f7fb 52%, #f4f7fb 100%);
      color: var(--ink);
    }}
    header {{
      position: relative;
      overflow: hidden;
      padding: 30px 34px 24px;
      color: #fff;
      border-bottom: 1px solid rgba(255,255,255,.16);
    }}
    header::before {{
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(115deg, rgba(255,255,255,.12), transparent 22%),
        radial-gradient(circle at 50% 20%, rgba(255,255,255,.14), transparent 16%);
      pointer-events: none;
    }}
    .hero {{
      position: relative;
      display: grid;
      grid-template-columns: minmax(280px, 1.1fr) minmax(280px, .9fr);
      gap: 28px;
      align-items: stretch;
      z-index: 1;
    }}
    h1 {{ margin: 0; font-size: clamp(34px, 5vw, 66px); line-height: .95; letter-spacing: 0; max-width: 780px; }}
    .eyebrow {{ display: inline-flex; align-items: center; gap: 8px; margin-bottom: 12px; color: #ffe7ad; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; font-size: 12px; }}
    .deck {{ margin-top: 14px; max-width: 820px; color: rgba(255,255,255,.82); line-height: 1.6; font-size: 15px; }}
    .hero-actions {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
    .hero-pill {{ border: 1px solid rgba(255,255,255,.22); background: rgba(255,255,255,.10); color: #fff; border-radius: 999px; padding: 9px 12px; font-size: 12px; font-weight: 800; backdrop-filter: blur(8px); }}
    .stadium-card {{
      min-height: 238px;
      position: relative;
      border-radius: 18px;
      border: 1px solid rgba(255,255,255,.20);
      background:
        linear-gradient(90deg, rgba(255,255,255,.10) 1px, transparent 1px) 0 0 / 38px 38px,
        linear-gradient(0deg, rgba(255,255,255,.08) 1px, transparent 1px) 0 0 / 38px 38px,
        linear-gradient(135deg, rgba(14,122,79,.95), rgba(11,95,63,.95));
      box-shadow: 0 24px 80px rgba(0,0,0,.28);
      overflow: hidden;
    }}
    .pitch-line {{ position: absolute; inset: 25px; border: 2px solid rgba(255,255,255,.48); border-radius: 12px; }}
    .pitch-line::before {{ content: ""; position: absolute; top: 0; bottom: 0; left: 50%; border-left: 2px solid rgba(255,255,255,.42); }}
    .pitch-line::after {{ content: ""; position: absolute; width: 86px; height: 86px; border: 2px solid rgba(255,255,255,.42); border-radius: 50%; left: calc(50% - 43px); top: calc(50% - 43px); }}
    .trophy {{
      position: absolute; right: 30px; top: 30px; width: 82px; height: 116px;
      background: linear-gradient(160deg, #fff1b8, #d9a441 45%, #8a5a00);
      clip-path: polygon(31% 0, 69% 0, 76% 16%, 88% 20%, 76% 44%, 63% 47%, 58% 70%, 72% 84%, 72% 100%, 28% 100%, 28% 84%, 42% 70%, 37% 47%, 24% 44%, 12% 20%, 24% 16%);
      filter: drop-shadow(0 12px 18px rgba(0,0,0,.30));
    }}
    .ball {{
      position: absolute; left: 16%; bottom: 18%; width: 42px; height: 42px; border-radius: 50%;
      background: radial-gradient(circle at 35% 30%, #fff 0 22%, #111 23% 30%, #fff 31% 52%, #111 53% 60%, #fff 61%);
      animation: roll 5.6s ease-in-out infinite;
      box-shadow: 0 10px 22px rgba(0,0,0,.30);
    }}
    @keyframes roll {{ 0%,100% {{ transform: translateX(0) rotate(0deg); }} 50% {{ transform: translateX(220px) rotate(260deg); }} }}
    .score-chip {{ position: absolute; left: 28px; bottom: 28px; background: rgba(3,7,18,.58); color: #fff; border: 1px solid rgba(255,255,255,.20); border-radius: 12px; padding: 12px 14px; backdrop-filter: blur(8px); }}
    .score-chip span {{ display: block; color: #f8d77a; font-size: 12px; font-weight: 800; }}
    .score-chip strong {{ font-size: 24px; }}
    nav {{ display: flex; gap: 8px; padding: 12px 34px; background: rgba(5,15,25,.90); border-bottom: 1px solid rgba(255,255,255,.10); position: sticky; top: 0; z-index: 4; backdrop-filter: blur(12px); }}
    .tab-btn {{ border: 1px solid rgba(255,255,255,.14); background: rgba(255,255,255,.08); color: rgba(255,255,255,.78); padding: 10px 15px; border-radius: 999px; cursor: pointer; font-weight: 800; transition: transform .18s ease, background .18s ease; }}
    .tab-btn:hover {{ transform: translateY(-1px); background: rgba(255,255,255,.14); }}
    .tab-btn.active {{ color: #172033; background: linear-gradient(135deg, #ffe8a3, #d9a441); border-color: transparent; }}
    main {{ padding: 20px 34px 36px; }}
    .view {{ display: none; }}
    .view.active {{ display: block; animation: rise .28s ease both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .controls, .simulator, .metric, .chart, .table-wrap, .scenario-card {{ background: var(--surface); border: 1px solid rgba(215,224,234,.9); border-radius: 14px; box-shadow: 0 12px 34px rgba(15, 23, 42, .07); }}
    .controls {{ display: grid; grid-template-columns: repeat(6, minmax(130px, 1fr)); gap: 12px; padding: 14px; margin-bottom: 16px; }}
    label {{ display: block; color: var(--muted); font-size: 12px; font-weight: 650; margin-bottom: 5px; }}
    select, input {{ width: 100%; padding: 9px 10px; border: 1px solid var(--line); border-radius: 6px; background: #fff; color: var(--ink); }}
    input[type="range"] {{ padding: 0; accent-color: var(--green); }}
    .simulator {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 18px; padding: 16px; margin-bottom: 16px; background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(248,251,255,.98)); }}
    .sim-title {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }}
    .sim-title h2 {{ margin: 0; font-size: 18px; }}
    .sim-title span {{ color: var(--muted); font-size: 12px; }}
    .sim-controls {{ display: grid; grid-template-columns: repeat(2, minmax(150px, 1fr)); gap: 14px; }}
    .scenario-deck {{ display: grid; grid-template-columns: repeat(4, minmax(130px, 1fr)); gap: 10px; margin: 12px 0 15px; }}
    .scenario-card {{ padding: 12px; cursor: pointer; text-align: left; transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease; }}
    .scenario-card:hover {{ transform: translateY(-2px); border-color: rgba(217,164,65,.75); box-shadow: 0 16px 38px rgba(217,164,65,.15); }}
    .scenario-card strong {{ display: block; font-size: 13px; }}
    .scenario-card span {{ display: block; margin-top: 4px; color: var(--muted); font-size: 11px; line-height: 1.35; }}
    .range-line {{ display: flex; align-items: center; justify-content: space-between; color: var(--muted); font-size: 12px; margin-top: 4px; }}
    .stage-panel {{ display: grid; grid-template-columns: 1fr; gap: 12px; }}
    .money-wall {{ display: flex; flex-wrap: wrap; align-content: flex-start; gap: 6px; min-height: 70px; padding: 10px; background: #f8fbff; border: 1px dashed var(--line); border-radius: 8px; }}
    .coin {{ width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; background: #f7c948; color: #6b4400; font-weight: 800; box-shadow: inset 0 -2px 0 rgba(0,0,0,.12); animation: pop .22s ease both; }}
    @keyframes pop {{ from {{ transform: scale(.72); opacity: .25; }} to {{ transform: scale(1); opacity: 1; }} }}
    .player-row {{ display: flex; flex-wrap: wrap; gap: 6px; padding: 10px; background: #fbfcfe; border: 1px dashed var(--line); border-radius: 8px; }}
    .player-chip {{ height: 28px; min-width: 34px; padding: 0 8px; display: inline-flex; align-items: center; justify-content: center; border-radius: 999px; background: #e8f7f1; color: #08745b; font-weight: 700; font-size: 12px; }}
    .player-chip.core {{ background: #fff4da; color: #8a5a00; }}
    .player-chip.absent {{ background: #f1f5f9; color: #94a3b8; text-decoration: line-through; }}
    .verdict {{ padding: 15px; border-radius: 14px; border: 1px solid var(--line); background: radial-gradient(circle at 100% 0%, rgba(217,164,65,.18), transparent 32%), #fbfcfe; }}
    .verdict-main {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
    .mood {{ font-size: 34px; font-weight: 900; line-height: 1; }}
    .verdict h3 {{ margin: 0; font-size: 21px; }}
    .verdict p {{ margin: 6px 0 0; color: var(--muted); font-size: 13px; line-height: 1.45; }}
    .tier-strip {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; margin-top: 12px; }}
    .tier {{ height: 8px; border-radius: 99px; background: #e5e7eb; }}
    .tier.active.risk {{ background: #dc2626; }}
    .tier.active.low {{ background: #f97316; }}
    .tier.active.mid {{ background: #eab308; }}
    .tier.active.high {{ background: #16a34a; }}
    .tier.active.perfect {{ background: #2563eb; }}
    .lab-cards {{ display: grid; grid-template-columns: repeat(3, minmax(160px, 1fr)); gap: 12px; margin-top: 14px; }}
    .lab-card {{ padding: 13px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfe; }}
    .lab-card span {{ color: var(--muted); font-size: 12px; }}
    .lab-card strong {{ display: block; margin-top: 6px; font-size: 22px; }}
    .action-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }}
    .action-btn {{ border: 0; background: var(--blue); color: #fff; border-radius: 7px; padding: 10px 13px; font-weight: 800; cursor: pointer; }}
    .ghost-btn {{ border: 1px solid var(--line); color: var(--ink); background: #fff; border-radius: 7px; padding: 10px 13px; font-weight: 800; cursor: pointer; }}
    .modal {{ position: fixed; inset: 0; display: none; align-items: center; justify-content: center; padding: 22px; background: rgba(15, 23, 42, .48); z-index: 10; }}
    .modal.open {{ display: flex; }}
    .modal-card {{ width: min(720px, 100%); background: #fff; border-radius: 10px; border: 1px solid var(--line); box-shadow: 0 18px 60px rgba(15, 23, 42, .22); padding: 20px; animation: rise .2s ease both; }}
    .modal-head {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; }}
    .modal-head h2 {{ margin: 0; font-size: 22px; }}
    .close {{ border: 1px solid var(--line); background: #fff; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-weight: 900; }}
    .brief-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; margin-top: 14px; }}
    .brief-box {{ padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfe; }}
    .brief-box span {{ color: var(--muted); font-size: 12px; }}
    .brief-box strong {{ display: block; margin-top: 5px; font-size: 19px; }}
    .insight {{ margin-top: 14px; padding: 12px; border-radius: 8px; background: #eef6ff; color: #1e3a8a; line-height: 1.5; }}
    .metrics {{ display: grid; grid-template-columns: repeat(5, minmax(150px, 1fr)); gap: 12px; margin-bottom: 16px; }}
    .metric {{ padding: 15px; position: relative; overflow: hidden; }}
    .metric::after {{ content: ""; position: absolute; inset: auto -24px -36px auto; width: 82px; height: 82px; border-radius: 50%; background: rgba(15,139,111,.09); }}
    .metric span {{ color: var(--muted); font-size: 12px; }}
    .metric strong {{ display: block; margin-top: 7px; font-size: 25px; }}
    .grid {{ display: grid; grid-template-columns: 1.12fr 1fr; gap: 16px; }}
    .chart {{ padding: 16px; min-height: 332px; background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(249,251,255,.98)); }}
    .chart h2, .table-wrap h2 {{ margin: 0 0 12px; font-size: 17px; }}
    svg {{ width: 100%; height: 270px; display: block; }}
    .axis {{ stroke: #9aa6b2; stroke-width: 1; }}
    .bar {{ fill: var(--green); }}
    .bar2 {{ fill: var(--blue); }}
    .bar3 {{ fill: var(--gold); }}
    .dot {{ fill: var(--rose); opacity: .82; }}
    .tick {{ fill: var(--muted); font-size: 11px; }}
    .empty {{ height: 270px; display: grid; place-items: center; color: var(--muted); }}
    .table-wrap {{ margin-top: 16px; padding: 16px; overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; min-width: 1080px; font-size: 13px; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid var(--line); text-align: left; }}
    th {{ color: var(--muted); background: #fbfcfe; position: sticky; top: 0; }}
    .tag {{ display: inline-block; padding: 3px 8px; border-radius: 999px; background: #edf4ff; color: #2456a6; white-space: nowrap; }}
    .tag.premium {{ background: #fff4da; color: #8a5a00; }}
    .tag.watchlist {{ background: #f3f4f6; color: #475569; }}
    @media (max-width: 980px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .hero {{ grid-template-columns: 1fr; }}
      .stadium-card {{ min-height: 210px; }}
      .scenario-deck {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      nav {{ padding-left: 18px; padding-right: 18px; overflow-x: auto; }}
      .controls, .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .simulator {{ grid-template-columns: 1fr; }}
      .sim-controls {{ grid-template-columns: 1fr; }}
      .lab-cards, .brief-grid {{ grid-template-columns: 1fr; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <div>
        <div class="eyebrow">World Cup Commercial Control Room</div>
        <h1>WorldCupROI Intelligence Platform</h1>
        <div class="deck">Interactive panel analytics for World Cup sponsorship ROI. Filter by team, sponsor, match stage, and commercial segment; test sponsorship moves inside the simulator lab.</div>
        <div class="hero-actions">
          <span class="hero-pill">ROI Forecasting</span>
          <span class="hero-pill">Sponsor Simulation</span>
          <span class="hero-pill">Fan Attention Engine</span>
        </div>
      </div>
      <div class="stadium-card" aria-label="World Cup inspired pitch visual">
        <div class="pitch-line"></div>
        <div class="trophy"></div>
        <div class="ball"></div>
        <div class="score-chip"><span>LIVE ROI SIGNAL</span><strong id="heroSignal">2.68x</strong></div>
      </div>
    </div>
  </header>
  <nav>
    <button class="tab-btn active" data-tab="overview">Overview</button>
    <button class="tab-btn" data-tab="lab">Simulator Lab</button>
    <button class="tab-btn" data-tab="sponsors">Sponsor Map</button>
    <button class="tab-btn" data-tab="panel">Panel Explorer</button>
  </nav>
  <main>
    <section class="controls">
      <div><label for="team">Team</label><select id="team"></select></div>
      <div><label for="sponsor">Sponsor</label><select id="sponsor"></select></div>
      <div><label for="stage">Stage</label><select id="stage"></select></div>
      <div><label for="segment">Segment</label><select id="segment"></select></div>
      <div><label for="metric">Ranking Metric</label><select id="metric">
        <option value="predicted_roi">Predicted ROI</option>
        <option value="commercial_momentum">Commercial Momentum</option>
        <option value="fan_score_panel">FanScore</option>
        <option value="roi_per_million_spend">ROI per $M Spend</option>
      </select></div>
      <div><label for="search">Search</label><input id="search" placeholder="team, sponsor, opponent"></div>
    </section>
    <section class="view active" id="overview">
      <section class="metrics" id="metrics"></section>
      <section class="grid">
        <div class="chart"><h2 id="rankTitle">Top Teams</h2><svg id="teamBars"></svg></div>
        <div class="chart"><h2>ROI by Stage</h2><svg id="stageBars"></svg></div>
      </section>
    </section>
    <section class="view" id="lab">
      <section class="simulator">
        <div>
          <div class="sim-title">
            <h2>Sponsor Strategy Simulator</h2>
            <span>Inputs recalculate ROI, rankings, tags, and output metrics.</span>
          </div>
          <div class="scenario-deck">
            <button class="scenario-card" data-preset="balanced"><strong>Balanced Play</strong><span>Reset to neutral baseline.</span></button>
            <button class="scenario-card" data-preset="allin"><strong>All-in Sponsor</strong><span>High spend and strong activation push.</span></button>
            <button class="scenario-card" data-preset="starout"><strong>Star Out</strong><span>Core player risk and squad pressure.</span></button>
            <button class="scenario-card" data-preset="surge"><strong>Media Surge</strong><span>Better players plus confident spend.</span></button>
          </div>
          <div class="sim-controls">
            <div>
              <label for="spendBoost">Sponsor Investment</label>
              <input id="spendBoost" type="range" min="50" max="200" value="100" step="5">
              <div class="range-line"><span>lean</span><strong id="spendLabel">100%</strong><span>aggressive</span></div>
            </div>
            <div>
              <label for="coreImpact">Core Player Change</label>
              <input id="coreImpact" type="range" min="-40" max="40" value="0" step="5">
              <div class="range-line"><span>down</span><strong id="coreLabel">0%</strong><span>boost</span></div>
            </div>
            <div>
              <label for="availability">Squad Availability</label>
              <input id="availability" type="range" min="60" max="110" value="100" step="5">
              <div class="range-line"><span>thin</span><strong id="availabilityLabel">100%</strong><span>strong</span></div>
            </div>
            <div>
              <label for="absentPlayers">Absent Key Players</label>
              <input id="absentPlayers" type="range" min="0" max="5" value="0" step="1">
              <div class="range-line"><span>full squad</span><strong id="absentLabel">0</strong><span>high risk</span></div>
            </div>
          </div>
          <div class="lab-cards" id="labCards"></div>
          <div class="action-row">
            <button class="action-btn" id="openBrief">Open Strategy Brief</button>
            <button class="ghost-btn" id="resetSim">Reset Simulation</button>
          </div>
        </div>
        <div class="stage-panel">
          <div class="verdict" id="verdict"></div>
          <div class="money-wall" id="moneyWall"></div>
          <div class="player-row" id="playerWall"></div>
        </div>
      </section>
    </section>
    <section class="view" id="sponsors">
      <section class="grid">
        <div class="chart"><h2>Sponsor Efficiency Map</h2><svg id="sponsorDots"></svg></div>
        <div class="chart"><h2>Commercial Segment Mix</h2><svg id="segmentBars"></svg></div>
      </section>
    </section>
    <section class="view" id="panel">
      <section class="table-wrap">
        <h2>Ranked Panel Rows</h2>
        <table id="rows"></table>
      </section>
    </section>
  </main>
  <div class="modal" id="briefModal">
    <div class="modal-card">
      <div class="modal-head"><h2>Strategy Brief</h2><button class="close" id="closeBrief">x</button></div>
      <div id="briefContent"></div>
    </div>
  </div>
  <script>
    const source = {payload_json};
    const panel = source.panel;
    const fmt = (x, d=2) => Number(x || 0).toFixed(d);
    const byId = id => document.getElementById(id);
    const opt = (v, label=v) => `<option value="${{v}}">${{label}}</option>`;
    let latestRows = [];
    let latestTier = null;

    function populateSelect(id, values) {{
      byId(id).innerHTML = opt('All') + values.map(v => opt(v)).join('');
    }}
    populateSelect('team', source.teams);
    populateSelect('sponsor', source.sponsorNames);
    populateSelect('stage', source.stages);
    populateSelect('segment', source.segments);

    function simulationInputs() {{
      return {{
        spend: Number(byId('spendBoost').value) / 100,
        core: Number(byId('coreImpact').value) / 100,
        availability: Number(byId('availability').value) / 100,
        absent: Number(byId('absentPlayers').value)
      }};
    }}

    function filtered() {{
      const team = byId('team').value;
      const sponsor = byId('sponsor').value;
      const stage = byId('stage').value;
      const segment = byId('segment').value;
      const q = byId('search').value.trim().toLowerCase();
      return panel.filter(d =>
        (team === 'All' || d.team === team) &&
        (sponsor === 'All' || d.sponsor === sponsor) &&
        (stage === 'All' || d.stage === stage) &&
        (segment === 'All' || d.commercial_segment === segment) &&
        (!q || [d.team, d.opponent, d.sponsor, d.stage].join(' ').toLowerCase().includes(q))
      );
    }}
    function applySimulation(rows) {{
      const sim = simulationInputs();
      return rows.map(d => {{
        const spendLift = Math.log(sim.spend) * 0.28 + (sim.spend - 1) * 0.10 * Number(d.activation_quality || 0);
        const playerLift = sim.core * 0.72 + (sim.availability - 1) * 0.58 - sim.absent * 0.075;
        const attentionLift = sim.core * 0.16 - sim.absent * 0.018;
        const adjustedRoi = Math.max(0.45, Number(d.predicted_roi) + spendLift + playerLift);
        const adjustedMomentum = Math.max(0.05, Math.min(1.2, Number(d.commercial_momentum) + attentionLift + (sim.spend - 1) * 0.07));
        const adjustedSpend = Math.max(0.1, Number(d.sponsor_spend_m) * sim.spend);
        const adjustedFan = Math.max(0.01, Math.min(1.2, Number(d.fan_score_panel) + attentionLift));
        return {{
          ...d,
          base_roi: Number(d.predicted_roi),
          predicted_roi: adjustedRoi,
          commercial_momentum: adjustedMomentum,
          sponsor_spend_m: adjustedSpend,
          fan_score_panel: adjustedFan,
          roi_per_million_spend: adjustedRoi / adjustedSpend,
          roi_delta: adjustedRoi - Number(d.predicted_roi)
        }};
      }});
    }}
    const avg = (rows, key) => rows.length ? rows.reduce((s, d) => s + Number(d[key] || 0), 0) / rows.length : 0;
    const sum = (rows, key) => rows.reduce((s, d) => s + Number(d[key] || 0), 0);

    function grouped(rows, groupKey, metric, mode='avg') {{
      const map = new Map();
      rows.forEach(d => {{
        const k = d[groupKey];
        if (!map.has(k)) map.set(k, []);
        map.get(k).push(d);
      }});
      return [...map.entries()].map(([name, items]) => ({{
        name,
        value: mode === 'sum' ? sum(items, metric) : avg(items, metric),
        count: items.length
      }})).sort((a, b) => b.value - a.value);
    }}

    function renderMetrics(rows) {{
      byId('heroSignal').textContent = fmt(avg(rows, 'predicted_roi')) + 'x';
      byId('metrics').innerHTML = [
        ['Panel rows', rows.length],
        ['Avg ROI', fmt(avg(rows, 'predicted_roi')) + 'x'],
        ['ROI delta', (avg(rows, 'roi_delta') >= 0 ? '+' : '') + fmt(avg(rows, 'roi_delta')) + 'x'],
        ['Avg momentum', fmt(avg(rows, 'commercial_momentum'))],
        ['ROI / $M', fmt(avg(rows, 'roi_per_million_spend'))]
      ].map(([label, value]) => `<div class="metric"><span>${{label}}</span><strong>${{value}}</strong></div>`).join('');
    }}

    function benefitTier(avgRoi, avgDelta) {{
      if (avgRoi >= 3.25 || avgDelta >= 0.35) return {{ idx: 4, cls: 'perfect', title: 'PERFECT', mood: ':D', note: 'Premium output. ROI and momentum are strong enough for aggressive activation.' }};
      if (avgRoi >= 2.9 || avgDelta >= 0.15) return {{ idx: 3, cls: 'high', title: 'HAPPY', mood: ':)', note: 'High efficiency. The sponsorship mix is producing clear upside.' }};
      if (avgRoi >= 2.55 || avgDelta >= -0.05) return {{ idx: 2, cls: 'mid', title: 'STABLE', mood: ':|', note: 'Balanced result. ROI is acceptable, but upside depends on attention quality.' }};
      if (avgRoi >= 2.25 || avgDelta >= -0.25) return {{ idx: 1, cls: 'low', title: 'CAUTION', mood: ':/', note: 'Weak output. Player or media risk is reducing commercial efficiency.' }};
      return {{ idx: 0, cls: 'risk', title: 'LOW RETURN', mood: ':(', note: 'ROI is under pressure. Spend discipline and recovery strategy are needed.' }};
    }}

    function renderSimulator(rows) {{
      const sim = simulationInputs();
      byId('spendLabel').textContent = `${{Math.round(sim.spend * 100)}}%`;
      byId('coreLabel').textContent = `${{sim.core >= 0 ? '+' : ''}}${{Math.round(sim.core * 100)}}%`;
      byId('availabilityLabel').textContent = `${{Math.round(sim.availability * 100)}}%`;
      byId('absentLabel').textContent = String(sim.absent);

      const tier = benefitTier(avg(rows, 'predicted_roi'), avg(rows, 'roi_delta'));
      latestTier = tier;
      byId('verdict').innerHTML = `
        <div class="verdict-main">
          <div><h3>${{tier.title}}</h3><p>${{tier.note}}</p></div>
          <div class="mood">${{tier.mood}}</div>
        </div>
        <div class="tier-strip">${{['risk','low','mid','high','perfect'].map((c, i) => `<span class="tier ${{i <= tier.idx ? 'active ' + c : ''}}"></span>`).join('')}}</div>
      `;

      const coinCount = Math.max(2, Math.min(18, Math.round(sim.spend * 8)));
      byId('moneyWall').innerHTML = Array.from({{length: coinCount}}, (_, i) => `<span class="coin" title="Sponsor investment unit ${{i + 1}}">$</span>`).join('');

      const activePlayers = Math.max(6, 11 - sim.absent);
      const playerTokens = [];
      for (let i = 0; i < 11; i++) {{
        const absent = i >= activePlayers;
        const core = i < 3;
        const label = core ? `Core ${{i + 1}}` : `P${{i + 1}}`;
        playerTokens.push(`<span class="player-chip ${{core ? 'core' : ''}} ${{absent ? 'absent' : ''}}" title="${{absent ? 'Unavailable' : 'Available'}}">${{label}}</span>`);
      }}
      byId('playerWall').innerHTML = playerTokens.join('');
      byId('labCards').innerHTML = [
        ['Simulated ROI', fmt(avg(rows, 'predicted_roi')) + 'x'],
        ['Avg ROI Delta', (avg(rows, 'roi_delta') >= 0 ? '+' : '') + fmt(avg(rows, 'roi_delta')) + 'x'],
        ['Spend Efficiency', fmt(avg(rows, 'roi_per_million_spend')) + 'x/$M']
      ].map(([label, value]) => `<div class="lab-card"><span>${{label}}</span><strong>${{value}}</strong></div>`).join('');
    }}

    function renderBrief() {{
      const rows = latestRows;
      const top = [...rows].sort((a, b) => Number(b.predicted_roi) - Number(a.predicted_roi))[0] || {{}};
      const risk = Number(byId('absentPlayers').value) >= 3 ? 'Player availability is the main downside risk.' :
        Number(byId('spendBoost').value) >= 150 ? 'Investment is aggressive; monitor ROI per spend.' :
        'Scenario is balanced; attention quality is the key lever.';
      byId('briefContent').innerHTML = `
        <div class="brief-grid">
          <div class="brief-box"><span>Verdict</span><strong>${{latestTier ? latestTier.title : 'STABLE'}}</strong></div>
          <div class="brief-box"><span>Top opportunity</span><strong>${{top.team || 'N/A'}} x ${{top.sponsor || 'N/A'}}</strong></div>
          <div class="brief-box"><span>Simulated ROI</span><strong>${{fmt(avg(rows, 'predicted_roi'))}}x</strong></div>
          <div class="brief-box"><span>Commercial momentum</span><strong>${{fmt(avg(rows, 'commercial_momentum'))}}</strong></div>
        </div>
        <div class="insight">${{risk}} Recommended next move: compare the top-ranked panel rows, then adjust sponsor investment until ROI delta and ROI per spend move in the same direction.</div>
      `;
    }}

    function barChart(id, rows, cls='bar') {{
      const svg = byId(id), w = 760, h = 270, p = 36;
      if (!rows.length) {{
        svg.setAttribute('viewBox', `0 0 ${{w}} ${{h}}`);
        svg.innerHTML = `<text class="tick" x="${{w / 2}}" y="${{h / 2}}" text-anchor="middle">No matching data</text>`;
        return;
      }}
      const max = Math.max(...rows.map(d => +d.value)) || 1;
      svg.setAttribute('viewBox', `0 0 ${{w}} ${{h}}`);
      svg.innerHTML = `<line class="axis" x1="${{p}}" y1="${{h-p}}" x2="${{w-p}}" y2="${{h-p}}"/>`;
      const bw = (w - p * 2) / rows.length * 0.72;
      rows.forEach((d, i) => {{
        const step = (w - p * 2) / rows.length;
        const x = p + i * step + bw * 0.18;
        const bh = (+d.value / max) * (h - p * 2);
        const y = h - p - bh;
        svg.innerHTML += `<rect class="${{cls}}" x="${{x}}" y="${{y}}" width="${{bw}}" height="${{bh}}" rx="3"><title>${{d.name}}: ${{fmt(d.value)}} across ${{d.count}} rows</title></rect>`;
        svg.innerHTML += `<text class="tick" x="${{x + bw/2}}" y="${{h-8}}" text-anchor="middle">${{String(d.name).slice(0, 10)}}</text>`;
        svg.innerHTML += `<text class="tick" x="${{x + bw/2}}" y="${{Math.max(14, y-5)}}" text-anchor="middle">${{fmt(d.value)}}</text>`;
      }});
    }}

    function dotChart(rows) {{
      const svg = byId('sponsorDots'), w = 760, h = 270, p = 40;
      const groupedSponsors = grouped(rows, 'sponsor', 'predicted_roi').map(s => {{
        const items = rows.filter(d => d.sponsor === s.name);
        return {{ name: s.name, x: avg(items, 'commercial_momentum'), y: avg(items, 'roi_per_million_spend'), count: items.length }};
      }});
      svg.setAttribute('viewBox', `0 0 ${{w}} ${{h}}`);
      svg.innerHTML = `<line class="axis" x1="${{p}}" y1="${{h-p}}" x2="${{w-p}}" y2="${{h-p}}"/><line class="axis" x1="${{p}}" y1="${{p}}" x2="${{p}}" y2="${{h-p}}"/>`;
      if (!groupedSponsors.length) return;
      const xs = groupedSponsors.map(d => d.x), ys = groupedSponsors.map(d => d.y);
      const xmin = Math.min(...xs), xmax = Math.max(...xs), ymin = Math.min(...ys), ymax = Math.max(...ys);
      const sx = v => p + ((v - xmin) / ((xmax - xmin) || 1)) * (w - p * 2);
      const sy = v => h - p - ((v - ymin) / ((ymax - ymin) || 1)) * (h - p * 2);
      groupedSponsors.slice(0, 12).forEach(d => {{
        svg.innerHTML += `<circle class="dot" cx="${{sx(d.x)}}" cy="${{sy(d.y)}}" r="${{Math.max(5, Math.min(12, d.count / 12))}}"><title>${{d.name}} | momentum ${{fmt(d.x)}} | ROI/spend ${{fmt(d.y)}} | rows ${{d.count}}</title></circle>`;
        svg.innerHTML += `<text class="tick" x="${{sx(d.x)+9}}" y="${{sy(d.y)+4}}">${{d.name}}</text>`;
      }});
    }}

    function renderTable(rows, metric) {{
      const cols = ['team','opponent','stage','sponsor','result_for_team','attention_segment','commercial_segment','fan_score_panel','sponsor_spend_m','commercial_momentum','predicted_roi','roi_delta','roi_per_million_spend'];
      const top = [...rows].sort((a, b) => Number(b[metric]) - Number(a[metric])).slice(0, 30);
      byId('rows').innerHTML =
        `<thead><tr>${{cols.map(c => `<th>${{c}}</th>`).join('')}}</tr></thead><tbody>` +
        top.map(r => `<tr>${{cols.map(c => {{
          const val = r[c];
          if (c === 'commercial_segment') return `<td><span class="tag ${{String(val).toLowerCase()}}">${{val}}</span></td>`;
          if (c === 'attention_segment') return `<td><span class="tag">${{val}}</span></td>`;
          return `<td>${{typeof val === 'number' ? fmt(val, 3) : val}}</td>`;
        }}).join('')}}</tr>`).join('') +
        `</tbody>`;
    }}

    function render() {{
      const rows = applySimulation(filtered());
      latestRows = rows;
      const metric = byId('metric').value;
      const segmentRows = grouped(rows, 'commercial_segment', 'predicted_roi').map(d => ({{...d, value: d.count}}));
      byId('rankTitle').textContent = `Top Teams by ${{byId('metric').selectedOptions[0].textContent}}`;
      renderSimulator(rows);
      renderMetrics(rows);
      barChart('teamBars', grouped(rows, 'team', metric).slice(0, 12), 'bar');
      barChart('segmentBars', segmentRows, 'bar2');
      barChart('stageBars', grouped(rows, 'stage', 'predicted_roi'), 'bar3');
      dotChart(rows);
      renderTable(rows, metric);
    }}
    ['team','sponsor','stage','segment','metric','search','spendBoost','coreImpact','availability','absentPlayers'].forEach(id => byId(id).addEventListener('input', render));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.addEventListener('click', () => {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
      btn.classList.add('active');
      byId(btn.dataset.tab).classList.add('active');
    }}));
    byId('openBrief').addEventListener('click', () => {{
      renderBrief();
      byId('briefModal').classList.add('open');
    }});
    byId('closeBrief').addEventListener('click', () => byId('briefModal').classList.remove('open'));
    byId('briefModal').addEventListener('click', e => {{
      if (e.target.id === 'briefModal') byId('briefModal').classList.remove('open');
    }});
    byId('resetSim').addEventListener('click', () => {{
      byId('spendBoost').value = 100;
      byId('coreImpact').value = 0;
      byId('availability').value = 100;
      byId('absentPlayers').value = 0;
      render();
    }});
    document.querySelectorAll('.scenario-card').forEach(card => card.addEventListener('click', () => {{
      const preset = card.dataset.preset;
      const presets = {{
        balanced: [100, 0, 100, 0],
        allin: [185, 20, 105, 0],
        starout: [90, -30, 75, 4],
        surge: [145, 35, 110, 0]
      }};
      const [spend, core, availability, absent] = presets[preset];
      byId('spendBoost').value = spend;
      byId('coreImpact').value = core;
      byId('availability').value = availability;
      byId('absentPlayers').value = absent;
      render();
    }}));
    render();
  </script>
</body>
</html>"""


def main() -> None:
    ensure_predictions()
    DASHBOARD_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_DIR / "roi_predictions.csv")
    panel = build_team_panel(df)
    team_year, sponsor_summary = aggregate_panel(panel)

    panel.to_csv(DATA_DIR / "panel_dataset.csv", index=False)
    team_year.to_csv(DATA_DIR / "team_year_panel.csv", index=False)
    sponsor_summary.to_csv(DATA_DIR / "sponsor_panel_summary.csv", index=False)
    (DASHBOARD_DIR / "panel_dashboard.html").write_text(build_html(panel, sponsor_summary), encoding="utf-8")

    summary_md = [
        "# WorldCupROI Panel Data",
        "",
        "Panel grain: `year x match_id x team x sponsor`.",
        "",
        f"- Panel rows: {len(panel)}",
        f"- Teams: {panel['team'].nunique()}",
        f"- Sponsors: {panel['sponsor'].nunique()}",
        f"- Average predicted ROI: {panel['predicted_roi'].mean():.3f}",
        f"- Average commercial momentum: {panel['commercial_momentum'].mean():.3f}",
        "",
        "## Core Variables",
        "",
        "- `fan_score_panel`: player followers, event attention, and media reposts.",
        "- `sponsor_power_index`: sponsor spend, brand fit, activation quality, and sports presence.",
        "- `commercial_momentum`: blended signal combining fan attention, sponsor power, exposure, and match points.",
        "- `roi_per_million_spend`: predicted ROI normalized by sponsor spend.",
    ]
    (REPORT_DIR / "panel_data_summary.md").write_text("\n".join(summary_md), encoding="utf-8")
    print(f"Saved panel dataset to {DATA_DIR / 'panel_dataset.csv'}")
    print(f"Saved HTML dashboard to {DASHBOARD_DIR / 'panel_dashboard.html'}")


if __name__ == "__main__":
    main()
