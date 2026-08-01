# OpenAI Audio Transcriptions API Application and Usage

The OpenAI Audio Transcriptions API transcribes audio into text and is **fully compatible with OpenAI's `/v1/audio/transcriptions`**. Any OpenAI SDK can be pointed at `https://api.acedata.cloud` by changing `base_url`, with your AceData Token as the API key, and will work immediately without any other modifications.

This document mainly introduces the usage process of the OpenAI Audio Transcriptions API, allowing you to easily transcribe audio using the Whisper model.

## Application Process

To use the OpenAI Audio Transcriptions API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [OpenAI Audio Transcriptions API →](https://platform.acedata.cloud/documents/openai-audio-transcriptions)

## Endpoint

```
POST https://api.acedata.cloud/v1/audio/transcriptions
```

- **Authorization**: `Authorization: ******` request header
- **Request format**: `multipart/form-data`
- **Billing**: charged by audio duration; durations under 1 second are billed as 1 second.

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | file | yes | Audio file to transcribe, maximum 25 MB. Supports `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, `webm`. |
| `model` | string | no | Transcription model. Currently supports `whisper-1` (default). |
| `language` | string | no | Language of the audio as an ISO-639-1 code (e.g. `en`, `zh`). Providing this improves accuracy and speed; omit to auto-detect. |
| `prompt` | string | no | A prompt to guide the writing style, or to supply proper nouns and terminology that improve recognition accuracy. |
| `response_format` | string | no | `json` (default), `text`, `srt`, `verbose_json`, or `vtt`. |
| `temperature` | number | no | Sampling temperature from 0–1, default 0. |
| `timestamp_granularities[]` | array | no | Timestamp granularity: `word` or `segment`. Must be used with `response_format=verbose_json`. |
| `stream` | boolean | no | `whisper-1` does not support streaming; this parameter is accepted but ignored, and a complete result is always returned (consistent with OpenAI's official behavior). |

## Basic Usage

Below is a basic cURL example:

```shell
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1
```

The response is as follows:

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint. The quick brown fox jumps over the lazy dog."
}
```

Equivalent Python sample code:

```python
import requests

url = "https://api.acedata.cloud/v1/audio/transcriptions"

headers = {
    "authorization": "******"
}

files = {
    "file": open("audio.mp3", "rb")
}
data = {
    "model": "whisper-1"
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.text)
```

## Using the Official OpenAI SDK

If you are already using the official OpenAI Python SDK, you only need to change `base_url` and `api_key`:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.acedata.cloud/v1",
    api_key="{token}"
)

with open("audio.mp3", "rb") as f:
    result = client.audio.transcriptions.create(model="whisper-1", file=f)

print(result.text)
```

## Generating Subtitles

Set `response_format` to `srt` or `vtt` to receive a ready-to-use subtitle file directly:

```shell
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F response_format=srt \
  -o subtitle.srt
```

The response content (`Content-Type: text/plain`):

```
1
00:00:00,000 --> 00:00:03,800
Ace Data Cloud Platform is testing the speech recognition endpoint.

2
00:00:03,800 --> 00:00:06,280
The quick brown fox jumps over the lazy dog.
```

## Word-Level Timestamps

When you need start and end times for every word, use `verbose_json` together with `timestamp_granularities[]=word`:

```shell
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  -F response_format=verbose_json \
  -F 'timestamp_granularities[]=word'
```

The response is as follows:

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

## Pricing

| Model | Price |
| --- | --- |
| `whisper-1` | $0.0078 / minute |

> Billed by actual audio duration. Durations under 1 second are billed as 1 second; a single request is capped at 1 hour.

## Notes

- Single file maximum is **25 MB**. For larger files, split or compress first (reducing bit rate is usually sufficient; audio quality requirements for speech recognition are not high).
- This endpoint **does not support streaming** (`stream` parameter is accepted but ignored and a complete result is always returned).
- Parameters are consistent with OpenAI's official `/v1/audio/transcriptions`; any official SDK just needs `base_url` changed.
- `include[]`, `chunking_strategy`, `languages[]`, `keywords[]`, `known_speaker_names[]`, and `known_speaker_references[]` are capabilities of other transcription models. `whisper-1` does not support them; supplying them returns a 400 error rather than silently ignoring them.
- Requests can be time-consuming; the recommended client timeout is at least 300 seconds.

## Error Handling

| Status | code | Description |
| --- | --- | --- |
| 400 | `bad_request` | No `file` provided, file cannot be parsed, or an invalid parameter was supplied (`model`/`response_format` value unsupported, `temperature` outside 0–1, `timestamp_granularities[]` used without `verbose_json`, or an unsupported parameter passed for `whisper-1`). |
| 401 | `authentication_failed` | Token is invalid. |
| 403 | `used_up` | Insufficient balance. |
| 413 | `request_too_large` | Audio file exceeds the 25 MB limit. |
| 429 | `too_many_requests` | Too many requests; please retry later. |
| 500 | `api_error` | Internal service error; please retry later. |

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

## Conclusion

Through this document, you have learned how to easily transcribe audio into text using the OpenAI Audio Transcriptions API. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
