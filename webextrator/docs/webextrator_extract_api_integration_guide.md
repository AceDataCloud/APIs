# WebExtrator Extract API Integration Guide

`POST https://api.acedata.cloud/webextrator/extract`

This document introduces the WebExtrator Extract API. This API builds on top of the Render API to provide intelligent content extraction. It supports extracting articles, markdown, plain text, links, or custom structured data — with an optional LLM post-processing step for advanced use cases.

## Application Process

To use the WebExtrator Extract API, apply for the corresponding service on the WebExtrator service page. After entering the page, click the "Acquire" button to obtain the credentials needed for the request.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Parameters

The Extract API accepts all parameters from the [Render API](webextrator_render_api_integration_guide.md), plus the following additional fields:

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `expected_type` | string | ❌ | `markdown` | Desired extraction output: `markdown` / `article` / `text` / `links` / `structured` |
| `enable_llm` | boolean | ❌ | false | Enable LLM post-processing (recommended for `article` / `structured`) |
| `instruction` | string | ❌ | - | LLM extraction instruction, e.g. "Extract product title, price, and specifications" |

## Synchronous Response

```json
{
  "success": true,
  "task_id": "550e8400-...",
  "trace_id": "550e8400-...",
  "started_at": "2026-05-02T10:30:00.123Z",
  "finished_at": "2026-05-02T10:30:08.789Z",
  "elapsed": 8.666,
  "data": {
    "kind": "extract",
    "expected_type": "article",
    "url": "https://example.com/post/1",
    "title": "Sample Article",
    "author": "John Doe",
    "published_at": "2026-05-01",
    "content": "# Sample Article\n\nBody text ...",
    "summary": "This article introduces ..."
  }
}
```

The async mode, error codes, and billing rules are identical to those of the `/webextrator/render` API.

## Example: Extract Article (with LLM enabled)

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

Python example:

```python
import requests

url = "https://api.acedata.cloud/webextrator/extract"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "url": "https://example.com/news/1",
    "expected_type": "article",
    "enable_llm": True
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Example: Async + Custom Structured Extraction

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://shop.example.com/item/123",
    "expected_type": "structured",
    "enable_llm": true,
    "instruction": "Extract product title, price, stock, and 3 main image URLs",
    "callback_url": "https://your-domain.com/wbx-callback"
  }'
```

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. Error codes: `bad_request` / `forbidden` / `too_many_requests` / `not_found` / `api_error` / `timeout` / `unknown` / `busy`.

## Conclusion

Through this document, you have learned how to use the WebExtrator Extract API to intelligently extract content from web pages, including articles, markdown, plain text, links, and custom structured data. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
