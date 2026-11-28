# Seedance Tasks API Integration and Usage

The main function of the Seedance Tasks API is to query the execution status of tasks by inputting the task ID returned by the Seedance Videos Generation API.

This document describes the Seedance Tasks API integration, helping you query the status and final result of an asynchronous Seedance video generation task.

## Get an API key

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Keep the key on your server and use it in place of `{token}` in the examples.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

API reference: [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8), [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c).

## Request Example

The Seedance Tasks API queries the result of a task created by the Seedance Videos Generation API. For how to create a task, see [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) and submit the request with `"async": true` (or a `callback_url`).

We will take a task ID returned by the Seedance Videos Generation API as an example. Suppose the task ID is `ec22ae22-0140-4033-8c86-a48b536da595`.

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly after application.

**Request Body** includes:

- `id`: The task ID returned by the Seedance Videos Generation API.

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
  "data": {
    "task_id": "cgt-20251222005129-62fhb",
    "status": "processing"
  }
}
```

When the task has completed, the response includes the final `video_url`:

```json
{
  "success": true,
  "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "data": {
    "task_id": "cgt-20251222005129-62fhb",
    "status": "succeeded",
    "video_url": "https://platform.cdn.acedata.cloud/seedance/f592800a-b87c-4705-8796-cbb8018cae35.mp4",
    "model": "doubao-seedance-2-0-260128"
  }
}
```

The returned result contains the following fields:

- `success`: whether the query succeeded.
- `task_id`: the ID of the video generation task.
- `trace_id`: the trace ID for this request.
- `data`: the task result, including `status` and — once the task is `succeeded` — the `video_url` and `model`.

Poll this endpoint until `data.status` is `succeeded` (or a terminal failure state), then download the video from `data.video_url`.

## Error Codes

| HTTP Status | Code | Meaning |
| ---- | ---- | ---- |
| 400 | `bad_request` | Invalid request, e.g. a missing or malformed task `id`. |
| 401 | `invalid_token` | The token is invalid or wrong. |
| 401 | `token_expired` | The token has expired. |
| 404 | `not_found` | The specified task ID was not found. |

Each error response includes a `trace_id` to help with debugging and support.
