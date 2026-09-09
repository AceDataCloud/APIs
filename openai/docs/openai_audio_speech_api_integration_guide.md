# OpenAI Text-to-Speech API (`/v1/audio/speech`)

Synthesize text into natural speech with the OpenAI-compatible `POST /v1/audio/speech` endpoint. The response contains the audio bytes synchronously.

## Request Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `input` | string | yes | Text to synthesize. |
| `model` | string | no | `tts-1` or `tts-1-hd` (default). |
| `voice` | string | no | `alloy` (default), `echo`, `fable`, `onyx`, `nova`, or `shimmer`. |
| `response_format` | string | no | `mp3` (default), `opus`, `aac`, `flac`, `wav`, or `pcm`. |
| `speed` | number | no | Speech speed from 0.25 through 4.0; default 1.0. |

## Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/speech' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -o speech.mp3 \
  -d '{
    "model": "tts-1-hd",
    "input": "What if one API gave you every AI video model?",
    "voice": "nova",
    "response_format": "mp3"
  }'
```

The default response has `Content-Type: audio/mpeg`; write its binary body to a file.

With the official OpenAI Python SDK:

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.acedata.cloud/v1", api_key="{token}")
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input="Hello from Ace Data Cloud."
)
response.stream_to_file("speech.mp3")
```

The alias `POST /openai/audio/speech` is also supported. Billing is based on request text size; consult current platform pricing before use.

## Errors

- `400`: Empty input or invalid parameters.
- `401`: Invalid authorization token.
- `403`: Insufficient balance.
- `429`: Rate limit exceeded.
- `500`: Service error.
