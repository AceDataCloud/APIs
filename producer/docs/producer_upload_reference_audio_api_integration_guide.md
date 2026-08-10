# Producer Upload Reference Audio API Integration Instructions

Producer allows you to upload reference audio for secondary creation. This document explains the integration method for the Producer Upload Reference Audio API.

## Basic Usage

This API has one required input parameter:

- `audio_url`: a publicly accessible audio URL. The upstream guide uses an MP3 CDN URL.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/producer/upload' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "audio_url": "https://cdn.acedata.cloud/suno_demo.mp3"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "23e7d4ec-d1a8-429f-87d8-9f53fc3b6666",
  "data": {
    "audio_id": "d906da31-87cb-42f5-98df-2fc4969923b1",
    "lyric": "[Mandopop, Acoustic Pop]\n[Soft female vocals, bright and cheerful]\n\n[Verse 1]\nThe sunlight shines on the beach",
    "audio_url": "https://platform2.cdn.acedata.cloud/fish/5ade0339-5f11-487e-aacc-06a908271706.mp3?example=audio-001"
  }
}
```

The `audio_id` field in `data` is the uploaded song ID. Use it with the [Producer Audios Generation API](producer_audios_generation_api_integration_guide.md) for cover, extend, or other secondary creation workflows.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)

