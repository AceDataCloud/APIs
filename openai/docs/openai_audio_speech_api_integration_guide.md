The OpenAI Audio Speech API converts text to speech using an OpenAI-compatible request.

## Authentication

Send your Ace Data Cloud API Token with HTTP bearer authentication.

```http
Authorization: ******
Content-Type: application/json
```

## Request Body

| Field | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `input` | string | Yes | - | Text to synthesize. |
| `model` | string | No | `tts-1-hd` | `tts-1` or `tts-1-hd`. |
| `voice` | string | No | `alloy` | `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer`. |
| `response_format` | string | No | `mp3` | `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`. |
| `speed` | number | No | `1.0` | Speech speed. |

## Generate Speech

```bash
curl --request POST 'https://api.acedata.cloud/v1/audio/speech' \
  --header 'Authorization: ******' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "tts-1-hd",
    "input": "Hello from Ace Data Cloud.",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

A successful request returns audio data. Save it using an extension matching `response_format`.

## Errors

- `400`: Invalid request parameters.
- `401`: Missing or invalid API Token.
- `403`: Access denied.
- `429`: Rate limit exceeded.
- `500`: Internal service error.
