# Cross-Validation Generalization Report

Cross-validation, sub-sample validation, and temporal sliding validation evaluate whether the current fallback models generalize beyond a single deterministic holdout split.

## Summary

| validation_type | task | model | metric | folds | mean | std | min | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kfold | match_outcome | CentroidOutcomeModel | accuracy | 5 | 0.5236 | 0.0494 | 0.4639 | 0.6000 |
| kfold | match_outcome | CentroidOutcomeModel | log_loss | 5 | 0.9888 | 0.0189 | 0.9707 | 1.0165 |
| kfold | sponsor_roi | RidgeROIModel | mae | 5 | 0.1159 | 0.0085 | 0.1061 | 0.1278 |
| kfold | sponsor_roi | RidgeROIModel | r2 | 5 | 0.8447 | 0.0108 | 0.8364 | 0.8632 |
| kfold | sponsor_roi | RidgeROIModel | rmse | 5 | 0.1424 | 0.0083 | 0.1325 | 0.1518 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5571 | 0.0000 | 0.5571 | 0.5571 |
| subsample_55pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9801 | 0.0000 | 0.9801 | 0.9801 |
| subsample_55pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1154 | 0.0000 | 0.1154 | 0.1154 |
| subsample_55pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8459 | 0.0000 | 0.8459 | 0.8459 |
| subsample_55pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1432 | 0.0000 | 0.1432 | 0.1432 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5411 | 0.0000 | 0.5411 | 0.5411 |
| subsample_70pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9566 | 0.0000 | 0.9566 | 0.9566 |
| subsample_70pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1120 | 0.0000 | 0.1120 | 0.1120 |
| subsample_70pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8565 | 0.0000 | 0.8565 | 0.8565 |
| subsample_70pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1378 | 0.0000 | 0.1378 | 0.1378 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4863 | 0.0000 | 0.4863 | 0.4863 |
| subsample_85pct | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0182 | 0.0000 | 1.0182 | 1.0182 |
| subsample_85pct | sponsor_roi | RidgeROIModel | mae | 1 | 0.1160 | 0.0000 | 0.1160 | 0.1160 |
| subsample_85pct | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8358 | 0.0000 | 0.8358 | 0.8358 |
| subsample_85pct | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1438 | 0.0000 | 0.1438 | 0.1438 |
| temporal_train_to_1938_test_1950 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5455 | 0.0000 | 0.5455 | 0.5455 |
| temporal_train_to_1938_test_1950 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0430 | 0.0000 | 1.0430 | 1.0430 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1065 | 0.0000 | 0.1065 | 0.1065 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8947 | 0.0000 | 0.8947 | 0.8947 |
| temporal_train_to_1938_test_1950 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1286 | 0.0000 | 0.1286 | 0.1286 |
| temporal_train_to_1950_test_1954 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6154 | 0.0000 | 0.6154 | 0.6154 |
| temporal_train_to_1950_test_1954 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9945 | 0.0000 | 0.9945 | 0.9945 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1032 | 0.0000 | 0.1032 | 0.1032 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7617 | 0.0000 | 0.7617 | 0.7617 |
| temporal_train_to_1950_test_1954 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1511 | 0.0000 | 0.1511 | 0.1511 |
| temporal_train_to_1954_test_1958 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.3429 | 0.0000 | 0.3429 | 0.3429 |
| temporal_train_to_1954_test_1958 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.1170 | 0.0000 | 1.1170 | 1.1170 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1394 | 0.0000 | 0.1394 | 0.1394 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.6840 | 0.0000 | 0.6840 | 0.6840 |
| temporal_train_to_1954_test_1958 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1747 | 0.0000 | 0.1747 | 0.1747 |
| temporal_train_to_1958_test_1962 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5000 | 0.0000 | 0.5000 | 0.5000 |
| temporal_train_to_1958_test_1962 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0147 | 0.0000 | 1.0147 | 1.0147 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1316 | 0.0000 | 0.1316 | 0.1316 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7770 | 0.0000 | 0.7770 | 0.7770 |
| temporal_train_to_1958_test_1962 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1648 | 0.0000 | 0.1648 | 0.1648 |
| temporal_train_to_1962_test_1966 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5312 | 0.0000 | 0.5312 | 0.5312 |
| temporal_train_to_1962_test_1966 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0350 | 0.0000 | 1.0350 | 1.0350 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1379 | 0.0000 | 0.1379 | 0.1379 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7660 | 0.0000 | 0.7660 | 0.7660 |
| temporal_train_to_1962_test_1966 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1671 | 0.0000 | 0.1671 | 0.1671 |
| temporal_train_to_1966_test_1970 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.7188 | 0.0000 | 0.7188 | 0.7188 |
| temporal_train_to_1966_test_1970 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.8165 | 0.0000 | 0.8165 | 0.8165 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1057 | 0.0000 | 0.1057 | 0.1057 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.9040 | 0.0000 | 0.9040 | 0.9040 |
| temporal_train_to_1966_test_1970 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1229 | 0.0000 | 0.1229 | 0.1229 |
| temporal_train_to_1970_test_1974 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5000 | 0.0000 | 0.5000 | 0.5000 |
| temporal_train_to_1970_test_1974 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0542 | 0.0000 | 1.0542 | 1.0542 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1324 | 0.0000 | 0.1324 | 0.1324 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8069 | 0.0000 | 0.8069 | 0.8069 |
| temporal_train_to_1970_test_1974 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1594 | 0.0000 | 0.1594 | 0.1594 |
| temporal_train_to_1974_test_1978 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5789 | 0.0000 | 0.5789 | 0.5789 |
| temporal_train_to_1974_test_1978 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9631 | 0.0000 | 0.9631 | 0.9631 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1172 | 0.0000 | 0.1172 | 0.1172 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8646 | 0.0000 | 0.8646 | 0.8646 |
| temporal_train_to_1974_test_1978 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1344 | 0.0000 | 0.1344 | 0.1344 |
| temporal_train_to_1978_test_1982 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4808 | 0.0000 | 0.4808 | 0.4808 |
| temporal_train_to_1978_test_1982 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9983 | 0.0000 | 0.9983 | 0.9983 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1218 | 0.0000 | 0.1218 | 0.1218 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8002 | 0.0000 | 0.8002 | 0.8002 |
| temporal_train_to_1978_test_1982 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1520 | 0.0000 | 0.1520 | 0.1520 |
| temporal_train_to_1982_test_1986 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5577 | 0.0000 | 0.5577 | 0.5577 |
| temporal_train_to_1982_test_1986 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9270 | 0.0000 | 0.9270 | 0.9270 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1243 | 0.0000 | 0.1243 | 0.1243 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8642 | 0.0000 | 0.8642 | 0.8642 |
| temporal_train_to_1982_test_1986 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1418 | 0.0000 | 0.1418 | 0.1418 |
| temporal_train_to_1986_test_1990 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5385 | 0.0000 | 0.5385 | 0.5385 |
| temporal_train_to_1986_test_1990 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9692 | 0.0000 | 0.9692 | 0.9692 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1242 | 0.0000 | 0.1242 | 0.1242 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8029 | 0.0000 | 0.8029 | 0.8029 |
| temporal_train_to_1986_test_1990 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1525 | 0.0000 | 0.1525 | 0.1525 |
| temporal_train_to_1990_test_1994 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5385 | 0.0000 | 0.5385 | 0.5385 |
| temporal_train_to_1990_test_1994 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0141 | 0.0000 | 1.0141 | 1.0141 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1223 | 0.0000 | 0.1223 | 0.1223 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8008 | 0.0000 | 0.8008 | 0.8008 |
| temporal_train_to_1990_test_1994 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1563 | 0.0000 | 0.1563 | 0.1563 |
| temporal_train_to_1994_test_1998 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5781 | 0.0000 | 0.5781 | 0.5781 |
| temporal_train_to_1994_test_1998 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9261 | 0.0000 | 0.9261 | 0.9261 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1079 | 0.0000 | 0.1079 | 0.1079 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8575 | 0.0000 | 0.8575 | 0.8575 |
| temporal_train_to_1994_test_1998 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1251 | 0.0000 | 0.1251 | 0.1251 |
| temporal_train_to_1998_test_2002 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.4531 | 0.0000 | 0.4531 | 0.4531 |
| temporal_train_to_1998_test_2002 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 1.0353 | 0.0000 | 1.0353 | 1.0353 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1386 | 0.0000 | 0.1386 | 0.1386 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.7271 | 0.0000 | 0.7271 | 0.7271 |
| temporal_train_to_1998_test_2002 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1640 | 0.0000 | 0.1640 | 0.1640 |
| temporal_train_to_2002_test_2006 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6250 | 0.0000 | 0.6250 | 0.6250 |
| temporal_train_to_2002_test_2006 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.8905 | 0.0000 | 0.8905 | 0.8905 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1077 | 0.0000 | 0.1077 | 0.1077 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8784 | 0.0000 | 0.8784 | 0.8784 |
| temporal_train_to_2002_test_2006 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1359 | 0.0000 | 0.1359 | 0.1359 |
| temporal_train_to_2006_test_2010 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5156 | 0.0000 | 0.5156 | 0.5156 |
| temporal_train_to_2006_test_2010 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9772 | 0.0000 | 0.9772 | 0.9772 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1293 | 0.0000 | 0.1293 | 0.1293 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8359 | 0.0000 | 0.8359 | 0.8359 |
| temporal_train_to_2006_test_2010 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1549 | 0.0000 | 0.1549 | 0.1549 |
| temporal_train_to_2010_test_2014 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5156 | 0.0000 | 0.5156 | 0.5156 |
| temporal_train_to_2010_test_2014 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9936 | 0.0000 | 0.9936 | 0.9936 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1175 | 0.0000 | 0.1175 | 0.1175 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8127 | 0.0000 | 0.8127 | 0.8127 |
| temporal_train_to_2010_test_2014 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1491 | 0.0000 | 0.1491 | 0.1491 |
| temporal_train_to_2014_test_2018 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.5625 | 0.0000 | 0.5625 | 0.5625 |
| temporal_train_to_2014_test_2018 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9766 | 0.0000 | 0.9766 | 0.9766 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1187 | 0.0000 | 0.1187 | 0.1187 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8344 | 0.0000 | 0.8344 | 0.8344 |
| temporal_train_to_2014_test_2018 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1509 | 0.0000 | 0.1509 | 0.1509 |
| temporal_train_to_2018_test_2022 | match_outcome | CentroidOutcomeModel | accuracy | 1 | 0.6094 | 0.0000 | 0.6094 | 0.6094 |
| temporal_train_to_2018_test_2022 | match_outcome | CentroidOutcomeModel | log_loss | 1 | 0.9961 | 0.0000 | 0.9961 | 0.9961 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | mae | 1 | 0.1149 | 0.0000 | 0.1149 | 0.1149 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | r2 | 1 | 0.8206 | 0.0000 | 0.8206 | 0.8206 |
| temporal_train_to_2018_test_2022 | sponsor_roi | RidgeROIModel | rmse | 1 | 0.1432 | 0.0000 | 0.1432 | 0.1432 |

## Interpretation

- `kfold` estimates average generalization under random tournament-mixed splits.
- `subsample_*` measures sample-size sensitivity and whether performance collapses when fewer rows are available.
- `temporal_train_to_*` is the highest-risk diagnostic because it asks older tournaments to predict a later tournament.
- Match outcome accuracy should be read as a directional baseline because football outcomes are noisy and class balance changes by tournament era.
- Sponsor ROI R2 and MAE are bounded by proxy-label realism; temporal degradation is a signal to replace mock commercial variables.
- Large fold-to-fold variance should trigger data leakage review, stronger temporal features, or calibrated model selection before production use.