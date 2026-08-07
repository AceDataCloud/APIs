# Video Generation

## Request

`POST https://api.acedata.cloud/minimax/videos`

| Field | Type | Default | Constraints |
| --- | --- | --- | --- |
| `model` | string | — | required; `MiniMax-H3` |
| `content` | object[] | — | required; non-empty multimodal content array |
| `resolution` | string | — | required; `768P` or `2K` |
| `duration` | integer | — | required; 4–15 |
| `ratio` | string | — | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16` |
| `aigc_watermark` | boolean | false | add an AIGC watermark |
| `callback_url` | string | — | public HTTP(S) webhook |

Each `content` item has a `type`: `text`, `image_url`, `video_url`, or `audio_url`. A text item provides the required prompt, with a maximum length of 7000 characters. Media items contain a media object such as `"image_url": {"url": "https://..."}` and a `role`: `first_frame`, `last_frame`, `reference_image`, `reference_video`, or `reference_audio`. Media URLs support public URLs, `mm_file://{file_id}`, and matching Base64 data URIs.

Text-to-video requires a non-`adaptive` `ratio`:

```json
{
  "model": "MiniMax-H3",
  "content": [
    {
      "type": "text",
      "text": "A red fox running through a snowy forest at dawn, low tracking shot"
    }
  ],
  "resolution": "2K",
  "duration": 5,
  "ratio": "16:9"
}
```

## First-frame image-to-video example

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
  "duration": 5,
  "ratio": "adaptive"
}
```

First- and last-frame image items may be combined. Reference images, videos, and audio can also be combined using `reference_image`, `reference_video`, and `reference_audio` roles. Multimodal references support up to nine images, three videos, and three audio clips. Do not mix first/last-frame items with multimodal references.

## Create response

```json
{
  "task_id": "TASK_ID"
}
```

Creation is always asynchronous. Retrieve the successful video or task error through the task API.
