# Grok Videos API Integration Guide

xAI Grok provides a powerful AI video generation capability. By inputting a text prompt or a reference image, you can generate high-quality videos using the Grok Videos API.

This document mainly introduces the usage process of the Grok Videos API, allowing you to easily utilize the official Grok video generation features.

## Application Process

To use the Grok Videos API, you can first visit the [Grok Videos API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be) page and click the "Acquire" button to obtain the credentials needed for the request.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

Upon the first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

The Grok Videos API supports generating videos from a text prompt (text-to-video) or a reference image (image-to-video).

### Request Parameters

- `prompt`: The text description of the video you want to generate.
- `model`: The model to use for video generation. Currently supports:
  - `grok-imagine-video-1.5-fast` (default) — faster generation
  - `grok-imagine-video-1.5` — higher quality generation
- `image_url`: Optional. The URL of a reference image for image-to-video generation.
- `reference_image_urls`: Optional. An array of reference image URLs.
- `aspect_ratio`: Optional. The aspect ratio of the generated video. Supported values: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`.
- `resolution`: Optional. The resolution of the generated video. Supported values: `480p` (default), `720p`, `1080p`.
- `duration`: Optional. The duration of the video in seconds, between 1 and 30. Default is `6`.
- `callback_url`: Optional. A URL to receive the result asynchronously via a POST request.
- `async`: Optional. Set to `true` to return immediately with a `task_id` for asynchronous retrieval.

### Text-to-Video Example

The following example generates a video from a text prompt:

```bash
curl -X POST 'https://api.acedata.cloud/grok/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "grok-imagine-video-1.5-fast",
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "duration": 6
}'
```

Python sample code:

```python
import requests

url = "https://api.acedata.cloud/grok/videos"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "model": "grok-imagine-video-1.5-fast",
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "duration": 6
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

After a successful request, the API returns a response like:

```json
{
  "success": true,
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "data": [
    {
      "id": "grok-imagine-video-1.5-fast:41eb9a5f-3b2d-4d1e-9f5a-6c2f1a0b9e77",
      "video_url": "https://cdn.acedata.cloud/c8cbf53aa0.mp4",
      "state": "succeeded"
    }
  ]
}
```

The returned fields are:

- `success`: Whether the request was successful.
- `task_id`: The ID of this video generation task, used to query task status via the Tasks API.
- `trace_id`: A unique trace ID for this request.
- `data`: An array of generated video results, each containing:
  - `id`: The ID of the generated video item.
  - `video_url`: The URL of the generated video.
  - `state`: The state of the video item — `pending`, `succeeded`, or `failed`.

## Image-to-Video Functionality

To generate a video based on a reference image, supply the `image_url` parameter alongside your prompt:

```python
import requests

url = "https://api.acedata.cloud/grok/videos"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "model": "grok-imagine-video-1.5-fast",
    "prompt": "The cat slowly wakes up and stretches",
    "image_url": "https://cdn.acedata.cloud/5hmkdg.jpg",
    "aspect_ratio": "16:9",
    "duration": 6
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Asynchronous Callback

Since video generation can take some time, the API supports asynchronous operation via a `callback_url`. When specified, the API returns a `task_id` immediately, and once the video is ready the result is POSTed to your callback URL.

```bash
curl -X POST 'https://api.acedata.cloud/grok/videos' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "grok-imagine-video-1.5-fast",
  "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
  "callback_url": "https://webhook.site/your-unique-url"
}'
```

The immediate response will be:

```json
{
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea"
}
```

After generation completes, the full result is sent to your `callback_url`.

You can also poll the task status using the [Grok Tasks API](grok_tasks_api_integration_guide.md).

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Bad request, possibly due to missing or invalid parameters (e.g., `prompt is required for text-to-video.`).
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `403 used_up`: Your balance is not sufficient for the current request.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "error": {
    "code": "bad_request",
    "message": "prompt is required for text-to-video."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Conclusion

Through this document, you have learned how to use the Grok Videos API to generate videos from text prompts and reference images. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
