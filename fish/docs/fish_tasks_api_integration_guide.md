# Fish Tasks API Integration and Usage

The Fish Tasks API lets you query async Fish TTS jobs after the original request returns a `task_id`.
Use it to retrieve a single task by `id` or `trace_id`, or to fetch multiple tasks in one batch request.

## Application Process

To use the Fish Tasks API, first get your API token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).
Use the same token for both the Fish TTS API and the Fish Tasks API.

## Endpoint

```text
POST https://api.acedata.cloud/fish/tasks
```

## Request Headers

- `accept: application/json`
- `authorization: ******`
- `content-type: application/json`

## Query a Single Task

Use `action: "retrieve"` with either `id` or `trace_id`:

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks'   -H 'accept: application/json'   -H 'authorization: ******'   -H 'content-type: application/json'   -d '{
    "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
    "action": "retrieve"
  }'
```

```python
import requests

url = "https://api.acedata.cloud/fish/tasks"
headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json",
}
payload = {
    "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
    "action": "retrieve",
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

```json
{
  "_id": "68cfad98550a4144a5476a92",
  "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
  "api_id": "8e6f8083-4683-45fe-a993-3e1d993fc999",
  "application_id": "3559d836-2505-46be-96ea-ea72bcb7c080",
  "created_at": 1758440856.34,
  "started_at": "2026-05-11T01:23:04.742Z",
  "finished_at": 1758440872.118,
  "elapsed": 15.778,
  "credential_id": "881ad87d-8ba7-40b7-ac45-d19e41ae6e3a",
  "request": {
    "text": "Today is a beautiful day. Let's go for a walk.",
    "format": "mp3",
    "callback_url": "https://webhook.site/4815f79f-a40f-4078-ac85-1cc126b6bb34"
  },
  "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
  "type": "audios",
  "user_id": "ad7afe47-cea9-4cda-980f-2ad8810e51cf",
  "response": {
    "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
    "audio_url": "https://platform2.cdn.acedata.cloud/fish/bd66b8c5-7543-4557-b684-baa72407e336.mp3"
  }
}
```

Returned task records include the following fields:

- `id`: the generated task ID, used to uniquely identify the synthesis task.
- `request`: the original request body submitted to the Fish TTS API.
- `response`: the final callback payload returned by the task.
- `created_at`: the task creation time as a Unix timestamp in seconds.
- `started_at`: the task start time as an ISO-8601 UTC timestamp.
- `finished_at`: the task completion time as a Unix timestamp in seconds. This field is absent until the task finishes.
- `elapsed`: the task runtime in seconds. This field is absent until the task finishes.

## Batch Query Operation

To query multiple task IDs at once, set `action` to `retrieve_batch` and provide an `ids` array:

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks'   -H 'accept: application/json'   -H 'authorization: ******'   -H 'content-type: application/json'   -d '{
    "ids": ["2725a2d3-f87e-4905-9c53-9988d5a7b2f5"],
    "action": "retrieve_batch"
  }'
```

```json
{
  "items": [
    {
      "id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
      "created_at": 1758440856.34,
      "started_at": "2026-05-11T01:23:04.742Z",
      "finished_at": 1758440872.118,
      "elapsed": 15.778,
      "request": {
        "text": "Today is a beautiful day. Let's go for a walk.",
        "format": "mp3"
      },
      "response": {
        "task_id": "2725a2d3-f87e-4905-9c53-9988d5a7b2f5",
        "audio_url": "https://platform2.cdn.acedata.cloud/fish/bd66b8c5-7543-4557-b684-baa72407e336.mp3"
      }
    }
  ],
  "count": 1
}
```

## Error Handling

- `400 token_mismatched`: missing or invalid parameters.
- `400 api_not_implemented`: unsupported request shape.
- `401 invalid_token`: invalid or missing authorization token.
- `429 too_many_requests`: rate limit exceeded.
- `500 api_error`: internal server error.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
