# Happy Horse Videos API Integration Guide

The Happy Horse Videos API supports text-to-video, first-frame image-to-video,
reference-image-to-video, and video editing through one endpoint.

## Endpoint

```text
POST https://api.acedata.cloud/happyhorse/videos
```

Authenticate every request with an Ace Data Cloud API token:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Create a token in the [Ace Data Cloud console](https://platform.acedata.cloud/console/credentials).

## Actions and Models

| Action | Models | Required fields |
|---|---|---|
| `generate` | `happyhorse-1.0-t2v`, `happyhorse-1.1-t2v` | `prompt` |
| `image_to_video` | `happyhorse-1.0-i2v`, `happyhorse-1.1-i2v` | `image_url` |
| `reference_to_video` | `happyhorse-1.0-r2v`, `happyhorse-1.1-r2v` | `prompt`, `image_urls` |
| `video_edit` | `happyhorse-1.0-video-edit` | `prompt`, `video_url` |

If `model` is omitted, each action uses its latest available model. The default action is
`generate`.

## Request Fields

| Field | Type | Values and behavior |
|---|---|---|
| `action` | string | `generate`, `image_to_video`, `reference_to_video`, `video_edit` |
| `model` | string | Must belong to the selected action's model family |
| `prompt` | string | Required for text, reference, and edit actions; optional for image-to-video |
| `image_url` | string | First-frame URL for image-to-video |
| `image_urls` | string[] | 1-9 references for reference-to-video; 0-5 for editing |
| `video_url` | string | Source video URL for editing |
| `resolution` | string | `720P` or `1080P`; default `1080P` |
| `ratio` | string | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`; text/reference actions only |
| `duration` | integer | 3-15 seconds; text/image/reference actions only; default 5 |
| `watermark` | boolean | Add the Happy Horse watermark; default `false` |
| `audio_setting` | string | `auto` or `origin`; video editing only |
| `seed` | integer | 0-2147483647 |
| `callback_url` | string | Webhook URL for asynchronous delivery |
| `async` | boolean | Return a task ID immediately for polling |

Resolution uses an uppercase `P`. Image-to-video derives its ratio from the first-frame image.
Video editing derives duration and ratio from the source video.

## Text-to-Video

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A cinematic white horse lifts its head, its mane moving in the sunrise wind, slow camera push",
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5
  }'
```

## First-Frame Image-to-Video

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "image_to_video",
    "model": "happyhorse-1.1-i2v",
    "image_url": "https://cdn.acedata.cloud/b1c82e4937.png",
    "prompt": "The horse lifts its head while the mane moves in the wind, gentle camera push",
    "resolution": "1080P",
    "duration": 5
  }'
```

The prompt is optional. Do not pass `ratio`; the service follows the input image.

## Reference-to-Video

Pass 1-9 reference images. In the prompt, `character1`, `character2`, and later names refer to the
images in array order.

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "reference_to_video",
    "model": "happyhorse-1.1-r2v",
    "prompt": "character1 walks through a sunrise meadow with the warm leather and gold style from character2",
    "image_urls": [
      "https://cdn.acedata.cloud/b1c82e4937.png",
      "https://cdn.acedata.cloud/eb75d88a3f.png"
    ],
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5
  }'
```

## Video Editing

Pass the source video, editing instructions, and optionally up to 5 references. Set
`audio_setting` to `origin` to preserve source audio.

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "video_edit",
    "model": "happyhorse-1.0-video-edit",
    "prompt": "Apply the warm leather and gold style from the reference while preserving camera motion",
    "video_url": "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4",
    "image_urls": ["https://cdn.acedata.cloud/eb75d88a3f.png"],
    "resolution": "720P",
    "audio_setting": "origin"
  }'
```

Do not pass `duration` or `ratio` for editing; those fields are derived from the source video.

## Synchronous Response

Without `async` or `callback_url`, the request waits for completion and returns the final video:

```json
{
  "success": true,
  "task_id": "27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1",
  "trace_id": "6071ab5e-2f37-46f0-9e07-f1e378112e69",
  "data": [
    {
      "id": "9650580f-6d9e-4bc1-823a-29011790c5cb",
      "video_url": "https://platform2.cdn.acedata.cloud/happyhorse/27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1.mp4",
      "state": "succeeded",
      "duration": 5,
      "resolution": "720P",
      "ratio": null
    }
  ]
}
```

`task_id` is the Ace Data Cloud task ID. `data[].id` is the upstream Happy Horse task ID. Use
`trace_id` when contacting support.

## Asynchronous Processing

Set `"async": true` to return immediately:

```json
{"task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea"}
```

Poll it through the [Tasks API](happyhorse_tasks_api_integration_guide.md). Alternatively, provide
`callback_url`; the service posts the final response to that URL.

## Errors

| Status | Meaning |
|---|---|
| `400` | Missing field, invalid action/model pairing, out-of-range duration, or too many images |
| `401` | Missing or invalid API token |
| `403` | Insufficient balance or content moderation rejection |
| `429` | Upstream rate limit; retry with backoff |
| `500` | Upstream generation or internal service failure |

Failed generation tasks are not billed. For video editing, billing duration is based on the
upstream-reported input plus output duration rather than a request field.