# Kimi API

Moonshot AI Kimi generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Kimi](https://platform.acedata.cloud/service/kimi)

Keywords: kimi-api, moonshot-ai, kimi-k2, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Kimi on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Kimi is Moonshot AI's powerful AI dialogue system featuring strong reasoning capabilities and the ability to handle extended contexts. The Kimi K2.5 series supports multi-turn conversations, streaming responses, and advanced reasoning with thought processes visible to users.

## Application Process

To use the Kimi API, apply for the corresponding service on the [Kimi Chat Completion API](https://platform.acedata.cloud/documents/b23bbfa3-c820-47ee-b307-6c6dedc9d0cf) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Kimi on Ace Data Cloud](https://platform.acedata.cloud/service/kimi)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/kimi/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Kimi.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Kimi Chat Completion API](https://platform.acedata.cloud/documents/b23bbfa3-c820-47ee-b307-6c6dedc9d0cf) | `/kimi/chat/completions` | [Kimi Chat Completion API Integration Guide](docs/kimi_chat_completions_api_integration_guide.md) |
