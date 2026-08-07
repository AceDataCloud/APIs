# Task Retrieval

`POST https://api.acedata.cloud/minimax/tasks` is free and never charges the generation again.

## Retrieve one

```json
{
  "action": "retrieve",
  "id": "TASK_ID"
}
```

`action` defaults to `retrieve`, so sending only `id` is also valid.

## Retrieve several

```json
{
  "action": "retrieve_batch",
  "ids": ["TASK_ID_1", "TASK_ID_2"]
}
```

The response contains `items` and `count`. Batch queries can also filter with `trace_ids`, `application_id`, `created_at_min`, `created_at_max`, `offset`, and `limit`.

## Delete a task record

```json
{
  "action": "delete",
  "id": "TASK_ID"
}
```

Deletion removes only the stored task record in AceDataCloud. It does not cancel generation already in progress or delete downloaded videos.
