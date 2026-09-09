# Pipedream submission packet

This directory is an owner handoff for proposing an Ace Data Cloud app and a deliberately narrow first set of Pipedream components. It is not a published integration, an accepted partner application, or evidence of Pipedream review.

Last contract and registry check: **2026-09-10**.

## Current gate

`submission-packet.json` is `app-request-required`. A read-only check of the Pipedream registry tree found no matching Ace Data Cloud app directory on 2026-09-10. Pipedream's contribution guide says a missing app must first be requested so Pipedream can create the registry directory. The owner must obtain the confirmed app slug and authentication schema before component implementation or submission.

Do not run `pd publish`, open a registry PR, send credentials, or claim marketplace availability from this repository. Those are external actions and require separate approval.

## Proposed first release: 3 sources + 3 actions

### Polling sources

| Source | Endpoint | Emit rule |
| --- | --- | --- |
| New Wan Video Task Completed | `POST /wan/tasks` | Configured task has numeric `finished_at` |
| New Suno Music Task Completed | `POST /suno/tasks` | Configured task has numeric `finished_at` |
| New Flux Image Task Completed | `POST /flux/tasks` | Configured task has numeric `finished_at` |

These are polling sources, not webhooks. Each requires 1–50 user-supplied task IDs and calls `retrieve_batch` every 15 minutes by default. The public task contracts do not promise an unfiltered “list all of my tasks” operation, so a source must not omit `taskIds` or imply account-wide coverage.

Implementation requirements:

- ESM `.mjs` components in the Pipedream-assigned app directory, initial version `0.0.1`, with a README and scrubbed static test event per source.
- Standard `timer` and `db` props plus the app prop and a required `taskIds` string array capped at 50.
- `dedupe: "unique"`; event ID `<service>:<task.id>:<task.finished_at>`; useful summary and timestamp metadata.
- Initial run emits at most the 50 configured tasks and only when `finished_at` is numeric. Later runs emit only unseen terminal task versions.
- Exponential backoff for HTTP 429 and actionable errors for every non-2xx response.
- Emit only `id`, `type`, `created_at`, `started_at`, `finished_at`, `elapsed`, and `response`. Do not emit user, application, authorization, or credential metadata returned by the task record.
- Confirm scheduled polling and deduplication with repeated **RUN NOW** executions before opening the registry PR.

### Actions

| Action | Stage | Endpoint | Required inputs |
| --- | --- | --- | --- |
| Search Google | Production | `POST /serp/google` | `query` |
| Create Chat Completion | Beta | `POST /v1/chat/completions` | `model`, `messages` |
| Generate Flux Image | Production | `POST /flux/images` | `prompt`, `size`; component fixes `action=generate`, `async=false` |

Implementation requirements:

- Use the app prop for managed authentication and `axios` from `@pipedream/platform`.
- Expose the packet's required/optional fields with clear labels. Keep chat `stream=false`; the first release must return a normal JSON value rather than a stream.
- Return the API response object and export a short `$summary`; wrap API errors with status, trace ID when present, and a user-actionable message without exposing the token.
- Apply the packet's `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations.
- Keep each action narrow. Do not add a generic request proxy or undocumented fields.
- Test each action in a private workflow with a dedicated test account before registry submission.

## Authentication and test account

Proposed app authentication:

- auth type: API key;
- secret field: `api_token`;
- request header: `Authorization: Bearer <api_token>`;
- connection check: `GET https://api.acedata.cloud/v1/models`, requiring HTTP 200, `object=list`, and a `data` array.

The API token must be stored only in Pipedream's connected-account secret field. Never commit it, put it in a component prop default, sample event, fixture, issue, PR body, log, or screenshot.

Before external submission, the owner should provision a dedicated test account with:

1. no production user data;
2. only enough funded balance to exercise the three actions and polling tests;
3. a separately revocable API token;
4. an owner and expiry date recorded internally;
5. delivery to Pipedream only through the secure channel Pipedream approves.

The packet intentionally contains no token or credential ID.

## Cost and data boundary

- Search, chat completion, and image generation may be billable according to current pricing. Each **Create Chat Completion** action execution sends one billable chat-completion request. Polling and retries also create API requests; validate current billing before enabling scheduled sources.
- Search queries, chat messages, image prompts, configured task IDs, generated results, and task responses pass through Pipedream and may remain in workflow event/execution history under the user's Pipedream retention settings.
- Source allowlisting removes account and credential metadata from emitted events, but generated content can still contain sensitive material supplied by the user.
- Public references for reviewers:
  - [Privacy policy](https://platform.acedata.cloud/privacy)
  - [Terms](https://platform.acedata.cloud/terms)
  - [Support](https://platform.acedata.cloud/support?utm_source=pipedream&utm_medium=integration&utm_campaign=pipedream-support)
  - [Create an API token](https://platform.acedata.cloud/console/credentials?utm_source=pipedream&utm_medium=integration&utm_campaign=pipedream-auth-setup)

## Owner checklist

### Gate A — app and auth

- [ ] Request the missing app through Pipedream Support or the process Pipedream directs.
- [ ] Receive a Pipedream-created registry app directory and confirmed slug.
- [ ] Confirm API-key auth storage, header injection, and connection-test behavior with Pipedream.
- [ ] Provide logo/brand assets in the format Pipedream requests; do not infer requirements absent from their response.
- [ ] Record the request URL and reviewer/owner internally.

### Gate B — implementation and verification

- [ ] Implement exactly the three sources and three actions in `PipedreamHQ/pipedream` using the assigned slug.
- [ ] Add component READMEs, scrubbed source test events, shared request helpers, 429 backoff, and actionable errors.
- [ ] Validate every endpoint/method/field against the API IDs in `submission-packet.json`.
- [ ] Use the dedicated test account; test invalid auth, 429 handling, malformed/non-2xx errors, normal responses, source dedupe, and initial-event cap.
- [ ] Confirm source events exclude user/application/authorization/credential metadata.
- [ ] Run the registry's current lint/test commands from the contribution environment and save output.

### Gate C — external review and publication

- [ ] Obtain separate authorization to open the external registry PR.
- [ ] Open the PR against Pipedream's required base with the six components and no credentials.
- [ ] Address Pipedream review; record the PR URL, final commit, checks, and reviewer outcome.
- [ ] After Pipedream merges and publishes, verify the public app plus all six component pages using a fresh connected account.
- [ ] Only then change the internal status from externally gated to implemented and record the public URLs.

## Acceptance evidence

The integration is complete only when the owner has all of the following:

- confirmed Pipedream app slug and auth configuration;
- registry PR and merged commit URLs;
- green registry checks;
- sanitized test evidence for all six components;
- public app URL and six public component URLs;
- fresh connected-account proof that each component runs;
- support/privacy/terms links visible in the final listing;
- attribution campaigns preserved exactly as listed in the packet.

Until then, the accurate status is **owner-handoff / externally-gated**.

## Official Pipedream references

- [Apps](https://pipedream.com/docs/apps)
- [Registry contributions](https://pipedream.com/docs/components/contributing)
- [Source development](https://pipedream.com/docs/components/contributing/sources-quickstart)
- [Action development](https://pipedream.com/docs/components/contributing/actions-quickstart)
- [Component guidelines](https://pipedream.com/docs/components/contributing/guidelines)
