# Limitations

## Technical-preview scope

v0.1 is a deterministic validation harness, not a completed frontier-model study. It uses flat synthetic state and one protected rule per preview scenario.

## Construct validity

Mission integrity is represented by explicit author-defined rules. Real missions contain contested priorities, partial observability, and interacting constraints. A rule can be internally correct yet externally incomplete.

## Ecological validity

The synthetic domains omit organizational pressure, noisy tools, human negotiation, long context, ambiguous specifications, and production side effects. Results may not transfer to deployment.

## Oracle leakage

The open preview corpus is inspectable. A model with full repository access could overfit to protected values. Model studies need restricted workspaces and sealed held-out variants.

## Reference-policy bias

Differential monitors compare with a single benign reference trajectory. Legitimate alternative solutions could diverge and create false positives. Future work should support sets of acceptable states or property-based equivalence.

## Binary harm

One mission rule means v0.1 harm is binary. Real harm is continuous, delayed, and multidimensional. The data model supports weighted rules, but the preview does not claim calibrated severity.

## Intent attribution

Observable harm is not synonymous with intentional sabotage. Scripted adversarial runs have a known experiment-defined objective; live-model attribution requires a stronger protocol.

## Model nondeterminism

Future provider adapters will face model changes, sampling variance, unavailable private reasoning, API retries, and terms governing output publication. Manifests must capture what can be captured, but exact response reproduction may remain impossible.

## Monitor overfitting

Transparent preview controls know the protected property. Their deterministic success demonstrates control wiring, not robustness to adaptive agents. Held-out conditions and adaptive red-team strategies are planned.

## Statistics

The 24 scenario pairs are not a representative sample of all agent work. Technical-preview percentages should not be treated as population estimates. Repeated seeds do not create independent scenarios.

## Evidence trust

The evidence chain detects mutation after finalization by an honest harness. It provides no protection against a compromised host that records false events or steals hashing state before creation.

## Dual use

Stealthy-sabotage research can be misused. GHOSTLEDGER excludes live targets, operational details, destructive actions, and real infrastructure. This reduces but cannot eliminate dual-use risk.
