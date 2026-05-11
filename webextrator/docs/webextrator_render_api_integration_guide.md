# WebExtrator Render API Integration Guide

`POST https://api.acedata.cloud/webextrator/render`

This document introduces the WebExtrator Render API. This API provides headless browser rendering for any URL and returns rendered HTML, plain text, page title, and final URL.

## Application Process

To use the WebExtrator Render API, apply for the corresponding service on the WebExtrator service page. After entering the page, click the "Acquire" button to obtain the credentials needed for the request.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Request Parameters

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `url` | string | ✅ | - | The URL of the page to render |
| `user_agent` | string | ❌ | System default | Custom User-Agent |
| `timeout` | number | ❌ | 30 | Total timeout in seconds for the render operation |
| `wait_until` | string | ❌ | `networkidle` | Load completion event: `load` / `domcontentloaded` / `networkidle` / `commit` |
| `delay` | number | ❌ | - | Additional wait time after load completes (seconds) |
| `wait_for_selector` | string | ❌ | - | Wait until this CSS selector appears |
| `block_resources` | string[] | ❌ | - | Block resource types: `image` / `media` / `font` / `stylesheet` / `xhr` / `fetch` |
| `headers` | object | ❌ | - | Additional HTTP headers |
| `callback_url` | string | ❌ | - | If provided, request is processed asynchronously and final result is POSTed to this URL |

## Synchronous Response (without callback_url)

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z",
  "finished_at": "2026-05-02T10:30:05.456Z",
  "elapsed": 5.333,
  "data": {
    "kind": "render",
    "url": "https://example.com",
    "finalUrl": "https://example.com/",
    "title": "Example Domain",
    "status": 200,
    "html": "<!DOCTYPE html><html>...</html>",
    "text": "Example Domain ...",
    "userAgent": "Mozilla/5.0 ...",
    "elapsedMs": 5300
  }
}
```

## Async Mode (with `callback_url`)

When `callback_url` is provided, the platform processes the request asynchronously and sends the final result via POST callback.

## Error Response

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "url is required"
  }
}
```

Error codes include: `bad_request` / `unauthorized` / `too_many_requests` / `api_error` / `timeout`.

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

Python example:

```python
import requests

url = "https://api.acedata.cloud/webextrator/render"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "url": "https://example.com",
    "wait_until": "networkidle",
    "block_resources": ["image", "media", "font"]
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Conclusion

Through this document, you have learned how to use the WebExtrator Render API to render any web page and receive the fully rendered HTML, text, title, and final URL. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
