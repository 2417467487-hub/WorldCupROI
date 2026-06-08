from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DASHBOARD_DIR = ROOT / "dashboard"
REPORT_DIR = ROOT / "reports"


def ensure_data() -> None:
    if not (DATA_DIR / "panel_dataset.csv").exists():
        from build_panel_data import main as build_panel

        build_panel()
    if not (DATA_DIR / "scenario_recommendations.csv").exists():
        from scenario_engine import main as run_scenarios

        run_scenarios()
    if not (REPORT_DIR / "attention_funnel.csv").exists():
        from user_behavior_analysis import main as run_user

        run_user()
    if not (REPORT_DIR / "deep_analysis_landing_report.md").exists():
        from deep_analysis_extensions import main as run_deep_analysis

        run_deep_analysis()


def top_records(df: pd.DataFrame, sort_col: str, n: int = 120) -> list[dict]:
    return df.sort_values(sort_col, ascending=False).head(n).round(4).to_dict(orient="records")


def build_dashboard() -> str:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv")
    funnel = pd.read_csv(REPORT_DIR / "attention_funnel.csv")
    personas = pd.read_csv(REPORT_DIR / "user_personas.csv") if (REPORT_DIR / "user_personas.csv").exists() else pd.DataFrame()
    sponsor_influence = pd.read_csv(REPORT_DIR / "sponsor_influence_scores.csv") if (REPORT_DIR / "sponsor_influence_scores.csv").exists() else pd.DataFrame()
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv") if (DATA_DIR / "roi_uncertainty.csv").exists() else pd.DataFrame()
    future_roi = pd.read_csv(REPORT_DIR / "future_roi_forecast.csv") if (REPORT_DIR / "future_roi_forecast.csv").exists() else pd.DataFrame()
    sentiment_events = pd.read_csv(REPORT_DIR / "sentiment_event_roi_impact.csv") if (REPORT_DIR / "sentiment_event_roi_impact.csv").exists() else pd.DataFrame()
    resource_mix = pd.read_csv(REPORT_DIR / "resource_optimization_top_budget_mix.csv") if (REPORT_DIR / "resource_optimization_top_budget_mix.csv").exists() else pd.DataFrame()
    graph_attention = pd.read_csv(REPORT_DIR / "graph_attention_roi_contributions.csv") if (REPORT_DIR / "graph_attention_roi_contributions.csv").exists() else pd.DataFrame()
    extreme = pd.read_csv(REPORT_DIR / "extreme_scenario_roi_risk.csv") if (REPORT_DIR / "extreme_scenario_roi_risk.csv").exists() else pd.DataFrame()
    commercial = pd.read_csv(DATA_DIR / "commercial_decision_metrics.csv") if (DATA_DIR / "commercial_decision_metrics.csv").exists() else pd.DataFrame()

    payload = {
        "panel": top_records(panel, "predicted_roi", 700),
        "scenarios": top_records(scenarios, "roi_lift", 700),
        "funnel": funnel.round(4).to_dict(orient="records"),
        "personas": top_records(personas, "avg_conversion_proxy", 80) if not personas.empty else [],
        "sponsorInfluence": top_records(sponsor_influence, "sponsor_influence", 80) if not sponsor_influence.empty else [],
        "uncertainty": top_records(uncertainty, "roi_mean", 160) if not uncertainty.empty else [],
        "futureRoi": future_roi.round(4).to_dict(orient="records"),
        "sentimentEvents": sentiment_events.round(4).to_dict(orient="records"),
        "resourceMix": top_records(resource_mix, "risk_adjusted_roi", 80) if not resource_mix.empty else [],
        "graphAttention": top_records(graph_attention, "attention_roi_contribution", 80) if not graph_attention.empty else [],
        "extreme": top_records(extreme, "scenario_roi", 160) if not extreme.empty else [],
        "commercial": top_records(commercial, "commercial_decision_score", 160) if not commercial.empty else [],
        "teams": sorted(panel["team"].dropna().unique().tolist()),
        "sponsors": sorted(panel["sponsor"].dropna().unique().tolist()),
    }
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WorldCupROI Decision Dashboard</title>
  <script src="../assets/vendor/plotly.min.js"></script>
  <style>
    :root {{
      --pitch:#07543f;
      --pitch-dark:#052c22;
      --pitch-soft:#0b6b50;
      --gold:#f2c75c;
      --gold-2:#d9a441;
      --red:#c8102e;
      --blue:#0072b2;
      --green:#009e73;
      --orange:#e69f00;
      --ink:#102033;
      --muted:#667085;
      --line:#d9e2ec;
      --paper:#ffffff;
      --bg:#f4f7fb;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      color:var(--ink);
      background:
        radial-gradient(circle at 15% 0%, rgba(242,199,92,.30), transparent 28rem),
        radial-gradient(circle at 84% 8%, rgba(200,16,46,.22), transparent 24rem),
        linear-gradient(180deg, var(--pitch-dark) 0, #071d18 260px, var(--bg) 260px);
    }}
    body::before {{
      content:"";
      position:fixed;
      inset:0;
      pointer-events:none;
      opacity:.12;
      background:
        linear-gradient(90deg, transparent 49.7%, #fff 49.8%, #fff 50.2%, transparent 50.3%),
        radial-gradient(circle at 50% 150px, transparent 0 72px, #fff 73px 75px, transparent 76px),
        linear-gradient(0deg, transparent 49.7%, #fff 49.8%, #fff 50.2%, transparent 50.3%);
      background-size:100% 320px, 100% 320px, 100% 320px;
      background-position:center top;
    }}
    header {{
      position:relative;
      color:#fff;
      padding:24px 42px 20px;
      overflow:hidden;
    }}
    header::after {{
      content:"";
      position:absolute;
      right:40px;
      top:34px;
      width:168px;
      height:168px;
      border:2px solid rgba(242,199,92,.38);
      border-radius:50%;
      box-shadow:0 0 0 42px rgba(255,255,255,.035), inset 0 0 0 42px rgba(255,255,255,.025);
    }}
    .eyebrow {{
      color:var(--gold);
      font-size:12px;
      font-weight:900;
      text-transform:uppercase;
      letter-spacing:.12em;
    }}
    h1 {{
      max-width:960px;
      margin:8px 0 8px;
      font-size:clamp(34px,4.8vw,58px);
      line-height:.96;
      letter-spacing:0;
    }}
    .deck {{
      max-width:980px;
      color:rgba(255,255,255,.82);
      line-height:1.55;
      font-size:16px;
    }}
    .hero-strip {{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:12px;
    }}
    .badge {{
      border:1px solid rgba(242,199,92,.34);
      color:#fff;
      background:rgba(255,255,255,.08);
      border-radius:999px;
      padding:6px 10px;
      font-size:12px;
      font-weight:800;
      backdrop-filter:blur(8px);
    }}
    nav {{
      position:sticky;
      top:0;
      z-index:5;
      display:flex;
      gap:10px;
      padding:10px 42px;
      background:rgba(5,23,19,.94);
      border-top:1px solid rgba(255,255,255,.10);
      border-bottom:1px solid rgba(255,255,255,.12);
      overflow-x:auto;
    }}
    button {{ font:inherit; }}
    .navbtn {{
      border:1px solid rgba(255,255,255,.16);
      color:rgba(255,255,255,.84);
      background:rgba(255,255,255,.08);
      padding:9px 15px;
      border-radius:999px;
      cursor:pointer;
      font-weight:900;
    }}
    .navbtn.active {{
      color:#182033;
      background:linear-gradient(135deg,#ffe8a3,var(--gold-2));
      border-color:transparent;
      box-shadow:0 8px 22px rgba(242,199,92,.22);
    }}
    main {{ padding:16px 42px 42px; }}
    .controls,.card,.kpi {{
      background:rgba(255,255,255,.98);
      border:1px solid var(--line);
      border-radius:10px;
      box-shadow:0 14px 34px rgba(15,23,42,.08);
    }}
    .controls {{
      display:grid;
      grid-template-columns:repeat(4,minmax(170px,1fr));
      gap:12px;
      padding:12px;
      margin-bottom:12px;
    }}
    label {{
      display:block;
      font-size:12px;
      color:var(--muted);
      font-weight:900;
      margin-bottom:6px;
    }}
    select,input {{
      width:100%;
      border:1px solid var(--line);
      border-radius:8px;
      padding:9px;
      background:#fbfdff;
      color:var(--ink);
    }}
    .kpis {{
      display:grid;
      grid-template-columns:repeat(5,minmax(130px,1fr));
      gap:12px;
      margin-bottom:12px;
    }}
    .kpi {{ padding:12px 14px; }}
    .kpi span {{
      color:var(--muted);
      font-size:12px;
      font-weight:900;
    }}
    .kpi strong {{
      display:block;
      margin-top:6px;
      font-size:25px;
      letter-spacing:-.01em;
    }}
    .view {{ display:none; }}
    .view.active {{ display:block; }}
    .grid {{
      display:grid;
      grid-template-columns:1.08fr .92fr;
      gap:16px;
    }}
    .card {{
      min-height:405px;
      padding:16px;
      margin-bottom:16px;
    }}
    .card h2 {{
      margin:0 0 3px;
      font-size:20px;
      letter-spacing:0;
    }}
    .note {{
      margin:0 0 12px;
      color:var(--muted);
      font-size:13px;
      line-height:1.45;
    }}
    .plot {{ width:100%; height:350px; }}
    table {{
      border-collapse:collapse;
      width:100%;
      font-size:13px;
      background:#fff;
    }}
    th,td {{
      border-bottom:1px solid var(--line);
      padding:10px 9px;
      text-align:left;
      vertical-align:top;
    }}
    th {{
      color:var(--muted);
      text-transform:uppercase;
      font-size:11px;
      letter-spacing:.04em;
    }}
    .takeaway {{
      margin-top:10px;
      padding:12px 14px;
      border-left:4px solid var(--gold-2);
      background:#fff7dc;
      color:#3b2b09;
      border-radius:8px;
      font-size:13px;
    }}
    @media(max-width:980px) {{
      header,main,nav {{ padding-left:20px; padding-right:20px; }}
      .controls,.kpis,.grid {{ grid-template-columns:1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="eyebrow">FIFA-style sponsorship intelligence · Discover -> Explain -> Predict -> Simulate -> Recommend</div>
    <h1>WorldCupROI Decision Dashboard</h1>
    <div class="deck">A World Cup inspired sponsorship intelligence platform for audience research, sponsor ROI modeling, scenario simulation, graph influence, and risk-aware recommendations.</div>
    <div class="hero-strip">
      <div class="badge">Real match history</div>
      <div class="badge">Sponsor ROI model</div>
      <div class="badge">SHAP-style drivers</div>
      <div class="badge">Conformal intervals</div>
      <div class="badge">NetworkX influence</div>
    </div>
  </header>
  <nav>
    <button class="navbtn active" data-tab="discover">Discover</button>
    <button class="navbtn" data-tab="explain">Explain</button>
    <button class="navbtn" data-tab="predict">Predict</button>
    <button class="navbtn" data-tab="simulate">Simulate</button>
    <button class="navbtn" data-tab="recommend">Recommend</button>
  </nav>
  <main>
    <section class="controls">
      <div><label>Team</label><select id="team"></select></div>
      <div><label>Sponsor</label><select id="sponsor"></select></div>
      <div><label>Strategy</label><select id="strategy"><option>All</option><option>conservative</option><option>balanced</option><option>aggressive</option></select></div>
      <div><label>Search</label><input id="search" placeholder="team, sponsor, stage"></div>
    </section>
    <section class="kpis" id="kpis"></section>
    <section class="view active" id="discover">
      <div class="grid">
        <div class="card"><h2>Audience x ROI Map</h2><p class="note">Fan attention, commercial momentum, and sponsor ROI in one scatter view.</p><div id="discoverMap" class="plot"></div></div>
        <div class="card"><h2>Attention Funnel</h2><p class="note">Media exposure -> user attention -> social interaction -> sponsor conversion.</p><div id="funnelPlot" class="plot"></div></div>
      </div>
    </section>
    <section class="view" id="explain">
      <div class="grid">
        <div class="card"><h2>User Personas</h2><p class="note">Top fan segments by conversion proxy and attention quality.</p><div id="personaPlot" class="plot"></div></div>
        <div class="card"><h2>Sponsor Influence Graph Signal</h2><p class="note">NetworkX centrality and sponsor influence for sponsor-team-player relationships.</p><div id="graphPlot" class="plot"></div></div>
      </div>
    </section>
    <section class="view" id="predict">
      <div class="grid">
        <div class="card"><h2>ROI Confidence Interval</h2><p class="note">Conformal-style interval bands around sponsor ROI estimates.</p><div id="intervalPlot" class="plot"></div></div>
        <div class="card"><h2>Top Predicted ROI</h2><p class="note">Highest ROI opportunities after current filters.</p><div id="topRoiPlot" class="plot"></div></div>
        <div class="card"><h2>Future Event ROI Trend</h2><p class="note">Planning forecast across upcoming World Cup cycles.</p><div id="futurePlot" class="plot"></div></div>
        <div class="card"><h2>Sentiment Event Impact</h2><p class="note">Attention and sentiment shocks mapped to sponsor ROI movement.</p><div id="sentimentPlot" class="plot"></div></div>
      </div>
    </section>
    <section class="view" id="simulate">
      <div class="grid">
        <div class="card"><h2>Scenario ROI Lift</h2><p class="note">Distribution of ROI lift across sponsor strategy scenarios.</p><div id="scenarioPlot" class="plot"></div></div>
        <div class="card"><h2>Risk vs ROI</h2><p class="note">Trade-off between scenario risk score and expected sponsor ROI.</p><div id="riskPlot" class="plot"></div></div>
        <div class="card"><h2>Budget x Media Optimization</h2><p class="note">Risk-adjusted ROI under sponsor budget and media multiplier choices.</p><div id="budgetPlot" class="plot"></div></div>
        <div class="card"><h2>Extreme Scenario Stress Test</h2><p class="note">Key player injury, sentiment crisis, policy change, and viral upside intervals.</p><div id="extremePlot" class="plot"></div></div>
      </div>
    </section>
    <section class="view" id="recommend">
      <div class="card"><h2>Recommended Sponsor Actions</h2><p class="note">Ranked strategy actions with confidence intervals and risk labels.</p><table id="recommendTable"></table><div class="takeaway">Business takeaway: prioritize high-lift strategies only when interval width and risk score stay within a reviewable range.</div></div>
      <div class="grid">
        <div class="card"><h2>Integrated Commercial Decision Score</h2><p class="note">ROI, media value, fan conversion, social spread, and brand influence combined.</p><div id="commercialPlot" class="plot"></div></div>
        <div class="card"><h2>Graph Attention ROI Contribution</h2><p class="note">Interpretable graph contribution from sponsor-team-player relationships.</p><div id="attentionPlot" class="plot"></div></div>
      </div>
      <div class="card"><h2>Resource Allocation Recommendations</h2><p class="note">Top budget and media activation combinations ranked by risk-adjusted ROI.</p><table id="resourceTable"></table><div class="takeaway">Business takeaway: scale spend only where media sensitivity, commercial score, and downside risk agree.</div></div>
    </section>
  </main>
  <script>
    const source = {data_json};
    const $ = id => document.getElementById(id);
    const avg = (rows,key)=>rows.length?rows.reduce((s,d)=>s+Number(d[key]||0),0)/rows.length:0;
    const fmt = (x,d=2)=>Number(x||0).toFixed(d);
    const config = {{responsive:true, displaylogo:false, modeBarButtonsToRemove:['lasso2d','select2d']}};
    const funnelLabel = (stage) => ({{
      '媒体曝光':'Media Exposure',
      '用户关注':'User Attention',
      '社交互动':'Social Interaction',
      '赞助转化':'Sponsor Conversion',
      'media_exposure':'Media Exposure',
      'user_attention':'User Attention',
      'social_interaction':'Social Interaction',
      'sponsor_conversion':'Sponsor Conversion'
    }}[stage] || stage);
    const academicLayout = (title, xTitle='', yTitle='') => ({{
      title:{{text:title,x:0.02,xanchor:'left',font:{{size:17,color:'#102033'}}}},
      margin:{{l:58,r:24,t:58,b:58}},
      paper_bgcolor:'#ffffff',
      plot_bgcolor:'#ffffff',
      font:{{family:'Inter, Segoe UI, Arial',color:'#102033',size:12}},
      xaxis:{{title:xTitle,showgrid:true,gridcolor:'#e6edf5',zeroline:false,linecolor:'#b8c4d2',ticks:'outside'}},
      yaxis:{{title:yTitle,showgrid:true,gridcolor:'#e6edf5',zeroline:false,linecolor:'#b8c4d2',ticks:'outside'}},
      legend:{{orientation:'h',y:1.12,x:1,xanchor:'right',bgcolor:'rgba(255,255,255,.84)',bordercolor:'#d9e2ec',borderwidth:1}},
      colorway:['#009E73','#0072B2','#E69F00','#D55E00','#7B61FF','#56B4E9']
    }});
    function opts(id, values) {{ $(id).innerHTML='<option>All</option>'+values.map(v=>`<option>${{v}}</option>`).join(''); }}
    opts('team', source.teams); opts('sponsor', source.sponsors);
    function panelRows() {{
      const team=$('team').value, sponsor=$('sponsor').value, q=$('search').value.toLowerCase().trim();
      return source.panel.filter(d=>(team==='All'||d.team===team)&&(sponsor==='All'||d.sponsor===sponsor)&&(!q||[d.team,d.opponent,d.sponsor,d.stage].join(' ').toLowerCase().includes(q)));
    }}
    function scenarioRows() {{
      const strategy=$('strategy').value, q=$('search').value.toLowerCase().trim();
      return source.scenarios.filter(d=>(strategy==='All'||d.strategy_type===strategy)&&(!q||[d.team_a,d.team_b,d.stage,d.scenario,d.strategy_type].join(' ').toLowerCase().includes(q)));
    }}
    function kpis(rows, scenarios) {{
      $('kpis').innerHTML=[
        ['Rows',rows.length],
        ['Avg ROI',fmt(avg(rows,'predicted_roi'))+'x'],
        ['FanScore',fmt(avg(rows,'fan_score_panel'))],
        ['Scenario lift',fmt(avg(scenarios,'roi_lift'))+'x'],
        ['Risk score',fmt(avg(scenarios,'risk_score'))]
      ].map(([a,b])=>`<div class="kpi"><span>${{a}}</span><strong>${{b}}</strong></div>`).join('');
    }}
    function render() {{
      const rows=panelRows(), scenarios=scenarioRows();
      kpis(rows, scenarios);
      Plotly.react('discoverMap',[{{x:rows.map(d=>d.fan_score_panel),y:rows.map(d=>d.predicted_roi),mode:'markers',type:'scatter',name:'Team x Sponsor',text:rows.map(d=>`${{d.team}} x ${{d.sponsor}}`),marker:{{size:rows.map(d=>8+d.event_attention_m/8),color:rows.map(d=>d.commercial_momentum),colorscale:[[0,'#0072B2'],[.5,'#009E73'],[1,'#E69F00']],showscale:true,colorbar:{{title:'Momentum'}},opacity:.82,line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Audience Attention vs Predicted ROI','FanScore panel','Predicted sponsor ROI'),config);
      Plotly.react('funnelPlot',[{{x:source.funnel.map(d=>funnelLabel(d.stage)),y:source.funnel.map(d=>d.avg_score),type:'bar',name:'Funnel score',marker:{{color:['#0072B2','#009E73','#E69F00','#D55E00'],line:{{color:'#ffffff',width:1.2}}}}}}],academicLayout('Media Exposure -> Conversion Funnel','Funnel stage','Average score'),config);
      Plotly.react('personaPlot',[{{x:source.personas.slice(0,12).map(d=>d.team),y:source.personas.slice(0,12).map(d=>d.avg_conversion_proxy),type:'bar',name:'Conversion proxy',text:source.personas.slice(0,12).map(d=>d.persona),marker:{{color:'#009E73',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Top User Personas by Conversion Proxy','Team','Conversion proxy'),config);
      Plotly.react('graphPlot',[{{x:source.sponsorInfluence.slice(0,12).map(d=>d.source),y:source.sponsorInfluence.slice(0,12).map(d=>d.sponsor_influence),type:'bar',name:'Sponsor influence',marker:{{color:'#0072B2',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Sponsor Influence from Graph Centrality','Sponsor node','Influence score'),config);
      const u=source.uncertainty.slice(0,80);
      Plotly.react('intervalPlot',[{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_ci_high),mode:'lines',line:{{width:0}},showlegend:false,hoverinfo:'skip'}},{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_ci_low),mode:'lines',fill:'tonexty',fillcolor:'rgba(0,114,178,.18)',line:{{width:0}},name:'ROI interval'}},{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_mean),mode:'lines+markers',name:'ROI mean',line:{{color:'#0072B2',width:2.4}},marker:{{color:'#E69F00',size:6}}}}],academicLayout('ROI Prediction Interval / Conformal Signal','Match ID','Sponsor ROI'),config);
      const top=[...rows].sort((a,b)=>b.predicted_roi-a.predicted_roi).slice(0,15);
      Plotly.react('topRoiPlot',[{{x:top.map(d=>d.predicted_roi),y:top.map(d=>d.team),type:'bar',orientation:'h',name:'Predicted ROI',marker:{{color:'#E69F00',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Top Predicted ROI','Predicted sponsor ROI','Team'),config);
      Plotly.react('futurePlot',[{{x:source.futureRoi.map(d=>d.cycle),y:source.futureRoi.map(d=>d.forecast_roi),mode:'lines+markers',name:'Forecast ROI',line:{{color:'#009E73',width:3}},marker:{{size:10,color:'#E69F00',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Future World Cup Cycle ROI Forecast','Cycle','Forecast sponsor ROI'),config);
      Plotly.react('sentimentPlot',[{{x:source.sentimentEvents.map(d=>d.event_type),y:source.sentimentEvents.map(d=>d.avg_roi_delta),type:'bar',name:'Avg ROI delta',marker:{{color:source.sentimentEvents.map(d=>d.avg_roi_delta),colorscale:[[0,'#D55E00'],[.5,'#F2C75C'],[1,'#009E73']],line:{{color:'#ffffff',width:1}}}},text:source.sentimentEvents.map(d=>`n=${{d.samples}}`)}}],academicLayout('Key Event Sentiment Impact on ROI','Event type','Average ROI delta'),config);
      Plotly.react('scenarioPlot',[{{x:scenarios.map(d=>d.scenario),y:scenarios.map(d=>d.roi_lift),type:'box',name:'ROI lift',boxpoints:false,marker:{{color:'#009E73'}}}}],academicLayout('Scenario ROI Lift Distribution','Scenario','ROI lift'),config);
      Plotly.react('riskPlot',[{{x:scenarios.map(d=>d.risk_score),y:scenarios.map(d=>d.scenario_roi),mode:'markers',type:'scatter',name:'Scenario',text:scenarios.map(d=>d.strategy_recommendation),marker:{{size:11,color:scenarios.map(d=>d.roi_lift),colorscale:[[0,'#D55E00'],[.5,'#F2C75C'],[1,'#009E73']],showscale:true,colorbar:{{title:'ROI lift'}},line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Risk vs Scenario ROI','Risk score','Scenario ROI'),config);
      Plotly.react('budgetPlot',[{{x:source.resourceMix.map(d=>d.budget_m),y:source.resourceMix.map(d=>d.risk_adjusted_roi),mode:'markers',type:'scatter',name:'Budget mix',text:source.resourceMix.map(d=>`${{d.sponsor}} · media x${{d.media_multiplier}}`),marker:{{size:source.resourceMix.map(d=>8+Number(d.media_multiplier||1)*5),color:source.resourceMix.map(d=>d.media_multiplier),colorscale:[[0,'#0072B2'],[.5,'#009E73'],[1,'#E69F00']],showscale:true,colorbar:{{title:'Media x'}},line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Budget and Media Sensitivity','Budget, USD millions','Risk-adjusted ROI'),config);
      const ex=source.extreme.slice(0,80);
      Plotly.react('extremePlot',[{{x:ex.map(d=>d.extreme_scenario),y:ex.map(d=>d.roi_ci_high),mode:'markers',marker:{{color:'rgba(0,0,0,0)'}},showlegend:false,hoverinfo:'skip'}},{{x:ex.map(d=>d.extreme_scenario),y:ex.map(d=>d.roi_ci_low),type:'box',name:'Risk interval',boxpoints:false,marker:{{color:'#0072B2'}}}},{{x:ex.map(d=>d.extreme_scenario),y:ex.map(d=>d.scenario_roi),type:'box',name:'Scenario ROI',boxpoints:false,marker:{{color:'#E69F00'}}}}],academicLayout('Extreme Scenario ROI and Risk Intervals','Extreme scenario','ROI'),config);
      const rec=[...scenarios].sort((a,b)=>b.roi_lift-a.roi_lift).slice(0,18);
      const cols=['strategy_type','scenario','team_a','team_b','scenario_roi','roi_lift','risk_level','roi_ci_low','roi_ci_high','strategy_recommendation'];
      $('recommendTable').innerHTML=`<thead><tr>${{cols.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>${{rec.map(r=>`<tr>${{cols.map(c=>`<td>${{typeof r[c]==='number'?fmt(r[c],3):r[c]}}</td>`).join('')}}</tr>`).join('')}}</tbody>`;
      const commercial=source.commercial.slice(0,15);
      Plotly.react('commercialPlot',[{{x:commercial.map(d=>d.commercial_decision_score),y:commercial.map(d=>`${{d.team}} x ${{d.sponsor}}`),type:'bar',orientation:'h',name:'Decision score',marker:{{color:'#009E73',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Integrated Commercial Decision Score','Composite score','Team x Sponsor'),config);
      Plotly.react('attentionPlot',[{{x:source.graphAttention.slice(0,14).map(d=>d.attention_roi_contribution),y:source.graphAttention.slice(0,14).map(d=>d.node.replace('sponsor:','')),type:'bar',orientation:'h',name:'Attention contribution',marker:{{color:'#0072B2',line:{{color:'#ffffff',width:1}}}}}}],academicLayout('Graph Attention ROI Contribution','Contribution score','Sponsor node'),config);
      const mix=source.resourceMix.slice(0,12);
      const mixCols=['sponsor','budget_m','media_multiplier','expected_roi','risk_adjusted_roi','risk_penalty','recommendation'];
      $('resourceTable').innerHTML=`<thead><tr>${{mixCols.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>${{mix.map(r=>`<tr>${{mixCols.map(c=>`<td>${{typeof r[c]==='number'?fmt(r[c],3):r[c]}}</td>`).join('')}}</tr>`).join('')}}</tbody>`;
    }}
    ['team','sponsor','strategy','search'].forEach(id=>$(id).addEventListener('input',render));
    document.querySelectorAll('.navbtn').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.navbtn').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');$(b.dataset.tab).classList.add('active');setTimeout(render,60);}}));
    render();
  </script>
</body>
</html>"""


def main() -> None:
    ensure_data()
    DASHBOARD_DIR.mkdir(exist_ok=True)
    out = DASHBOARD_DIR / "panel_dashboard.html"
    out.write_text(build_dashboard(), encoding="utf-8")
    print(f"Saved five-page Plotly dashboard to {out}")


if __name__ == "__main__":
    main()
