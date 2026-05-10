# Fish Model Create API Integration Guide

The Fish Model Create API (`POST /fish/model`) is fully compatible with the [Fish Audio official Model API](https://docs.fish.audio/resources/api-reference/model). It allows you to create a new cloned voice model (Voice Model) based on audio samples.

> To list voice models, see the [Fish Model Query API](fish_model_query_api_integration_guide.md). To retrieve a specific voice model by ID, see the [Fish Model Get API](fish_model_get_api_integration_guide.md).

## Application

To use the API, visit the [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button to obtain your credentials.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Differences from the Official API

- **Authentication**: Uses `Authorization: Bearer {token}` where `{token}` is the key obtained on this platform.
- **Sample upload format**: This API currently only supports JSON format submissions, with audio sample URLs passed in the `voices` field. Fish Audio officially supports multipart/msgpack binary uploads; URL-based submission covers approximately 80% of common use cases.
- **Response structure**: `POST /fish/model` passes through the Fish upstream response directly without platform envelope wrapping. Errors use the platform standard structure `{success: false, error: {code, message}, trace_id}`.

## Request Example

A minimal create request requires the `title` and `voices` fields. `voices` is a list of audio sample URLs; files of 30 seconds or longer and 16 kHz or higher sample rate are recommended.

```bash
curl -X POST 'https://api.acedata.cloud/fish/model' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "title": "My Cloned Voice",
    "description": "A voice model cloned from a podcast recording",
    "voices": [
      "https://example.com/sample-voice.mp3"
    ],
    "cover_image": "https://example.com/cover.png",
    "visibility": "private"
  }'
```

### Python Example

```python
import requests

url = "https://api.acedata.cloud/fish/model"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "title": "My Cloned Voice",
    "description": "A voice model cloned from a podcast recording",
    "voices": [
        "https://example.com/sample-voice.mp3"
    ],
    "visibility": "private"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Response Example

The successful response passes through Fish Audio's ModelEntity object directly:

```json
{
  "_id": "d7900c21663f485ab63ebdb7e5905036",
  "type": "tts",
  "title": "My Cloned Voice",
  "description": "A voice model cloned from a podcast recording",
  "cover_image": "https://example.com/cover.png",
  "train_mode": "fast",
  "state": "trained",
  "tags": [],
  "samples": [],
  "created_at": "2025-05-09T12:34:56.789Z",
  "updated_at": "2025-05-09T12:34:56.789Z",
  "languages": ["zh", "en"],
  "visibility": "private",
  "lock_visibility": false,
  "like_count": 0,
  "mark_count": 0,
  "shared_count": 0,
  "task_count": 0,
  "author": {
    "_id": "user_id",
    "nickname": "user_nickname",
    "avatar": "user_avatar"
  }
}
```

The returned `_id` can be used as the `reference_id` value in subsequent `POST /fish/tts` requests to synthesize speech using this cloned voice.

## Billing

This API charges only when creating a voice model (`POST /fish/model` with a `voices` field in the request body). Querying voice models (`GET /fish/model`) is free.

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

The Fish Model Create API is fully compatible with the Fish Audio official ModelEntity interface, allowing you to migrate existing voice cloning management code with zero code changes. The created voice `_id` can be passed directly to the [Fish TTS API](fish_tts_api_integration_guide.md) as the `reference_id` field for speech synthesis.
