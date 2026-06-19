# Fish Model Get API Integration Guide

This document introduces the integration guide for the Fish Model Get API (`GET /fish/model/{id}`). This endpoint is fully compatible with the [Fish Audio official OpenAPI](https://docs.fish.audio/resources/api-reference/model) and is used to query the complete details of a single voice model by ID.

## Application Process

To use Fish Model Get API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish Model API →](https://platform.acedata.cloud/services/fish)

## Differences from the Official API

- **Authentication method**: Uses the standard Authorization header with your Ace Data Cloud API token.
- **Response structure**: Directly passes through the voice model entity from Fish upstream without platform envelope wrapping; errors use the platform standard error structure.
- **Path parameter**: `{id}` is the voice model `_id`, which can be obtained from the [Fish Model Query API](https://platform.acedata.cloud/documents/fish-model-query).

## Request Example

```shell
curl 'https://api.acedata.cloud/fish/model/d7900c21663f485ab63ebdb7e5905036' \
  -H 'accept: application/json' \
  -H 'authorization: ******'
```

Simply replace `{id}` in the URL path with the specific voice model ID. No query parameters or request body are required.

## Response Example

```json
{
  "_id": "d7900c21663f485ab63ebdb7e5905036",
  "type": "tts",
  "title": "Marcus Aurelius",
  "description": "Fish Model Id Response 200 Example",
  "cover_image": "https://api.fish.audio/v1/file/voice-cover.jpg",
  "train_mode": "fast",
  "state": "trained",
  "tags": ["historical"],
  "samples": [
    {
      "title": "sample 1",
      "text": "Hello, this is a sample.",
      "task_id": "ad1c50e6f1a4474d96a17a91da93dac2",
      "audio": "https://api.fish.audio/v1/file/sample-1.mp3"
    }
  ],
  "created_at": "2024-09-01T07:53:39.476000Z",
  "updated_at": "2024-09-01T07:53:39.476000Z",
  "languages": ["en"],
  "visibility": "public",
  "lock_visibility": false,
  "like_count": 12,
  "mark_count": 3,
  "shared_count": 0,
  "task_count": 5,
  "unliked": false,
  "liked": false,
  "marked": false,
  "author": {
    "_id": "8e0b7add9a474db4b46abe51ef64b3c0",
    "nickname": "AceDataCloud"
  }
}
```

The returned `_id` can be used as the value of the `reference_id` field in the [Fish TTS API](https://platform.acedata.cloud/documents/fish-tts) to perform speech synthesis with this voice model.

## Billing Information

This endpoint is free of charge — querying voice model details by ID is a free operation.

## Error Handling

- `400 token_mismatched`: Missing or invalid request parameters.
- `400 api_not_implemented`: Unsupported request method or parameters.
- `401 invalid_token`: Missing or invalid authentication information.
- `404 no_api`: API does not exist, please make sure the URL is correct.
- `429 too_many_requests`: Rate limit exceeded for the current account.
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

The Fish Model Get API lets you fetch the complete voice model object for a known `_id`, including metadata, sample clips, and visibility information needed before synthesis.
