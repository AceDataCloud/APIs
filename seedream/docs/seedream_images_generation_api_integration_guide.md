# Seedream Images API integration guide

Use `POST https://api.acedata.cloud/seedream/images` with an AceDataCloud bearer token. Acquire a token from the [Seedream API page](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e).

## Seedream 5.0 capability matrix

| Capability | 5.0 Pro | 5.0 Lite |
|---|---|---|
| Model | `doubao-seedream-5-0-pro-260628` | `doubao-seedream-5-0-260128` (alias `doubao-seedream-5-0-lite-260128`) |
| Single image generation/editing | Yes | Yes |
| Reference images | Up to 10 | Up to 14 |
| Sequential images / streaming / web search | No | Yes |
| Layer decomposition / transparent background | Yes | No |
| Prompt optimization | `standard`, `fast` | `standard` |
| Preset sizes | `1K`, `1.5K`, `2K` | `2K`, `3K`, `4K` |

Explicit `WIDTHxHEIGHT` values are accepted within each model's pixel and aspect-ratio limits. Seedream 4.5 and 4.0 remain supported for compatibility.

## Generate or edit images

```bash
curl https://api.acedata.cloud/seedream/images \
  -H 'Authorization: Bearer YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "a four-panel storyboard of a courier crossing a rainy neon city",
    "size": "2K",
    "sequential_image_generation": "auto",
    "sequential_image_generation_options": {"max_images": 4},
    "watermark": false
  }'
```

Add `image` as one URL/Base64 string or an array for editing. Lite requires input image count plus requested outputs to be at most 15. `response_format` is `url` or `b64_json`; Pro/Lite `output_format` is `jpeg` or `png`. Lite supports `tools: [{"type":"web_search"}]` when current information matters.

## Transparent-background Pro edit

```json
{
  "model": "doubao-seedream-5-0-pro-260628",
  "prompt": "replace the parrot with a peacock",
  "image": "https://example.com/transparent-layer.png",
  "background": "transparent",
  "output_format": "png",
  "size": "1.5K"
}
```

This mode requires exactly one transparent PNG input. `background: transparent` cannot be combined with JPEG output or layer decomposition.

## Decompose one image into editable layers

```json
{
  "model": "doubao-seedream-5-0-pro-260628",
  "image": "https://example.com/poster.png",
  "layer_decomposition": true,
  "size": "auto",
  "watermark": false
}
```

`prompt` is optional: omit it for automatic decomposition, describe desired elements, or use normalized `<bbox>` coordinates. The result has one base image (`z_index: 0`) plus up to 16 transparent PNG layers. Layer objects may contain `name`, `description`, and `bounding_box.absolute`/`normalized`. Draw layers in ascending `z_index` at their bounding-box positions to reconstruct the image. Any failed layer fails the whole Pro decomposition.

## Async and streaming

Use `"async": true` to return a `task_id`, then poll `POST /seedream/tasks` with `{"action":"retrieve","id":"..."}`. A real public `callback_url` can receive the result instead.

Lite/4.x streaming uses `"stream": true` and `Accept: application/x-ndjson`. Read one JSON event per line until `image_generation.completed`. Do not combine streaming with `async` or `callback_url`.

## Response fields

A normal response includes `success`, `task_id`, `trace_id`, `data`, optional `tools`, and `usage`. Each data item can contain `image_url` or `b64_json`, `size`, and `output_format`. Lite image sets can include per-item `error` objects without discarding successful items. Layer responses additionally include `z_index`, `name`, `description`, and bounding boxes.

Result URLs are temporary; persist files promptly. Current Credits are listed on the [live pricing page](https://platform.acedata.cloud/services/seedream?tab=pricing). Pro outputs are billed individually by actual size; layer outputs use the layer price tier. Lite bills only successful outputs.

## Error codes

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `bad_request` | Unsupported model/parameter combination or invalid input |
| 401 | `invalid_token`, `token_expired` | Invalid authentication |
| 403 | `used_up`, `forbidden` | Insufficient balance or blocked content |
| 429 | `too_many_requests` | Rate limited |
| 500 | `api_error` | Service error |
