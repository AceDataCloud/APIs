# WebExtrator Render API Integration Guide

`POST https://api.acedata.cloud/webextrator/render`

This document introduces the WebExtrator Render API. This API provides headless browser rendering for any URL, returning the fully rendered HTML, markdown, plain text, screenshot, and extracted links.

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
| `timeout` | number | ❌ | 30000 | Single render timeout in milliseconds, max 120000 |
| `wait_until` | string | ❌ | `load` | Load completion event: `load` / `domcontentloaded` / `networkidle` |
| `delay` | number | ❌ | 0 | Additional wait time after load completes (milliseconds), max 30000 |
| `wait_for_selector` | string | ❌ | - | Wait until this CSS selector appears |
| `block_resources` | string[] | ❌ | - | Block resource types: `image` / `media` / `font` / `stylesheet`, etc. |
| `headers` | object | ❌ | - | Additional HTTP headers |
| `cookies` | array | ❌ | - | Cookie list; each element has the form `{name, value, domain, path}` |
| `callback_url` | string | ❌ | - | Async mode callback URL; if provided, the task ID is returned immediately and the result is delivered via POST callback |

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
    "title": "Example Domain",
    "html": "<!doctype html>...",
    "text": "Example Domain ...",
    "markdown": "# Example Domain\n...",
    "screenshot": "data:image/png;base64,iVBORw0K...",
    "links": ["https://www.iana.org/domains/example"]
  }
}
```

## Async Mode (with callback_url)

Initial response:

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z"
}
```

The response header will include `x-usage-exempt: true`, indicating that this synchronous handshake is not billed. Once the task actually completes, the platform will send a POST to the `callback_url` with the same `data` field as the synchronous response, plus the same `task_id` / `trace_id` / `started_at` / `finished_at` / `elapsed` fields.

## Error Response

```json
{
  "success": false,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z",
  "error": {
    "code": "timeout",
    "message": "page load timed out after 30000ms"
  }
}
```

Error codes: `bad_request` / `forbidden` / `too_many_requests` / `not_found` / `api_error` / `timeout` / `unknown` / `busy`.

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

Through this document, you have learned how to use the WebExtrator Render API to render any web page and receive the fully rendered HTML, markdown, text, screenshot, and links. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
