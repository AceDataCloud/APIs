# Integration and Use of OpenAI Audio Transcriptions API

The OpenAI Audio Transcriptions API transcribes audio files into text. It is **fully compatible with OpenAI's `/v1/audio/transcriptions`** endpoint — any OpenAI SDK can point its `base_url` at `https://api.acedata.cloud` and swap the key for your AceData Token to use this API without any other code changes. The endpoint returns the transcription synchronously.

## Application Process

To use the OpenAI Audio Transcriptions API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Endpoint

```
POST https://api.acedata.cloud/v1/audio/transcriptions
```

## Request Headers

- `authorization: ******
- `content-type: multipart/form-data`

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | file | yes | The audio file to transcribe (max 25 MB). Supported formats: `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, `webm`. |
| `model` | string | no | Transcription model. Currently supports `whisper-1` (default). |
| `language` | string | no | Language of the audio, in ISO-639-1 format (e.g. `en`, `zh`). Specifying the language improves accuracy and speed; leave blank for automatic detection. |
| `prompt` | string | no | Optional text to guide the model's style, or provide proper nouns and terminology to improve recognition accuracy. |
| `response_format` | string | no | Output format: `json` (default), `text`, `srt`, `verbose_json`, or `vtt`. |
| `temperature` | number | no | Sampling temperature between 0 and 1, default `0`. |
| `timestamp_granularities[]` | array | no | Timestamp granularity: `word` or `segment`. Requires `response_format=verbose_json`. |

## Basic Usage

### CURL

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1
```

### Python

```python
import requests

url = "https://api.acedata.cloud/v1/audio/transcriptions"
headers = {
    "authorization": "******",
}
with open("audio.mp3", "rb") as f:
    files = {"file": f}
    data = {"model": "whisper-1"}
    response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

### Response Example

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint. The quick brown fox jumps over the lazy dog."
}
```

## Advanced Usage

### Generate Subtitles

Set `response_format` to `srt` or `vtt` to get a ready-to-use subtitle file:

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F response_format=srt \
  -o subtitle.srt
```

Response body (`Content-Type: text/plain`):

```
1
00:00:00,000 --> 00:00:03,800
Ace Data Cloud Platform is testing the speech recognition endpoint.

2
00:00:03,800 --> 00:00:06,280
The quick brown fox jumps over the lazy dog.
```

### Word-Level Timestamps

Use `verbose_json` with `timestamp_granularities[]=word` to get per-word start/end times:

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F response_format=verbose_json \
  -F 'timestamp_granularities[]=word'
```

Response:

```json
{
  "task": "transcribe",
  "language": "english",
  "duration": 6.29,
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint. The quick brown fox jumps over the lazy dog.",
  "words": [
    { "word": "Ace", "start": 0.0, "end": 0.32 },
    { "word": "Data", "start": 0.32, "end": 0.54 },
    { "word": "Cloud", "start": 0.54, "end": 0.86 }
  ]
}
```

### Using the Official OpenAI SDK

Because this endpoint is OpenAI-compatible, you can use the official `openai` Python library by setting `base_url`:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.acedata.cloud/v1",
    api_key="<token>",
)
with open("audio.mp3", "rb") as f:
    result = client.audio.transcriptions.create(model="whisper-1", file=f)
print(result.text)
```

## Pricing

| Model | Price |
| --- | --- |
| `whisper-1` | $0.0078 / minute |

Billing is based on actual audio duration; durations under 1 second are rounded up to 1 second. A single request is capped at 1 hour.

## Error Handling

| Status Code | Code | Description |
| --- | --- | --- |
| 400 | `bad_request` | No `file` provided, the file could not be parsed, or a parameter is invalid. |
| 401 | `authentication_failed` | The token is invalid. |
| 403 | `used_up` | Your balance is not enough. |
| 413 | `request_too_large` | The audio file exceeds the 25 MB limit. |
| 429 | `too_many_requests` | Transcription upstream is busy; please try again later. |
| 500 | `api_error` | Failed to transcribe the audio; please try again later. |

### Error Response Example

```json
{
  "error": {
    "code": "bad_request",
    "message": "Please provide an audio `file` to transcribe."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Notes

- Single file maximum size is **25 MB**. For larger files, split them or reduce the bitrate first.
- This endpoint **does not support streaming** (`stream` parameter is ignored).
- Requests can take some time to complete; set your client timeout to at least 300 seconds.
