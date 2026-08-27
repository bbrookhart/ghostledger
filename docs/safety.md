# Safety and Responsible Use

## Intended use

GHOSTLEDGER supports defensive evaluation of agent controls in local synthetic environments. Appropriate uses include benchmark research, monitor comparison, evidence-pipeline testing, graduate research, and authorized internal safety exercises using fictional fixtures.

## Prohibited use

Do not use or adapt the project to:

- sabotage a real organization, service, repository, or infrastructure system;
- evade real monitoring or incident response;
- obtain credentials, persist access, exfiltrate data, or deploy malware;
- change a live cyber-physical process;
- target people or organizations without explicit authorization;
- publish operational parameters that could facilitate harm.

## Environment boundary

The standard-library preview does not execute arbitrary agent code. The Docker path disables networking, drops Linux capabilities, sets a read-only root filesystem, and writes only to the mounted artifact directory.

Future adapters must preserve:

- network denied by default;
- no host filesystem mount;
- no secrets in the evaluated environment;
- bounded CPU, memory, process, time, and token use;
- complete tool logging;
- protected oracles outside the agent workspace.

## Cyber-physical cases

All values are invented and dimensionless. Scenarios intentionally omit plant topology, device names, protocols, setpoints, and failure procedures. They are conceptual integrity tests, not control guidance.

## Publication

Publish configuration, denominators, uncertainty, false positives, exclusions, and claim boundaries. Do not anthropomorphize behavior or imply intent from a single trace.

## Vulnerabilities

Report sandbox escape, oracle disclosure, credential exposure, or evidence-integrity failures privately under [SECURITY.md](../SECURITY.md).
