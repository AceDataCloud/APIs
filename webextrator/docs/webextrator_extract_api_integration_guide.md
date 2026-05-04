# WebExtrator Extract API Integration Guide

`POST https://api.acedata.cloud/webextrator/extract`

The WebExtrator Extract API builds on top of the `/webextrator/render` endpoint by adding intelligent content extraction. In addition to all Render API parameters, it supports the following extra fields:

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
    "title": "Example Article",
    "author": "John Doe",
    "published_at": "2026-05-01",
    "content": "# Example Article\n\nBody text ...",
    "summary": "This article introduces ..."
  }
}
```

Async mode, error codes, and billing rules are identical to `/webextrator/render`.

## Example: Extract Article Body (with LLM)

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

## Example: Async + Custom Structured Extraction

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://shop.example.com/item/123",
    "expected_type": "structured",
    "enable_llm": true,
    "instruction": "Extract product title, price, inventory, and 3 main image URLs",
    "callback_url": "https://your-domain.com/wbx-callback"
  }'
```

## Conclusion

Through this document, you have learned how to use the WebExtrator Extract API to intelligently extract content from web pages. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
