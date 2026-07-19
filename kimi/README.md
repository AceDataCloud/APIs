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

Kimi is a series of AI models launched by Moonshot AI. The currently recommended `kimi-k3` is designed for long-context programming, agents, complex reasoning, and knowledge work, and is available through the OpenAI-compatible Chat Completions API. Kimi K2 models remain available for compatibility with existing applications.

## Application Process

To use the Kimi API, first create an API token in the [Ace Data Cloud console](https://platform.acedata.cloud/console/applications).

One API token can call all services on the platform, so you do not need to apply separately for each service. The first application grants a free quota for trial usage; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Kimi on Ace Data Cloud](https://platform.acedata.cloud/services/kimi)
- Docs: [Developer documentation](https://docs.acedata.cloud)
- Authentication: `Authorization: <YOUR_API_TOKEN>`

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
