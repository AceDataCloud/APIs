# Fish Model Query API Integration Guide

This document introduces the Fish Model Query API (`GET /fish/model`) integration instructions. This interface is fully compatible with the [Fish Audio Official OpenAPI](https://docs.fish.audio/resources/api-reference/model), and is used for paginated querying of voice models visible to the current account or across the entire platform.

## Application Process

To use Fish Model Query API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish Model API →](https://platform.acedata.cloud/services/fish)

## Differences from the Official API

- **Authentication method**: Uses the standard Authorization header with your Ace Data Cloud API token.
- **Response structure**: Directly passes through Fish upstream's paginated response without platform envelope wrapping; errors use the platform standard error structure.

## Request Example

```shell
curl -G 'https://api.acedata.cloud/fish/model' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  --data-urlencode 'page_size=10' \
  --data-urlencode 'page_number=1' \
  --data-urlencode 'self=true'
```

## Query Parameters

- `page_size`: Number of items per page, default 10.
- `page_number`: Page number, starting from 1.
- `title`: Fuzzy search by title.
- `tag`: Filter by tags.
- `self`: When set to `true`, only returns voices created by the current account.
- `author_id`: Filter by creator.
- `language`: Filter by voice language.
- `title_language`: Filter by title language.
- `sort_by`: Optional sort expression supported by the upstream API.

## Response Example

```json
{
  "total": 424123,
  "items": [
    {
      "_id": "d7900c21663f485ab63ebdb7e5905036",
      "title": "Marcus Aurelius",
      "type": "tts",
      "languages": ["en"],
      "tags": ["historical"],
      "visibility": "public",
      "state": "trained"
    }
  ]
}
```

The returned `_id` can be used as the `reference_id` in the [Fish TTS API](https://platform.acedata.cloud/documents/fish-tts) for speech synthesis.

## Billing Information

This API is free of charge — querying voice models is a free operation.

## Error Handling

- `400 token_mismatched`: Missing or invalid request parameters.
- `400 api_not_implemented`: Unsupported request method or parameters.
- `401 invalid_token`: Missing or invalid authentication information.
- `404 no_api`: API does not exist, please make sure the URL is correct.
- `429 too_many_requests`: Exceeded the rate limit for the current account.
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

The Fish Model Query API provides voice model retrieval capabilities fully compatible with Fish Audio's official API and helps you build selection flows for subsequent TTS requests.
