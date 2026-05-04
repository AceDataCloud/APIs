# WebExtrator Tasks API Integration Guide

`POST https://api.acedata.cloud/webextrator/tasks` (**free**)

Query historical `render` / `extract` tasks (retained for 7 days).

## Single Task Query

By task ID:

```json
{
  "action": "retrieve",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

Or by `trace_id`:

```json
{
  "action": "retrieve",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

Returns a single task object containing `request`, `response`, `started_at`, `finished_at`, and other fields.

## Batch Query

```json
{
  "action": "retrieve_batch",
  "ids": ["...", "..."],
  "limit": 12,
  "offset": 0
}
```

You can also use `trace_ids`, or omit both to paginate through your own task history.

Returns:

```json
{
  "items": [ { "...task..." }, "..." ],
  "count": 2
}
```

## Field Reference

| Field | Description |
|------|------|
| `id` / `task_id` | Unique task ID |
| `trace_id` | Call-chain ID (aligned with PlatformGateway / CLS) |
| `type` | `render` or `extract` |
| `request` | Original request body |
| `response` | Render / extract result (same as `data` in the sync response) |
| `started_at` / `finished_at` / `elapsed` | Timestamps and elapsed time (seconds) |

> This endpoint is **free** and does not count toward usage.

## Conclusion

Through this document, you have learned how to use the WebExtrator Tasks API to query the status and results of render and extract tasks. We hope this document can help you better integrate and use this API. If you have any questions, please feel free to contact our technical support team.
