# DeepSeek API

DeepSeek generative services, including chat completions.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - DeepSeek](https://platform.acedata.cloud/service/deepseek)

Keywords: deepseek-api, deepseek-v3, chat-completions, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use DeepSeek on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

DeepSeek is a powerful AI dialogue system featuring outstanding language understanding and generation capabilities. DeepSeek-V3 and its variants are widely used across industries for daily conversations, creative writing, professional consulting, and code programming.

## Application Process

To use the DeepSeek API, apply for the corresponding service on the [DeepSeek Chat Completion API](https://platform.acedata.cloud/documents/2d6a9bae-9a70-4aaa-bd72-28e5bd60fa67) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [DeepSeek on Ace Data Cloud](https://platform.acedata.cloud/service/deepseek)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/deepseek/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for DeepSeek.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [DeepSeek Chat Completion API](https://platform.acedata.cloud/documents/2d6a9bae-9a70-4aaa-bd72-28e5bd60fa67) | `/deepseek/chat/completions` | [DeepSeek Chat Completion API Integration Guide](docs/deepseek_chat_completions_api_integration_guide.md) |
