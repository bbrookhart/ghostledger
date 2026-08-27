# Project Status

## Release

Current version: **v0.1.0 deterministic technical preview**

The preview is designed to establish a credible, testable foundation. “Complete” below means implemented and covered by local tests; it does not mean the research question is solved.

## Capability matrix

| Capability | Status | Evidence |
| --- | --- | --- |
| Typed scenario validation | Complete | `models.py`, catalog tests |
| 24 scenario pairs / 48 cases | Complete | `scenario validate`, corpus data |
| Six synthetic domains | Complete | Catalog validation |
| All 18 taxonomy classes | Complete | Taxonomy coverage test |
| Public/protected scenario split | Complete | `public_view()` and tests |
| Benign and sabotage reference agents | Complete | Engine trajectories |
| Controls C00–C10 | Complete for deterministic state | Engine and corpus-wide tests |
| C11 named layered posture | Complete as CLI alias/research label | `LAYERED` tuple and docs |
| Observation-channel enforcement | Complete | Engine channel test |
| Hash-linked events | Complete | Mutation and reorder tests |
| Covered-file integrity manifest | Complete | Bundle tamper test |
| Replay equivalence | Complete | CLI replay and state digests |
| Campaign execution | Complete | JSON manifest runner |
| Campaign resume | Complete | Stored manifest and completed-run index |
| JSON/Markdown/HTML reporting | Complete | Reporter tests |
| Provider-backed model adapters | Planned | No public implementation claim |
| Sealed holdout packs | Planned | Threat model documents leakage risk |
| Statistical model comparison | Planned | Requires preregistration and real runs |
| Human-review burden study | Planned | Cost fields not yet collected |
| Inspect/PyRIT adapters | Planned | No compatibility claim |

## Known technical debt

- The synthetic state map is intentionally simpler than a containerized repository or service graph.
- Preview harm is binary because each case has one protected rule.
- Linux container image tags are human-readable rather than digest-pinned in v0.1; release maintainers should resolve and verify a digest before a high-assurance image release.
- GitHub Actions use maintained major-version tags; commit-SHA pinning is planned for the hardened release workflow.
- The preview has no cost or latency accounting for external models because it makes no provider calls.

## v0.2 gates

- containerized software-workspace adapter;
- acceptable-state sets for diverse benign solutions;
- calibrated continuous harm in at least two domains;
- Inspect export adapter;
- sealed scenario-pack tooling;
- signed release artifacts and SBOM;
- action and base-image immutable pinning.

## Research-release gates

- frozen live-model protocol;
- provider and privacy review;
- development/validation/test split;
- preregistered thresholds and exclusion rules;
- scenario-level power analysis;
- independent scenario review;
- reproducible raw outcome release consistent with provider terms.
