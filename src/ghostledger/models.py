"""Typed domain models and schema validation for GHOSTLEDGER."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

__version__ = "0.1.0"
SCHEMA_VERSION = "1.0"

JsonValue = str | int | float | bool | None
Condition = Literal["benign", "adversarial"]


class ValidationError(ValueError):
    """Raised when benchmark data violates the public schema contract."""


@dataclass(frozen=True)
class Rule:
    path: str
    op: Literal["eq", "neq", "gte", "lte", "in"]
    value: JsonValue | list[JsonValue]
    weight: float = 1.0
    label: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Rule:
        required = {"path", "op", "value"}
        if missing := required - data.keys():
            raise ValidationError(f"rule missing keys: {sorted(missing)}")
        if data["op"] not in {"eq", "neq", "gte", "lte", "in"}:
            raise ValidationError(f"unsupported rule operator: {data['op']}")
        return cls(
            path=str(data["path"]),
            op=data["op"],
            value=data["value"],
            weight=float(data.get("weight", 1.0)),
            label=str(data.get("label", data["path"])),
        )


@dataclass(frozen=True)
class Action:
    path: str
    value: JsonValue
    summary: str
    consequence: Literal["routine", "high"] = "routine"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Action:
        required = {"path", "value", "summary"}
        if missing := required - data.keys():
            raise ValidationError(f"action missing keys: {sorted(missing)}")
        consequence = data.get("consequence", "routine")
        if consequence not in {"routine", "high"}:
            raise ValidationError(f"invalid action consequence: {consequence}")
        return cls(
            path=str(data["path"]),
            value=data["value"],
            summary=str(data["summary"]),
            consequence=consequence,
        )


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    version: str
    title: str
    domain: str
    primary_class: str
    secondary_classes: tuple[str, ...]
    difficulty: Literal["introductory", "intermediate", "advanced"]
    horizon: Literal["short", "medium", "long"]
    task: str
    initial_state: dict[str, JsonValue]
    visible_rules: tuple[Rule, ...]
    mission_rules: tuple[Rule, ...]
    benign_actions: tuple[Action, ...]
    sabotage_actions: tuple[Action, ...]
    expected_change_paths: tuple[str, ...]
    protected_paths: tuple[str, ...]
    allowed_paths: tuple[str, ...]
    downstream_asset: str
    safety_note: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Scenario:
        required = {
            "scenario_id",
            "version",
            "title",
            "domain",
            "primary_class",
            "difficulty",
            "horizon",
            "task",
            "initial_state",
            "visible_rules",
            "mission_rules",
            "benign_actions",
            "sabotage_actions",
            "expected_change_paths",
            "protected_paths",
            "allowed_paths",
            "downstream_asset",
            "safety_note",
        }
        if missing := required - data.keys():
            raise ValidationError(f"scenario missing keys: {sorted(missing)}")
        scenario = cls(
            scenario_id=str(data["scenario_id"]),
            version=str(data["version"]),
            title=str(data["title"]),
            domain=str(data["domain"]),
            primary_class=str(data["primary_class"]),
            secondary_classes=tuple(map(str, data.get("secondary_classes", []))),
            difficulty=data["difficulty"],
            horizon=data["horizon"],
            task=str(data["task"]),
            initial_state=dict(data["initial_state"]),
            visible_rules=tuple(Rule.from_dict(rule) for rule in data["visible_rules"]),
            mission_rules=tuple(Rule.from_dict(rule) for rule in data["mission_rules"]),
            benign_actions=tuple(Action.from_dict(action) for action in data["benign_actions"]),
            sabotage_actions=tuple(Action.from_dict(action) for action in data["sabotage_actions"]),
            expected_change_paths=tuple(map(str, data["expected_change_paths"])),
            protected_paths=tuple(map(str, data["protected_paths"])),
            allowed_paths=tuple(map(str, data["allowed_paths"])),
            downstream_asset=str(data["downstream_asset"]),
            safety_note=str(data["safety_note"]),
        )
        scenario.validate()
        return scenario

    def validate(self) -> None:
        if not self.scenario_id.startswith("GL-"):
            raise ValidationError(f"invalid scenario id: {self.scenario_id}")
        if self.difficulty not in {"introductory", "intermediate", "advanced"}:
            raise ValidationError(f"invalid difficulty: {self.difficulty}")
        if self.horizon not in {"short", "medium", "long"}:
            raise ValidationError(f"invalid horizon: {self.horizon}")
        if not self.visible_rules or not self.mission_rules:
            raise ValidationError("visible and protected mission rules are both required")
        if self.visible_rules == self.mission_rules:
            raise ValidationError("visible and mission oracles must be distinct")
        action_paths = {action.path for action in self.benign_actions + self.sabotage_actions}
        unknown = action_paths - set(self.allowed_paths)
        if unknown:
            raise ValidationError(f"actions use undeclared paths: {sorted(unknown)}")
        if not set(self.protected_paths).issubset(self.initial_state):
            raise ValidationError("every protected path must exist in initial state")

    def public_view(self) -> dict[str, Any]:
        """Return the information exposed to an evaluated agent."""
        return {
            "schema_version": SCHEMA_VERSION,
            "scenario_id": self.scenario_id,
            "version": self.version,
            "title": self.title,
            "domain": self.domain,
            "task": self.task,
            "initial_state": self.initial_state,
            "visible_acceptance": [asdict(rule) for rule in self.visible_rules],
            "allowed_paths": self.allowed_paths,
        }


@dataclass(frozen=True)
class Event:
    schema_version: str
    run_id: str
    event_id: str
    sequence: int
    logical_time: int
    actor: dict[str, str]
    action: str
    resource: str
    request_digest: str
    response_digest: str
    decision: str
    policy_reasons: tuple[str, ...]
    previous_event_digest: str
    event_digest: str


@dataclass(frozen=True)
class MonitorDecision:
    monitor_id: str
    channels: tuple[str, ...]
    score: float
    threshold: float
    detected: bool
    reason_codes: tuple[str, ...]
    evidence_sequences: tuple[int, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Outcome:
    schema_version: str
    run_id: str
    scenario_id: str
    scenario_version: str
    condition: Condition
    controls: tuple[str, ...]
    channels: tuple[str, ...]
    visible_success: float
    mission_integrity: float
    harm: float
    detected: bool
    prevented: bool
    contained: bool
    recovery_completeness: float
    state_digest: str
    final_state_digest: str
    evidence_root: str
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
