# Fish TTS API Integration Guide

The Fish TTS API (`POST /fish/tts`) is fully compatible with the [Fish Audio official TTS OpenAPI](https://docs.fish.audio/text-to-speech/text-to-speech). You can migrate existing code that calls `https://api.fish.audio/v1/tts` to `https://api.acedata.cloud/fish/tts` by replacing only the authentication credentials — the request body structure remains identical.

## Application

To use the API, visit the [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button to obtain your credentials.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Differences from the Official API

This API retains all Fish Audio official request and response fields, with the following minor additions to improve platform integration:

- **Authentication**: Uses `Authorization: Bearer {token}` where `{token}` is the key obtained on this platform, not a Fish Audio official key.
- **TTS model selection**: Specified via the HTTP request header `model`. Accepted values are `s1` or `s2-pro`; the default is `s2-pro`, consistent with Fish Audio.
- **`latency` default value**: The upstream `/fish/v1/tts` returns an error when `latency` is not provided. This API automatically sets `latency=normal` when the field is omitted, matching Fish Audio's default behavior.
- **Async callback (platform extension)**: When an additional `callback_url` field is included in the request body, the API immediately returns `{task_id, started_at}`. Once the upstream finishes generating, the complete result (including `audio_url`) is sent via POST JSON to the specified `callback_url`. The Fish Audio official API does not support this field; passing it triggers only this platform's async flow.

All other TTS request body fields (`text`, `reference_id`, `references`, `prosody`, `format`, `sample_rate`, `mp3_bitrate`, `chunk_length`, `temperature`, `top_p`, etc.) are passed through directly to the upstream with behavior identical to the official documentation.

## Basic Usage

A minimal request requires only the `text` field:

```bash
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, how are you today?"
  }'
```

### Response Example

```json
{
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

The response fields are:

- `audio_url`: The URL of the generated audio, available for direct download or playback.
- `latency_ms` (optional): Upstream processing time in milliseconds.

### Using a Cloned Voice

To use a cloned voice, add `reference_id` to the request body:

```bash
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, how are you today?",
    "reference_id": "d7900c21663f485ab63ebdb7e5905036",
    "format": "mp3",
    "sample_rate": 44100
  }'
```

The `reference_id` value is the `_id` returned when creating a voice model via the [Fish Model Create API](fish_model_create_api_integration_guide.md) or retrieved via the [Fish Model Query API](fish_model_query_api_integration_guide.md).

## Async Callback

For long text, TTS generation may take significant time. Keeping an open HTTP connection wastes system resources. This API provides async callback support (an extension relative to the Fish Audio official API).

The flow is: include an additional `callback_url` in the request body. The API immediately returns a response containing `task_id`. Once the upstream finishes generating, the final `audio_url` and other fields are sent via POST JSON to the `callback_url`, with the same `task_id` included so you can correlate the async result with the original request.

### Async Request Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, how are you today?",
    "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
  }'
```

### Immediate Response

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "started_at": "2025-05-09T12:34:56.789Z"
}
```

### Callback Payload (sent to `callback_url`)

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
}
```

You can also use the [Fish Tasks API](fish_tasks_api_integration_guide.md) to poll the task status by `task_id`.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

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

The Fish TTS API is fully compatible with the Fish Audio official OpenAPI, allowing you to migrate existing projects with zero code changes while benefiting from the platform's unified authentication, usage accounting, and async callback capabilities. For long text generation, the async callback is recommended to avoid holding open HTTP connections.
