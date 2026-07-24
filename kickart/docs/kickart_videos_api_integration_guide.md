# Kickart Videos API Integration Guide

This guide was generated from the upstream Kickart OpenAPI spec because no English MDX guide is currently published in `AceDataCloud/Docs`. Use it as the local integration reference for `/kickart/videos`.

## Application Process

Create or reuse your Ace Data Cloud API token in the Kickart service page, then call the endpoint below with `application/json` request bodies. One token can be reused across Ace Data Cloud services.

## Endpoint

`POST https://api.acedata.cloud/kickart/videos`

## Request Fields

- `mode` — Kickart Videos Mode (optional; allowed values: fast, pro; default: `fast`).
- `type` — Kickart Videos Type (optional; allowed values: intro, main; default: `intro`).
- `template_id` — Kickart Videos Template Id (optional).
- `product_url` — Kickart Videos Product Url (optional).
- `product_id` — Kickart Videos Product Id (optional).
- `user_images` — Kickart Videos User Images (optional).
- `user_videos` — Kickart Videos User Videos (optional).
- `duration` — Kickart Videos Duration (required; allowed values: 15, 30, 45, 60).
- `aspect_ratio` — Kickart Videos Aspect Ratio (optional; allowed values: 9:16, 16:9, 3:4, 4:3, 1:1; default: `9:16`).
- `language` — Kickart Videos Language (optional; allowed values: zh, en, en-us, pt-br, ja, es-mx, id, ms, tl; default: `zh`).
- `purpose` — Kickart Videos Purpose (optional).
- `prompt` — Kickart Videos Prompt (optional).
- `nle_subtitle_enabled` — Kickart Videos Nle Subtitle Enabled (optional; default: `True`).
- `use_subtitle_erasure` — Kickart Videos Use Subtitle Erasure (optional; default: `False`).
- `watermark` — Kickart Videos Watermark (optional; default: `False`).
- `callback_url` — Kickart Videos Callback Url (optional).
- `async` — Kickart Videos Async (optional).

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/kickart/videos" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
  "template_id": "1690784258",
  "product_url": "https://example.com/resource",
  "duration": 15,
  "aspect_ratio": "9:16",
  "language": "zh",
  "prompt": "Create a short product showcase video."
}'
```

## Response Example

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
  "data": {
    "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
    "video_url": "https://cdn.acedata.cloud/kickart/example.mp4",
    "produce_id": "1fe8d587-7eb3-4094-8624-1abc847e9248",
    "usage": 0.21,
    "template_id": "226527799033910",
    "mode": "fast",
    "type": "intro",
    "duration": 15
  }
}
```

## Asynchronous Usage

This endpoint supports asynchronous processing. Pass `callback_url` to receive the final result via webhook, or set `async` to `true` when you want the API to return a `task_id` immediately and handle polling in your own workflow.

## Notes

- Authentication uses the shared Ace Data Cloud bearer token in the `authorization` header.
- Response payloads return `task_id` values for downstream tracking and asynchronous workflows.
- Refer to the Kickart README in this package for the full endpoint list.
