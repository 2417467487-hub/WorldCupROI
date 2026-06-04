# Project Artifacts

This page keeps the generated media, showcase documents, and reproducibility entrypoints organized inside WorldCupROI.

## Showcase Media

| Artifact | Path | Purpose |
|---|---|---|
| Dashboard overview GIF | `assets/gifs/dashboard_overview.gif` | Main README hero animation showing KPIs, ROI, FanScore, and sponsor ranking. |
| Scenario simulation GIF | `assets/gifs/scenario_simulation.gif` | Demonstrates sponsor spend, media exposure, and player-status interaction. |
| Risk uncertainty GIF | `assets/gifs/risk_uncertainty.gif` | Shows prediction intervals, Monte Carlo risk, and negative ROI probability. |
| Network graph GIF | `assets/gifs/network_graph.gif` | Shows Sponsor-Team-Player relationship exploration and centrality ranking. |
| Demo video | `assets/videos/worldcuproi_demo.mp4` | Three-minute project walkthrough for GitHub, portfolio, and presentation use. |
| Video cover | `assets/images/video_cover.png` | README video thumbnail. |

## Preview Images

| Artifact | Path | Purpose |
|---|---|---|
| Dashboard preview | `assets/images/gif_previews/dashboard_overview.png` | Static fallback preview for the dashboard overview GIF. |
| Scenario preview | `assets/images/gif_previews/scenario_simulation.png` | Static fallback preview for scenario simulation. |
| Risk preview | `assets/images/gif_previews/risk_uncertainty.png` | Static fallback preview for risk analysis. |
| Network preview | `assets/images/gif_previews/network_graph.png` | Static fallback preview for graph intelligence. |
| Showcase background | `assets/images/showcase_background.png` | High-resolution background used by generated showcase media. |
| GIF background | `assets/images/showcase_background_gif.png` | Lightweight background used by GIF rendering. |

## Documentation

| Document | Path | Role |
|---|---|---|
| Demo video guide | `docs/demo_video.md` | Storyboard, timing, and public mirror placeholders for the demo video. |
| Project artifact index | `docs/project_artifacts.md` | Inventory of generated showcase files and how they fit into the project. |
| Research brief | `reports/sponsorship_intelligence_brief.md` | Commercial and research framing for the platform. |
| Dataset card | `docs/dataset_card.md` | Data boundaries, mock/proxy fields, and future real-API extension notes. |

## Reproducibility Entrypoints

| Entrypoint | Command | Output |
|---|---|---|
| Full analytics pipeline | `python scripts/run_pipeline.py` | Rebuilds data, features, models, reports, and dashboard outputs. |
| README/model visuals | `make assets` | Regenerates README figures, model visuals, and showcase media. |
| Showcase media only | `python scripts/generate_showcase_media.py` | Rebuilds GIFs, video cover, preview images, and demo video. |
| Dashboard | `streamlit run dashboard/app.py` | Starts the interactive dashboard locally. |

## Repository Language Notes

Generated HTML dashboards and media assets are marked through `.gitattributes` so GitHub language statistics emphasize the Python analytics platform rather than static exports.
