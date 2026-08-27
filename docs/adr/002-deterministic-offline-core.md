# ADR-002: Deterministic offline core

Status: Accepted
Date: 2026-08-27

## Context

Provider-only benchmarks are expensive, nondeterministic, difficult to test in CI, and easy to confuse with model findings.

## Decision

The default package has no runtime dependencies or network requirement. Scripted benign and adversarial adapters validate the harness. Live models are future opt-in adapters.

## Consequences

Every contributor can reproduce mechanics locally. The preview deliberately makes no frontier-model behavior claim.
