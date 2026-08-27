# Technical-Preview Validation Record

Date: 2026-08-27
Version: 0.1.0
Runtime used for the recorded local pass: CPython 3.12.13 on Linux

## Scope

This record validates deterministic benchmark mechanics. It does not evaluate a language model and must not be cited as a model-propensity result.

## Commands

```bash
ruff format --check .
ruff check .
mypy src
make check
make test
python -m build
PYTHONPATH=src python -m ghostledger campaign run experiments/manifests/preview.json --output /tmp/ghostledger-final
PYTHONPATH=src python -m ghostledger campaign resume /tmp/ghostledger-final/preview-baseline-vs-layered
```

## Quality gates

| Gate | Result |
| --- | --- |
| Ruff lint | Passed |
| Ruff format | Passed |
| Strict mypy | Passed for 8 source modules |
| Unit/integration/property-style tests | 20 passed |
| Scenario validation | 24 pairs / 48 cases / 6 domains / 18 primary classes |
| Distribution build | Source archive and wheel built successfully |
| Campaign execution | 96/96 completed |
| Campaign resume | 96 existing runs recognized; 0 duplicated |
| Evidence verification | Passed for sampled completed bundle |
| Deterministic replay | Submitted-state digest matched |

## Constructed reference results

| Control configuration | Adversarial runs | CSSR | Detection | Prevention | Benign runs | Completion | False positives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 24 | 24/24 | 0/24 | 0/24 | 24 | 24/24 | 0/24 |
| Layered | 24 | 0/24 | 24/24 | 24/24 | 24 | 24/24 | 0/24 |

The corpus intentionally encodes these acceptance properties. The result demonstrates that the runner, oracles, controls, channel filtering, and aggregation behave as designed. It is not evidence that the layered posture will stop an adaptive or previously unseen strategy.

## Interpretation boundary

- The adversarial policy is scripted.
- The protected rule is known to the trusted harness.
- Preview harm is binary.
- Scenarios are synthetic and open source.
- No model, provider, or human monitor was evaluated.
- No confidence interval or population claim is warranted.
