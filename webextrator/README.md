# WebExtrator API

Extract readable Markdown and structured content from web pages through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/webextrator/webextrator_extract) · [Models and pricing](https://platform.acedata.cloud/services/webextrator?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/webextrator/webextrator_extract)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/webextrator/extract \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "url": "https://docs.acedata.cloud/en/quickstart"
}'
```

Read `data.markdown` from the response. The following fields illustrate a successful result.

```json
{
  "success": true,
  "data": {
    "markdown": "# Quickstart\n\nStart your first API request."
  }
}
```

## Endpoints

| Path | Purpose | Cost (Credits) | Guide |
|---|---|---|---|
| `POST /webextrator/render` | Headless Chromium render, returns raw HTML + text + title | 0.005 | [Render API guide](docs/webextrator_render_api_integration_guide.md) |
| `POST /webextrator/extract` | Render + structured extraction (schema.org + LLM types) | 0.005 | [Extract API guide](docs/webextrator_extract_api_integration_guide.md) |
| `POST /webextrator/tasks` | Look up historical render / extract tasks (7-day retention) | Free | [Tasks API guide](docs/webextrator_tasks_api_integration_guide.md) |

Pricing as of May 2026. Service is metered in Credits via your AceDataCloud
account; cache hits are still billed at the configured rate to keep cost
predictable.

---

## When to use which

| You want… | Use | Why |
|---|---|---|
| Bypass JS rendering and read the final HTML / text | `/webextrator/render` | Single Patchright navigation, no extraction work |
| Pull article / product / video / recipe / job metadata from a real-world URL | `/webextrator/extract` | schema.org mapper covers ~60 % of the long tail with zero LLM cost; LLM fills the rest |
| Convert a page to clean markdown for downstream LLM input | `/webextrator/extract` | Returns Turndown-converted markdown + readability text in addition to structured payload |
| Look up a result you got via async / callback mode | `/webextrator/tasks` | Retrieves the full envelope by `task_id` or `trace_id` |

---

## How extraction works

The Extract API is a **three-tier pipeline**:

1. **schema.org JSON-LD mapper** *(deterministic, zero LLM cost)*.
   If the page ships `<script type="application/ld+json">` blocks (Wikipedia,
   BestBuy, AllRecipes, YouTube, most news sites, most product pages), the
   mapper walks `@graph` containers and `@type` arrays and emits a typed entity
   for `Article` / `Product` / `Recipe` / `VideoObject` / `Event` / `JobPosting`
   / `FAQPage`, plus a `BreadcrumbList`.

2. **LLM-first typed extractor** *(only when schema.org returned nothing)*.
   Triggered by `enable_llm: true`. Detects the page kind from URL heuristics
   (or your `expected_type` hint) and asks the model for a strict JSON payload
   validated against a Zod schema. Schemas:
   `article` / `product` / `discussion` / `recipe` / `video` / `job`. Failures
   surface as `structured.llmError` and never crash the request.

3. **Readability + markdown fallback** *(always runs)*.
   Mozilla Readability for clean text, Turndown for markdown, OG / `<meta>`
   tags for title / description / image / site_name. These populate the
   top-level fields whenever schema.org and the LLM didn't.

URL repetition? **Step 0 is the Redis result cache** — identical requests
return in <1 ms regardless of the pipeline behind them. See the Extract guide
for `bypass_cache` and `cache_ttl_seconds`.

---

## SDKs and Tooling

- **HTTP / cURL** — examples in every guide.
- **Python** — `requests` examples in every guide.
- **Node.js** — `fetch` examples in every guide.
- **Webhooks** — `callback_url` is supported on all three endpoints for async
  job completion notifications.

---

## API Reference

| API | Path | Integration guide |
|---|---|---|
| WebExtrator Render API | `/webextrator/render` | [Render API integration guide](docs/webextrator_render_api_integration_guide.md) |
| WebExtrator Extract API | `/webextrator/extract` | [Extract API integration guide](docs/webextrator_extract_api_integration_guide.md) |
| WebExtrator Tasks API | `/webextrator/tasks` | [Tasks API integration guide](docs/webextrator_tasks_api_integration_guide.md) |

## Troubleshooting

- For authentication errors, check the copied API key, service access, expiration and configured usage limits. [API key guide](https://docs.acedata.cloud/en/authentication)
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
