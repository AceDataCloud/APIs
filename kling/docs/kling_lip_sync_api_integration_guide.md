# Kling Lip Sync API Integration Guide

This article introduces the Kling Lip Sync API integration instructions. By inputting a Kling video and an audio source or text, you can generate a video where the character speaks in sync (lip sync).

## Application Process

To use the API, you need to first apply for the corresponding service on the [Kling Lip Sync API](https://platform.acedata.cloud/documents/kling-lip-sync) page. After entering the page, click the "Acquire" button.

There will be a free quota offered for the first application, allowing you to use the API for free.

## Basic Usage

Drive an **existing Kling video** (5s or 10s) with audio or text so the character speaks in sync. The API supports two modes:

- `audio2video`: drive the video with an audio file or URL
- `text2video`: drive the video with text using a specified voice

You must provide either `video_id` (a Kling-generated video ID) or `video_url` (a public video URL), but not both.

### Request Headers

| Field | Value | Description |
| --- | --- | --- |
| `authorization` | `******` | Your API key |
| `content-type` | `application/json` | Request body format |
| `accept` | `application/json` | Response format |

### Request Body

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `mode` | string | yes | — | Generation mode. Options: `audio2video`, `text2video` |
| `video_id` | string | one-of | — | ID of a Kling-generated video (e.g. the `video_id` returned by `/kling/videos`). Only 5s/10s videos generated within the last 30 days. Provide `video_id` OR `video_url`, not both |
| `video_url` | string | one-of | — | Public URL of a video. Constraints: `.mp4`/`.mov`, ≤100MB, 2–10s, 720p/1080p only, dimensions 720–1920px. Provide `video_id` OR `video_url` |
| `audio_url` | string | conditional | — | Download URL of the driving audio. Required when `mode=audio2video` and `audio_type=url`. Formats `.mp3`/`.wav`/`.m4a`/`.aac`, ≤5MB |
| `audio_type` | string | no | `url` | How audio is supplied. Options: `url`, `file` |
| `audio_file` | string | conditional | — | Base64 of the audio file. Required when `audio_type=file`. Same formats, ≤5MB |
| `text` | string | conditional | — | Text to speak. Required when `mode=text2video`, max 120 characters |
| `voice_id` | string | conditional | — | Voice ID. Required when `mode=text2video` |
| `voice_language` | string | no | `zh` | Voice language. Options: `zh`, `en` |
| `voice_speed` | float | no | `1.0` | Speech rate, range `0.8`–`2.0` |
| `callback_url` | string | no | — | Callback URL for async mode |
| `async` | boolean | no | `false` | Async mode. When `true`, returns `task_id` immediately; poll via `/kling/tasks` |

## Request Examples

### Audio-Driven (audio2video)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895055164389466178",
  "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav"
}'
```

### Text-Driven (text2video)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "text2video",
  "video_id": "895055164389466178",
  "text": "Hi, long time no see. I am doing well, take care of yourself.",
  "voice_id": "genshin_vindi2",
  "voice_language": "en",
  "voice_speed": 1.0
}'
```

## Response

Upon successful request, the API returns the following result:

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

The returned result contains the following fields:

- `success`: whether the call succeeded.
- `task_id`: the task ID, usable with `/kling/tasks` to query status.
- `video_id`: the Kling ID of the generated video (reusable for further operations).
- `video_url`: the URL of the talking video hosted on our CDN.
- `duration`: the video duration in seconds.
- `state`: the task status, `succeed` or `failed`.

## Asynchronous Callback

Since the Kling Lip Sync API may take some time, the API also supports asynchronous callbacks. Provide a `callback_url` field or set `async=true` when making the request. The API immediately returns a result containing only a `task_id`. When the task completes, the result is sent via POST JSON to the specified `callback_url`.

You can also poll for the status using the `/kling/tasks` endpoint:

```bash
curl -X POST 'https://api.acedata.cloud/kling/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "id": "07a3ec65-9f7e-4a09-b7b7-282684082527",
  "action": "retrieve"
}'
```

## Full Pipeline: Talking Photo

You can combine `/kling/videos` image2video with `/kling/lip-sync` to build a complete talking-photo pipeline:

```bash
# Step 1: animate the photo
curl -X POST 'https://api.acedata.cloud/kling/videos' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "model": "kling-v2-1-master",
  "action": "image2video",
  "start_image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
  "prompt": "look at camera, natural",
  "duration": 5,
  "mode": "pro"
}'
# Returns: { "video_id": "895055164389466178", ... }

# Step 2: lip-sync it with audio
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "mode": "audio2video",
  "video_id": "895055164389466178",
  "audio_url": "https://your.cdn/voice.mp3"
}'
# Returns: { "video_url": "https://platform2.cdn.acedata.cloud/kling/....mp4", ... }
```

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 bad_request`: Missing or invalid parameters (e.g. no mode, video/audio conflict, text over 120 chars).
- `401 authorization_missing`: Missing or invalid API key.
- `403 forbidden`: Blocked by content moderation.
- `429 too_many_requests`: Too many requests, exceeded the rate limit.
- `500 api_error`: Internal server error.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "bad_request",
    "message": "one of video_id or video_url is required"
  },
  "trace_id": "f07cab09-3c18-4d74-9030-64ee840d9f16"
}
```

## Notes

- `video_id` must be a Kling video generated within 30 days and either 5s or 10s; otherwise pass a constraint-compliant video via `video_url`.
- A clear, frontal, single-person video gives the best lip-sync results.
- Audio or text length should match the video length (audio no longer than the video).
- Billing occurs on success (2.45 Credits/call); validation failures (4xx) are not billed.

## Conclusion

Through this document, you have learned how to use the Kling Lip Sync API to drive a video with audio or text for synchronized lip movement. We hope this document helps you integrate and use the API more effectively. If you have any questions, please feel free to contact our technical support team.
