# Fish Audios Generation API Integration Guide

The Fish Audios Generation API (`POST /fish/audios`) allows you to clone a voice by providing a prompt and a voice ID, producing an audio output in the cloned voice.

## Application

To use the API, visit the [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) page and click the "Acquire" button to obtain your credentials.

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Basic Usage

To generate audio, provide a prompt, action, voice ID, and model. Set the `action` field to `speech`, and specify the `model` (currently `fish-tts` is the primary model).

**Request Headers** include:

- `accept`: The format of the response you want to receive, set to `application/json`.
- `authorization`: The API key, selected after application.

**Request Body** includes:

- `model`: The voice cloning model. Primary option: `fish-tts`.
- `action`: The action for this voice cloning task (e.g., `speech`).
- `prompt`: The text prompt to be converted to speech in the cloned voice.
- `voice_id`: The voice model ID to use for cloning.
- `callback_url`: (Optional) A URL to receive the callback result asynchronously.

<p><img src="https://cdn.acedata.cloud/0jnfqb.png" width="500" class="m-auto"></p>

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/fish/audios' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "speech",
  "prompt": "Hello, how are you today?",
  "model": "fish-tts",
  "voice_id": "d7900c21663f485ab63ebdb7e5905036"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/fish/audios"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "action": "speech",
    "prompt": "Hello, how are you today?",
    "model": "fish-tts",
    "voice_id": "d7900c21663f485ab63ebdb7e5905036"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
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

Response fields:

- `success`: Status of the voice cloning task.
- `data`: The result of the voice cloning task.
  - `audio_url`: The URL of the generated cloned-voice audio.

## Async Callback

Because Fish Audios Generation can take 1–2 minutes, this API also supports async callbacks to avoid holding long HTTP connections.

The flow is: include an additional `callback_url` in the request body. The API immediately returns a `task_id`. When the task finishes, the result is sent via POST JSON to the specified `callback_url`, also including the `task_id` for correlation.

### Webhook Setup

For demonstration, use a public webhook service like [https://webhook.site/](https://webhook.site/) to get a temporary webhook URL:

![](https://cdn.acedata.cloud/tbcnai.png)

### Async Request Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/audios' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "action": "speech",
  "prompt": "Hello, how are you today?",
  "model": "fish-tts",
  "voice_id": "d7900c21663f485ab63ebdb7e5905036",
  "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
}'
```

### Immediate Response

```json
{
  "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5"
}
```

### Callback Payload (sent to `callback_url`)

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

The `task_id` field in the callback payload matches the one returned in the immediate response, allowing you to correlate the result with the original request.

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

Through this guide, you have learned how to use the Fish Audios Generation API to clone a voice using a text prompt. If you have any questions, please contact our technical support team.
