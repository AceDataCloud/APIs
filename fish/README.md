# Fish Voice Generation API

Fish Audio text-to-speech and voice-cloning service: synthesize speech from text and create custom voice models from reference audio.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Voice Generation](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_services_caf99abc_ddcf_4714_b2a5_862d9b469509)

Keywords: fish-api, fish-audio, text-to-speech, tts, voice-clone, voice-model, speech-synthesis, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Fish Voice Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Fish TTS API converts text into natural speech using a saved voice model or a one-shot HTTPS reference audio sample. The Fish Model APIs create, query, and fetch custom voice models from reference audio, and the Fish Tasks API polls asynchronous jobs.

## Application Process

To use the Fish TTS API, apply for the corresponding service on the [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_77adcb84_d59f_5ef9_b8a0_8b35eb42a71d) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Voice Generation on Ace Data Cloud](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_services_caf99abc_ddcf_4714_b2a5_862d9b469509)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "text": "Hello, this is a demonstration of AI voice synthesis."
  }'
```

### One-shot voice clone

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2-pro" \
  --data '{
    "text": "New speech in the referenced voice.",
    "format": "mp3",
    "references": [{
      "audio": "https://cdn.acedata.cloud/reference.mp3",
      "text": "The exact reference transcript."
    }]
  }'
```

This conditions only the current request. Use `reference_id` for a saved/public voice; never combine it with `references`.

### Create a reusable public voice

`POST /fish/model` saves a cloned voice long-term and publicly: other users may search for and use it. Omit `visibility`; passing `private` or `unlist` does not make the voice private. Only submit reference audio you have permission to process and publish as a reusable voice.

Send `voices` as one publicly downloadable HTTP(S) audio URL string, not an array or multipart upload. Prefer a direct URL ending in `.mp3` or `.wav`. Replace the example URL with your authorized audio before calling:

```bash
curl --request POST "https://api.acedata.cloud/fish/model" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "title": "My public voice",
    "voices": "https://example.com/sample-voice.mp3"
  }'
```

Successful creation returns HTTP **201** with the voice model object. Retain its `_id` and pass it as `reference_id` to `/fish/tts`. For HTTP 400 caused by a reference-audio download, duration, or format error, check the URL and actual file format.

### List voices created by your account

```bash
curl --get "https://api.acedata.cloud/fish/model" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --data-urlencode "self=true" \
  --data-urlencode "page_number=1" \
  --data-urlencode "page_size=5"
```

`self=true` lists voices created and saved through Ace Data Cloud by the calling account, including voices created with different API tokens belonging to that account. It filters the list only; the voices remain publicly usable. Results default to newest-created first with 1-based pagination. `author_id` can further filter the author; `sort_by` supports `created_at` and `task_count` in this mode.

Do not combine `title_language` with `self=true`; title-language filtering applies to the public voice library instead. The response contains `total`, `items`, and `has_more`: `has_more` is a boolean for `self=true`, but may be `null` for public-library queries. Treat `null` as an unspecified pagination signal, not an explicit end-of-list.

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_77adcb84_d59f_5ef9_b8a0_8b35eb42a71d) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/fc541fac-a941-47fd-b6f7-48d6cb9da523?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_fc541fac_a941_47fd_b6f7_48d6cb9da523) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |
| [Fish Model Create API](https://platform.acedata.cloud/documents/82dcabe9-b1a3-541f-80f1-decb183b920c?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_82dcabe9_b1a3_541f_80f1_decb183b920c) | `/fish/model` | Create a custom voice model from reference audio |
| [Fish Model Query API](https://platform.acedata.cloud/documents/0a2c983b-e20f-5926-a45f-07b61373617d?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_0a2c983b_e20f_5926_a45f_07b61373617d) | `/fish/model` | List voice models |
| [Fish Model Get API](https://platform.acedata.cloud/documents/70f84537-7c48-57d3-9a21-b2a4f55e8f31?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents_70f84537_7c48_57d3_9a21_b2a4f55e8f31) | `/fish/model/{id}` | Fetch a single voice model |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_platform)
- [Ace Data Cloud Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_support) or browse the latest documentation on [docs.acedata.cloud](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_api_readme_documents)
