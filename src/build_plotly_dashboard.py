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


def top_records(df: pd.DataFrame, sort_col: str, n: int = 80) -> list[dict]:
    return df.sort_values(sort_col, ascending=False).head(n).round(4).to_dict(orient="records")


def build_dashboard() -> str:
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    scenarios = pd.read_csv(DATA_DIR / "scenario_recommendations.csv")
    funnel = pd.read_csv(REPORT_DIR / "attention_funnel.csv")
    personas = pd.read_csv(REPORT_DIR / "user_personas.csv") if (REPORT_DIR / "user_personas.csv").exists() else pd.DataFrame()
    sponsor_influence = pd.read_csv(REPORT_DIR / "sponsor_influence_scores.csv") if (REPORT_DIR / "sponsor_influence_scores.csv").exists() else pd.DataFrame()
    uncertainty = pd.read_csv(DATA_DIR / "roi_uncertainty.csv") if (DATA_DIR / "roi_uncertainty.csv").exists() else pd.DataFrame()

    payload = {
        "panel": top_records(panel, "predicted_roi", 500),
        "scenarios": top_records(scenarios, "roi_lift", 500),
        "funnel": funnel.round(4).to_dict(orient="records"),
        "personas": top_records(personas, "avg_conversion_proxy", 60) if not personas.empty else [],
        "sponsorInfluence": top_records(sponsor_influence, "sponsor_influence", 60) if not sponsor_influence.empty else [],
        "uncertainty": top_records(uncertainty, "roi_mean", 120) if not uncertainty.empty else [],
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
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {{ --ink:#102033; --muted:#68768a; --line:#dbe4ee; --green:#0f8b6f; --blue:#2457c5; --orange:#f28c28; --gold:#d9a441; --red:#c2415d; --bg:#f4f7fb; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:linear-gradient(180deg,#07140f 0,#0c1a2a 310px,var(--bg) 310px); }}
    header {{ color:#fff; padding:34px 36px 24px; }}
    .eyebrow {{ color:#ffe7ad; font-size:12px; font-weight:850; text-transform:uppercase; letter-spacing:.08em; }}
    h1 {{ margin:10px 0 10px; font-size:clamp(34px,5vw,62px); line-height:.96; letter-spacing:0; }}
    .deck {{ max-width:900px; color:rgba(255,255,255,.82); line-height:1.55; }}
    nav {{ position:sticky; top:0; z-index:5; display:flex; gap:10px; padding:12px 36px; background:rgba(5,15,25,.93); overflow-x:auto; }}
    button {{ font:inherit; }}
    .navbtn {{ border:1px solid rgba(255,255,255,.14); color:rgba(255,255,255,.82); background:rgba(255,255,255,.08); padding:10px 15px; border-radius:999px; cursor:pointer; font-weight:800; }}
    .navbtn.active {{ color:#172033; background:linear-gradient(135deg,#ffe8a3,#d9a441); border-color:transparent; }}
    main {{ padding:20px 36px 38px; }}
    .controls,.card,.kpi {{ background:#fff; border:1px solid var(--line); border-radius:12px; box-shadow:0 14px 34px rgba(15,23,42,.08); }}
    .controls {{ display:grid; grid-template-columns:repeat(4,minmax(160px,1fr)); gap:12px; padding:14px; margin-bottom:16px; }}
    label {{ display:block; font-size:12px; color:var(--muted); font-weight:800; margin-bottom:6px; }}
    select,input {{ width:100%; border:1px solid var(--line); border-radius:8px; padding:10px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(5,minmax(130px,1fr)); gap:12px; margin-bottom:16px; }}
    .kpi {{ padding:14px; }}
    .kpi span {{ color:var(--muted); font-size:12px; font-weight:800; }}
    .kpi strong {{ display:block; margin-top:6px; font-size:25px; }}
    .view {{ display:none; }}
    .view.active {{ display:block; }}
    .grid {{ display:grid; grid-template-columns:1.08fr .92fr; gap:16px; }}
    .card {{ min-height:360px; padding:14px; margin-bottom:16px; }}
    .card h2 {{ margin:0 0 8px; font-size:18px; }}
    .plot {{ width:100%; height:330px; }}
    table {{ border-collapse:collapse; width:100%; font-size:13px; }}
    th,td {{ border-bottom:1px solid var(--line); padding:9px; text-align:left; }}
    th {{ color:var(--muted); }}
    @media(max-width:900px) {{ .controls,.kpis,.grid {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <div class="eyebrow">Discover -> Explain -> Predict -> Simulate -> Recommend</div>
    <h1>WorldCupROI Decision Dashboard</h1>
    <div class="deck">A reproducible sports sponsorship platform for audience research, sponsor ROI modeling, scenario simulation, graph intelligence, and business recommendations.</div>
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
    <section class="view active" id="discover"><div class="grid"><div class="card"><h2>Audience x ROI Map</h2><div id="discoverMap" class="plot"></div></div><div class="card"><h2>Attention Funnel</h2><div id="funnelPlot" class="plot"></div></div></div></section>
    <section class="view" id="explain"><div class="grid"><div class="card"><h2>Fan Personas</h2><div id="personaPlot" class="plot"></div></div><div class="card"><h2>Sponsor Influence Graph Signal</h2><div id="graphPlot" class="plot"></div></div></div></section>
    <section class="view" id="predict"><div class="grid"><div class="card"><h2>ROI Confidence Interval</h2><div id="intervalPlot" class="plot"></div></div><div class="card"><h2>Top Predicted ROI</h2><div id="topRoiPlot" class="plot"></div></div></div></section>
    <section class="view" id="simulate"><div class="grid"><div class="card"><h2>Scenario ROI Lift</h2><div id="scenarioPlot" class="plot"></div></div><div class="card"><h2>Risk vs ROI</h2><div id="riskPlot" class="plot"></div></div></div></section>
    <section class="view" id="recommend"><div class="card"><h2>Recommended Sponsor Actions</h2><table id="recommendTable"></table></div></section>
  </main>
  <script>
    const source = {data_json};
    const $ = id => document.getElementById(id);
    const avg = (rows,key)=>rows.length?rows.reduce((s,d)=>s+Number(d[key]||0),0)/rows.length:0;
    const fmt = (x,d=2)=>Number(x||0).toFixed(d);
    const layout = title => ({{title,margin:{{l:44,r:20,t:48,b:42}},paper_bgcolor:'rgba(255,255,255,0)',plot_bgcolor:'rgba(255,255,255,0)',font:{{family:'Inter,Segoe UI,Arial',color:'#102033'}},legend:{{orientation:'h',y:1.08,x:1,xanchor:'right'}}}});
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
      Plotly.react('discoverMap',[{{x:rows.map(d=>d.fan_score_panel),y:rows.map(d=>d.predicted_roi),mode:'markers',type:'scatter',text:rows.map(d=>`${{d.team}} x ${{d.sponsor}}`),marker:{{size:rows.map(d=>8+d.event_attention_m/8),color:rows.map(d=>d.commercial_momentum),colorscale:'Viridis',showscale:true,opacity:.82}}}}],layout('Audience Attention vs Predicted ROI'),{{responsive:true}});
      Plotly.react('funnelPlot',[{{x:source.funnel.map(d=>d.stage),y:source.funnel.map(d=>d.avg_score),type:'bar',marker:{{color:['#2457c5','#0f8b6f','#f28c28','#d9a441']}}}}],layout('Media Exposure -> Conversion Funnel'),{{responsive:true}});
      Plotly.react('personaPlot',[{{x:source.personas.slice(0,12).map(d=>d.team),y:source.personas.slice(0,12).map(d=>d.avg_conversion_proxy),type:'bar',text:source.personas.slice(0,12).map(d=>d.persona),marker:{{color:'#0f8b6f'}}}}],layout('Top User Personas by Conversion Proxy'),{{responsive:true}});
      Plotly.react('graphPlot',[{{x:source.sponsorInfluence.slice(0,12).map(d=>d.source),y:source.sponsorInfluence.slice(0,12).map(d=>d.sponsor_influence),type:'bar',marker:{{color:'#2457c5'}}}}],layout('Sponsor Influence from Graph Centrality'),{{responsive:true}});
      const u=source.uncertainty.slice(0,80);
      Plotly.react('intervalPlot',[{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_ci_high),mode:'lines',line:{{width:0}},showlegend:false}},{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_ci_low),mode:'lines',fill:'tonexty',fillcolor:'rgba(36,87,197,.18)',line:{{width:0}},name:'interval'}},{{x:u.map(d=>d.match_id),y:u.map(d=>d.roi_mean),mode:'lines+markers',name:'mean',line:{{color:'#2457c5'}}}}],layout('ROI Confidence Interval'),{{responsive:true}});
      const top=[...rows].sort((a,b)=>b.predicted_roi-a.predicted_roi).slice(0,15);
      Plotly.react('topRoiPlot',[{{x:top.map(d=>d.team),y:top.map(d=>d.predicted_roi),type:'bar',marker:{{color:'#f28c28'}}}}],layout('Top Predicted ROI'),{{responsive:true}});
      Plotly.react('scenarioPlot',[{{x:scenarios.map(d=>d.scenario),y:scenarios.map(d=>d.roi_lift),type:'box',boxpoints:false,marker:{{color:'#0f8b6f'}}}}],layout('Scenario ROI Lift Distribution'),{{responsive:true}});
      Plotly.react('riskPlot',[{{x:scenarios.map(d=>d.risk_score),y:scenarios.map(d=>d.scenario_roi),mode:'markers',type:'scatter',text:scenarios.map(d=>d.strategy_recommendation),marker:{{size:10,color:scenarios.map(d=>d.roi_lift),colorscale:'RdYlGn',showscale:true}}}}],layout('Risk vs Scenario ROI'),{{responsive:true}});
      const rec=[...scenarios].sort((a,b)=>b.roi_lift-a.roi_lift).slice(0,18);
      const cols=['strategy_type','scenario','team_a','team_b','scenario_roi','roi_lift','risk_level','roi_ci_low','roi_ci_high','strategy_recommendation'];
      $('recommendTable').innerHTML=`<thead><tr>${{cols.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>${{rec.map(r=>`<tr>${{cols.map(c=>`<td>${{typeof r[c]==='number'?fmt(r[c],3):r[c]}}</td>`).join('')}}</tr>`).join('')}}</tbody>`;
    }}
    ['team','sponsor','strategy','search'].forEach(id=>$(id).addEventListener('input',render));
    document.querySelectorAll('.navbtn').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.navbtn').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');$(b.dataset.tab).classList.add('active');setTimeout(render,40);}}));
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
