"""Exercise the sync workflow with a fake GitHub CLI; never contact GitHub."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STEPS = yaml.safe_load((ROOT / ".github/workflows/sync-from-docs.yml").read_text())[
    "jobs"
]["create-task"]["steps"]
SHA = "a" * 40
FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with Path(os.environ["GH_CALLS"]).open("a") as log:
    log.write(json.dumps(args) + "\\n")
if args[:2] == ["issue", "list"]:
    print(os.environ.get("EXISTING_ISSUE", ""))
elif args[:1] == ["api"] and "/repos/AceDataCloud/APIs/issues" in args:
    payload = json.load(sys.stdin)
    Path(os.environ["ISSUE_PAYLOAD"]).write_text(json.dumps(payload))
    print(json.dumps({"number": 42, "node_id": "issue-node"}))
elif args[:2] == ["api", "graphql"]:
    print("copilot-node" if any("suggestedActors" in arg for arg in args) else "{}")
else:
    sys.exit("Unexpected GitHub mutation: " + repr(args))
"""


class DocsSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        gh = self.root / "gh"
        gh.write_text(FAKE_GH)
        gh.chmod(0o755)
        self.env = {
            **os.environ,
            "PATH": str(self.root) + os.pathsep + os.environ["PATH"],
            "GH_TOKEN": "offline-test-token",
            "GH_CALLS": str(self.root / "calls.jsonl"),
            "ISSUE_PAYLOAD": str(self.root / "issue.json"),
            "GITHUB_OUTPUT": str(self.root / "output"),
            "SOURCE_SHA": SHA,
            "COMMIT_INFO": "abcdef Documentation update",
            "RECENT_CHANGES": "abcdef Updated parameters",
            "CHANGED_SERVICES": "openai,nano-banana",
            "REPO": "AceDataCloud/APIs",
        }

    def run_step(self, name, **env):
        script = next(step["run"] for step in STEPS if step.get("name") == name)
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", script],
            env={**self.env, **env},
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_new_snapshot_creates_and_assigns_one_review_issue(self):
        result = self.run_step("Create issue for Copilot")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads((self.root / "issue.json").read_text())
        self.assertIn(
            f"https://github.com/AceDataCloud/Docs/tree/{SHA}", payload["body"]
        )
        self.assertIn("\n\n## Changed Services\n", payload["body"])
        self.assertFalse(payload["body"].startswith('"'))
        calls = [
            json.loads(line)
            for line in (self.root / "calls.jsonl").read_text().splitlines()
        ]
        self.assertEqual(len(calls), 4)  # lookup, create, find actor, assign

    def test_retry_preserves_existing_issue_and_does_not_touch_prs(self):
        result = self.run_step("Create issue for Copilot", EXISTING_ISSUE="42")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "issue.json").exists())
        calls = (self.root / "calls.jsonl").read_text().splitlines()
        self.assertEqual(len(calls), 1)

    def test_dispatch_requires_immutable_source_but_manual_can_resolve_main(self):
        for sha in ["", "main", "a" * 40 + "\nref=other"]:
            result = self.run_step(
                "Resolve source request",
                EVENT_NAME="repository_dispatch",
                EVENT_SHA=sha,
            )
            self.assertNotEqual(result.returncode, 0)
        result = self.run_step(
            "Resolve source request", EVENT_NAME="repository_dispatch", EVENT_SHA=SHA
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_step(
            "Resolve source request", EVENT_NAME="workflow_dispatch", MANUAL_SHA=""
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ref=main", (self.root / "output").read_text())


if __name__ == "__main__":
    unittest.main()
