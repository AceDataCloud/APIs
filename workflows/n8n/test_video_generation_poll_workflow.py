from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW = json.loads((ROOT / "video-generation-poll.json").read_text())
NODES = {node["name"]: node for node in WORKFLOW["nodes"]}


class VideoGenerationPollWorkflowTest(unittest.TestCase):
    def test_graph_routes_every_failure_and_bounded_loop(self) -> None:
        self.assertEqual(len(NODES), 18)
        self.assertEqual(self._targets("Submit succeeded", 0), ["Task ID exists"])
        self.assertEqual(self._targets("Submit succeeded", 1), ["Stop on submit error"])
        self.assertEqual(self._targets("Task ID exists", 0), ["Create bounded poll attempts"])
        self.assertEqual(self._targets("Task ID exists", 1), ["Stop on missing task ID"])
        self.assertEqual(self._targets("Loop over poll attempts", 0), ["Stop on polling timeout"])
        self.assertEqual(self._targets("Loop over poll attempts", 1), ["Wait before polling"])
        self.assertEqual(self._targets("Poll succeeded", 0), ["Task finished"])
        self.assertEqual(self._targets("Poll succeeded", 1), ["Stop on poll error"])
        self.assertEqual(self._targets("Task finished", 0), ["Video result succeeded"])
        self.assertEqual(self._targets("Task finished", 1), ["Loop over poll attempts"])
        self.assertEqual(self._targets("Video result succeeded", 0), ["Return video result"])
        self.assertEqual(self._targets("Video result succeeded", 1), ["Stop on terminal failure"])

    def test_submit_contract_selects_documented_text_and_image_modes(self) -> None:
        node = NODES["Submit video with Ace Data Cloud"]
        parameters = node["parameters"]
        self._assert_http_contract(node, "https://api.acedata.cloud/wan/videos")
        body = parameters["body"]
        for fragment in (
            "action: $json.image_url ? 'image2video' : 'text2video'",
            "model: $json.image_url ? 'wan2.6-i2v' : 'wan2.6-t2v'",
            "prompt: $json.prompt",
            "image_url: $json.image_url || undefined",
            "ratio: $json.ratio",
            "async: true",
        ):
            self.assertIn(fragment, body)
        values = self._assignments("Set video input")
        self.assertTrue(values["prompt"])
        self.assertEqual(values["image_url"], "")
        self.assertEqual(values["ratio"], "16:9")

    def test_poll_contract_uses_submit_task_id_and_fixed_retrieve_action(self) -> None:
        node = NODES["Poll video task"]
        self._assert_http_contract(node, "https://api.acedata.cloud/wan/tasks")
        body = node["parameters"]["body"]
        self.assertIn("action: 'retrieve'", body)
        self.assertIn("$('Submit video with Ace Data Cloud').first().json.body.task_id", body)

    def test_polling_is_exactly_twenty_attempts_at_fifteen_seconds(self) -> None:
        code = NODES["Create bounded poll attempts"]["parameters"]["jsCode"]
        self.assertIn("Array.from({ length: 20 }", code)
        self.assertIn("poll_attempt: index + 1", code)
        loop = NODES["Loop over poll attempts"]
        self.assertEqual(loop["type"], "n8n-nodes-base.splitInBatches")
        self.assertEqual(loop["typeVersion"], 3)
        self.assertEqual(loop["parameters"]["batchSize"], 1)
        wait = NODES["Wait before polling"]["parameters"]
        self.assertEqual(wait, {"amount": 15, "unit": "seconds"})
        timeout = NODES["Stop on polling timeout"]["parameters"]["errorMessage"]
        self.assertIn("20 polls", timeout)
        self.assertIn("approximately 5 minutes", timeout)

    def test_guards_require_http_task_id_and_terminal_result_contracts(self) -> None:
        for name in ("Submit succeeded", "Poll succeeded"):
            condition = self._condition(name)
            self.assertEqual(condition["leftValue"], "={{ $json.statusCode }}")
            self.assertEqual(condition["rightValue"], 200)
            self.assertEqual(condition["operator"], {"type": "number", "operation": "equals"})
        task_id = self._condition("Task ID exists")
        self.assertEqual(task_id["operator"], {"type": "boolean", "operation": "true", "singleValue": True})
        self.assertIn("typeof $json.body.task_id === 'string'", task_id["leftValue"])
        finished = self._condition("Task finished")
        self.assertIn("typeof $json.body.finished_at === 'number'", finished["leftValue"])
        result = self._condition("Video result succeeded")
        self.assertIn("$json.body.response?.success === true", result["leftValue"])
        self.assertIn("response?.video_url", result["leftValue"])
        self.assertNotIn("status", finished["leftValue"].lower())

    def test_error_nodes_fail_closed_with_response_context(self) -> None:
        expected = {
            "Stop on submit error": ("statusCode", "$json.body"),
            "Stop on missing task ID": ("task_id", "$json.body"),
            "Stop on poll error": ("statusCode", "$json.body"),
            "Stop on terminal failure": ("terminal failure", "$json.body"),
            "Stop on polling timeout": ("20 polls", "task_id"),
        }
        for name, fragments in expected.items():
            parameters = NODES[name]["parameters"]
            self.assertEqual(parameters["errorType"], "errorMessage")
            for fragment in fragments:
                self.assertIn(fragment, parameters["errorMessage"])

    def test_output_is_structured_and_uses_validated_task_record(self) -> None:
        output = self._assignments("Return video result")
        self.assertEqual(
            set(output),
            {"status", "task_id", "model", "prompt", "video_url", "thumbnail_url", "elapsed_seconds"},
        )
        self.assertEqual(output["status"], "success")
        self.assertIn("$json.body.response.video_url", output["video_url"])
        self.assertIn("$json.body.id", output["task_id"])
        self.assertIn("Set video input", output["model"])
        self.assertIn("Set video input", output["prompt"])

    def test_export_has_stable_identity_and_no_secret_or_credential_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-video-generation-poll-v1")
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

    def test_documentation_covers_setup_cost_data_and_import_safety(self) -> None:
        readme = (ROOT / "video-generation-poll.md").read_text()
        for text in (
            "utm_campaign=n8n-video-generation-poll",
            "Header Auth",
            "one billable video-generation request",
            "up to 20 task-retrieval requests",
            "Last contract verification: **2026-09-10**",
            "can overwrite an existing workflow",
            "contains no credential ID",
            "does not infer undocumented status strings",
            "approximately five minutes",
            "present in n8n execution data",
        ):
            self.assertIn(text, readme)

    def _assert_http_contract(self, node: dict, url: str) -> None:
        parameters = node["parameters"]
        self.assertEqual(parameters["method"], "POST")
        self.assertEqual(parameters["url"], url)
        self.assertEqual(parameters["authentication"], "genericCredentialType")
        self.assertEqual(parameters["genericAuthType"], "httpHeaderAuth")
        self.assertEqual(parameters["options"]["timeout"], 60000)
        self.assertEqual(
            parameters["options"]["response"]["response"],
            {"fullResponse": True, "neverError": True, "responseFormat": "json"},
        )
        self.assertNotIn("credentials", node)

    def _assignments(self, node: str) -> dict[str, object]:
        return {
            item["name"]: item["value"]
            for item in NODES[node]["parameters"]["assignments"]["assignments"]
        }

    def _condition(self, node: str) -> dict:
        return NODES[node]["parameters"]["conditions"]["conditions"][0]

    def _targets(self, node: str, output: int) -> list[str]:
        return [entry["node"] for entry in WORKFLOW["connections"][node]["main"][output]]


if __name__ == "__main__":
    unittest.main()
