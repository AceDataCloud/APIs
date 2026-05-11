# WebExtrator Tasks API Integration Guide

`POST https://api.acedata.cloud/webextrator/tasks` (**Free**)

This document introduces the WebExtrator Tasks API. This API allows you to query historical `render` / `extract` tasks (retained for 7 days).

## Application Process

The WebExtrator Tasks API is bundled with the existing WebExtrator service. If you already have access to the WebExtrator Render or Extract API, you can call this endpoint with the same authorization token — no additional application is required.

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Single Task Query

Query by task ID:

```json
{
  "action": "retrieve",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Or query by `trace_id`:

```json
{
  "action": "retrieve",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

Returns a single task object containing `request` / `response` / `started_at` / `finished_at`, and other fields.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/webextrator/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve",
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/webextrator/tasks"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "action": "retrieve",
    "id": "550e8400-e29b-41d4-a716-446655440000"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

## Batch Query

```json
{
  "action": "retrieve_batch",
  "ids": ["...", "..."],
  "limit": 12,
  "offset": 0
}
```

You can also use `trace_ids`, or omit both to paginate through your own task history.

Returns:

```json
{
  "items": [ { }, ... ],
  "count": 2
}
```

Example single-task response:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "render",
  "started_at": "2025-05-02T10:30:00.123Z",
  "finished_at": "2025-05-02T10:30:05.456Z",
  "elapsed": 5.333,
  "request": {
    "url": "https://example.com"
  },
  "response": {
    "kind": "render",
    "title": "Example Domain"
  }
}
```

## Error Handling

| HTTP | `error.code` | Meaning |
|------|--------------|---------|
| 400 | `bad_request` | Validation failed (`action` missing, invalid ID input, etc.) |
| 401 | `unauthorized` | Missing or invalid `Authorization: Bearer ...` |

```json
{
  "error": {
    "code": "bad_request",
    "message": "invalid action"
  }
}
```

## Field Definitions

| Field | Description |
|------|------|
| `id` / `task_id` | Unique task ID |
| `trace_id` | Call chain ID |
| `type` | `render` or `extract` |
| `request` | Original request body |
| `response` | Final result envelope |
| `started_at` / `finished_at` / `elapsed` | Timestamps and duration (seconds) |

> This API is free and does not count toward usage.

## Python Example (Polling until completion)

```python
import os
import time
import requests

API_KEY = os.environ["ACEDATA_API_KEY"]

while True:
    r = requests.post(
        "https://api.acedata.cloud/webextrator/tasks",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "action": "retrieve",
            "id": "550e8400-e29b-41d4-a716-446655440000",
        },
    ).json()
    if r.get("finished_at"):
        print(r["elapsed"])
        break
    time.sleep(2)
```

## Node.js Example (Fetch completed task)

```javascript
const res = await fetch('https://api.acedata.cloud/webextrator/tasks', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.ACEDATA_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ action: 'retrieve', id: '550e8400-e29b-41d4-a716-446655440000' }),
});

const result = await res.json();
console.log(result?.response);
```

## Notes

- Task records are retained for 7 days.
- `retrieve` returns a single task object.
- `retrieve_batch` returns `{ "items": [...], "count": n }`.
- Querying tasks is free.

## Conclusion

Through this document, you have learned how to use the WebExtrator Tasks API to query single or batch historical render and extract tasks. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
