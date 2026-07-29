# AI Chat API

AI Dialogue service supporting a wide range of large language models for chat, multi-turn conversations, multimodal input, structured streaming, tool invocation, and image recognition.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home pages: [AI Chat API](https://platform.acedata.cloud/documents/aichat-conversations) · [AI Chat v2 API](https://platform.acedata.cloud/documents/aichat2-conversations)

Keywords: aichat-api, ai-dialogue, chat-api, multi-turn-conversation, gpt-4, grok, streaming, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use AI Chat on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Ace Data Cloud provides both the classic AI Chat API (`/aichat/conversations`) and the newer AI Chat v2 API (`/aichat2/conversations`). Both support simple question-answer chat, multi-turn stateful conversations, streaming responses, model presets, and image recognition. AI Chat v2 additionally adds multimodal `message` input, tool invocation, pause/resume flows, and lightweight conversation CRUD actions on the same endpoint.

## Application Process

To use the AI Chat APIs, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

A single API Token works across Ace Data Cloud services, so you do not need to apply separately for AI Chat. New accounts receive free starter credit, and you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin) when needed.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service pages: [AI Chat API](https://platform.acedata.cloud/documents/aichat-conversations) · [AI Chat v2 API](https://platform.acedata.cloud/documents/aichat2-conversations)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/aichat2/conversations" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-4o",
    "question": "Introduce AceDataCloud in one sentence."
  }'
```

For legacy integrations, `/aichat/conversations` remains available and is documented below alongside the newer `/aichat2/conversations` endpoint.

## APIs and Guides

Explore the supported endpoints and integration guides for AI Chat.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [AI Chat v2 API](https://platform.acedata.cloud/documents/aichat2-conversations) | `/aichat2/conversations` | [AI Chat v2 API Integration Guide](docs/aichat2_conversations_api_integration_guide.md) |
| [AI Chat API](https://platform.acedata.cloud/documents/aichat-conversations) | `/aichat/conversations` | [AI Chat Conversations API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
