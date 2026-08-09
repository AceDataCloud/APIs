# MiniMax H3 API

Generate 4–15 second videos from text and media references through AceDataCloud.

MCP integration: [MiniMax H3 MCP](https://github.com/AceDataCloud/MinimaxMCP).

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `https://api.acedata.cloud/minimax/videos` | Create a video generation task |
| POST | `https://api.acedata.cloud/minimax/tasks` | Retrieve one or more task records, or delete a task record |

All endpoints require bearer authentication with an API token from the AceDataCloud console.

## Quick start

```bash
curl -X POST https://api.acedata.cloud/minimax/videos \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-H3",
    "content": [
      {
        "type": "text",
        "text": "让画面中的人物自然移动，镜头缓慢推进"
      },
      {
        "type": "image_url",
        "image_url": {
          "url": "https://cdn.acedata.cloud/b1c82e4937.png"
        },
        "role": "first_frame"
      }
    ],
    "resolution": "2K",
    "duration": 5,
    "ratio": "adaptive"
  }'
```

The response returns a `task_id`. Poll it with the task API:

```bash
curl -X POST https://api.acedata.cloud/minimax/tasks \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{"action":"retrieve","id":"TASK_ID"}'
```

## Content inputs

Each video request sends a `content` array. Items can be text or media references:

- `text` content includes a `text` field up to 7000 characters.
- `image_url`, `video_url`, and `audio_url` content include a media object with a `url` field.
- Media items can set `role` to `first_frame`, `last_frame`, `reference_image`, `reference_video`, or `reference_audio`.

Public pricing is **$0.057143/s for 768P** and **$0.091429/s for 2K** on the largest package. Failed tasks are not charged.

- [Video generation guide](docs/videos.md)
- [Task API guide](docs/tasks.md)
- [AceDataCloud console](https://platform.acedata.cloud/console/applications)
