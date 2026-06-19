# Fish TTS API Integration Guide

This document introduces the integration guide for the Fish TTS API. This interface is fully compatible with the [Fish Audio official OpenAPI](https://docs.fish.audio/text-to-speech/text-to-speech), allowing you to directly migrate existing code calling `https://api.fish.audio/v1/tts` to `https://api.acedata.cloud/fish/tts` by simply replacing the authentication information without modifying the request body structure.

## Application Process

To use Fish TTS API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish TTS API →](https://platform.acedata.cloud/services/fish)

## Differences from the Official API

This API retains the request and response fields of the Fish Audio official API with the following minor enhancements for better integration on our platform:

- **Authentication method**: Uses the standard Authorization header with your Ace Data Cloud API token, not a Fish official key.
- **TTS model selection**: Specified via the HTTP request header `model`, options are `s1` or `s2-pro`, with the default being `s2-pro`.
- **Default `latency` value**: If `latency` is omitted, this interface automatically adds `latency=normal`.
- **Asynchronous callback**: When an additional `callback_url` field is included in the request body, the API can be paired with `POST /fish/tasks` to track the asynchronous result.

Apart from the above differences, request body fields such as `text`, `reference_id`, `references`, `prosody`, `format`, `sample_rate`, `mp3_bitrate`, `chunk_length`, `temperature`, `top_p`, and `normalize` are transparently passed upstream.

## Basic Usage

The minimal request only requires the `text` field.

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a Fish-Audio-compatible test."
  }'
```

Example response:

```json
{
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

If you want to use a cloned voice, add `reference_id` in the request body:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a Fish-Audio-compatible test.",
    "reference_id": "d7900c21663f485ab63ebdb7e5905036",
    "format": "mp3",
    "sample_rate": 44100
  }'
```

## Request Parameters

- `text` (required): Text content to synthesize.
- `reference_id`: Optional cloned voice ID returned by the Fish model APIs.
- `format`: Optional audio format. Supported values are `mp3`, `wav`, `pcm`, and `opus`.
- `sample_rate`: Optional output sample rate.
- `mp3_bitrate`: Optional MP3 bitrate. Supported values are `64`, `128`, and `192`.
- `opus_bitrate`: Optional Opus bitrate.
- `latency`: Optional latency mode. Supported values are `normal` and `balanced`.
- `chunk_length`, `min_chunk_length`, `temperature`, `top_p`, `repetition_penalty`, `max_new_tokens`, `normalize`, `prosody`, `references`: Optional advanced synthesis controls.
- `callback_url`: Optional webhook URL for asynchronous processing.
- `async`: Optional boolean to enable asynchronous processing semantics on the platform side.

## Asynchronous Tasks

For long-running synthesis requests, you can include `callback_url` and then poll the task using the [Fish Tasks API](https://platform.acedata.cloud/documents/fish-tasks).

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a Fish-Audio-compatible test.",
    "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
  }'
```

After the task completes, the final result can be retrieved from your callback receiver or polled with `POST /fish/tasks`.

## Error Handling

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Unsupported request method or parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `404 no_api`: API does not exist, please make sure the URL is correct.
- `429 too_many_requests`: Too many requests, rate limit exceeded.
- `500 api_error`: Internal server error.

### Error Response Example

```json
{
  "error": {
    "code": "api_error",
    "message": "Internal server error."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Conclusion

The Fish TTS API lets you keep a Fish Audio-compatible request format while benefiting from Ace Data Cloud authentication, usage accounting, and task polling support.
