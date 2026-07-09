# Seedream Tasks API Integration and Usage

The Seedream Tasks API queries the execution status and results of tasks created by the Seedream Images Generation API, supporting both single and batch task queries.

## Application Process

Open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token. **A single API Token works across every service on the platform.**

## Single Task Query

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "id": "a6e0d456-189b-4c78-9232-2fe72166ab39",
    "action": "retrieve"
  }'
```

### Response Example

```json
{
  "success": true,
  "task_id": "84d1544a-9043-4dde-a98b-e889dacd75f6",
  "trace_id": "176acf03-7ca7-4fc6-85db-e3724d4f59eb",
  "data": [
    {
      "prompt": "a white siamese cat",
      "size": "2048x2048",
      "image_url": "https://platform.cdn.acedata.cloud/seedream/6e5f9085-cc4a-4801-b77b-31550129ff19.jpg"
    }
  ]
}
```

The `data` array contains the task results. Each item includes:
- `image_url`: link to the generated image.
- `prompt`: the prompt text.
- `size`: pixel dimensions of the generated image.

## Batch Query

Query multiple tasks in a single request using `action: retrieve_batch` and an `ids` array.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "ids": ["84d1544a-9043-4dde-a98b-e889dacd75f6", "c9aaffa2-b8ac-40ff-8468-43e77cb9ddde"],
    "action": "retrieve_batch"
  }'
```

### Response Example

```json
{
  "items": [
    {
      "id": "84d1544a-9043-4dde-a98b-e889dacd75f6",
      "trace_id": "176acf03-7ca7-4fc6-85db-e3724d4f59eb",
      "request": {
        "action": "generate",
        "model": "doubao-seedream-4-0-250828",
        "prompt": "a white siamese cat"
      },
      "response": {
        "success": true,
        "task_id": "84d1544a-9043-4dde-a98b-e889dacd75f6",
        "trace_id": "176acf03-7ca7-4fc6-85db-e3724d4f59eb",
        "data": [
          {
            "prompt": "a white siamese cat",
            "size": "2048x2048",
            "image_url": "https://platform.cdn.acedata.cloud/seedream/6e5f9085-cc4a-4801-b77b-31550129ff19.jpg"
          }
        ]
      }
    }
  ],
  "count": 1
}
```

The response includes:
- `items`: array of task detail objects.
- `count`: number of tasks returned.

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | token_mismatched | Token does not match the API |
| 400 | api_not_implemented | API not implemented |
| 400 | bad_request | Missing or invalid parameters |
| 401 | invalid_token | Token invalid or missing |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | api_error | Internal server error |
