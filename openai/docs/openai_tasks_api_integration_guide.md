# OpenAI Tasks API Application and Usage

The OpenAI Tasks API is used to query the results of tasks previously submitted to OpenAI image endpoints in **callback mode**. Use this API when you cannot wait for a synchronous HTTP response, or when you wish to query a task result later using its `id` or a custom `trace_id`.

> Only tasks submitted with a `callback_url` are persisted. Requests made in synchronous (non-callback) mode are not stored.

## Application Process

The OpenAI Tasks API shares authorization with the existing OpenAI services. If you have already applied for [OpenAI Images Generations](https://platform.acedata.cloud/services/06f2acb7-3a85-4b5a-bda8-2d9bbe2b4c8f), you can use the same token to call this API directly — no additional application is required.

New users receive a free quota upon first application.

## API Endpoint

```
POST https://api.acedata.cloud/openai/tasks
```

Supported `action` values:

| Action | Description |
| --- | --- |
| `retrieve` | Query a single task by `id` or `trace_id` |
| `retrieve_batch` | Batch query by `ids` / `trace_ids` / `application_id` / `user_id` |

## Request Headers

- `accept: application/json`
- `authorization: Bearer {token}`
- `content-type: application/json`

## Single Task Query (`retrieve`)

### Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `action` | string | Yes | Fixed value: `retrieve` |
| `id` | string | One of the two | The task ID returned when the image request was submitted |
| `trace_id` | string | One of the two | The custom `trace_id` you passed in the original request |

At least one of `id` or `trace_id` must be provided. If both are provided, `trace_id` takes precedence.

### Code Examples

#### cURL

```bash
curl -X POST 'https://api.acedata.cloud/openai/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve",
    "id": "7489df4c-ef03-4de0-b598-e9a590793434"
  }'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/openai/tasks"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {
    "action": "retrieve",
    "trace_id": "my-custom-trace-001",
}
response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

When the task exists:

```json
{
  "_id": "67a1b2c3d4e5f6a7b8c9d0e1",
  "id": "7489df4c-ef03-4de0-b598-e9a590793434",
  "trace_id": "my-custom-trace-001",
  "type": "images_generations",
  "application_id": "9dec7b2a-1cad-41ff-8536-d4ddaf2525d4",
  "user_id": "5d8e7f6a-1234-4abc-9def-0123456789ab",
  "credential_id": "68253cc8-505d-47f4-97ad-0050a62e4975",
  "created_at": 1763142607.967,
  "finished_at": 1763142637.404,
  "duration": 29.437,
  "request": {
    "model": "gpt-image-1",
    "prompt": "A cat sitting on a table",
    "size": "1024x1024",
    "callback_url": "https://your.server/callback"
  },
  "response": {
    "created": 1763142637,
    "data": [
      { "url": "https://platform.cdn.acedata.cloud/openai/...png" }
    ],
    "success": true
  }
}
```

When no matching task is found, an empty object is returned:

```json
{}
```

### Field Descriptions

- `id`: The task ID generated when the original image request was accepted.
- `trace_id`: The custom tracking identifier passed in the original request, used for client-side business association.
- `type`: The upstream endpoint type, e.g., `images_generations`, `images_edits`, `chat_completions_image`, etc.
- `request`: The complete request body of the original request.
- `response`: The final response body returned by the upstream endpoint upon callback completion.
- `created_at` / `finished_at` / `duration`: Unix timestamps (seconds) and execution duration (seconds).
- `application_id` / `user_id` / `credential_id`: The associated application, end user, and credential IDs.

## Batch Query (`retrieve_batch`)

### Request Body

| Field | Type | Description |
| --- | --- | --- |
| `action` | string | Fixed value: `retrieve_batch` |
| `ids` | string[] | Query by a list of task IDs |
| `trace_ids` | string[] | Query by a list of `trace_id` values |
| `application_id` | string | Query all tasks for an application |
| `user_id` | string | Query all tasks for an end user |
| `type` | string | Filter by upstream type (e.g., `images_generations`) |
| `offset` | int | Pagination start index, default `0` |
| `limit` | int | Items per page, default `12` |
| `created_at_min` | float | Start timestamp (Unix seconds) |
| `created_at_max` | float | End timestamp (Unix seconds) |

Provide one of `ids` / `trace_ids` / `application_id` / `user_id` or a `created_at_*` time window.

### cURL Example

```bash
curl -X POST 'https://api.acedata.cloud/openai/tasks' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve_batch",
    "trace_ids": ["my-trace-001", "my-trace-002"]
  }'
```

### Response Example

```json
{
  "items": [
    {
      "_id": "67a1b2c3d4e5f6a7b8c9d0e1",
      "id": "7489df4c-ef03-4de0-b598-e9a590793434",
      "trace_id": "my-trace-001",
      "type": "images_generations",
      "request": { "model": "gpt-image-1", "prompt": "A cat" },
      "response": { "data": [{ "url": "https://...png" }] },
      "created_at": 1763142607.967,
      "finished_at": 1763142637.404
    }
  ],
  "count": 1
}
```

## End-to-End Example: Submit and Poll

The Tasks API primarily serves asynchronous workflows in callback mode. Here is a complete example:

```python
import os, time, uuid, requests

API = "https://api.acedata.cloud"
HEADERS = {
    "authorization": f"Bearer {os.environ['ACEDATA_API_KEY']}",
    "content-type": "application/json",
}

# 1. Submit an image generation task with a callback_url and trace_id
trace_id = str(uuid.uuid4())
submit = requests.post(
    f"{API}/openai/images/generations",
    headers=HEADERS,
    json={
        "model": "gpt-image-1",
        "prompt": "A watercolor-style cat sitting on a table",
        "callback_url": "https://webhook.site/your-uuid",
        "trace_id": trace_id,
    },
).json()
print("submitted:", submit)

# 2. Poll the Tasks API until the task completes
while True:
    task = requests.post(
        f"{API}/openai/tasks",
        headers=HEADERS,
        json={"action": "retrieve", "trace_id": trace_id},
    ).json()
    if task and task.get("response"):
        print("finished:", task["response"])
        break
    time.sleep(3)
```

## Notes

- The Tasks API itself is **not billed**; polling it is free. Only the original image generation/editing requests incur charges.
- A task record is only created when the original request includes a `callback_url`; synchronous calls do not produce queryable tasks.
- Task records beyond the platform's retention period may be purged.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Conclusion

Through this document, you have learned how to use the OpenAI Tasks API to query the results of previously submitted image tasks. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
