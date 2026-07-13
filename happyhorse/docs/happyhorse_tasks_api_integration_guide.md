# Happy Horse Tasks API Integration Guide

Use the Happy Horse Tasks API to retrieve video generation and editing jobs submitted through
`POST /happyhorse/videos`.

## Endpoint

```text
POST https://api.acedata.cloud/happyhorse/tasks
```

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Retrieve One Task

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/tasks" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "action": "retrieve"
  }'
```

`action` defaults to `retrieve`, but sending it explicitly makes the request unambiguous.

## Single-Task Response

The task record preserves both the original video request and its current or final response:

```json
{
  "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "request": {
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A cinematic shot of a white horse running across a moonlit beach",
    "resolution": "720P",
    "duration": 5
  },
  "type": "videos",
  "response": {
    "success": true,
    "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
    "data": [
      {
        "id": "1469cfc3-3004-4d9e-ab10-xxxxxx",
        "video_url": "https://cdn.acedata.cloud/happyhorse/c8cbf53aa0.mp4",
        "state": "succeeded",
        "duration": 5,
        "resolution": "720P",
        "ratio": "16:9"
      }
    ]
  }
}
```

Important fields:

| Field | Meaning |
|---|---|
| `id` | Ace Data Cloud task ID |
| `request` | Original `/happyhorse/videos` request body |
| `response` | Current or final Videos API response |
| `response.data[].state` | `pending`, `succeeded`, or `error` |
| `response.data[].video_url` | Final CDN URL when successful |
| `response.trace_id` | Trace ID for support and debugging |

If `response` or its final `video_url` is not available yet, wait about 15 seconds and query the
same task again. Stop polling on a final video URL or terminal error.

## Retrieve Multiple Tasks

Set `action` to `retrieve_batch` and pass the IDs array:

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/tasks" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "ids": [
      "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
      "27837f92-d1c1-4db4-ad9a-4e6e81d9f6c1"
    ],
    "action": "retrieve_batch"
  }'
```

The response contains:

```json
{
  "items": [],
  "count": 0
}
```

`items` contains matching task records in the same shape as the single-task response. `count` is
the number of matching records.

## Python Polling Example

```python
import time

import requests

task_id = "YOUR_TASK_ID"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
}

for _ in range(100):
    task = requests.post(
        "https://api.acedata.cloud/happyhorse/tasks",
        headers=headers,
        json={"id": task_id, "action": "retrieve"},
        timeout=30,
    ).json()
    response = task.get("response") or {}
    videos = response.get("data") or []
    if videos and videos[0].get("video_url"):
        print(videos[0]["video_url"])
        break
    if videos and videos[0].get("state") == "error":
        raise RuntimeError(response)
    time.sleep(15)
else:
    raise TimeoutError(f"Task {task_id} did not finish in time")
```

## Errors

| Status | Meaning |
|---|---|
| `400` | Missing IDs or invalid action |
| `401` | Missing or invalid API token |
| `500` | Internal task lookup failure |

Use the same token that submitted the video task.