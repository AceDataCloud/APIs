# Fish Audios Generation API Integration Instructions

This article will introduce the integration instructions for the Fish Audios Generation API, which can clone your own voice by inputting prompt words.

## Application Process

To use Fish Audios Generation API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish Audios Generation API →](https://platform.acedata.cloud/documents/fish-audios)

## Basic Usage

The basic usage involves inputting the prompt word `prompt`, the cloning action `action`, the voice ID `voice_id`, and the model `model` to obtain the processed result.

**Request Headers** include:

- `accept`: the format of the response result you want to receive, set to `application/json`.
- `authorization`: the key to call the API.

**Request Body** includes:

- `model`: the model for cloning the voice, mainly the `fish-tts` model.
- `action`: the action for this voice cloning task (e.g. `speech`).
- `prompt`: the prompt word to be cloned.
- `voice_id`: the voice ID for cloning.
- `callback_url`: the URL for receiving the callback result.

### Code Example

```shell
curl -X POST 'https://api.acedata.cloud/fish/audios' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "speech",
  "prompt": "a white siamese cat",
  "model": "fish-tts",
  "voice_id": "d7900c21663f485ab63ebdb7e5905036"
}'
```

### Response Example

```json
{
  "success": true,
  "task_id": "5872ab00-3cf4-4040-a798-8510aaa16756",
  "trace_id": "5eda3694-448a-4b72-af33-2acb3851ffe1",
  "data": [
    {
      "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
    }
  ]
}
```

The returned result contains multiple fields:

- `success`: the status of the voice cloning task.
- `data`: the result of the voice cloning task.
  - `audio_url`: the audio link result of the voice cloning task.

## Asynchronous Callback

Since the time taken by the Fish Audios Generation API to generate is relatively long, approximately 1–2 minutes, this API also provides support for asynchronous callbacks.

When the client initiates a request with an additional `callback_url` field, the API will immediately return a result containing a `task_id` field. When the task is completed, the result will be sent to the `callback_url` in the form of a POST JSON, which also includes the `task_id` field, allowing the task result to be associated by ID.

```shell
curl -X POST 'https://api.acedata.cloud/fish/audios' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "action": "speech",
  "prompt": "a white siamese cat",
  "model": "fish-tts",
  "voice_id": "d7900c21663f485ab63ebdb7e5905036",
  "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
}'
```

Immediately returns:

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5"
}
```

After a moment, `callback_url` will receive:

```json
{
  "success": true,
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
  "data": [
    {
      "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
    }
  ]
}
```

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

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
