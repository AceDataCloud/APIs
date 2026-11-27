"""Mirror selection must handle hyphenated service names and mapping-only updates."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sync_matrix", ROOT / "scripts/sync_matrix.py")
sync_matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_matrix)


class SyncMatrixTests(unittest.TestCase):
    def setUp(self):
        self.mappings = {
            "suno": {"repo": "AceDataCloud/SunoAPI", "exclude": [".github"]},
            "qwen-image": {"repo": "AceDataCloud/QwenImageAPI", "create_missing": True},
        }

    def test_hyphenated_directory_is_selected(self):
        matrix = sync_matrix.build_matrix(self.mappings, ["qwen-image/README.md"])
        self.assertEqual([row["dir"] for row in matrix], ["qwen-image"])
        self.assertTrue(matrix[0]["create_missing"])
        self.assertEqual(matrix[0]["exclude"], [])

    def test_mapping_only_change_resynchronizes_metadata_and_files(self):
        matrix = sync_matrix.build_matrix(self.mappings, ["sync.yaml"])
        self.assertEqual([row["dir"] for row in matrix], list(self.mappings))
        self.assertEqual(matrix[0]["exclude"], [".github"])
        self.assertFalse(matrix[0]["create_missing"])

    def test_all_changed_directories_from_push_diff_are_included_once(self):
        matrix = sync_matrix.build_matrix(
            self.mappings, ["suno/README.md", "qwen-image/docs/images.md", "suno/docs/tasks.md"]
        )
        self.assertEqual([row["dir"] for row in matrix], ["suno", "qwen-image"])
        self.assertEqual(sync_matrix.build_matrix(self.mappings, ["README.md"]), [])

    def test_yaml_excludes_and_names_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sync.yaml"
            path.write_text("mappings:\n  qwen-image:\n    repo: AceDataCloud/QwenImageAPI\n    exclude: ['.github', 'docs/private notes']\n")
            mappings = sync_matrix.load_mappings(path)
            self.assertEqual(mappings["qwen-image"]["exclude"], [".github", "docs/private notes"])
            path.write_text("mappings:\n  ../invalid:\n    repo: AceDataCloud/QwenImageAPI\n")
            with self.assertRaises(ValueError):
                sync_matrix.load_mappings(path)
