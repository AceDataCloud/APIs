#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "suno" / "README.md"
DOCS_URL = (
    "https://platform.acedata.cloud/documents/suno-audios"
    "?utm_source=github&utm_medium=repo&utm_campaign=api-suno"
)
SUPPORT_URL = (
    "https://platform.acedata.cloud/support"
    "?utm_source=github&utm_medium=repo&utm_campaign=api-suno"
)
UUID_DOCUMENT = re.compile(
    r"https://platform\.acedata\.cloud/documents/"
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.IGNORECASE,
)
GUIDE_LINK = re.compile(r"\]\((docs/[^)\s#?]+\.md)\)")
CONTRACT_ROWS = {
    "POST /suno/audios": "docs/suno_audios_generation_api_integration_guide.md",
    "POST /suno/custom-models": "docs/suno_custom_models_api_integration_guide.md",
    "POST /suno/lyrics": "docs/suno_lyrics_generation_api_integration_guide.md",
    "POST /suno/mashup-lyrics": "docs/suno_mashup_lyrics_generation_api_integration_guide.md",
    "POST /suno/midi": "docs/suno_midi_api_integration_guide.md",
    "POST /suno/mp4": "docs/suno_mp4_api_integration_guide.md",
    "POST /suno/persona": "docs/suno_persona_api_integration_guide.md",
    "POST /suno/style": "docs/suno_style_api_integration_guide.md",
    "POST /suno/tasks": "docs/suno_tasks_api_integration_guide.md",
    "POST /suno/timing": "docs/suno_timing_api_integration_guide.md",
    "POST /suno/upload": "docs/suno_upload_api_integration_guide.md",
    "POST /suno/voices": "docs/suno_voices_api_integration_guide.md",
    "POST /suno/vox": "docs/suno_vox_api_integration_guide.md",
    "POST /suno/wav": "docs/suno_wav_api_integration_guide.md",
}


class StructureParser(HTMLParser):
    VOID_ELEMENTS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, tuple[int, int]]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag not in self.VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag, attrs

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            self.errors.append(f"unexpected </{tag}> at line {self.getpos()[0]}")
            return
        open_tag, position = self.stack[-1]
        if open_tag != tag:
            self.errors.append(
                f"expected </{open_tag}> for line {position[0]} before </{tag}> "
                f"at line {self.getpos()[0]}"
            )
            return
        self.stack.pop()


def raw_html_bounds(text: str) -> tuple[int, int] | None:
    start = text.find("<style>")
    end = text.find("\n## APIs and Guides", start)
    if start < 0 or end < 0:
        return None
    return start, end


def validate_html(text: str) -> list[str]:
    bounds = raw_html_bounds(text)
    if bounds is None:
        return ["raw HTML fragment boundaries are missing"]
    parser = StructureParser()
    parser.feed(text[bounds[0] : bounds[1]])
    errors = list(parser.errors)
    errors.extend(
        f"unclosed <{tag}> from line {position[0]}" for tag, position in parser.stack
    )
    return errors


def validate_fences(text: str) -> list[str]:
    errors: list[str] = []
    bounds = raw_html_bounds(text)
    open_fence: tuple[str, int, int] | None = None
    offset = 0
    fence_pattern = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
    for line_number, line_with_ending in enumerate(text.splitlines(keepends=True), start=1):
        line = line_with_ending.rstrip("\r\n")
        match = fence_pattern.match(line)
        if match:
            marker, suffix = match.groups()
            if bounds is not None and bounds[0] <= offset < bounds[1]:
                errors.append(f"code fence leaked into raw HTML at line {line_number}")
            if open_fence is None:
                open_fence = (marker[0], len(marker), line_number)
            elif (
                marker[0] == open_fence[0]
                and len(marker) >= open_fence[1]
                and not suffix.strip()
            ):
                open_fence = None
        offset += len(line_with_ending)
    if open_fence is not None:
        errors.append(f"unclosed code fence from line {open_fence[2]}")
    return errors


def validate_text(text: str, docs_dir: Path) -> list[str]:
    errors: list[str] = []

    quick_starts = re.findall(r"^## Quick Start$", text, re.MULTILINE)
    if len(quick_starts) != 1:
        errors.append(f"expected one Quick Start heading, found {len(quick_starts)}")

    required = {
        "owner metadata": "**Owner:** Ace Data Cloud API Platform team",
        "public availability boundary": "This is an availability check only",
        "no-charge boundary": "POST /suno/tasks` is the confirmed zero-consumption",
        "empty batch request": "'{\"action\":\"retrieve_batch\",\"ids\":[]}'",
        "empty batch success": "{\"items\":[],\"count\":0}",
        "auth limitation": "does not verify credit balance or prove that paid generation is enabled",
        "paid boundary": "POST /suno/audios` is a paid generation operation",
        "tracked API reference": DOCS_URL,
        "tracked support link": SUPPORT_URL,
    }
    for label, fragment in required.items():
        if fragment not in text:
            errors.append(f"missing {label}")

    reviewed = re.search(r"\*\*Contract last reviewed:\*\* (\d{4}-\d{2}-\d{2})", text)
    if not reviewed:
        errors.append("missing contract review date")
    else:
        try:
            date.fromisoformat(reviewed.group(1))
        except ValueError:
            errors.append("invalid contract review date")

    forbidden = {
        "invalid service URL": r"https://platform\.acedata\.cloud/service/suno(?:\b|/)",
        "legacy UUID document URL": UUID_DOCUMENT,
        "unresolved translation token": r"\$t\(",
        "supplier media host": r"https://cdn\d*\.suno\.ai",
        "empty paid request body": r"--data\s+['\"]{}['\"]",
    }
    for label, pattern in forbidden.items():
        if re.search(pattern, text):
            errors.append(f"found {label}")

    guide_refs = set(GUIDE_LINK.findall(text))
    expected_guides = {
        f"docs/{path.name}" for path in docs_dir.glob("*.md") if path.is_file()
    }
    if guide_refs != expected_guides:
        missing = sorted(expected_guides - guide_refs)
        unexpected = sorted(guide_refs - expected_guides)
        if missing:
            errors.append(f"missing guide links: {', '.join(missing)}")
        if unexpected:
            errors.append(f"unexpected guide links: {', '.join(unexpected)}")

    for operation, guide in CONTRACT_ROWS.items():
        row = re.compile(rf"`{re.escape(operation)}`[^\n]*\({re.escape(guide)}\)")
        if not row.search(text):
            errors.append(f"missing contract row for {operation}")

    boundary_order = [
        text.find("### 1. Check service availability (public)"),
        text.find("### 2. Verify your bearer token (no charge)"),
        text.find("### 3. Generate only when you intend to spend credits (paid)"),
    ]
    if any(position < 0 for position in boundary_order) or boundary_order != sorted(boundary_order):
        errors.append("availability, authentication, and paid boundaries are missing or out of order")

    errors.extend(validate_fences(text))
    errors.extend(validate_html(text))
    return errors


def validate_readme(path: Path = README) -> list[str]:
    return validate_text(path.read_text(), path.parent / "docs")


def main() -> int:
    errors = validate_readme()
    if errors:
        for error in errors:
            print(f"suno/README.md: {error}", file=sys.stderr)
        return 1
    print("Suno onboarding boundaries, links, guides, fences, and HTML are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
