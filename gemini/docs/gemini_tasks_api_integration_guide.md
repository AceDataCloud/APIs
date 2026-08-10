# Gemini Tasks API Integration and Usage

The Gemini Tasks API returns the recorded request and latest known result for Gemini asynchronous jobs, including video generation tasks created by `POST /gemini/videos`.

## Application Process

Create an API Token in the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications), then send it in the `Authorization` header.

One API Token works across Ace Data Cloud services. New accounts receive starter credit, and you can top up shared balance in the [console](https://platform.acedata.cloud/console/coin).

Full documentation: [Gemini Tasks API](https://platform.acedata.cloud/documents/gemini-tasks)

## Single Task Query

Use the task ID returned by the Gemini Videos API and submit `action: "retrieve"`.

### Request Body

- `id` (string): task ID to query.
- `action` (string): use `retrieve` for a single task lookup.

### CURL Example

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

### Response Example

```json
{
  "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
  "type": "videos",
  "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
  "created_at": 1784112953.856,
  "started_at": 1784112954.102,
  "finished_at": 1784113021.328,
  "elapsed": 67.226,
  "request": {
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9",
    "async": true
  },
  "response": {
    "success": true,
    "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
    "data": [
      {
        "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
        "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
        "state": "succeeded"
      }
    ]
  }
}
```

The task record can include:

- `id`: task identifier.
- `type`: task type, such as `videos`.
- `trace_id`: request trace identifier.
- `request`: the request body recorded when the task was created.
- `response`: the latest stored result from the originating API call.
- `created_at`: task creation time, as a Unix timestamp in seconds.
- `started_at`: processing start time, when available.
- `finished_at`: processing completion time, when available.
- `elapsed`: total processing duration in seconds, when available.

## Batch Query Operation

To query multiple task IDs at once, submit `action: "retrieve_batch"` together with `ids`.

### Request Body

- `ids` (array): task IDs to query.
- `action` (string): use `retrieve_batch` for batch lookup.

### CURL Example

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

### Response Example

```json
{
  "items": [
    {
      "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
      "type": "videos",
      "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
      "created_at": 1784112953.856,
      "request": {
        "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
        "model": "omni-flash",
        "aspect_ratio": "16:9",
        "async": true
      },
      "response": {
        "success": true,
        "task_id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
        "trace_id": "fb751e1e-4705-49ea-9fd4-5024b7865ea2",
        "data": [
          {
            "id": "omni-flash:job_01k777hjrbfrgs2060q5zvf2a5",
            "video_url": "https://cdn.acedata.cloud/43a57990c0.mp4",
            "state": "succeeded"
          }
        ]
      }
    }
  ],
  "count": 1
}
```

Each object inside `items` follows the same structure as a single-task response. The current OpenAPI also allows an empty object when no task matches the requested identifier.

## Error Handling

The current Gemini Tasks OpenAPI documents the following error responses:

| HTTP Status Code | Meaning |
| --- | --- |
| 400 | Invalid request parameters |
| 401 | Authentication failed |
| 500 | Internal server error |
