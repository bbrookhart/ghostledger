from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

from ghostledger.engine import run_scenario
from ghostledger.evidence import EvidenceLedger, verify_bundle, verify_events


class EventLedgerTests(unittest.TestCase):
    def test_hash_chain_is_valid(self) -> None:
        ledger = EvidenceLedger("glrun_test")
        ledger.append(
            actor="target",
            action="test",
            resource="fixture",
            request={"a": 1},
            response={"ok": True},
            decision="executed",
        )
        ledger.append(
            actor="control",
            action="verify",
            resource="fixture",
            request={"a": 1},
            response={"valid": True},
            decision="allowed",
        )
        valid, errors = ledger.verify()
        self.assertTrue(valid, errors)

    def test_event_mutation_is_detected(self) -> None:
        ledger = EvidenceLedger("glrun_test")
        event = ledger.append(
            actor="target",
            action="test",
            resource="fixture",
            request={"a": 1},
            response={"ok": True},
            decision="executed",
        )
        record = asdict(event)
        record["decision"] = "allowed"
        valid, errors = verify_events([record])
        self.assertFalse(valid)
        self.assertTrue(any("event digest mismatch" in item for item in errors))

    def test_event_reordering_is_detected(self) -> None:
        ledger = EvidenceLedger("glrun_test")
        first = ledger.append(
            actor="target",
            action="one",
            resource="fixture",
            request={},
            response={},
            decision="executed",
        )
        second = ledger.append(
            actor="target",
            action="two",
            resource="fixture",
            request={},
            response={},
            decision="executed",
        )
        valid, _ = verify_events([asdict(second), asdict(first)])
        self.assertFalse(valid)

    def test_bundle_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, run_dir = run_scenario("GL-SW-001", condition="benign", output_root=Path(tmp))
            valid, errors = verify_bundle(run_dir)
            self.assertTrue(valid, errors)
            outcome_path = run_dir / "outcome.json"
            outcome = json.loads(outcome_path.read_text())
            outcome["visible_success"] = 0.0
            outcome_path.write_text(json.dumps(outcome))
            valid, errors = verify_bundle(run_dir)
            self.assertFalse(valid)
            self.assertIn("file digest mismatch: outcome.json", errors)


if __name__ == "__main__":
    unittest.main()
