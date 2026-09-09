from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW_PATH = ROOT / "serp-research.json"
WORKFLOW = json.loads(WORKFLOW_PATH.read_text())


class SerpWorkflowTest(unittest.TestCase):
    def test_graph_is_complete_and_deterministic(self) -> None:
        nodes = {node["name"]: node for node in WORKFLOW["nodes"]}
        self.assertEqual(set(nodes), {"Run manually", "Set search input", "Search with Ace Data Cloud"})
        self.assertEqual(WORKFLOW["connections"]["Run manually"]["main"][0][0]["node"], "Set search input")
        self.assertEqual(
            WORKFLOW["connections"]["Set search input"]["main"][0][0]["node"],
            "Search with Ace Data Cloud",
        )

    def test_http_node_uses_fixed_api_and_separate_header_credential(self) -> None:
        node = next(node for node in WORKFLOW["nodes"] if node["type"] == "n8n-nodes-base.httpRequest")
        parameters = node["parameters"]
        self.assertEqual(parameters["url"], "https://api.acedata.cloud/serp/google")
        self.assertEqual(parameters["method"], "POST")
        self.assertEqual(parameters["authentication"], "genericCredentialType")
        self.assertEqual(parameters["genericAuthType"], "httpHeaderAuth")
        self.assertEqual(parameters["options"]["timeout"], 60000)
        self.assertNotIn("credentials", node)

    def test_export_contains_stable_identity_but_no_secret_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-serp-research-v1")
        for field in ("active", "versionId", "meta"):
            self.assertNotIn(field, WORKFLOW)
        self.assertEqual(WORKFLOW["pinData"], {})
        serialized = json.dumps(WORKFLOW)
        self.assertIsNone(re.search(r"(?:sk-|Bearer [A-Za-z0-9_-]{8,}|api[_-]?key\s*[:=])", serialized, re.IGNORECASE))

    def test_documentation_has_attributed_setup_and_security_boundary(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn("utm_campaign=n8n-serp-research", readme)
        self.assertIn("Header Auth", readme)
        self.assertIn("contains no credential ID or secret", readme)


if __name__ == "__main__":
    unittest.main()
