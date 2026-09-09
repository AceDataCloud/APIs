from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW_PATH = ROOT / "search-summary.json"
WORKFLOW = json.loads(WORKFLOW_PATH.read_text())
NODES = {node["name"]: node for node in WORKFLOW["nodes"]}


class SearchSummaryWorkflowTest(unittest.TestCase):
    def test_graph_has_success_and_explicit_failure_routes(self) -> None:
        self.assertEqual(len(NODES), 10)
        self.assertEqual(self._targets("Search succeeded", 0), ["Build grounded summary request"])
        self.assertEqual(self._targets("Search succeeded", 1), ["Stop on search error"])
        self.assertEqual(self._targets("Summary succeeded", 0), ["Return structured report"])
        self.assertEqual(self._targets("Summary succeeded", 1), ["Stop on summary error"])
        self.assertNotIn("Stop on search error", WORKFLOW["connections"])
        self.assertNotIn("Stop on summary error", WORKFLOW["connections"])

    def test_http_nodes_use_fixed_contracts_and_separate_auth(self) -> None:
        expected = {
            "Search with Ace Data Cloud": ("https://api.acedata.cloud/serp/google", 60000),
            "Summarize with Ace Data Cloud": ("https://api.acedata.cloud/v1/chat/completions", 120000),
        }
        for name, (url, timeout) in expected.items():
            node = NODES[name]
            parameters = node["parameters"]
            self.assertEqual(parameters["method"], "POST")
            self.assertEqual(parameters["url"], url)
            self.assertEqual(parameters["authentication"], "genericCredentialType")
            self.assertEqual(parameters["genericAuthType"], "httpHeaderAuth")
            self.assertEqual(parameters["options"]["timeout"], timeout)
            self.assertEqual(
                parameters["options"]["response"]["response"],
                {"fullResponse": True, "neverError": True, "responseFormat": "json"},
            )
            self.assertNotIn("credentials", node)

    def test_payloads_match_public_request_contracts(self) -> None:
        search_body = NODES["Search with Ace Data Cloud"]["parameters"]["body"]
        self.assertIn("query: $json.query", search_body)
        self.assertIn("type: 'search'", search_body)
        self.assertIn("number: $json.number", search_body)
        chat_body = NODES["Summarize with Ace Data Cloud"]["parameters"]["body"]
        self.assertIn("model: $json.model", chat_body)
        self.assertIn("messages: $json.messages", chat_body)
        self.assertIn("temperature: 0.2", chat_body)
        input_values = {
            item["name"]: item["value"]
            for item in NODES["Set research input"]["parameters"]["assignments"]["assignments"]
        }
        self.assertEqual(input_values["model"], "claude-sonnet-5")
        self.assertGreaterEqual(input_values["number"], 1)
        self.assertLessEqual(input_values["number"], 100)

    def test_summary_is_grounded_and_sources_are_preserved(self) -> None:
        assignments = {
            item["name"]: item["value"]
            for item in NODES["Build grounded summary request"]["parameters"]["assignments"]["assignments"]
        }
        messages = assignments["messages"]
        for field in ("organic", "title", "link", "snippet"):
            self.assertIn(field, messages)
        self.assertIn("do not invent facts", messages)
        report = {
            item["name"]: item["value"]
            for item in NODES["Return structured report"]["parameters"]["assignments"]["assignments"]
        }
        self.assertEqual(set(report), {"status", "query", "model", "summary", "sources"})
        self.assertIn("choices[0].message.content", report["summary"])
        self.assertIn("Search with Ace Data Cloud", report["sources"])

    def test_status_gates_and_error_nodes_fail_closed(self) -> None:
        for name in ("Search succeeded", "Summary succeeded"):
            condition = NODES[name]["parameters"]["conditions"]["conditions"]
            self.assertEqual(len(condition), 1)
            self.assertEqual(condition[0]["leftValue"], "={{ $json.statusCode }}")
            self.assertEqual(condition[0]["rightValue"], 200)
            self.assertEqual(condition[0]["operator"], {"type": "number", "operation": "equals"})
        for name in ("Stop on search error", "Stop on summary error"):
            parameters = NODES[name]["parameters"]
            self.assertEqual(parameters["errorType"], "errorMessage")
            self.assertIn("statusCode", parameters["errorMessage"])
            self.assertIn("$json.body", parameters["errorMessage"])

    def test_export_has_stable_identity_and_no_secret_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-search-summary-v1")
        self.assertEqual(WORKFLOW["pinData"], {})
        for field in ("active", "versionId", "meta"):
            self.assertNotIn(field, WORKFLOW)
        serialized = json.dumps(WORKFLOW)
        self.assertIsNone(re.search(r"(?:sk-|Bearer [A-Za-z0-9_-]{8,}|api[_-]?key\s*[:=])", serialized, re.IGNORECASE))
        self.assertNotIn("http://", serialized)

    def test_documentation_covers_setup_cost_data_and_import_safety(self) -> None:
        readme = (ROOT / "search-summary.md").read_text()
        for text in (
            "utm_campaign=n8n-search-summary",
            "Header Auth",
            "two billable API calls",
            "Last contract verification: **2026-09-10**",
            "can overwrite an existing workflow",
            "contains no credential ID",
            "up to `number` organic result titles, links, and snippets",
        ):
            self.assertIn(text, readme)

    def _targets(self, node: str, output: int) -> list[str]:
        return [entry["node"] for entry in WORKFLOW["connections"][node]["main"][output]]


if __name__ == "__main__":
    unittest.main()
