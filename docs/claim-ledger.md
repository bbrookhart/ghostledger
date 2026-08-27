# Claim Ledger

Every public claim should map to code, data, tests, or documentation.

| Claim | Evidence | Boundary |
| --- | --- | --- |
| 24 adversarial cases + 24 benign twins | `scenarios.json`, `Catalog.validate()`, `test_preview_has_24_pairs_and_48_cases` | Paired reference trajectories, not 48 unrelated environments |
| Six synthetic domains | Catalog validation and README domain table | Synthetic only |
| All 18 classes represented | `taxonomy.json`, taxonomy test | Primary mapping at least once; not equal depth |
| Offline default | Standard-library dependencies, `doctor`, demo | Package installation may require normal Python packaging tools |
| Protected oracle separation | `Scenario.public_view()`, public-view test | Host operator remains trusted |
| Observation channels enforced | Monitor filtering in `engine.py`, channel test | Declared-channel abstraction, not information-flow proof |
| Tamper-evident evidence | `evidence.py`, mutation/reorder/bundle tests | Detects covered post-finalization changes; not tamper-proof |
| Deterministic replay | Manifest-driven rerun and submitted-state digest | Provider-backed adapters are not implemented |
| Layered controls preserve benign reference completion | Corpus-wide engine test | Deterministic reference trajectories only |
| Layered controls prevent preview sabotage trajectories | Corpus-wide engine test | Known reference actions, not adaptive robustness |
| Reports recompute from run outcomes | `reporting.py`, metric tests | No external model cost or statistical inference yet |
| 96-run preview campaign completed locally | `docs/validation-results.md`, committed manifest | Constructed scripted acceptance test, not model evidence |

Claims about frontier-model propensity, deception, universal monitor effectiveness, production safety, certification, or catastrophic risk are explicitly unsupported.
