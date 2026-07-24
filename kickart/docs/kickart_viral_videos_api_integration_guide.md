# Kickart Viral Videos API Integration Guide

This guide was generated from the upstream Kickart OpenAPI spec because no English MDX guide is currently published in `AceDataCloud/Docs`. Use it as the local integration reference for `/kickart/viral-videos`.

## Application Process

Create or reuse your Ace Data Cloud API token in the Kickart service page, then call the endpoint below with `application/json` request bodies. One token can be reused across Ace Data Cloud services.

## Endpoint

`POST https://api.acedata.cloud/kickart/viral-videos`

## Request Fields

- `mode` — Kickart Viral Videos Mode (optional; allowed values: pro, advanced; default: `pro`).
- `template_id` — Kickart Viral Videos Template Id (optional).
- `ref_video` — Kickart Viral Videos Ref Video (required).
- `product_url` — Kickart Viral Videos Product Url (optional).
- `product_id` — Kickart Viral Videos Product Id (optional).
- `product_images` — Kickart Viral Videos Product Images (optional).
- `model_images` — Kickart Viral Videos Model Images (optional).
- `language` — Kickart Viral Videos Language (required; allowed values: zh, en, en-us, pt-br, ja, es-mx, id, ms, tl).
- `ai_product_analysis` — Kickart Viral Videos Ai Product Analysis (optional; default: `True`).
- `similarity` — Kickart Viral Videos Similarity (optional; allowed values: high, medium; default: `medium`).
- `nle_subtitle_enabled` — Kickart Viral Videos Nle Subtitle Enabled (optional; default: `True`).
- `use_subtitle_erasure` — Kickart Viral Videos Use Subtitle Erasure (optional; default: `False`).
- `prompt` — Kickart Viral Videos Prompt (optional).
- `location_images` — Kickart Viral Videos Location Images (optional).
- `watermark` — Kickart Viral Videos Watermark (optional; default: `False`).
- `callback_url` — Kickart Viral Videos Callback Url (optional).
- `async` — Kickart Viral Videos Async (optional).

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/kickart/viral-videos" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
  "template_id": "1690784258",
  "ref_video": "https://example.com/resource",
  "product_url": "https://example.com/resource",
  "language": "zh",
  "prompt": "Create a short product showcase video."
}'
```

## Response Example

```json
{
  "success": true,
  "task_id": "7621886649043206198",
  "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
  "data": {
    "task_id": "7621886649043206198",
    "video_url": "https://cdn.acedata.cloud/kickart/example.mp4",
    "usage": 1.75,
    "template_id": "208714754",
    "mode": "pro"
  }
}
```

## Asynchronous Usage

This endpoint supports asynchronous processing. Pass `callback_url` to receive the final result via webhook, or set `async` to `true` when you want the API to return a `task_id` immediately and handle polling in your own workflow.

## Notes

- Authentication uses the shared Ace Data Cloud bearer token in the `authorization` header.
- Response payloads return `task_id` values for downstream tracking and asynchronous workflows.
- Refer to the Kickart README in this package for the full endpoint list.
