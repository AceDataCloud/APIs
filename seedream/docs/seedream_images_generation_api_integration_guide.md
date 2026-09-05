# Seedream Images Generation API Integration Instructions

This article introduces the Seedream Images Generation API integration, generating and editing ByteDance Seedream (Doubao) images via custom parameters.

## Application Process

Apply for the service on the [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) page and click "Acquire". First-time applicants get a free quota. **One API token calls every platform service.**

## Basic Usage

Request body fields:

- `model`: one of `doubao-seedream-5-0-pro-260628`, `doubao-seedream-5-0-260128`, `doubao-seedream-5-0-lite-260128`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828`. Pass the complete model string; abbreviations return 400.
- `prompt`: image description (required).
- `size`: output resolution, either a preset (`1K`, `1.5K`, `2K`, `3K`, `4K`, or `auto`) or an explicit pixel size such as `2048x2048`; supported presets vary by model.
- `image`: source image URL/Base64 string or an array of image URLs/Base64 values for editing (up to 14 entries). All supported models accept image input.
- `sequential_image_generation`: set to `auto` to generate related image sets; `disabled` by default. `sequential_image_generation_options.max_images` accepts 1-15.
- `stream`: enables streaming output when supported.
- `response_format`: `url` (default) or `b64_json`.
- `watermark`: whether to add a watermark.
- `output_format`: `jpeg` or `png` for supported models.
- `tools`: currently supports `{ "type": "web_search" }` for online search on supported models.
- `optimize_prompt_options.mode`: `standard` or `fast`.
- `layer_decomposition`: request layer decomposition when supported.
- `background`: `transparent` or `opaque` when supported.
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
  "data": [
    {
      "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png",
      "model": "doubao-seedream-5-0-260128"
    }
  ]
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

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | bad_request | Invalid model/params |
| 401 | invalid_token / token_expired | Token bad |
| 500 | internal_error | Upstream error |
