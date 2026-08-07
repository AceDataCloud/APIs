# MiniMax H3 API

Generate 4–15 second videos from text, one to nine reference images, or one to three audio references through AceDataCloud.

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
    "model": "minimax-h3",
    "prompt": "A red fox running through a snowy forest at dawn, low tracking shot",
    "resolution": "768P",
    "ratio": "16:9",
    "duration": 4,
    "async": true
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

The API does not accept `action`. It infers the mode:

1. prompt only → text-to-video
2. one image without audio → first-frame image-to-video
3. multiple images or any audio → multimodal reference video

Pricing is resolution-based:

- `768P`: **$0.057143/second**
- `2K`: **$0.091429/second**

Only successful tasks are billed.

- [Video generation guide](docs/videos.md)
- [Task API guide](docs/tasks.md)
- [AceDataCloud console](https://platform.acedata.cloud/console/applications)
