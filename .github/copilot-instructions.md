# Copilot Sync Instructions for AceDataCloud APIs

## Repository Structure

This is a monorepo with one API documentation package per subdirectory (e.g., `suno/`, `luma/`, `flux/`).

## Source of Truth

The **AceDataCloud/Docs** repo is the source of truth:

- `openapi/<service>.json` — OpenAPI specs for each service
- `guides/<service>.md` — Usage guides

## What to Sync

When the Docs repo changes, compare the OpenAPI specs against the API docs and update:

1. **API endpoints** — ensure all paths from OpenAPI specs are documented
2. **Request/response examples** — match OpenAPI request body and response schemas
3. **Parameter descriptions** — update to match OpenAPI parameter descriptions
4. **Authentication requirements** — reflect any auth changes

## Rules

- Do NOT modify CI/CD workflows or sync.yaml
- Each subdirectory is independent — only update directories for changed services
- Keep examples accurate and runnable
