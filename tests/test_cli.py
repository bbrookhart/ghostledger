from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ghostledger.cli import main


class CliTests(unittest.TestCase):
    def test_doctor(self) -> None:
        self.assertEqual(main(["doctor"]), 0)

    def test_demo_and_evidence_verify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["demo", "--output", str(root)]), 0)
            runs = sorted((root / "demo" / "runs").iterdir())
            self.assertEqual(len(runs), 4)
            self.assertEqual(main(["evidence", "verify", str(runs[0])]), 0)

    def test_campaign_resume_does_not_duplicate_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "small.json"
            manifest.write_text(
                json.dumps(
                    {
                        "name": "small",
                        "scenarios": ["GL-SW-001"],
                        "conditions": ["benign"],
                        "control_sets": {"baseline": "baseline"},
                        "seeds": [0],
                    }
                )
            )
            output = root / "campaigns"
            self.assertEqual(main(["campaign", "run", str(manifest), "--output", str(output)]), 0)
            campaign = output / "small"
            self.assertEqual(len(list((campaign / "runs").iterdir())), 1)
            self.assertEqual(main(["campaign", "resume", str(campaign)]), 0)
            self.assertEqual(len(list((campaign / "runs").iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
