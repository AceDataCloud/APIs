# WebExtrator Render API Integration Guide

`POST https://api.acedata.cloud/webextrator/render`

The WebExtrator Render API fully renders a web page using a headless browser and returns its HTML, plain text, Markdown, screenshot, and links. It supports both synchronous and asynchronous (callback) modes.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request headers.

## Request Parameters

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `url` | string | ✅ | - | The URL of the page to render |
| `user_agent` | string | ❌ | System default | Custom User-Agent string |
| `timeout` | number | ❌ | 30000 | Rendering timeout in milliseconds (max 120000) |
| `wait_until` | string | ❌ | `load` | Load completion event: `load` / `domcontentloaded` / `networkidle` |
| `delay` | number | ❌ | 0 | Additional wait time after page load (milliseconds, max 30000) |
| `wait_for_selector` | string | ❌ | - | Wait for this CSS selector to appear before returning |
| `block_resources` | string[] | ❌ | - | Resource types to block: `image` / `media` / `font` / `stylesheet`, etc. |
| `headers` | object | ❌ | - | Additional HTTP headers to include in the request |
| `cookies` | array | ❌ | - | Cookie list; each element has the form `{name, value, domain, path}` |
| `callback_url` | string | ❌ | - | Async mode callback address; when provided, returns a task ID immediately and delivers the result via POST callback |

## Synchronous Response (without `callback_url`)

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

## Asynchronous Mode (with `callback_url`)

Initial response:

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": "2026-05-02T10:30:00.123Z"
}
```

The response headers will include `x-usage-exempt: true`, indicating that this synchronous handshake is not billed. Once the task completes, the platform sends a POST to `callback_url` with the same `data` field as the synchronous response, along with `task_id`, `trace_id`, `started_at`, `finished_at`, and `elapsed` fields.

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

## Conclusion

Through this document, you have learned how to use the WebExtrator Render API to fully render web pages and retrieve their content. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
