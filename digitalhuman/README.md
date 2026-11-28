# Digital Human API

Create a talking-person video from a portrait and speech audio through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/digitalhuman-videos?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/digitalhuman?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/digitalhuman-videos?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application** and click the copy button marked **1**. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Save the copied key in your terminal. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Replace the two URLs with an accessible, clear portrait and speech audio that you have permission to use. Keep both files reachable while the task runs.

### Submit a request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/digital-human/videos \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "image_url": "https://YOUR_PORTRAIT_IMAGE",
  "audio_url": "https://YOUR_SPEECH_AUDIO",
  "async": true
}'
```

### Submission response JSON

The following JSON examples illustrate the documented fields. IDs, timestamps and output URLs are placeholders. Use the values returned by your own request.

```json
{
  "success": true,
  "task_id": "TASK_ID",
  "trace_id": "TRACE_ID",
  "state": "pending"
}
```

Save `task_id` and query that same task.

### Query the task

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/digital-human/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"TASK_ID"}'
```

### Processing response JSON

```json
{
  "id": "TASK_ID",
  "status": "running",
  "kind": "video",
  "created_at": 1790000000,
  "started_at": 1790000001,
  "finished_at": null,
  "elapsed": null,
  "request": {
    "image_url": "https://YOUR_PORTRAIT_IMAGE",
    "audio_url": "https://YOUR_SPEECH_AUDIO",
    "async": true
  },
  "response": {
    "success": true,
    "task_id": "TASK_ID",
    "trace_id": "TRACE_ID",
    "state": "running",
    "progress": 20
  }
}
```

Query again after a few seconds while processing continues.

### Completed response JSON

```json
{
  "id": "TASK_ID",
  "status": "succeed",
  "kind": "video",
  "created_at": 1790000000,
  "started_at": 1790000001,
  "finished_at": 1790000045,
  "elapsed": 44,
  "request": {
    "image_url": "https://YOUR_PORTRAIT_IMAGE",
    "audio_url": "https://YOUR_SPEECH_AUDIO",
    "async": true
  },
  "response": {
    "success": true,
    "task_id": "TASK_ID",
    "trace_id": "TRACE_ID",
    "video_url": "https://media.example.com/result.mp4",
    "state": "succeed",
    "progress": 100,
    "duration": 5,
    "width": 1280,
    "height": 720
  }
}
```

For this detailed `retrieve` response, wait for `response.state` to become `succeed` or `failed`. A successful query can have `response.success=true` while video processing is still running. On completion read `response.video_url`; on failure read `response.error`.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

## API reference

- [`/digital-human/videos`](https://platform.acedata.cloud/documents/digitalhuman-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/digital-human/voices`](https://platform.acedata.cloud/documents/digitalhuman-voices?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/digital-human/tasks`](https://platform.acedata.cloud/documents/digitalhuman-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Troubleshooting

- For authentication errors, open [Manage Keys](https://platform.acedata.cloud/console/credentials?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) to check the key’s allowed APIs, expiration and usage limit.
- If the application balance is insufficient, click **Top Up** on its card.
- For request validation errors, compare the model and required fields with the linked API reference.
- For a long-running or failed task, retain `task_id` and `trace_id` when contacting [support](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen).

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage.
