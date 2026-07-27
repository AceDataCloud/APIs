# WebExtrator Render API Integration Guide

`POST https://api.acedata.cloud/webextrator/render`

The WebExtrator Render API is a headless-Chromium rendering service. Give it a
URL and get back the fully-rendered HTML (including JavaScript-injected
content), plain text, page title, and the final URL after redirects.

Render is the lowest-level WebExtrator endpoint. If you want **structured**
content extraction (article body, product price, recipe ingredients, …) use
[`/webextrator/extract`](webextrator_extract_api_integration_guide.md) instead —
it runs the same render + a typed extraction pipeline on top.

---

## Application Process

To use the WebExtrator Render API, apply for the service on the
[WebExtrator service page](https://platform.acedata.cloud/service/webextrator).
Click **Acquire** to obtain the credentials needed for the request. A free
quota is provided to first-time applicants.

---

## Authentication

All WebExtrator endpoints use the standard AceDataCloud bearer-token scheme:

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

---

## Request Body

| Field | Type | Required | Default | Description |
|---|---|:---:|---|---|
| `url` | string | ✅ | — | Page URL to render. Must be `http(s)://`. |
| `user_agent` | string | ❌ | rotating modern Chrome UA | Override the browser User-Agent header. |
| `timeout` | number | ❌ | 30 | Per-request navigation timeout in **seconds**. |
| `wait_until` | enum | ❌ | `networkidle` | Page-ready condition: `load` \| `domcontentloaded` \| `networkidle` \| `commit`. |
| `delay` | number | ❌ | 0 | Extra wait **in seconds** after `wait_until` fires (use for SPAs that re-render). |
| `wait_for_selector` | string | ❌ | — | CSS selector to wait for before considering the page ready. Cuts down on flaky `networkidle` failures. |
| `block_resources` | string[] | ❌ | `["image","font","media"]` (server default) | Resource types to drop. Choices: `image`, `font`, `media`, `stylesheet`, `xhr`, `fetch`. Blocking saves bandwidth and renders faster. |
| `headers` | object | ❌ | — | Additional request headers sent to the target site (e.g. `{"Accept-Language": "en-US"}`). |
| `cookies` | array | ❌ | — | Cookies to install before navigation. See [Cookie shape](#cookie-shape). |
| `callback_url` | string | ❌ | — | If set, the platform `POST`s the final envelope here when the job finishes (also enables async mode automatically). |
| `bypass_cache` | boolean | ❌ | false | Skip the Redis result cache for this request (still writes the fresh result back). |
| `cache_ttl_seconds` | number | ❌ | 3600 | Override the global cache TTL for this entry. `0` is allowed and means "don't cache this response". |
| `async` | boolean | ❌ | `false` | Set to `true` to return `task_id` immediately; result is delivered via `callback_url` or the Tasks API. |

> Note: parameters use **snake_case** on the platform contract. The internal
> render service uses `camelCase`; both are documented in the OpenAPI spec but
> external callers should always use snake_case.

### Cookie shape

```json
{
  "name":      "string",
  "value":     "string",
  "domain":    "string",
  "path":      "/",
  "expires":   1735689600,
  "httpOnly":  false,
  "secure":    true,
  "sameSite":  "Lax"
}
```

---

## Response (Sync mode)

The envelope is the standard AceDataCloud `success / error` shape.

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z",
  "finished_at": "2026-05-02T10:30:01.234Z",
  "elapsed": 1.111,
  "data": {
    "kind": "render",
    "url": "https://example.com",
    "finalUrl": "https://example.com/",
    "title": "Example Domain",
    "status": 200,
    "html": "<!DOCTYPE html><html>...</html>",
    "text": "Example Domain\nThis domain is for use in illustrative examples...",
    "userAgent": "Mozilla/5.0 ...",
    "elapsedMs": 1108
  }
}
```

| Field | Type | Description |
|---|---|---|
| `data.kind` | string | Always `"render"`. |
| `data.url` | string | The URL you supplied. |
| `data.finalUrl` | string | The URL after redirects. |
| `data.title` | string | `document.title` of the rendered page. |
| `data.status` | number \| null | HTTP status of the main navigation response. |
| `data.html` | string | Full rendered HTML. |
| `data.text` | string | `document.body.innerText` — quick plain-text snapshot (Extract API returns a cleaner Readability text). |
| `data.userAgent` | string | UA actually used (after pool rotation, if any). |
| `data.elapsedMs` | number | Render time (browser only). |
| `data.cached` | boolean? | `true` if served from Redis cache. |
| `data.cacheStoredAt` | number? | Unix-ms timestamp when the cached entry was first stored. |

---

## Response (Async mode)

When `async: true` (or `callback_url` is set):

```json
{
  "success": true,
  "task_id": "550e8400-...",
  "trace_id": "6ba7b810-...",
  "started_at": "2026-05-02T10:30:00.123Z"
}
```

Status code is `200`. Result is delivered either by `POST` to your `callback_url`
or by polling [`/webextrator/tasks`](webextrator_tasks_api_integration_guide.md).

### Callback shape

The platform `POST`s the **same envelope** you would have received in sync mode
to `callback_url` with `Content-Type: application/json`. Acknowledge with any
`2xx`; the platform retries `5xx` with exponential backoff for ~5 minutes.

---

## Error Responses

| HTTP | `error.code` | Meaning |
|---|---|---|
| 400 | `bad_request` | Body failed Zod validation (missing `url`, wrong types, …). |
| 401 | `unauthorized` | Missing or invalid `Authorization: Bearer …`. |
| 402 | (x402) | Insufficient platform balance — see x402 payment envelope. |
| 408 | `timeout` | Navigation exceeded `timeout`. |
| 429 | `queue_busy` | Sync queue depth too high — retry, or use `async: true`. |
| 500 | `internal_error` | Unhandled server-side failure (browser crash, etc.). Auto-retried by the worker once. |

Errors share the standard envelope:

```json
{
  "success": false,
  "task_id": "...",
  "trace_id": "...",
  "started_at": "...",
  "finished_at": "...",
  "elapsed": 0.012,
  "error": {
    "code": "bad_request",
    "message": "url: Invalid url"
  }
}
```

---

## Examples

### cURL

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

### Python (requests)

```python
import os
import requests

API_KEY = os.environ["ACEDATA_API_KEY"]

resp = requests.post(
    "https://api.acedata.cloud/webextrator/render",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "url": "https://example.com",
        "wait_until": "networkidle",
        "block_resources": ["image", "media", "font"],
    },
    timeout=60,
)
resp.raise_for_status()
data = resp.json()["data"]
print(data["title"], data["status"], len(data["html"]))
```

### Node.js (fetch)

```js
const apiKey = process.env.ACEDATA_API_KEY;

const res = await fetch('https://api.acedata.cloud/webextrator/render', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com',
    wait_until: 'networkidle',
    block_resources: ['image', 'media', 'font'],
  }),
});
const { data } = await res.json();
console.log(data.title, data.status, data.html.length);
```

### Async + callback

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "async": true,
    "callback_url": "https://your-app.example.com/hooks/webextrator"
  }'
```

You will receive `{ "success": true, "task_id": "...", "trace_id": "...", "started_at": "..." }` immediately. Your
`callback_url` will be called once the job finishes (typically within a few
seconds for normal pages, up to a minute for heavy SPAs).

### Forcing a re-render past the cache

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "bypass_cache": true
  }'
```

---

## Tips and Gotchas

- **`wait_until` choice matters.** `networkidle` is the safest but slowest;
  `domcontentloaded` is fast but may miss late XHR-injected content; `load`
  works well for classic static pages.
- **Cache key ignores `async`.** Sync and async requests for the same URL
  hit the same cache entry — flip `async` freely without invalidating anything.
- **Cache key ignores `bypass_cache` and `cache_ttl_seconds`.** Those are
  operational toggles, not part of the response.
- **Cookies and headers DO partition the cache.** If you customise them per
  request, expect cache misses on the first call per unique combination.
- **Heavy pages can exceed the default 30 s timeout.** For SPAs that lazy-load,
  set `timeout: 60` and `wait_until: "domcontentloaded"` + `delay: 4` and a
  `wait_for_selector` for the element you actually care about.
- **`block_resources` is your fastest path to lower latency.** Default already
  blocks images / fonts / media. Add `stylesheet` if your extraction doesn't
  need CSS-driven layout.
