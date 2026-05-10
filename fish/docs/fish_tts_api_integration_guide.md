# Fish TTS API Integration Guide

This article introduces the Fish TTS API integration guide. The API is fully compatible with the [Fish Audio official OpenAPI](https://docs.fish.audio/text-to-speech/text-to-speech). You can migrate existing code that calls `https://api.fish.audio/v1/tts` to `https://api.acedata.cloud/fish/tts` by replacing only the authentication credentials — no changes to the request body structure are needed.

## Application Process

To use the API, visit the [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will automatically return to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## Differences from the Official API

This API retains all Fish Audio official request and response fields while making the following additions to support better integration on our platform:

- **Authentication**: Use `Authorization: Bearer {token}`, where `{token}` is the key applied for on this platform — not the Fish official key.
- **TTS model selection**: Specified via the HTTP request header `model`. Options are `s1` or `s2-pro`. Default is `s2-pro`, consistent with Fish official.
- **`latency` default value**: The upstream `/fish/v1/tts` returns an error when `latency` is not provided. This API automatically sets `latency=normal` when omitted, matching Fish's default behavior.
- **Asynchronous callback (platform extension)**: When an extra `callback_url` field is included in the request body, the API immediately returns `{task_id, started_at}`. Once the upstream completes the generation, the full result `{audio_url, ...}` will be posted as JSON to that URL. The Fish official API does not support this field — providing it will only trigger our asynchronous workflow.

All other TTS request body fields (`text`, `reference_id`, `references`, `prosody`, `format`, `sample_rate`, `mp3_bitrate`, `chunk_length`, `temperature`, `top_p`, etc.) are passed directly to upstream and behave exactly as described in the official documentation.

## Basic Usage

The minimum request only requires one field — `text`. Example CURL:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a test of the Fish TTS API."
  }'
```

Response example:

```json
{
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

The response fields match Fish Audio's official fields:

- `audio_url`: The generated audio URL, available for direct download or playback.
- `latency_ms` (optional): Upstream processing time in milliseconds.

To use a cloned voice, add `reference_id` to the request body:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a test of the Fish TTS API.",
    "reference_id": "d7900c21663f485ab63ebdb7e5905036",
    "format": "mp3",
    "sample_rate": 44100
  }'
```

## Asynchronous Callback

Because Fish TTS can take a long time for long texts, maintaining a persistent HTTP connection consumes system resources. This API provides asynchronous callback support (this is an extension relative to the Fish official API).

The flow is: the client includes an extra `callback_url` field in the request body, and the API immediately returns a response containing `task_id`. Once the upstream completes the generation, the final `audio_url` and other fields are sent via POST JSON to `callback_url`, with the same `task_id` included in the body so you can correlate the result with the original request.

Request example:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a test of the Fish TTS API.",
    "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
  }'
```

Immediate response:

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "started_at": "2025-05-09T12:34:56.789Z"
}
```

After a short wait, `callback_url` will receive the full result:

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
}
```

You can also use the [Fish Tasks API](https://platform.acedata.cloud/documents/fc541fac-a941-47fd-b6f7-48d6cb9da523) to poll task status by `task_id`.

## Error Handling

This API preserves Fish Audio's official HTTP status codes, but uses the platform's unified response body format for consistency with `/fish/audios` and `/fish/voices`:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Conclusion

The Fish TTS API is fully compatible with Fish Audio's official OpenAPI, allowing zero-code migration from existing projects while gaining unified authentication, usage metering, and asynchronous callback support. For long text generation, using asynchronous callbacks is recommended to avoid long-lived HTTP connection overhead.
