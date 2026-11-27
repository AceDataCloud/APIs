# ACE Music API

Create songs from a short description or your own lyrics through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/acemusic-audios-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/acemusic?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/acemusic-audios-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

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
curl --fail-with-body --silent --show-error https://api.acedata.cloud/acemusic/audios \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "generate",
  "model": "acemusic-v1.1",
  "custom": false,
  "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
  "async": true
}'
```

### Submission response JSON

The following JSON examples illustrate the documented fields. IDs, timestamps and output URLs are placeholders. Use the values returned by your own request.

```json
{
  "task_id": "TASK_ID",
  "trace_id": "TRACE_ID",
  "status": "created"
}
```

Save `task_id` and query that same task.

### Query the task

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/acemusic/tasks \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{"action":"retrieve","id":"TASK_ID"}'
```

### Processing response JSON

```json
{
  "id": "TASK_ID",
  "type": "audios",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "acemusic-v1.1",
    "custom": false,
    "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
    "async": true
  },
  "finished_at": null,
  "state": "processing"
}
```

Query again after a few seconds while processing continues.

### Completed response JSON

```json
{
  "id": "TASK_ID",
  "type": "audios",
  "created_at": 1790000000,
  "trace_id": "TRACE_ID",
  "request": {
    "action": "generate",
    "model": "acemusic-v1.1",
    "custom": false,
    "prompt": "An uplifting acoustic folk song about a new beginning, with warm vocals",
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
        "id": "AUDIO_ID_1",
        "model": "acemusic-v1.1",
        "state": "succeeded",
        "title": "A New Beginning",
        "audio_url": "https://media.example.com/song-1.mp3"
      },
      {
        "id": "AUDIO_ID_2",
        "model": "acemusic-v1.1",
        "state": "succeeded",
        "title": "A New Beginning",
        "audio_url": "https://media.example.com/song-2.mp3"
      }
    ],
    "status": "succeeded"
  },
  "state": "succeeded"
}
```

Continue while `state` is processing. Stop on `succeeded`, `failed`, or `partial_failed`. For a successful two-song group, read `response.data[*].audio_url`. On failure inspect `response.error`.

Keep querying the original task after a timeout or page reload. Submit again when you intend to start another generation.

## API reference

- [`/acemusic/audios`](https://platform.acedata.cloud/documents/acemusic-audios?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/acemusic/lyrics`](https://platform.acedata.cloud/documents/acemusic-lyrics?utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [`/acemusic/tasks`](https://platform.acedata.cloud/documents/acemusic-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## More examples and integrations

- [Song generation, upload, cover and mashup](https://platform.acedata.cloud/documents/acemusic-audios-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
- [Lyrics](https://platform.acedata.cloud/documents/acemusic-lyrics-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Task retrieval](https://platform.acedata.cloud/documents/acemusic-tasks-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [OpenAPI](openapi.json)
- [SDKs](https://github.com/AceDataCloud/SDK) · [CLI](https://pypi.org/project/acemusic-cli/) · [MCP and integrations](https://github.com/AceDataCloud/AceMusicMCP)

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
