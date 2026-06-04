.PHONY: pipeline dashboard assets

pipeline:
	python scripts/run_pipeline.py

dashboard:
	streamlit run dashboard/app.py

assets:
	python scripts/generate_readme_assets.py
	python scripts/generate_model_visuals.py
	python scripts/generate_showcase_media.py
