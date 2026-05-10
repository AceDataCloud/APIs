# Fish Model Get API Integration Guide

The Fish Model Get API (`GET /fish/model/{id}`) is fully compatible with the [Fish Audio official Model API](https://docs.fish.audio/resources/api-reference/model). It allows you to **retrieve the complete details of a single cloned voice model by its ID**.

> To create a voice model, see the [Fish Model Create API](fish_model_create_api_integration_guide.md). To paginate through voice model lists, see the [Fish Model Query API](fish_model_query_api_integration_guide.md).

## Application

To use the API, visit the [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button to obtain your credentials.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Differences from the Official API

- **Authentication**: Uses `Authorization: Bearer {token}` where `{token}` is the key obtained on this platform.
- **Response structure**: Passes through the Fish upstream ModelEntity object directly without platform envelope wrapping. Errors use the platform standard structure `{success: false, error: {code, message}, trace_id}`.
- **Path parameter**: `{id}` is the voice model's `_id`, obtainable from the [Fish Model Create API](fish_model_create_api_integration_guide.md) at creation time or from the [Fish Model Query API](fish_model_query_api_integration_guide.md) via paginated listing.

## Request Example

Replace `{id}` in the URL path with the specific voice model ID. No query parameters or request body are required.

```bash
curl 'https://api.acedata.cloud/fish/model/d7900c21663f485ab63ebdb7e5905036' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}'
```

### Python Example

```python
import requests

model_id = "d7900c21663f485ab63ebdb7e5905036"
url = f"https://api.acedata.cloud/fish/model/{model_id}"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}"
}

response = requests.get(url, headers=headers)
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
  "samples": [
    {
      "audio": "https://example.com/sample-voice.mp3",
      "text": ""
    }
  ],
  "created_at": "2025-05-09T12:34:56.789Z",
  "updated_at": "2025-05-09T12:34:56.789Z",
  "languages": ["zh", "en"],
  "visibility": "private",
  "lock_visibility": false,
  "default_text": "",
  "default_mode": "fast",
  "like_count": 0,
  "mark_count": 0,
  "shared_count": 0,
  "task_count": 0,
  "unliked": false,
  "liked": false,
  "marked": false,
  "author": {
    "_id": "00000000000000000000000000000000",
    "nickname": "",
    "avatar": ""
  }
}
```

The returned `_id` can be used as the `reference_id` value in subsequent [Fish TTS API](fish_tts_api_integration_guide.md) requests to synthesize speech using this cloned voice.

## Billing

This API is free — retrieving voice model details by ID does not incur charges. Only `POST /fish/model` with a `voices` field in the request body (creating a new voice) is billed.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `404 not_found`: The specified `_id` does not exist or is not visible to the current account.
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

The Fish Model Get API provides fully compatible single voice detail retrieval capability with Fish Audio official. After obtaining a voice model ID, you can use this API to retrieve the complete ModelEntity object (including samples, state, visibility, and statistics fields), and then use the [Fish TTS API](fish_tts_api_integration_guide.md) to complete an end-to-end clone + synthesis workflow.
