# ADR-003: Explicit observation channels

Status: Accepted
Date: 2026-08-27

## Context

Monitor performance cannot be interpreted without knowing whether the monitor saw final output, actions, diffs, provenance, or downstream state.

## Decision

Every monitor declares required channels. A run counts a decision only if all those channels are configured.

## Consequences

Channel ablations are enforceable rather than descriptive. Future monitors must use the same contract.
