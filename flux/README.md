# FLUX API

Generate images from text and edit reference images through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/flux-images-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/flux?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/flux-images-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Find **General Application**. If it is missing, select **Initialize General Application**. Use the copy button marked **1** to copy its API key. Confirm service access and enough balance for your first request.

![General Application with the API key copy button marked 1 and Manage Keys marked 2](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

For a separate key, select **Manage Keys** (marked **2**) → **Create**. Enter a name for your integration, review optional usage limits, expiration and allowed APIs, then select **Create**. The screenshot uses an example name.

![Create New Credential with a name, optional restrictions and the Create button](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

3. Copy the raw key value and save it in your terminal environment. The HTTP examples add the `Bearer` prefix for you.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

[Step-by-step API key guide](https://platform.acedata.cloud/documents/api-key-guide?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Quickstart

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/flux/images \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "action": "generate",
  "model": "flux-2-klein",
  "prompt": "A blue ceramic coffee mug on a white table, soft morning light, product photograph",
  "size": "1024x1024"
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

Explore the supported endpoints and integration guides for Flux Image Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Flux Images Generation API](https://platform.acedata.cloud/documents/flux-images?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/flux/images` | [Flux Images Generation API Integration Guide](https://platform.acedata.cloud/documents/flux-images-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Flux Tasks API](https://platform.acedata.cloud/documents/flux-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/flux/tasks` | [Flux Tasks API Integration Guide](https://platform.acedata.cloud/documents/flux-tasks-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |

## FLUX 3 video generation

`POST /flux/videos` now supports `action="generate"` with `mode` set to `t2v`, `i2v`, `v2v`, or `draft_enhance`. Use `async=true`, retain the returned task ID, and poll `/flux/tasks`. Video editing and upscaling are not published.

Normal generation accepts `model="flux-3"`, `prompt`, `duration`, `resolution`, `draft`, and `generate_audio`; preserve explicit `false`. I2V additionally needs `keyframes`, V2V needs `start_video`, and draft enhancement needs an owned `draft_task_id`. See the [current video guide](https://platform.acedata.cloud/documents/flux-videos-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) for mode-specific limits and examples.

Flux AI image generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

![Flux Image Generation](https://cdn.acedata.cloud/cdfv2n.jpg)

API home page: [Ace Data Cloud - Flux Image Generation](https://platform.acedata.cloud/services/e8ebe055-429a-48e9-9d34-5089eae5fd89?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

Keywords: flux-api, ai-image, image-generation, black-forest-labs, rest-api, ai-api, aiimage, AI API, REST API, Developer API, Ace Data Cloud

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
