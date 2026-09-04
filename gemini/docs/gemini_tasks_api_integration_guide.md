# Gemini Tasks API Integration and Usage

The Gemini Tasks API retrieves the execution status and result of asynchronous Gemini video tasks.

## Authentication

Obtain an API token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and send it in the `Authorization` header. One API token can call all services on the platform.

## Retrieve One Task

Send a POST request to `/gemini/tasks` with `action` set to `retrieve`:

```bash
curl -X POST "https://api.acedata.cloud/gemini/tasks" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "b8976e18-32dc-4718-9ed8-1ea090fcb6ea",
    "action": "retrieve"
  }'
```

The response includes the task `id`, original `request`, task `type`, and `response`. Timing fields include `created_at`, `started_at`, `finished_at`, and `elapsed`; completion-only fields are omitted while a task is still running.

## Retrieve Multiple Tasks

Set `action` to `retrieve_batch` and provide `ids`:

```bash
curl -X POST "https://api.acedata.cloud/gemini/tasks" \
  -H "Authorization: ******" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": [
      "b8976e18-32dc-4718-9ed8-1ea090fcb6ea"
    ],
    "action": "retrieve_batch"
  }'
```
