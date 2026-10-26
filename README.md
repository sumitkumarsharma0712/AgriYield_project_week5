# AgriYield — Predictive Modelling Framework for Agribusiness

A reproducible, scenario-agnostic machine-learning framework for forecasting agricultural
yields and other agribusiness performance metrics. Built for the Week 4 task
*"Predictive Modeling Framework"* (Junior Data Scientist Internship, Nagpur).

**Author:** Sumit Kumar Sharma

## What it does
`data → feature engineering (lags, domain indices) → chronological split → time-aware tuning →
model comparison vs. naive baselines → ensemble → conformal uncertainty → explainability →
ablation → robustness (unseen districts, drift) → saved model + figures + CSV reports`

| Layer | Module | Highlights |
|---|---|---|
| Config | `config.py` | A `Scenario` object declares target, time, entity and feature groups. |
| Data | `data_generator.py` | Agronomy-driven simulators for crop yield and dairy milk; `load_data` accepts real CSVs. |
| Features | `features.py` | Leak-free lags/rolling stats, heat-stress, water-supply, THI, seasonality … |
| Models | `models.py` | Ridge, Random Forest, Extra Trees, Gradient Boosting; forward-chaining CV; randomized search. |
| Evaluation | `evaluate.py` | RMSE/MAE/MAPE/sMAPE/R²/bias, skill score, conformal intervals, PSI drift. |
| Orchestration | `pipeline.py` | Runs everything, writes `outputs/<scenario>/`. |

## Quick start
```bash
pip install -r requirements.txt
python run_pipeline.py --scenario crop_yield          # ~3–5 min
python run_pipeline.py --scenario dairy_milk          # same framework, new problem
python run_pipeline.py --scenario all --n-iter 12     # reproduces the report
python run_pipeline.py --scenario crop_yield --data my_real_data.csv   # your own data
pytest -q                                             # unit tests
```

## Using it for a new agribusiness problem
1. Add a `Scenario(...)` in `config.py` (target, time column, entity columns, feature groups).
2. Add a small `*_domain_features` function in `features.py` (optional but valuable).
3. Provide a CSV with those columns and run `run_pipeline.py --scenario <name> --data file.csv`.

Everything else — splitting, tuning, baselines, intervals, explainability, drift — is reused unchanged.

## Outputs (`outputs/<scenario>/`)
`summary.json`, `model_comparison.csv`, `test_predictions.csv`, `permutation_importance.csv`,
`ablation.csv`, `drift_psi.csv`, `metrics_by_*.csv`, `cv_fold_rmse.csv`, `champion_model.joblib`, `figures/*.png`.

## Important note on data
The included datasets are **simulated** with documented agronomic relationships (water-use response,
heat stress at flowering, diminishing returns to nitrogen, pest damage, technology trend, drought/flood
years). They demonstrate the framework end to end; accuracy numbers therefore reflect the simulator and must
be re-established on real district/farm data (e.g. Agricoop/DES crop statistics, IMD rainfall, Soil Health
Card, Sentinel-2 NDVI). The code has no dependence on the simulator beyond the column schema.

## Design principles
* **No leakage** – lags use strictly earlier periods; the test years are untouched until final scoring.
* **Time-aware validation** – expanding-window folds; model chosen on CV, not on test.
* **Honest baselines** – every model is reported as skill versus a naive forecast.
* **Uncertainty** – 90 % split-conformal intervals with measured coverage.
* **Explainability & robustness** – permutation importance, feature-group ablation, leave-district-out CV, PSI drift.

---
# Week 5 — Model Evaluation and Reporting (`agrieval`)

`src/agrieval/` turns a trained model's test predictions into stakeholder-ready evidence.

| Module | Purpose |
|---|---|
| `config.py` | Evaluation policy: tolerance band, shortfall definition, cost weights, traffic-light thresholds |
| `metrics.py` | RMSE/MAE/MAPE/WAPE/R², bias, MASE, calibration, within-tolerance, asymmetric business cost, shortfall precision/recall, interval score, cluster-bootstrap CIs, paired bootstrap test |
| `scorecard.py` | Traffic-light report card and auto-written plain-language executive summary |
| `visuals.py` | 10 non-expert charts (one message per chart, colour + text labels) |
| `run_evaluation.py` | Orchestrator → `outputs/evaluation/<scenario>/` |

```bash
python run_pipeline.py --scenario all --n-iter 12      # train (Week 4)
python src/agrieval/run_evaluation.py                  # evaluate and report (Week 5)
python -m unittest discover -s tests                   # 17 tests
```
Outputs per scenario: `executive_summary.md`, `evaluation_summary.json`, `metrics_*.csv`, `figures/01…10_*.png`.
Any model's predictions (columns `y_pred`, `lo`, `hi` + entity/time keys) can be evaluated the same way.
