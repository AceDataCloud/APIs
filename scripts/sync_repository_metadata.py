"""Publish the reviewed GitHub About fields independently of file changes."""

import json
import os
import re
import subprocess


def sync_metadata(repository, metadata):
    if metadata is None:
        return
    if not re.fullmatch(r"AceDataCloud/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Invalid mirror repository")
    for endpoint, method, payload in [
        (f"repos/{repository}", "PATCH", {key: metadata[key] for key in ("description", "homepage")}),
        (f"repos/{repository}/topics", "PUT", {"names": metadata["topics"]}),
    ]:
        subprocess.run(
            ["gh", "api", "--method", method, endpoint, "--input", "-"],
            input=json.dumps(payload),
            text=True,
            stdout=subprocess.DEVNULL,
            check=True,
        )
    print(f"Updated About metadata for {repository}")


if __name__ == "__main__":
    sync_metadata(os.environ["MIRROR_REPOSITORY"], json.loads(os.environ["MIRROR_METADATA"]))
