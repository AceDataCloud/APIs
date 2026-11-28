# HappyHorse API

Generate videos through Ace Data Cloud and retrieve the completed video by task ID.

[API documentation](https://platform.acedata.cloud/documents/happyhorse-videos-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/happyhorse?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/happyhorse-videos-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Store the copied key in the `ACEDATACLOUD_API_KEY` environment variable on your server. Replace `YOUR_API_KEY` below with the copied value. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

### Submit a request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/happyhorse/videos \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "generate",
  "model": "happyhorse-1.1-t2v",
  "prompt": "A sailboat crossing a calm lake at sunrise, slow camera pan",
  "duration": 5,
  "resolution": "720P",
  "async": true
}'
```

### Submission response JSON

The following JSON examples illustrate the documented fields. IDs, timestamps and output URLs are placeholders. Use the values returned by your own request.

```json
{
  "task_id": "TASK_ID"
}
```

Save `task_id` and query that same task.

### Query the task

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/happyhorse/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"TASK_ID"}'
```

### Processing response JSON

```json
{
  "id": "TASK_ID",
  "type": "videos",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A sailboat crossing a calm lake at sunrise, slow camera pan",
    "duration": 5,
    "resolution": "720P",
    "async": true
  },
  "finished_at": null
}
```

Query again after a few seconds while processing continues.

### Completed response JSON

```json
{
  "id": "TASK_ID",
  "type": "videos",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A sailboat crossing a calm lake at sunrise, slow camera pan",
    "duration": 5,
    "resolution": "720P",
    "async": true
  },
  "finished_at": 1790000045,
  "elapsed": 45,
  "response": {
    "success": true,
    "task_id": "TASK_ID",
    "trace_id": "TRACE_ID",
    "data": [
      {
        "id": "VIDEO_ID",
        "video_url": "https://media.example.com/result.mp4",
        "state": "succeeded"
      }
    ]
  }
}
```

Continue while `finished_at` is null or absent. When the task finishes, inspect `response.success` and the result state. On success, open `response.data[0].video_url`. On failure, inspect `response.error` and retain the original task ID for support.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

## APIs and Guides

| API | Path | Integration guide |
|---|---|---|
| [Happy Horse Videos API](https://platform.acedata.cloud/documents/happyhorse-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/happyhorse/videos` | [Videos API Integration Guide](docs/happyhorse_videos_api_integration_guide.md) |
| [Happy Horse Tasks API](https://platform.acedata.cloud/documents/happyhorse-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/happyhorse/tasks` | [Tasks API Integration Guide](docs/happyhorse_tasks_api_integration_guide.md) |

## Agent Integrations

- MCP package: [`mcp-happyhorse`](https://pypi.org/project/mcp-happyhorse/)
- Hosted MCP: `https://happyhorse.mcp.acedata.cloud/mcp`
- Agent Skill: [`happyhorse-video`](https://github.com/AceDataCloud/Skills/tree/main/skills/happyhorse-video)

## Troubleshooting

- For authentication errors, open [Manage Keys](https://platform.acedata.cloud/console/credentials?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) to check the key’s allowed APIs, expiration and usage limit.
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
