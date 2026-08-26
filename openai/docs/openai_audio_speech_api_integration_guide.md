# OpenAI Audio Speech API Application and Usage

The OpenAI Audio Speech API synthesizes speech audio from text input.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. A single API Token works across every service on the platform.

## Endpoint

```http
POST https://api.acedata.cloud/v1/audio/speech
```

## Request Headers

- `accept: audio/mpeg`
- `authorization: ******`
- `content-type: application/json`

## Request Body

| Field | Type | Required | Description |
| ---- | ---- | ---- | ---- |
| `input` | string | Yes | Text to synthesize. |
| `model` | string | No | `tts-1` or `tts-1-hd`. Defaults to `tts-1-hd`. |
| `voice` | string | No | `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer`. Defaults to `alloy`. |
| `response_format` | string | No | `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`. Defaults to `mp3`. |
| `speed` | number | No | Playback speed multiplier. Defaults to `1.0`. |

## Code Example

```bash
curl -X POST 'https://api.acedata.cloud/v1/audio/speech' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  --output speech.mp3 \
  -d '{
    "model": "tts-1-hd",
    "input": "Hello from AceData Cloud.",
    "voice": "nova",
    "response_format": "mp3"
  }'
```

```python
import requests

url = "https://api.acedata.cloud/v1/audio/speech"
headers = {
    "authorization": "******",
    "content-type": "application/json",
}
payload = {
    "model": "tts-1-hd",
    "input": "Hello from AceData Cloud.",
    "voice": "nova",
    "response_format": "mp3",
}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

## Response

A successful request returns binary audio content. For `response_format: "mp3"`, the response content type is `audio/mpeg`.

## Error Handling

Common error responses include:

- `400 bad_request`: Missing or empty `input` text.
- `401 authentication_failed`: Invalid token.
- `403 used_up`: Insufficient balance.
- `429 too_many_requests`: Rate limit exceeded.
- `500 api_error`: Internal server error.
