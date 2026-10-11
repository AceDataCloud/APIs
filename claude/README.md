# Claude API

Anthropic Claude generative services, including chat completions and native messages API.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Claude](https://platform.acedata.cloud/services/fa3cba27-b01c-4657-942f-63589f727b00?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_services_fa3cba27_b01c_4657_942f_63589f727b00)

Keywords: claude-api, anthropic, claude-opus-5-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-opus-4-8, claude-sonnet-5, claude-chat-completions, claude-messages, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use Claude on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Claude is Anthropic's AI assistant, offering powerful language understanding and generation. `claude-opus-5-5` is available through the native Messages API with a 1M-token context window and up to 128K output tokens. The current flagship `claude-fable-5-1` provides a 1M-token context window and up to 128K output tokens. The earlier `claude-fable-5` remains available alongside `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5`, and `claude-haiku-4-5-20251001`. It supports OpenAI-compatible chat completions format as well as Anthropic's native messages API, with features including multi-turn dialogue, streaming responses, vision models, and extended thinking.

## Application Process

To use the Claude API, apply for the corresponding service on the [Claude Chat Completion API](https://platform.acedata.cloud/documents/280928a2-2dce-419c-adb5-1ea835e8183a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_documents_280928a2_2dce_419c_adb5_1ea835e8183a) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Claude on Ace Data Cloud](https://platform.acedata.cloud/services/fa3cba27-b01c-4657-942f-63589f727b00?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_services_fa3cba27_b01c_4657_942f_63589f727b00)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "claude-fable-5-1",
    "messages": [{"role": "user", "content": "Hello, Claude!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Claude.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Claude Chat Completion API](https://platform.acedata.cloud/documents/280928a2-2dce-419c-adb5-1ea835e8183a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_documents_280928a2_2dce_419c_adb5_1ea835e8183a) | `/v1/chat/completions` | [Claude Chat Completion API Integration Guide](docs/claude_chat_completions_api_integration_guide.md) |
| [Claude Messages API](https://platform.acedata.cloud/documents/280928a2-2dce-419c-adb5-1ea835e8183a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_documents_280928a2_2dce_419c_adb5_1ea835e8183a) | `/v1/messages` | [Claude Messages API Integration Guide](docs/claude_messages_api_integration_guide.md) |
| [Claude Messages Count Tokens API](https://platform.acedata.cloud/documents/claude-messages-count-tokens?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=claude_api_readme_documents_claude_messages_count_tokens) | `/v1/messages/count_tokens` | [Claude Messages Count Tokens API Integration Guide](docs/claude_messages_count_tokens_api_integration_guide.md) |
