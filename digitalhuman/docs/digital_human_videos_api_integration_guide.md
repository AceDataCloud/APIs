# Digital Human Videos API Integration Guide

This guide explains how to generate digital human videos with synchronized speech using the Digital Human Videos API.

## Authentication

Send your Ace Data Cloud API token in the `authorization` header for every request.

## Request Endpoint

`POST https://api.acedata.cloud/digital-human/videos`

## Request Body

- `video_url`: public URL of the source face video (preferred). Supply either `video_url` or `image_url`.
- `image_url`: public URL of a source face photo. Supply either `video_url` or `image_url`.
- `audio_url`: public URL of the driving audio (`.wav`, `.mp3`, `.m4a`). Or supply `text` + `voice_id`.
- `text`: spoken text for TTS (requires `voice_id`).
- `voice_id`: a cloned voice from `POST /digital-human/voices`.
- `engine`: deprecated. Accepted for backward compatibility.
- `guidance`: lip-sync strength.
- `steps`: diffusion steps.
- `seam_fix`: apply mouth-seam reduction blend.
- `speed`: audio tempo multiplier.
- `resolution`: deprecated. Output is rendered at 720p.
- `callback_url`: webhook for asynchronous callback.
- `async`: when `true`, the API returns immediately with `task_id`.

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/digital-human/videos' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
    "audio_url": "https://cdn1.suno.ai/ec13e502-d043-4eb2-92ee-e900c6da69d1.wav",
    "async": true
  }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "0c0b4d3a-2f1e-4a6b-9c2d-2b3c4d5e6f70",
  "trace_id": "a9063166-26ed-4451-85b5-54e896817c69",
  "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
  "duration": 17.2,
  "width": 1280,
  "height": 720,
  "engine": "latentsync",
  "state": "succeed"
}
```

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
