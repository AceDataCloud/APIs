# WebExtrator Extract API Integration Guide

`POST https://api.acedata.cloud/webextrator/extract`

The WebExtrator Extract API turns a URL into a typed, structured payload —
Article, Product, Recipe, Video, Discussion, Job — with markdown and clean text
on the side. It is the right endpoint to call when you want **clean structured
data** rather than raw HTML.

Under the hood Extract runs a three-tier pipeline:

1. **schema.org JSON-LD mapper** — deterministic, zero LLM cost. Covers
   Wikipedia / BestBuy / AllRecipes / YouTube / most news / most product pages.
2. **LLM-first typed extractor** — for pages without JSON-LD (Amazon, Hacker
   News, Greenhouse, blogs). Zod-validated typed payload per kind.
3. **Readability + markdown fallback** — always runs; populates the basic
   top-level fields when neither layer above filled them.

Repeat URL requests hit a Redis result cache and return in <1 ms.

---

## Application Process

To use the WebExtrator Extract API, apply for the service on the
[WebExtrator service page](https://platform.acedata.cloud/service/webextrator).
Click **Acquire** to obtain the credentials needed for the request. A free
quota is provided to first-time applicants.

---

## Authentication

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

---

## Request Body

Extract accepts **everything** Render accepts (see
[Render API guide](webextrator_render_api_integration_guide.md#request-body) —
`url`, `user_agent`, `timeout`, `wait_until`, `delay`, `wait_for_selector`,
`block_resources`, `headers`, `cookies`, `callback_url`, `bypass_cache`,
`cache_ttl_seconds`, `mode`) plus the two Extract-specific fields:

| Field | Type | Required | Default | Description |
|---|---|:---:|---|---|
| `expected_type` | enum | ❌ | auto | Hint at the page kind: `product` \| `article` \| `general`. Skips the URL/text heuristic and dispatches directly. |
| `enable_llm` | boolean | ❌ | `false` | Allow the LLM-first extractor to run when schema.org returned nothing. Required for the typed payload on Amazon / HN / Greenhouse-style pages. |

> When the page already ships schema.org JSON-LD, `enable_llm` has no effect —
> the deterministic mapper wins and we never spend the LLM call. You always
> get the typed payload for free.

---

## Response (Sync)

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z",
  "finished_at": "2026-05-02T10:30:02.535Z",
  "elapsed": 2.412,
  "data": {
    "kind": "extract",
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "finalUrl": "https://en.wikipedia.org/wiki/Diffbot",
    "contentType": "article",
    "title": "Diffbot",
    "description": "American machine learning and knowledge management company",
    "byline": "Contributors to Wikimedia projects",
    "language": "en",
    "siteName": "Wikipedia",
    "publishedAt": "2007-08-08T05:47:27Z",
    "images": ["https://en.wikipedia.org/static/images/icons/enwiki-25.svg"],
    "links": ["https://en.wikipedia.org/wiki/Machine_learning"],
    "markdown": "# Diffbot\n\nDiffbot is a developer of machine learning ...",
    "text":     "Diffbot is a developer of machine learning algorithms ...",
    "structured": {
      "schemaOrg": { "primary": { /* typed entity */ }, "breadcrumbs": [], "all": [] },
      "openGraph": { "title": "...", "description": "...", "image": "...", "type": "..." },
      "jsonLd":   [ /* raw passthrough */ ]
    },
    "rawSignals": {
      "hasJsonLd": true,
      "title": "Diffbot - Wikipedia",
      "metaDescription": null,
      "pageStatus": 200,
      "textLength": 11473
    },
    "elapsedMs": 2412
  }
}
```

### Top-level data fields

| Field | Type | Description |
|---|---|---|
| `kind` | string | Always `"extract"`. |
| `url` | string | The URL you supplied. |
| `finalUrl` | string | URL after redirects. |
| `contentType` | enum | `product` \| `article` \| `general`. Derived from `expected_type` if given, else from schema.org primary, else heuristic. |
| `title` | string | Readability `<title>` or render `document.title`. |
| `description` | string? | First non-empty of: `<meta name="description">` → `og:description` → schema.org / LLM payload → trimmed first paragraph. |
| `byline` | string? | Author / channel / company name. Sourced from `<meta name="author">`, then schema.org / LLM payload. |
| `language` | string? | `<html lang>` value. |
| `siteName` | string? | `og:site_name`. |
| `publishedAt` | string? | ISO 8601. `article:published_time` meta → `<time datetime>` → schema.org / LLM payload. |
| `images` | string[] | Up to 50 `<img src>` values, resolved to absolute URLs, deduped, `data:` URIs dropped. |
| `links` | string[] | Up to 100 outbound link URLs, fragment-only / `javascript:` / `mailto:` / `tel:` filtered. |
| `markdown` | string | Turndown-rendered body markdown. |
| `text` | string | Mozilla Readability `textContent`. |
| `structured` | object | Full structured payload — see below. |
| `rawSignals` | object | Diagnostic counts for debugging. |
| `cached` | boolean? | `true` if served from cache. |
| `cacheStoredAt` | number? | Unix-ms when the cached entry was first stored. |

### `data.structured`

| Sub-field | When present | Description |
|---|---|---|
| `schemaOrg` | always | `{ primary, breadcrumbs, all }`. `primary` is the highest-priority typed entity (see below); `null` if none found. |
| `openGraph` | always | `{ title, description, image, type }` from `<meta property="og:*">`. |
| `jsonLd` | always | Raw passthrough of every `<script type="application/ld+json">` block parsed into JSON. |
| `llm` | when LLM ran & succeeded | `{ kind, data, model, promptCharCount }`. Typed Zod-validated payload — see [LLM extractor schemas](#llm-extractor-schemas). |
| `llmError` | when LLM ran & failed | `{ kind, error, model }`. Errors never crash the request; the heuristic payload still ships. |
| `amazon` | when URL is `amazon.*` | Legacy pre-LLM amazon scraper output. Will be deprecated. |

---

## schema.org mapper coverage

The mapper recognises these types (priority order — first match wins as
`structured.schemaOrg.primary`):

| schema.org type | mapped kind | Surfaced fields |
|---|---|---|
| `Product` | product | `name, sku, gtin, model, color, brand, url, images, offer.{price,currency,availability,condition,seller}, rating.{value,count}, reviews[], properties[]` |
| `Recipe` | recipe | `name, description, image, datePublished, author, cookTime, prepTime, totalTime, recipeYield, ingredients[], instructions[], nutrition, rating, keywords, recipeCategory, recipeCuisine` |
| `VideoObject` | video | `name, description, thumbnailUrl, uploadDate, duration, embedUrl, contentUrl, channel, interactionCount` |
| `JobPosting` | job | `title, description, datePosted, validThrough, hiringOrganization, jobLocation, baseSalary, employmentType` |
| `Event` (and `*Event`) | event | `name, description, startDate, endDate, location.{name,address}, organizer, offer.{url,price,currency}` |
| `Article` / `NewsArticle` / `BlogPosting` / `ScholarlyArticle` / `TechArticle` / `Report` / `*NewsArticle` | article | `subtype, headline, description, datePublished, dateModified, author, publisher, image[], url, sameAs[]` |
| `FAQPage` | faq | `questions[{question, answer}]` |
| `BreadcrumbList` | (sibling) | Always surfaced in `structured.schemaOrg.breadcrumbs[]`, never as primary. |

The mapper handles:

- `@graph` containers (recursively flattened).
- `@type` arrays (e.g. `["Recipe", "NewsArticle"]` — both are recognised, the
  higher-priority kind wins).
- The `http://schema.org/` prefix variant.
- Nested `Offer` and `AggregateOffer` (reads `lowPrice` on the latter).
- Relative image URLs (resolved against `finalUrl`).

---

## LLM extractor schemas

When `enable_llm: true` **and** schema.org returned no primary entity, the
extractor picks one of these typed schemas based on URL heuristics (or your
`expected_type` hint) and validates the model's JSON output against it:

| Kind | URL heuristic | Required field | Optional fields |
|---|---|---|---|
| `article` | text ≥ 400 chars and no other match | `headline` | `description, byline, publishedAt, language, topics[], sections[{heading,summary}]` |
| `product` | `amazon.* / ebay.* / aliexpress.* / temu.* / walmart.* / bestbuy.*` | `name` | `description, brand, sku, price, currency, availability, rating.{value,count}, bullets[], specifications[{name,value}]` |
| `discussion` | `news.ycombinator.com / reddit.com / lobste.rs` | `title` | `author, postedAt, points, commentCount, body, url` |
| `recipe` | `allrecipes / foodnetwork / seriouseats / epicurious / bonappetit / simplyrecipes` | `name` | `description, author, cookTime, prepTime, totalTime, recipeYield, ingredients[], instructions[], nutrition, rating, keywords[]` |
| `video` | `youtube.com/watch / youtu.be / vimeo.com/<id> / tiktok.com/@/video` | `name` | `description, channel, uploadDate, duration, viewCount, likeCount, thumbnailUrl, transcript` |
| `job` | `greenhouse.io / lever.co / jobs.* / careers.* / workable.com / bamboohr` | `title` | `description, company, location, remote, employmentType, datePosted, validThrough, salaryMin, salaryMax, salaryCurrency, salaryPeriod, responsibilities[], qualifications[]` |

When the LLM call succeeds you also get the typed payload back-filling the
top-level fields:

- `article` → `description`, `byline`, `publishedAt`, `language`
- `product` → `description`
- `discussion` → `description` (= body, ≤ 280 chars), `byline` (= author), `publishedAt` (= postedAt)
- `recipe` → `description`, `byline` (= author)
- `video` → `description`, `byline` (= channel), `publishedAt` (= uploadDate)
- `job` → `description`, `byline` (= company), `publishedAt` (= datePosted)

Back-fills only fire if the deterministic source didn't already populate that
field — the LLM is always a last resort.

---

## Caching

Identical requests hash to the same Redis key:
`webextrator:cache:extract:<sha256(canonical-json)>`. Cache keys ignore `mode`,
`bypass_cache`, and `cache_ttl_seconds` (those are operational toggles, not
part of the response). Cookies / headers DO partition the cache.

| Field | Effect |
|---|---|
| `bypass_cache: true` | Skip the read; still write the fresh result back so subsequent identical calls hit. |
| `cache_ttl_seconds: 0` | Don't cache this response at all. |
| `cache_ttl_seconds: N` | Override the 3600 s default for this entry. |

Cached responses set `data.cached: true` and `data.cacheStoredAt: <unix-ms>`.

---

## Async mode and callbacks

Set `mode: "async"` to fire-and-forget. The platform returns
`{ "jobId": "...", "status": "queued" }` (HTTP 202) immediately and posts the
final envelope to your `callback_url` (if provided) once the job finishes. Use
[`/webextrator/tasks`](webextrator_tasks_api_integration_guide.md) to look up
results by `task_id` or `trace_id` later.

---

## Examples

### 1. Article from Wikipedia (schema.org wins; no LLM needed)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "expected_type": "article"
  }'
```

Key fields in `data.structured.schemaOrg.primary`:

```json
{
  "kind": "article",
  "subtype": "Article",
  "headline": "American machine learning and knowledge management company",
  "datePublished": "2007-08-08T05:47:27Z",
  "dateModified": "2025-07-10T20:42:45Z",
  "author": { "name": "Contributors to Wikimedia projects", "type": "Organization" },
  "publisher": { "name": "Wikimedia Foundation, Inc." }
}
```

### 2. Product page (BestBuy ships JSON-LD)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bestbuy.com/product/apple-airpods-pro-2nd-generation-white/JJ8ZH6TPSW",
    "expected_type": "product"
  }'
```

Surfaced from schema.org:

```json
{
  "kind": "product",
  "name": "Apple - Refurbished Excellent - AirPods Pro (2nd generation) - White",
  "sku": "10845412",
  "model": "MQD83AM/A",
  "color": "White",
  "brand": "Apple",
  "offer": { "price": 159.99, "currency": "USD", "availability": "https://schema.org/InStock", "seller": "Best Buy" },
  "rating": { "value": 4.4, "count": 8 }
}
```

### 3. Recipe page (Recipe + nutrition + steps)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
  }'
```

Surfaced from schema.org:

```json
{
  "kind": "recipe",
  "name": "Easy Meatloaf",
  "cookTime": "PT60M",
  "totalTime": "PT75M",
  "recipeYield": "8 / 1 (9x5-inch) meatloaf",
  "ingredients": ["1 1/2 pounds ground beef", "..."],
  "instructions": [{ "text": "Preheat oven to 350°F ..." }, "..."],
  "rating": { "value": 4.7, "count": 9348 }
}
```

### 4. HN discussion (no JSON-LD — LLM is required)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com/item?id=37000000",
    "enable_llm": true
  }'
```

Look in `data.structured.llm.data`:

```json
{
  "kind": "discussion",
  "title": "Show HN: A new way to extract web pages",
  "author": "alice",
  "points": 173,
  "commentCount": 42,
  "body": "Hi HN, we built a self-hosted alternative to Diffbot's Analyze API ..."
}
```

The top-level response is also back-filled: `byline = "alice"`,
`publishedAt = "..."`.

### 5. Amazon product (Amazon ships no JSON-LD — LLM is required)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B0BSHF7WHW",
    "expected_type": "product",
    "enable_llm": true
  }'
```

`data.structured.llm.data` (typed `product`):

```json
{
  "kind": "product",
  "name": "Apple 2023 MacBook Pro M2 Pro 14-inch",
  "brand": "Apple",
  "price": 1799,
  "currency": "USD",
  "bullets": ["Apple M2 Pro chip with 10-core CPU", "..."],
  "specifications": [{ "name": "Display size", "value": "14.2 inches" }, "..."]
}
```

### Python (requests)

```python
import os, requests

API_KEY = os.environ["ACEDATA_API_KEY"]

resp = requests.post(
    "https://api.acedata.cloud/webextrator/extract",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "url": "https://en.wikipedia.org/wiki/Diffbot",
        "expected_type": "article",
    },
    timeout=120,
)
resp.raise_for_status()
data = resp.json()["data"]

primary = (data.get("structured") or {}).get("schemaOrg", {}).get("primary")
print("contentType:", data["contentType"])
print("title:      ", data["title"])
print("byline:     ", data.get("byline"))
print("publishedAt:", data.get("publishedAt"))
if primary and primary["kind"] == "article":
    print("headline:   ", primary["headline"])
    print("dateModified:", primary.get("dateModified"))
```

### Node.js (fetch)

```js
const apiKey = process.env.ACEDATA_API_KEY;

const res = await fetch('https://api.acedata.cloud/webextrator/extract', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.allrecipes.com/recipe/16354/easy-meatloaf/',
  }),
});
const { data } = await res.json();
const recipe = data?.structured?.schemaOrg?.primary;
console.log(recipe.name, recipe.cookTime, recipe.ingredients.length, 'ingredients');
```

---

## Tips and Gotchas

- **Always set `expected_type` when you know it.** Free hint, no cost, skips
  the URL/text heuristic. Especially valuable on pages whose URL doesn't
  match the built-in patterns.
- **`enable_llm: true` is free when schema.org wins.** The LLM is only called
  when no schema.org primary was found, so flipping it on by default is safe
  for traffic dominated by sites that ship JSON-LD.
- **Inspect `rawSignals.hasJsonLd` first when debugging.** If `true` and
  `structured.schemaOrg.primary` is `null`, the JSON-LD present uses a `@type`
  the mapper doesn't recognise — open an issue and we'll add it.
- **`structured.llmError` is informational.** The request still succeeds and
  the heuristic-only payload still ships. Check `llmError.error` for the
  reason (timeout, JSON parse failure, Zod validation failure).
- **Don't rely on `links[]` being clean for non-article pages.** It's
  best-effort — we keep up to 100 outbound URLs, fragment-only and
  `javascript:` filtered, but no content-relevance ranking.
- **Cache hits are still billed.** Caching is for *latency* (and to protect
  the underlying browser pool), not for cost.
