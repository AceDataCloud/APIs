# Kimi API

Moonshot AI Kimi generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Kimi](https://platform.acedata.cloud/services/kimi?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_services_kimi)

Keywords: kimi-api, moonshot-ai, kimi-k3.1-pro, kimi-k3, kimi-k2, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Kimi on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Kimi is Moonshot AI's powerful AI dialogue system. The current flagship, `kimi-k3.1-pro`, supports reasoning, visual understanding, and tool calling. Its official context window is up to 1,048,576 tokens; actual request limits depend on the current API. `kimi-k3` and Kimi K2 models remain available for compatibility. K3.1 Pro always uses reasoning and supports the top-level `reasoning_effort` values `low`, `high`, and `max`; use `max` for K3.

## Application Process

To use the Kimi API, apply for the corresponding service on the [Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_documents_kimi_chat_completions) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Kimi on Ace Data Cloud](https://platform.acedata.cloud/services/kimi?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_services_kimi)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/kimi/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kimi-k3.1-pro",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Kimi.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kimi_api_readme_documents_kimi_chat_completions) | `/kimi/chat/completions` | [Kimi Chat Completion API Integration Guide](docs/kimi_chat_completions_api_integration_guide.md) |
