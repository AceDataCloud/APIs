# WebExtrator Tasks API Integration Guide

`POST https://api.acedata.cloud/webextrator/tasks` (**Free**)

This API queries historical `render` / `extract` task records (retained for 7 days).

## Authentication

Add `Authorization: Bearer <your API Key>` to the request header.

## Request Parameters

### `action: "retrieve"` (single task)

| Field | Type | Required | Description |
|------|------|:----:|------|
| `action` | const | ✅ | Fixed value: `"retrieve"` |
| `id` | string | one of | Task ID |
| `trace_id` | string | one of | Trace ID |

Use either `id` or `trace_id`.

### `action: "retrieve_batch"` (batch query)

| Field | Type | Required | Description |
|------|------|:----:|------|
| `action` | const | ✅ | Fixed value: `"retrieve_batch"` |
| `ids` | string[] | one of | Task ID list |
| `trace_ids` | string[] | one of | Trace ID list |
| `offset` | number | ❌ | Pagination offset |
| `limit` | number | ❌ | Page size |

Use either `ids` or `trace_ids`.

## Single Task Response

```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "trace_id": "550e8400-e29b-41d4-a716-446655440001",
    "type": "extract",
    "created_at": 1730000000000,
    "started_at": "2026-05-02T10:30:00.123Z",
    "finished_at": "2026-05-02T10:30:02.535Z",
    "elapsed": 2.412,
    "request": { "url": "https://example.com" },
    "response": { "success": true, "data": {} }
  }
}
```

If no record is found, the API returns `{ "task": null }` (HTTP 200).

## Batch Response

```json
{
  "tasks": [
    { "id": "550e8400-e29b-41d4-a716-446655440000" },
    { "id": "550e8400-e29b-41d4-a716-446655440002" }
  ],
  "offset": 0,
  "limit": 50
}
```

## Example

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve",
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

## Error Response

| HTTP | `error.code` | Meaning |
|------|--------------|------|
| 400 | `bad_request` | Invalid request body. |
| 401 | `unauthorized` | Missing or invalid token. |

```json
{ "error": { "code": "bad_request", "message": "..." } }
```
