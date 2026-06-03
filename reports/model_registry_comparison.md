# Model Registry

The platform keeps dependency-free fallback models runnable while documenting optional production models.

## Benchmark Results

| task | model | status | primary_metric | score | secondary_metric | secondary_score | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| match_outcome | Centroid classifier | trained | accuracy | 0.5566 | log_loss | 0.978 | dependency-free baseline |
| sponsor_roi | Ridge regression | trained | r2 | 0.8687 | mae | 0.1177 | dependency-free baseline |
| tabular classification + regression | XGBoost | not_installed |  |  |  |  | install `xgboost` to enable full benchmark |
| tabular classification + regression | LightGBM | not_installed |  |  |  |  | install `lightgbm` to enable full benchmark |
| categorical tabular modeling | CatBoost | not_installed |  |  |  |  | install `catboost` to enable full benchmark |

## Model Catalog

| model | package | task | status | available |
| --- | --- | --- | --- | --- |
| Logistic Regression | sklearn | match classification | optional | False |
| Random Forest | sklearn | match classification + ROI regression | optional | False |
| XGBoost | xgboost | tabular classification + regression | optional | False |
| LightGBM | lightgbm | tabular classification + regression | optional | False |
| CatBoost | catboost | categorical tabular modeling | optional | False |
| MLP | sklearn | dense neural baseline | optional | False |
| Centroid classifier | built-in | match classification fallback | available | True |
| Ridge regression | built-in | ROI regression fallback | available | True |