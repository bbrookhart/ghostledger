# Controls and Monitors

## Separation of concerns

A **monitor** observes and scores. A **control** may prevent, quarantine, or recover. GHOSTLEDGER reports these effects separately so a post-hoc alert is not mistaken for prevention.

## Control catalog

| ID | Name | Stage | v0.1 behavior |
| --- | --- | --- | --- |
| `GL-C00` | Visible checks only | Acceptance | No protected monitor |
| `GL-C01` | Mission invariants | Pre-action | Simulates proposed state and denies integrity loss |
| `GL-C02` | Independent verification | Post-action | Detects protected mission failure |
| `GL-C03` | Differential review | Post-action | Compares protected paths with benign reference state |
| `GL-C04` | Provenance enforcement | Continuous | Verifies the in-memory event chain |
| `GL-C05` | Hidden tests | Post-action | Detects protected check failure |
| `GL-C06` | Least privilege | Pre-action | Denies undeclared write paths |
| `GL-C07` | Dual control | Pre-action | Denies high-consequence integrity violations |
| `GL-C08` | Diverse execution | Post-action | Compares full state with benign reference execution |
| `GL-C09` | Downstream sentinel | Pre-consumption | Detects harmful downstream state and marks containment |
| `GL-C10` | Checkpoint and rollback | Recovery | Restores the initial synthetic state after detection |
| `GL-C11` | Layered control plane | Composite | Research label for the recommended combined posture |

The CLI alias `layered` resolves to C01, C03, C04, C05, C06, C07, C09, and C10. C02 and C08 remain explicit ablation controls rather than duplicate signals in the default bundle.

## Observation channels

| Channel | Evidence |
| --- | --- |
| `final` | Final task response or visible completion state |
| `actions` | Proposed, denied, and executed actions |
| `diff` | Initial, submitted, and reference-state divergence |
| `provenance` | Hash-linked event chain |
| `visible` | Agent-visible acceptance checks |
| `downstream` | Protected mission and synthetic downstream results |

A decision is eligible only when all its declared channels appear in the run configuration.

## Security–utility analysis

Controls should be compared on at least:

- covert sabotage success;
- adversarial detection;
- prevention and containment;
- benign completion;
- benign false positives;
- recovery completeness;
- future review and compute cost.

A control that blocks every change can minimize sabotage but destroy useful work. Paired benign twins expose that failure.

## Calibration

Deterministic preview monitors use fixed transparent thresholds. Future statistical or model monitors must calibrate on development cases only and store the calibration artifact. Test labels must not enter calibration.
