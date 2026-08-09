# Video Generation

## Request

`POST https://api.acedata.cloud/minimax/videos`

| Field | Type | Default | Constraints |
| --- | --- | --- | --- |
| `model` | string | — | required; `MiniMax-H3` |
| `content` | object[] | — | required; contains one non-empty `text` item (max 7000 chars) |
| `resolution` | string | — | required; `768P` or `2K` |
| `duration` | integer | — | required; 4–15 |
| `ratio` | string | `adaptive` | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16` |
| `async` | boolean | `false` | `false` returns the completed `task`; `true` returns immediately with task identifiers |
| `callback_url` | string | — | public HTTP(S) webhook; enables async mode |

The API does not accept legacy `prompt`, `image_urls`, `audio_urls`, `messages`, or `first_frame_image` fields.

## Content items

| `type` | Data field | `role` | Purpose |
| --- | --- | --- | --- |
| `text` | `text` | — | Required prompt |
| `image_url` | `image_url.url` | `first_frame`, `last_frame`, `reference_image` | Frame control or visual reference |
| `video_url` | `video_url.url` | `reference_video` | Motion or camera reference |
| `audio_url` | `audio_url.url` | `reference_audio` | Dialogue, music, or rhythm reference |

Media URLs may be public HTTPS URLs, `mm_file://{file_id}` references, or Base64 data URIs. First/last frames cannot be combined with reference media. Use at most one first frame, one last frame, nine reference images, three reference videos, and three reference audio files; reference media totals at most 12 files.

## Image-to-video example

```json
{
  "model": "MiniMax-H3",
  "content": [
    {
      "type": "text",
      "text": "Preserve the character while the camera slowly pushes in"
    },
    {
      "type": "image_url",
      "image_url": { "url": "https://cdn.acedata.cloud/b1c82e4937.png" },
      "role": "first_frame"
    }
  ],
  "resolution": "2K",
  "ratio": "9:16",
  "duration": 8
}
```

For text-only requests, provide only the `text` item and use a fixed `ratio`. For first/last-frame requests, use `adaptive` or omit `ratio`.

## Response modes and callbacks

By default, creating a video waits for generation to finish and returns the complete task:

```json
{
  "task": {
    "id": "TASK_ID",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "content": {
      "url": "https://cdn.acedata.cloud/minimax/TASK_ID.mp4"
    },
    "resolution": "2K",
    "duration": 8,
    "usage": {
      "total_seconds": 8,
      "input_seconds": 0,
      "output_seconds": 8,
      "input_image_count": 1
    },
    "ratio": "9:16",
    "task_type": "generation",
    "modality": "video"
  }
}
```

When `async` is `true` or `callback_url` is set, the create request returns immediately:

```json
{
  "task_id": "TASK_ID",
  "trace_id": "trace_7f8c2b1a"
}
```

When `callback_url` is set, the API posts the final task result to that URL after completion; the payload matches the task retrieval response. Save the `task_id` and poll the task API as a fallback.
