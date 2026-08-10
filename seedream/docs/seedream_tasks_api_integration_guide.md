# Seedream Tasks API Integration and Usage

The Seedream Tasks API queries the execution status of an async task created by the Seedream Images Generation API.

## Application Process

Get an API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications); use a task ID returned by the [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) (submit with `"async": true`).

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{ "id": "ec22ae22-0140-4033-8c86-a48b536da595", "action": "retrieve" }'
```

## Response Example

```json
{
  "id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "type": "images",
  "created_at": 1766427547.107,
  "started_at": 1766427547.167,
  "finished_at": 1766427560.667,
  "elapsed": 13.5,
  "request": { "model": "doubao-seedream-5-0-260128", "prompt": "a white siamese cat" },
  "response": { "success": true, "data": [{ "image_url": "https://platform.cdn.acedata.cloud/seedream/xxxx.png" }] }
}
```

The task record contains request and final response data. `finished_at` and `elapsed` are absent until processing completes.

## Batch Retrieval

Use `action: "retrieve_batch"` with an `ids` array to retrieve multiple task records:

```bash
curl -X POST 'https://api.acedata.cloud/seedream/tasks' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{ "ids": ["ec22ae22-0140-4033-8c86-a48b536da595"], "action": "retrieve_batch" }'
```

The response contains `items` (task records) and `count` (the number returned).

## Error Codes

| HTTP | Code | Meaning |
| ---- | ---- | ---- |
| 400 | bad_request | Missing/invalid task id |
| 401 | invalid_token | Token bad |
| 429 | too_many_requests | Rate limit exceeded |
| 500 | api_error | Upstream error |
