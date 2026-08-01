# OpenAI Text-to-Speech API (/v1/audio/speech)
Synthesize text into natural-sounding speech with an interface that is fully compatible with OpenAI's `/v1/audio/speech` API. Point your SDK or HTTP client at `https://api.acedata.cloud` and use your Ace Data Cloud token in the `Authorization` header.

## Application Process
Get your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications). The same token works across the OpenAI-compatible APIs on the platform, so no separate application is required for speech synthesis.

## Endpoint
```text
POST https://api.acedata.cloud/v1/audio/speech
```

## Request Headers
- `authorization: ******`
- `content-type: application/json`

## Request Parameters
| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `input` | string | yes | The text to synthesize into speech. |
| `model` | string | no | `tts-1` (faster) or `tts-1-hd` (higher quality, default). |
| `voice` | string | no | `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer` (default `alloy`). |
| `response_format` | string | no | `mp3` (default), `opus`, `aac`, `flac`, `wav`, or `pcm`. |
| `speed` | number | no | Speech speed from `0.25` to `4.0`, default `1.0`. |

## Example
### CURL
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

### Python SDK
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.acedata.cloud/v1",
    api_key="{token}",
)

client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input="Hello from Ace Data Cloud.",
).stream_to_file("speech.mp3")
```

The response body is the audio file itself. Save it to disk (for example `speech.mp3`) and play it directly.

## Pricing
| Model | OpenAI official | This platform (~15% off) |
| --- | --- | --- |
| `tts-1` | $15 / 1M chars | ~$12.75 / 1M chars |
| `tts-1-hd` | $30 / 1M chars | ~$25.5 / 1M chars |

> Billing is based on request text size. The `official_price` field in the platform response shows the official OpenAI price for comparison.

## Error Codes
| Status | code | Description |
| --- | --- | --- |
| 400 | `bad_request` | Empty `input` or invalid parameters. |
| 401 | `authentication_failed` | Invalid token. |
| 403 | `used_up` | Insufficient balance. |
| 429 | `too_many_requests` | Too many requests; retry later. |
| 500 | `api_error` | Upstream or internal service error. |
