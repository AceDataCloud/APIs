# Kling Talking Photo API Integration Guide

Turn one photo and one audio file into a talking video in a single call.

## Endpoint

- Method: `POST`
- URL: `https://api.acedata.cloud/kling/talking-photo`
- Authentication: Include an `authorization` header with your bearer token.
- Content-Type: `application/json`

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `image_url` | string | Yes | Public portrait image URL. |
| `audio_url` | string | Yes | Public audio URL (for example `.mp3`, `.wav`, `.m4a`, `.aac`). |
| `prompt` | string | No | Motion or expression hint for generation. |
| `model` | string | No | Model for animation step. Enum: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`. |
| `duration` | integer | No | Video duration. Enum: `5`, `10`. |
| `mode` | string | No | Quality mode. Enum: `std`, `pro`. |
| `callback_url` | string | No | Callback URL. |
| `async` | boolean | No | Async mode. When true, returns `task_id` immediately. |

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/kling/talking-photo' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
    "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav",
    "duration": 5
  }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "video_id": "895055968777281546",
  "video_url": "https://platform2.cdn.acedata.cloud/kling/07a3ec65-9f7e-4a09-b7b7-282684082527.mp4",
  "source_video_url": "https://platform2.cdn.acedata.cloud/kling/163ac822-1a15-4f5e-a2eb-465154df15af.mp4",
  "duration": 5,
  "state": "succeed"
}
```
