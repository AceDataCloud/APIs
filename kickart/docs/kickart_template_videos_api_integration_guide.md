# Kickart Template Videos API Integration Guide

This guide was generated from the upstream Kickart OpenAPI spec because no English MDX guide is currently published in `AceDataCloud/Docs`. Use it as the local integration reference for `/kickart/template-videos`.

## Application Process

Create or reuse your Ace Data Cloud API token in the Kickart service page, then call the endpoint below with `application/json` request bodies. One token can be reused across Ace Data Cloud services.

## Endpoint

`POST https://api.acedata.cloud/kickart/template-videos`

## Request Fields

- `template_id` — Kickart Template Videos Template Id (required).
- `resource_list` — Kickart Template Videos Resource List (required).
- `resolution` — Kickart Template Videos Resolution (optional).
- `watermark` — Kickart Template Videos Watermark (optional).
- `callback_url` — Kickart Template Videos Callback Url (optional).
- `async` — Kickart Template Videos Async (optional).

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/kickart/template-videos" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
  "template_id": "1690784258",
  "resource_list": [
    "resource-1"
  ]
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
    "usage": 0.36,
    "template_id": "1690784258"
  }
}
```

## Asynchronous Usage

This endpoint supports asynchronous processing. Pass `callback_url` to receive the final result via webhook, or set `async` to `true` when you want the API to return a `task_id` immediately and handle polling in your own workflow.

## Notes

- Authentication uses the shared Ace Data Cloud bearer token in the `authorization` header.
- Response payloads return `task_id` values for downstream tracking and asynchronous workflows.
- Refer to the Kickart README in this package for the full endpoint list.
