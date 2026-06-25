# Gemini Tasks API Integration Guide

The Gemini Tasks API allows you to query the execution status and result of a task created by the [Gemini Videos Generation API](gemini_videos_api_integration_guide.md) using its task ID.

## Application Process

To use the Gemini Tasks API, obtain your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in or registering, you will be automatically returned to the current page.

A single API Token grants access to all platform services. There is a free quota available for first-time applicants, allowing you to use the API for free.

> 📘 Full documentation: [Gemini Videos Generation API →](https://platform.acedata.cloud/documents/gemini-videos)

## Request Example

The Gemini Tasks API retrieves the result of a Gemini Videos Generation API task. Refer to [Gemini Videos Generation API](gemini_videos_api_integration_guide.md) for details on how to start a generation task and obtain a `task_id`.

### Request Headers

- `accept`: Response format, set to `application/json`.
- `authorization`: Your API key, prefixed with `******

### Request Body

- `id`: The task ID to query.
- `action`: Operation type. Use `retrieve` for a single task query.

### cURL

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "action": "retrieve"
  }'
```

### Python

```python
import requests

url = "https://api.acedata.cloud/gemini/tasks"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "action": "retrieve"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

On a successful request, the API returns the task details. The `request` field contains the original request body, and the `response` field contains the generation result:

```json
{
  "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "request": {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
  },
  "type": "videos",
  "response": {
    "success": true,
    "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
    "data": [
      {
        "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
        "video_url": "https://cdn.acedata.cloud/gemini/example-video.mp4",
        "state": "succeeded"
      }
    ]
  }
}
```

Response fields:

- `id`: The task ID used to uniquely identify this generation task.
- `request`: The request body that was submitted when the task was created.
- `response`: The generation result returned when the task completed.

## Batch Query

To query multiple task IDs at once, set `action` to `retrieve_batch` and pass an array of IDs in `ids`:

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "ids": ["b8976e18-32dc-4718-9ed8-1ea090fcb6ea"],
    "action": "retrieve_batch"
  }'
```

## Error Handling

| Status | Error Code | Description |
| ------ | ---------- | ----------- |
| 400 | `token_mismatched` | The token does not match the API. |
| 401 | `invalid_token` | Authentication failed — token is invalid or wrong. |
| 500 | `api_error` | Internal server error. |

Error response example:

```json
{
  "error": {
    "code": "token_mismatched",
    "message": "The specified token is not matched with API."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```
