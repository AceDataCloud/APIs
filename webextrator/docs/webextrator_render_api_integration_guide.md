# WebExtrator Render API Integration Guide

`POST https://api.acedata.cloud/webextrator/render`

This API renders a web page using a headless browser and returns structured render output.

## Application Process

To use the WebExtrator Render API, apply for the corresponding service on the [WebExtrator service page](https://platform.acedata.cloud/service/webextrator) and click **Acquire**.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Request Parameters

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `url` | string | ✅ | - | The URL to render (`http(s)://`). |
| `user_agent` | string | ❌ | System default | Custom User-Agent. |
| `timeout` | number | ❌ | `30` | Render timeout in seconds. |
| `wait_until` | string | ❌ | `networkidle` | `load` / `domcontentloaded` / `networkidle` / `commit`. |
| `delay` | number | ❌ | `0` | Extra wait time (seconds) after `wait_until`. |
| `wait_for_selector` | string | ❌ | - | Wait for a CSS selector before capture. |
| `block_resources` | string[] | ❌ | `"image","font","media"` | Blocked resource types. |
| `headers` | object | ❌ | - | Extra HTTP headers. |
| `cookies` | array | ❌ | - | Cookies to inject before navigation. |
| `callback_url` | string | ❌ | - | Callback URL for async result delivery. |
| `bypass_cache` | boolean | ❌ | `false` | Skip cache read for this request. |
| `cache_ttl_seconds` | number | ❌ | `3600` | Cache TTL for this response (`0` = do not cache). |
| `mode` | string | ❌ | `sync` | `sync` or `async`. |

## Synchronous Response (`mode=sync`)

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
    "text": "Example Domain ...",
    "userAgent": "Mozilla/5.0 ...",
    "elapsedMs": 1108
  }
}
```

## Asynchronous Mode (`mode=async`)

The API returns immediately:

```json
{ "jobId": "550e8400-...", "status": "queued" }
```

When the task finishes, the platform POSTs the full result envelope to `callback_url` (if provided). You can also query result status using the [Tasks API](webextrator_tasks_api_integration_guide.md).

## Error Response

| HTTP | `error.code` | Meaning |
|------|--------------|------|
| 400 | `bad_request` | Invalid request body. |
| 401 | `unauthorized` | Missing or invalid token. |
| 402 | `x402` | Insufficient balance. |
| 408 | `timeout` | Render exceeded timeout. |
| 429 | `queue_busy` | Queue is busy. Retry or use async mode. |
| 500 | `internal_error` | Internal server error. |

```json
{
  "success": false,
  "task_id": "...",
  "trace_id": "...",
  "started_at": "...",
  "finished_at": "...",
  "elapsed": 0.012,
  "error": { "code": "bad_request", "message": "url: Invalid url" }
}
```

## Example

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
