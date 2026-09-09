# Coze Suno pilot owner handoff

This packet prepares one bounded, synchronous Suno OpenAPI pilot for owner review. It is **not a published listing**, submission receipt, Coze review, or proof that a public plugin is currently installable. Until every external evidence slot is complete, its status is **owner-handoff / externally-gated**.

Last packet verification: **2026-09-10**.

## Why one pilot

The first submission uses `coze/suno.yaml` and its single `generateMusic` operation. Keeping one outcome and one operation makes authentication, cost, result shape, attribution, and rollback auditable before any broader catalog work.

The packet binds the exact source revision and schema SHA-256. If `coze/suno.yaml` changes, validation fails until the owner deliberately reviews the new contract and updates the checksum.

## Owner decisions

Before any external action, the accountable owner must:

1. choose **coze.cn or coze.com** and record why that region is appropriate;
2. identify the publisher account, publishing authority, operational owner, and rollback owner;
3. provision a revocable, least-privilege funded test token without committing or pasting it into repository artifacts;
4. confirm current Coze import, auth, privacy, support, and review requirements in the chosen region;
5. obtain separate authorization for submission.

Do not publish, submit a review form, edit a live listing, or transmit credentials based only on this packet.

## Import and auth check

1. Verify the current file checksum matches `pilot.schema.sha256` in `submission-packet.json`.
2. Import `coze/suno.yaml` into a private draft plugin.
3. Configure HTTP Bearer authentication as a managed Coze service credential.
4. Confirm an invalid token fails without exposing the token in the response, logs, screenshots, or issue text.
5. Run the packet's minimal private test as **one billable synchronous request**. Check current pricing before execution.
6. Save only timestamp, schema checksum, target channel, sanitized response shape, status, and trace ID.

A successful response must have HTTP 200, `success=true`, a non-empty `data` array, at least one HTTPS `audio_url`, and a non-empty `trace_id`. Do not store generated media or prompts beyond the reviewer evidence policy unless the owner has approved that retention.

## External review and rollback

- Keep listing ID, listing URL, and review state unresolved until Coze supplies them.
- Record the exact submitted schema checksum and submission receipt.
- After approval, install from a fresh account and repeat the managed-credential workflow before marking the listing installable.
- If behavior differs from the checked-in schema, withdraw or disable the draft/listing under the chosen account's rollback procedure; do not silently edit the live definition.
- Record privacy-safe D7 repeat and attributed first-payment evidence only after real usage exists. Packet presence is not conversion evidence.

## Acceptance evidence

Completion requires all eight evidence slots in `submission-packet.json`: owner/channel, schema import, auth validation, first workflow, review, public listing, D7 repeat, and first payment. Each must retain an immutable reference without secrets or raw credentials.
