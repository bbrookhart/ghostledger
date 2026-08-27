# Security Policy

## Supported version

GHOSTLEDGER is a research technical preview. Security fixes target the latest release on `main`.

## Report privately

Do not open a public issue for a vulnerability that could expose credentials, escape the local evaluation boundary, corrupt evidence without detection, or create a plausible path to unsafe real-world use.

Use GitHub's private vulnerability reporting feature for this repository. Include:

- affected version and commit;
- minimal reproduction in the synthetic range;
- expected and observed trust boundary;
- impact and prerequisites;
- suggested remediation, if known.

Do not test against systems you do not own or lack explicit authorization to assess.

## Scope

High-value reports include:

- access from the evaluated-agent view to protected mission oracles;
- path traversal or host filesystem access;
- failure of the evidence chain to detect covered-file mutation;
- secret exposure in logs or reports;
- unsafe HTML rendering from benchmark-controlled strings;
- network access despite the documented sandbox configuration.

Ordinary disagreement with a scenario oracle is a methodology issue, not a security vulnerability. Open a normal issue with a proposed paired-case correction.

## Disclosure

We will acknowledge a valid private report, reproduce it in the supported configuration, coordinate a remediation, and credit the reporter when requested. There is no bug bounty program.
