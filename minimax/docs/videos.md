# Video Generation

## Request

`POST https://api.acedata.cloud/minimax/videos`

| Field | Type | Default | Constraints |
| --- | --- | --- | --- |
| `model` | string | — | required; only `MiniMax-H3` |
| `content` | object[] | — | required; at least one non-empty text item |
| `resolution` | string | — | required; `768P` or `2K` |
| `duration` | integer | — | required; 4–15 |
| `ratio` | string | `adaptive` | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16` |
| `aigc_watermark` | boolean | false | add an AIGC watermark |
| `callback_url` | string | — | public HTTP(S) webhook |

The API is always asynchronous and returns a `task_id`. It does not accept legacy fields such as `prompt`, `image_urls`, `audio_urls`, `messages`, `first_frame_image`, or `async`; put all text and media in `content`.

Each `content` item has a `type` of `text`, `image_url`, `video_url`, or `audio_url`. Media values are objects with a `url` field. Supported roles are `first_frame`, `last_frame`, `reference_image`, `reference_video`, and `reference_audio`.

For text-to-video, set a fixed `ratio`; `adaptive` is for frame-based or reference workflows. Media URLs can be public HTTPS URLs, `mm_file://{file_id}` references, or Base64 data URIs.

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

## Multimodal reference example

```json
{
  "model": "MiniMax-H3",
  "content": [
    {
      "type": "text",
      "text": "Keep the character consistent while matching the reference performance and audio rhythm"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "YOUR_CHARACTER_IMAGE_URL"
      },
      "role": "reference_image"
    },
    {
      "type": "video_url",
      "video_url": {
        "url": "YOUR_PERFORMANCE_VIDEO_URL"
      },
      "role": "reference_video"
    },
    {
      "type": "audio_url",
      "audio_url": {
        "url": "YOUR_AUDIO_URL"
      },
      "role": "reference_audio"
    }
  ],
  "resolution": "2K",
  "duration": 5,
  "ratio": "adaptive"
}
```

## Final result fields

A successful task retrieval response contains `task`. The task includes:

- `id`: public AceDataCloud task ID
- `model`: `MiniMax-H3`
- `status`: `queued`, `running`, `succeeded`, `failed`, or `cancelled`
- `content.url`: AceDataCloud CDN URL after success
- `duration`: final billed seconds
- `ratio`: output aspect ratio
- `resolution`: `768P` or `2K`
- `usage`: billing usage fields
- `task_type`: `generation`
- `modality`: `video`
