"""Fast offline release checks used by CI and maintainers."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".txt", ".svg"}
PLACEHOLDERS = re.compile(
    r"\b(" + "|".join(("TO" + "DO", "T" + "BD", "FIX" + "ME", "LOREM" + " IPSUM")) + r")\b",
    re.IGNORECASE,
)
SECRET_MARKERS = ("AK" + "IA", "BEGIN " + "PRIVATE KEY")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_SOURCE = re.compile(r"(?:src|href)=\"([^\"]+)\"")


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part.startswith(".") and part not in {".github"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDERS.search(text):
            errors.append(f"placeholder token: {path.relative_to(ROOT)}")
        if any(marker in text for marker in SECRET_MARKERS):
            errors.append(f"secret-like fixture: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".md":
            targets = MARKDOWN_LINK.findall(text) + HTML_SOURCE.findall(text)
            for target in targets:
                clean = target.split("#", 1)[0].strip()
                if not clean or clean.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (path.parent / clean).resolve()
                if not resolved.exists():
                    errors.append(f"broken local link in {path.relative_to(ROOT)}: {target}")
    for name in ["taxonomy.json", "scenarios.json"]:
        path = ROOT / "src" / "ghostledger" / "data" / name
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid {name}: {exc}")
    if errors:
        print("repository checks failed:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in errors), file=sys.stderr)
        return 1
    print("repository checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
