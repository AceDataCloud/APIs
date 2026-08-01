# OpenAI Audio Transcriptions API (/v1/audio/transcriptions)
Convert uploaded audio files into text with an interface compatible with OpenAI's `/v1/audio/transcriptions` API. Use your Ace Data Cloud token in the `Authorization` header and call the endpoint directly or through the official OpenAI SDK by changing the `base_url`.

## Application Process
Get your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications). The same token works across the OpenAI-compatible APIs on the platform, so no separate application is required for transcription.

## Endpoint
```text
POST https://api.acedata.cloud/v1/audio/transcriptions
```

## Request Headers
- `authorization: ******`
- `content-type: multipart/form-data`

## Request Parameters
| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | file | yes | Audio file to transcribe. Maximum size is **25 MB**. Supported formats: `flac`, `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `ogg`, `wav`, `webm`. |
| `model` | string | no | `whisper-1` (default) or `gpt-transcribe`. |
| `language` | string | no | ISO-639-1 language code such as `en` or `zh`. Leave blank for automatic detection. |
| `prompt` | string | no | Extra context or terminology hints to improve recognition quality. |
| `response_format` | string | no | For `whisper-1`: `json` (default), `text`, `srt`, `verbose_json`, or `vtt`. For `gpt-transcribe`: `json` or `text`. |
| `temperature` | number | no | Sampling temperature from `0` to `1`, default `0`. |
| `timestamp_granularities[]` | array | no | `word` or `segment`. Supported only by `whisper-1` and requires `response_format=verbose_json`. |
| `languages[]` | array | no | Candidate languages (ISO-639-1). Supported only by `gpt-transcribe`; do not send together with `language`. |
| `keywords[]` | array | no | Domain terms or proper nouns to bias recognition. Supported only by `gpt-transcribe`. |
| `stream` | boolean | no | Streaming is not supported. If provided, the API still returns the full result in a normal response. |

## Which Model Should You Choose?
| Capability | `whisper-1` | `gpt-transcribe` |
| --- | --- | --- |
| Price | $0.0078 / minute | **$0.0059 / minute** |
| Accuracy | Good | **Better**, especially for brand names and proper nouns |
| Subtitle output (`srt` / `vtt`) | ✅ | ❌ |
| Word-level timestamps | ✅ | ❌ |
| `languages[]` / `keywords[]` | ❌ | ✅ |
| Detected language in response | Requires `verbose_json` | Returned by default |

**Choose `whisper-1` when you need subtitle files or timestamps. For most other cases, `gpt-transcribe` is the better and cheaper default.**

## Example
### CURL
```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F 'file=@sample.mp3' \
  -F 'model=gpt-transcribe' \
  -F 'languages[]=en' \
  -F 'keywords[]=Ace Data Cloud'
```

### Python
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.acedata.cloud/v1",
    api_key="{token}",
)

with open("sample.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="gpt-transcribe",
    )

print(transcript)
```

## Notes
- The endpoint does **not** support streaming output.
- Parameters unsupported by the selected model return `400` instead of being silently ignored.
- Requests can take a while to finish. A client timeout of at least **300 seconds** is recommended for long audio.

## Error Codes
| Status | code | Description |
| --- | --- | --- |
| 400 | `bad_request` | Missing `file`, invalid audio, invalid parameter combination, unsupported `model` or `response_format`, invalid `temperature`, or model-specific parameter misuse. |
| 401 | `authentication_failed` | Invalid token. |
| 403 | `used_up` | Insufficient balance. |
| 413 | `request_too_large` | The uploaded audio exceeds the 25 MB limit. |
| 429 | `too_many_requests` | The service is busy; retry later. |
| 500 | `api_error` | Internal service error; retry later. |
