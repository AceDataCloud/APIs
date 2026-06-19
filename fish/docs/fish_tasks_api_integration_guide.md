# Fish Tasks API Integration Guide

The main function of the Fish Tasks API is to query the execution status of asynchronous Fish tasks by using a task ID returned from the Fish TTS API.

This document provides integration instructions for the Fish Tasks API, helping you retrieve the status or final result of single or batch Fish tasks.

## Application Process

To use Fish Tasks API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [Fish Tasks API →](https://platform.acedata.cloud/documents/fish-tasks)

## Request Example

The Fish Tasks API can be used to query the results of asynchronous requests submitted to the [Fish TTS API](https://platform.acedata.cloud/documents/fish-tts).

To query a single task, submit the task ID with `action` set to `retrieve`.

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "action": "retrieve"
}'
```

### Response Example

```json
{
  "_id": "68cfad98550a4144a5476a92",
  "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "api_id": "8e6f8083-4683-45fe-a993-3e1d993fc999",
  "application_id": "3559d836-2505-46be-96ea-ea72bcb7c080",
  "created_at": 1758440856.34,
  "credential_id": "881ad87d-8ba7-40b7-ac45-d19e41ae6e3a",
  "request": {
    "text": "Hello, this is a Fish-Audio-compatible test.",
    "reference_id": "d7900c21663f485ab63ebdb7e5905036",
    "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
  },
  "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
  "type": "audios",
  "user_id": "ad7afe47-cea9-4cda-980f-2ad8810e51cf",
  "response": {
    "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
  }
}
```

The returned result contains multiple fields:

- `id`: The task ID used to uniquely identify this synthesis task.
- `request`: The original request information submitted when the task was created.
- `response`: The final response body returned after the task completes.

## Batch Query Operation

To query multiple tasks at once, submit an `ids` array and set `action` to `retrieve_batch`.

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "ids": ["2725a2d3-f87e-4905-9c53-9988d5a7b2f5", "2725a2d3-f87e-4905-9c53-9988d5a7b2f6"],
  "action": "retrieve_batch"
}'
```

Example batch response:

```json
{
  "items": [
    {
      "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
      "request": {
        "text": "Hello, this is a Fish-Audio-compatible test."
      },
      "response": {
        "audio_url": "https://platform.r2.fish.audio/task/b627c2f7d38a4083a837570ba6d0962f.mp3"
      }
    },
    {
      "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f6",
      "request": {
        "text": "Another synthesis request."
      },
      "response": {
        "audio_url": "https://platform.r2.fish.audio/task/c627c2f7d38a4083a837570ba6d0962f.mp3"
      }
    }
  ],
  "count": 2
}
```

## Error Handling

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, rate limit exceeded.
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

Through the Fish Tasks API, you can query the status and result payloads for asynchronous Fish synthesis jobs without keeping long-lived HTTP connections open.
