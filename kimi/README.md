# Kimi API

Moonshot AI Kimi generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Kimi](https://platform.acedata.cloud/services/kimi)

Keywords: kimi-api, moonshot-ai, kimi-k3, kimi-k2, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Kimi on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Kimi is Moonshot AI's powerful AI dialogue system. The current flagship, `kimi-k3`, supports reasoning, vision, tool calling, a 1,048,576-token context window, and up to 16,384 output tokens. Kimi K2 models remain available for compatibility with existing applications.

## Application Process

To use the Kimi API, apply for the corresponding service on the [Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Kimi on Ace Data Cloud](https://platform.acedata.cloud/services/kimi)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/kimi/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kimi-k3",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Kimi.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions) | `/kimi/chat/completions` | [Kimi Chat Completion API Integration Guide](docs/kimi_chat_completions_api_integration_guide.md) |
