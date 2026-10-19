# Search to structured summary (optional HTTP workflow)

[`search-summary.json`](search-summary.json) combines a web search with a short Markdown summary and numbered sources. This advanced example uses built-in n8n nodes for instances that cannot install community packages. For native service discovery and credentials, start with [Google Search](https://github.com/AceDataCloud/GoogleSearchN8N#readme), [Ace Data Cloud Chat Model](https://github.com/AceDataCloud/AceChatN8N#readme), and the [n8n integration guide](https://docs.acedata.cloud/en/integrations/n8n).

This HTTP workflow is a separate importable example. It does not install a native provider or indicate official n8n template approval.

## Import and credentials

1. Download the JSON and choose **Import from File** in n8n. It is inactive and has no credential IDs, tokens, pinned responses, or saved user data.
2. Its stable ID is `acedata-search-summary-v1`. CLI import **can overwrite an existing workflow** with the same ID. Use an isolated user folder/database for validation; change the ID before importing another copy.
3. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=n8n_search_summary_api_key). Sign in or register, find **General application**, and choose **Initialize General Application** if necessary. A dedicated application's key is limited to its service.
4. Copy its API Key, or choose **Keys / Manage Keys → Create** for a separately named key. Review expiration, usage limit and **Allowed APIs**. This workflow needs both SERP search and chat completions; a task-query-only key is insufficient. Check the application's balance and [current model pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=n8n_search_summary_pricing). Trial availability is whatever your account currently displays.
5. Create one n8n **Header Auth** credential with name `Authorization` and value `Bearer <YOUR_API_TOKEN>`. Select it separately in **Search with Ace Data Cloud** and **Summarize with Ace Data Cloud** before running. The token belongs in n8n's credential store. A `platform-...` management token is not an application API key.
6. In **Set research input**, enter the exact chat-completions model ID you have chosen and can use. The exported model field is deliberately empty, so local input validation rejects an unconfigured run before search. Do not choose a model that only supports a different protocol. Model-directory visibility is **not a guarantee** of endpoint compatibility, entitlement, or price.

## Inputs and bounds

| Field | Exported value | Requirement |
| --- | --- | --- |
| `query` | Example research question | Non-blank string, at most 500 characters |
| `number` | `5` | Integer from 1 to 10 |
| `model` | Empty | Exact ID for `/v1/chat/completions`; no automatic model substitution |
| `max_tokens` | `512` | Integer from 32 to 1024; select a model supporting this parameter and `temperature` |

After validation, the workflow sends one `POST /serp/google`. Only HTTP 200 continues. It considers at most 100 organic records, keeps up to `number` usable records, and forwards only their numbered title (200 characters), HTTP(S) link (2048 characters), and snippet (1000 characters). Empty or malformed results stop before the second request.

The second request is one non-streaming `POST /v1/chat/completions`, with the exact selected model, bounded source data, `temperature=0.2`, and `max_tokens`. The system prompt treats source text as untrusted data and asks for citations and uncertainty. This instruction cannot guarantee factual accuracy or resistance to every prompt injection; review the summary and linked evidence before using them.

## Results and failures

Success requires HTTP 200, a non-empty returned model and assistant text, and `finish_reason=stop`. An empty, malformed, truncated, or otherwise unfinished completion stops explicitly. Output contains `status`, `query`, `requested_model`, returned `model`, `summary`, and the same bounded `sources` supplied to the model.

HTTP errors preserve the service's status and body in the error branch. Requests have 60-second search and 120-second chat timeouts. Both nodes explicitly disable **Retry On Fail** and redirects. There is no retry loop, fallback model, or automatic resubmission.

## Cost, data and validation limits

- A complete execution makes **two billable API calls**: one search and one chat request. `max_tokens` limits output; it does not fix the price. A failed or timed-out request may already have incurred usage. Inspect the original execution and [usage history](https://platform.acedata.cloud/console?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=n8n_search_summary_usage) before manually retrying. Rerunning the workflow repeats both requests.
- Search receives the query; chat receives the query and bounded search records. Query, sources, prompts, output, error bodies and identifiers may remain in n8n execution storage. Configure retention and avoid secrets or personal information.
- CI tests the exported JavaScript expressions and failure routes. The pinned n8n 2.43.7 host check imports/exports the workflow and verifies missing-credential failure with container networking disabled. These checks send no service requests and do not demonstrate a completed research run, billing, or registration attribution.

To reproduce the free host check, run the Docker command in [the workflow's CI definition](../../.github/workflows/n8n-search-summary.yml). Do not execute the configured workflow against a real service unless you intend both charges.
