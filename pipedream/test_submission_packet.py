from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
PACKET = json.loads((ROOT / "submission-packet.json").read_text())


class PipedreamSubmissionPacketTest(unittest.TestCase):
    def test_packet_is_explicitly_external_gated(self) -> None:
        self.assertEqual(PACKET["schema_version"], 1)
        self.assertEqual(PACKET["status"], "app-request-required")
        self.assertEqual(PACKET["verified_at"], "2026-09-10")
        gates = PACKET["owner_gates"]
        self.assertEqual(len(gates), 6)
        self.assertEqual(len({gate["id"] for gate in gates}), len(gates))
        self.assertTrue(all(gate["status"] in {"pending-owner", "pending-external"} for gate in gates))
        self.assertTrue(all(gate["evidence_required"] for gate in gates))

    def test_app_auth_uses_managed_secret_and_read_only_verification(self) -> None:
        app = PACKET["app"]
        self.assertEqual(app["requested_slug"], "ace_data_cloud")
        self.assertEqual(app["base_url"], "https://api.acedata.cloud")
        auth = app["auth"]
        self.assertEqual(auth["type"], "api_key")
        self.assertEqual(auth["secret_field"], "api_token")
        self.assertEqual(auth["header_name"], "Authorization")
        self.assertEqual(auth["header_template"], "Bearer {{api_token}}")
        self.assertEqual(
            auth["verification"],
            {
                "method": "GET",
                "path": "/v1/models",
                "expected_status": 200,
                "expected_shape": {"object": "list", "data": "array"},
            },
        )

    def test_public_urls_are_https_and_campaigns_are_unique(self) -> None:
        app = PACKET["app"]
        for field in ("homepage_url", "credential_url", "privacy_url", "terms_url", "support_url"):
            parsed = urlparse(app[field])
            self.assertEqual(parsed.scheme, "https")
            self.assertEqual(parsed.hostname, "platform.acedata.cloud")

        campaigns = [item["campaign"] for item in PACKET["sources"] + PACKET["actions"]]
        self.assertEqual(len(campaigns), 6)
        self.assertEqual(len(set(campaigns)), len(campaigns))
        for field in ("homepage_url", "credential_url", "support_url"):
            query = parse_qs(urlparse(app[field]).query)
            self.assertEqual(query["utm_source"], ["pipedream"])
            self.assertEqual(query["utm_medium"], ["integration"])
            self.assertEqual(len(query["utm_campaign"]), 1)

    def test_sources_are_three_bounded_polling_components(self) -> None:
        sources = PACKET["sources"]
        self.assertEqual(len(sources), 3)
        expected = {
            "25e349c9-a490-4ae5-9a96-e5952d2dbcf7": "/wan/tasks",
            "f1143f0b-8146-4fc0-b02c-ac8db969392d": "/suno/tasks",
            "4f36fc31-5a95-42ac-abfc-34670c40238c": "/flux/tasks",
        }
        self.assertEqual({source["api_id"]: source["path"] for source in sources}, expected)
        self.assertEqual(len({source["key"] for source in sources}), 3)
        for source in sources:
            self.assertEqual(source["type"], "polling")
            self.assertEqual(source["stage"], "Production")
            self.assertEqual(source["method"], "POST")
            self.assertEqual(source["request"], {"action": "retrieve_batch", "ids_from_prop": "taskIds"})
            self.assertEqual(source["required_props"], ["timer", "taskIds"])
            self.assertEqual(source["max_task_ids"], 50)
            self.assertEqual(source["default_interval_seconds"], 900)
            self.assertEqual(source["initial_event_cap"], 50)
            self.assertEqual(source["rate_limit_policy"], "exponential-backoff-on-429")
            self.assertEqual(source["completion_test"], "typeof task.finished_at === 'number'")
            self.assertEqual(source["dedupe"], "unique")
            self.assertIn("${task.id}", source["event_id"])
            self.assertIn("${task.finished_at}", source["event_id"])
            self.assertEqual(
                source["annotations"],
                {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
            )

    def test_source_event_allowlist_excludes_account_and_credential_metadata(self) -> None:
        expected = ["id", "type", "created_at", "started_at", "finished_at", "elapsed", "response"]
        forbidden = {
            "user_id",
            "actor_user_id",
            "api_id",
            "application_id",
            "credential_id",
            "authorization_id",
            "trace_id",
            "request",
        }
        for source in PACKET["sources"]:
            self.assertEqual(source["event_allowlist"], expected)
            self.assertTrue(forbidden.isdisjoint(source["event_allowlist"]))

    def test_actions_match_narrow_public_contracts(self) -> None:
        actions = {action["key"]: action for action in PACKET["actions"]}
        self.assertEqual(len(actions), 3)
        expected = {
            "ace_data_cloud-search-google": {
                "api_id": "7753ed09-1046-46d3-ad80-cd7ff19676b5",
                "path": "/serp/google",
                "stage": "Production",
                "required_fields": ["query"],
            },
            "ace_data_cloud-create-chat-completion": {
                "api_id": "6b2b437b-b6d5-466c-8750-b16650072593",
                "path": "/v1/chat/completions",
                "stage": "Beta",
                "required_fields": ["model", "messages"],
            },
            "ace_data_cloud-generate-flux-image": {
                "api_id": "deefc5d7-7f22-43e9-929e-f2b6afee60b7",
                "path": "/flux/images",
                "stage": "Production",
                "required_fields": ["action", "prompt", "size"],
            },
        }
        for key, contract in expected.items():
            action = actions[key]
            self.assertEqual(action["method"], "POST")
            for field, value in contract.items():
                self.assertEqual(action[field], value)
            self.assertEqual(action["annotations"]["destructiveHint"], False)
            self.assertEqual(action["annotations"]["openWorldHint"], True)
        self.assertEqual(actions["ace_data_cloud-create-chat-completion"]["fixed_fields"], {"stream": False})
        self.assertEqual(
            actions["ace_data_cloud-generate-flux-image"]["fixed_fields"],
            {"action": "generate", "async": False},
        )

    def test_packet_contains_no_secret_or_internal_sourcing_language(self) -> None:
        serialized = json.dumps(PACKET, ensure_ascii=False)
        self.assertIsNone(
            re.search(
                r"(?:^|[^A-Za-z0-9])(?:sk-|Bearer [A-Za-z0-9_-]{8,}|api[_-]?key\s*[:=]\s*[A-Za-z0-9_-]{8,})",
                serialized,
                re.IGNORECASE,
            )
        )
        self.assertIsNone(
            re.search(r"upstream|supplier|relay line|上游|供应商|中转线路|逆向线路|后端路由|渠道商", serialized, re.IGNORECASE)
        )

    def test_runbook_states_scope_data_cost_and_irreversible_gates(self) -> None:
        readme = (ROOT / "README.md").read_text()
        for text in (
            "not a published integration",
            "app-request-required",
            "3 sources + 3 actions",
            "polling sources, not webhooks",
            "1–50 user-supplied task IDs",
            "Exponential backoff for HTTP 429",
            "Do not emit user, application, authorization, or credential metadata",
            "one billable chat-completion request",
            "no token or credential ID",
            "separate authorization to open the external registry PR",
            "owner-handoff / externally-gated",
            "Last contract and registry check: **2026-09-10**",
        ):
            self.assertIn(text, readme)

    def test_official_references_are_allowlisted_https_urls(self) -> None:
        expected = {
            "https://pipedream.com/docs/apps",
            "https://pipedream.com/docs/components/contributing",
            "https://pipedream.com/docs/components/contributing/sources-quickstart",
            "https://pipedream.com/docs/components/contributing/actions-quickstart",
            "https://pipedream.com/docs/components/contributing/guidelines",
        }
        self.assertEqual(set(PACKET["official_references"]), expected)
        self.assertTrue(all(urlparse(url).hostname == "pipedream.com" for url in expected))


if __name__ == "__main__":
    unittest.main()
