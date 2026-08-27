from __future__ import annotations

import unittest

from ghostledger.catalog import Catalog, taxonomy


class CatalogTests(unittest.TestCase):
    def test_preview_has_24_pairs_and_48_cases(self) -> None:
        stats = Catalog().validate()
        self.assertEqual(stats["scenario_pairs"], 24)
        self.assertEqual(stats["adversarial_cases"], 24)
        self.assertEqual(stats["benign_twins"], 24)
        self.assertEqual(stats["total_cases"], 48)

    def test_all_domains_are_represented(self) -> None:
        self.assertEqual(len(Catalog().validate()["domains"]), 6)

    def test_all_taxonomy_classes_are_primary_somewhere(self) -> None:
        expected = {item["id"] for item in taxonomy()}
        actual = {item.primary_class for item in Catalog().list()}
        self.assertEqual(expected, actual)

    def test_public_view_hides_protected_material(self) -> None:
        view = Catalog().get("GL-SW-001").public_view()
        self.assertNotIn("mission_rules", view)
        self.assertNotIn("sabotage_actions", view)
        self.assertNotIn("protected_paths", view)
        self.assertIn("visible_acceptance", view)

    def test_every_pair_has_distinct_benign_and_sabotage_trajectory(self) -> None:
        for scenario in Catalog().list():
            with self.subTest(scenario=scenario.scenario_id):
                self.assertNotEqual(scenario.benign_actions, scenario.sabotage_actions)


if __name__ == "__main__":
    unittest.main()
