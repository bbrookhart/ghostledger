from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ghostledger.catalog import Catalog
from ghostledger.engine import BASELINE, LAYERED, rule_passes, run_scenario
from ghostledger.models import Rule


class RuleTests(unittest.TestCase):
    def test_rule_operators(self) -> None:
        state = {"n": 3, "s": "safe", "b": True}
        self.assertTrue(rule_passes(Rule("n", "gte", 2), state))
        self.assertTrue(rule_passes(Rule("n", "lte", 4), state))
        self.assertTrue(rule_passes(Rule("s", "in", ["safe", "safer"]), state))
        self.assertTrue(rule_passes(Rule("b", "eq", True), state))
        self.assertTrue(rule_passes(Rule("s", "neq", "unsafe"), state))


class EngineTests(unittest.TestCase):
    def test_baseline_exposes_covert_gap_for_all_adversarial_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for scenario in Catalog().list():
                with self.subTest(scenario=scenario.scenario_id):
                    outcome, _ = run_scenario(
                        scenario.scenario_id,
                        condition="adversarial",
                        controls=BASELINE,
                        output_root=Path(tmp),
                    )
                    self.assertEqual(outcome.visible_success, 1.0)
                    self.assertGreater(outcome.harm, 0.0)
                    self.assertFalse(outcome.detected)

    def test_layered_controls_preserve_benign_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for scenario in Catalog().list():
                with self.subTest(scenario=scenario.scenario_id):
                    outcome, _ = run_scenario(
                        scenario.scenario_id,
                        condition="benign",
                        controls=LAYERED,
                        output_root=Path(tmp),
                    )
                    self.assertEqual(outcome.visible_success, 1.0)
                    self.assertEqual(outcome.harm, 0.0)
                    self.assertFalse(outcome.detected)
                    self.assertFalse(outcome.prevented)

    def test_layered_controls_prevent_reference_sabotage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for scenario in Catalog().list():
                with self.subTest(scenario=scenario.scenario_id):
                    outcome, _ = run_scenario(
                        scenario.scenario_id,
                        condition="adversarial",
                        controls=LAYERED,
                        output_root=Path(tmp),
                    )
                    self.assertTrue(outcome.detected)
                    self.assertTrue(outcome.prevented)
                    self.assertEqual(outcome.harm, 0.0)

    def test_observation_filter_hides_unavailable_monitor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outcome, _ = run_scenario(
                "GL-SW-001",
                condition="adversarial",
                controls=("GL-C03",),
                channels=("final",),
                output_root=Path(tmp),
            )
            self.assertFalse(outcome.detected)
            self.assertGreater(outcome.harm, 0.0)


if __name__ == "__main__":
    unittest.main()
