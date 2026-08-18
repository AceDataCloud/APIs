# DeepSeek API

DeepSeek AI generative services, including OpenAI-compatible chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - DeepSeek](https://platform.acedata.cloud/service/deepseek)

Keywords: deepseek-api, deepseek-ai, deepseek-chat-completions, deepseek-r1, deepseek-v3, deepseek-v4-flash, deepseek-v4-pro, openai-compatible, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use DeepSeek on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

DeepSeek on Ace Data Cloud provides OpenAI-compatible chat completions through `/deepseek/chat/completions`. It supports DeepSeek reasoning and chat models including `deepseek-r1`, `deepseek-r1-0528`, `deepseek-v3`, `deepseek-v3-250324`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, and `deepseek-v4-pro`, along with streaming, tool calls, response-format controls, and common sampling parameters.

## Application Process

To use the DeepSeek API, apply for the corresponding service on the [DeepSeek API](https://platform.acedata.cloud/service/deepseek) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [DeepSeek on Ace Data Cloud](https://platform.acedata.cloud/service/deepseek)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/deepseek/chat/completions" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "Hello, DeepSeek!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for DeepSeek.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [DeepSeek Chat Completions API](https://platform.acedata.cloud/service/deepseek) | `/deepseek/chat/completions` | [DeepSeek Chat Completions API Integration Guide](docs/deepseek_chat_completions_api_integration_guide.md) |
