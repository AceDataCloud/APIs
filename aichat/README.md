# AI Chat API

AI Dialogue service supporting a wide range of large language models for chat, multi-turn conversations, streaming responses, image recognition, and next-generation agentic workflows.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - AI Chat](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a)

Keywords: aichat-api, ai-dialogue, chat-api, multi-turn-conversation, gpt-4, grok, streaming, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use AI Chat on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

AI Chat provides two conversation APIs. The classic [`/aichat/conversations`](https://platform.acedata.cloud/documents/aichat-conversations) endpoint offers a simplified chat workflow with built-in multi-turn context, streaming responses, model presets, and image recognition via reference URLs. The newer [`/aichat2/conversations`](https://platform.acedata.cloud/documents/aichat2-conversations) endpoint is backward compatible with the classic API while adding multimodal `message` input, structured streaming events, built-in tool invocation, asynchronous execution, and conversation CRUD actions.

## Application Process

To use the AI Chat API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API token.

A single API token works across services on the platform, so you do not need to apply separately for AI Chat. New accounts receive free starter credit, and you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Recommended endpoint: [`/aichat2/conversations`](https://platform.acedata.cloud/documents/aichat2-conversations)
- Classic endpoint: [`/aichat/conversations`](https://platform.acedata.cloud/documents/aichat-conversations)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/aichat2/conversations" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-5.4",
    "question": "Introduce AceDataCloud in one sentence."
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for AI Chat.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [AI Chat v2 API](https://platform.acedata.cloud/documents/aichat2-conversations) | `/aichat2/conversations` | [AI Chat v2 API Integration Guide](docs/aichat2_conversations_api_integration_guide.md) |
| [AI Chat Conversations API](https://platform.acedata.cloud/documents/aichat-conversations) | `/aichat/conversations` | [AI Chat Conversations API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
