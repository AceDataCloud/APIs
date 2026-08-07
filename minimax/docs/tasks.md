# Task Retrieval

`POST https://api.acedata.cloud/minimax/tasks` is free and never charges the generation again.

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

The response contains `items` and `total`. You can also filter and paginate tasks with `created_at_min`, `created_at_max`, `offset`, and `limit`.

## Delete a task record

```json
{
  "action": "delete",
  "id": "TASK_ID"
}
```

Deletion removes the stored task record only. It does not cancel a generation already in progress.

## Task result

A retrieved task contains `id`, `model` (`MiniMax-H3`), `status`, `task_type` (`generation`), and `modality` (`video`). `status` can be `queued`, `running`, `succeeded`, `failed`, or `cancelled`.

For a successful task, the completed video URL is `task.content.url`. Failed tasks provide `task.error.code` and `task.error.message`. Usage includes `total_seconds`, `input_seconds`, `output_seconds`, and `input_image_count`.
