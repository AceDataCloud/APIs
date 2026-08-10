---
title: "Gemini Tasks API Integration and Usage"
description: "Gemini AI integration guide - Ace Data Cloud"
---

Use the Gemini Tasks API to retrieve the status and result of Gemini video-generation tasks.

## Retrieve a task

```bash
curl -X POST 'https://api.acedata.cloud/gemini/tasks' \
  -H 'Authorization: ******' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"id":"b8976e18-32dc-4718-9ed8-1ea090fcb6ea","action":"retrieve"}'
```

The response includes `id`, `type`, `request`, `response`, `created_at`, `started_at`, and—after completion—`finished_at` and `elapsed`.

## Retrieve tasks in bulk

Set `action` to `retrieve_batch` and provide task IDs in `ids`:

```json
{
  "ids": ["b8976e18-32dc-4718-9ed8-1ea090fcb6ea"],
  "action": "retrieve_batch"
}
```
