# Gemini Tasks API Integration and Usage

The Gemini Tasks API lets you query async Gemini tasks after the original request returns a `task_id`.
Use it to retrieve one task by `id` or fetch multiple tasks in a single batch request.

## Endpoint

```text
POST https://api.acedata.cloud/gemini/tasks
```

## Request Headers

- `accept: application/json`
- `authorization: ******`
- `content-type: application/json`

## Query a Single Task

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' -H 'accept: application/json' -H 'authorization: ******' -H 'content-type: application/json' -d '{
  "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "action": "retrieve"
}'
```

### Response Example

```json
{
  "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "request": {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9"
  },
  "type": "videos",
  "created_at": 1763142607.967,
  "started_at": "2025-11-14T17:50:07.970000000Z",
  "finished_at": 1763142637.404,
  "elapsed": 29.437,
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

Returned task records include the following fields:

- `id`: the generated task ID.
- `request`: the original request body.
- `response`: the final response body.
- `created_at`: the task creation time as a Unix timestamp in seconds.
- `started_at`: the task start time as an ISO-8601 UTC timestamp.
- `finished_at`: the task completion time as a Unix timestamp in seconds. This field is absent until the task finishes.
- `elapsed`: the task runtime in seconds. This field is absent until the task finishes.

## Batch Query Operation

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' -H 'accept: application/json' -H 'authorization: ******' -H 'content-type: application/json' -d '{
  "ids": ["b8976e18-32dc-4718-9ed8-1ea090fcb6ea"],
  "action": "retrieve_batch"
}'
```
