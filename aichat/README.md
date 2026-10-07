# AI Chat API

AI Dialogue service supporting a wide range of large language models for chat, multi-turn conversations, streaming responses, and image recognition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - AI Chat](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a)

Keywords: aichat-api, ai-dialogue, chat-api, multi-turn-conversation, gpt-4, grok, streaming, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use AI Chat on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The AI Chat Conversations API enables you to send a question to a large language model and receive an answer. It supports a broad range of models (GPT-6, GPT-4o, Grok, Gemini, GLM, Kimi, and more), multi-turn stateful conversations, streaming responses, model presets, and image recognition via reference URLs — all without needing to manage message history or token limits yourself.

## Application Process

To use the AI Chat API, apply for the corresponding service on the [AI Chat API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [AI Chat on Ace Data Cloud](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a)
- Docs: [Developer documentation](https://docs.acedata.cloud)

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
| [AI Chat Conversations API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) | `/aichat/conversations` | [AI Chat Conversations API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |

## AI Chat v2 Execution Limits

[AI Chat v2](https://platform.acedata.cloud/documents/aichat2-conversations) supports agent tool calls. The following limits apply to v2, not the `/aichat/conversations` endpoint documented above.

| Endpoint | Optional field | Range | Default when omitted |
| --- | --- | --- | --- |
| `POST /aichat2/conversations` | `max_turns` | 1–500 | 500 |
| `POST /aichat2/scheduled-tasks` | `template.max_turns` | 1–500 | 500 |

Setting `max_turns` to `1` requests a single answer without tool calls. For scheduled tasks, `template.max_turns` limits agent turns per run, not scheduling frequency. Each model call is still billed for actual usage; 500 is an upper bound, and a run may end earlier due to timeout, authorization, or other execution conditions.

Repeated AI execution failures do not automatically pause a scheduled task: it will try again at the next scheduled time. Automatic pausing occurs after five consecutive failures to hand the task to the execution service. Insufficient balance marks a run as failed and triggers a recharge notification. An enabled task does not mean its latest run succeeded; check run history with `action: "retrieve_runs"` on `POST /aichat2/scheduled-tasks` for execution results.

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
