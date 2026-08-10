# Producer Lyrics Generation API Integration Instructions

Producer allows you to generate lyrics from a prompt. This document explains the integration method for the Producer Lyrics Generation API.

## Basic Usage

This API has one required input parameter:

- `prompt`: the prompt for generating lyrics.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/producer/lyrics' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "prompt": "A song about winter"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "d354b519-43c0-4888-a3da-83adbf845fd6",
  "data": {
    "title": "Mercy in the Trees",
    "lyrics": "[Verse 1]\nI walked out past the railyard\nWhere the pines grow thick with frost\n\n[Chorus]\nWinter is a heavy coat\nWinter is a heavy coat"
  }
}
```

The `lyrics` field in `data` contains the generated lyrics content.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)

