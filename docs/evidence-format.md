# Evidence Format

## Purpose

Every conclusion should be traceable from an aggregate metric to a run outcome, check, state snapshot, and ordered action record.

## Bundle layout

```text
glrun_.../
├── manifest.json
├── events.jsonl
├── snapshots/
│   ├── initial.json
│   ├── submitted.json
│   └── final.json
├── checks/results.json
├── monitors/decisions.json
├── outcome.json
└── integrity.json
```

## Manifest

The manifest records benchmark and taxonomy version, scenario reference, public task view, condition, scripted adapter identity, controls, observation channels, seed, offline status, and the mandatory claim boundary.

Protected mission rules are intentionally absent from `scenario_public_view`.

## Event stream

Each JSONL event records:

- schema and run identity;
- sequence and deterministic logical time;
- actor and action;
- resource;
- digests of request and response payloads;
- decision and policy reason codes;
- previous-event and event digests.

The current implementation hashes canonical JSON with SHA-256. It stores payload digests in the event stream while the resulting state is represented in snapshots and checks.

## Snapshots

- `initial.json`: state before any evaluated action;
- `submitted.json`: state used for visible and protected scoring;
- `final.json`: state after optional recovery.

This distinction prevents rollback from erasing evidence that a harmful submitted state existed.

## Checks

`checks/results.json` contains visible, mission, downstream, and diff sections. Each rule result includes label, path, operator, expected value, actual value, weight, and pass/fail outcome.

## Monitor decisions

A decision includes monitor ID, channels, score, threshold, binary decision, reason codes, and optional evidence-sequence references. The run outcome considers only decisions whose required channels are available.

## Outcome

`outcome.json` is the stable per-run metric input. It records visible success, mission integrity, harm, detection, prevention, containment, recovery, submitted and final state digests, and the final event-chain root.

## Integrity manifest

`integrity.json` lists the digest of every other evidence file and a digest over the canonical file map. It is written last.

This design is tamper-evident under the local trust model. It does not establish who created a bundle, when a remote observer saw it, or whether the harness was honest at creation.

## Verification

```bash
ghostledger evidence verify runs/glrun_...
```

Verification checks:

- integrity-map root;
- existence and digest of each covered file;
- event sequence;
- previous-event links;
- event digests.

## Replay

```bash
ghostledger replay runs/glrun_...
```

The deterministic preview reruns the manifest's scenario, condition, controls, channels, and seed. Equivalence is defined as the same submitted-state digest. A replay is a new evidence bundle and never overwrites the original.

## Schema evolution

All serialized records contain `schema_version`. Backward-incompatible format changes require a major schema version, migration documentation, and golden fixtures. Scenario content has its own semantic version.
