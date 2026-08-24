# Wan Videos Generation API Integration Guide

`POST https://api.acedata.cloud/wan/videos` generates Wan videos. Use an `Authorization` bearer token and a JSON request body.

## Request

`model` is the only field required for every request. Current models include `wan3.0-video` and the Wan 2.6 models supported by the selected generation mode. Supply `prompt` for text-to-video, or `media` for image/video-guided generation.

```bash
curl -X POST 'https://api.acedata.cloud/wan/videos' \
  -H 'Authorization: ******' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "wan3.0-video",
    "prompt": "A cinematic aerial shot of a mountain lake at sunrise",
    "duration": 5,
    "ratio": "16:9",
    "async": true
  }'
```

## Parameters

| Parameter | Description |
| --- | --- |
| `model` | Required. The Wan model to use. |
| `prompt` | Text instruction for the video. |
| `media` | Optional reference media for supported image/video-guided models. |
| `ratio` | Output aspect ratio. Use `adaptive` when the model supports adapting to reference media. |
| `duration` | Video duration. Supported values are model-specific: use 2–30 seconds or `-1` for automatic duration where supported. |
| `seed` | Optional integer seed for reproducible generation. |
| `watermark` | Whether to add a watermark when supported. |
| `async` | When `true`, returns immediately with a task ID. |
| `callback_url` | Optional URL that receives the completed result. |

## Asynchronous Results

Set `async` to `true` or provide a `callback_url` for long-running generation. The immediate response includes a `task_id` and `trace_id`. Poll the [Wan Tasks API](wan_tasks_api_integration_guide.md) using the task ID, or receive the final result at `callback_url`.

## Error Handling

Errors return a standard object with `success: false`, an `error.code`, an `error.message`, and `trace_id`. Common errors include invalid request parameters (`400`), an invalid token (`401`), rate limiting (`429`), and internal API errors (`500`).
