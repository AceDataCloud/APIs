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

The response is a task record object (`id`, `request`, `response`, `created_at`, `started_at`, `finished_at`, `elapsed`, `trace_id`, and related metadata fields). Poll approximately every five seconds until the stored `response` contains a successful result or an error.

`action` supports `retrieve` and `retrieve_batch`.

For retrieve_batch requests, use `ids` with multiple task IDs.
