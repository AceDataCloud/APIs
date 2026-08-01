# Digital Human Voices API Integration Guide

This guide explains how to clone a voice for digital human text-to-speech generation.

## Authentication

Send your Ace Data Cloud API token in the `authorization` header for every request.

## Request Endpoint

`POST https://api.acedata.cloud/digital-human/voices`

## Request Body

- `audio_url` (required): public URL of a clean 10-20 second voice sample.
- `lang`: voice language (`zh` or `en`).
- `name`: optional voice label.
- `async`: when `true`, the API returns immediately with `task_id`.

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/digital-human/voices' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "audio_url": "https://cdn1.suno.ai/ec13e502-d043-4eb2-92ee-e900c6da69d1.wav",
    "lang": "zh"
  }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "...",
  "trace_id": "...",
  "voice_id": "f754a190e26c",
  "state": "succeed"
}
```

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
