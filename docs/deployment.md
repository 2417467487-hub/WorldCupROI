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
5. Optional CI/CD: add GitHub secret `STREAMLIT_DEPLOY_HOOK_URL` if your Streamlit Cloud workspace exposes a deploy webhook. The `.github/workflows/streamlit-cloud.yml` workflow will smoke test the app and call the hook after pushes to `main`.

## GitHub Actions CI/CD

- `.github/workflows/ci.yml`: compile modules and run the reproducible pipeline.
- `.github/workflows/streamlit-cloud.yml`: build demo artifacts, smoke test Streamlit, and optionally trigger Streamlit Cloud redeploy.

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