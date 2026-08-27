"""Remove only generated GHOSTLEDGER output directories."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for name in ("runs", "replays", "campaigns", "artifacts", "reports", "dist", "build"):
    target = ROOT / name
    if target.is_dir():
        shutil.rmtree(target)
        print(f"removed {target.relative_to(ROOT)}")
