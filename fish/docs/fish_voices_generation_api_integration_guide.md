# Fish Voices Generation API Integration Guide

The Fish Voices Generation API (`POST /fish/voices`) allows you to create your own voice model by uploading an audio URL. The resulting voice model can be used for speech synthesis with the [Fish TTS API](fish_tts_api_integration_guide.md) or [Fish Audios Generation API](fish_audios_generation_api_integration_guide.md).

## Application

To use the API, visit the [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) page and click the "Acquire" button to obtain your credentials.

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Basic Usage

To create a voice, provide the audio URL of the voice sample you want to clone.

**Request Headers** include:

- `accept`: The format of the response you want to receive, set to `application/json`.
- `authorization`: The API key, selected after application.

**Request Body** includes:

- `voice_url`: The URL of the audio sample to clone.
- `title`: The title for the voice model.
- `image_urls`: (Optional) Cover image URLs for the voice model.
- `description`: (Optional) A description of the voice model.
- `callback_url`: (Optional) A URL to receive the callback result asynchronously.

<p><img src="https://cdn.acedata.cloud/278ikr.png" width="500" class="m-auto"></p>

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/fish/voices' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
  "title": "My Voice Model",
  "description": "A cloned voice model"
}'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/fish/voices"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
    "title": "My Voice Model",
    "description": "A cloned voice model"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "success": true,
  "task_id": "b01db503-dd9e-4f92-861a-344f14756217",
  "trace_id": "8731a2f1-7736-4a47-98e7-da942f9346a7",
  "data": {
    "_id": "d5d21261512b4852b9ccd709facf93f3",
    "type": "tts",
    "title": "My Voice Model",
    "description": "A cloned voice model",
    "cover_image": "coverimage/d5d21261512b4852b9ccd709facf93f3",
    "train_mode": "fast",
    "state": "trained",
    "tags": [],
    "samples": [
      {
        "title": "Default Sample",
        "text": "Sample text for voice demonstration.",
        "task_id": "4ae961828fc94c07b2103dc039a8466b",
        "audio": "task/4ae961828fc94c07b2103dc039a8466b.mp3"
      }
    ],
    "created_at": "2025-09-21T07:29:41.058506Z",
    "updated_at": "2025-09-21T07:29:41.057917Z",
    "languages": ["en"],
    "visibility": "public",
    "lock_visibility": false,
    "like_count": 0,
    "mark_count": 0,
    "shared_count": 0,
    "task_count": 0,
    "author": {
      "_id": "7ecad23df62a4174acd6a2a6cb5201ee",
      "nickname": "Matthew Garcia",
      "avatar": "avatars/7ecad23df62a4174acd6a2a6cb5201ee.jpg"
    }
  }
}
```

Response fields:

- `success`: Status of the voice creation task.
- `data`: The result of the voice creation task.
  - `_id`: The voice model ID. Use this as the `voice_id` in the Fish Audios API, or as `reference_id` in the Fish TTS API.
  - `title`: The voice model title.
  - `description`: The voice model description.
  - `train_mode`: The training mode used for this voice model.
  - `state`: The training state of the voice model.
  - `tags`: Style tags for the voice model.

## Async Callback

Because Fish Voices Generation can take 1–2 minutes, this API also supports async callbacks to avoid holding long HTTP connections.

The flow is: include an additional `callback_url` in the request body. The API immediately returns a `task_id`. When the task finishes, the result is sent via POST JSON to the specified `callback_url`, also including the `task_id` for correlation.

### Webhook Setup

For demonstration, use a public webhook service like [https://webhook.site/](https://webhook.site/) to get a temporary webhook URL:

![](https://cdn.acedata.cloud/tbcnai.png)

### Async Request Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/voices' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "voice_url": "https://platform.r2.fish.audio/task/604133d7b3c7430385382470f67770e8.mp3",
  "title": "My Voice Model",
  "description": "A cloned voice model",
  "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
}'
```

### Immediate Response

```json
{
  "task_id": "9f626a13-96ec-4dec-8846-dc5aab7362a8"
}
```

### Callback Payload (sent to `callback_url`)

```json
{
  "success": true,
  "task_id": "9f626a13-96ec-4dec-8846-dc5aab7362a8",
  "trace_id": "3fcdea82-7c1c-4a0a-b8d8-f7616f722d8f",
  "data": {
    "_id": "fa75e7c3f02f42e79a6aa622b6cf075e",
    "type": "tts",
    "title": "My Voice Model",
    "description": "A cloned voice model",
    "cover_image": "coverimage/fa75e7c3f02f42e79a6aa622b6cf075e",
    "train_mode": "fast",
    "state": "trained",
    "tags": [],
    "samples": [],
    "created_at": "2025-09-21T07:36:20.200865Z",
    "updated_at": "2025-09-21T07:36:20.200353Z",
    "languages": ["en"],
    "visibility": "public",
    "like_count": 0,
    "mark_count": 0,
    "shared_count": 0,
    "task_count": 0,
    "author": {
      "_id": "7ecad23df62a4174acd6a2a6cb5201ee",
      "nickname": "Matthew Garcia",
      "avatar": "avatars/7ecad23df62a4174acd6a2a6cb5201ee.jpg"
    }
  }
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

Through this guide, you have learned how to use the Fish Voices Generation API to create a custom voice model from an audio URL. The `_id` returned in `data` can be used directly as the `voice_id` in the [Fish Audios Generation API](fish_audios_generation_api_integration_guide.md) or as `reference_id` in the [Fish TTS API](fish_tts_api_integration_guide.md). If you have any questions, please contact our technical support team.
