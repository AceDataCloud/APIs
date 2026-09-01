# Fish Tasks API Integration and Usage

The main function of the Fish Tasks API is to query the execution status of tasks by inputting the task ID returned by the Fish TTS API.

This document describes the Fish Tasks API integration, helping you query the status and final result of an asynchronous Fish voice generation task.

## Application Process

To use the Fish Tasks API, you first need to apply for the corresponding service on the application page [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d), and then copy the task ID returned by the Fish TTS API.

Finally, go to the Tasks API page [Fish Tasks API](https://platform.acedata.cloud/documents/fc541fac-a941-47fd-b6f7-48d6cb9da523) to apply for the corresponding service. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Example

The Fish Tasks API queries the result of a task created by the Fish TTS API. Create the task with `"async": true` (or a `callback_url`), then poll with the returned `id`.

### Request Body

- `id`: a single task ID returned by the Fish TTS API.
- `ids`: optional array to query multiple tasks at once.
- `action`: `retrieve` (the default) for one task or `retrieve_batch` for multiple tasks.

### Code Example

```bash
curl -X POST 'https://api.acedata.cloud/fish/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978",
    "action": "retrieve"
  }'
```

```python
import requests

url = "https://api.acedata.cloud/fish/tasks"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {"id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978", "action": "retrieve"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

```json
{
  "id": "8a72ff98-4023-4006-a9f7-4cb2fa04f978",
  "type": "audios",
  "created_at": 1758440856.34,
  "started_at": 1758440856.4,
  "finished_at": 1758440869.2,
  "elapsed": 12.8,
  "trace_id": "e2d308bc-4df8-4c69-9369-a60f3c54f2b3",
  "request": {"text": "Hello"},
  "response": {"audio_url": "https://platform2.cdn.acedata.cloud/fish/8a72ff98-4023-4006-a9f7-4cb2fa04f978.mp3"}
}
```

Task records always include `id`, `type`, `created_at`, `trace_id`, and `request`. `response`, `started_at`, `finished_at`, and `elapsed` are returned when available; the latter two are `null` until completion.

For a batch lookup, submit `{"ids": ["task-1", "task-2"], "action": "retrieve_batch"}`. The response is `{"items": [<task records>], "count": 2}`.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
