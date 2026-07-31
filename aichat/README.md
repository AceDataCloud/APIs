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

The AI Chat Conversations API enables you to send a question to a large language model and receive an answer. It supports a broad range of models (GPT-4, GPT-4o, Grok, GLM, Kimi, and more), multi-turn stateful conversations, streaming responses, model presets, and image recognition via reference URLs — all without needing to manage message history or token limits yourself.

## Application Process

To use the APIs in this service, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

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

Explore the supported endpoints and integration guides for AI Dialogue.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [AI Chat v2 API Integration Instructions](https://platform.acedata.cloud/documents/aichat-conversations) | `/aichat2/conversations` | [AI Chat v2 API Integration Instructions](docs/aichat2_conversations_api_integration_guide.md) |
| [AI Chat API Integration Instructions](https://platform.acedata.cloud/documents/aichat-conversations) | `/aichat/conversations` | [AI Chat API Integration Instructions](docs/aichat_conversations_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
