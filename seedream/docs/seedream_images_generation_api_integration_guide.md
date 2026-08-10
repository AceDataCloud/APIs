# Seedream Images Generation API Integration Instructions

This article introduces the Seedream Images Generation API integration, generating and editing ByteDance Seedream (Doubao) images via custom parameters.

## Application Process

Get an API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications). **One API token calls every platform service.** New accounts receive a free quota; recharge shared balance in the [console](https://platform.acedata.cloud/console/coin) when needed.

## Basic Usage

Request body fields:

- `model`: one of `doubao-seedream-5-0-pro-260628`, `doubao-seedream-5-0-260128`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828`.
- `prompt`: image description (required).
- `size`: output resolution; supported presets vary by model. 5.0 Pro supports `1K`/`2K`, 5.0 Lite supports `2K`/`3K`/`4K`, 4.5 supports `2K`/`4K`, and 4.0 supports `1K`/`2K`/`4K`.
- `image`: source image URL or Base64 value array for editing. All supported models accept image input.
- `sequential_image_generation`: generate a related image set; supported by 5.0 Lite, 4.5, and 4.0. Use `sequential_image_generation_options.max_images` to set its size.
- `stream`: enable streaming output; supported by 5.0 Lite, 4.5, and 4.0.
- `response_format`: `url` (default) or `b64_json`.
- `watermark`: whether to add a watermark (default `true`).
- `output_format`: `jpeg` (default) or `png`; supported by 5.0 Pro and 5.0 Lite.
- `tools`: use `web_search`; supported by 5.0 Lite.
- `optimize_prompt_options.mode`: prompt-optimization mode.
- `callback_url` / `async`: async modes; `async: true` returns a `task_id` polled via Seedream Tasks API.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/images' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "a serene mountain lake at sunrise, photorealistic",
    "size": "2K"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": [{
    "prompt": "a serene mountain lake at sunrise, photorealistic",
    "size": "2048x2048",
    "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png"
  }]
}
```

## Image Editing

Use a supported model with the `image` array:

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "make the sky golden hour, add warm tone",
  "image": ["https://example.com/photo.png"]
}
```

## Asynchronous Processing

Set `callback_url` to receive the result as a POST JSON callback. Alternatively, set `async` to `true` to receive a `task_id` immediately, then poll `/seedream/tasks` until the task completes.

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | bad_request | Invalid model/params |
| 401 | invalid_token / token_expired | Token bad |
| 403 | used_up | Insufficient balance or restricted access |
| 404 | no_api | Invalid endpoint |
| 413 | request_too_large | Request body too large |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | api_error | Upstream error |
