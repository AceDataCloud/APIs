# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. You can drive an existing Kling video with audio or text so the character speaks in sync.

## Basic Usage

- **Endpoint**: `POST https://api.acedata.cloud/kling/lip-sync`
- **Request format**: `application/json`
- **Response format**: `application/json`
- **Pricing**: **2.45 Credits** per successful call

This API works well with `/kling/videos` `image2video` to build talking-photo and digital-human narration workflows.

## Request Headers

| Field | Value | Description |
| --- | --- | --- |
| `authorization` | Use your API access key | Your API key, [get it here](https://platform.acedata.cloud) |
| `content-type` | `application/json` | Request body format |
| `accept` | `application/json` | Response format |

## Request Body

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `mode` | string | yes | — | Generation mode. Enum: `audio2video`, `text2video` |
| `video_id` | string | one-of | — | ID of a Kling-generated video (for example, the `video_id` returned by `/kling/videos` `image2video`). Only 5s or 10s videos generated within the last 30 days are supported. Provide `video_id` or `video_url` |
| `video_url` | string | one-of | — | Public URL of a video. Supported formats: `.mp4` and `.mov`, up to 100MB, 2–10 seconds, 720p or 1080p, with dimensions between 720px and 1920px. Provide `video_url` or `video_id` |
| `audio_url` | string | conditional | — | Download URL of the driving audio. Required when `mode=audio2video` and `audio_type=url`. Supported formats: `.mp3`, `.wav`, `.m4a`, `.aac`, up to 5MB |
| `audio_type` | string | no | `url` | How audio is supplied. Enum: `url`, `file` |
| `audio_file` | string | conditional | — | Base64-encoded audio file. Required when `audio_type=file`. Supported formats are the same as `audio_url`, up to 5MB |
| `text` | string | conditional | — | Text to speak. Required when `mode=text2video`. Maximum 120 characters |
| `voice_id` | string | conditional | — | Voice ID. Required when `mode=text2video` |
| `voice_language` | string | no | `zh` | Voice language. Enum: `zh`, `en` |
| `voice_speed` | float | no | `1.0` | Speech rate, range `0.8` to `2.0`, one decimal place |
| `callback_url` | string | no | — | Callback URL. If provided, or if `async=true`, the API returns a `task_id` immediately and sends the result asynchronously |
| `async` | boolean | no | `false` | When `true`, the API returns a `task_id` immediately. You can then poll `/kling/tasks` or receive the result through `callback_url` |

## Request Examples

### Audio-driven (`audio2video`)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  -d '{
    "mode": "audio2video",
    "video_id": "895055164389466178",
    "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav"
  }'
```

### Text-driven (`text2video`)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  -d '{
    "mode": "text2video",
    "video_id": "895055164389466178",
    "text": "Hi, long time no see. I am doing well, take care of yourself.",
    "voice_id": "genshin_vindi2",
    "voice_language": "en",
    "voice_speed": 1.0
  }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "07a3ec65-9f7e-4a09-b7b7-282684082527",
  "video_id": "895055968777281546",
  "video_url": "https://platform2.cdn.acedata.cloud/kling/07a3ec65-9f7e-4a09-b7b7-282684082527.mp4",
  "duration": "4.966",
  "state": "succeed"
}
```

The returned result contains multiple fields:

- `success`: whether the call succeeded.
- `task_id`: the task ID, which can be used with `/kling/tasks` to query progress later.
- `video_id`: the Kling ID of the generated video. You can reuse it for subsequent `extend` or `lip-sync` requests.
- `video_url`: the URL of the generated talking video.
- `duration`: the duration of the generated video in seconds.
- `state`: the task status, such as `succeed` or `failed`.

## Async Mode

When `callback_url` or `async: true` is provided, the API returns immediately with a `task_id`. You can then:

- Poll `POST /kling/tasks` with body `{ "action": "retrieve", "id": "<task_id>" }`
- Receive the final result through your `callback_url`

## Full Pipeline Example

```bash
# Step 1: animate a still image and get a video_id
curl -X POST 'https://api.acedata.cloud/kling/videos' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  -d '{"model":"kling-v2-1-master","action":"image2video","start_image_url":"https://cdn.acedata.cloud/4hfydw.jpg","prompt":"look at camera, natural","duration":5,"mode":"pro"}'

# Step 2: lip-sync the generated video with audio
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'accept: application/json' \
  -d '{"mode":"audio2video","video_id":"895055164389466178","audio_url":"https://your.cdn/voice.mp3"}'
```

## Error Response

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "one of video_id or video_url is required"
  },
  "trace_id": "f07cab09-3c18-4d74-9030-64ee840d9f16",
  "task_id": "f490537f-2e5c-4739-8149-6252fba2091c"
}
```

Common error codes:

- `400 bad_request`: Missing or invalid parameters
- `401 authorization_missing`: Missing or invalid API key
- `403 forbidden`: Blocked by content moderation
- `429 too_many_requests`: Upstream concurrency limit reached
- `500 api_error`: Upstream or internal service error

## Notes

- `video_id` must be a Kling video generated within the last 30 days and must be 5 or 10 seconds long. Otherwise, use `video_url`.
- For best lip-sync results, use a clear, front-facing, single-person video.
- Audio or text length should match the video duration, and the audio should not be longer than the video.
- Billing occurs only when the request succeeds.
