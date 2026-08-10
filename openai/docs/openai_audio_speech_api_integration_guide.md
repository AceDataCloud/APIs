# OpenAI Audio Speech API Integration and Usage

The OpenAI Audio Speech API converts input text to spoken audio through the Ace Data Cloud OpenAI-compatible endpoint.

## Endpoint

```text
POST https://api.acedata.cloud/v1/audio/speech
```

Use your Ace Data Cloud API token in the `Authorization` header and send a JSON request body.

## Request Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `model` | string enum: `tts-1`, `tts-1-hd` | No | `tts-1-hd` | Openai Audio Speech Model |
| `input` | string | Yes |  | Openai Audio Speech Input |
| `voice` | string enum: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer` | No | `alloy` | Openai Audio Speech Voice |
| `response_format` | string enum: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` | No | `mp3` | Openai Audio Speech Response Format |
| `speed` | number | No | `1.0` | Openai Audio Speech Speed |

## CURL Code Example

```bash
curl --request POST "https://api.acedata.cloud/v1/audio/speech" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --output speech.mp3 \
  --data '{
    "model": "tts-1-hd",
    "input": "Hello from AceData Cloud.",
    "voice": "nova",
    "response_format": "mp3"
  }'
```

## Response

A successful request returns binary audio. The current OpenAPI response content type is `audio/mpeg`; choose the file extension that matches your `response_format`.

Error responses are JSON objects with an `error` object and `trace_id` for support.
