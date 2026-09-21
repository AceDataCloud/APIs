# Search to structured summary

[`search-summary.json`](search-summary.json) turns one research question into a grounded Markdown report:

1. search the web with `POST https://api.acedata.cloud/serp/google`;
2. stop with the returned HTTP status and body when search fails;
3. keep the first configured organic results and build a source-bounded prompt;
4. summarize them with `POST https://api.acedata.cloud/v1/chat/completions`;
5. stop with the returned HTTP status and body when summarization fails;
6. return `status`, `query`, `model`, `summary`, and the source records.

Last contract verification: **2026-09-10**.

## Import and setup

1. Download `search-summary.json`.
2. In n8n, choose **Import from File**. For CLI import, run `n8n import:workflow --input=search-summary.json` against an isolated n8n user folder/database first.
3. The stable template ID is `acedata-search-summary-v1`. An n8n CLI import can overwrite an existing workflow with the same ID; change or remove the ID before importing if you need a separate copy.
4. [Create an Ace Data Cloud API token](https://platform.acedata.cloud/?utm_source=n8n&utm_medium=workflow&utm_campaign=n8n-search-summary).
5. Create one **Header Auth** credential:
   - Name: `Authorization`
   - Value: `Bearer <YOUR_API_TOKEN>`
6. Select that credential separately in both HTTP Request nodes.
7. Edit `query`, `number`, or `model` in **Set research input**, then run the workflow.

The exported workflow contains no credential ID, token, pinned response, or user data. n8n stores credential data separately from the workflow JSON.

## Inputs

| Field | Default | Contract |
| --- | --- | --- |
| `query` | `How can teams use MCP for AI automation?` | Non-empty search query |
| `number` | `5` | SERP supports 1–100; this value also bounds sources sent to the model |
| `model` | `claude-sonnet-5` | Must remain in the chat completions model enum |

## Output and failure behavior

A successful run returns:

```json
{
  "status": "success",
  "query": "...",
  "model": "claude-sonnet-5",
  "summary": "## Key findings ...",
  "sources": [{"title": "...", "link": "https://...", "snippet": "..."}]
}
```

Both HTTP nodes request the full response and treat non-2xx responses as data so the following IF node can inspect `statusCode`. Only HTTP 200 continues. Search and chat failures terminate explicitly with the status and response body; the chat node has a 120-second request timeout.

## Cost and data boundary

- A complete run makes **two billable API calls**: one SERP request and one chat-completions request. Failed or retried executions can add calls. Check current pricing before activation.
- The search query is sent to the search API. The query plus up to `number` organic result titles, links, and snippets are sent to the selected chat model.
- Do not send secrets, personal data, or content you are not authorized to process.
- The model is instructed to use only supplied results, but generated summaries still require review before publication or decisions.
