"""The APIs monorepo is the only source of standalone API repository writes."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class MirrorOwnershipTests(unittest.TestCase):
    def test_mirrors_run_after_merge_and_have_no_second_schedule(self):
        path = ROOT / ".github/workflows/sync-to-repos.yml"
        data = yaml.safe_load(path.read_text())
        triggers = data.get("on", data.get(True))
        self.assertEqual(triggers["push"]["branches"], ["main"])
        self.assertNotIn("schedule", triggers)
        self.assertNotIn("repository_dispatch", triggers)
        self.assertIn("--delete", path.read_text())
        self.assertIn("sync.yaml", path.read_text())

    def test_no_legacy_agent_dispatch_listener_remains(self):
        self.assertFalse((ROOT / ".github/workflows/sync-from-docs.yml").exists())


if __name__ == "__main__":
    unittest.main()
