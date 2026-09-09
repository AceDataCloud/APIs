from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml


ROOT = Path(__file__).resolve().parent
PACKET = json.loads((ROOT / "submission-packet.json").read_text())
SCHEMA_PATH = ROOT.parent / PACKET["pilot"]["schema"]["path"]
SCHEMA = yaml.safe_load(SCHEMA_PATH.read_text())


class CozeSubmissionPacketTest(unittest.TestCase):
    def test_packet_is_explicitly_owner_and_external_gated(self) -> None:
        self.assertEqual(PACKET["schema_version"], 1)
        self.assertEqual(PACKET["status"], "pending-owner")
        self.assertEqual(PACKET["verified_at"], "2026-09-10")
        self.assertEqual(PACKET["pilot"]["channel"], "owner-selection-required")
        self.assertEqual(PACKET["pilot"]["listing"]["review_state"], "not-submitted")
        self.assertIs(PACKET["pilot"]["listing"]["publicly_installable"], False)
        for gate in PACKET["owner_gates"]:
            self.assertIn(gate["status"], {"pending-owner", "pending-external"})
            self.assertTrue(gate["evidence_required"])

    def test_packet_binds_exact_schema_checksum_and_operation(self) -> None:
        contract = PACKET["pilot"]["schema"]
        self.assertEqual(
            hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(), contract["sha256"]
        )
        self.assertEqual(SCHEMA["openapi"], contract["openapi"])
        operation = SCHEMA["paths"][contract["path_template"]][
            contract["method"].lower()
        ]
        self.assertEqual(operation["operationId"], contract["operation_id"])
        self.assertEqual(SCHEMA["servers"], [{"url": "https://api.acedata.cloud"}])
        self.assertNotIn("callback_url", json.dumps(operation))
        self.assertNotIn('"async"', json.dumps(operation))

    def test_review_input_matches_schema_and_is_synchronous(self) -> None:
        pilot = PACKET["pilot"]
        self.assertEqual(pilot["schema"]["execution"], "synchronous")
        self.assertIs(pilot["review_test"]["billable"], True)
        request_schema = SCHEMA["paths"]["/suno/audios"]["post"]["requestBody"][
            "content"
        ]["application/json"]["schema"]
        properties = request_schema["properties"]
        self.assertTrue(set(pilot["review_test"]["input"]).issubset(properties))
        self.assertIn(
            pilot["review_test"]["input"]["model"], properties["model"]["enum"]
        )
        self.assertIn("API token", pilot["review_test"]["never_store"])

    def test_public_urls_are_https_and_campaigns_are_unique(self) -> None:
        metadata = PACKET["pilot"]["public_metadata"]
        campaigns: list[str] = []
        for key, value in metadata.items():
            parsed = urlparse(value)
            self.assertEqual(parsed.scheme, "https", key)
            self.assertEqual(parsed.hostname, "platform.acedata.cloud", key)
            query = parse_qs(parsed.query)
            if key in {"homepage_url", "credential_url", "pricing_url", "support_url"}:
                self.assertEqual(query["utm_source"], ["coze"])
                self.assertEqual(query["utm_medium"], ["plugin"])
                campaigns.extend(query["utm_campaign"])
        self.assertEqual(len(campaigns), len(set(campaigns)))

    def test_evidence_slots_cover_import_auth_outcome_and_measurement(self) -> None:
        slots = {slot["id"]: slot for slot in PACKET["evidence_slots"]}
        self.assertEqual(
            set(slots),
            {
                "owner-channel",
                "schema-import",
                "auth-validation",
                "first-workflow",
                "review",
                "listing",
                "d7-repeat",
                "first-payment",
            },
        )
        self.assertTrue(
            all(
                slot["status"] in {"pending-owner", "pending-external"}
                for slot in slots.values()
            )
        )

    def test_packet_contains_no_secret_or_internal_sourcing_language(self) -> None:
        serialized = json.dumps(PACKET, ensure_ascii=False)
        self.assertIsNone(
            re.search(r"Bearer [A-Za-z0-9_-]{8,}|sk-[A-Za-z0-9_-]{8,}", serialized)
        )
        self.assertIsNone(
            re.search(
                r"upstream|supplier|relay line|上游|供应商|中转线路|逆向线路|后端路由|渠道商",
                serialized,
                re.IGNORECASE,
            )
        )

    def test_runbook_refuses_premature_publication_claims(self) -> None:
        readme = (ROOT / "SUBMISSION.md").read_text()
        for text in (
            "not a published listing",
            "owner-handoff / externally-gated",
            "Do not publish",
            "one billable synchronous request",
            "schema SHA-256",
            "coze.cn or coze.com",
            "Last packet verification: **2026-09-10**",
        ):
            self.assertIn(text, readme)


if __name__ == "__main__":
    unittest.main()
