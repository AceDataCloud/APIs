# WebExtrator Extract API Integration Guide

`POST https://api.acedata.cloud/webextrator/extract`

This API performs intelligent extraction and returns structured content (for example `article`, `product`, or `general`) with cleaned markdown/text.

## Application Process

To use the WebExtrator Extract API, apply for the corresponding service on the [WebExtrator service page](https://platform.acedata.cloud/service/webextrator) and click **Acquire**.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Request Parameters

The Extract API accepts all Render API parameters (`url`, `user_agent`, `timeout`, `wait_until`, `delay`, `wait_for_selector`, `block_resources`, `headers`, `cookies`, `callback_url`, `bypass_cache`, `cache_ttl_seconds`, `mode`) plus:

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `expected_type` | string | ❌ | auto | Extraction hint: `product` / `article` / `general`. |
| `enable_llm` | boolean | ❌ | `false` | Allow LLM-based typed extraction when deterministic extraction is not enough. |

## Synchronous Response (`mode=sync`)

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
    "url": "https://example.com/article",
    "finalUrl": "https://example.com/article",
    "contentType": "article",
    "title": "Example Article",
    "description": "...",
    "byline": "...",
    "markdown": "# Example Article\n...",
    "text": "Example Article ...",
    "structured": {},
    "elapsedMs": 2412
  }
}
```

## Asynchronous Mode (`mode=async`)

The API returns immediately:

```json
{ "jobId": "550e8400-...", "status": "queued" }
```

Final results are delivered through `callback_url` or can be queried with the [Tasks API](webextrator_tasks_api_integration_guide.md).

## Example: Article Extraction

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/news/1",
    "expected_type": "article",
    "enable_llm": true
  }'
```

## Example: Async Structured Extraction

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://shop.example.com/item/123",
    "expected_type": "product",
    "enable_llm": true,
    "mode": "async",
    "callback_url": "https://your-domain.com/wbx-callback"
  }'
```

## Error Handling

Error envelope and status code behavior follow `/webextrator/render`.
