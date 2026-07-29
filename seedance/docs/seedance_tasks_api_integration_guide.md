# Seedance Tasks API Integration and Usage

The main function of the Seedance Tasks API is to query the execution status of tasks by inputting the task ID returned by the Seedance Videos Generation API.

This document describes the Seedance Tasks API integration, helping you query the status and full detail of an asynchronous Seedance video generation task, either individually or in batch.

## Application Process

To use the Seedance Tasks API, you first need to apply for the corresponding service on the application page [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8), and then copy the task ID returned by the Seedance Videos Generation API.

Finally, go to the Tasks API page [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c) to apply for the corresponding service. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the [login page](https://platform.acedata.cloud) inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Request Example

The Seedance Tasks API queries the result of a task created by the Seedance Videos Generation API. For how to create a task, see [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) and submit the request with `"async": true` (or a `callback_url`).

We will take a task ID returned by the Seedance Videos Generation API as an example. Suppose the task ID is `9462ca25-468b-45a5-9e75-6f516dedcc80`.

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: The key to call the API, which can be selected directly after application.

**Request Body** includes:

- `id`: The task ID returned by the Seedance Videos Generation API.
- `action`: The operation to perform. Use `retrieve` (default) for a single task or `retrieve_batch` for multiple tasks.

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
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
payload = {
    "id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
    "action": "retrieve"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

### Response Example

A successful retrieve response returns the full task record, including the original request and response:

```json
{
  "_id": "69480c5cff2676299c7b351d",
  "id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
  "api_id": "44e45d2b-8754-4a93-b793-c63271335f6f",
  "application_id": "1456a4bf-e2f4-4247-9b2d-fb49effc6eca",
  "created_at": 1766329436.091,
  "credential_id": "3e20b461-f750-48d3-a1f7-3aea48d15d77",
  "request": {
    "model": "doubao-seedance-1-0-pro-250528",
    "content": [
      {
        "type": "text",
        "text": "Multiple shots. A detective enters a dimly lit room."
      }
    ],
    "callback_url": "dummy"
  },
  "trace_id": "24b1b09c-5649-4290-98db-eab23e5efcac",
  "type": "videos",
  "user_id": "ad7afe47-cea9-4cda-980f-2ad8810e51cf",
  "response": {
    "success": true,
    "task_id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
    "trace_id": "24b1b09c-5649-4290-98db-eab23e5efcac",
    "data": {
      "task_id": "cgt-20251221230356-sxgt7",
      "status": "succeeded",
      "video_url": "https://platform.cdn.acedata.cloud/seedance/d1c2e49e-d854-4a2e-b0c0-88e520f82e2e.mp4",
      "last_frame_url": null,
      "model": "doubao-seedance-1-0-pro-250528"
    }
  }
}
```

The key fields in the returned result:

- `id`: The ID of the generated task, used to uniquely identify this generation task.
- `request`: The original request body when the task was initiated.
- `response`: The full response from the video generation, including `data.status`, `data.video_url`, and `data.model`.

Check `response.data.status` to determine if the task has completed. Poll this endpoint until `response.data.status` is `succeeded` (or a terminal failure state), then download the video from `response.data.video_url`.

## Batch Query

To query multiple tasks at once, use `action: "retrieve_batch"` with an `ids` array:

### Code Example

#### CURL

```bash
curl -X POST 'https://api.acedata.cloud/seedance/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "ids": ["9462ca25-468b-45a5-9e75-6f516dedcc80", "d9e576bd-ca14-4c6f-a541-f4734e941dbe"],
    "action": "retrieve_batch"
  }'
```

### Response Example

The batch response wraps results in an `items` array with a `count` field:

```json
{
  "items": [
    {
      "_id": "69480c5cff2676299c7b351d",
      "id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
      "request": {
        "model": "doubao-seedance-1-0-pro-250528",
        "content": [{ "type": "text", "text": "Multiple shots. A detective enters a dimly lit room." }]
      },
      "response": {
        "success": true,
        "task_id": "9462ca25-468b-45a5-9e75-6f516dedcc80",
        "data": {
          "task_id": "cgt-20251221230356-sxgt7",
          "status": "succeeded",
          "video_url": "https://platform.cdn.acedata.cloud/seedance/d1c2e49e-d854-4a2e-b0c0-88e520f82e2e.mp4",
          "model": "doubao-seedance-1-0-pro-250528"
        }
      }
    },
    {
      "_id": "69480e0dff2676299c7cb98b",
      "id": "d9e576bd-ca14-4c6f-a541-f4734e941dbe",
      "request": {
        "model": "doubao-seedance-1-0-pro-250528",
        "content": [{ "type": "text", "text": "Multiple shots. A detective enters a dimly lit room." }]
      },
      "response": {
        "success": true,
        "task_id": "d9e576bd-ca14-4c6f-a541-f4734e941dbe",
        "data": {
          "task_id": "cgt-20251221231109-cnkhp",
          "status": "succeeded",
          "video_url": "https://platform.cdn.acedata.cloud/seedance/eb99ba03-178c-4616-8d19-e625fee2e884.mp4",
          "model": "doubao-seedance-1-0-pro-250528"
        }
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
| 429 | `too_many_requests` | You have exceeded the rate limit. |
| 500 | `api_error` | An internal or upstream error occurred. |

Each error response includes a `trace_id` to help with debugging and support.
