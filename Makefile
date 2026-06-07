PYTHON ?= ml-python

.PHONY: pipeline demo dashboard assets health

pipeline:
	$(PYTHON) scripts/run_pipeline.py

dashboard:
	$(PYTHON) -m streamlit run dashboard/app.py

demo:
	$(PYTHON) scripts/run_pipeline.py --demo

assets:
	$(PYTHON) scripts/generate_readme_assets.py
	$(PYTHON) scripts/generate_model_visuals.py
	$(PYTHON) scripts/generate_showcase_media.py

health:
	$(PYTHON) src/platform_health.py
