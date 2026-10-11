# AI Chat API

AI Dialogue service supporting a wide range of large language models for chat, multi-turn conversations, streaming responses, and image recognition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - AI Chat](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents_59fb1199_6694_4afb_a222_3554d7f7d05a)

Keywords: aichat-api, ai-dialogue, chat-api, multi-turn-conversation, gpt-4, grok, streaming, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Why Use AI Chat on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The AI Chat Conversations API enables you to send a question to a large language model and receive an answer. It supports a broad range of models (GPT-6, GPT-4o, Grok, Gemini, GLM, Kimi, and more), multi-turn stateful conversations, streaming responses, model presets, and image recognition via reference URLs — all without needing to manage message history or token limits yourself.

## Application Process

To use the AI Chat API, apply for the corresponding service on the [AI Chat API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents_59fb1199_6694_4afb_a222_3554d7f7d05a) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [AI Chat on Ace Data Cloud](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents_59fb1199_6694_4afb_a222_3554d7f7d05a)
- Docs: [Developer documentation](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents)

```bash
curl --request POST "https://api.acedata.cloud/aichat/conversations" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-4o",
    "question": "What is the capital of France?"
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for AI Chat.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [AI Chat Conversations API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents_59fb1199_6694_4afb_a222_3554d7f7d05a) | `/aichat/conversations` | [AI Chat Conversations API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |

## AI Chat v2 Execution Limits

[AI Chat v2](https://platform.acedata.cloud/documents/aichat2-conversations?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents_aichat2_conversations) supports agent tool calls. The following limits apply to v2, not the `/aichat/conversations` endpoint documented above.

| Endpoint | Optional field | Range | Default when omitted |
| --- | --- | --- | --- |
| `POST /aichat2/conversations` | `max_turns` | 1–500 | 500 |
| `POST /aichat2/scheduled-tasks` | `template.max_turns` | 1–500 | 500 |

Setting `max_turns` to `1` requests a single answer without tool calls. For scheduled tasks, `template.max_turns` limits agent turns per run, not scheduling frequency. Each model call is still billed for actual usage; 500 is an upper bound, and a run may end earlier due to timeout, authorization, or other execution conditions.

Repeated AI execution failures do not automatically pause a scheduled task: it will try again at the next scheduled time. Automatic pausing occurs after five consecutive failures to hand the task to the execution service. Insufficient balance marks a run as failed and triggers a recharge notification. An enabled task does not mean its latest run succeeded; check run history with `action: "retrieve_runs"` on `POST /aichat2/scheduled-tasks` for execution results.

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_platform)
- [Ace Data Cloud Docs](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_support) or browse the latest documentation on [docs.acedata.cloud](https://platform.acedata.cloud/documents?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_api_readme_documents)
