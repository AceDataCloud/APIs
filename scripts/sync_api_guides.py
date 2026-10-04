#!/usr/bin/env python3
"""Publish API repository guides from Backend sources and published translations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
URL = "https://platform.acedata.cloud/api/v1/documents/?limit=1000"


def feed(language: str) -> dict:
    with urlopen(
        Request(URL, headers={"Accept-Language": language}), timeout=60
    ) as response:
        value = json.load(response)
    if not isinstance(value.get("items"), list) or len(value["items"]) < value.get(
        "count", 0
    ):
        raise ValueError("Expected complete public document feed")
    result = {}
    for item in value["items"]:
        api_id = item.get("api_id")
        if not api_id:
            continue
        # One API can have separate create/query guides. Prefer its canonical
        # path alias instead of letting feed ordering select the last guide.
        canonical = (item.get("api") or {}).get("path", "").strip("/").replace("/", "-")
        if api_id not in result or item.get("alias") == canonical:
            result[api_id] = item
    return result


def synchronize(backend: Path, root: Path, english: dict, chinese: dict) -> list[str]:
    spec = importlib.util.spec_from_file_location(
        "contracts", backend / "scripts/ecosystem_contracts.py"
    )
    contracts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contracts)
    services = contracts.load_services(backend)
    aliases = {s["alias"]: s for s in services}
    changed = []

    def write(path, text):
        text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        if not path.exists() or path.read_text() != text:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            changed.append(str(path.relative_to(root)))

    for directory in re.findall(
        r"^  ([a-z0-9-]+):$", (root / "sync.yaml").read_text(), re.M
    ):
        alias = {"nanobanana": "nano-banana", "face": "face-change"}.get(
            directory, directory
        )
        service = aliases.get(alias, {})
        package = root / directory
        if not package.is_dir():
            raise ValueError(f"Missing package {directory}")
        title = service.get("display_name") or directory.title()
        lines = [
            f"# {title} API",
            "",
            f"Public API documentation for {title} on [Ace Data Cloud](https://platform.acedata.cloud).",
            "",
            "Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.",
            "",
            "Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.",
            "",
            "| Method | Endpoint | Current guide |",
            "| --- | --- | --- |",
        ]
        generated = set()
        for api in service.get("apis", []):
            item = english.get(api["id"])
            zh = chinese.get(api["id"])
            source = backend / api.get("guide_source", "_missing")
            if not item or not source.is_file():
                continue
            body = source.read_text()
            slug = source.stem.removeprefix("development_")
            zh_path = package / "docs/zh-CN" / f"{slug}.md"
            write(zh_path, body)
            generated.add(zh_path)
            published_source = ((zh or {}).get("sibling") or {}).get("content", "")
            translated = (item.get("sibling") or {}).get("content", "")

            def normalize(value):
                return re.sub(r"\s+", " ", value).strip()

            if translated and normalize(published_source) == normalize(body):
                content = translated
            else:
                content = f"# {api.get('name') or slug}\n\nThe updated English translation is pending. Use the [current backend guide](zh-CN/{slug}.md) and [OpenAPI reference](platform/openapi/{alias}.json).\n"
            target = package / "docs" / f"{slug}.md"
            write(target, content.rstrip() + "\n")
            generated.add(target)
            lines.append(
                f"| {api.get('method', 'POST')} | `{api['path']}` | [English](docs/{slug}.md) · [中文](docs/zh-CN/{slug}.md) |"
            )
        if not generated:
            lines += [
                "",
                "No API guides for this service are currently published in the platform catalog.",
            ]
        if (package / "docs/platform/README.md").exists():
            lines += [
                "",
                "Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.",
            ]
        lines += [
            "",
            "Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.",
            "",
        ]
        lines += (
            [
                "<!-- platform-reference:start -->",
                "Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.",
                "<!-- platform-reference:end -->",
                "",
            ]
            if (package / "docs/platform/README.md").exists()
            else []
        )
        write(package / "README.md", "\n".join(lines))
        # This documentation repository owns these generated API guide directories.
        for path in [
            *(package / "docs").glob("*.md"),
            *(package / "docs/zh-CN").glob("*.md"),
        ]:
            if path not in generated:
                path.unlink()
                changed.append(str(path.relative_to(root)))
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    english = feed("en")
    chinese = feed("zh-CN")
    changed = synchronize(args.backend_dir, args.output_dir, english, chinese)
    print(f"Updated {len(changed)} API guide files.")


if __name__ == "__main__":
    main()
