"""The APIs monorepo is the only source of standalone API repository writes."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class MirrorOwnershipTests(unittest.TestCase):
    def test_mirrors_run_after_merge_and_have_no_second_schedule(self):
        path = ROOT / ".github/workflows/sync-to-repos.yml"
        data = yaml.safe_load(path.read_text())
        triggers = data.get("on", data.get(True))
        self.assertEqual(triggers["push"]["branches"], ["main"])
        self.assertNotIn("schedule", triggers)
        self.assertNotIn("repository_dispatch", triggers)
        self.assertIn("--delete", path.read_text())
        self.assertIn("sync.yaml", path.read_text())

    def test_no_legacy_agent_dispatch_listener_remains(self):
        self.assertFalse((ROOT / ".github/workflows/sync-from-docs.yml").exists())

    def test_trial_concurrency_guidance_is_in_public_mirror_readmes(self):
        mappings = yaml.safe_load((ROOT / "sync.yaml").read_text())["mappings"]
        paths = [ROOT / "README.md"] + [
            ROOT / directory / "README.md"
            for directory in mappings
            if directory not in {"sora", "face"}
        ]
        for path in paths:
            with self.subTest(readme=path.relative_to(ROOT)):
                text = path.read_text()
                guidance = text.split("## Trial account concurrency\n\n", 1)[1].split("\n## ", 1)[0]
                for requirement in (
                    "neither a successful paid top-up nor an administrator's manual credit addition",
                    "one billable request at a time across the entire account",
                    "shared by all API keys and services",
                    "Rewards, redemption cards and transferred credits do not count as paid top-ups",
                    "removes this trial restriction; balance and key usage-limit checks still apply",
                    "429 too_many_requests",
                    "Wait for the active request's final result",
                    "Free task polling remains available",
                    "acceptance or a task ID is not completion",
                    "keep querying the same task",
                    "disconnect or proxy timeout does not mean execution stopped",
                    "contact support with `trace_id`",
                    "changes neither trial API availability nor pricing",
                    "fees are settled after execution based on actual usage",
                ):
                    self.assertIn(requirement, guidance)

    def test_trial_limit_does_not_redefine_realtime_billing(self):
        for path in (ROOT / "README.md", ROOT / "openai/README.md"):
            with self.subTest(readme=path.relative_to(ROOT)):
                self.assertIn(
                    "Realtime connection authentication does not occupy this ordinary-request slot "
                    "and retains its existing per-turn billing",
                    path.read_text(),
                )
        self.assertIn("read-only user flag `has_recharged`", (ROOT / "README.md").read_text())
        self.assertIn("it is not a request parameter", (ROOT / "README.md").read_text())
        self.assertNotIn("No Rate Limits", (ROOT / "openai/README.md").read_text())

    def test_suno_replacement_guide_uses_local_lyrics_and_checks_audio(self):
        import json
        text = (ROOT / 'suno/docs/suno_audios_generation_api_integration_guide.md').read_text()
        section = text.split('## Replace Section\n', 1)[1].split('\n## ', 1)[0]
        request = json.loads(section.split('```json\n', 1)[1].split('\n```', 1)[0])
        self.assertEqual('replace_section', request['action'])
        self.assertEqual('YOUR_COMPLETED_AUDIO_ID', request['audio_id'])
        self.assertEqual(request['lyric'], request['prompt'])
        self.assertEqual('full_song', request['replace_section_result_mode'])
        self.assertTrue(request['async'])
        self.assertLess(request['replace_section_start'], request['replace_section_end'])
        self.assertNotIn('"success":', section)
        for requirement in ('response.data', 'Listen to both', 'not an audio transcript',
                            'does not mean equal length', 'recheck its duration and interval',
                            'already concatenated', 'cannot lock replacement length'):
            self.assertIn(requirement, section)
        for filename, fee in (
            ('suno_audios_generation_api_integration_guide.md', '0.56 Credits'),
            ('suno_lyrics_generation_api_integration_guide.md', '0.08 Credits'),
            ('suno_voices_api_integration_guide.md', '0.15 Credits'),
        ):
            guide = (ROOT / 'suno/docs' / filename).read_text()
            self.assertIn(fee, guide)
            self.assertIn('failed requests are not charged', guide)


if __name__ == "__main__":
    unittest.main()
