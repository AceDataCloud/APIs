from __future__ import annotations

import unittest
from pathlib import Path

import yaml
from openapi_spec_validator import validate


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "suno.yaml"
SCHEMA = yaml.safe_load(SCHEMA_PATH.read_text())
REQUEST = SCHEMA["paths"]["/suno/audios"]["post"]["requestBody"]["content"]["application/json"]["schema"]
PROPERTIES = REQUEST["properties"]


class CozeSunoContractTest(unittest.TestCase):
    def test_is_valid_fixed_endpoint_openapi(self) -> None:
        validate(SCHEMA)
        self.assertEqual(SCHEMA["servers"], [{"url": "https://api.acedata.cloud"}])
        self.assertEqual(SCHEMA["security"], [{"bearerAuth": []}])
        self.assertEqual(SCHEMA["paths"]["/suno/audios"]["post"]["operationId"], "generateMusic")

    def test_models_match_the_current_generation_contract(self) -> None:
        self.assertEqual(
            PROPERTIES["model"]["enum"],
            [
                "chirp-v5-5",
                "chirp-v5",
                "chirp-v4-5-plus",
                "chirp-v4-5",
                "chirp-v4",
                "chirp-v3-5",
                "chirp-v3-0",
            ],
        )
        self.assertEqual(PROPERTIES["model"]["default"], "chirp-v5-5")

    def test_custom_generation_fields_are_constrained(self) -> None:
        self.assertEqual(PROPERTIES["vocal_gender"]["enum"], ["m", "f"])
        self.assertEqual((PROPERTIES["duration"]["minimum"], PROPERTIES["duration"]["maximum"]), (10, 360))
        for field in ("weirdness", "style_influence"):
            self.assertEqual((PROPERTIES[field]["minimum"], PROPERTIES[field]["maximum"]), (0, 1))
        for field in ("lyric_prompt", "negative_tags"):
            self.assertEqual(PROPERTIES[field]["type"], "string")

    def test_plugin_stays_synchronous_and_generation_only(self) -> None:
        for excluded in ("action", "async", "callback_url"):
            self.assertNotIn(excluded, PROPERTIES)


if __name__ == "__main__":
    unittest.main()
