"""Scenario and taxonomy registry."""

from __future__ import annotations

import json
from collections.abc import Iterable
from importlib.resources import files
from typing import Any

from ghostledger.models import Scenario, ValidationError


def _load_json(name: str) -> Any:
    resource = files("ghostledger").joinpath("data", name)
    return json.loads(resource.read_text(encoding="utf-8"))


class Catalog:
    """Validated immutable view of the built-in preview corpus."""

    def __init__(self, scenarios: Iterable[Scenario] | None = None) -> None:
        loaded = list(
            scenarios or (Scenario.from_dict(item) for item in _load_json("scenarios.json"))
        )
        self._scenarios = {scenario.scenario_id: scenario for scenario in loaded}
        if not self._scenarios:
            raise ValidationError("scenario catalog is empty")
        if len(self._scenarios) != len(loaded):
            raise ValidationError("scenario IDs must be unique")

    def list(self) -> list[Scenario]:
        return sorted(self._scenarios.values(), key=lambda item: item.scenario_id)

    def get(self, scenario_id: str) -> Scenario:
        try:
            return self._scenarios[scenario_id]
        except KeyError as exc:
            raise ValidationError(f"unknown scenario: {scenario_id}") from exc

    def validate(self) -> dict[str, Any]:
        scenarios = self.list()
        domains = sorted({scenario.domain for scenario in scenarios})
        classes = sorted({scenario.primary_class for scenario in scenarios})
        return {
            "scenario_pairs": len(scenarios),
            "adversarial_cases": len(scenarios),
            "benign_twins": len(scenarios),
            "total_cases": len(scenarios) * 2,
            "domains": domains,
            "primary_classes": classes,
            "valid": True,
        }


def taxonomy() -> list[dict[str, str]]:
    return list(_load_json("taxonomy.json"))
