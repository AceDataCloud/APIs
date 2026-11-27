# Nano Banana API

Generate images from text and edit reference images through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/nano-banana/nanobanana_images) · [Models and pricing](https://platform.acedata.cloud/services/nano-banana?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/nano-banana/nanobanana_images)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/nano-banana/images \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "generate",
  "model": "nano-banana-2.1",
  "prompt": "A blue ceramic coffee mug on a white table, soft morning light, product photograph",
  "count": 1
}'
```

Read `data[0].image_url` from the response. The following fields illustrate a successful result and media URLs are placeholders.

```json
{
  "success": true,
  "data": [
    {
      "image_url": "https://media.example.com/image.png"
    }
  ]
}
```

Open or download the URL returned by your own request.

## APIs and Guides

Explore the supported endpoints and integration guides for Nano Banana Image Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Nano Banana Images API](https://platform.acedata.cloud/documents/23985a11-d713-41d1-ad84-24b021805b3d?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/nano-banana/images` | [Nano Banana Images API Integration Guide](https://platform.acedata.cloud/documents/2fb479f8-63ec-424c-a93e-b12cd4250f9e?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [$t(document_title_nanobanana_tasks_api)](https://platform.acedata.cloud/documents/617810f5-081f-4866-a21a-cededecb0ccd?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/nano-banana/tasks` | [Nano Banana Tasks API Integration Guide](https://platform.acedata.cloud/documents/e01ef840-3158-4eec-a6e7-337dada8d155?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |

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
