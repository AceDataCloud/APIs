# Maestro Videos API Integration Guide

`POST https://api.acedata.cloud/maestro/videos`

The Maestro Videos API accepts a production brief and creates an asynchronous video job. A headless AI director plans the content, generates or selects media, produces voiceover and music, edits, captions, checks, and renders the finished video.

The endpoint returns a `task_id` immediately. Retrieve progress and final output with `POST /maestro/tasks` or provide a `callback_url` for terminal-state delivery.

## Authentication

Create an API token in the [Ace Data Cloud console](https://platform.acedata.cloud/console/applications). Send it as a Bearer token:

```http
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json
Accept: application/json
```

Keep tokens outside source control and never expose them in client-side code or logs.

## Request Body

| Field | Type | Required | Default | Description |
|---|---|---:|---|---|
| `prompt` | string | yes | - | Natural-language brief covering the subject, audience, content, tone, and desired result |
| `action` | string | no | `generate` | `generate` or `edit` on Lite; `remix` on Standard or Pro; `extend` on Pro |
| `ref_task_id` | string | conditional | - | Required when `action` is `remix`, `edit`, or `extend` |
| `file_urls` | string[] | no | - | Public image, video, or audio references |
| `langs` | string[] | no | `["zh-cn"]` | Output language codes; the first item is primary. Lite supports 1, Standard 2, and Pro 4 |
| `aspect` | string | no | `9:16` | `9:16`, `16:9`, or `1:1`; Lite renders 720p/24fps, Standard and Pro render 1080p/30fps |
| `duration` | integer | no | `30` | Target length in seconds: Lite 5–30, Standard 5–120, or Pro 5–300 |
| `quality` | string | no | `standard` | `lite`, `standard`, or `pro` |
| `scenario` | string | no | `auto` | Lite: `auto`, `narrated`, or `captions`; Standard adds `avatar`; Pro adds `drama` |
| `style` | string | no | `auto` | Named preset or freeform visual-style hint |
| `voice` | string | no | `auto` | Voice preset or a 32-hex-character Fish reference ID |
| `callback_url` | string | no | - | Public webhook URL called when the task reaches a terminal state |

### Actions

- `generate`: produce a new video.
- `remix`: reinterpret an earlier video while retaining it as creative context.
- `edit`: apply targeted changes to an earlier video.
- `extend`: continue or lengthen an earlier video.

Every non-`generate` action requires `ref_task_id` and creates a new task ID.

### Production SKUs

- `lite`: 720p/24fps production for 5–30-second videos.
- `standard`: 1080p/30fps production for 5–120-second videos.
- `pro`: 1080p/30fps high-bitrate production for 5–300-second videos.

Lite supports `generate` and `edit`; Standard adds `remix`; Pro adds `extend`. Every non-`generate` action requires `ref_task_id`.

### Scenarios

- `auto`: let the director choose from the brief.
- `narrated`: multi-scene explainer, documentary, brand, history, or product video.
- `captions`: automatic subtitles for a source video supplied in `file_urls`.
- `avatar`: talking-head or digital-human production. Supply a usable portrait in `file_urls`.
- `drama`: character and dialogue-driven short drama.

Lite supports `auto`, `narrated`, and `captions`; Standard adds `avatar`; Pro adds `drama`.

### Styles and Voices

Named style presets include `cinematic`, `glass`, `luxury`, `swiss`, `modern`, `editorial`, `warm`, `vibrant`, `neon`, `mono`, `pastel`, `bold`, `industrial`, `futuristic`, and `retro`. A freeform style string is also accepted as a soft direction.

Voice presets include:

- `auto`
- `warm-female`, `bright-female`, `anchor-female`, `clean-female`
- `calm-male`, `deep-male`, `documentary-male`, `energetic-male`, `storyteller-male`

Voice controls timbre, not language. One preset can speak each language in `langs`. Advanced callers may pass a 32-hex-character Fish `reference_id` instead of a preset.

## Create a Video

```bash
curl --request POST 'https://api.acedata.cloud/maestro/videos' \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "prompt": "Create a concise product launch video for first-time customers. Show the camera body and close with a clear call to action.",
    "file_urls": [
      "https://example.com/product.jpg",
      "https://example.com/logo.png"
    ],
    "langs": ["en", "de"],
    "aspect": "16:9",
    "duration": 45,
    "quality": "pro",
    "scenario": "narrated",
    "style": "editorial",
    "voice": "documentary-male"
  }'
```

Python example:

```python
import os

import requests

response = requests.post(
    "https://api.acedata.cloud/maestro/videos",
    headers={
        "Authorization": f"Bearer {os.environ['ACEDATACLOUD_API_TOKEN']}",
        "Content-Type": "application/json",
    },
    json={
        "prompt": "Create a concise product launch video for first-time customers.",
        "file_urls": ["https://example.com/product.jpg"],
        "langs": ["en", "de"],
        "aspect": "16:9",
        "duration": 45,
        "quality": "pro",
        "scenario": "narrated",
        "style": "editorial",
    },
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

Accepted response shape:

```json
{
  "success": true,
  "task_id": "f57e99c4-f60f-4373-a155-17742ce2357d",
  "trace_id": "70e1cb12-c619-4292-a416-90191205996b"
}
```

- `task_id`: UUID used with `POST /maestro/tasks`.
- `trace_id`: request trace identifier for diagnostics and support.

An accepted task is not a completed video. Poll the returned task ID before presenting an output URL.

## Reference Media

`file_urls` accepts public image, video, and audio URLs. Typical uses include product photos, logos, portrait references, source footage, and reference audio. Local paths are not accessible to the service; upload local files to public storage first.

## Multilingual Production

Pass several language codes in `langs`. Lite supports one language, Standard supports up to two, and Pro supports up to four:

```json
{
  "prompt": "Explain the three main benefits of our customer-support product.",
  "langs": ["zh-cn", "en", "ja"],
  "aspect": "16:9",
  "duration": 30
}
```

Successful output is represented by delivered items in `response.data.variants`. Inspect the actual variants instead of assuming every requested language was produced; each delivered language after the first costs 6 additional credits.

## Remix, Edit, or Extend

```bash
curl --request POST 'https://api.acedata.cloud/maestro/videos' \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "action": "edit",
    "ref_task_id": "f57e99c4-f60f-4373-a155-17742ce2357d",
    "prompt": "Keep the structure and visuals. Tighten the opening and use a warmer narrator."
  }'
```

The response contains a new `task_id`. Retrieve that new task for the revised output; the source task remains unchanged. Lite supports `edit`, Standard adds `remix`, and Pro adds `extend`.

## Billing

Maestro settles a successful job after production based on actual delivered duration, SKU, scenario, and language variants; billed duration never exceeds the requested duration. Failed tasks are not charged, and polling `POST /maestro/tasks` is free.

`credits = delivered duration in seconds × SKU price per second × scenario multiplier + 6 × max(delivered language count − 1, 0)`

| SKU | Price per second | Maximum duration | Output | Added scenarios and actions |
|---|---:|---:|---|---|
| `lite` | 0.20 credits | 30 seconds | 720p / 24fps | `auto`, `narrated`, `captions`; `generate`, `edit` |
| `standard` | 0.60 credits | 120 seconds | 1080p / 30fps | Adds `avatar` and `remix` |
| `pro` | 1.20 credits | 300 seconds | 1080p / 30fps high bitrate | Adds `drama` and `extend` |

`avatar` has a 1.15× multiplier, `drama` has a 1.35× multiplier, and all other scenarios use 1×.

## Errors

Field validation is performed by the Maestro service. A missing `prompt`, an invalid `action`, a `remix`/`edit`/`extend` without `ref_task_id`, a non-list `file_urls`, or an invalid `quality` or `voice` returns HTTP 400 with a plain `detail` message:

```json
{
  "detail": "missing field: prompt"
}
```

Gateway-level rejections (authentication, balance, rate limiting, infrastructure) use the standard envelope instead:

```json
{
  "error": {
    "code": "bad_request",
    "message": "Request validation failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

Relevant gateway codes include `bad_request`, `no_token`, `invalid_token`, `token_expired`, `token_mismatched`, `used_up`, `forbidden`, `too_many_requests`, `api_error`, and `timeout`. Use the HTTP status and `trace_id` when handling or reporting failures.

## Next Step

Use the [Maestro Tasks API guide](maestro_tasks_api_integration_guide.md) to retrieve progress and finished variants.