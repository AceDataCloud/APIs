# Seedance Videos Generation API Integration Instructions

This article introduces the Seedance Videos Generation API integration instructions, which can generate official ByteDance Seedance (Doubao) videos by inputting custom parameters such as a multimodal `content` array, model, resolution, aspect ratio, and duration.

## Application Process

To use the Seedance Videos Generation API, apply for the corresponding service on the [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to input a `content` array containing a single text item plus a `model`. The result is the generated video. The request body fields are described below:

- `model`: the model used to generate the video. Available values:
  - **Seedance 2.0 series** (multimodal reference: real-person / character image, reference audio, reference video): `doubao-seedance-2-0-260128` (standard), `doubao-seedance-2-0-fast-260128` (fast), `doubao-seedance-2-0-mini-260615` (lightweight).
  - **Seedance 1.x**: `doubao-seedance-1-5-pro-251215`, `doubao-seedance-1-0-pro-250528`, `doubao-seedance-1-0-pro-fast-251015`, `doubao-seedance-1-0-lite-t2v-250428`, `doubao-seedance-1-0-lite-i2v-250428`.
- `content`: the input array. Each item carries a `type` of `text`, `image_url`, `audio_url`, or `video_url`:
  - `text`: `{ "type": "text", "text": "..." }` — the prompt (max 1000 characters).
  - `image_url`: `{ "type": "image_url", "role": "first_frame|last_frame|reference_image", "image_url": { "url": "https://..." } }`.
  - `audio_url` (Seedance 2.0): `{ "type": "audio_url", "audio_url": { "url": "https://..." } }` — reference audio for voice timbre / background music.
  - `video_url` (Seedance 2.0): `{ "type": "video_url", "video_url": { "url": "https://..." } }` — reference video for subject, camera movement, motion or overall style.
- `resolution`: output resolution, one of `480p`, `720p`, `1080p`, `4k`. `4k` is supported only by `doubao-seedance-2-0-260128`; `doubao-seedance-2-0-fast-260128` and `doubao-seedance-2-0-mini-260615` cap at `720p`. If omitted, a default resolution is selected based on the chosen model.
- `ratio`: aspect ratio, one of `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive`. Default `16:9`.
- `duration`: video duration in seconds, model-specific:
  - Seedance 1.0 Pro / 1.0 Pro Fast: `2`–`12`.
  - Seedance 1.5 Pro: `4`–`12`, or `-1` for automatic duration.
  - Seedance 2.0 series: `4`–`15`, or `-1` for automatic duration.
- `frames`: frame count, `29`–`361` (must satisfy 25+4n). Use either `duration` or `frames`; if both are specified, `frames` takes precedence over `duration`.
- `seed`: random seed, integer `-1`–`4294967295` (`-1` = random).
- `camerafixed`: whether to fix the camera position, `true` / `false`.
- `watermark`: whether to add a watermark, `true` / `false`.
- `generate_audio`: whether to generate audio. Supported by `doubao-seedance-1-5-pro-251215` and the `doubao-seedance-2-0` series; other models ignore it. Default `false`.
- `callback_url`: an asynchronous callback URL. When provided, the API returns immediately with a `task_id` and POSTs the result to this URL when generation completes.
- `async`: optional. When `true`, the API returns immediately with a `task_id` (no `callback_url` required); poll the result with the Seedance Tasks API.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedance/videos' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      { "type": "text", "text": "A street dancer doing breakdancing moves in an urban setting" }
    ],
    "resolution": "1080p",
    "ratio": "16:9",
    "duration": 5
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": {
    "task_id": "cgt-20251222005129-62fhb",
    "status": "succeeded",
    "video_url": "https://platform.cdn.acedata.cloud/seedance/f592800a-b87c-4705-8796-cbb8018cae35.mp4",
    "model": "doubao-seedance-2-0-260128"
  }
}
```

The returned result contains the following fields:

- `success`: the status of the video generation task.
- `task_id`: the ID of the video generation task.
- `trace_id`: the trace ID for this request.
- `data`: the result of the video generation task, including `status`, `video_url`, and `model`.

Download the generated video from the `video_url` field.

## Workflows

### Text-to-Video

Pass a single `text` item in the `content` array (see the request example above).

### Image-to-Video

Add an `image_url` item with a `role`:

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    { "type": "text", "text": "the person starts dancing gracefully" },
    { "type": "image_url", "role": "first_frame", "image_url": { "url": "https://example.com/dancer.jpg" } }
  ],
  "resolution": "720p",
  "duration": 5
}
```

Image roles:

- `first_frame` — the image is used as the opening frame.
- `last_frame` — the image is used as the closing frame.
- `reference_image` — the image is used as a style / subject / real-person reference.

`first_frame` and `last_frame` may be combined in a single request, but `reference_image` is mutually exclusive with `first_frame` / `last_frame`.

### Real-Person / Character Reference (Seedance 2.0)

The Seedance 2.0 series can keep a specific person or character consistent across a brand-new scene. Pass one or more photos as `image_url` items with `role: "reference_image"` (up to 9):

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    { "type": "text", "text": "the same person walking through a neon-lit night market, cinematic" },
    { "type": "image_url", "role": "reference_image", "image_url": { "url": "https://example.com/person.jpg" } }
  ],
  "resolution": "1080p",
  "duration": 8
}
```

### Reference Audio / Video (Seedance 2.0)

The Seedance 2.0 series also accepts reference audio (voice timbre, background music) and reference video (subject, camera movement, motion, overall style). Limits: up to 3 audio and 3 video references.

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    { "type": "text", "text": "a singer performing on stage, matching the reference voice and motion" },
    { "type": "image_url", "role": "reference_image", "image_url": { "url": "https://example.com/person.jpg" } },
    { "type": "audio_url", "audio_url": { "url": "https://example.com/voice.mp3" } },
    { "type": "video_url", "video_url": { "url": "https://example.com/motion.mp4" } }
  ],
  "generate_audio": true
}
```

## Asynchronous Generation

Video generation can take time. To avoid long-held HTTP connections, use one of the asynchronous modes:

- **Callback**: set `callback_url`. The API returns immediately with a `task_id` and POSTs the final result to your URL when generation completes.
- **Polling**: set `"async": true`. The API returns immediately with a `task_id`; poll the result with the [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c).

## Error Codes

| HTTP Status | Code | Meaning |
| ---- | ---- | ---- |
| 400 | `bad_request` | Invalid request, e.g. an invalid `model`. |
| 401 | `invalid_token` | The token is invalid or wrong. |
| 401 | `token_expired` | The token has expired. |
| 400 | `no_token` | No token was specified for the request. |
| 500 | `internal_error` | An internal or upstream error occurred. |

Each error response includes a `trace_id` to help with debugging and support.
