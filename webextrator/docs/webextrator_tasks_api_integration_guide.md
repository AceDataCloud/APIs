# WebExtrator Tasks API Integration Guide

`POST https://api.acedata.cloud/webextrator/tasks` (**Free**)

This document introduces the WebExtrator Tasks API. This API allows you to query historical `render` / `extract` tasks (retained for 7 days).

## Application Process

The WebExtrator Tasks API is bundled with the existing WebExtrator service. If you already have access to the WebExtrator Render or Extract API, you can call this endpoint with the same authorization token — no additional application is required.

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

### CURL Example

```bash
curl -X POST 'https://api.acedata.cloud/webextrator/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve_batch",
    "ids": ["550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440002"],
    "limit": 12,
    "offset": 0
  }'
```

## Field Definitions

| Field | Description |
|------|------|
| `id` / `task_id` | Unique task ID |
| `trace_id` | Call chain ID (aligned with PlatformGateway / CLS) |
| `type` | `render` or `extract` |
| `request` | Original request body |
| `response` | Render / extraction result (same as the `data` field in a sync response) |
| `started_at` / `finished_at` / `elapsed` | Timestamps and duration (seconds) |

> This API is free and does not count toward usage.

## Conclusion

Through this document, you have learned how to use the WebExtrator Tasks API to query single or batch historical render and extract tasks. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
