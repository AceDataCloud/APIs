# Producer Music Generation API

AI music generation service supporting songs, lyrics, covers, extensions, stem separation, WAV/MP4 export, and reference-audio uploads.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Producer Music Generation](https://platform.acedata.cloud/services/864a7efd-c7a3-4ad8-b372-ba8d64cdeda8?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_services_864a7efd_c7a3_4ad8_b372_ba8d64cdeda8)

Keywords: producer-api, ai-music, music-generation, song-generation, lyrics, cover, extend, stems, text-to-music, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Producer Music Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Producer Audios Generation API generates AI songs from a text `prompt` or custom `lyric`, with support for instrumental-only tracks, covers, extensions, and section replacement. The Producer Lyrics Generation API drafts lyrics from a prompt. The Producer Wav / Videos APIs export a finished track to WAV audio or MP4 video, the Upload API registers a reference audio for cover/extend, and the Tasks API polls asynchronous jobs.

## Application Process

To use the Producer Audios Generation API, apply for the corresponding service on the [Producer Audios Generation API](https://platform.acedata.cloud/documents/01d96900-9f8c-41d7-814c-95c7a885ba61?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents_01d96900_9f8c_41d7_814c_95c7a885ba61) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Producer Music Generation on Ace Data Cloud](https://platform.acedata.cloud/services/864a7efd-c7a3-4ad8-b372-ba8d64cdeda8?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_services_864a7efd_c7a3_4ad8_b372_ba8d64cdeda8)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/producer/audios" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "generate",
    "prompt": "upbeat electronic dance track with synth leads"
  }'
```

## Models

| Model | Notes |
| ---- | ---- |
| `FUZZ-2.0 Pro` | Default, highest quality |
| `FUZZ-2.0` | Standard quality |
| `FUZZ-2.0 Raw` | Raw output variant |
| `FUZZ-1.1 Pro` | Pro v1.1 |
| `FUZZ-1.0 Pro` | Pro v1.0 |
| `FUZZ-1.1` / `FUZZ-1.0` / `FUZZ-0.8` | Earlier versions |

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Producer Audios Generation API](https://platform.acedata.cloud/documents/01d96900-9f8c-41d7-814c-95c7a885ba61?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents_01d96900_9f8c_41d7_814c_95c7a885ba61) | `/producer/audios` | [Producer Audios Generation API Integration Guide](docs/producer_audios_generation_api_integration_guide.md) |
| [Producer Tasks API](https://platform.acedata.cloud/documents/e706d672-d7c9-4232-8652-0cf53219e7bf?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents_e706d672_d7c9_4232_8652_0cf53219e7bf) | `/producer/tasks` | [Producer Tasks API Integration Guide](docs/producer_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_platform)
- [Ace Data Cloud Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_support) or browse the latest documentation on [docs.acedata.cloud](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=producer_api_readme_documents)
