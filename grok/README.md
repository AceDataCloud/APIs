# Grok API

xAI Grok generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Grok](https://platform.acedata.cloud/service/grok)

Keywords: grok-api, xai-grok, grok-4.5, grok-4, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Grok on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

xAI Grok is a powerful AI dialogue system known for its unique humorous style and real-time web information retrieval capabilities. The current flagship, `grok-4.5`, leads the lineup, with `grok-4`, `grok-4-0709`, `grok-3`, and `grok-3-fast` also available. Grok supports multi-turn conversations, streaming responses, and a range of models suited for daily conversations, creative writing, technical analysis, and code debugging.

## Application Process

To use the Grok API, apply for the corresponding service on the [Grok Chat Completion API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Grok on Ace Data Cloud](https://platform.acedata.cloud/service/grok)
- Docs: [Developer documentation](https://docs.acedata.cloud)

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
| [Grok Chat Completion API](https://platform.acedata.cloud/documents/faf08b59-36aa-4d26-b5d9-a18f113cc2be) | `/grok/chat/completions` | [Grok Chat Completion API Integration Guide](docs/grok_chat_completions_api_integration_guide.md) |
