# OpenAI Models, Audio, and Realtime API Integration Guide

This guide covers OpenAI-compatible utility endpoints that are available through Ace Data Cloud in addition to chat, responses, images, embeddings, and tasks.

## Authentication

Use the same Ace Data Cloud OpenAI service token as the other OpenAI endpoints:

- HTTP endpoints: `Authorization: ******`
- Browser Realtime WebSocket connections: pass `realtime, acedata-token.<YOUR_API_KEY>` via `Sec-WebSocket-Protocol`

## Models API

List available models for the account.

```bash
curl -X GET "https://api.acedata.cloud/openai/models" \
  -H "accept: application/json" \
  -H "authorization: ******"
```

Successful responses include `object: "list"` and a `data` array of model objects with fields such as `id`, `object`, `created`, and `owned_by`.

## Audio Speech API

Generate speech audio from text.

```bash
curl -X POST "https://api.acedata.cloud/v1/audio/speech" \
  -H "authorization: ******" \
  -H "content-type: application/json" \
  --output speech.mp3 \
  -d '{
    "model": "tts-1-hd",
    "input": "Hello from AceData Cloud.",
    "voice": "nova",
    "response_format": "mp3"
  }'
```

Request fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `input` | string | Yes | Text to synthesize. |
| `model` | string | No | `tts-1` or `tts-1-hd`; defaults to `tts-1-hd`. |
| `voice` | string | No | `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer`; defaults to `alloy`. |
| `response_format` | string | No | `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`; defaults to `mp3`. |
| `speed` | number | No | Speech speed; defaults to `1.0`. |

## Audio Transcriptions API

Transcribe an uploaded audio file.

```bash
curl -X POST "https://api.acedata.cloud/v1/audio/transcriptions" \
  -H "authorization: ******" \
  -F "file=@/path/to/audio.mp3" \
  -F "model=whisper-1" \
  -F "response_format=json"
```

Request fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | file | Yes | Audio file to transcribe. |
| `model` | string | No | `whisper-1` or `gpt-transcribe`; defaults to `whisper-1`. |
| `language` | string | No | Input language hint. |
| `prompt` | string | No | Prompt to guide transcription. |
| `response_format` | string | No | `json`, `text`, `srt`, `verbose_json`, or `vtt`; defaults to `json`. |
| `temperature` | number | No | Sampling temperature; defaults to `0`. |
| `timestamp_granularities[]` | string[] | No | Timestamp granularity values: `word` or `segment`. |
| `stream` | boolean | No | Whether to stream transcription events; defaults to `false`. |

The JSON response contains a `text` field. When `stream=true`, the endpoint can return `text/event-stream` events such as `transcript.text.delta` and `transcript.text.done`.

## Realtime API

Create a low-latency speech-to-speech WebSocket session using the OpenAI Realtime GA event protocol.

```bash
wscat -c "wss://api.acedata.cloud/v1/realtime?model=gpt-realtime-2.1&voice=alloy" \
  -H "Authorization: ******"
```

Query parameters:

| Field | Required | Description |
| --- | --- | --- |
| `model` | Yes | Realtime model. Use `gpt-realtime-2.1` for best quality or `gpt-realtime-2.1-mini` for lower cost. Older compatible values include `gpt-realtime-2`, `gpt-realtime`, and `gpt-realtime-mini`. |
| `voice` | No | Output voice selected when the connection is established. Values include `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`; defaults to `alloy`. |

The client and server exchange Realtime JSON events such as `session.update`, `input_audio_buffer.append`, `response.create`, `response.output_audio.delta`, and `response.done`. Audio transport is fixed to mono PCM16 at 24 kHz. Invalid session changes return recoverable `error` events and keep the WebSocket open.

## Error Handling

Common error responses use JSON with an `error` object and `trace_id`.

- `400 bad_request`: Missing or invalid request data.
- `401 authentication_failed` or `invalid_token`: Missing or invalid token.
- `403 used_up`: Insufficient account balance.
- `413 request_too_large`: Uploaded transcription file is too large.
- `429 too_many_requests`: Rate limit or service busy.
- `500 api_error`: Internal server error.
