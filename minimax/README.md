# MiniMax H3 Video Generation API

Create 4–15 second MiniMax H3 video tasks with text, image, video, and audio references through AceDataCloud.

MCP integration: [MiniMax H3 MCP](https://github.com/AceDataCloud/MinimaxMCP).

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `https://api.acedata.cloud/minimax/videos` | Create a video task |
| POST | `https://api.acedata.cloud/minimax/tasks` | Retrieve or delete task records |

## Quick start

```bash
curl -X POST https://api.acedata.cloud/minimax/videos \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-H3",
    "content": [{
      "type": "text",
      "text": "A red fox running through a snowy forest at dawn, low tracking shot"
    }],
    "resolution": "2K",
    "duration": 5,
    "ratio": "16:9"
  }'
```

Poll the returned `task_id`:

```bash
curl -X POST https://api.acedata.cloud/minimax/tasks \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action":"retrieve","id":"TASK_ID"}'
```

## Content modes

The required `content` array must include a non-empty `text` item. Add media items to create:

1. text-to-video
2. first-frame or first/last-frame image-to-video
3. multimodal reference video using images, video, and audio

Media content uses `image_url`, `video_url`, or `audio_url` objects with a `url` property and an appropriate `role`. The API does not accept legacy `prompt`, `image_urls`, `audio_urls`, or `async` fields. Creation is always asynchronous.

Only successful tasks are charged.

- [Video generation guide](docs/videos.md)
- [Task API guide](docs/tasks.md)
- [AceDataCloud console](https://platform.acedata.cloud/console/applications)
