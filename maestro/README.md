# Maestro API

Generate videos through Ace Data Cloud and retrieve the completed video by task ID.

[API documentation](https://platform.acedata.cloud/documents/maestro-videos-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/maestro?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/maestro-videos-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. If needed, select **Initialize General Application** first. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

[API key help](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Quickstart

### Submit a request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/maestro/videos \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "prompt": "Create a 10-second explainer about how rainbows form, with English narration.",
  "duration": 10
}'
```

### Submission response JSON

The following JSON examples illustrate the documented fields. IDs, timestamps and output URLs are placeholders. Use the values returned by your own request.

```json
{
  "success": true,
  "task_id": "TASK_ID",
  "trace_id": "TRACE_ID"
}
```

Save `task_id` and query that same task.

### Query the task

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/maestro/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"TASK_ID"}'
```

### Processing response JSON

```json
{
  "id": "TASK_ID",
  "trace_id": "TRACE_ID",
  "status": "producing",
  "created_at": 1790000000,
  "progress": {
    "percent": 20,
    "stage": "producing"
  },
  "request": {
    "prompt": "Create a 10-second explainer about how rainbows form, with English narration.",
    "duration": 10
  }
}
```

Query again after a few seconds while processing continues.

### Completed response JSON

```json
{
  "id": "TASK_ID",
  "trace_id": "TRACE_ID",
  "status": "succeeded",
  "created_at": 1790000000,
  "progress": {
    "percent": 100,
    "stage": "producing"
  },
  "request": {
    "prompt": "Create a 10-second explainer about how rainbows form, with English narration.",
    "duration": 10
  },
  "elapsed": 45,
  "response": {
    "success": true,
    "data": {
      "variants": [
        {
          "lang": "en",
          "kind": "video",
          "output_url": "https://media.example.com/result.mp4"
        }
      ]
    }
  }
}
```

Stop when `status` is `succeeded` or `failed`. On success, open `response.data.variants[0].output_url`. Inspect `response.error` on failure.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

## APIs and Guides

| API | Path | Integration Guide |
|---|---|---|
| [Maestro Videos API](https://platform.acedata.cloud/documents/maestro-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `POST /maestro/videos` | [Video production guide](docs/maestro_videos_api_integration_guide.md) |
| [Maestro Tasks API](https://platform.acedata.cloud/documents/maestro-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `POST /maestro/tasks` | [Task retrieval guide](docs/maestro_tasks_api_integration_guide.md) |

## Troubleshooting

- For authentication errors, check the copied API key, service access, expiration and configured usage limits. [API key guide](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
