# Kling Lip Sync API Integration Guide

This guide explains how to use the Kling Lip Sync API. You can drive an existing Kling video with audio or text so the character speaks in sync.

## Basic Information

- Endpoint: `POST https://api.acedata.cloud/kling/lip-sync`
- Request format: `application/json`
- Response format: `application/json`
- Authentication: API key passed as a ****** in the `authorization` header.

## Request Headers

- `accept`: `application/json`
- `authorization`: ****** API key.
- `content-type`: `application/json`

## Request Body Parameters

- `mode` (required): generation mode, supports `audio2video` and `text2video`.
- `video_id` / `video_url` (one required): provide either a Kling-generated video ID or a public video URL.
- `audio_url` (required when `mode=audio2video`): URL of the driving audio.
- `audio_type` (optional): `url` (default) or `file`.
- `audio_file` (required when `audio_type=file`): Base64 audio content.
- `text` (required when `mode=text2video`): speech text (max 120 characters).
- `voice_id` (required when `mode=text2video`): voice ID.
- `voice_language` (optional): `zh` (default) or `en`.
- `voice_speed` (optional): speech rate, range `0.8` to `2.0`.
- `callback_url` (optional): callback URL for asynchronous completion.
- `async` (optional): when `true`, immediately returns `task_id` and you can query progress through `/kling/tasks`.

## Request Examples

### Audio-driven (`audio2video`)

```bash
curl -X POST 'https://api.acedata.cloud/kling/lip-sync' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
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

## Async Query

If you provide `callback_url` or set `async=true`, the API returns `task_id` immediately. You can then query task status through `/kling/tasks` with:

```json
{
  "action": "retrieve",
  "id": "YOUR_TASK_ID"
}
```

## Error Handling

Common errors:

- `400 bad_request`: missing or invalid parameters.
- `401 authorization_missing`: missing or invalid API key.
- `429 too_many_requests`: concurrency/rate limit reached.
- `500 api_error`: internal or upstream service error.

Example:

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

- `video_id` must refer to a Kling-generated video within 30 days.
- For best results, use clear frontal portraits and match audio/text length to video length.
