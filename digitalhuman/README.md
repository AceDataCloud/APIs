# Digital Human API

Create a talking-person video from a portrait and speech audio through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/api-reference/digitalhuman/digital-human-videos) · [Models and pricing](https://platform.acedata.cloud/services/digitalhuman?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/5ced04db-8d92-4a6b-b988-91423dcc1f02?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

Replace the two URLs with an accessible, clear portrait and speech audio that you have permission to use. Keep both files reachable while the task runs.

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

Save the returned `task_id`. An accepted response has this shape.

```json
{"task_id":"YOUR_TASK_ID"}
```

Query that same task approximately every 10 seconds.

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/digital-human/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"YOUR_TASK_ID"}'
```

The detailed task response includes `status`, `finished_at` and `response`. Continue until `finished_at` is set, then inspect `response.success`. On success, open `response.video_url`. On failure, inspect the returned error and keep the original task ID for support.

A completed result contains fields like these. The media URL below is illustrative.

```json
{
  "finished_at": 1790000000,
  "response": {
    "success": true,
    "video_url": "https://media.example.com/result.mp4"
  }
}
```

Keep polling the original task after a timeout or page reload. Submit again only when you intend to start a new generation.

## API reference

- [`/digital-human/videos`](https://platform.acedata.cloud/documents/5ced04db-8d92-4a6b-b988-91423dcc1f02?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/digital-human/voices`](https://platform.acedata.cloud/documents/c334172a-a0b1-451f-8137-d9c9830a15b9?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/digital-human/tasks`](https://platform.acedata.cloud/documents/74bb973d-939a-4a6e-89f4-1667deb8ea3b?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
