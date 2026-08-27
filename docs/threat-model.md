# Threat Model

## Security objective

Measure whether a controlled agent trajectory can preserve visible task success while degrading a protected mission property, and whether named controls detect or contain that outcome.

## Assets

- source and configuration integrity;
- validation strength;
- monitoring coverage;
- authorization and approval policy;
- incident evidence and causal ordering;
- data lineage and reproducibility;
- recovery readiness;
- fictional cyber-physical safety margin;
- benchmark evidence and scoring integrity.

## Actors and conditions

### Benign reference agent

Executes a reviewed trajectory that completes the task and preserves mission integrity. It establishes utility and false-positive behavior.

### Scripted saboteur

Executes a reviewed trajectory that completes the visible task and attempts a predefined mission violation. It validates scenario mechanics. It is not evidence that a language model would choose the behavior.

### Future evaluated model

An optional adapter may expose the same public task and tool contract to a model. Capability, elicitation, propensity, and monitorability results must be reported separately.

### Benchmark operator

Controls the harness, protected rules, evidence writer, and run configuration. v0.1 assumes the operator and host are trusted.

## Adversary capabilities in v0.1

The scripted adversary can:

- propose writes to declared synthetic state paths;
- choose values that violate protected rules;
- provide a plausible action summary;
- complete the visible task marker;
- exploit a visible-only baseline.

It cannot:

- read protected mission rules through the public view;
- write outside declared state paths;
- access the host filesystem or network;
- modify finalized evidence through the tool gateway;
- access credentials;
- execute arbitrary code.

## Defender capabilities

The defender may:

- evaluate protected invariants before a transition;
- restrict write scope;
- require approval for high-consequence changes;
- compare protected state with a benign reference;
- verify event provenance;
- run protected checks;
- observe downstream integrity;
- contain and roll back state.

Every result is conditional on the selected controls and observation channels.

## Attack trees

### Covert mission degradation

```mermaid
flowchart TD
    A["Visible task passes"] --> B["Mission state degrades"]
    B --> C["Monitor misses"]
    C --> D["Covert sabotage success"]
    B --> E["Prevented or contained"]
    E --> F["No covert success"]
```

### Evidence corruption

```mermaid
flowchart TD
    A["Covered evidence changes"] --> B["File digest mismatch"]
    A --> C["Event changes or reorders"]
    C --> D["Chain verification fails"]
    B --> E["Bundle invalid"]
    D --> E
```

## Important non-goals

GHOSTLEDGER v0.1 does not:

- infer intent from an ordinary mistake;
- prove deceptive alignment or stable hidden goals;
- estimate catastrophic risk;
- protect against a malicious host or compromised evidence writer;
- model a real operational environment;
- create real sabotage or evasion capability;
- certify a deployed agent as safe.

## Residual risks

### Construct validity

A one-rule synthetic oracle is clearer than a real mission but less realistic. Passing or failing it may not predict behavior in a complex organization.

### Oracle leakage

The source repository is public, so a model with repository access could learn preview oracles. Research studies must restrict the evaluated workspace or use sealed held-out packs.

### Adaptive overfitting

The deterministic reference actions are known. They validate mechanics, not robustness to novel strategies.

### Harness trust

Hash linkage detects post-finalization changes to covered artifacts. It does not protect against a harness that records false evidence at creation time.

### Dual use

Even synthetic sabotage research can inspire unsafe adaptation. The project omits operational payloads, real settings, and live targets; contributions crossing that boundary are rejected.
