# Seedance Tasks API Integration and Usage

The main function of the Seedance Tasks API is to query the execution status of tasks by inputting the task ID returned by the Seedance Videos Generation API.

This document describes the Seedance Tasks API integration, helping you query the status and final result of an asynchronous Seedance video generation task.

## Application Process

To use the Seedance Tasks API, you first need to apply for the corresponding service on the application page [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8), and then copy the task ID returned by the Seedance Videos Generation API.

Finally, go to the Tasks API page [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c) to apply for the corresponding service. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Example

The Seedance Tasks API queries the result of a task created by the Seedance Videos Generation API. For how to create a task, see [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) and submit the request with `"async": true` (or a `callback_url`).

We will take a task ID returned by the Seedance Videos Generation API as an example. Suppose the task ID is `ec22ae22-0140-4033-8c86-a48b536da595`.

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly after application.

**Request Body** includes:

- `id`: The task ID returned by the Seedance Videos Generation API (single retrieval).
- `ids`: An array of task IDs for batch retrieval (use with `action: "retrieve_batch"`).
- `action`: The retrieval action. One of:
  - `retrieve` (default) — retrieve a single task by `id`.
  - `retrieve_batch` — retrieve multiple tasks by `ids`.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "id": "ec22ae22-0140-4033-8c86-a48b536da595"
  }'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/seedance/tasks"
headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json",
}
payload = {"id": "ec22ae22-0140-4033-8c86-a48b536da595"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

While the task is still running, the `status` will not yet be `succeeded`:

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": [
    {
      "id": "cgt-20251222005129-62fhb",
      "status": "processing"
    }
  ]
}
```

When the task has completed, the response includes the final `content.video_url`:

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": [
    {
      "id": "cgt-20251222005129-62fhb",
      "model": "doubao-seedance-2-0-260128",
      "status": "succeeded",
      "content": {
        "video_url": "https://platform.cdn.acedata.cloud/seedance/f592800a-b87c-4705-8796-cbb8018cae35.mp4"
      },
      "seed": 10,
      "resolution": "1080p",
      "ratio": "16:9",
      "duration": 5,
      "framespersecond": 24,
      "execution_expires_after": 172800,
      "usage": {
        "completion_tokens": 108900,
        "total_tokens": 108900
      },
      "created_at": 1743414619,
      "updated_at": 1743414673
    }
  ]
}
```

The returned result contains the following fields:

- `success`: whether the query succeeded.
- `task_id`: the ID of the video generation task.
- `trace_id`: the trace ID for this request.
- `data`: array of task result objects. Each item includes:
  - `id`: the internal generation task ID.
  - `model`: the model used (present when task is complete).
  - `status`: the task status (`processing`, `succeeded`, `failed`).
  - `content.video_url`: URL of the generated video (present when `status` is `succeeded`).
  - `seed`, `resolution`, `ratio`, `duration`, `framespersecond`: generation parameters.
  - `execution_expires_after`: seconds until the task result expires.
  - `usage.completion_tokens`, `usage.total_tokens`: token consumption for billing.
  - `created_at`, `updated_at`: Unix timestamps.

Poll this endpoint until `data[0].status` is `succeeded` (or a terminal failure state), then download the video from `data[0].content.video_url`.

## Batch Retrieval

To retrieve multiple tasks at once, use `action: "retrieve_batch"` with an `ids` array:

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "action": "retrieve_batch",
    "ids": [
      "ec22ae22-0140-4033-8c86-a48b536da595",
      "fa33bf33-0251-5144-9d97-b59c647eb6a6"
    ]
  }'
```

## Error Codes

| HTTP Status | Code | Meaning |
| ---- | ---- | ---- |
| 400 | `bad_request` | Invalid request, e.g. a missing or malformed task `id`. |
| 401 | `invalid_token` | The token is invalid or wrong. |
| 401 | `token_expired` | The token has expired. |
| 404 | `not_found` | The specified task ID was not found. |

Each error response includes a `trace_id` to help with debugging and support.
