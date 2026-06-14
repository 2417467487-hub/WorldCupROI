# Model Registry

The platform keeps dependency-free fallback models runnable while documenting optional production models.

## Benchmark Results

| task | model | status | primary_metric | score | secondary_metric | secondary_score | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| match_outcome | Centroid classifier | trained | accuracy | 0.5023 | log_loss | 1.0097 | dependency-free baseline |
| sponsor_roi | Ridge regression | trained | r2 | 0.8478 | mae | 0.1165 | dependency-free baseline |
| match_outcome | Logistic Regression | trained | accuracy | 0.5399 | package | sklearn | optional benchmark |
| match_outcome | Random Forest | trained | accuracy | 0.5211 | package | sklearn | optional benchmark |
| match_outcome | MLP | trained | accuracy | 0.4836 | package | sklearn | optional benchmark |
| sponsor_roi | Random Forest | trained | r2 | 0.8186 | mae | 0.1249 | optional benchmark |
| sponsor_roi | MLP | trained | r2 | -3.7307 | mae | 0.6281 | optional benchmark |
| tabular classification + regression | XGBoost | available |  |  |  |  | install `xgboost` to enable full benchmark |
| tabular classification + regression | LightGBM | available |  |  |  |  | install `lightgbm` to enable full benchmark |
| categorical tabular modeling | CatBoost | available |  |  |  |  | install `catboost` to enable full benchmark |

## Model Catalog

| model | package | task | status | available |
| --- | --- | --- | --- | --- |
| Logistic Regression | sklearn | match classification | optional | True |
| Random Forest | sklearn | match classification + ROI regression | optional | True |
| XGBoost | xgboost | tabular classification + regression | optional | True |
| LightGBM | lightgbm | tabular classification + regression | optional | True |
| CatBoost | catboost | categorical tabular modeling | optional | True |
| MLP | sklearn | dense neural baseline | optional | True |
| Centroid classifier | built-in | match classification fallback | available | True |
| Ridge regression | built-in | ROI regression fallback | available | True |