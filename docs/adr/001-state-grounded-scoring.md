# ADR-001: State-grounded primary scoring

Status: Accepted
Date: 2026-08-27

## Context

Textual outputs and model graders can miss consequential side effects or reproduce the same biases as the evaluated agent.

## Decision

Primary visible success and mission harm are computed from deterministic state rules. Model judgments may become secondary annotations but cannot decide sabotage success alone.

## Consequences

Scenarios require explicit state and protected properties. This improves auditability but limits the first release to domains that can be safely represented with deterministic oracles.
