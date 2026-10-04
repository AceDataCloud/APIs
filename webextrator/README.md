# WebExtrator API

WebExtrator is Ace Data Cloud's web rendering and intelligent content extraction
service. Give it a URL and get back either the fully-rendered HTML (`render`) or
a typed structured payload (`extract`) — Article / Product / Recipe / Video /
Discussion / Job — all behind a single `Authorization: Bearer` API key.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square)
![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square)
![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud — WebExtrator](https://platform.acedata.cloud/service/webextrator)

Keywords: web extract api, web scraping api, headless chromium, schema.org
mapper, structured content extraction, llm extraction, content type detection,
patchright, readability, web rendering, ai api, rest api, developer tools,
Ace Data Cloud

---

## Why WebExtrator on Ace Data Cloud

- **Three-layer extraction pipeline** — deterministic schema.org JSON-LD
  mapper first; LLM type-aware extractor (Article / Product / Recipe / Video /
  Discussion / Job) for sites without structured data; result cache (Redis)
  collapses duplicate URLs to <1 ms.
- **Real headless Chromium via Patchright** — bypasses simple bot checks out of
  the box, supports custom UA / cookies / headers / wait conditions.
- **Synchronous and asynchronous modes** — get a result inline in seconds, or
  fire-and-forget with a callback URL and retrieve later via the Tasks API.
- **Production-grade auth and billing** — one API key, one bill, usage tracked
  per request via the standard AceDataCloud platform.
- **Free quota for new users** — try the service before you commit.

---

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

## Quick Start

### 1. Render a page

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "wait_until": "networkidle",
    "block_resources": ["image", "media", "font"]
  }'
```

### 2. Extract typed content

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "expected_type": "article"
  }'
```

Response (trimmed) — the `structured.schemaOrg.primary` block is the typed
payload, and `description / byline / publishedAt` are back-filled from it:

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": 1777717800.123,
  "finished_at": 1777717802.535,
  "elapsed": 2.412,
  "data": {
    "kind": "extract",
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "finalUrl": "https://en.wikipedia.org/wiki/Diffbot",
    "contentType": "article",
    "title": "Diffbot",
    "description": "American machine learning and knowledge management company",
    "byline": "Contributors to Wikimedia projects",
    "publishedAt": "2007-08-08T05:47:27Z",
    "language": "en",
    "images": ["https://en.wikipedia.org/static/images/icons/enwiki-25.svg"],
    "links": ["https://en.wikipedia.org/wiki/Machine_learning"],
    "markdown": "# Diffbot\n\nDiffbot is a developer of machine learning ...",
    "text": "Diffbot is a developer of machine learning algorithms ...",
    "structured": {
      "schemaOrg": {
        "primary": {
          "kind": "article",
          "subtype": "Article",
          "headline": "American machine learning and knowledge management company",
          "datePublished": "2007-08-08T05:47:27Z",
          "dateModified": "2025-07-10T20:42:45Z",
          "author": { "name": "Contributors to Wikimedia projects", "type": "Organization" },
          "publisher": { "name": "Wikimedia Foundation, Inc." }
        },
        "breadcrumbs": [],
        "all": [ /* ... */ ]
      },
      "openGraph": { /* ... */ },
      "jsonLd": [ /* raw passthrough */ ]
    },
    "elapsedMs": 2412
  }
}
```

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

## Application Process

To use the WebExtrator API, apply for the service on the
[WebExtrator service page](https://platform.acedata.cloud/service/webextrator).
After landing on the page, click the **Acquire** button to obtain credentials.

If you are not logged in or registered, you will be automatically redirected to
the login page inviting you to register and log in.

A free quota is provided to first-time applicants — try the API before
committing to paid usage.

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
