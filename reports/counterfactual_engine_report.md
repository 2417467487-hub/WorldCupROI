# Counterfactual Engine Report

This module simulates player injury, media change and budget interventions and reports ROI change intervals.

| scenario | avg_delta | low | high |
| --- | --- | --- | --- |
| budget_cut | -0.1404 | 3.9818 | 4.2258 |
| budget_reallocation | 0.1128 | 4.2455 | 4.4685 |
| late_stage_activation | 0.1884 | 4.3001 | 4.5651 |
| media_surge | 0.228 | 4.3292 | 4.6152 |
| player_injury_shock | -0.2632 | 3.824 | 4.138 |

## Upgrade Path

- Synthetic Control: build sponsor/team counterfactual baselines from comparable historical matches.
- SCM: formalize injury, exposure and budget interventions as structural equations.
- Causal sensitivity: evaluate how robust ROI lift is to unobserved media quality.