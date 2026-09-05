# GLM API

GLM (General Language Model) generative services by Zhipu AI, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - GLM](https://platform.acedata.cloud/service/glm)

Keywords: glm-api, glm-5.3, glm-5.2, glm-5.1, glm-4.7, chat-completions, zhipu-ai, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use GLM on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

GLM (General Language Model) is the next-generation large language model series by Zhipu AI (Z.ai), featuring powerful Chinese and English understanding and generation capabilities. The current flagship `glm-5.3`, along with `glm-5.2`, `glm-5.1`, `glm-5`, `glm-4.7`, `glm-4.6` and other new-generation models, has been extensively optimized for long-context, tool calling, and code tasks. They are widely applicable to intelligent Q&A, content creation, code assistance, customer service bots, and more.

## Application Process

To use the GLM API, obtain an API token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications). One API token can call all services on the platform.

There is a free quota available for first-time applicants. When it is used up, you can recharge your general balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [GLM on Ace Data Cloud](https://platform.acedata.cloud/service/glm)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/glm/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "glm-5.2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for GLM.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [GLM Chat Completion API](https://platform.acedata.cloud/documents/glm-chat-completions) | `/glm/chat/completions` | [GLM Chat Completion API Integration Guide](docs/glm_chat_completions_api_integration_guide.md) |
