# Kling Lip Sync API Integration Guide

Drive an existing Kling video with audio or text so the character speaks in sync.

## Endpoint

- Method: `POST`
- URL: `https://api.acedata.cloud/kling/lip-sync`
- Authentication: Include an `authorization` header with your bearer token.
- Content-Type: `application/json`

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `mode` | string | Yes | Generation mode. Enum: `audio2video`, `text2video`. |
| `video_id` | string | One-of | Kling video ID. Provide `video_id` or `video_url`. |
| `video_url` | string | One-of | Public video URL. Provide `video_id` or `video_url`. |
| `audio_url` | string | Conditional | Required when `mode=audio2video` and `audio_type=url`. |
| `audio_type` | string | No | Audio input type. Enum: `url`, `file`. Default: `url`. |
| `audio_file` | string | Conditional | Required when `audio_type=file` (base64 audio). |
| `text` | string | Conditional | Required when `mode=text2video`. |
| `voice_id` | string | Conditional | Required when `mode=text2video`. |
| `voice_language` | string | No | Enum: `zh`, `en`. |
| `voice_speed` | number | No | Speech speed for `text2video`. |
| `callback_url` | string | No | Callback URL. |
| `async` | boolean | No | Async mode. When true, returns `task_id` immediately. |

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
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "video_id": "895047463190134880",
  "video_url": "https://cdn.acedata.cloud/bafb400e8a.mp4",
  "duration": 5,
  "state": "succeed"
}
```

## Error Example

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
