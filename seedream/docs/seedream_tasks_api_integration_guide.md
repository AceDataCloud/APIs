# Seedream Tasks API Integration and Usage

The Seedream Tasks API queries the execution status of an async task created by the Seedream Images Generation API.

## Application Process

Apply on the [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75) page; copy a task ID returned by the [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) (submit with `"async": true`).

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{ "action": "retrieve", "id": "ec22ae22-0140-4033-8c86-a48b536da595" }'
```

Request body fields:

- `id`: task ID to retrieve.
- `ids`: array of task IDs for batch retrieval.
- `action`: `retrieve` (default) for one task, or `retrieve_batch` for multiple tasks.

## Response Example

A single-task query returns a task record with the original request and response payloads:

```json
{
  "id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "type": "images",
  "created_at": 1766427547.107,
  "started_at": 1766427547.167,
  "finished_at": 1766427560.667,
  "elapsed": 13.5,
  "trace_id": "176acf03-7ca7-4fc6-85db-e3724d4f59eb",
  "request": {
    "model": "doubao-seedream-5-0-260128",
    "prompt": "a white siamese cat"
  },
  "response": {
    "success": true,
    "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
    "data": [
      {
        "prompt": "a white siamese cat",
        "size": "2048x2048",
        "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png"
      }
    ]
  }
}
```

For batch queries, send `{ "action": "retrieve_batch", "ids": ["task-id-1", "task-id-2"] }`; the response is `{ "items": [...], "count": 2 }`. Poll until the nested `response.data` contains the final image result, then download each `image_url`.

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | token_mismatched / api_not_implemented | Missing or invalid parameters |
| 401 | invalid_token | Token bad |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | api_error | Server error |
