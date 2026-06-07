# Deployment Guide

## One-Command Local Run

```powershell
make demo
make dashboard
```

## Streamlit Cloud

1. Push the repository to GitHub.
2. Create a Streamlit Cloud app from `dashboard/app.py`.
3. Set Python dependencies from `requirements.txt`.
4. Run `make demo` locally before each release to refresh committed demo artifacts.

## GitHub Pages

1. Run `make assets` and `make pipeline`.
2. Publish `index.html`, `dashboard/panel_dashboard.html`, `assets/`, `docs/`, and selected `reports/` files.
3. Use GitHub Pages branch settings to serve from the repository root.

## Docker

```powershell
docker build -t worldcuproi .
docker run --rm -p 8501:8501 worldcuproi
```

## Demo Mode Contract

`--demo` uses local fallback/demo data and does not require external APIs. This keeps the project reproducible for reviewers, Streamlit Cloud, and offline portfolio demos.