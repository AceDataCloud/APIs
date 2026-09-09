#!/usr/bin/env python3
from __future__ import annotations

import unittest

from check_suno_onboarding import README, validate_text


class SunoOnboardingValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = README.read_text()
        cls.docs_dir = README.parent / "docs"

    def errors_for(self, text: str) -> str:
        return "\n".join(validate_text(text, self.docs_dir))

    def test_canonical_readme_is_valid(self) -> None:
        self.assertEqual(validate_text(self.text, self.docs_dir), [])

    def test_duplicate_quick_start_and_invalid_service_url_fail(self) -> None:
        changed = self.text.replace(
            "## Why Use Suno Music Generation on Ace Data Cloud",
            "## Quick Start\n\nhttps://platform.acedata.cloud/service/suno\n\n"
            "## Why Use Suno Music Generation on Ace Data Cloud",
        )
        errors = self.errors_for(changed)
        self.assertIn("expected one Quick Start heading, found 2", errors)
        self.assertIn("found invalid service URL", errors)

    def test_missing_safe_boundary_and_paid_warning_fail(self) -> None:
        changed = self.text.replace(
            "{\"items\":[],\"count\":0}",
            "{\"success\":true}",
        ).replace(
            "POST /suno/audios` is a paid generation operation",
            "POST /suno/audios` generates music",
        )
        errors = self.errors_for(changed)
        self.assertIn("missing empty batch success", errors)
        self.assertIn("missing paid boundary", errors)

    def test_legacy_tokens_and_uuid_links_fail(self) -> None:
        changed = self.text + (
            "\n[$t(old_title)](https://platform.acedata.cloud/documents/"
            "4da95d9d-7722-4a72-857d-bf6be86036e9)\n"
        )
        errors = self.errors_for(changed)
        self.assertIn("found unresolved translation token", errors)
        self.assertIn("found legacy UUID document URL", errors)

    def test_raw_html_fence_and_unclosed_html_fail(self) -> None:
        changed = self.text.replace(
            ".tag-item {", ".tag-item\n```css\n{", 1
        ).replace("</section>", "", 1)
        errors = self.errors_for(changed)
        self.assertIn("code fence leaked into raw HTML", errors)
        self.assertIn("unclosed code fence", errors)
        self.assertRegex(errors, r"expected </|unclosed <")

    def test_commonmark_fence_variants_inside_html_fail(self) -> None:
        for fence in ("   ```css", "  ~~~css"):
            with self.subTest(fence=fence):
                changed = self.text.replace(
                    ".tag-item {", f".tag-item\n{fence}\n{{", 1
                )
                self.assertIn("code fence leaked into raw HTML", self.errors_for(changed))

    def test_markdown_html_like_text_after_raw_fragment_is_allowed(self) -> None:
        changed = self.text.replace(
            "</div>\n\n## APIs and Guides",
            "</div>\n\n<https://docs.acedata.cloud>\n\n"
            "```text\n<task-id>\n```\n\n## APIs and Guides",
            1,
        )
        self.assertEqual(validate_text(changed, self.docs_dir), [])

    def test_guide_inventory_drift_fails(self) -> None:
        changed = self.text.replace(
            "(docs/suno_wav_api_integration_guide.md)",
            "(docs/not_checked_in.md)",
        )
        errors = self.errors_for(changed)
        self.assertIn("missing guide links: docs/suno_wav_api_integration_guide.md", errors)
        self.assertIn("unexpected guide links: docs/not_checked_in.md", errors)
        self.assertIn("missing contract row for POST /suno/wav", errors)


if __name__ == "__main__":
    unittest.main()
