PYTHON ?= E:/workspace/tools/bin/ml-python.cmd

.PHONY: pipeline demo dashboard assets platform-gif streamlit-gif hero-gif preview-gifs health

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
	$(PYTHON) scripts/generate_decision_intelligence_figures.py
	$(PYTHON) scripts/generate_showcase_media.py
	node scripts/capture_static_platform_gif.js
	node scripts/capture_static_preview_gifs.js
	node scripts/capture_static_hero_gif.js
	node scripts/capture_streamlit_dashboard_gif.js

platform-gif:
	node scripts/capture_static_platform_gif.js

streamlit-gif:
	node scripts/capture_streamlit_dashboard_gif.js

hero-gif:
	node scripts/capture_static_hero_gif.js

preview-gifs:
	node scripts/capture_static_preview_gifs.js

health:
	$(PYTHON) src/platform_health.py
