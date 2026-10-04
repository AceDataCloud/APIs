import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "sync", Path(__file__).parents[1] / "scripts/sync_api_guides.py"
)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class GuideSyncTests(unittest.TestCase):
    def test_current_source_is_preserved_and_stale_translation_is_not_published(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            backend = root / "backend"
            target = root / "consumer"
            (backend / "scripts").mkdir(parents=True)
            (backend / "docs").mkdir()
            (target / "sample/docs").mkdir(parents=True)
            (backend / "docs/development_sample.md").write_text(
                "# 当前指南\nNew parameter."
            )
            (backend / "scripts/ecosystem_contracts.py").write_text(
                'def load_services(root):\n    return [{"alias":"sample", "apis":[{"id":"api", "path":"/sample/run", "method":"POST", "guide_source":"docs/development_sample.md"}]}]\n'
            )
            (target / "sync.yaml").write_text(
                "mappings:\n  sample:\n    repo: example/sample\n"
            )
            old = target / "sample/docs/old.md"
            old.write_text("outdated")
            en = {"api": {"sibling": {"content": "# stale English"}}}
            zh = {"api": {"sibling": {"content": "# old Chinese"}}}
            sync.synchronize(backend, target, en, zh)
            self.assertFalse(old.exists())
            self.assertEqual(
                (target / "sample/docs/zh-CN/sample.md").read_text(),
                "# 当前指南\nNew parameter.\n",
            )
            self.assertNotIn(
                "stale English", (target / "sample/docs/sample.md").read_text()
            )
            self.assertEqual(sync.synchronize(backend, target, en, zh), [])
            zh["api"]["sibling"]["content"] = "# 当前指南\nNew parameter."
            sync.synchronize(backend, target, en, zh)
            self.assertIn(
                "stale English", (target / "sample/docs/sample.md").read_text()
            )


if __name__ == "__main__":
    unittest.main()
