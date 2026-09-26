#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- canonical-acquisition -->"


def acquisition_url(campaign: str) -> str:
    if not re.fullmatch(r"api-[a-z0-9-]+", campaign):
        raise ValueError(f"invalid API campaign {campaign!r}")
    return (
        "https://platform.acedata.cloud/"
        f"?utm_source=github&utm_medium=repo&utm_campaign={campaign}"
    )


def mapped_apis() -> set[str]:
    return set(
        re.findall(r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE)
    )


def validate_link(path: Path, campaign: str, errors: list[str]) -> None:
    text = path.read_text()
    url = acquisition_url(campaign)
    expected = f"{MARKER}\n[Start building]({url})"
    if text.count(MARKER) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one acquisition marker")
    if text.count(url) != 1 or expected not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing canonical {campaign} link")
    generated_start = text.find("<!-- BEGIN GENERATED")
    if generated_start >= 0 and text.find(MARKER) > generated_start:
        errors.append(f"{path.relative_to(ROOT)}: acquisition link is inside generated content")


def main() -> int:
    errors: list[str] = []
    mappings = mapped_apis()
    validate_link(ROOT / "README.md", "api-catalog", errors)
    for alias in sorted(mappings):
        validate_link(ROOT / alias / "README.md", f"api-{alias}", errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Acquisition links match the catalog and {len(mappings)} mapped APIs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
