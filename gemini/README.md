# Gemini API

Google Gemini services on Ace Data Cloud, including chat completions, native `generateContent` / `streamGenerateContent`, video generation, and task lookup.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Gemini](https://platform.acedata.cloud/service/gemini)

Keywords: gemini-api, google-gemini, gemini-3.1-pro, gemini-3.5-flash, chat-completions, generate-content, stream-generate-content, video-generation, tasks-api, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Gemini on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Google Gemini on Ace Data Cloud supports both the OpenAI-compatible chat completions format and Google's native `generateContent` / `streamGenerateContent` format, plus video generation and task retrieval endpoints. Common model values include `gemini-3.1-pro`, `gemini-3.5-flash`, `gemini-3.1-flash-lite-preview`, `gemini-3.0-pro`, `gemini-3-flash-preview`, `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, and `gemini-2.0-flash`.

## Application Process

Create an API Token in the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications), then send it in the `Authorization` header.

One API Token works across Ace Data Cloud services. New accounts receive starter credit, and you can top up shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Gemini on Ace Data Cloud](https://platform.acedata.cloud/service/gemini)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/gemini/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-3.5-flash",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Gemini.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Gemini Chat Completion API](https://platform.acedata.cloud/documents/gemini-chat-completions) | `/gemini/chat/completions` | [Gemini Chat Completion API Integration Guide](docs/gemini_chat_completions_api_integration_guide.md) |
| [Gemini Generate Content API](https://platform.acedata.cloud/documents/gemini-generate-content-api) | `/v1beta/models/{model}:generateContent` | [Gemini Generate Content API Integration Guide](docs/gemini_generate_content_api_integration_guide.md) |
| [Gemini Stream Generate Content API](https://platform.acedata.cloud/documents/gemini-generate-content-api) | `/v1beta/models/{model}:streamGenerateContent?alt=sse` | [Gemini Generate Content API Integration Guide](docs/gemini_generate_content_api_integration_guide.md) |
| [Gemini Videos Generation API](https://platform.acedata.cloud/documents/gemini-videos) | `/gemini/videos` | [Gemini Videos Generation API Integration Guide](docs/gemini_videos_generation_api_integration_guide.md) |
| [Gemini Tasks API](https://platform.acedata.cloud/documents/gemini-tasks) | `/gemini/tasks` | [Gemini Tasks API Integration Guide](docs/gemini_tasks_api_integration_guide.md) |
