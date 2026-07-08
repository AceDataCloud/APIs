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

- `id`: The task ID returned by the Seedance Videos Generation API.
- `action`: The operation to perform. Use `retrieve` (default) to query a single task, or `retrieve_batch` to query multiple tasks at once.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "id": "ec22ae22-0140-4033-8c86-a48b536da595",
    "action": "retrieve"
  }'
```

#### Python

```python
import requests

url = "https://api.acedata.cloud/seedance/tasks"
headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json",
}
payload = {"id": "ec22ae22-0140-4033-8c86-a48b536da595", "action": "retrieve"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

```json
{
  "id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "request": {
    "model": "doubao-seedance-1-0-pro-250528",
    "content": [
      {
        "type": "text",
        "text": "A kitten yawning at the camera."
      }
    ]
  },
  "response": {
    "success": true,
    "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
    "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
    "data": {
      "task_id": "cgt-20251222005129-62fhb",
      "status": "succeeded",
      "video_url": "https://platform.cdn.acedata.cloud/seedance/f592800a-b87c-4705-8796-cbb8018cae35.mp4",
      "last_frame_url": null,
      "model": "doubao-seedance-1-0-pro-250528"
    }
  }
}
```

The returned result contains the following fields:

- `id`: The ID of the generated task, used to uniquely identify this generation task.
- `request`: The request body when the task was created.
- `response`: The response body of the task, including `success`, `task_id`, `trace_id`, and `data`.
  - `data.status`: The current task status (`processing`, `succeeded`, or a failure state).
  - `data.video_url`: The generated video URL (available once `status` is `succeeded`).
  - `data.model`: The model used to generate the video.

Poll this endpoint until `response.data.status` is `succeeded` (or a terminal failure state), then download the video from `response.data.video_url`.

## Batch Query

To query multiple tasks at once, use `action: "retrieve_batch"` with an `ids` array instead of a single `id`:

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "ids": ["ec22ae22-0140-4033-8c86-a48b536da595", "d9e576bd-ca14-4c6f-a541-f4734e941dbe"],
    "action": "retrieve_batch"
  }'
```

The response contains an `items` array of task records and a `count` field:

```json
{
  "items": [
    {
      "id": "ec22ae22-0140-4033-8c86-a48b536da595",
      "request": { "model": "doubao-seedance-1-0-pro-250528", "content": [...] },
      "response": {
        "success": true,
        "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
        "data": { "status": "succeeded", "video_url": "https://platform.cdn.acedata.cloud/seedance/..." }
      }
    },
    {
      "id": "d9e576bd-ca14-4c6f-a541-f4734e941dbe",
      "request": { "model": "doubao-seedance-1-0-pro-250528", "content": [...] },
      "response": {
        "success": true,
        "task_id": "d9e576bd-ca14-4c6f-a541-f4734e941dbe",
        "data": { "status": "succeeded", "video_url": "https://platform.cdn.acedata.cloud/seedance/..." }
      }
    }
  ],
  "count": 2
}
```

## Error Codes

| HTTP Status | Code | Meaning |
| ---- | ---- | ---- |
| 400 | `bad_request` | Invalid request, e.g. a missing or malformed task `id`. |
| 401 | `invalid_token` | The token is invalid or wrong. |
| 401 | `token_expired` | The token has expired. |
| 404 | `not_found` | The specified task ID was not found. |

Each error response includes a `trace_id` to help with debugging and support.
