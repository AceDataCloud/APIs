# Seedance API

Generate videos through Ace Data Cloud and retrieve the completed video by task ID.

[API documentation](https://platform.acedata.cloud/documents/seedance-videos-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/seedance?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/seedance-videos-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. If needed, select **Initialize General Application** first. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

### Submit a request

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
curl --fail-with-body --silent --show-error https://api.acedata.cloud/seedance/tasks \
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
  },
  "finished_at": 1790000045,
  "elapsed": 45,
  "response": {
    "success": true,
    "task_id": "TASK_ID",
    "trace_id": "TRACE_ID",
    "data": {
      "id": "VIDEO_ID",
      "model": "doubao-seedance-2-5-260628",
      "status": "succeeded",
      "content": {
        "video_url": "https://media.example.com/result.mp4"
      },
      "resolution": "720p",
      "duration": 5
    }
  }
}
```

Continue while `finished_at` is null or absent. When the task finishes, inspect `response.success` and the result state. On success, read `response.data.content.video_url` or `response.data.video_url`, depending on the returned result. In JavaScript use `response.data.content?.video_url ?? response.data.video_url`. On failure, inspect `response.error` and retain the original task ID for support.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

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
| [Seedance Videos Generation API](https://platform.acedata.cloud/documents/seedance-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedance/videos` | [Seedance Videos Generation API Integration Guide](docs/seedance_videos_generation_api_integration_guide.md) |
| [Seedance Tasks API](https://platform.acedata.cloud/documents/seedance-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedance/tasks` | [Seedance Tasks API Integration Guide](docs/seedance_tasks_api_integration_guide.md) |

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
