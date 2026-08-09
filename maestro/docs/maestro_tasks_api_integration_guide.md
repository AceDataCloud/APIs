# Maestro Tasks API Integration Guide

`POST https://api.acedata.cloud/maestro/tasks`

The Maestro Tasks API retrieves one video job. Polling is free.

## Authentication

Use the same Ace Data Cloud Bearer token that created the video:

```http
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json
Accept: application/json
```

## Retrieve One Task

Request body:

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | yes | `task_id` returned by `POST /maestro/videos` |
| `action` | string | no | `retrieve`; this is the default when omitted |

```bash
curl --request POST 'https://api.acedata.cloud/maestro/tasks' \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{
    "id": "f57e99c4-f60f-4373-a155-17742ce2357d",
    "action": "retrieve"
  }'
```

Python example:

```python
import os

import requests

response = requests.post(
    "https://api.acedata.cloud/maestro/tasks",
    headers={
        "Authorization": "******",
        "Content-Type": "application/json",
    },
    json={
        "id": "f57e99c4-f60f-4373-a155-17742ce2357d",
        "action": "retrieve",
    },
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

## Task Shape

The following is an illustrative shape. URLs and optional fields vary with the delivered production:

```json
{
  "id": "f57e99c4-f60f-4373-a155-17742ce2357d",
  "trace_id": "70e1cb12-c619-4292-a416-90191205996b",
  "status": "succeeded",
  "progress": {
    "percent": 100,
    "stage": "rendering",
    "message": "Rendering scene 2",
    "activity": null,
    "render": null
  },
  "created_at": 1750000000,
  "elapsed": 312,
  "request": {
    "prompt": "Create a beginner-friendly vector database video.",
    "langs": ["en"],
    "aspect": "16:9",
    "duration": 30
  },
  "response": {
    "success": true,
    "data": {
      "variants": [
        {
          "lang": "en",
          "aspect": "16:9",
          "kind": "video",
          "title": "What is a vector database?",
          "output_url": "https://cdn.example/video.mp4"
        }
      ],
      "project": {
        "tarball_url": "https://cdn.example/project.tar.gz",
        "outputs": ["https://cdn.example/video.mp4"]
      },
      "percent": 100,
      "stage": "rendering",
      "progress": [
        {"stage": "rendering", "message": "Rendering scene 2", "pct": 100, "t": 1750000300}
      ]
    }
  },
  "agent": null
}
```

Key fields:

- `status`: authoritative lifecycle state. Typical values are `pending`, `scripting`, `generating`, `rendering`, `captioning`, `qc`, `succeeded`, and `failed`. Terminal values are `succeeded` and `failed`.
- `progress.percent`: normalized progress from 0 through 100.
- `progress.stage`, `message`, `activity`, and `render`: latest available production telemetry. Optional values may be `null`.
- `request`: normalized creation request stored with the task.
- `response`: final result or failure information when available.
- `response.data.variants`: delivered language variants. Read each actual `output_url` from this array.
- `response.data.project`: project-level artifacts when present.
- `response.data.progress`: append-only production event history when present.

A succeeded task may retain the name of its last execution stage in `progress.stage`; use top-level `status`, not the stage name, to decide whether the task is complete.

## Polling

Poll at a reasonable cadence and use exponential backoff with jitter. Continue through nonterminal statuses, then stop at `succeeded` or `failed`. Do not create a duplicate video merely because production is taking time.

Example polling logic with application-supplied timing:

```python
import os
import random
import time

import requests

task_id = "f57e99c4-f60f-4373-a155-17742ce2357d"
delay = float(os.environ["MAESTRO_INITIAL_POLL_DELAY"])
maximum_delay = float(os.environ["MAESTRO_MAXIMUM_POLL_DELAY"])
backoff_factor = float(os.environ["MAESTRO_POLL_BACKOFF_FACTOR"])

while True:
    response = requests.post(
        "https://api.acedata.cloud/maestro/tasks",
        headers={"Authorization": "******"},
        json={"id": task_id, "action": "retrieve"},
        timeout=30,
    )
    response.raise_for_status()
    task = response.json()

    if task["status"] in {"succeeded", "failed"}:
        break

    time.sleep(delay + random.random())
    delay = min(delay * backoff_factor, maximum_delay)

print(task)
```

Choose these client-side timing values for your workload and current service behavior; the API does not publish fixed polling-interval guarantees.

## Errors

If a single task is not found, the service returns HTTP 404 with a JSON `detail` message:

```json
{
  "detail": "task not found"
}
```

Authentication, rate-limit, and infrastructure errors passing through Ace Data Cloud use the standard gateway envelope:

```json
{
  "error": {
    "code": "invalid_token",
    "message": "Invalid token"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

Use the HTTP status and `trace_id` in retry, diagnostics, and support flows.

## Related API

Create or iterate on videos with the [Maestro Videos API guide](maestro_videos_api_integration_guide.md).