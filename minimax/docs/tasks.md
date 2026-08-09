# Task Retrieval

`POST https://api.acedata.cloud/minimax/tasks` retrieves or deletes MiniMax task records. This endpoint requires bearer authentication with an API token from the AceDataCloud console.

## Parameters

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `action` | string | `retrieve` | `retrieve`, `retrieve_batch`, or `delete` |
| `id` | string | — | Task ID for `retrieve` or `delete` |
| `ids` | string[] | — | Task IDs for `retrieve_batch` |
| `limit` | integer | — | Maximum records to return when listing records |
| `offset` | integer | — | Record offset when listing records |
| `created_at_min` | number | — | Minimum creation timestamp filter |
| `created_at_max` | number | — | Maximum creation timestamp filter |

## Retrieve one

```json
{
  "action": "retrieve",
  "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28"
}
```

The response contains a `task` object:

```json
{
  "task": {
    "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1785125529,
    "updated_at": 1785125946,
    "content": {
      "url": "https://cdn.acedata.cloud/minimax/c0f63a98-a7dc-4a09-a1fb-46d32b312a28.mp4"
    },
    "resolution": "2K",
    "duration": 5,
    "usage": {
      "total_seconds": 5,
      "input_seconds": 0,
      "output_seconds": 5,
      "input_image_count": 1
    },
    "ratio": "adaptive",
    "task_type": "generation",
    "modality": "video"
  }
}
```

Poll approximately every five seconds until the task `status` is `succeeded`, `failed`, or `cancelled`.

## Retrieve several

```json
{
  "action": "retrieve_batch",
  "ids": ["TASK_ID_1", "TASK_ID_2"]
}
```

Batch responses contain `items` and `total`.

## Delete a task record

```json
{
  "action": "delete",
  "id": "TASK_ID"
}
```

Delete responses contain the deleted task `id` and a `deleted` boolean. Deletion removes the stored task record only. It does not cancel a generation already in progress.
