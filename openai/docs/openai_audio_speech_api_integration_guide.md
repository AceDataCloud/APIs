# OpenAI Audio Speech API Application and Usage

The OpenAI Audio Speech API converts input text into speech audio.

## Application Process

Use an Ace Data Cloud API token from the [console](https://platform.acedata.cloud/console/applications). Send the token in the `Authorization` header.

## Endpoint

```text
POST https://api.acedata.cloud/v1/audio/speech
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| `Authorization` | Yes | Ace Data Cloud API token. |
| `Content-Type` | Yes | `application/json`. |

## Request Body

| Field | Required | Description |
| --- | --- | --- |
| `input` | Yes | Text to synthesize. |
| `model` | No | `tts-1` or `tts-1-hd`; defaults to `tts-1-hd`. |
| `voice` | No | `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer`; defaults to `alloy`. |
| `response_format` | No | `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`; defaults to `mp3`. |
| `speed` | No | Speech speed; defaults to `1.0`. |

## Basic Usage

```shell
curl -X POST "https://api.acedata.cloud/v1/audio/speech" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -o speech.mp3 \
  -d '{
    "model": "tts-1-hd",
    "input": "Hello from Ace Data Cloud.",
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
    "input": "Hello from Ace Data Cloud.",
    "voice": "nova",
    "response_format": "mp3",
}

response = requests.post(url, json=payload, headers=headers)
with open("speech.mp3", "wb") as f:
    f.write(response.content)
```

## Error Handling

Invalid requests return `400`, invalid tokens return `401`, insufficient balance returns `403`, rate limits return `429`, and server errors return `500`.

## Conclusion

Use this endpoint when you need OpenAI-compatible text-to-speech generation through Ace Data Cloud.
