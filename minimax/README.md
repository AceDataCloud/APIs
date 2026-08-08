# MiniMax H3 API

Generate 4–15 second videos from text, first or last frames, and image, video, or audio references through AceDataCloud.

MCP integration: [MiniMax H3 MCP](https://github.com/AceDataCloud/MinimaxMCP).

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `https://api.acedata.cloud/minimax/videos` | Create a video task |
| POST | `https://api.acedata.cloud/minimax/tasks` | Retrieve, list, cancel, or delete task records |

## Quick start

```bash
curl -X POST https://api.acedata.cloud/minimax/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-H3",
    "content": [
      {
        "type": "text",
        "text": "A red fox running through a snowy forest at dawn, low tracking shot"
      }
    ],
    "resolution": "2K",
    "duration": 5,
    "ratio": "16:9",
    "aigc_watermark": false
  }'
```

Poll the returned `task_id`:

```bash
curl -X POST https://api.acedata.cloud/minimax/tasks \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action":"retrieve","id":"TASK_ID"}'
```

## Modes

The API uses MiniMax H3's multimodal `content` array and is always asynchronous. It does not accept legacy fields such as `prompt`, `image_urls`, `audio_urls`, `messages`, `first_frame_image`, or `async`.

Common content roles:

- text only → text-to-video; `ratio` is required and cannot be `adaptive`
- `image_url` with `first_frame` and/or `last_frame` → first-frame, last-frame, or first/last-frame video
- `image_url`, `video_url`, or `audio_url` with `reference_*` roles → multimodal reference video

Each request must include a non-empty text content item. Only successful tasks are charged; task retrieval is free.

- [Video generation guide](docs/videos.md)
- [Task API guide](docs/tasks.md)
- [AceDataCloud console](https://platform.acedata.cloud/console/applications)
