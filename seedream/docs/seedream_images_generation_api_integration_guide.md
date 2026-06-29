# Seedream Images Generation API Integration Instructions

This article introduces the Seedream Images Generation API integration, generating and editing ByteDance Seedream (Doubao) images via custom parameters.

## Application Process

Apply for the service on the [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) page and click "Acquire". First-time applicants get a free quota. **One API token calls every platform service.**

## Basic Usage

Request body fields:

- `model`: one of `doubao-seedream-5-0-260128`, `doubao-seedream-5.0-lite`, `doubao-seedream-4-5-251128`, `doubao-seedream-4-0-250828`, `doubao-seedream-3-0-t2i-250415`, `doubao-seededit-3-0-i2i-250628`.
- `prompt`: image description (required).
- `size`: output resolution `1K` / `2K` / `4K`.
- `image_url`: source image for editing (SeedEdit `doubao-seededit-3-0-i2i-250628`).
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
  "data": { "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png", "model": "doubao-seedream-5-0-260128" }
}
```

## Image Editing (SeedEdit)

Use `doubao-seededit-3-0-i2i-250628` with `image_url`:

```json
{
  "model": "doubao-seededit-3-0-i2i-250628",
  "prompt": "make the sky golden hour, add warm tone",
  "image_url": "https://example.com/photo.png"
}
```

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | bad_request | Invalid model/params |
| 401 | invalid_token / token_expired | Token bad |
| 500 | internal_error | Upstream error |
