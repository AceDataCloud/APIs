# OpenAI Speech Recognition API (`/v1/audio/transcriptions`)

Transcribe audio with the OpenAI-compatible `POST /v1/audio/transcriptions` endpoint. Requests use `multipart/form-data`.

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | file | yes | Audio up to 25 MB: FLAC, MP3, MP4, MPEG, MPGA, M4A, OGG, WAV, or WebM. |
| `model` | string | no | `whisper-1` (default) or `gpt-transcribe`. |
| `language` | string | no | ISO-639-1 language code; omit for automatic detection. |
| `prompt` | string | no | Style, proper-noun, or terminology hint. |
| `response_format` | string | no | `whisper-1`: `json`, `text`, `srt`, `verbose_json`, or `vtt`; `gpt-transcribe`: `json` or `text`. |
| `temperature` | number | no | Sampling temperature from 0 through 1. |
| `timestamp_granularities[]` | array | no | `word` or `segment`, with `whisper-1` and `verbose_json`. |
| `languages[]` | array | no | Candidate languages for `gpt-transcribe`; do not combine with `language`. |
| `keywords[]` | array | no | Recognition hints for `gpt-transcribe`. |
| `stream` | boolean | no | Enables SSE for `gpt-transcribe`; `whisper-1` returns a complete response. |

## Basic Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1
```

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint."
}
```

For subtitles, set `response_format=srt` or `response_format=vtt`. For word-level timestamps, use:

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F response_format=verbose_json \
  -F 'timestamp_granularities[]=word'
```

## Streaming Transcription

`gpt-transcribe` supports SSE incremental output:

```bash
curl -N -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=gpt-transcribe \
  -F stream=true
```

`transcript.text.delta` events contain incremental text. `transcript.text.done` contains the complete text and usage. An `event: error` terminates failed processing; disconnecting cancels processing.

## Official SDK

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.acedata.cloud/v1", api_key="{token}")
with open("audio.mp3", "rb") as audio:
    result = client.audio.transcriptions.create(model="whisper-1", file=audio)
print(result.text)
```

The alias `POST /openai/audio/transcriptions` is also supported. Billing uses audio duration rounded up to the nearest second. A request may contain at most one hour of audio; use a client timeout of at least 300 seconds.

## Errors

- `400`: Missing or invalid file or model-specific parameters.
- `401`: Invalid authorization token.
- `403`: Insufficient balance.
- `413`: File exceeds 25 MB.
- `429`: Rate limit exceeded.
- `500`: Service error.
