# Captcha Tasks API Integration Guide

`POST /captcha/tasks` retrieves the result of a captcha request submitted with
`async: true`. It supports both token and recognition captcha APIs.

## Authentication

```http
Authorization: ******
```

## Request

| Field | Required | Description |
| --- | --- | --- |
| `task_id` | Yes | The task ID returned by an asynchronous captcha request. |

```bash
curl --request POST "https://api.acedata.cloud/captcha/tasks" \
  --header "accept: application/json" \
  --header "Authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002"
  }'
```

### Processing response

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "processing"
}
```

### Completed token response

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni......"
}
```

When `status` is `ready`, token APIs return `token`, recognition APIs return
`solution`, and image-to-text APIs return `text`. Completed responses can also
include `started_at`, `finished_at`, and `elapsed` timing fields.

## Errors

The endpoint returns `400` when `task_id` is missing, `401` for an invalid or
missing API token, and `404` when the task does not exist. Error responses
include an `error` object and `trace_id`.
