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
    def test_operation_specific_targets_match_snapshot_model_contracts(self):
        expected = {
            "aichat-v2": ("gemini-4-neon",),
            "claude-chat": ("gpt-5.6-sol-fast",),
            "gemini-chat": ("gemini-4-carbon", "gemini-4-hydrogen", "gemini-4-neon"),
            "gemini-native": ("gemini-4-carbon", "gemini-4-hydrogen", "gemini-4-neon"),
            "glm": ("glm-4.5", "glm-4.5v"),
            "nano-banana": ("nano-banana-2.1",),
            "openai-embeddings": ("text-embedding-3-small", "text-embedding-3-large"),
        }
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        for service, additions in expected.items():
            contracts = updater.selected_contracts((service,))
            for api_id, path in contracts.items():
                wanted = updater.model_enum(snapshot["contracts"][api_id]["definition"], path)
                self.assertTrue(set(additions) <= set(wanted))
                for name in updater.selected_outputs((service,)):
                    if not name.endswith(".json") or name == updater.OUTPUTS[0]:
                        continue
                    document = json.loads((COZE / name).read_text())
                    self.assertEqual(wanted, updater.model_enum(document, path))
        claude = json.loads((COZE / "imports/claude.json").read_text())
        self.assertIn("claude-sonnet-5-5", updater.model_enum(claude, "/v1/messages"))
        self.assertNotIn("claude-sonnet-5-5", updater.model_enum(claude, "/v1/chat/completions"))
        openai = json.loads((COZE / "imports/openai.json").read_text())
        self.assertNotIn("text-embedding-ada-002", updater.model_enum(openai, "/openai/embeddings"))

    def test_native_model_refresh_keeps_model_in_the_path_only(self):
        services = ("gemini-native",)
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        model = "fixture-native-model"
        api_id, path = next(iter(updater.selected_contracts(services).items()))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(COZE / name, root / name)
            (root / "openapi").mkdir()
            definition = copy.deepcopy(snapshot["contracts"][api_id]["definition"])
            updater.model_enum(definition, path).append(model)
            (root / "openapi" / f"{api_id}.json").write_text(json.dumps(definition))
            updated = updater.update_snapshot(snapshot, root, [model], "revision", services)
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, updated, services)
            document = json.loads((root / "plugins/gemini.json").read_text())
            self.assertIn(model, updater.model_enum(document, path))
            body = document["paths"][path]["post"]["requestBody"]["content"]["application/json"]["schema"]
            self.assertNotIn("model", body.get("properties", {}))
            self.assertNotIn(model, updater.model_enum(document, "/gemini/chat/completions"))

    def test_image_additions_keep_compatible_aliases_in_both_plugins(self):
        services = ("gpt-image",)
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        model = "fixture-compatible-image-alias"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(COZE / name, root / name)
            for name in updater.selected_outputs(services):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(COZE / name, target)
            (root / "openapi").mkdir()
            for api_id, path in updater.selected_contracts(services).items():
                definition = copy.deepcopy(snapshot["contracts"][api_id]["definition"])
                updater.model_enum(definition, path).append(model)
                (root / "openapi" / f"{api_id}.json").write_text(json.dumps(definition))
            updated = updater.update_snapshot(snapshot, root, [model], "fixture-revision", services)
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, updated, services)
            for service in ("gpt-image", "openai"):
                for directory in ("plugins", "imports"):
                    document = json.loads((root / directory / f"{service}.json").read_text())
                    for path in updater.selected_contracts(services).values():
                        self.assertIn(model, updater.model_enum(document, path))
            self.assertEqual(updater.update_snapshot(updated, root, [model], "fixture-revision", services), updated)

    def test_selected_compatibility_contracts_preserve_other_snapshot_content(self):
        services = ("claude", "aichat")
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        before = copy.deepcopy(snapshot)
        contracts = updater.selected_contracts(services)
        with tempfile.TemporaryDirectory() as temp:
            backend = Path(temp)
            (backend / "openapi").mkdir()
            for api_id, path in contracts.items():
                definition = copy.deepcopy(snapshot["contracts"][api_id]["definition"])
                updater.model_enum(definition, path).append("fixture-new-model")
                (backend / "openapi" / f"{api_id}.json").write_text(json.dumps(definition))
            updated = updater.update_snapshot(snapshot, backend, ["fixture-new-model"], "revision", services)
            self.assertEqual(snapshot, before)
            self.assertEqual(updater.update_snapshot(updated, backend, ["fixture-new-model"], "revision", services), updated)
            for api_id, path in contracts.items():
                contract = updated["contracts"][api_id]
                self.assertEqual(updater.model_enum(contract["definition"], path).pop(), "fixture-new-model")
                updates = contract["backend_model_enum_updates"]
                provenance = updates.pop()
                if not updates:
                    contract.pop("backend_model_enum_updates")
                self.assertEqual(provenance["revision"], "revision")
                self.assertEqual(provenance["models_added"], ["fixture-new-model"])
            self.assertEqual(updated, before)

    def test_deepseek_retirement_requires_backend_absence_and_rebuilds_the_service_plugin(self):
        services = ("deepseek",)
        snapshot = json.loads((COZE / updater.OUTPUTS[0]).read_text())
        active, retired = "deepseek-test-active", "deepseek-test-retired"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(COZE / name, root / name)
            (root / "openapi").mkdir()
            contracts = updater.selected_contracts(services)
            for api_id, path in contracts.items():
                definition = snapshot["contracts"][api_id]["definition"]
                updater.model_enum(definition, path).append(retired)
                source = copy.deepcopy(definition)
                ids = updater.model_enum(source, path)
                ids.remove(retired)
                ids.append(active)
                (root / "openapi" / f"{api_id}.json").write_text(json.dumps(source))
            with self.assertRaisesRegex(ValueError, "still present"):
                updater.update_snapshot(snapshot, root, [active], "revision", services, [active])
            updated = updater.update_snapshot(snapshot, root, [active], "revision", services, [retired])
            self.assertEqual(updater.update_snapshot(updated, root, [active], "revision", services, [retired]), updated)
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, updated, services)
            for api_id, path in contracts.items():
                contract = updated["contracts"][api_id]
                self.assertNotIn(retired, updater.model_enum(contract["definition"], path))
                self.assertEqual(contract["backend_model_enum_updates"][-1]["models_removed"], [retired])
            plugin = json.loads((root / "plugins/deepseek.json").read_text())
            ids = updater.model_enum(plugin, "/aichat/conversations")
            self.assertIn(active, ids)
            self.assertNotIn(retired, ids)

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

    def test_compatibility_regeneration_keeps_excluded_aichat_plugin_absent(self):
        services = ("claude", "aichat")
        outputs = updater.selected_outputs(services)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("catalog", "plugins"):
                shutil.copytree(COZE / name, root / name)
            for name in outputs:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(COZE / name, target)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            snapshot = json.loads((root / updater.OUTPUTS[0]).read_text())
            for api_id, path in updater.selected_contracts(services).items():
                updater.model_enum(snapshot["contracts"][api_id]["definition"], path).append("fixture-new-model")
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, snapshot, services)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            changed = {str(name) for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
            self.assertEqual(changed, set(outputs))
            for name in ("plugins/claude.json", "imports/claude.json"):
                document = json.loads((root / name).read_text())
                for path in updater.SERVICE_CONTRACTS["claude"].values():
                    self.assertIn("fixture-new-model", updater.model_enum(document, path))
            self.assertFalse((root / "plugins/aichat.json").exists())
            self.assertFalse((root / "imports/aichat.json").exists())
            with contextlib.redirect_stdout(io.StringIO()):
                updater.regenerate(root, snapshot, services)
            self.assertEqual(after, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
