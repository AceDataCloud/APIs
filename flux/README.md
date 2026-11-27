# FLUX API

Generate images from text and edit reference images through Ace Data Cloud.

[API documentation](https://docs.acedata.cloud/en/guides/flux/flux_images) · [Models and pricing](https://platform.acedata.cloud/services/flux?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://docs.acedata.cloud/zh-Hans/guides/flux/flux_images)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or create an account.
2. Open **General application**. If it is missing, select **Initialize General Application**. Copy its **API Key**, or create a separate key in **Manage Keys**. Confirm access to this service and enough balance for the request.
3. Save the raw key in your terminal environment.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

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
| [Flux Images Generation API](https://platform.acedata.cloud/documents/6b9197c5-7a3f-4878-a43f-7f94e7e66394?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/flux/images` | [Flux Images Generation API Integration Guide](https://platform.acedata.cloud/documents/92754994-3970-4f2a-9bf3-113149c25c11?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |
| [Flux Tasks API](https://platform.acedata.cloud/documents/39b38bbe-60f3-40da-b2b6-5ce1e091852b?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/flux/tasks` | [Flux Tasks API Integration Guide](https://platform.acedata.cloud/documents/5998d153-b9a6-4798-b5d9-8f523d0d626f?utm_source=github&utm_medium=referral&utm_campaign=evergreen) |

## FLUX 3 video generation

`POST /flux/videos` now supports `action="generate"` with `mode` set to `t2v`, `i2v`, `v2v`, or `draft_enhance`. Use `async=true`, retain the returned task ID, and poll `/flux/tasks`. Video editing and upscaling are not published.

Normal generation accepts `model="flux-3"`, `prompt`, `duration`, `resolution`, `draft`, and `generate_audio`; preserve explicit `false`. I2V additionally needs `keyframes`, V2V needs `start_video`, and draft enhancement needs an owned `draft_task_id`. See the [current video guide](https://platform.acedata.cloud/documents/flux-videos-integration?utm_source=github&utm_medium=referral&utm_campaign=evergreen) for mode-specific limits and examples.

Flux AI image generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

![Flux Image Generation](https://cdn.acedata.cloud/cdfv2n.jpg)

API home page: [Ace Data Cloud - Flux Image Generation](https://platform.acedata.cloud/services/e8ebe055-429a-48e9-9d34-5089eae5fd89?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

Keywords: flux-api, ai-image, image-generation, black-forest-labs, rest-api, ai-api, aiimage, AI API, REST API, Developer API, Ace Data Cloud

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
