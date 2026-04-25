# AI Chat API

AI dialogue service supporting multiple large language models with simplified multi-turn conversation management.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - AI Chat](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a)

Keywords: aichat, ai-dialogue, chat-api, multi-turn-conversation, gpt, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use AI Chat API on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The AI Chat API simplifies integrating large language model conversations into your application. Unlike raw Chat Completions APIs that require managing the full message history, the AI Chat API handles context management internally — you never need to worry about passing prior messages or handling token limit issues.

Key features include:

- **Simple single-turn Q&A** — send a question, get an answer, no history needed
- **Stateful multi-turn conversations** — pass `stateful: true` and reuse the returned `id` for follow-up questions
- **Streaming responses** — set `accept: application/x-ndjson` for token-by-token streaming output
- **Model presets** — provide a `preset` (system prompt) to give the model a custom role
- **Image recognition** — pass image URLs via `references` with a vision-capable model
- **Web-browsing models** — select browsing-enabled models for real-time internet search

## API Endpoints

| Endpoint | Description |
|---|---|
| `POST /aichat/conversations` | Send a question and receive an AI-generated answer |

## Supported Models

The API supports a wide range of models including:

- **GPT-5 series**: `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.4`, `gpt-5.4-pro`, `gpt-5.2`, `gpt-5.1`, `gpt-5`, `gpt-5-mini`, `gpt-5-nano`
- **GPT-4.1 series**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`
- **GPT-4o series**: `gpt-4o`, `gpt-4o-mini`, `gpt-4o-all`, `gpt-4o-image`
- **GPT-4 series**: `gpt-4`, `gpt-4-all`, `gpt-4-turbo`, `gpt-4-vision-preview`
- **o-series reasoning**: `o1`, `o1-pro`, `o3`, `o3-mini`, `o4-mini`
- **DeepSeek**: `deepseek-r1`, `deepseek-v3`
- **Grok**: `grok-3`
- **GLM**: `glm-5.1`, `glm-4.7`, `glm-4.6`, `glm-4.5-air`, `glm-3-turbo`

## Quick Start

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-4o",
    "question": "What is the capital of France?"
  }'
```

Response:

```json
{
  "answer": "The capital of France is Paris."
}
```

## APIs and Guides

| Document | Endpoint | Guide |
|---|---|---|
| [AI Chat Conversations API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) | `/aichat/conversations` | [AI Chat API Integration Guide](docs/aichat_conversations_api_integration_guide.md) |
