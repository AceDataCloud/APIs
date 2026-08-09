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
| `async` | boolean | `false` | `false` waits for and returns the completed task; `true` returns task identifiers immediately |
| `callback_url` | string | — | public HTTP(S) webhook; enables asynchronous mode |

The API does not accept legacy `prompt`, `image_urls`, `audio_urls`, `messages`, or `first_frame_image` fields. Put prompts and media in `content`; do not send legacy and current formats together.

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

## Response and callbacks

By default, the request waits for completion and returns the completed task. Read the generated video from `task.content.url` when `task.status` is `succeeded`:

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
    "ratio": "9:16",
    "task_type": "generation",
    "modality": "video"
  }
}
```

Set `async` to `true` (or provide `callback_url`) to return immediately:

```json
{ "task_id": "TASK_ID", "trace_id": "TRACE_ID" }
```

When `callback_url` is set, it receives the final task result. Save the returned `task_id` and poll the task API as a fallback.
