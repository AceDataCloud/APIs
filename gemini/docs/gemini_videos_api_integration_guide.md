# Gemini Videos Generation API Integration Guide

This document describes the integration instructions for the Gemini Videos Generation API, which generates Google Gemini (omni-flash) videos from a text prompt and optional reference images.

## Application Process

To use the Gemini Videos Generation API, first visit [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in or registering, you will be automatically returned to the current page.

A single API Token grants access to all platform services. There is a free quota available for first-time applicants, allowing you to use the API for free.

> 📘 Full documentation: [Gemini Videos Generation API →](https://platform.acedata.cloud/documents/gemini-videos)

## Basic Usage

To generate a video, provide a text `prompt`, the `model`, and optionally an `aspect_ratio`.

**Request Headers:**

- `accept`: Response format, set to `application/json`.
- `authorization`: Your API key, prefixed with `******

**Request Body:**

- `prompt`: Text prompt describing the video content. **Required.**
- `model`: Video generation model. Currently only `omni-flash` is supported (default: `omni-flash`).
- `aspect_ratio`: Aspect ratio of the generated video — `16:9` (landscape) or `9:16` (portrait). Default: `16:9`.
- `image_urls`: Optional array of reference image (or video) URLs to guide generation. Empty entries are ignored.
- `callback_url`: Optional async callback URL. When set, the API returns a `task_id` immediately and POSTs the result to this URL on completion.
- `async`: Optional. When `true`, the API returns a `task_id` immediately without waiting for generation to finish. Poll the [Gemini Tasks API](gemini_tasks_api_integration_guide.md) to retrieve the result.

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/gemini/videos' \
  -H 'authorization: ******' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -d '{
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
  }'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/gemini/videos"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "success": true,
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "data": [
    {
      "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
      "video_url": "https://cdn.acedata.cloud/gemini/example-video.mp4",
      "state": "succeeded"
    }
  ]
}
```

Response fields:

- `success`: Whether the video generation request succeeded.
- `task_id`: ID of this video generation task.
- `trace_id`: Trace ID for this request, useful for debugging.
- `data`: List of generated video results.
  - `id`: Unique identifier of the generated video.
  - `video_url`: URL of the generated video.
  - `state`: Task state — `pending`, `succeeded`, or `failed`.

Use the `video_url` from `data` to retrieve the generated video.

## Image-to-Video

To generate a video guided by reference images, pass one or more image URLs in the `image_urls` field:

```json
{
  "prompt": "The character slowly turns around and smiles at the camera",
  "model": "omni-flash",
  "aspect_ratio": "9:16",
  "image_urls": [
    "https://cdn.acedata.cloud/example-reference.png"
  ]
}
```

## Async Generation

Video generation may take some time to complete. To avoid holding a long connection open, set `async` to `true` (or provide a `callback_url`). The API will return a `task_id` immediately:

```json
{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9",
  "async": true
}
```

Immediate response:

```json
{
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea"
}
```

Use the [Gemini Tasks API](gemini_tasks_api_integration_guide.md) to poll for the result.

## Callback URL

Alternatively, provide a `callback_url` and the API will POST the final result to that address when generation is complete:

```json
{
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "model": "omni-flash",
  "aspect_ratio": "16:9",
  "callback_url": "https://your-domain.com/callback/gemini"
}
```

## Error Handling

| Status | Error Code | Description |
| ------ | ---------- | ----------- |
| 400 | `bad_request` | Invalid parameters, e.g. missing `prompt` or invalid `aspect_ratio`. |
| 401 | `invalid_token` | Authentication failed — token is invalid or wrong. |
| 403 | `used_up` | Insufficient balance, or prompt blocked by content policy. |
| 500 | `api_error` | Internal server error or upstream generation failure. |

Error response example:

```json
{
  "error": {
    "code": "bad_request",
    "message": "prompt is required when generate video."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```
