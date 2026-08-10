# OpenAI Audio Transcriptions API Integration and Usage

The OpenAI Audio Transcriptions API converts uploaded audio into text. It accepts `multipart/form-data` and is compatible with OpenAI-style transcription parameters.

## Endpoint

```text
POST https://api.acedata.cloud/v1/audio/transcriptions
```

Use your Ace Data Cloud API token in the `Authorization` header.

## Request Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | string | Yes |  | Openai Audio Transcriptions File |
| `model` | string enum: `whisper-1`, `gpt-transcribe` | No | `whisper-1` | Openai Audio Transcriptions Model |
| `language` | string | No |  | Openai Audio Transcriptions Language |
| `prompt` | string | No |  | Openai Audio Transcriptions Prompt |
| `response_format` | string enum: `json`, `text`, `srt`, `verbose_json`, `vtt` | No | `json` | Openai Audio Transcriptions Response Format |
| `temperature` | number | No | `0` | Openai Audio Transcriptions Temperature |
| `timestamp_granularities[]` | array | No |  | Openai Audio Transcriptions Timestamp Granularities |
| `stream` | boolean | No | `False` | Openai Audio Transcriptions Stream |
| `languages[]` | array | No |  | Openai Audio Transcriptions Languages |
| `keywords[]` | array | No |  | Openai Audio Transcriptions Keywords |

## CURL Code Example

```bash
curl --request POST "https://api.acedata.cloud/v1/audio/transcriptions" \
  --header "Authorization: ******" \
  --form "file=@/path/to/audio.mp3" \
  --form "model=whisper-1" \
  --form "response_format=json"
```

## Response Example

```json
{
  "text": "Ace Data Cloud Platform is testing the speech recognition endpoint. The quick brown fox jumps over the lazy dog."
}
```

Set `response_format` to `text`, `srt`, `verbose_json`, or `vtt` when you need another response shape. When `stream` is enabled, the API can return `text/event-stream` transcript events.
