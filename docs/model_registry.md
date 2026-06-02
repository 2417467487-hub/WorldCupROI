# Model Zoo and Upgrade Path

WorldCupROI keeps the default pipeline lightweight, while documenting a full research-grade model family.

## Traditional ML

| Model | Use |
|---|---|
| Logistic Regression | interpretable match outcome baseline |
| Random Forest | robust tabular baseline |
| XGBoost | non-linear tabular prediction with SHAP support |
| LightGBM | scalable gradient boosting for large feature tables |
| CatBoost | categorical-heavy sponsor and team features |

## Deep Learning

| Model | Use |
|---|---|
| MLP | dense sports-business feature learning |
| LSTM / GRU | temporal attention and team form sequences |
| TabNet | attentive tabular feature selection |
| TabTransformer | contextual categorical embeddings |

## Graph Neural Networks

| Model | Graph |
|---|---|
| GCN | team-player-sponsor-match graph |
| GraphSAGE | inductive sponsor/team relationship modeling |

## Ensemble and Report Generation

| Method | Use |
|---|---|
| Stacking | combine match, fan, sponsor, and ROI learners |
| Voting | robust classification/regression ensemble |
| Generative report model | convert predictions, SHAP, and scenarios into narrative business recommendations |

## Uncertainty Quantification

| Method | Output |
|---|---|
| Conformal prediction | ROI prediction intervals and coverage |
| Bootstrap | confidence intervals for ROI estimates |
| Monte Carlo | negative ROI probability and risk distribution |
| Ensemble variance | model disagreement risk score |
