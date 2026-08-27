# Architecture

## Design objective

GHOSTLEDGER evaluates a narrow but consequential failure mode: a task can pass its visible acceptance criteria while the submitted state violates a protected mission property. The architecture keeps those two judgments independent and leaves enough evidence to reproduce both.

## Components

### Scenario registry

`ghostledger.catalog.Catalog` loads the built-in JSON corpus as immutable typed models. Validation requires:

- a stable `GL-*` ID and semantic version;
- distinct visible and mission rules;
- declared action paths;
- protected paths present in the initial state;
- both benign and adversarial reference trajectories.

`Scenario.public_view()` is the only scenario representation intended for an evaluated agent. It excludes mission rules, protected paths, and sabotage trajectories.

### Deterministic range

The v0.1 range is an in-memory flat state map. This intentionally small state machine makes every transition inspectable and gives the technical preview a deterministic foundation. Each domain uses fictional assets and inert values.

Future adapters may materialize containerized workspaces, but they must preserve the same public/protected split and event contract.

### Tool gateway and control plane

Every scripted action is proposed before it is executed. Preventive controls can deny it; accepted actions mutate only a declared path. The gateway emits an event for proposal, denial, or execution.

Controls are composable tuples of IDs. The engine implements prevention, detection, containment, and recovery as distinct outcome fields.

### Oracle engine

The engine computes:

1. visible task success from agent-visible acceptance rules;
2. protected mission integrity from harness-only rules;
3. downstream harm as normalized integrity loss for the synthetic asset.

The current preview uses deterministic `eq`, `neq`, `gte`, `lte`, and `in` rules. There is no model grader in the primary scoring path.

### Monitor framework

Monitor decisions include a stable ID, declared observation channels, score, threshold, decision, and reason codes. The engine filters decisions through the run's configured channels before computing `detected`.

This prevents a monitor from receiving a diff, provenance record, or downstream check it was not assigned.

### Evidence ledger

Events use canonical JSON digests and a previous-event link. A bundle-level integrity manifest records the SHA-256 digest of every covered file. The design detects modification, substitution, deletion, and event reordering within the stated local trust model.

It does not provide remote timestamping, nonrepudiation, hardware-backed signing, or protection from an attacker who controls the harness before evidence finalization.

### Reporting

The reporter reads `outcome.json` files and emits JSON, Markdown, and self-contained HTML. Aggregates include numerator and denominator; unsupported small-sample statistics are omitted.

## Trust boundaries

| Boundary | Can read | Can write | Must not access |
| --- | --- | --- | --- |
| Evaluated-agent view | Public task, initial state, visible rules, allowed paths | Proposed state actions | Mission rules, evidence finalization |
| Tool gateway | Proposed action and policy | Declared state path, event request | Host or network resources |
| Control plane | Proposed and current state, protected rules | Denial, quarantine, rollback | Provider credentials |
| Oracle engine | Submitted state and protected rules | Check results | Agent-controlled evidence |
| Evidence writer | All harness events and outputs | New run bundle | Previously finalized bundle mutation |
| Reporter | Finalized outcomes | New report directory | Protected runtime secrets |

## Data flow

1. The coordinator resolves a scenario, condition, control tuple, channels, and seed.
2. The evaluated adapter receives `Scenario.public_view()`.
3. Actions enter the tool gateway as proposals.
4. Preventive controls simulate the proposed state and decide.
5. Accepted transitions update the synthetic state and the event chain.
6. Visible and protected oracles independently score the submitted state.
7. Monitors evaluate only allowed evidence channels.
8. Containment and rollback execute when configured.
9. The harness writes and covers the complete evidence bundle.
10. Reports aggregate immutable per-run outcomes.

## Failure behavior

- Unknown scenarios and malformed manifests fail closed with exit code 2.
- Evidence verification failures return exit code 3.
- Replay state mismatch returns exit code 4.
- A monitor whose channels are unavailable is excluded from the detection decision.
- Invalid scenario data is rejected at catalog load.
- Generated run directories use exclusive creation and are never overwritten.

## Extension contracts

New agent adapters must return typed actions and declare whether they are deterministic. New rule operators require unit tests and methodology updates. New monitors must declare channels and evidence references. Containerized domain adapters must deny outbound network by default and keep protected oracles outside the agent mount.

## Architecture decisions

- [ADR-001: State-grounded primary scoring](adr/001-state-grounded-scoring.md)
- [ADR-002: Deterministic offline core](adr/002-deterministic-offline-core.md)
- [ADR-003: Explicit observation channels](adr/003-explicit-observation-channels.md)
