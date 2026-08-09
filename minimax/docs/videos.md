# Video Generation

## Request

`POST https://api.acedata.cloud/minimax/videos`

This endpoint requires bearer authentication with an API token from the AceDataCloud console.

| Field | Type | Default | Constraints |
| --- | --- | --- | --- |
| `model` | string | — | required; only `MiniMax-H3` |
| `content` | array | — | required; at least 1 item |
| `content[].type` | string | — | required; `text`, `image_url`, `video_url`, or `audio_url` |
| `content[].text` | string | — | required for text content; max 7000 chars |
| `content[].image_url.url` | string | — | media URL for `image_url` content |
| `content[].video_url.url` | string | — | media URL for `video_url` content |
| `content[].audio_url.url` | string | — | media URL for `audio_url` content |
| `content[].role` | string | — | `first_frame`, `last_frame`, `reference_image`, `reference_video`, or `reference_audio` |
| `resolution` | string | — | required; `768P` or `2K` |
| `duration` | integer | — | required; 4–15 |
| `ratio` | string | — | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16` |
| `callback_url` | string | — | public webhook URL |
| `aigc_watermark` | boolean | false | add an AIGC watermark |

## Example

```json
{
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
}
```

A successful create response returns the task ID:

```json
{
  "task_id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28"
}
```

## Final task fields

Retrieve the task to inspect the final result. A video task can contain:

- `id`: public AceDataCloud task ID
- `model`: `MiniMax-H3`
- `status`: `queued`, `running`, `succeeded`, `failed`, or `cancelled`
- `error`: object with `code` and `message` when the task fails
- `created_at` and `updated_at`: Unix timestamps
- `content.url`: generated video URL
- `resolution`: `768P` or `2K`
- `duration`: final billed seconds
- `usage`: `total_seconds`, `input_seconds`, `output_seconds`, and `input_image_count`
- `ratio`: output aspect ratio
- `task_type`: `generation`
- `modality`: `video`
