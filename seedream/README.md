# Seedream Image Generation API

ByteDance Seedream AI image generation & editing service.

API home page: [Ace Data Cloud - Seedream Image Generation](https://platform.acedata.cloud/services/a0a296f0-22de-422b-943d-1c623a73b8dd?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_services_a0a296f0_22de_422b_943d_1c623a73b8dd)

Keywords: seedream-api, ai-image, image-generation, image-editing, bytedance, doubao, seededit, text-to-image, rest-api, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Overview

The Seedream Images API generates, edits, streams, and decomposes images with `doubao-seedream-4-0-250828`, `doubao-seedream-4-5-251128`, `doubao-seedream-5-0-lite-260128`, and `doubao-seedream-5-0-pro-260628`. The Seedream Tasks API queries async task status.

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/seedream/images" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"model": "doubao-seedream-5-0-lite-260128", "prompt": "a serene mountain lake at sunrise, photorealistic", "size": "2K"}'
```

## Models

| Model | Notes |
| ---- | ---- |
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

## APIs and Guides

| API | Path | Guide |
| ---- | ---- | ---- |
| [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_documents_86ad30f3_0bc8_4b9b_b019_b9fa5b05672e) | `/seedream/images` | [Integration Guide](docs/seedream_images_generation_api_integration_guide.md) |
| [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_documents_a89ab5c9_f956_42b5_a867_abb3d00d2f75) | `/seedream/tasks` | [Integration Guide](docs/seedream_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_platform)
- [Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=seedream_api_readme_documents) · [Status](https://status.acedata.cloud) · [GitHub Org](https://github.com/AceDataCloud)
