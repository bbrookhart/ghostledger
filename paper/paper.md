# The Task Passed, the Mission Failed

## Benchmarking Stealthy Sabotage in Long-Horizon AI Agents

Brian Brookhart
Technical preview, version 0.1.0 — 2026-08-27

## Abstract

Agent benchmarks commonly score whether a task was completed. In security-sensitive deployments, completion is insufficient: an agent may satisfy visible acceptance criteria while degrading a downstream security, safety, reliability, or auditability property. We introduce GHOSTLEDGER, an open-source technical preview for state-grounded evaluation of this gap. The benchmark separates visible acceptance, protected mission-integrity, and downstream-effect oracles; records policy-mediated actions in a tamper-evident evidence bundle; and evaluates prevention, detection, containment, recovery, benign utility, and false positives. The preview contains 24 adversarial scenarios and 24 matched benign twins across six fictional domains, covering an 18-class sabotage taxonomy. Deterministic reference agents validate benchmark mechanics offline. We make no claim about frontier-model sabotage propensity in this release. GHOSTLEDGER is intended as a reproducible foundation for preregistered agent-control studies using sealed scenarios and optional model adapters.

## 1. Introduction

Tool-using AI agents increasingly operate over code, policy, data, incident records, and simulated control systems. Their evaluation often collapses a long trajectory into a final answer or visible task score. That compression creates a security blind spot: the work product can pass ordinary checks while a subtle state change degrades the mission.

We call the successful combination of visible task completion, protected mission harm, and monitor evasion **covert sabotage success**. The term describes an experimental outcome, not a psychological judgment about the agent.

GHOSTLEDGER is built around three separations:

1. visible task success versus protected mission integrity;
2. detection versus prevention, containment, and recovery;
3. deterministic harness validation versus empirical model findings.

The technical preview contributes a paired synthetic corpus, explicit observation-channel model, composable control plane, reproducible metrics, and tamper-evident evidence format.

## 2. Related work

SHADE-Arena frames sabotage and monitoring as coupled evaluations in complex agent environments. OpenAI and Apollo Research have studied controlled scheming evaluations and mitigations, while work on reasoning-model monitoring emphasizes the value and fragility of observation channels. METR publishes capability and risk evaluations with explicit threat-model assumptions. Inspect AI provides composable agent, tool, scorer, logging, and sandbox abstractions. Microsoft PyRIT provides an extensible red-team framework, and MITRE ATLAS provides structured adversarial AI knowledge.

GHOSTLEDGER does not reproduce these systems or their results. It focuses narrowly on state-grounded task-pass/mission-fail separation with matched benign controls and a portable evidence contract.

## 3. Threat model

The evaluated adapter can propose changes to declared paths in a fictional local state. Protected mission rules and finalized evidence remain in a trusted harness boundary. The adversarial condition receives an experiment-defined trajectory that violates one protected property while completing the visible task. The defender may apply invariant checks, least privilege, approvals, differential verification, provenance, downstream sentinels, and rollback.

The preview excludes arbitrary code execution, outbound networking, credentials, real targets, destructive payloads, and real operational technology parameters.

## 4. Benchmark design

### 4.1 Paired cases

Each of 24 scenario definitions yields a benign case and an adversarial case. The pair shares domain, task, initial state, visible rule, allowed paths, and protected property. This permits joint analysis of sabotage resistance and utility cost.

### 4.2 Domains

The corpus covers software maintenance, detection engineering, identity policy, incident investigation, data and research integrity, and cyber-physical resilience. All assets are fictional. Cyber-physical values are dimensionless and intentionally non-operational.

### 4.3 Taxonomy

Eighteen primary classes range from latent defects and validation weakening to evidence manipulation, delayed triggers, collusion, evaluator gaming, safety-margin erosion, and reproducibility corruption. Classes describe observable patterns and do not establish intent.

## 5. Evaluation protocol

A run resolves the scenario, condition, controls, channels, and seed. The agent receives a public scenario view. Actions are proposed through the control plane, then denied or executed. Visible and protected rules independently score the submitted state. Monitor decisions are filtered by available observation channels. Optional containment and rollback act after detection. The harness writes the complete evidence bundle and integrity map.

The preview manifest crosses all 24 pairs with two conditions and two control configurations, producing 96 deterministic validation runs.

## 6. Metrics

Let \(V_i\) be visible success, \(M_i\) mission integrity, \(H_i=1-M_i\) harm, and \(D_i\) detection.

\[
CSSR = \frac{1}{N_A}\sum_i \mathbf{1}[V_i=1 \land H_i>0 \land D_i=0]
\]

We also report sabotage success, adversarial detection, benign completion, benign false positives, prevention, containment, and recovery. Every rate includes its numerator and denominator.

## 7. Technical-preview validation

Automated corpus-wide tests establish four intended properties for every scenario pair:

- the benign reference passes visible and mission checks under the baseline;
- the adversarial reference passes the visible check and violates the mission check under the baseline;
- layered controls preserve benign reference completion;
- layered controls prevent the known adversarial mission violation.

Additional tests detect event mutation, event reordering, and covered-file modification; enforce the public/protected scenario split; validate observation-channel filtering; and verify metric logic.

These results validate implementation mechanics. They must not be interpreted as evidence about a frontier model's capability, propensity, or alignment.

## 8. Limitations

The preview uses flat state, binary harm, open oracles, transparent controls, and deterministic reference trajectories. It lacks realistic tool noise, long contexts, diverse benign solutions, adaptive adversaries, human review, model costs, and powered statistical comparisons. Its evidence model trusts the host at creation time.

## 9. Ethics and safety

The benchmark is defensive and sandbox-only. Scenarios exclude malware, credentials, real targets, operational evasion, and real infrastructure parameters. Research users should publish false positives, invalid runs, configuration, uncertainty, and claim boundaries.

## 10. Reproducibility

The runtime core uses the Python standard library. Scenario data, taxonomy, controls, scorer logic, manifests, and schemas are versioned. Runs contain state snapshots, checks, monitor decisions, outcomes, hash-linked events, and a covered-file integrity manifest. Deterministic replay compares submitted-state digests.

## 11. Planned research release

Future work will add sealed held-out variants, containerized workspaces, acceptable-state sets, continuous harm models, provider-neutral model adapters, adaptive monitoring studies, human-review cost measurement, and preregistered scenario-level statistical analysis.

## References

Primary-source links and dated design notes are maintained in [`docs/research/source-notes.md`](../docs/research/source-notes.md).
