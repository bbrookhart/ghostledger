"""Tamper-evident event and artifact handling."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ghostledger.models import SCHEMA_VERSION, Event, MonitorDecision, Outcome


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class EvidenceLedger:
    """Append-only hash-linked event ledger owned by the evaluation harness."""

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.events: list[Event] = []
        self.logical_time = 0

    def append(
        self,
        *,
        actor: str,
        action: str,
        resource: str,
        request: Any,
        response: Any,
        decision: str,
        reasons: tuple[str, ...] = (),
    ) -> Event:
        sequence = len(self.events) + 1
        self.logical_time += 1
        previous = self.events[-1].event_digest if self.events else "sha256:" + "0" * 64
        unsigned = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "event_id": f"glevent_{sequence:06d}",
            "sequence": sequence,
            "logical_time": self.logical_time,
            "actor": {"type": "agent" if actor == "target" else "control", "id": actor},
            "action": action,
            "resource": resource,
            "request_digest": digest(request),
            "response_digest": digest(response),
            "decision": decision,
            "policy_reasons": reasons,
            "previous_event_digest": previous,
        }
        event = Event(
            schema_version=SCHEMA_VERSION,
            run_id=self.run_id,
            event_id=f"glevent_{sequence:06d}",
            sequence=sequence,
            logical_time=self.logical_time,
            actor={"type": "agent" if actor == "target" else "control", "id": actor},
            action=action,
            resource=resource,
            request_digest=digest(request),
            response_digest=digest(response),
            decision=decision,
            policy_reasons=reasons,
            previous_event_digest=previous,
            event_digest=digest(unsigned),
        )
        self.events.append(event)
        return event

    def verify(self) -> tuple[bool, list[str]]:
        return verify_events([asdict(event) for event in self.events])


def verify_events(events: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    previous = "sha256:" + "0" * 64
    for expected_sequence, event in enumerate(events, 1):
        supplied = event.get("event_digest")
        unsigned = {key: value for key, value in event.items() if key != "event_digest"}
        if event.get("sequence") != expected_sequence:
            errors.append(f"event {expected_sequence}: sequence mismatch")
        if event.get("previous_event_digest") != previous:
            errors.append(f"event {expected_sequence}: previous digest mismatch")
        calculated = digest(unsigned)
        if supplied != calculated:
            errors.append(f"event {expected_sequence}: event digest mismatch")
        previous = str(supplied)
    return not errors, errors


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_bundle(
    root: Path,
    *,
    manifest: dict[str, Any],
    events: list[Event],
    initial_state: dict[str, Any],
    submitted_state: dict[str, Any],
    final_state: dict[str, Any],
    checks: dict[str, Any],
    decisions: list[MonitorDecision],
    outcome: Outcome,
) -> Path:
    run_dir = root / outcome.run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    _write_json(run_dir / "manifest.json", manifest)
    (run_dir / "events.jsonl").write_text(
        "".join(json.dumps(asdict(event), sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )
    _write_json(run_dir / "snapshots" / "initial.json", initial_state)
    _write_json(run_dir / "snapshots" / "submitted.json", submitted_state)
    _write_json(run_dir / "snapshots" / "final.json", final_state)
    _write_json(run_dir / "checks" / "results.json", checks)
    _write_json(run_dir / "monitors" / "decisions.json", [asdict(item) for item in decisions])
    _write_json(run_dir / "outcome.json", outcome.as_dict())
    covered = sorted(path for path in run_dir.rglob("*") if path.is_file())
    files = {str(path.relative_to(run_dir)): file_digest(path) for path in covered}
    integrity = {
        "schema_version": SCHEMA_VERSION,
        "algorithm": "sha256",
        "files": files,
        "root_digest": digest(files),
        "scope_note": "Detects modification, deletion, or substitution of listed local evidence files.",
    }
    _write_json(run_dir / "integrity.json", integrity)
    return run_dir


def verify_bundle(run_dir: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    try:
        integrity = json.loads((run_dir / "integrity.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, [f"cannot read integrity manifest: {exc}"]
    files = integrity.get("files", {})
    if integrity.get("root_digest") != digest(files):
        errors.append("integrity root digest mismatch")
    for relative, expected in files.items():
        path = run_dir / relative
        if not path.is_file():
            errors.append(f"missing covered file: {relative}")
        elif file_digest(path) != expected:
            errors.append(f"file digest mismatch: {relative}")
    try:
        events = [json.loads(line) for line in (run_dir / "events.jsonl").read_text().splitlines()]
        valid, event_errors = verify_events(events)
        if not valid:
            errors.extend(event_errors)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot verify event ledger: {exc}")
    return not errors, errors
