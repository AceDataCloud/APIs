# Gemini Videos API Integration Guide

Google Gemini supports AI video generation from text prompts and optional reference images using the `omni-flash` model. This document describes how to generate videos with the Gemini Videos API and how to retrieve the results of async video generation tasks using the Gemini Tasks API.

## Application Process

To use the Gemini Videos API, visit the [Gemini Videos API](https://platform.acedata.cloud/documents/gemini-videos-api) page and click the "Acquire" button to obtain the credentials needed for the request.

If you are not logged in or registered, you will be automatically redirected to the login page. Upon the first application, there will be a free quota provided.

## Basic Usage

Send a POST request to `/gemini/videos`:

```bash
curl -X POST "https://api.acedata.cloud/gemini/videos" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
  }'
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Text prompt describing the video to generate |
| `model` | string | No | Model to use. Currently supports `omni-flash` (default: `omni-flash`) |
| `aspect_ratio` | string | No | Aspect ratio of the output video. Options: `16:9`, `9:16` (default: `16:9`) |
| `image_urls` | array | No | Optional list of reference image URLs for image-to-video generation |
| `callback_url` | string | No | URL to receive the result when the task completes |
| `async` | boolean | No | When `true`, returns a task ID immediately without waiting for the video to complete |

### Synchronous Response

When `async` is `false` (default), the API waits for the video to complete and returns the result directly:

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

- `success`: Whether the request was successful.
- `task_id`: The unique ID of the video generation task.
- `trace_id`: Trace ID for debugging purposes.
- `data`: Array of generated video results. Each item contains:
  - `id`: Job ID for the generated video.
  - `video_url`: URL of the generated video file.
  - `state`: Task state, one of `pending`, `succeeded`, or `failed`.

### Asynchronous Generation

For long-running video generation, you can use async mode by setting `"async": true`. The API returns a task ID immediately, and you can poll the task status using the Gemini Tasks API.

```bash
curl -X POST "https://api.acedata.cloud/gemini/videos" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A timelapse of a flower blooming at dawn",
    "model": "omni-flash",
    "aspect_ratio": "16:9",
    "async": true
  }'
```

Response:

```json
{
  "success": true,
  "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "data": [
    {
      "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
      "video_url": null,
      "state": "pending"
    }
  ]
}
```

## Image-to-Video Generation

You can provide one or more reference images using `image_urls` to guide the video generation:

```bash
curl -X POST "https://api.acedata.cloud/gemini/videos" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "The cat slowly wakes up and stretches",
    "model": "omni-flash",
    "image_urls": ["https://example.com/cat.jpg"]
  }'
```

## Retrieving Task Results

Use the Gemini Tasks API (`/gemini/tasks`) to retrieve the status and result of an async video generation task.

### Retrieve a Single Task

```bash
curl -X POST "https://api.acedata.cloud/gemini/tasks" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
    "action": "retrieve"
  }'
```

### Retrieve Multiple Tasks

```bash
curl -X POST "https://api.acedata.cloud/gemini/tasks" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": [
      "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
      "omni-flash:job_02k888ijscgsht3171r6awg3b6"
    ],
    "action": "retrieve_batch"
  }'
```

### Tasks Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | No | Single task ID to retrieve (used with `action: retrieve`) |
| `ids` | array | No | List of task IDs to retrieve (used with `action: retrieve_batch`) |
| `action` | string | No | Operation type. Options: `retrieve` (default), `retrieve_batch` |

### Tasks Response

```json
{
  "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
  "request": {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash"
  },
  "response": {
    "video_url": "https://cdn.acedata.cloud/gemini/example-video.mp4",
    "state": "succeeded"
  }
}
```

## Error Handling

| HTTP Status Code | Error Code | Meaning |
|-----------------|------------|---------|
| 400 | `bad_request` | Invalid request parameters, e.g. missing required `prompt` |
| 401 | `invalid_token` | Authentication failed, please check your API token |
| 403 | `used_up` | Insufficient balance, please top up in Ace Data Cloud |
| 500 | `api_error` | Internal server error |

### Error Response Example

```json
{
  "error": {
    "code": "bad_request",
    "message": "prompt is required when generate video."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```
