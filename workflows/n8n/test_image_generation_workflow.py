from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW = json.loads((ROOT / "image-generation.json").read_text())
NODES = {node["name"]: node for node in WORKFLOW["nodes"]}


class ImageGenerationWorkflowTest(unittest.TestCase):
    def test_graph_routes_transport_and_result_failures_explicitly(self) -> None:
        self.assertEqual(len(NODES), 8)
        self.assertEqual(self._targets("Request succeeded", 0), ["Image result exists"])
        self.assertEqual(self._targets("Request succeeded", 1), ["Stop on API error"])
        self.assertEqual(self._targets("Image result exists", 0), ["Return image result"])
        self.assertEqual(self._targets("Image result exists", 1), ["Stop on missing image"])

    def test_http_node_uses_fixed_public_contract_and_separate_auth(self) -> None:
        node = NODES["Generate image with Ace Data Cloud"]
        parameters = node["parameters"]
        self.assertEqual(parameters["method"], "POST")
        self.assertEqual(parameters["url"], "https://api.acedata.cloud/flux/images")
        self.assertEqual(parameters["authentication"], "genericCredentialType")
        self.assertEqual(parameters["genericAuthType"], "httpHeaderAuth")
        self.assertEqual(parameters["options"]["timeout"], 180000)
        self.assertEqual(
            parameters["options"]["response"]["response"],
            {"fullResponse": True, "neverError": True, "responseFormat": "json"},
        )
        self.assertNotIn("credentials", node)

    def test_payload_matches_generation_request_contract(self) -> None:
        body = NODES["Generate image with Ace Data Cloud"]["parameters"]["body"]
        for fragment in (
            "action: 'generate'",
            "prompt: $json.prompt",
            "size: $json.size",
            "model: $json.model",
            "count: 1",
            "async: false",
        ):
            self.assertIn(fragment, body)
        values = {
            item["name"]: item["value"]
            for item in NODES["Set image input"]["parameters"]["assignments"]["assignments"]
        }
        self.assertEqual(values["model"], "flux-2-klein")
        self.assertEqual(values["size"], "1024x1024")
        self.assertTrue(values["prompt"])

    def test_guards_require_http_200_and_a_real_image(self) -> None:
        status = NODES["Request succeeded"]["parameters"]["conditions"]["conditions"][0]
        self.assertEqual(status["leftValue"], "={{ $json.statusCode }}")
        self.assertEqual(status["rightValue"], 200)
        self.assertEqual(status["operator"], {"type": "number", "operation": "equals"})
        result = NODES["Image result exists"]["parameters"]["conditions"]["conditions"][0]
        self.assertEqual(result["operator"], {"type": "boolean", "operation": "true", "singleValue": True})
        self.assertIn("$json.body.success === true", result["leftValue"])
        self.assertIn("data?.[0]?.image_url", result["leftValue"])

    def test_error_nodes_include_actionable_response_context(self) -> None:
        api_error = NODES["Stop on API error"]["parameters"]
        self.assertEqual(api_error["errorType"], "errorMessage")
        self.assertIn("statusCode", api_error["errorMessage"])
        self.assertIn("$json.body", api_error["errorMessage"])
        missing = NODES["Stop on missing image"]["parameters"]
        self.assertEqual(missing["errorType"], "errorMessage")
        self.assertIn("without a usable image result", missing["errorMessage"])
        self.assertIn("$json.body", missing["errorMessage"])

    def test_output_is_structured_and_uses_validated_result(self) -> None:
        output = {
            item["name"]: item["value"]
            for item in NODES["Return image result"]["parameters"]["assignments"]["assignments"]
        }
        self.assertEqual(set(output), {"status", "model", "prompt", "size", "image_url", "seed"})
        self.assertIn("$json.body.data[0].image_url", output["image_url"])
        self.assertIn("Set image input", output["model"])
        self.assertIn("Set image input", output["size"])

    def test_export_has_stable_identity_and_no_secret_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-image-generation-v1")
        self.assertEqual(WORKFLOW["pinData"], {})
        for field in ("active", "versionId", "meta"):
            self.assertNotIn(field, WORKFLOW)
        serialized = json.dumps(WORKFLOW)
        self.assertIsNone(re.search(r"(?:sk-|Bearer [A-Za-z0-9_-]{8,}|api[_-]?key\s*[:=])", serialized, re.IGNORECASE))
        self.assertNotIn("http://", serialized)

    def test_documentation_covers_setup_cost_data_and_import_safety(self) -> None:
        readme = (ROOT / "image-generation.md").read_text()
        for text in (
            "utm_campaign=n8n-image-generation",
            "Header Auth",
            "one billable image-generation API call",
            "Last contract verification: **2026-09-10**",
            "can overwrite an existing workflow",
            "contains no credential ID",
            "fixes it at one",
            "returned CDN URL is present in n8n execution data",
        ):
            self.assertIn(text, readme)

    def _targets(self, node: str, output: int) -> list[str]:
        return [entry["node"] for entry in WORKFLOW["connections"][node]["main"][output]]


if __name__ == "__main__":
    unittest.main()
