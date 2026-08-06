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

Kimi is a series of AI models launched by Dark Side of the Moon. The recommended `kimi-k3` model is aimed at long-range programming, agents, complex reasoning, and knowledge work, and can be called through the OpenAI-compatible Chat Completions API. Compatible K2 models, including `kimi-k2.6`, `kimi-k2-thinking-turbo`, `kimi-k2.5`, and `kimi-k2-thinking`, remain available.

## Application Process

To use the Kimi API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token. One API Token can call all services on the platform without applying separately for each service.

The first application grants a free trial quota. When the quota is insufficient, recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

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
    "messages": [{"role": "user", "content": "Hello!"}],
    "reasoning_effort": "max"
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Kimi.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions) | `/kimi/chat/completions` | [Kimi Chat Completion API Integration Guide](docs/kimi_chat_completions_api_integration_guide.md) |
