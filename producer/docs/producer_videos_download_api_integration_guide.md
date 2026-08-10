# Producer Videos Download API Integration Instructions

Producer allows you to download videos related to songs. This document explains the integration method for the Producer Videos Download API.

## Basic Usage

This API has one required input parameter:

- `audio_id`: the unique ID of the song.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/producer/videos' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "audio_id": "a54609c6-13e2-4176-be0f-4d7eebc68e1f"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "1237fc8f-ed3f-41fd-a889-a737fd7777da",
  "trace_id": "19db6190-d9ef-4a4f-a102-9f51b611c8b5",
  "data": {
    "video_url": "https://platform2.cdn.acedata.cloud/gemini/04a043bd-6b23-4b4e-945c-ce48158c3eee.mp4?example=video-001"
  }
}
```

The `video_url` field in `data` is the download link for the video.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)

