# Fish Model API Integration Guide

This article introduces the Fish Model API integration guide. The API is fully compatible with the [Fish Audio official OpenAPI](https://docs.fish.audio/resources/api-reference/model) and includes:

- `POST /fish/model`: Create a new cloned voice model (Voice Model) based on audio samples.
- `GET /fish/model`: Paginate and query voice models visible to the current account or across the platform.

## Application Process

To use the API, visit the [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will automatically return to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## Differences from the Official API

- **Authentication**: Use `Authorization: Bearer {token}`, where `{token}` is the key applied for on this platform.
- **Sample upload when creating a model**: This API currently only supports JSON submission, using the `voices` field to pass audio sample URLs. Fish Audio officially supports direct binary upload via multipart/msgpack — that is not yet implemented here. URL-based submission covers approximately 80% of common use cases.
- **Response structure**: Both `POST /fish/model` and `GET /fish/model` directly proxy Fish's upstream response without any platform envelope wrapping. Errors use the platform standard structure `{success: false, error: {code, message}, trace_id}`.

## Create Voice Model (POST /fish/model)

The minimum request requires `title` and `voices`. `voices` is a list of audio sample URLs. Files of 30 seconds or longer, with a sample rate of 16k or higher, are recommended.

```shell
curl -X POST 'https://api.acedata.cloud/fish/model' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "title": "My Cloned Voice",
    "description": "A voice cloned from a podcast recording",
    "voices": [
      "https://example.com/sample-voice.mp3"
    ],
    "cover_image": "https://example.com/cover.png",
    "visibility": "private"
  }'
```

The successful response directly returns Fish platform's ModelEntity object:

```json
{
  "_id": "d7900c21663f485ab63ebdb7e5905036",
  "type": "tts",
  "title": "My Cloned Voice",
  "description": "A voice cloned from a podcast recording",
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

The returned `_id` can be used as the `reference_id` field value in subsequent `POST /fish/tts` requests to synthesize speech using the cloned voice.

## Query Voice Model List (GET /fish/model)

```shell
curl -G 'https://api.acedata.cloud/fish/model' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  --data-urlencode 'page_size=10' \
  --data-urlencode 'page_number=1' \
  --data-urlencode 'self=true'
```

Available query parameters (consistent with Fish Audio official):

- `page_size`: Number of results per page. Default is 10.
- `page_number`: Page number, starting from 1.
- `title`: Fuzzy search by title.
- `tag`: Filter by tag.
- `self`: When set to `true`, returns only voice models created by the current account.
- `author_id`: Filter by creator.
- `language`: Filter by voice language.
- `title_language`: Filter by title language.

The successful response directly proxies Fish platform's paginated structure:

```json
{
  "items": [
    {
      "_id": "d7900c21663f485ab63ebdb7e5905036",
      "title": "My Cloned Voice",
      "description": "A voice cloned from a podcast recording",
      "cover_image": "https://example.com/cover.png",
      "type": "tts",
      "state": "trained",
      "tags": [],
      "languages": ["zh", "en"],
      "visibility": "private",
      "created_at": "2025-05-09T12:34:56.789Z",
      "updated_at": "2025-05-09T12:34:56.789Z"
    }
  ],
  "total": 1
}
```

## Billing

This API only charges for model creation (`POST /fish/model` with a `voices` field in the request body). Querying the voice model list (`GET /fish/model`) is free.

## Error Handling

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

The Fish Model API is fully compatible with Fish Audio's official OpenAPI ModelEntity interface, allowing migration of existing voice clone management code with zero code changes. The voice `_id` created here can be directly passed to the [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d) `reference_id` field for speech synthesis.
