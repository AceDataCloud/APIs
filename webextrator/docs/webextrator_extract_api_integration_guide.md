# WebExtrator Extract API Integration Guide

`POST https://api.acedata.cloud/webextrator/extract`

This document introduces the WebExtrator Extract API. This API builds on top of the Render API to provide intelligent content extraction. It supports extracting articles, markdown, plain text, links, or custom structured data — with an optional LLM post-processing step for advanced use cases.

## Application Process

To use the WebExtrator Extract API, apply for the corresponding service on the WebExtrator service page. After entering the page, click the "Acquire" button to obtain the credentials needed for the request.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Request Parameters

The Extract API accepts all parameters from the [Render API](webextrator_render_api_integration_guide.md), plus the following additional fields:

| Field | Type | Required | Default | Description |
|------|------|:----:|------|------|
| `expected_type` | string | ❌ | - | Hint the page type to optimize extraction: `product` / `article` / `general` |
| `enable_llm` | boolean | ❌ | false | Enable optional LLM-based semantic normalization |

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
    "url": "https://www.amazon.com/dp/B0C1234567",
    "contentType": "product",
    "title": "Acme Widget",
    "description": "A widget that does things.",
    "byline": "Acme Inc.",
    "siteName": "Amazon.com",
    "images": [
      "https://example.com/widget.jpg"
    ],
    "links": [
      "https://example.com/related"
    ],
    "markdown": "# Acme Widget\n...",
    "structured": {
      "price": 19.99,
      "currency": "USD",
      "brand": "Acme",
      "rating": 4.5
    }
  }
}
```

The async mode, error codes, and billing rules are identical to those of the `/webextrator/render` API.

## Example: Extract Product (with LLM enabled)

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B0C1234567",
    "expected_type": "product",
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
    "url": "https://www.amazon.com/dp/B0C1234567",
    "expected_type": "product",
    "enable_llm": True
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Example: Async Extraction

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/news/1",
    "callback_url": "https://your-domain.com/wbx-callback"
  }'
```

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. Error codes include: `bad_request` / `unauthorized` / `too_many_requests` / `api_error` / `timeout`.

## Conclusion

Through this document, you have learned how to use the WebExtrator Extract API to intelligently extract content from web pages, including articles, markdown, plain text, links, and custom structured data. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
