from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW = json.loads((ROOT / "lyrics-to-music-poll.json").read_text())
NODES = {node["name"]: node for node in WORKFLOW["nodes"]}


class LyricsToMusicPollWorkflowTest(unittest.TestCase):
    def test_graph_routes_lyrics_music_and_poll_failures_explicitly(self) -> None:
        self.assertEqual(len(NODES), 23)
        expected = {
            "Lyrics request succeeded": (["Lyrics result exists"], ["Stop on lyrics API error"]),
            "Lyrics result exists": (["Submit music with Ace Data Cloud"], ["Stop on missing lyrics"]),
            "Music submit succeeded": (["Music task ID exists"], ["Stop on music submit error"]),
            "Music task ID exists": (["Create bounded poll attempts"], ["Stop on missing music task ID"]),
            "Loop over poll attempts": (["Stop on polling timeout"], ["Wait before polling"]),
            "Music poll succeeded": (["Music task finished"], ["Stop on music poll error"]),
            "Music task finished": (["Music result succeeded"], ["Loop over poll attempts"]),
            "Music result succeeded": (["Return song result"], ["Stop on terminal failure"]),
        }
        for node, (true_targets, false_targets) in expected.items():
            self.assertEqual(self._targets(node, 0), true_targets)
            self.assertEqual(self._targets(node, 1), false_targets)

    def test_lyrics_request_matches_required_contract(self) -> None:
        node = NODES["Generate lyrics with Ace Data Cloud"]
        self._assert_http_contract(node, "https://api.acedata.cloud/suno/lyrics", 120000)
        body = node["parameters"]["body"]
        self.assertIn("prompt: $json.theme", body)
        self.assertIn("model: $json.lyrics_model", body)
        values = self._assignments("Set song input")
        self.assertTrue(values["theme"])
        self.assertTrue(values["style"])
        self.assertEqual(values["lyrics_model"], "default")
        self.assertEqual(values["music_model"], "chirp-v5-5")

    def test_music_request_uses_generated_lyrics_in_custom_async_mode(self) -> None:
        node = NODES["Submit music with Ace Data Cloud"]
        self._assert_http_contract(node, "https://api.acedata.cloud/suno/audios", 60000)
        body = node["parameters"]["body"]
        for fragment in (
            "action: 'generate'",
            "music_model",
            "custom: true",
            "lyric: $json.body.data[0].text",
            "title: $json.body.data[0].title",
            "Set song input",
            "instrumental: false",
            "async: true",
        ):
            self.assertIn(fragment, body)

    def test_poll_request_uses_music_task_id_and_retrieve_action(self) -> None:
        node = NODES["Poll music task"]
        self._assert_http_contract(node, "https://api.acedata.cloud/suno/tasks", 60000)
        body = node["parameters"]["body"]
        self.assertIn("action: 'retrieve'", body)
        self.assertIn("$('Submit music with Ace Data Cloud').first().json.body.task_id", body)
        self.assertNotIn("Generate lyrics with Ace Data Cloud').first().json.body.task_id", body)

    def test_polling_is_exactly_twenty_attempts_at_fifteen_seconds(self) -> None:
        code = NODES["Create bounded poll attempts"]["parameters"]["jsCode"]
        self.assertIn("Array.from({ length: 20 }", code)
        self.assertIn("poll_attempt: index + 1", code)
        loop = NODES["Loop over poll attempts"]
        self.assertEqual(loop["type"], "n8n-nodes-base.splitInBatches")
        self.assertEqual(loop["typeVersion"], 3)
        self.assertEqual(loop["parameters"]["batchSize"], 1)
        self.assertEqual(NODES["Wait before polling"]["parameters"], {"amount": 15, "unit": "seconds"})
        timeout = NODES["Stop on polling timeout"]["parameters"]["errorMessage"]
        self.assertIn("20 polls", timeout)
        self.assertIn("approximately 5 minutes", timeout)

    def test_guards_require_exact_http_and_semantic_results(self) -> None:
        for name in ("Lyrics request succeeded", "Music submit succeeded", "Music poll succeeded"):
            condition = self._condition(name)
            self.assertEqual(condition["leftValue"], "={{ $json.statusCode }}")
            self.assertEqual(condition["rightValue"], 200)
            self.assertEqual(condition["operator"], {"type": "number", "operation": "equals"})
        lyrics = self._condition("Lyrics result exists")["leftValue"]
        self.assertIn("$json.body.success === true", lyrics)
        self.assertIn("data?.[0]?.text", lyrics)
        self.assertIn("data[0].title", lyrics)
        task_id = self._condition("Music task ID exists")["leftValue"]
        self.assertIn("typeof $json.body.task_id === 'string'", task_id)
        finished = self._condition("Music task finished")["leftValue"]
        self.assertIn("typeof $json.body.finished_at === 'number'", finished)
        self.assertNotIn("status", finished.lower())
        result = self._condition("Music result succeeded")["leftValue"]
        self.assertIn("$json.body.response?.success === true", result)
        self.assertIn("Array.isArray($json.body.response?.data)", result)
        self.assertIn("data[0]?.audio_url", result)

    def test_error_nodes_fail_closed_with_response_context(self) -> None:
        expected = {
            "Stop on lyrics API error": ("statusCode", "$json.body"),
            "Stop on missing lyrics": ("usable lyrics result", "$json.body"),
            "Stop on music submit error": ("statusCode", "$json.body"),
            "Stop on missing music task ID": ("task_id", "$json.body"),
            "Stop on music poll error": ("statusCode", "$json.body"),
            "Stop on terminal failure": ("terminal failure", "$json.body"),
            "Stop on polling timeout": ("20 polls", "task_id"),
        }
        for name, fragments in expected.items():
            parameters = NODES[name]["parameters"]
            self.assertEqual(parameters["errorType"], "errorMessage")
            for fragment in fragments:
                self.assertIn(fragment, parameters["errorMessage"])

    def test_output_is_structured_and_uses_validated_first_track(self) -> None:
        output = self._assignments("Return song result")
        self.assertEqual(
            set(output),
            {
                "status",
                "lyrics_task_id",
                "music_task_id",
                "model",
                "title",
                "style",
                "lyrics",
                "audio_id",
                "audio_url",
                "image_url",
                "duration_seconds",
                "elapsed_seconds",
            },
        )
        self.assertEqual(output["status"], "success")
        self.assertIn("Generate lyrics with Ace Data Cloud", output["lyrics_task_id"])
        self.assertIn("$json.body.id", output["music_task_id"])
        self.assertIn("$json.body.response.data[0].audio_url", output["audio_url"])
        self.assertIn("Set song input", output["model"])

    def test_export_has_stable_identity_and_no_secret_or_credential_material(self) -> None:
        self.assertEqual(WORKFLOW["id"], "acedata-lyrics-to-music-poll-v1")
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
        readme = (ROOT / "lyrics-to-music-poll.md").read_text()
        for text in (
            "utm_campaign=n8n-lyrics-to-music-poll",
            "Header Auth",
            "one billable lyrics-generation request and one billable music-generation request",
            "plus up to 20 task-retrieval requests",
            "Last contract verification: **2026-09-10**",
            "can overwrite an existing workflow",
            "contains no credential ID",
            "does not infer undocumented task status strings",
            "approximately five minutes",
            "present in n8n execution data",
            "first usable track",
        ):
            self.assertIn(text, readme)

    def _assert_http_contract(self, node: dict, url: str, timeout: int) -> None:
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
