# Seedream API

Generate images from text and edit reference images through Ace Data Cloud.

[API documentation](https://platform.acedata.cloud/documents/seedream-images-integration?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Models and pricing](https://platform.acedata.cloud/services/seedream?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [中文文档](https://platform.acedata.cloud/documents/seedream-images-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Get an API key

1. Open [Applications](https://platform.acedata.cloud/console/applications?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen) and sign in or register.
2. Open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Confirm access to this service and enough balance for your request.

![Copy the API key from General Application using the button marked 1](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

3. Store the copied key in the `ACEDATACLOUD_API_KEY` environment variable on your server. Replace `YOUR_API_KEY` below with the copied value. The examples add the `Bearer` prefix in the HTTP header.

```bash
export ACEDATACLOUD_API_KEY='YOUR_API_KEY'
```

## Quickstart

### Request

```bash
curl --fail-with-body --silent --show-error https://api.acedata.cloud/seedream/images \
  --header "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "doubao-seedream-5-5-261028",
  "prompt": "A blue ceramic coffee mug on a white table, soft morning light, product photograph",
  "size": "2K"
}'
```

### Response JSON

Illustrative response with placeholder identifiers and output values.

```json
{
  "success": true,
  "task_id": "TASK_ID",
  "trace_id": "TRACE_ID",
  "data": [
    {
      "image_url": "https://media.example.com/image.png",
      "prompt": "A blue ceramic coffee mug on a white table, soft morning light, product photograph"
    }
  ]
}
```

Open or download `data[0].image_url` returned by your request.

## APIs and Guides

| API | Path | Guide |
| ---- | ---- | ---- |
| [Seedream Images API](https://platform.acedata.cloud/documents/seedream-images?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedream/images` | [Integration Guide](docs/seedream_images_generation_api_integration_guide.md) |
| [Seedream Tasks API](https://platform.acedata.cloud/documents/seedream-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen) | `/seedream/tasks` | [Integration Guide](docs/seedream_tasks_api_integration_guide.md) |

## Models

| Model | Notes |
| ---- | ---- |
| `doubao-seedream-5-5-261028` | Multi-turn editing, native transparent PNG, up to 99 editable layers and optional OCR; 1K/1.5K/2K |
| `doubao-seedream-5-0-flash-260915` | Fast single-image generation and editing, up to 16 editable layers; 1K/1.5K/2K |
| `doubao-seedream-5-0-pro-260628` | Single image, precise editing, transparent background, layer decomposition; 1K/1.5K/2K |
| `doubao-seedream-5-0-lite-260128` | Sequential images, streaming, web search; 2K/3K/4K |
| `doubao-seedream-4-5-251128` | 4.5 |
| `doubao-seedream-4-0-250828` | 4.0 |

## Key 5.0 operations

- Generate/edit: `prompt`, optional `image`, model-specific `size`, `output_format`, and prompt optimization.
- Lite image sets: `sequential_image_generation: "auto"` plus `max_images`; input + output ≤ 15.
- Pro transparent edit: one transparent PNG, `background: "transparent"`, `output_format: "png"`.
- Pro layers: one PNG/JPEG, `layer_decomposition: true`; returns a base plus up to 16 positioned PNG layers.
- Lite streaming: `stream: true` with `Accept: application/x-ndjson`; do not combine with async/callback.

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
