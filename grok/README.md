# Grok API

xAI Grok generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Grok](https://platform.acedata.cloud/services/cbfe0ade-0b4e-4c42-83f4-3e2d5b429545?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_services_cbfe0ade_0b4e_4c42_83f4_3e2d5b429545)

Keywords: grok-api, xai-grok, grok-4.7, grok-4.5, grok-4, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Grok on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

xAI Grok is a powerful AI dialogue system known for its unique humorous style and real-time web information retrieval capabilities. The current flagship, `grok-4.7`, leads the lineup, with `grok-4.5`, `grok-4`, `grok-4-0709`, `grok-3`, and `grok-3-fast` also available. Grok supports multi-turn conversations, streaming responses, and a range of models suited for daily conversations, creative writing, technical analysis, and code debugging.

## Application Process

To use the Grok API, apply for the corresponding service on the [Grok Chat Completion API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_documents_faf08b59_36aa_4d26_b5d9_a18f113cc2be) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Grok on Ace Data Cloud](https://platform.acedata.cloud/services/cbfe0ade-0b4e-4c42-83f4-3e2d5b429545?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_services_cbfe0ade_0b4e_4c42_83f4_3e2d5b429545)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/grok/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "grok-4.5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Grok.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Grok Chat Completion API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=grok_api_readme_documents_faf08b59_36aa_4d26_b5d9_a18f113cc2be) | `/grok/chat/completions` | [Grok Chat Completion API Integration Guide](docs/grok_chat_completions_api_integration_guide.md) |
