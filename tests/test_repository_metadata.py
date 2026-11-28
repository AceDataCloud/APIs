"""About publishing must safely send exact fields and surface failed writes."""

import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sync_repository_metadata", ROOT / "scripts/sync_repository_metadata.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class RepositoryMetadataTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "description": 'Suno API: "songs" and `examples`',
            "homepage": "https://platform.acedata.cloud/services/suno?lang=en&utm_source=github",
            "topics": ["suno", "api"],
        }

    @patch.object(publisher.subprocess, "run")
    def test_sends_structured_json_without_shell_interpolation(self, run):
        publisher.sync_metadata("AceDataCloud/SunoAPI", self.metadata)
        self.assertEqual(run.call_count, 2)
        patch_call, topics_call = run.call_args_list
        self.assertEqual(patch_call.args[0], ["gh", "api", "--method", "PATCH", "repos/AceDataCloud/SunoAPI", "--input", "-"])
        self.assertEqual(json.loads(patch_call.kwargs["input"]), {key: self.metadata[key] for key in ("description", "homepage")})
        self.assertEqual(json.loads(topics_call.kwargs["input"]), {"names": ["suno", "api"]})
        self.assertTrue(patch_call.kwargs["check"])
        self.assertNotIn("shell", patch_call.kwargs)

    @patch.object(publisher.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "gh"))
    def test_api_failure_fails_the_sync_job(self, run):
        with self.assertRaises(subprocess.CalledProcessError):
            publisher.sync_metadata("AceDataCloud/SunoAPI", self.metadata)

    @patch.object(publisher.subprocess, "run")
    def test_unconfigured_metadata_does_not_write(self, run):
        publisher.sync_metadata("AceDataCloud/SunoAPI", None)
        run.assert_not_called()

    def test_metadata_runs_before_the_no_file_changes_exit(self):
        workflow = (ROOT / ".github/workflows/sync-to-repos.yml").read_text()
        self.assertLess(workflow.index("python3 scripts/sync_repository_metadata.py"), workflow.index("diff --cached --quiet"))
