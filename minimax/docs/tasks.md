# Task Retrieval

`POST https://api.acedata.cloud/minimax/tasks`

Task retrieval and task-record deletion are free operations.

## Authentication

```http
Authorization: ******
Content-Type: application/json
Accept: application/json
```

## Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `action` | string | no | `retrieve` (default), `retrieve_batch`, or `delete` |
| `id` | string | conditional | Task ID for `retrieve` or `delete` |
| `ids` | string[] | conditional | Task ID list for batch retrieval |
| `limit` | integer | no | Maximum number of items to return |
| `offset` | integer | no | Pagination offset |
| `created_at_min` | number | no | Return tasks created at/after this Unix timestamp |
| `created_at_max` | number | no | Return tasks created at/before this Unix timestamp |

## Retrieve one task

```json
{
  "action": "retrieve",
  "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28"
}
```

Possible shape:

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
    "ratio": "adaptive",
    "task_type": "generation",
    "modality": "video"
  }
}
```

`status` values: `queued`, `running`, `succeeded`, `failed`, `cancelled`.

## Retrieve task list

```json
{
  "action": "retrieve_batch",
  "limit": 20,
  "offset": 0
}
```

Possible shape:

```json
{
  "items": [
    {
      "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28",
      "status": "succeeded"
    }
  ],
  "total": 1
}
```

## Delete a task record

```json
{
  "action": "delete",
  "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28"
}
```

Possible shape:

```json
{
  "id": "c0f63a98-a7dc-4a09-a1fb-46d32b312a28",
  "deleted": true
}
```

Deletion removes the stored task record only. It does not cancel a generation already in progress.

## Errors

Common status codes: `400`, `401`, `429`, `500`.
