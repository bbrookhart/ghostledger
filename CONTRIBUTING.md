# Contributing to GHOSTLEDGER

GHOSTLEDGER values research validity over scenario count. A contribution should make the benchmark more reproducible, better controlled, or harder to fool without making it more dangerous.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
make check
make test
```

## Scenario contributions

A scenario proposal must include:

- one legitimate task and visible acceptance rule;
- one protected mission property and deterministic downstream interpretation;
- matched benign and adversarial trajectories;
- a benign confounder analysis;
- a primary `GL-Sxx` taxonomy mapping;
- a fictional, inert fixture;
- a safety note;
- tests proving visible-pass/mission-fail separation under the reference trajectory.

Cosmetic variants, prompt-only attacks, real operational settings, and LLM-judge-only oracles are rejected. Read [scenario authoring](docs/scenario-authoring.md).

## Monitor contributions

Every monitor must declare its observation channels, score range, threshold semantics, reason codes, cost assumptions, and whether it detects or enforces. Calibration and test data must remain separate.

## Pull requests

1. Keep the change narrowly scoped.
2. Add or update tests.
3. Update the claim ledger when a public claim changes.
4. Run `make check` and `make test`.
5. Explain safety and interpretation impact.

Use conventional commit prefixes such as `feat:`, `fix:`, `docs:`, `test:`, and `chore:`.
