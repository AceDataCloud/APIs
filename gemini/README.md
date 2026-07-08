# Gemini API

Google Gemini generative services, including chat completions, native generate content APIs, video generation, and task polling.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Gemini](https://platform.acedata.cloud/service/gemini)

Keywords: gemini-api, google-gemini, chat-completions, generate-content, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Gemini on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Google Gemini is a powerful AI conversation system that supports both OpenAI-compatible chat completions format and Google's native `generateContent` / `streamGenerateContent` endpoints. Gemini models support multi-modal inputs (text and images), thinking mode, function calling, JSON mode, video generation, and asynchronous task polling.

## Application Process

To use the Gemini API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Gemini on Ace Data Cloud](https://platform.acedata.cloud/service/gemini)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/gemini/chat/completions" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Gemini.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Gemini Chat Completion API](https://platform.acedata.cloud/documents/ae54bf9b-af41-4072-b969-3756b6d66834) | `/gemini/chat/completions` | [Gemini Chat Completion API Integration Guide](docs/gemini_chat_completions_api_integration_guide.md) |
| Gemini Generate Content API | `/v1beta/models/{model}:generateContent` | Native Gemini request format for multimodal prompts, tools, and structured generation. |
| Gemini Stream Generate Content API | `/v1beta/models/{model}:streamGenerateContent` | Streaming variant of `generateContent` for incremental token delivery. |
| Gemini Videos API | `/gemini/videos` | Submit Gemini video generation jobs with prompt- or image-driven workflows. |
| Gemini Tasks API | `/gemini/tasks` | Retrieve asynchronous Gemini job status and final results by task ID. |
