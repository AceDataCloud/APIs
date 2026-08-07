# Video Generation

## Request

`POST https://api.acedata.cloud/minimax/videos`

| Field | Type | Default | Constraints |
| --- | --- | --- | --- |
| `model` | string | `minimax-h3` | only `minimax-h3` |
| `prompt` | string | — | required, up to 7000 characters |
| `image_urls` | string[] | — | 1–9 public HTTP(S) URLs |
| `audio_urls` | string[] | — | 1–3 public WAV/MP3 URLs, requires `image_urls` |
| `resolution` | string | `2K` | `768P` or `2K` |
| `ratio` | string | `16:9` | `16:9` or `9:16` |
| `duration` | integer | 4 | 4–15 |
| `aigc_watermark` | boolean | `false` | add AIGC watermark when true |
| `async` | boolean | false | return task ID immediately |
| `callback_url` | string | — | public HTTP(S) webhook |

Mode rules: prompt only = text-to-video; one image without audio = first-frame image-to-video; multiple images or any audio = multimodal reference video.

## Resolution pricing

| Resolution | Max package price | 4-second example |
| --- | --- | --- |
| `768P` | **$0.057143/s** | $0.228572 |
| `2K` | **$0.091429/s** | $0.365716 |

Only successful tasks are billed.

## Image-to-video example

```json
{
  "model": "minimax-h3",
  "prompt": "Gentle camera push-in, natural motion, soft morning light",
  "image_urls": ["https://cdn.acedata.cloud/b1c82e4937.png"],
  "resolution": "768P",
  "duration": 4,
  "async": true
}
```

## Audio-guided example

```json
{
  "model": "minimax-h3",
  "prompt": "A dancer moves naturally to the rhythm, cuts follow the beat",
  "image_urls": ["https://cdn.acedata.cloud/b1c82e4937.png"],
  "audio_urls": ["https://cdn.acedata.cloud/6f7d62b18b.wav"],
  "resolution": "768P",
  "ratio": "9:16",
  "duration": 4,
  "async": true
}
```

## Final result fields

A successful final response contains `success`, `task_id`, `trace_id`, and `data`. The first result includes:

- `id`: public AceDataCloud task ID
- `model`: `minimax-h3`
- `mode`: `text_to_video`, `image_to_video`, or `audio_guided`
- `video_url`: AceDataCloud CDN URL
- `state`: `succeeded`
- `duration`: final billed seconds
- `ratio`: output aspect ratio
- `resolution`: output resolution

## Common errors

| HTTP | Code | Meaning |
| --- | --- | --- |
| 400 | `bad_request` | missing prompt, invalid resolution/ratio/duration, or too many assets |
| 403 | `forbidden` | content safety check failed |
| 429 | `busy` | service busy, retry later |
| 500 | `api_error` | temporary service error |
| 504 | `timeout` | wait timed out; task is not duplicated |
