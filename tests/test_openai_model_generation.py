import contextlib
import copy
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

COZE = Path(__file__).resolve().parents[1] / "coze"
spec = importlib.util.spec_from_file_location(
    "openai_model_updater", COZE / "update_openai_models.py"
)
updater = importlib.util.module_from_spec(spec)
with patch.object(sys, "path", [str(COZE), *sys.path]):
    spec.loader.exec_module(updater)


class OpenAIModelGenerationTests(unittest.TestCase):
    def test_selected_additions_preserve_historical_contracts_and_defaults(self):
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        before = copy.deepcopy(snapshot)
        with tempfile.TemporaryDirectory() as temp:
            backend = Path(temp)
            (backend / "openapi").mkdir()
            for api_id, path in updater.CONTRACTS.items():
                definition = copy.deepcopy(snapshot["contracts"][api_id]["definition"])
                updater.model_enum(definition, path).append("fixture-new-model")
                (backend / "openapi" / f"{api_id}.json").write_text(json.dumps(definition))
            updated = updater.update_snapshot(snapshot, backend, ["fixture-new-model"], "revision")
            self.assertEqual(snapshot, before)
            self.assertEqual(
                updater.update_snapshot(updated, backend, ["fixture-new-model"], "revision"),
                updated,
            )
            for api_id, path in updater.CONTRACTS.items():
                contract = updated["contracts"][api_id]
                self.assertEqual(updater.model_enum(contract["definition"], path).pop(), "fixture-new-model")
                updates = contract["backend_model_enum_updates"]
                provenance = updates.pop()
                if not updates:
                    contract.pop("backend_model_enum_updates")
                self.assertEqual(provenance["revision"], "revision")
                self.assertEqual(provenance["models_added"], ["fixture-new-model"])
                self.assertEqual(len(provenance["source_file_sha256"]), 64)
            self.assertEqual(updated, before)
            with self.assertRaises(ValueError):
                updater.update_snapshot(snapshot, backend, ["absent-model"], "revision")
            self.assertEqual(snapshot, before)

    def test_regeneration_preserves_unrelated_services_and_only_updates_allowlisted_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(COZE / name, root / name)
            for name in updater.OUTPUTS:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(COZE / name, target)
            marker = root / "unrelated.json"
            marker.write_text("keep this file verbatim\n")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            snapshot = json.loads((root / updater.OUTPUTS[0]).read_text())
            for api_id, path in updater.CONTRACTS.items():
                updater.model_enum(snapshot["contracts"][api_id]["definition"], path).append("fixture-new-model")
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, snapshot)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            changed = {str(name) for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
            self.assertEqual(changed, set(updater.OUTPUTS))
            for name in ("plugins/openai.json", "imports/openai.json"):
                document = json.loads((root / name).read_text())
                for path in updater.CONTRACTS.values():
                    self.assertIn("fixture-new-model", updater.model_enum(document, path))
            self.assertEqual(marker.read_text(), "keep this file verbatim\n")


if __name__ == "__main__":
    unittest.main()
