# Fish Model Query API Integration Guide

The Fish Model Query API (`GET /fish/model`) is fully compatible with the [Fish Audio official Model API](https://docs.fish.audio/resources/api-reference/model). It allows you to **paginate through** cloned voice models visible to your account or the entire platform.

> To create a voice model, see the [Fish Model Create API](fish_model_create_api_integration_guide.md). To retrieve a specific voice model by `_id`, see the [Fish Model Get API](fish_model_get_api_integration_guide.md).

## Application

To use the API, visit the [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button to obtain your credentials.

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will be returned to the current page.

First-time applicants receive a free quota to try the API at no charge.

## Differences from the Official API

- **Authentication**: Uses `Authorization: Bearer {token}` where `{token}` is the key obtained on this platform.
- **Response structure**: Passes through the Fish upstream paginated response directly without platform envelope wrapping. Errors use the platform standard structure `{success: false, error: {code, message}, trace_id}`.

## Request Example

```bash
curl -G 'https://api.acedata.cloud/fish/model' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  --data-urlencode 'page_size=10' \
  --data-urlencode 'page_number=1' \
  --data-urlencode 'self=true'
```

### Python Example

```python
import requests

url = "https://api.acedata.cloud/fish/model"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}"
}

params = {
    "page_size": 10,
    "page_number": 1,
    "self": "true"
}

response = requests.get(url, headers=headers, params=params)
print(response.text)
```

## Query Parameters

Consistent with Fish Audio official parameters:

- `page_size`: Number of results per page, default 10.
- `page_number`: Page number, starting from 1.
- `title`: Fuzzy search by title.
- `tag`: Filter by tag.
- `self`: Pass `true` to return only voice models created by the current account.
- `author_id`: Filter by creator.
- `language`: Filter by voice language.
- `title_language`: Filter by title language.

## Response Example

The successful response passes through Fish Audio's paginated structure directly:

```json
{
  "items": [
    {
      "_id": "d7900c21663f485ab63ebdb7e5905036",
      "title": "My Cloned Voice",
      "description": "A voice model cloned from a podcast recording",
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

The `_id` from any item in the result can be used as the `reference_id` value in subsequent [Fish TTS API](fish_tts_api_integration_guide.md) requests for speech synthesis using that cloned voice.

## Billing

This API is free — paginated voice model listing does not incur charges. Only `POST /fish/model` with a `voices` field in the request body (creating a new voice) is billed.

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

The Fish Model Query API provides fully compatible voice search capability with Fish Audio official, allowing you to maintain your own cloned voice library on this platform. Combined with the [Fish Model Get API](fish_model_get_api_integration_guide.md), you can retrieve the complete details of a single voice by its ID.
