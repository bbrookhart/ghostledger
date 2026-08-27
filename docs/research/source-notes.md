# Research Source Ledger

Accessed: **2026-08-27**. These primary sources inform research design; inclusion does not imply endorsement, official compatibility, or reproduced results.

## Anthropic — SHADE-Arena

Source: https://www.anthropic.com/research/shade-arena-sabotage-monitoring

Design influence:

- treat sabotage and monitoring as a coupled evaluation problem;
- use complex tool environments rather than final-answer prompts alone;
- distinguish an agent's main task from a controlled side objective;
- evaluate monitor performance as well as adversarial capability.

GHOSTLEDGER's distinct contribution is a compact, state-grounded, paired-case harness with explicit prevention, containment, recovery, and evidence-integrity semantics.

## OpenAI — Detecting and reducing scheming

Source: https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/

Design influence:

- separate hidden-misalignment evaluation from ordinary task failure;
- preserve careful claim language around controlled tests;
- treat mitigation as empirical and incomplete rather than proof of alignment.

## OpenAI — Detecting misbehavior in frontier reasoning models

Source: https://openai.com/index/chain-of-thought-monitoring/

Design influence:

- monitor behavior under explicit reward or acceptance loopholes;
- avoid optimizing only against a monitor in a way that may shift behavior out of view;
- maintain outcome and action evidence even when reasoning evidence is unavailable.

## OpenAI — Evaluating chain-of-thought monitorability

Source: https://openai.com/index/evaluating-chain-of-thought-monitorability/

Design influence:

- define monitorability relative to observations and properties of interest;
- compare observation channels explicitly;
- do not assume access to private chain of thought.

## METR — Risk assessment and evaluation reports

Source: https://metr.org/risk-assessment/

Design influence:

- bind conclusions to tested threat models and capability prerequisites;
- separate evaluation evidence from broad risk conclusions;
- record limitations, external review, and reproducibility constraints.

## UK AI Security Institute — Inspect AI

Sources:

- https://inspect.aisi.org.uk/
- https://inspect.aisi.org.uk/sandboxing.html
- https://inspect.aisi.org.uk/agents.html

Design influence:

- explicit datasets, agents, tools, scorers, and logs;
- sandbox requirements for tool-using agent evaluations;
- repeatable evaluation sets and resumable execution.

GHOSTLEDGER v0.1 is not an Inspect plugin. A future adapter should preserve GHOSTLEDGER's protected-oracle and evidence contracts.

## Microsoft — PyRIT

Source: https://github.com/microsoft/PyRIT

Design influence:

- reusable target and scoring abstractions;
- automated red-team campaign ergonomics;
- security-professional workflow and responsible disclosure.

GHOSTLEDGER focuses on stateful sabotage and mission-integrity evidence rather than general harmful-content elicitation.

## MITRE — ATLAS

Source: https://atlas.mitre.org/

Design influence:

- stable identifiers and explicit taxonomy documentation;
- mapping observable techniques without implying intent;
- future crosswalk potential for agent-system threat reporting.
