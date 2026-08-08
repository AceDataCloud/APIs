# Claude API

Anthropic Claude generative services, including chat completions, native messages, and token counting APIs.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Claude](https://platform.acedata.cloud/service/claude)

Keywords: claude-api, anthropic, claude-fable-5, claude-opus-5, claude-opus-4-8, claude-sonnet-5, claude-sonnet-4-6, claude-opus-4-7, claude-opus-4-6, claude-chat-completions, claude-messages, claude-count-tokens, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Claude on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Claude is Anthropic's AI assistant, offering powerful language understanding and generation. The current flagship `claude-fable-5` leads the lineup, alongside `claude-opus-5`, `claude-opus-4-8`, `claude-sonnet-5`, `claude-sonnet-4-6`, `claude-opus-4-7`, `claude-opus-4-6`, and `claude-haiku-4-5-20251001`. It supports OpenAI-compatible chat completions format as well as Anthropic's native messages API, with features including multi-turn dialogue, streaming responses, vision models, extended thinking, and token counting.

## Application Process

To use the Claude API, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

A single API Token works across every service on the platform. New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Claude on Ace Data Cloud](https://platform.acedata.cloud/service/claude)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/v1/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "claude-fable-5",
    "messages": [{"role": "user", "content": "Hello, Claude!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Claude.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Claude Chat Completion API](https://platform.acedata.cloud/documents/280928a2-2dce-419c-adb5-1ea835e8183a) | `/v1/chat/completions` | [Claude Chat Completion API Integration Guide](docs/claude_chat_completions_api_integration_guide.md) |
| [Claude Messages API](https://platform.acedata.cloud/documents/280928a2-2dce-419c-adb5-1ea835e8183a) | `/v1/messages` | [Claude Messages API Integration Guide](docs/claude_messages_api_integration_guide.md) |
| [Claude Messages Count Tokens API](https://platform.acedata.cloud/documents/claude-messages-count-tokens) | `/v1/messages/count_tokens` | [Claude Messages Count Tokens API Integration Guide](docs/claude_messages_count_tokens_api_integration_guide.md) |
