# HappyHorse API

Generate videos through Ace Data Cloud and retrieve the completed video by task ID.

[API documentation](https://docs.acedata.cloud/en/guides/happyhorse/happyhorse_videos) · [Models and pricing](https://platform.acedata.cloud/services/happyhorse?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/happyhorse/happyhorse_videos)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

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

Save the returned `task_id`. An accepted response has this shape.

```json
{"task_id":"YOUR_TASK_ID"}
```

Query that same task approximately every 10 seconds.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/happyhorse/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"YOUR_TASK_ID"}'
```

Continue until the task record has `finished_at`, then check `response.success`. On success, open `response.data[0].video_url`. If `response.success` is false, inspect `response.error` and keep the original task ID for support.

A completed result contains fields like these. The media URL below is illustrative.

```json
{
  "finished_at": 1790000000,
  "response": {
    "success": true,
    "data": [
      {
        "video_url": "https://media.example.com/result.mp4"
      }
    ]
  }
}
```

Keep polling the original task after a timeout or page reload. Submit again only when you intend to start a new generation.

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

- For authentication errors, check the copied API key, service access, expiration and configured usage limits. [API key guide](https://docs.acedata.cloud/en/authentication)
- For insufficient balance, open the application and review its balance and the current service price.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
