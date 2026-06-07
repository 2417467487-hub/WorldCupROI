PYTHON ?= ml-python

.PHONY: pipeline demo dashboard assets platform-gif streamlit-gif health

pipeline:
	$(PYTHON) scripts/run_pipeline.py

dashboard:
	$(PYTHON) -m streamlit run dashboard/app.py

demo:
	$(PYTHON) scripts/run_pipeline.py --demo

assets:
	$(PYTHON) scripts/generate_readme_assets.py
	$(PYTHON) scripts/generate_model_visuals.py
	$(PYTHON) scripts/generate_academic_figures.py
	$(PYTHON) scripts/generate_showcase_media.py
	node scripts/capture_static_platform_gif.js
	node scripts/capture_streamlit_dashboard_gif.js

platform-gif:
	node scripts/capture_static_platform_gif.js

streamlit-gif:
	node scripts/capture_streamlit_dashboard_gif.js

health:
	$(PYTHON) src/platform_health.py
