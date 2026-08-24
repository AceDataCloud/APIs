# OpenAI Audio Transcriptions API Application and Usage

The OpenAI Audio Transcriptions API transcribes uploaded audio files into text.

## Application Process

Use an Ace Data Cloud API token from the [console](https://platform.acedata.cloud/console/applications). Send the token in the `Authorization` header.

## Endpoint

```text
POST https://api.acedata.cloud/v1/audio/transcriptions
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization` | Yes | Ace Data Cloud API token. |
| `Content-Type` | Yes | `multipart/form-data`. |

## Request Body

| Field | Required | Description |
| --- | --- | --- |
| `file` | Yes | Audio file to transcribe. |
| `model` | No | `whisper-1` or `gpt-transcribe`; defaults to `whisper-1`. |
| `language` | No | Input language hint. |
| `prompt` | No | Optional prompt to guide transcription. |
| `response_format` | No | `json`, `text`, `srt`, `verbose_json`, or `vtt`; defaults to `json`. |
| `temperature` | No | Sampling temperature; defaults to `0`. |
| `timestamp_granularities[]` | No | `word` or `segment` timestamps. |
| `stream` | No | Set to `true` for streaming transcription events. |
| `languages[]` | No | Candidate languages for transcription. |
| `keywords[]` | No | Keywords to improve recognition. |

## Basic Usage

```shell
curl -X POST "https://api.acedata.cloud/v1/audio/transcriptions" \
  -H "Authorization: ******" \
  -F "file=@speech.mp3" \
  -F "model=whisper-1" \
  -F "response_format=json"
```

```python
import requests

url = "https://api.acedata.cloud/v1/audio/transcriptions"
headers = {"authorization": "******"}
files = {"file": open("speech.mp3", "rb")}
data = {
    "model": "whisper-1",
    "response_format": "json",
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.text)
```

## Response Example

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint."
}
```

## Error Handling

Invalid requests return `400`, invalid tokens return `401`, insufficient balance returns `403`, files that are too large return `413`, rate limits return `429`, and server errors return `500`.

## Conclusion

Use this endpoint for OpenAI-compatible audio transcription workflows.
