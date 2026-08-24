The OpenAI Audio Transcriptions API transcribes an uploaded audio file.

## Authentication

Send your Ace Data Cloud API Token with HTTP bearer authentication. Requests use `multipart/form-data`.

## Request Fields

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `file` | binary | Yes | - | Audio file to transcribe. |
| `model` | string | No | `whisper-1` | `whisper-1` or `gpt-transcribe`. |
| `language` | string | No | - | Input language hint. |
| `prompt` | string | No | - | Text that guides transcription style or vocabulary. |
| `response_format` | string | No | `json` | `json`, `text`, `srt`, `verbose_json`, or `vtt`. |
| `temperature` | number | No | `0` | Sampling temperature. |
| `timestamp_granularities[]` | array | No | - | Requested timestamp granularities. |
| `stream` | boolean | No | `false` | Return server-sent events when enabled. |
| `languages[]` | array | No | - | Language hints. |
| `keywords[]` | array | No | - | Keyword hints. |

## Transcribe Audio

```bash
curl --request POST 'https://api.acedata.cloud/v1/audio/transcriptions' \
  --header 'Authorization: ******' \
  --form 'file=@speech.mp3' \
  --form 'model=whisper-1' \
  --form 'response_format=json'
```

JSON response:

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint."
}
```

With `stream=true`, the endpoint returns `text/event-stream` transcript delta and completion events.

## Errors

- `400`: Invalid request parameters.
- `401`: Missing or invalid API Token.
- `403`: Access denied.
- `413`: Uploaded file is too large.
- `429`: Rate limit exceeded.
- `500`: Internal service error.
