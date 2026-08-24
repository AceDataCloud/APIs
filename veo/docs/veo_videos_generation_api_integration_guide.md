# Veo Videos Generation API Integration Guide

Use `POST https://api.acedata.cloud/veo/videos` to generate Google Veo videos.

## Request

Current models are Veo 3 and Veo 3.1 variants, including the ingredients variant. `veo2` and `veo2-fast` are no longer supported.

```bash
curl -X POST 'https://api.acedata.cloud/veo/videos' \
  -H 'Authorization: ******' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "veo31-fast",
    "prompt": "A ceramic mug rotating in morning light",
    "aspect_ratio": "16:9",
    "async": true
  }'
```

| Parameter | Description |
| --- | --- |
| `model` | A supported Veo 3 or Veo 3.1 model. |
| `prompt` | Text instruction for the video. |
| `image_urls` | Optional reference images. Image limits depend on the model; the ingredients variant supports multi-image input. |
| `aspect_ratio` | Output aspect ratio. |
| `resolution` | Requested output resolution, supported values depending on the model. |
| `async` | When `true`, returns immediately with a task ID. |
| `callback_url` | Optional URL that receives the completed result. |

## Asynchronous Results

Set `async: true` to receive a `task_id` immediately, then query [Veo Tasks](veo_tasks_api_integration_guide.md). Supplying `callback_url` sends the completed result to that URL instead.

Successful responses include `success`, `task_id`, `trace_id`, and generated items in `data`, including their `video_url` and state.

## Errors

Error responses contain `success: false`, an `error` object, and `trace_id`. Check request parameters, bearer-token validity, and rate limits before retrying.
