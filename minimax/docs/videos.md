# Video Generation

`POST https://api.acedata.cloud/minimax/videos`

## Authentication

```http
Authorization: ******
Content-Type: application/json
Accept: application/json
```

## Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | yes | Must be `MiniMax-H3` |
| `content` | object[] | yes | Ordered multimodal input blocks (see below) |
| `resolution` | string | yes | `768P` or `2K` |
| `duration` | integer | yes | Output duration in seconds |
| `ratio` | string | no | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, or `9:16` |
| `callback_url` | string | no | Public webhook URL for async completion callbacks |
| `aigc_watermark` | boolean | no | Whether to add an AIGC watermark (default `false`) |

### `content` item format

Each item in `content` is an object with a required `type`:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | yes | `text`, `image_url`, `video_url`, or `audio_url` |
| `text` | string | conditional | Required when `type` is `text` (max length 7000) |
| `image_url` | object | conditional | Required when `type` is `image_url`; shape: `{ "url": "https://..." }` |
| `video_url` | object | conditional | Required when `type` is `video_url`; shape: `{ "url": "https://..." }` |
| `audio_url` | object | conditional | Required when `type` is `audio_url`; shape: `{ "url": "https://..." }` |
| `role` | string | no | `first_frame`, `last_frame`, `reference_image`, `reference_video`, or `reference_audio` |

## Text-to-video example

```json
{
  "model": "MiniMax-H3",
  "content": [
    {
      "type": "text",
      "text": "A red fox running through a snowy forest at dawn, low tracking shot"
    }
  ],
  "resolution": "768P",
  "duration": 5,
  "ratio": "16:9"
}
```

## Image-guided example

```json
{
  "model": "MiniMax-H3",
  "content": [
    {
      "type": "image_url",
      "image_url": { "url": "https://cdn.acedata.cloud/reference.png" },
      "role": "first_frame"
    },
    {
      "type": "text",
      "text": "Preserve the character while the camera slowly pushes in"
    }
  ],
  "resolution": "2K",
  "duration": 5,
  "ratio": "adaptive"
}
```

## Accepted response

```json
{
  "task_id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28"
}
```

Retrieve the final result with `POST /minimax/tasks`.

## Errors

Common status codes: `400`, `401`, `403`, `422`, `429`, `500`.
