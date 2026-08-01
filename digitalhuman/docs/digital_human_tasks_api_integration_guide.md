# Digital Human Tasks API Integration Guide

This guide explains how to query or manage asynchronous Digital Human tasks.

## Authentication

Send your Ace Data Cloud API token in the `authorization` header for every request.

## Request Endpoint

`POST https://api.acedata.cloud/digital-human/tasks`

## Request Body

- `task_id` (required): task ID returned by the videos or voices API.
- `action`: optional. Supported values are `retrieve`, `retrieve_batch`, and `delete`.

When `action` is omitted, the API returns the flat polling shape (`state`, `progress`, `video_url`, and related fields).

## Request Example

```bash
curl -X POST 'https://api.acedata.cloud/digital-human/tasks' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "task_id": "task_49af42c410c24f04ad416b28af55d237"
  }'
```

## Response Example

```json
{
  "success": true,
  "task_id": "task_...",
  "trace_id": "...",
  "state": "succeed",
  "progress": 100,
  "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
  "duration": 17.2,
  "width": 1280,
  "height": 720,
  "engine": "latentsync"
}
```

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
