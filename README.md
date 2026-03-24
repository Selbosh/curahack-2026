# curAHack 2026 Challenge 5: Microbiome-Based CVD Prediction

**Challenge leads**: Kevin Iselborn and Yuichiro Iwashita

**Team members**:

- [Gerrit Großmann](https://github.com/gerritgr)
- [David Selby](https://github.com/Selbosh)
- [Kevin D Goveas](https://github.com/kxviel)
- [Amir Hussein Mahdavieh](https://github.com/amirmahdavieh)
- [Golbahar Abbasihormozi](https://github.com/abbasigolbahar)
- [Baris Akdogan](https://github.com/bbakdoga)

## Overview

This repository explores microbiome-based health classification on AGP and GGMP cohorts, starting from the Gut Age Index (GAI) pipeline in Bao et al. (2024) and extending it with direct classification experiments.

We now maintain two complementary baselines:

- A paper-comparable GAI view (for historical comparability).
- A strict nested-CV GAI view (for leakage-safe generalization estimates).

## Analyses

### What We Did

- Implemented and ran a direct classification workflow in [direct-classification.ipynb](direct-classification.ipynb):
	- Compared raw vs CLR-transformed OTU features.
	- Tested with/without age covariate.
	- Evaluated LightGBM, Random Forest, and MLP with stratified CV.
	- Added timing capture per model and per feature ablation.
	- Added hyperparameter tuning for tree-based models and compared tuned vs default performance.

- Reproduced and clarified the GAI baseline in [gai-baseline.ipynb](gai-baseline.ipynb):
	- Built a fast non-PyCaret baseline around the top 3 regressors from [compare_models.tsv](compare_models.tsv).
	- Included both age-fix and non-age-fix variants.
	- Applied logistic regression on corrected GAI for binary classification (as in [binary_classifier.ipynb](binary_classifier.ipynb)).
	- Added side-by-side reporting of paper-comparable vs strict nested-CV evaluation.

- Preserved the original paper pipeline script in [gai_cal.py](gai_cal.py) and original outputs in [my_output/AGP](my_output/AGP), [my_output/AGP-agefix](my_output/AGP-agefix), [my_output/GGMP](my_output/GGMP), and [my_output/GGMP-agefix](my_output/GGMP-agefix).

### Current Best Observed Metrics

The table below summarizes our latest notebook runs and the best observed values per dataset under each evaluation view.

| Evaluation view | Dataset | Best observed setup | Balanced Accuracy | AUC-ROC | Source |
|---|---|---|---:|---:|---|
| Paper-comparable | AGP | PyCaret CatBoost + corrected GAI logistic | 0.658 +/- 0.013 | 0.621 +/- 0.023 | [gai-baseline.ipynb](gai-baseline.ipynb), Section 9 |
| Paper-comparable | GGMP | PyCaret CatBoost + corrected GAI logistic | 0.731 +/- 0.007 | 0.686 +/- 0.012 | [gai-baseline.ipynb](gai-baseline.ipynb), Section 9 |
| Strict nested-CV | AGP | Random Forest (no age-fix) + corrected GAI logistic | 0.598 +/- 0.020 | 0.607 +/- 0.028 | [gai-baseline.ipynb](gai-baseline.ipynb), Section 6 |
| Strict nested-CV | GGMP | CatBoost/Random Forest (no age-fix) + corrected GAI logistic | 0.612 +/- 0.009 | 0.643 +/- 0.011 | [gai-baseline.ipynb](gai-baseline.ipynb), Section 6 |

Notes:

- Use strict nested-CV numbers as the primary benchmark for model selection and improvement claims.
- Use paper-comparable numbers as historical context and reproducibility checks.

### What We Have Not Done Yet

- Added richer demographic covariates (for example sex, smoking, education) into the direct-classification feature sets.
- Run a full, finalized cross-cohort transfer evaluation (train on AGP and test on GGMP, and vice versa) under one consistent protocol.

### Future extensions

- Exploiting taxonomy and prior knowledge about microbiome in the modelling process, for example for grouped feature selection or a graph-based architecture on ontology
- Tabular foundation models, such as TabPFN (depending on computational feasibility) or world models like TabuLa-8B that may be able to reason over semantic microbiome relationships

### Practical Reading Order

1. [gai-baseline.ipynb](gai-baseline.ipynb) for GAI baselines and evaluation caveats.
2. [direct-classification.ipynb](direct-classification.ipynb) for direct OTU-based classifiers and ablations.
3. [binary_classifier.ipynb](binary_classifier.ipynb) for the corrected-GAI logistic classification framing.

## Citation

Bao, Z., Yang, Z., Sun, R. _et al._ Predicting host health status through an integrated machine learning framework: insights from healthy gut microbiome aging trajectory. _Sci Rep_ **14**, 31143 (2024). <https://doi.org/10.1038/s41598-024-82418-3>
