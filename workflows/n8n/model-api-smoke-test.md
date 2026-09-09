# Model and API smoke test

[`model-api-smoke-test.json`](model-api-smoke-test.json) checks that a selected model appears in the Ace Data Cloud model directory, sends one minimal chat completion, validates the result contract, and returns a structured health report. It uses only built-in n8n nodes and stops explicitly when discovery, visibility, transport, or response validation fails.

Last contract verification: **2026-09-10**.

## Import and setup

1. Download `model-api-smoke-test.json`.
2. In n8n, choose **Import from File**. For CLI validation, run `n8n import:workflow --input=model-api-smoke-test.json` against an isolated n8n user folder/database first.
3. The stable template ID is `acedata-model-api-smoke-test-v1`. An n8n CLI import can overwrite an existing workflow with the same ID; change or remove the ID before importing if you need a separate copy.
4. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-model-api-smoke-test).
5. Create one **Header Auth** credential:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
6. Select that credential separately in **List models with Ace Data Cloud** and **Test completion with Ace Data Cloud**.
7. Edit `model`, `prompt`, or `max_tokens` in **Set smoke test input**, then run the workflow.

The exported workflow contains no credential ID, token, pinned response, or user data. n8n stores credential data separately from the workflow JSON.

## Inputs and checks

| Field | Default | Purpose |
| --- | --- | --- |
| `model` | `claude-sonnet-5` | Exact model ID required in discovery and requested for inference |
| `prompt` | Exact short reply instruction | Keeps the smoke result easy to inspect |
| `max_tokens` | `32` | Bounds the generated response and token consumption |

The workflow first calls `GET https://api.acedata.cloud/v1/models`. It requires all of the following before inference:

- exact HTTP 200;
- `object` equal to `list`;
- `data` as an array whose entries have non-empty string IDs;
- an entry whose ID exactly equals the requested model.

It then calls `POST https://api.acedata.cloud/v1/chat/completions` with the selected model, one user message, `temperature=0`, `stream=false`, and the configured token cap. A successful smoke test requires exact HTTP 200 plus a non-empty completion ID, resolved model, first assistant content, and numeric prompt/completion/total token usage.

## Result and failure boundaries

A successful run returns:

```json
{
  "status": "healthy",
  "checked_at": "2026-09-10T12:00:00.000Z",
  "requested_model": "claude-sonnet-5",
  "resolved_model": "claude-sonnet-5",
  "catalog_count": 96,
  "completion_id": "...",
  "content": "smoke test passed",
  "prompt_tokens": 14,
  "completion_tokens": 4,
  "total_tokens": 18
}
```

The failure branches distinguish:

- model-directory HTTP failure;
- HTTP 200 with a malformed model-directory envelope;
- requested model absent from a valid directory;
- completion HTTP failure;
- HTTP 200 with a completion missing required ID, model, content, or usage fields.

`healthy` means only that model discovery and one completion request passed these checks at `checked_at`. It is not a latency SLA, quality benchmark, multi-region test, or guarantee of future availability.

## Cost and data boundary

- Model discovery is followed by **one billable chat-completion request**. Failed or manually retried executions can add billable requests. Check current pricing before activation.
- The selected model and prompt are sent to the chat-completion API. The directory response, prompt, completion text, identifiers, and usage are present in n8n execution data.
- n8n executions can remain stored according to the instance's retention settings. Configure retention before processing sensitive material.
- Do not place secrets or personal data in the prompt. This smoke test is intentionally narrow; use dedicated monitoring for availability objectives, latency distributions, and broader endpoint coverage.
