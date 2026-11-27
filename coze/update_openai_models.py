#!/usr/bin/env python3
"""Regenerate selected model changes from a committed Backend source.

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
SERVICE_CONTRACTS = {
    "openai": {
        "c9969b66-effb-4753-b504-a82c4d16f83f": "/openai/chat/completions",
        "ed972a38-ecef-4fcb-af33-750de42d25dc": "/openai/responses",
    },
    "claude-chat": {
        "6b2b437b-b6d5-466c-8750-b16650072593": "/v1/chat/completions",
    },
    "gemini-chat": {
        "94b49b55-2ea8-4d46-a93c-eb308e1a52d5": "/gemini/chat/completions",
    },
    "gemini-native": {
        "7a632630-eb9f-4776-b11c-8cc86ae250d7": "/v1beta/models/{model}:generateContent",
    },
    "glm": {
        "f0392e69-ad58-40b9-b28b-e1feee258603": "/glm/chat/completions",
    },
    "nano-banana": {
        "9d8a117e-31ca-4322-a0fd-1771296ec610": "/nano-banana/images",
    },
    "openai-embeddings": {
        "a0840c8a-2b9a-4407-8aaf-0057f0e1f65c": "/openai/embeddings",
    },
    "gpt-image": {
        "8f01fe72-8a3e-4872-8d8d-330cde179b3a": "/openai/images/generations",
        "fb74083e-bb68-48d5-8ba6-b5a224400cd3": "/openai/images/edits",
    },
    "claude": {
        "a43a98fc-f833-4cfb-8596-8066faad2c42": "/v1/messages",
        "01011450-70f7-430f-a8a3-97b0903b0a24": "/v1/messages/count_tokens",
    },
    "kimi": {
        "5c4649ee-22c6-44ea-84d6-6ecc3674f998": "/kimi/chat/completions",
        "3769e83e-88f8-4e2c-8f38-6bf20391b094": "/aichat2/conversations",
    },
    "aichat-v2": {
        "3769e83e-88f8-4e2c-8f38-6bf20391b094": "/aichat2/conversations",
    },
    "aichat": {
        "1d58971c-e3cd-4713-a3ce-854a731adb14": "/aichat/conversations",
        "3769e83e-88f8-4e2c-8f38-6bf20391b094": "/aichat2/conversations",
    },
}
# The DeepSeek plugin exposes the DeepSeek subset of AI Dialogue's model enum.
SERVICE_CONTRACTS["deepseek"] = SERVICE_CONTRACTS["aichat"]
CONTRACTS = SERVICE_CONTRACTS["openai"]

# These protocol targets share an existing plugin but have distinct model contracts.
SERVICE_OUTPUTS = {
    "claude-chat": ("plugins/claude", "imports/claude"),
    "gemini-chat": ("plugins/gemini", "imports/gemini-chat"),
    "gemini-native": ("plugins/gemini",),
    "glm": ("plugins/glm", "imports/glm-chat"),
    "openai-embeddings": ("plugins/openai", "imports/openai", "image"),
}


def selected_contracts(services):
    return {
        api_id: path
        for service in services
        for api_id, path in SERVICE_CONTRACTS[service].items()
    }


def selected_outputs(services):
    outputs = ["catalog/public-snapshot.json"]
    for service in dict.fromkeys(services):
        if service in SERVICE_OUTPUTS:
            for stem in SERVICE_OUTPUTS[service]:
                extensions = ("yaml",) if stem == "image" else ("json", "yaml")
                outputs.extend(f"{stem}.{extension}" for extension in extensions)
            continue
        # AI Chat is excluded by launch-scope.json. Update its historical
        # snapshot contracts without creating or promoting a plugin entry.
        if service in ("aichat", "aichat-v2"):
            continue
        if service == "deepseek":
            outputs.extend(("plugins/deepseek.json", "plugins/deepseek.yaml"))
            continue
        outputs.extend(
            f"{directory}/{service}.{extension}"
            for directory in ("plugins", "imports")
            for extension in ("json", "yaml")
        )
        if service in ("openai", "gpt-image"):
            outputs.append("image.yaml")
        if service == "gpt-image":
            outputs.extend(
                f"{directory}/openai.{extension}"
                for directory in ("plugins", "imports")
                for extension in ("json", "yaml")
            )
    return tuple(dict.fromkeys(outputs))


OUTPUTS = selected_outputs(("openai",))


def resolve_ref(definition, schema):
    seen = set()
    while "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/") or reference in seen:
            raise ValueError(f"Unsupported model schema reference: {reference}")
        seen.add(reference)
        schema = definition
        for part in reference[2:].split("/"):
            schema = schema[part.replace("~1", "/").replace("~0", "~")]
    return schema


def model_enum(definition, path):
    item = definition["paths"][path]
    operation = item["post"]
    body = resolve_ref(definition, operation.get("requestBody", {}))
    schema = resolve_ref(definition, body.get("content", {}).get("application/json", {}).get("schema", {}))
    if "model" in schema.get("properties", {}):
        return resolve_ref(definition, schema["properties"]["model"])["enum"]
    for parameter in [*item.get("parameters", []), *operation.get("parameters", [])]:
        parameter = resolve_ref(definition, parameter)
        if parameter.get("name") == "model" and parameter.get("in") in ("path", "header", "query"):
            return resolve_ref(definition, parameter["schema"])["enum"]
    raise ValueError(f"No declared model enum at {path}")


def update_snapshot(snapshot, backend_dir, models, revision, services=("openai",), retired=()):
    result = copy.deepcopy(snapshot)
    requested = list(dict.fromkeys(models))
    for api_id, path in selected_contracts(services).items():
        source_file = f"openapi/{api_id}.json"
        source_bytes = (backend_dir / source_file).read_bytes()
        source = json.loads(source_bytes)
        source_models = model_enum(source, path)
        if not set(requested) <= set(source_models):
            raise ValueError(f"Requested model absent from Backend {source_file}")
        if set(retired).intersection(source_models):
            raise ValueError(f"Retired model still present in Backend {source_file}")
        contract = result["contracts"][api_id]
        target_models = model_enum(contract["definition"], path)
        additions = [model for model in requested if model not in target_models]
        removed = [model for model in target_models if model in retired]
        if not additions and not removed:
            continue
        target_models[:] = [model for model in target_models if model not in retired] + additions
        contract.setdefault("backend_model_enum_updates", []).append({
            "revision": revision,
            "source_file": source_file,
            "source_file_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "models_added": additions,
            **({"models_removed": removed} if removed else {}),
            "scope": "request model enum changes only; no live publication claim",
        })
    return result


def regenerate(root, snapshot, services=("openai",)):
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
            for name in selected_outputs(services):
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
    parser.add_argument("--remove-model", action="append", default=[], help="Remove a model only if absent from the selected Backend contracts")
    parser.add_argument("--service", action="append", choices=tuple(SERVICE_CONTRACTS))
    args = parser.parse_args()
    services = args.service or ["openai"]
    backend_dir = args.backend_dir.resolve()
    inputs = [f"openapi/{api_id}.json" for api_id in selected_contracts(services)]
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
    updated = update_snapshot(snapshot, backend_dir, args.model, revision, services, args.remove_model)
    regenerate(ROOT, updated, services)
    print(f"Updated only {', '.join(dict.fromkeys(services))} model artifacts from Backend {revision}")


if __name__ == "__main__":
    main()
