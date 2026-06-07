from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DASHBOARD_DIR = ROOT / "dashboard"


def ensure_data() -> None:
    if not (DATA_DIR / "panel_dataset.csv").exists():
        from build_panel_data import main as build_panel

        build_panel()


def build_dashboard(panel: pd.DataFrame, matches: pd.DataFrame) -> str:
    panel_payload = panel.round(4).to_dict(orient="records")
    match_payload = matches.round(4).to_dict(orient="records")
    payload = {
        "panel": panel_payload,
        "matches": match_payload,
        "teams": sorted(panel["team"].dropna().unique().tolist()),
        "sponsors": sorted(panel["sponsor"].dropna().unique().tolist()),
        "stages": sorted(panel["stage"].dropna().unique().tolist()),
        "weather": sorted(panel["weather"].dropna().unique().tolist()),
    }
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WorldCupROI Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {{
      --ink:#102033; --muted:#68768a; --line:#dbe4ee; --green:#0f8b6f;
      --blue:#2457c5; --orange:#f28c28; --gold:#d9a441; --red:#c2415d;
      --bg:#f4f7fb; --card:#ffffff;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink);
      background:
        radial-gradient(circle at 18% 0%, rgba(217,164,65,.26), transparent 26%),
        radial-gradient(circle at 88% 5%, rgba(15,139,111,.25), transparent 28%),
        linear-gradient(180deg,#07140f 0,#0c1a2a 360px,var(--bg) 360px,var(--bg) 100%);
    }}
    header {{ padding:34px 36px 28px; color:#fff; }}
    .hero {{ display:grid; grid-template-columns:minmax(320px,1.2fr) minmax(300px,.8fr); gap:28px; align-items:stretch; }}
    .eyebrow {{ color:#ffe7ad; text-transform:uppercase; font-size:12px; font-weight:850; letter-spacing:.08em; }}
    h1 {{ margin:10px 0 12px; font-size:clamp(36px,5vw,70px); line-height:.95; letter-spacing:0; }}
    .deck {{ max-width:860px; color:rgba(255,255,255,.82); line-height:1.6; }}
    .pitch {{
      min-height:250px; position:relative; border-radius:22px; overflow:hidden;
      border:1px solid rgba(255,255,255,.20);
      background:
        linear-gradient(90deg,rgba(255,255,255,.10) 1px,transparent 1px) 0 0/40px 40px,
        linear-gradient(0deg,rgba(255,255,255,.08) 1px,transparent 1px) 0 0/40px 40px,
        linear-gradient(135deg,#0e7a4f,#0a5f3d);
      box-shadow:0 26px 90px rgba(0,0,0,.28);
    }}
    .pitch::before {{ content:""; position:absolute; inset:28px; border:2px solid rgba(255,255,255,.50); border-radius:14px; }}
    .pitch::after {{ content:""; position:absolute; left:50%; top:28px; bottom:28px; border-left:2px solid rgba(255,255,255,.42); }}
    .ball {{ position:absolute; left:42px; bottom:42px; width:42px; height:42px; border-radius:50%; background:radial-gradient(circle at 34% 30%,#fff 0 22%,#111 23% 30%,#fff 31% 52%,#111 53% 60%,#fff 61%); animation:roll 5s ease-in-out infinite; }}
    @keyframes roll {{ 50% {{ transform:translateX(220px) rotate(260deg); }} }}
    .signal {{ position:absolute; right:26px; bottom:26px; padding:12px 15px; border-radius:14px; color:#fff; background:rgba(3,7,18,.60); border:1px solid rgba(255,255,255,.20); }}
    .signal span {{ display:block; color:#ffe7ad; font-size:12px; font-weight:800; }}
    .signal strong {{ font-size:26px; }}
    nav {{ position:sticky; top:0; z-index:5; padding:12px 36px; display:flex; gap:10px; background:rgba(5,15,25,.92); backdrop-filter:blur(14px); }}
    .navbtn {{ border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.08); color:rgba(255,255,255,.82); border-radius:999px; padding:10px 15px; font-weight:800; cursor:pointer; }}
    .navbtn.active {{ color:#172033; background:linear-gradient(135deg,#ffe8a3,#d9a441); border-color:transparent; }}
    main {{ padding:20px 36px 42px; }}
    .controls,.card,.sim {{ background:rgba(255,255,255,.97); border:1px solid var(--line); border-radius:18px; box-shadow:0 16px 42px rgba(15,23,42,.09); }}
    .controls {{ display:grid; grid-template-columns:repeat(6,minmax(130px,1fr)); gap:12px; padding:15px; margin-bottom:16px; }}
    label {{ display:block; font-size:12px; color:var(--muted); font-weight:800; margin-bottom:6px; }}
    select,input {{ width:100%; border:1px solid var(--line); border-radius:9px; padding:10px; background:#fff; color:var(--ink); }}
    input[type=range] {{ accent-color:var(--green); padding:0; }}
    .kpis {{ display:grid; grid-template-columns:repeat(5,minmax(140px,1fr)); gap:14px; margin-bottom:16px; }}
    .kpi {{ padding:16px; overflow:hidden; position:relative; }}
    .kpi small {{ display:block; color:var(--muted); font-weight:800; }}
    .kpi strong {{ display:block; margin-top:7px; font-size:28px; }}
    .kpi::after {{ content:""; position:absolute; right:-30px; bottom:-40px; width:95px; height:95px; border-radius:50%; background:rgba(15,139,111,.09); }}
    .view {{ display:none; }}
    .view.active {{ display:block; animation:rise .28s ease both; }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(8px); }} }}
    .grid {{ display:grid; grid-template-columns:1.08fr .92fr; gap:16px; }}
    .card {{ padding:16px; min-height:380px; }}
    .card h2,.sim h2 {{ margin:0 0 12px; font-size:18px; }}
    .plot {{ width:100%; height:350px; }}
    .sim {{ display:grid; grid-template-columns:1fr .9fr; gap:18px; padding:16px; }}
    .scenario-deck {{ display:grid; grid-template-columns:repeat(4,minmax(120px,1fr)); gap:10px; margin-bottom:14px; }}
    .scenario {{ text-align:left; border:1px solid var(--line); background:#fff; border-radius:13px; padding:12px; cursor:pointer; box-shadow:0 8px 22px rgba(15,23,42,.06); }}
    .scenario:hover {{ transform:translateY(-2px); border-color:var(--gold); }}
    .scenario strong {{ display:block; }}
    .scenario span {{ color:var(--muted); font-size:11px; }}
    .sim-controls {{ display:grid; grid-template-columns:repeat(2,minmax(140px,1fr)); gap:13px; }}
    .range-line {{ display:flex; justify-content:space-between; color:var(--muted); font-size:12px; margin-top:4px; }}
    .verdict {{ border-radius:16px; border:1px solid var(--line); background:radial-gradient(circle at 100% 0%,rgba(217,164,65,.20),transparent 32%),#fff; padding:16px; }}
    .verdict h3 {{ margin:0; font-size:26px; }}
    .verdict p {{ color:var(--muted); line-height:1.45; }}
    .tiers {{ display:grid; grid-template-columns:repeat(5,1fr); gap:6px; margin-top:12px; }}
    .tier {{ height:9px; border-radius:99px; background:#e6ebf1; }}
    .tier.on:nth-child(1) {{ background:#c2415d; }} .tier.on:nth-child(2) {{ background:#f97316; }}
    .tier.on:nth-child(3) {{ background:#eab308; }} .tier.on:nth-child(4) {{ background:#16a34a; }} .tier.on:nth-child(5) {{ background:#2457c5; }}
    .money,.players {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:12px; padding:10px; border:1px dashed var(--line); border-radius:14px; background:#f8fbff; }}
    .coin {{ width:28px; height:28px; border-radius:50%; display:grid; place-items:center; background:#f7c948; color:#6b4400; font-weight:900; animation:pop .2s ease both; }}
    @keyframes pop {{ from {{ transform:scale(.7); opacity:.35; }} }}
    .player {{ padding:6px 9px; border-radius:999px; background:#e8f7f1; color:#08745b; font-weight:800; font-size:12px; }}
    .player.core {{ background:#fff3d6; color:#8a5a00; }}
    .player.absent {{ color:#94a3b8; background:#f1f5f9; text-decoration:line-through; }}
    table {{ border-collapse:collapse; width:100%; font-size:13px; }}
    th,td {{ padding:10px; border-bottom:1px solid var(--line); text-align:left; }}
    th {{ color:var(--muted); }}
    @media(max-width:960px) {{ .hero,.grid,.sim {{ grid-template-columns:1fr; }} .controls,.kpis {{ grid-template-columns:repeat(2,1fr); }} .scenario-deck {{ grid-template-columns:repeat(2,1fr); }} nav {{ overflow-x:auto; }} }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <div>
        <div class="eyebrow">World Cup Commercial Control Room</div>
        <h1>WorldCupROI Intelligence Platform</h1>
        <div class="deck">A full interactive dashboard for match probability, sponsor ROI, FanScore, weather impact, and counterfactual sponsorship simulation.</div>
      </div>
      <div class="pitch"><div class="ball"></div><div class="signal"><span>LIVE ROI SIGNAL</span><strong id="heroSignal">--</strong></div></div>
    </div>
  </header>
  <nav>
    <button class="navbtn active" data-tab="overview">Overview</button>
    <button class="navbtn" data-tab="match">Match Probability</button>
    <button class="navbtn" data-tab="fan">FanScore</button>
    <button class="navbtn" data-tab="weather">Weather Lab</button>
    <button class="navbtn" data-tab="sim">Simulator</button>
    <button class="navbtn" data-tab="panel">Panel Explorer</button>
  </nav>
  <main>
    <section class="controls">
      <div><label>Team</label><select id="team"></select></div>
      <div><label>Sponsor</label><select id="sponsor"></select></div>
      <div><label>Stage</label><select id="stage"></select></div>
      <div><label>Weather</label><select id="weather"></select></div>
      <div><label>Year</label><input id="year" type="range" min="1930" max="2022" step="4" value="2022"><div class="range-line"><span>1930</span><strong id="yearLabel">2022</strong></div></div>
      <div><label>Search</label><input id="search" placeholder="team, sponsor, opponent"></div>
    </section>
    <section class="kpis" id="kpis"></section>
    <section class="view active" id="overview">
      <div class="grid">
        <div class="card"><h2>Sponsor ROI Map</h2><div id="roiScatter" class="plot"></div></div>
        <div class="card"><h2>Sponsor ROI Ring</h2><div id="roiRing" class="plot"></div></div>
        <div class="card"><h2>Top Teams by ROI</h2><div id="topTeams" class="plot"></div></div>
        <div class="card"><h2>Commercial Segment Mix</h2><div id="segmentMix" class="plot"></div></div>
      </div>
    </section>
    <section class="view" id="match"><div class="grid"><div class="card"><h2>Win / Draw / Loss Probability</h2><div id="matchProb" class="plot"></div></div><div class="card"><h2>Probability Heatmap</h2><div id="probHeat" class="plot"></div></div></div></section>
    <section class="view" id="fan"><div class="grid"><div class="card"><h2>FanScore Radar</h2><div id="fanRadar" class="plot"></div></div><div class="card"><h2>Player & Media Influence</h2><div id="fanBars" class="plot"></div></div></div></section>
    <section class="view" id="weather"><div class="grid"><div class="card"><h2>Weather x Stage ROI Heatmap</h2><div id="weatherHeat" class="plot"></div></div><div class="card"><h2>Temperature and Venue Impact</h2><div id="tempScatter" class="plot"></div></div></div></section>
    <section class="view" id="sim">
      <div class="sim">
        <div>
          <h2>Sponsor Strategy Simulator</h2>
          <div class="scenario-deck">
            <button class="scenario" data-preset="balanced"><strong>Balanced Play</strong><span>Neutral baseline</span></button>
            <button class="scenario" data-preset="allin"><strong>All-in Sponsor</strong><span>Spend and activation push</span></button>
            <button class="scenario" data-preset="starout"><strong>Star Out</strong><span>Player availability shock</span></button>
            <button class="scenario" data-preset="surge"><strong>Media Surge</strong><span>Attention and player boost</span></button>
          </div>
          <div class="sim-controls">
            <div><label>Sponsor Investment</label><input id="spend" type="range" min="50" max="200" value="100" step="5"><div class="range-line"><span>lean</span><strong id="spendLabel">100%</strong><span>aggressive</span></div></div>
            <div><label>Core Player Change</label><input id="core" type="range" min="-40" max="40" value="0" step="5"><div class="range-line"><span>down</span><strong id="coreLabel">0%</strong><span>boost</span></div></div>
            <div><label>Squad Availability</label><input id="avail" type="range" min="60" max="110" value="100" step="5"><div class="range-line"><span>thin</span><strong id="availLabel">100%</strong><span>strong</span></div></div>
            <div><label>Absent Key Players</label><input id="absent" type="range" min="0" max="5" value="0" step="1"><div class="range-line"><span>full</span><strong id="absentLabel">0</strong><span>risk</span></div></div>
          </div>
        </div>
        <div><div class="verdict" id="verdict"></div><div class="money" id="money"></div><div class="players" id="players"></div></div>
      </div>
    </section>
    <section class="view" id="panel"><div class="card"><h2>Ranked Panel Rows</h2><table id="rows"></table></div></section>
  </main>
  <script>
    const source = {data_json};
    const panel = source.panel;
    const matches = source.matches;
    const $ = id => document.getElementById(id);
    const fmt = (x,d=2)=>Number(x||0).toFixed(d);
    const avg = (rows,key)=>rows.length?rows.reduce((s,d)=>s+Number(d[key]||0),0)/rows.length:0;
    const sum = (rows,key)=>rows.reduce((s,d)=>s+Number(d[key]||0),0);
    const colors = {{green:'#0f8b6f',blue:'#2457c5',orange:'#f28c28',gold:'#d9a441',red:'#c2415d',ink:'#102033'}};
    const layout = title => ({{title,margin:{{l:42,r:18,t:48,b:42}},paper_bgcolor:'rgba(255,255,255,0)',plot_bgcolor:'rgba(255,255,255,0)',font:{{family:'Inter, Segoe UI, Arial',color:colors.ink}},hoverlabel:{{bgcolor:colors.ink,bordercolor:colors.gold,font:{{color:'#fff'}}}},legend:{{orientation:'h',y:1.08,x:1,xanchor:'right'}}}});
    function optionize(id, values) {{ $(id).innerHTML = '<option>All</option>' + values.map(v=>`<option>${{v}}</option>`).join(''); }}
    optionize('team', source.teams); optionize('sponsor', source.sponsors); optionize('stage', source.stages); optionize('weather', source.weather);
    function simInputs() {{ return {{spend:+$('spend').value/100, core:+$('core').value/100, avail:+$('avail').value/100, absent:+$('absent').value}}; }}
    function filteredBase() {{
      const team=$('team').value,sponsor=$('sponsor').value,stage=$('stage').value,weather=$('weather').value,year=+$('year').value,q=$('search').value.toLowerCase().trim();
      $('yearLabel').textContent=year;
      return panel.filter(d=>(team==='All'||d.team===team)&&(sponsor==='All'||d.sponsor===sponsor)&&(stage==='All'||d.stage===stage)&&(weather==='All'||d.weather===weather)&&d.year<=year&&(!q||[d.team,d.opponent,d.sponsor,d.stage].join(' ').toLowerCase().includes(q)));
    }}
    function applySim(rows) {{
      const s=simInputs();
      return rows.map(d=>{{
        const spendLift=Math.log(s.spend)*.28+(s.spend-1)*.1*Number(d.activation_quality||0);
        const playerLift=s.core*.72+(s.avail-1)*.58-s.absent*.075;
        const att=s.core*.16-s.absent*.018;
        const roi=Math.max(.45,Number(d.predicted_roi)+spendLift+playerLift);
        const spend=Math.max(.1,Number(d.sponsor_spend_m)*s.spend);
        return {{...d,predicted_roi:roi,roi_delta:roi-Number(d.predicted_roi),sponsor_spend_m:spend,roi_per_million_spend:roi/spend,commercial_momentum:Math.max(.05,Math.min(1.2,Number(d.commercial_momentum)+att+(s.spend-1)*.07)),fan_score_panel:Math.max(.01,Math.min(1.2,Number(d.fan_score_panel)+att))}};
      }});
    }}
    function grouped(rows,key,metric) {{ const m=new Map(); rows.forEach(d=>{{ const k=d[key]; if(!m.has(k))m.set(k,[]); m.get(k).push(d); }}); return [...m].map(([name,items])=>({{name,value:avg(items,metric),count:items.length}})).sort((a,b)=>b.value-a.value); }}
    function renderKpis(rows) {{ $('heroSignal').textContent=fmt(avg(rows,'predicted_roi'))+'x'; $('kpis').innerHTML=[['Panel rows',rows.length],['Avg ROI',fmt(avg(rows,'predicted_roi'))+'x'],['ROI delta',(avg(rows,'roi_delta')>=0?'+':'')+fmt(avg(rows,'roi_delta'))+'x'],['FanScore',fmt(avg(rows,'fan_score_panel'))],['ROI / $M',fmt(avg(rows,'roi_per_million_spend'))]].map(([a,b])=>`<div class="card kpi"><small>${{a}}</small><strong>${{b}}</strong></div>`).join(''); }}
    function renderOverview(rows) {{
      Plotly.react('roiScatter',[{{x:rows.map(d=>d.fan_score_panel),y:rows.map(d=>d.predicted_roi),mode:'markers',type:'scatter',text:rows.map(d=>`${{d.team}} vs ${{d.opponent}}<br>${{d.sponsor}}`),marker:{{size:rows.map(d=>Math.max(7,Math.min(28,d.event_attention_m/2))),color:rows.map(d=>d.commercial_momentum),colorscale:[[0,colors.blue],[.5,colors.green],[1,colors.orange]],showscale:true,line:{{color:'#fff',width:1.2}},opacity:.86}}}}],layout('Sponsor ROI Map: Attention vs Return'),{{responsive:true}});
      const roiPct=Math.max(0,Math.min(100,avg(rows,'predicted_roi')/4.2*100));
      Plotly.react('roiRing',[{{values:[roiPct,100-roiPct],labels:['ROI progress','Remaining'],type:'pie',hole:.72,textinfo:'none',marker:{{colors:[colors.orange,'#e8eef5']}}}}],{{...layout('Sponsor ROI Ring'),showlegend:false,annotations:[{{text:fmt(roiPct,0)+'%',showarrow:false,font:{{size:30,color:colors.ink}}}}]}},{{responsive:true}});
      const top=grouped(rows,'team','predicted_roi').slice(0,12);
      Plotly.react('topTeams',[{{x:top.map(d=>d.name),y:top.map(d=>d.value),type:'bar',marker:{{color:top.map(d=>d.value),colorscale:[[0,colors.blue],[.5,colors.green],[1,colors.orange]],line:{{color:'#fff',width:1}}}}}}],layout('Top Teams by Simulated ROI'),{{responsive:true}});
      const seg=grouped(rows,'commercial_segment','predicted_roi');
      Plotly.react('segmentMix',[{{labels:seg.map(d=>d.name),values:seg.map(d=>d.count),type:'pie',hole:.48,marker:{{colors:[colors.blue,colors.green,colors.orange]}}}}],layout('Commercial Segment Mix'),{{responsive:true}});
    }}
    function renderMatch(rows) {{
      const ms=matches.filter(m=>rows.some(r=>r.match_id===m.match_id)).slice(0,24);
      const x=ms.map(d=>d.match_id), pA=ms.map(d=>Math.max(.08,Math.min(.84,1/(1+Math.exp(-d.elo_diff/260))))); const pD=pA.map(p=>Math.max(.1,Math.min(.34,.30-Math.abs(p-.5)*.28))); const pB=pA.map((p,i)=>Math.max(.04,1-p-pD[i]));
      Plotly.react('matchProb',[{{x,y:pA,name:'Team A win',type:'bar',marker:{{color:colors.green}}}},{{x,y:pD,name:'Draw',type:'bar',marker:{{color:colors.orange}}}},{{x,y:pB,name:'Team B win',type:'bar',marker:{{color:colors.blue}}}}],{{...layout('Win / Draw / Loss Probability'),barmode:'stack',yaxis:{{tickformat:'.0%'}}}},{{responsive:true}});
      Plotly.react('probHeat',[{{z:[pA,pD,pB],x:x,y:['A win','Draw','B win'],type:'heatmap',colorscale:[[0,'#f8fbff'],[.5,'#8ed1b2'],[1,colors.orange]],hoverongaps:false}}],layout('Probability Heatmap'),{{responsive:true}});
    }}
    function renderFan(rows) {{
      const vals=[avg(rows,'player_followers_m'),avg(rows,'event_attention_m'),avg(rows,'media_reposts_k')/10,avg(rows,'fan_score_panel')*100,avg(rows,'commercial_momentum')*100]; const labs=['Player followers','Event attention','Media reposts','FanScore','Momentum'];
      Plotly.react('fanRadar',[{{type:'scatterpolar',r:[...vals,vals[0]],theta:[...labs,labs[0]],fill:'toself',line:{{color:colors.green,width:4}},fillcolor:'rgba(15,139,111,.24)',marker:{{color:colors.orange,size:8}}}}],{{...layout('FanScore Radar'),polar:{{bgcolor:'rgba(15,139,111,.04)',radialaxis:{{visible:true}}}},showlegend:false}},{{responsive:true}});
      Plotly.react('fanBars',[{{x:labs,y:vals,type:'bar',marker:{{color:[colors.blue,colors.green,colors.orange,colors.gold,colors.red]}}}}],layout('Player and Media Influence Components'),{{responsive:true}});
    }}
    function renderWeather(rows) {{
      const stages=[...new Set(rows.map(d=>d.stage))], weathers=[...new Set(rows.map(d=>d.weather))];
      const z=weathers.map(w=>stages.map(s=>avg(rows.filter(d=>d.weather===w&&d.stage===s),'predicted_roi')));
      Plotly.react('weatherHeat',[{{x:stages,y:weathers,z,type:'heatmap',colorscale:[[0,'#f8fbff'],[.4,'#bce7d1'],[.7,colors.green],[1,colors.orange]],xgap:3,ygap:3}}],layout('Weather x Stage ROI Heatmap'),{{responsive:true}});
      Plotly.react('tempScatter',[{{x:rows.map(d=>d.temperature_c),y:rows.map(d=>d.predicted_roi),mode:'markers',type:'scatter',text:rows.map(d=>`${{d.team}} / ${{d.weather}} / ${{d.stage}}`),marker:{{size:rows.map(d=>8+d.sponsor_power_index*14),color:rows.map(d=>d.sponsor_power_index),colorscale:[[0,colors.blue],[.6,colors.green],[1,colors.orange]],line:{{color:'#fff',width:1}},opacity:.82}}}}],layout('Temperature, Sponsor Power, and ROI'),{{responsive:true}});
    }}
    function tier(avgRoi,delta) {{ if(avgRoi>=3.25||delta>=.35)return[4,'PERFECT','Premium output. ROI and momentum support aggressive activation.']; if(avgRoi>=2.9||delta>=.15)return[3,'HAPPY','High efficiency. The sponsor mix is producing upside.']; if(avgRoi>=2.55||delta>=-.05)return[2,'STABLE','Balanced result. Upside depends on attention quality.']; if(avgRoi>=2.25||delta>=-.25)return[1,'CAUTION','Weak output. Player or media risk is reducing efficiency.']; return[0,'LOW RETURN','ROI is under pressure. Spend discipline is needed.']; }}
    function renderSim(rows) {{ const s=simInputs(); $('spendLabel').textContent=Math.round(s.spend*100)+'%'; $('coreLabel').textContent=(s.core>=0?'+':'')+Math.round(s.core*100)+'%'; $('availLabel').textContent=Math.round(s.avail*100)+'%'; $('absentLabel').textContent=s.absent; const [idx,title,note]=tier(avg(rows,'predicted_roi'),avg(rows,'roi_delta')); $('verdict').innerHTML=`<h3>${{title}}</h3><p>${{note}}</p><div class="tiers">${{[0,1,2,3,4].map(i=>`<span class="tier ${{i<=idx?'on':''}}"></span>`).join('')}}</div>`; $('money').innerHTML=Array.from({{length:Math.max(2,Math.min(18,Math.round(s.spend*8)))}},(_,i)=>`<span class="coin">$</span>`).join(''); $('players').innerHTML=Array.from({{length:11}},(_,i)=>`<span class="player ${{i<3?'core':''}} ${{i>=11-s.absent?'absent':''}}">${{i<3?'Core '+(i+1):'P'+(i+1)}}</span>`).join(''); }}
    function renderRows(rows) {{ const top=[...rows].sort((a,b)=>b.predicted_roi-a.predicted_roi).slice(0,28); const cols=['team','opponent','stage','sponsor','weather','predicted_roi','roi_delta','fan_score_panel','commercial_momentum','roi_per_million_spend']; $('rows').innerHTML=`<thead><tr>${{cols.map(c=>`<th>${{c}}</th>`).join('')}}</tr></thead><tbody>${{top.map(r=>`<tr>${{cols.map(c=>`<td>${{typeof r[c]==='number'?fmt(r[c],3):r[c]}}</td>`).join('')}}</tr>`).join('')}}</tbody>`; }}
    function renderAll() {{ const rows=applySim(filteredBase()); renderKpis(rows); renderOverview(rows); renderMatch(rows); renderFan(rows); renderWeather(rows); renderSim(rows); renderRows(rows); }}
    ['team','sponsor','stage','weather','year','search','spend','core','avail','absent'].forEach(id=>$(id).addEventListener('input',renderAll));
    document.querySelectorAll('.navbtn').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.navbtn').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');$(b.dataset.tab).classList.add('active');setTimeout(renderAll,50);}}));
    document.querySelectorAll('.scenario').forEach(card=>card.addEventListener('click',()=>{{const p={{balanced:[100,0,100,0],allin:[185,20,105,0],starout:[90,-30,75,4],surge:[145,35,110,0]}}[card.dataset.preset]; ['spend','core','avail','absent'].forEach((id,i)=>$(id).value=p[i]); renderAll();}}));
    renderAll();
  </script>
</body>
</html>"""


def main() -> None:
    ensure_data()
    panel = pd.read_csv(DATA_DIR / "panel_dataset.csv")
    matches = pd.read_csv(DATA_DIR / "modeling_dataset.csv")
    DASHBOARD_DIR.mkdir(exist_ok=True)
    (DASHBOARD_DIR / "panel_dashboard.html").write_text(build_dashboard(panel, matches), encoding="utf-8")
    print(f"Saved Plotly dashboard to {DASHBOARD_DIR / 'panel_dashboard.html'}")


if __name__ == "__main__":
    main()
