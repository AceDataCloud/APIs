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
