# Configs Guide

This folder contains configuration files for reproducible scripts.

## Baseline Configs

- [rf_experiments.yaml](rf_experiments.yaml) defines baseline Random Forest
  experiment settings.
- [final_rf.yaml](final_rf.yaml) defines the baseline final evaluation setup.

## Prototype Benchmark Config

- [model_benchmark_prototype.yaml](model_benchmark_prototype.yaml) defines the
  six-model prototype benchmark, including cost-sensitive, class-weighted, and
  training-only resampling candidates.

## Threshold / Cost Config

- [cost_scenarios_prototype.yaml](cost_scenarios_prototype.yaml) defines
  illustrative false-negative and false-positive cost scenarios.

## Explainability Config

- [explainability_prototype.yaml](explainability_prototype.yaml) defines focus
  models, permutation importance settings, stability seeds, and output paths.

The configs support reproducible portfolio artifacts. They do not define a
production decision rule.
