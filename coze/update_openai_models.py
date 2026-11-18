#!/usr/bin/env python3
"""Regenerate selected OpenAI model additions from a committed Backend source.

Keep the dated public snapshot and its other contracts intact. This is an offline
source update, not proof of API deployment or Coze import/store publication.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import build_catalog
import build_imports

ROOT = Path(__file__).resolve().parent
CONTRACTS = {
    "c9969b66-effb-4753-b504-a82c4d16f83f": "/openai/chat/completions",
    "ed972a38-ecef-4fcb-af33-750de42d25dc": "/openai/responses",
}
OUTPUTS = (
    "catalog/public-snapshot.json",
    "plugins/openai.json",
    "plugins/openai.yaml",
    "imports/openai.json",
    "imports/openai.yaml",
    "image.yaml",
)


def model_enum(definition, path):
    return definition["paths"][path]["post"]["requestBody"]["content"][
        "application/json"
    ]["schema"]["properties"]["model"]["enum"]


def update_snapshot(snapshot, backend_dir, models, revision):
    result = copy.deepcopy(snapshot)
    requested = list(dict.fromkeys(models))
    for api_id, path in CONTRACTS.items():
        source_file = f"openapi/{api_id}.json"
        source_bytes = (backend_dir / source_file).read_bytes()
        source = json.loads(source_bytes)
        source_models = model_enum(source, path)
        if not set(requested) <= set(source_models):
            raise ValueError(f"Requested model absent from Backend {source_file}")
        contract = result["contracts"][api_id]
        target_models = model_enum(contract["definition"], path)
        additions = [model for model in requested if model not in target_models]
        if not additions:
            continue
        # Preserve existing defaults and draft examples by appending new IDs.
        target_models.extend(additions)
        contract.setdefault("backend_model_enum_updates", []).append({
            "revision": revision,
            "source_file": source_file,
            "source_file_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "models_added": additions,
            "scope": "request model enum additions only; no live publication claim",
        })
    return result


def regenerate(root, snapshot):
    old_catalog_root, old_import_root = build_catalog.ROOT, build_imports.ROOT
    try:
        with tempfile.TemporaryDirectory(prefix="coze-openai-models-") as temp:
            stage = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(root / name, stage / name)
            (stage / OUTPUTS[0]).write_text(
                json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
            )
            build_catalog.ROOT = build_imports.ROOT = stage
            build_catalog.main()
            build_imports.main()
            for name in OUTPUTS:
                destination = root / name
                data = (stage / name).read_bytes()
                if destination.read_bytes() != data:
                    destination.write_bytes(data)
    finally:
        build_catalog.ROOT, build_imports.ROOT = old_catalog_root, old_import_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-dir", type=Path, required=True)
    parser.add_argument("--model", action="append", required=True)
    args = parser.parse_args()
    backend_dir = args.backend_dir.resolve()
    inputs = [f"openapi/{api_id}.json" for api_id in CONTRACTS]
    dirty = subprocess.check_output(
        ["git", "-C", str(backend_dir), "status", "--porcelain", "--", *inputs],
        text=True,
    )
    if dirty:
        parser.error("Commit the selected Backend OpenAPI inputs before generation")
    revision = subprocess.check_output(
        ["git", "-C", str(backend_dir), "rev-parse", "HEAD"], text=True
    ).strip()
    snapshot = json.loads((ROOT / OUTPUTS[0]).read_text())
    updated = update_snapshot(snapshot, backend_dir, args.model, revision)
    regenerate(ROOT, updated)
    print(f"Updated only OpenAI import artifacts from Backend {revision}")


if __name__ == "__main__":
    main()
