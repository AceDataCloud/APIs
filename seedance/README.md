# Seedance API

Generate videos through Ace Data Cloud and retrieve the completed video by task ID.

[API documentation](https://docs.acedata.cloud/en/guides/seedance/seedance_videos) · [Models and pricing](https://platform.acedata.cloud/services/seedance?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/seedance/seedance_videos)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/seedance/videos \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "doubao-seedance-2-5-260628",
  "content": [
    {
      "type": "text",
      "text": "A sailboat crossing a calm lake at sunrise, slow camera pan"
    }
  ],
  "duration": 5,
  "resolution": "720p",
  "async": true
}'
```

Save the returned `task_id`. An accepted response has this shape.

```json
{"task_id":"YOUR_TASK_ID"}
```

Query that same task approximately every 10 seconds.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/seedance/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"YOUR_TASK_ID"}'
```

Continue until the task record has `finished_at`, then check `response.success`. On success, open `response.data.content.video_url`. If `response.success` is false, inspect `response.error` and keep the original task ID for support.

A completed result contains fields like these. The media URL below is illustrative.

```json
{
  "finished_at": 1790000000,
  "response": {
    "success": true,
    "data": {
      "content": {
        "video_url": "https://media.example.com/result.mp4"
      }
    }
  }
}
```

Keep polling the original task after a timeout or page reload. Submit again only when you intend to start a new generation.

## Models

| Model | Generation | Notes |
| ---- | ---- | ---- |
| `doubao-seedance-2-5-260628` | 2.5 | Latest flagship, up to 30s, pure-audio/multimodal reference, edit/extend |
| `doubao-seedance-2-5-260628` | 2.5 | Up to 1080p/30s, pure-audio reference, edit/extend |
| `doubao-seedance-2-0-260128` | 2.0 | Highest resolution, multimodal reference, up to 4k |
| `doubao-seedance-2-0-fast-260128` | 2.0 Fast | Faster 2.0, up to 720p |
| `doubao-seedance-2-0-mini-260615` | 2.0 Mini | Lightweight / most cost-effective 2.0, up to 720p |
| `doubao-seedance-1-5-pro-251215` | 1.5 Pro | Supports audio generation |
| `doubao-seedance-1-0-pro-250528` | 1.0 Pro | Standard quality |
| `doubao-seedance-1-0-pro-fast-251015` | 1.0 Fast | Faster generation |
| `doubao-seedance-1-0-lite-t2v-250428` | 1.0 Lite T2V | Lightweight text-to-video |
| `doubao-seedance-1-0-lite-i2v-250428` | 1.0 Lite I2V | Lightweight image-to-video |

## APIs and Guides

Explore the supported endpoints and integration guides for Seedance Video Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedance/videos` | [Seedance Videos Generation API Integration Guide](docs/seedance_videos_generation_api_integration_guide.md) |
| [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedance/tasks` | [Seedance Tasks API Integration Guide](docs/seedance_tasks_api_integration_guide.md) |

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
