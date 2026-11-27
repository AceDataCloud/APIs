"""Every first-call example includes a readable, parseable response at that step."""

import json
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def quickstart(text):
    match = re.search(r"^## Quick ?[Ss]tart\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else None


def response_blocks(text):
    return [json.loads(value) for value in re.findall(r"```json\n(.*?)\n```", text, re.S)]


class QuickstartResponsesTests(unittest.TestCase):
    def test_all_api_quickstarts_include_response_json_after_the_request(self):
        mappings = yaml.safe_load((ROOT / "sync.yaml").read_text())["mappings"]
        paths = [ROOT / "README.md"] + [
            ROOT / service / "README.md" for service in mappings if service not in {"sora", "coze"}
        ]
        for path in paths:
            with self.subTest(readme=path.relative_to(ROOT)):
                content = path.read_text()
                section = quickstart(content)
                self.assertIsNotNone(section)
                blocks = response_blocks(section)
                self.assertTrue(blocks)
                self.assertTrue(all(isinstance(value, dict) and value for value in blocks))
                self.assertRegex(section, r"(?i)response JSON")
                self.assertLess(section.index("```bash"), section.index("```json"))
                self.assertNotIn("create-api-key-en.png", content)

    def test_async_quickstarts_show_acceptance_processing_and_completion(self):
        mappings = yaml.safe_load((ROOT / "sync.yaml").read_text())["mappings"]
        for service in mappings:
            path = ROOT / service / "README.md"
            section = quickstart(path.read_text())
            if not section or not re.search(r'"async"\s*:\s*true', section):
                continue
            with self.subTest(service=service):
                self.assertIn("### Submission response JSON", section)
                self.assertIn("### Processing response JSON", section)
                self.assertIn("### Completed response JSON", section)
                accepted, processing, completed = response_blocks(section)
                self.assertIn("task_id", accepted)
                self.assertTrue(processing)
                self.assertTrue(completed)
                self.assertNotEqual(processing, completed)
                self.assertIn("TASK_ID", json.dumps(accepted))
                self.assertIn("TASK_ID", json.dumps(processing))
                self.assertIn("TASK_ID", json.dumps(completed))

    def test_image_and_3d_secondary_quickstarts_have_response_examples(self):
        for service, title in (("openai", "Generate an image with GPT Image 2.6"), ("tripo", "Generate a model")):
            text = (ROOT / service / "README.md").read_text()
            section = text.split("## " + title + "\n", 1)[1].split("\n## ", 1)[0]
            with self.subTest(service=service):
                self.assertTrue(response_blocks(section))
                self.assertRegex(section, r"(?i)response JSON")

    def test_async_result_examples_keep_service_specific_nesting(self):
        rows = {
            "happyhorse": lambda value: value["response"]["data"][0]["video_url"],
            "acemusic": lambda value: value["response"]["data"][1]["audio_url"],
            "seedance": lambda value: value["response"]["data"]["content"]["video_url"],
            "minimax": lambda value: value["task"]["content"]["url"],
            "maestro": lambda value: value["response"]["data"]["variants"][0]["output_url"],
            "digitalhuman": lambda value: value["response"]["video_url"],
        }
        for service, output in rows.items():
            with self.subTest(service=service):
                blocks = response_blocks(quickstart((ROOT / service / "README.md").read_text()))
                self.assertTrue(output(blocks[-1]).startswith("https://"))
