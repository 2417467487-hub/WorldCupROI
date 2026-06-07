.PHONY: pipeline dashboard assets health

pipeline:
	python scripts/run_pipeline.py

dashboard:
	streamlit run dashboard/app.py

assets:
	python scripts/generate_readme_assets.py
	python scripts/generate_model_visuals.py
	python scripts/generate_showcase_media.py

health:
	python src/platform_health.py
