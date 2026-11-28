"""Select standalone mirrors from the YAML mapping and the complete push diff."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
SYNC_FILES = {"sync.yaml", ".github/workflows/sync-to-repos.yml", "scripts/sync_matrix.py", "scripts/sync_repository_metadata.py"}


def load_mappings(path):
    mappings = yaml.safe_load(path.read_text())["mappings"]
    for directory, config in mappings.items():
        if not re.fullmatch(r"[A-Za-z0-9_-]+", directory):
            raise ValueError(f"Invalid mirror directory: {directory}")
        if not re.fullmatch(r"AceDataCloud/[A-Za-z0-9_.-]+", config["repo"]):
            raise ValueError(f"Invalid mirror repository for {directory}")
        excludes = config.get("exclude", [])
        if not isinstance(excludes, list) or any(not isinstance(item, str) for item in excludes):
            raise ValueError(f"Invalid exclude list for {directory}")
        metadata = config.get("metadata")
        if metadata is not None:
            if not isinstance(metadata, dict) or set(metadata) != {"description", "homepage", "topics"}:
                raise ValueError(f"Invalid repository metadata for {directory}")
            description = metadata["description"]
            if not isinstance(description, str) or not description.strip() or len(description) > 350:
                raise ValueError(f"Invalid description for {directory}")
            homepage = metadata["homepage"]
            if not isinstance(homepage, str):
                raise ValueError(f"Invalid homepage for {directory}")
            url = urlparse(homepage)
            if url.scheme != "https" or url.netloc != "platform.acedata.cloud" or not re.fullmatch(r"/(services|documents)(/[A-Za-z0-9-]+)?", url.path):
                raise ValueError(f"Invalid homepage for {directory}")
            topics = metadata["topics"]
            if not isinstance(topics, list) or not 1 <= len(topics) <= 20 or any(
                not isinstance(topic, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic)
                for topic in topics
            ):
                raise ValueError(f"Invalid topics for {directory}")
    return mappings


def build_matrix(mappings, changed_paths, sync_all=False):
    sync_all = sync_all or bool(SYNC_FILES.intersection(changed_paths))
    changed_directories = {path.split("/", 1)[0] for path in changed_paths}
    return [
        {
            "dir": directory,
            "repo": config["repo"],
            "exclude": config.get("exclude", []),
            "create_missing": bool(config.get("create_missing", False)),
            "metadata": config.get("metadata"),
        }
        for directory, config in mappings.items()
        if sync_all or directory in changed_directories
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    mappings = load_mappings(ROOT / "sync.yaml")
    before = os.environ.get("BEFORE_SHA", "")
    sync_all = args.all or not before or set(before) == {"0"}
    changed_paths = []
    if not sync_all:
        changed_paths = subprocess.check_output(
            ["git", "diff", "--name-only", before, "HEAD"], cwd=ROOT, text=True
        ).splitlines()
    matrix = build_matrix(mappings, changed_paths, sync_all)
    for entry in matrix:
        if not (ROOT / entry["dir"] / "README.md").is_file():
            raise ValueError(f"Missing README for {entry['dir']}")
    output = (
        "matrix=" + json.dumps({"include": matrix}, separators=(",", ":")) + "\n"
        + "has_changes=" + str(bool(matrix)).lower() + "\n"
    )
    with open(os.environ["GITHUB_OUTPUT"], "a") as stream:
        stream.write(output)
    print(f"Selected {len(matrix)} mirrors")


if __name__ == "__main__":
    main()
