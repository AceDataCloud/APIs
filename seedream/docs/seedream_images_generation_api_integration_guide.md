# Seedream Images Generation API Integration Instructions

This article introduces the Seedream Images Generation API integration, generating and editing ByteDance Seedream (Doubao) images via custom parameters.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. **A single API Token works across every service on the platform.** New accounts receive free starter credit.

## Basic Usage

Request body fields:

- `action`: operation type, use `generate` for text-to-image generation (required).
- `model`: generation model, default is `doubao-seedream-5.0-lite`. Supported models: `doubao-seedream-5.0-lite` (latest), `doubao-seedream-4.5`, `doubao-seedream-4.0`, `doubao-seedream-3.0-t2i`, `doubao-seededit-3.0-i2i`.
- `prompt`: image description (required).
- `image`: source image(s) for editing, URL or Base64. `doubao-seedream-5.0-lite`, `doubao-seedream-4.5`, and `doubao-seedream-4.0` support single or multiple images; `doubao-seededit-3.0-i2i` supports single image only; `doubao-seedream-3.0-t2i` does not support this parameter.
- `size`: output resolution. Preset values (`2K`/`3K`/`4K` for 5.0-lite; `2K`/`4K` for 4.5; `1K`/`2K`/`4K` for 4.0) or pixel dimensions (e.g. `2048x2048`). `doubao-seedream-3.0-t2i` and `doubao-seededit-3.0-i2i` support pixel dimensions only.
- `seed`: random seed in range `[-1, 2147483647]`. Only supported by `doubao-seedream-3.0-t2i`.
- `sequential_image_generation`: generate a set of related images. Supported by 5.0-lite, 4.5, and 4.0, default `disabled`.
- `stream`: enable streaming output. Supported by 5.0-lite, 4.5, and 4.0, default `false`.
- `guidance_scale`: prompt relevance strength in range `[1, 10]`. Default `2.5` for `doubao-seedream-3.0-t2i`, `5.5` for `doubao-seededit-3.0-i2i`, not supported by other models.
- `response_format`: return format of the generated image, `url` (default) or `b64_json`.
- `watermark`: whether to add a watermark, default `true`.
- `output_format`: file format of the generated image, `jpeg` (default) or `png`. Only supported by `doubao-seedream-5.0-lite`.
- `tools`: tools the model may call, currently supports `web_search`. Only supported by `doubao-seedream-5.0-lite`.
- `callback_url`: URL to receive async callback results.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/images' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "action": "generate",
    "model": "doubao-seedream-4-0-250828",
    "prompt": "a white siamese cat",
    "size": "2K"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "25027ba3-0430-4a1b-91c8-d2297f19ba73",
  "trace_id": "8043a9e9-692f-43b0-82f7-5890f798be38",
  "data": [
    {
      "prompt": "a white siamese cat",
      "size": "2048x2048",
      "image_url": "https://platform.cdn.acedata.cloud/seedream/3c060029-69b1-406f-a957-fcd55ddc9386.jpg"
    }
  ]
}
```

The `data` array contains the generation results. Each item includes:
- `image_url`: link to the generated image.
- `prompt`: the prompt text.
- `size`: pixel dimensions of the generated image.

## Image Editing Task

Use `doubao-seedream-5.0-lite`, `doubao-seedream-4.5`, `doubao-seedream-4.0`, or `doubao-seededit-3.0-i2i` with the `image` parameter:

```json
{
  "action": "generate",
  "model": "doubao-seededit-3.0-i2i",
  "prompt": "make the sky golden hour, add warm tone",
  "image": ["https://example.com/photo.png"]
}
```

## Asynchronous Callback

Specify a `callback_url` in the request. The API immediately returns a `task_id`, and sends the full result via POST JSON to your `callback_url` when the task completes.

```bash
curl -X POST 'https://api.acedata.cloud/seedream/images' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "action": "generate",
    "model": "doubao-seedream-4-0-250828",
    "prompt": "a white siamese cat",
    "callback_url": "https://your-server.example.com/callback"
  }'
```

Immediate response:

```json
{
  "task_id": "c9aaffa2-b8ac-40ff-8468-43e77cb9ddde"
}
```

Callback payload (sent to `callback_url` on completion):

```json
{
  "success": true,
  "task_id": "c9aaffa2-b8ac-40ff-8468-43e77cb9ddde",
  "trace_id": "131a40c3-2eaf-44c9-af28-c9b408577286",
  "data": [
    {
      "prompt": "a white siamese cat",
      "size": "2048x2048",
      "image_url": "https://platform.cdn.acedata.cloud/seedream/3e88db7e-4771-4f6a-adbd-5ae4590c5d59.jpg"
    }
  ]
}
```

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | token_mismatched | Token does not match the API |
| 400 | api_not_implemented | API not implemented |
| 400 | bad_request | Invalid model or parameters |
| 400 | no_token | No token specified |
| 401 | invalid_token | Token invalid or wrong |
| 401 | token_expired | Token expired |
| 401 | token_mismatched | Token and API do not match |
| 403 | used_up | Insufficient balance |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | api_error | Internal server error |
