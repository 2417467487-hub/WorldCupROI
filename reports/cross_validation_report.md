# Cross-Validation Generalization Report

Cross-validation, sub-sample validation, and temporal sliding validation evaluate whether the current fallback models generalize beyond a single deterministic holdout split.

## Summary

| validation_type | task | model | metric | folds | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kfold | match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5436 | 0.0389 | 0.5026 | 0.6010 |
| kfold | match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9861 | 0.0230 | 0.9584 | 1.0150 |
| kfold | sponsor_roi | RidgeROIModel | mae | 5 | 0.1165 | 0.0072 | 0.1084 | 0.1254 |
| kfold | sponsor_roi | RidgeROIModel | r2 | 5 | 0.8813 | 0.0131 | 0.8670 | 0.8991 |
| kfold | sponsor_roi | RidgeROIModel | rmse | 5 | 0.1426 | 0.0074 | 0.1329 | 0.1495 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5438 | 0.0000 | 0.5438 | 0.5438 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9784 | 0.0000 | 0.9784 | 0.9784 |
| subsample_55pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1167 | 0.0000 | 0.1167 | 0.1167 |
| subsample_55pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8830 | 0.0000 | 0.8830 | 0.8830 |
| subsample_55pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1439 | 0.0000 | 0.1439 | 0.1439 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5552 | 0.0000 | 0.5552 | 0.5552 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9401 | 0.0000 | 0.9401 | 0.9401 |
| subsample_70pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1150 | 0.0000 | 0.1150 | 0.1150 |
| subsample_70pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8797 | 0.0000 | 0.8797 | 0.8797 |
| subsample_70pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1409 | 0.0000 | 0.1409 | 0.1409 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5310 | 0.0000 | 0.5310 | 0.5310 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0107 | 0.0000 | 1.0107 | 1.0107 |
| subsample_85pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1126 | 0.0000 | 0.1126 | 0.1126 |
| subsample_85pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8921 | 0.0000 | 0.8921 | 0.8921 |
| subsample_85pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1407 | 0.0000 | 0.1407 | 0.1407 |
| temporal_train_to_1938_test_1950 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5909 | 0.0000 | 0.5909 | 0.5909 |
| temporal_train_to_1938_test_1950 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0437 | 0.0000 | 1.0437 | 1.0437 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1462 | 0.0000 | 0.1462 | 0.1462 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.6311 | 0.0000 | 0.6311 | 0.6311 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1859 | 0.0000 | 0.1859 | 0.1859 |
| temporal_train_to_1950_test_1954 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5385 | 0.0000 | 0.5385 | 0.5385 |
| temporal_train_to_1950_test_1954 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0024 | 0.0000 | 1.0024 | 1.0024 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1213 | 0.0000 | 0.1213 | 0.1213 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8693 | 0.0000 | 0.8693 | 0.8693 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1497 | 0.0000 | 0.1497 | 0.1497 |
| temporal_train_to_1954_test_1958 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.3714 | 0.0000 | 0.3714 | 0.3714 |
| temporal_train_to_1954_test_1958 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.1387 | 0.0000 | 1.1387 | 1.1387 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1230 | 0.0000 | 0.1230 | 0.1230 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7394 | 0.0000 | 0.7394 | 0.7394 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1613 | 0.0000 | 0.1613 | 0.1613 |
| temporal_train_to_1958_test_1962 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4062 | 0.0000 | 0.4062 | 0.4062 |
| temporal_train_to_1958_test_1962 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0633 | 0.0000 | 1.0633 | 1.0633 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1430 | 0.0000 | 0.1430 | 0.1430 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7229 | 0.0000 | 0.7229 | 0.7229 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1772 | 0.0000 | 0.1772 | 0.1772 |
| temporal_train_to_1962_test_1966 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5000 | 0.0000 | 0.5000 | 0.5000 |
| temporal_train_to_1962_test_1966 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0056 | 0.0000 | 1.0056 | 1.0056 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1284 | 0.0000 | 0.1284 | 0.1284 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8446 | 0.0000 | 0.8446 | 0.8446 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1546 | 0.0000 | 0.1546 | 0.1546 |
| temporal_train_to_1966_test_1970 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.7500 | 0.0000 | 0.7500 | 0.7500 |
| temporal_train_to_1966_test_1970 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.8675 | 0.0000 | 0.8675 | 0.8675 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | mae | 1 | 0.0982 | 0.0000 | 0.0982 | 0.0982 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.9200 | 0.0000 | 0.9200 | 0.9200 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1225 | 0.0000 | 0.1225 | 0.1225 |
| temporal_train_to_1970_test_1974 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4737 | 0.0000 | 0.4737 | 0.4737 |
| temporal_train_to_1970_test_1974 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9963 | 0.0000 | 0.9963 | 0.9963 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1388 | 0.0000 | 0.1388 | 0.1388 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8426 | 0.0000 | 0.8426 | 0.8426 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1708 | 0.0000 | 0.1708 | 0.1708 |
| temporal_train_to_1974_test_1978 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5789 | 0.0000 | 0.5789 | 0.5789 |
| temporal_train_to_1974_test_1978 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0137 | 0.0000 | 1.0137 | 1.0137 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1245 | 0.0000 | 0.1245 | 0.1245 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8637 | 0.0000 | 0.8637 | 0.8637 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1452 | 0.0000 | 0.1452 | 0.1452 |
| temporal_train_to_1978_test_1982 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4808 | 0.0000 | 0.4808 | 0.4808 |
| temporal_train_to_1978_test_1982 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9947 | 0.0000 | 0.9947 | 0.9947 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1163 | 0.0000 | 0.1163 | 0.1163 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8332 | 0.0000 | 0.8332 | 0.8332 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1417 | 0.0000 | 0.1417 | 0.1417 |
| temporal_train_to_1982_test_1986 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5577 | 0.0000 | 0.5577 | 0.5577 |
| temporal_train_to_1982_test_1986 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9450 | 0.0000 | 0.9450 | 0.9450 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1208 | 0.0000 | 0.1208 | 0.1208 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8625 | 0.0000 | 0.8625 | 0.8625 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1412 | 0.0000 | 0.1412 | 0.1412 |
| temporal_train_to_1986_test_1990 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5577 | 0.0000 | 0.5577 | 0.5577 |
| temporal_train_to_1986_test_1990 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9787 | 0.0000 | 0.9787 | 0.9787 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1250 | 0.0000 | 0.1250 | 0.1250 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8711 | 0.0000 | 0.8711 | 0.8711 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1534 | 0.0000 | 0.1534 | 0.1534 |
| temporal_train_to_1990_test_1994 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5577 | 0.0000 | 0.5577 | 0.5577 |
| temporal_train_to_1990_test_1994 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0023 | 0.0000 | 1.0023 | 1.0023 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1305 | 0.0000 | 0.1305 | 0.1305 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8649 | 0.0000 | 0.8649 | 0.8649 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1688 | 0.0000 | 0.1688 | 0.1688 |
| temporal_train_to_1994_test_1998 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5781 | 0.0000 | 0.5781 | 0.5781 |
| temporal_train_to_1994_test_1998 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9360 | 0.0000 | 0.9360 | 0.9360 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1114 | 0.0000 | 0.1114 | 0.1114 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8972 | 0.0000 | 0.8972 | 0.8972 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1264 | 0.0000 | 0.1264 | 0.1264 |
| temporal_train_to_1998_test_2002 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4844 | 0.0000 | 0.4844 | 0.4844 |
| temporal_train_to_1998_test_2002 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0377 | 0.0000 | 1.0377 | 1.0377 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1312 | 0.0000 | 0.1312 | 0.1312 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8666 | 0.0000 | 0.8666 | 0.8666 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1559 | 0.0000 | 0.1559 | 0.1559 |
| temporal_train_to_2002_test_2006 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6406 | 0.0000 | 0.6406 | 0.6406 |
| temporal_train_to_2002_test_2006 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.8748 | 0.0000 | 0.8748 | 0.8748 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1166 | 0.0000 | 0.1166 | 0.1166 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.9124 | 0.0000 | 0.9124 | 0.9124 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1419 | 0.0000 | 0.1419 | 0.1419 |
| temporal_train_to_2006_test_2010 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4844 | 0.0000 | 0.4844 | 0.4844 |
| temporal_train_to_2006_test_2010 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9985 | 0.0000 | 0.9985 | 0.9985 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1289 | 0.0000 | 0.1289 | 0.1289 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8880 | 0.0000 | 0.8880 | 0.8880 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1534 | 0.0000 | 0.1534 | 0.1534 |
| temporal_train_to_2010_test_2014 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5625 | 0.0000 | 0.5625 | 0.5625 |
| temporal_train_to_2010_test_2014 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9713 | 0.0000 | 0.9713 | 0.9713 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1124 | 0.0000 | 0.1124 | 0.1124 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8838 | 0.0000 | 0.8838 | 0.8838 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1445 | 0.0000 | 0.1445 | 0.1445 |
| temporal_train_to_2014_test_2018 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6094 | 0.0000 | 0.6094 | 0.6094 |
| temporal_train_to_2014_test_2018 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9417 | 0.0000 | 0.9417 | 0.9417 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1176 | 0.0000 | 0.1176 | 0.1176 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8667 | 0.0000 | 0.8667 | 0.8667 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1471 | 0.0000 | 0.1471 | 0.1471 |
| temporal_train_to_2018_test_2022 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6250 | 0.0000 | 0.6250 | 0.6250 |
| temporal_train_to_2018_test_2022 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9797 | 0.0000 | 0.9797 | 0.9797 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1089 | 0.0000 | 0.1089 | 0.1089 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8884 | 0.0000 | 0.8884 | 0.8884 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1427 | 0.0000 | 0.1427 | 0.1427 |

## Interpretation

- `kfold` estimates average generalization under random tournament-mixed splits.
- `subsample_*` measures sample-size sensitivity and whether performance collapses when fewer rows are available.
- `temporal_train_to_*` is the highest-risk diagnostic because it asks older tournaments to predict a later tournament.
- Match outcome accuracy should be read as a directional baseline because football outcomes are noisy and class balance changes by tournament era.
- Sponsor ROI R2 and MAE are bounded by proxy-label realism; temporal degradation is a signal to replace mock commercial variables.
- Large fold-to-fold variance should trigger data leakage review, stronger temporal features, or calibrated model selection before production use.