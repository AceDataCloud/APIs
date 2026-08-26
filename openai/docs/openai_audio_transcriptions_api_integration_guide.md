# OpenAI Audio Transcriptions API Application and Usage

The OpenAI Audio Transcriptions API converts uploaded audio files into text.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. A single API Token works across every service on the platform.

## Endpoint

```http
POST https://api.acedata.cloud/v1/audio/transcriptions
```

## Request Headers

- `authorization: ******`
- `content-type: multipart/form-data`

## Request Body

| Field | Type | Required | Description |
| ---- | ---- | ---- | ---- |
| `file` | binary | Yes | Audio file to transcribe. |
| `model` | string | No | `whisper-1` or `gpt-transcribe`. Defaults to `whisper-1`. |
| `language` | string | No | Language hint for the audio. |
| `prompt` | string | No | Optional context prompt. |
| `response_format` | string | No | `json`, `text`, `srt`, `verbose_json`, or `vtt`. Defaults to `json`. |
| `temperature` | number | No | Sampling temperature. Defaults to `0`. |
| `timestamp_granularities[]` | string[] | No | Timestamp granularities: `word` and/or `segment`. |
| `stream` | boolean | No | When `true`, returns transcription events as `text/event-stream`. Defaults to `false`. |
| `languages[]` | string[] | No | Candidate languages for recognition. |
| `keywords[]` | string[] | No | Keywords to improve recognition. |

## Code Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  -H 'authorization: ******' \
  -F 'file=@speech.mp3' \
  -F 'model=whisper-1' \
  -F 'response_format=json'
```

```python
import requests

url = "https://api.acedata.cloud/v1/audio/transcriptions"
headers = {"authorization": "******"}
with open("speech.mp3", "rb") as audio:
    files = {"file": audio}
    data = {"model": "whisper-1", "response_format": "json"}
    response = requests.post(url, headers=headers, files=files, data=data)

print(response.json())
```

## Response Examples

JSON response:

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint. The quick brown fox jumps over the lazy dog."
}
```

Streaming response when `stream` is `true`:

```text
data: {"type":"transcript.text.delta","delta":"Hello"}

data: {"type":"transcript.text.done","text":"Hello world","usage":{"type":"tokens","input_tokens":14,"output_tokens":3,"total_tokens":17}}
```

## Error Handling

Common error responses include:

- `400 bad_request`: Missing audio `file`.
- `401 authentication_failed`: Invalid token.
- `403 used_up`: Insufficient balance.
- `413 request_too_large`: File is too large.
- `429 too_many_requests`: Transcription service is busy.
- `500 api_error`: Failed to transcribe the audio.
