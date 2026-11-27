# Copilot Sync Instructions for AceDataCloud APIs

## Repository Structure

This is a monorepo with one API documentation package per subdirectory (e.g., `suno/`, `luma/`, `flux/`).

## Source of Truth

The **AceDataCloud/PlatformBackend** commit linked in the sync PR is authoritative:

- `docs/` — customer guides and examples
- `openapi/` and service mappings — public request/response contracts
- Public document/catalog visibility — whether a capability may be advertised

Published Docs is a reference. The daily Backend controller owns sync PRs;
there is no Docs dispatch or automatic Copilot issue-assignment workflow.

## What to Sync

Use the exact Backend commit range linked in the sync PR. When that snapshot changes, compare the OpenAPI specs against the API docs and update:

1. **API endpoints** — ensure all paths from OpenAPI specs are documented
2. **Request/response examples** — match OpenAPI request body and response schemas
3. **Parameter descriptions** — update to match OpenAPI parameter descriptions
4. **Authentication requirements** — reflect any auth changes

## Rules

- Do NOT modify CI/CD workflows or sync.yaml
- Each subdirectory is independent — only update directories for changed services
- Keep examples accurate and runnable

- Keep changes incremental; do not copy the Backend guide tree.
- Standalone API repos are mirrors of this monorepo.

## API README structure

- Link customer documentation to verified `https://platform.acedata.cloud/documents/<alias>` pages, using `lang=en` or `lang=zh-cn`. Use the public Document alias rather than replacing a documentation host mechanically.
- Keep the API key steps illustrated with the existing redacted General Application and Create New Credential screenshots. Place each image beside the step it explains and link the platform API key guide.

- Write service landing READMEs in English Markdown. Link the existing Chinese guide for Chinese readers.
- Lead with the API purpose, current pricing and a direct Applications link. Put a valid minimal request immediately after the short API key steps.
- Match required fields, model IDs, endpoints and result paths to the pinned Backend contract. Include a successful response shape and, for asynchronous operations, query the original task through its terminal state.
- Keep detailed API guides and service-specific limitations accessible after the Quickstart. Preserve current billing and trial-concurrency information there.
- Keep website HTML/CSS in the website introduction source. Do not embed full landing-page markup or keyword lists into README files.
- Preserve the first-call structure when applying incremental capability updates.
