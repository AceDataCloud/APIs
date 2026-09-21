from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW = json.loads((ROOT / "model-api-smoke-test.json").read_text())
NODES = {node["name"]: node for node in WORKFLOW["nodes"]}


class ModelApiSmokeWorkflowTest(unittest.TestCase):
    def test_graph_routes_each_failure_class_explicitly(self) -> None:
        self.assertEqual(len(NODES), 15)
        expected = {
            "Model directory succeeded": (["Model directory is valid"], ["Stop on directory error"]),
            "Model directory is valid": (["Target model is listed"], ["Stop on invalid directory"]),
            "Target model is listed": (["Test completion with Ace Data Cloud"], ["Stop on missing model"]),
            "Completion request succeeded": (["Completion result is valid"], ["Stop on completion error"]),
            "Completion result is valid": (["Return health report"], ["Stop on invalid completion"]),
        }
        for node, (true_targets, false_targets) in expected.items():
            self.assertEqual(self._targets(node, 0), true_targets)
            self.assertEqual(self._targets(node, 1), false_targets)

    def test_directory_request_uses_fixed_https_endpoint_and_auth_boundary(self) -> None:
        node = NODES["List models with Ace Data Cloud"]
        parameters = node["parameters"]
        self.assertEqual(parameters["url"], "https://api.acedata.cloud/v1/models")
        self.assertNotIn("method", parameters)
        self._assert_http_options(node, 30000)

    def test_directory_guards_require_exact_http_shape_and_model_identity(self) -> None:
        status = self._condition("Model directory succeeded")
        self.assertEqual(status["leftValue"], "={{ $json.statusCode }}")
        self.assertEqual(status["rightValue"], 200)
        self.assertEqual(status["operator"], {"type": "number", "operation": "equals"})

        shape = self._condition("Model directory is valid")
        self.assertEqual(shape["operator"], {"type": "boolean", "operation": "true", "singleValue": True})
        for fragment in ("body.object === 'list'", "Array.isArray($json.body.data)", "typeof item.id === 'string'", "item.id.length > 0"):
            self.assertIn(fragment, shape["leftValue"])

        visibility = self._condition("Target model is listed")
        self.assertEqual(visibility["operator"], {"type": "boolean", "operation": "true", "singleValue": True})
        self.assertIn("item.id === $('Set smoke test input').first().json.model", visibility["leftValue"])

    def test_completion_request_is_minimal_bounded_and_non_streaming(self) -> None:
        values = self._assignments("Set smoke test input")
        self.assertEqual(values["model"], "claude-sonnet-5")
        self.assertEqual(values["prompt"], "Reply with exactly: smoke test passed")
        self.assertEqual(values["max_tokens"], 32)

        node = NODES["Test completion with Ace Data Cloud"]
        parameters = node["parameters"]
        self.assertEqual(parameters["method"], "POST")
        self.assertEqual(parameters["url"], "https://api.acedata.cloud/v1/chat/completions")
        self.assertTrue(parameters["sendBody"])
        self.assertEqual(parameters["contentType"], "raw")
        self.assertEqual(parameters["rawContentType"], "application/json")
        for fragment in ("model:", "messages: [{ role: 'user'", "max_tokens:", "temperature: 0", "stream: false"):
            self.assertIn(fragment, parameters["body"])
        self._assert_http_options(node, 120000)

    def test_completion_guards_require_exact_http_and_semantic_contract(self) -> None:
        status = self._condition("Completion request succeeded")
        self.assertEqual(status["leftValue"], "={{ $json.statusCode }}")
        self.assertEqual(status["rightValue"], 200)
        self.assertEqual(status["operator"], {"type": "number", "operation": "equals"})

        result = self._condition("Completion result is valid")
        self.assertEqual(result["operator"], {"type": "boolean", "operation": "true", "singleValue": True})
        for fragment in (
            "typeof $json.body.id === 'string'",
            "typeof $json.body.model === 'string'",
            "Array.isArray($json.body.choices)",
            "choices[0]?.message?.content",
            "usage?.prompt_tokens === 'number'",
            "usage?.completion_tokens === 'number'",
            "usage?.total_tokens === 'number'",
        ):
            self.assertIn(fragment, result["leftValue"])

    def test_error_nodes_fail_closed_with_diagnostic_context(self) -> None:
        expected = {
            "Stop on directory error": ("HTTP", "statusCode", "$json.body"),
            "Stop on invalid directory": ("HTTP 200", "object=list", "$json.body"),
            "Stop on missing model": ("Target model", "absent", "Set smoke test input"),
            "Stop on completion error": ("HTTP", "statusCode", "$json.body"),
            "Stop on invalid completion": ("HTTP 200", "id, model, content, and usage", "$json.body"),
        }
        for name, fragments in expected.items():
            parameters = NODES[name]["parameters"]
            self.assertEqual(parameters["errorType"], "errorMessage")
            for fragment in fragments:
                self.assertIn(fragment, parameters["errorMessage"])

    def test_health_report_is_structured_and_uses_validated_values(self) -> None:
        output = self._assignments("Return health report")
        self.assertEqual(
            set(output),
            {
                "status",
                "checked_at",
                "requested_model",
                "resolved_model",
                "catalog_count",
                "completion_id",
                "content",
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
            },
        )
        self.assertEqual(output["status"], "healthy")
        self.assertIn("$now.toISO()", output["checked_at"])
        self.assertIn("Set smoke test input", output["requested_model"])
        self.assertIn("$json.body.model", output["resolved_model"])
        self.assertIn("List models with Ace Data Cloud", output["catalog_count"])
        self.assertIn("$json.body.usage.total_tokens", output["total_tokens"])

    def test_export_has_stable_identity_and_no_secret_or_credential_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-model-api-smoke-test-v1")
        self.assertEqual(WORKFLOW["pinData"], {})
        for field in ("active", "versionId", "meta"):
            self.assertNotIn(field, WORKFLOW)
        for node in WORKFLOW["nodes"]:
            self.assertNotIn("credentials", node)
        serialized = json.dumps(WORKFLOW)
        self.assertIsNone(
            re.search(r"(?:^|[^A-Za-z0-9])(?:sk-|Bearer [A-Za-z0-9_-]{8,}|api[_-]?key\s*[:=])", serialized, re.IGNORECASE)
        )
        self.assertNotIn("http://", serialized)

    def test_documentation_covers_setup_cost_data_scope_and_import_safety(self) -> None:
        readme = (ROOT / "model-api-smoke-test.md").read_text()
        for text in (
            "utm_campaign=n8n-model-api-smoke-test",
            "Header Auth",
            "one billable chat-completion request",
            "Last contract verification: **2026-09-10**",
            "can overwrite an existing workflow",
            "contains no credential ID",
            "malformed model-directory envelope",
            "requested model absent",
            "missing required ID, model, content, or usage fields",
            "not a latency SLA",
            "present in n8n execution data",
        ):
            self.assertIn(text, readme)

    def _assert_http_options(self, node: dict, timeout: int) -> None:
        parameters = node["parameters"]
        self.assertEqual(parameters["authentication"], "genericCredentialType")
        self.assertEqual(parameters["genericAuthType"], "httpHeaderAuth")
        self.assertEqual(parameters["options"]["timeout"], timeout)
        self.assertEqual(
            parameters["options"]["response"]["response"],
            {"fullResponse": True, "neverError": True, "responseFormat": "json"},
        )
        self.assertNotIn("credentials", node)

    def _assignments(self, node: str) -> dict[str, object]:
        return {item["name"]: item["value"] for item in NODES[node]["parameters"]["assignments"]["assignments"]}

    def _condition(self, node: str) -> dict:
        return NODES[node]["parameters"]["conditions"]["conditions"][0]

    def _targets(self, node: str, output: int) -> list[str]:
        return [entry["node"] for entry in WORKFLOW["connections"][node]["main"][output]]


if __name__ == "__main__":
    unittest.main()
