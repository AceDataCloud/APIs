# Task Retrieval

`POST https://api.acedata.cloud/minimax/tasks` retrieves, lists, cancels, or deletes MiniMax H3 video tasks. Task retrieval is free and never charges the generation again.

## Retrieve one

```json
{
  "action": "retrieve",
  "id": "TASK_ID"
}
```

## Retrieve several

```json
{
  "action": "retrieve_batch",
  "ids": ["TASK_ID_1", "TASK_ID_2"]
}
```

You can also omit `ids` and filter with `created_at_min`, `created_at_max`, `offset`, and `limit` to page through tasks from the last seven days.

The batch response contains `items` and `total`. Poll approximately every 10 seconds until each task reaches `succeeded`, `failed`, or `cancelled`.

## Task result

`retrieve` returns a `task` object. A successful task includes:

```json
{
  "task": {
    "id": "TASK_ID",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "content": {
      "url": "https://cdn.acedata.cloud/minimax/TASK_ID.mp4"
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

Statuses are `queued`, `running`, `succeeded`, `failed`, and `cancelled`. Read `task.content.url` only after `succeeded`; failed tasks include `task.error`.

## Delete a task record

```json
{
  "action": "delete",
  "id": "TASK_ID"
}
```

For a `queued` task, delete cancels the task before it starts. For completed or failed tasks, it deletes the stored task record. Running or already cancelled tasks cannot be deleted or cancelled again.
