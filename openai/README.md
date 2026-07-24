# OpenAI API

OpenAI-compatible APIs for chat, embeddings, responses, image generation, image editing, model discovery, and task lookup.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - OpenAI](https://platform.acedata.cloud/service/openai)

Keywords: openai-api, openai-compatible, gpt-5.2, chat-completions, responses, embeddings, image-generation, image-editing, rest-api, ai-api, Ace Data Cloud

## Why Use OpenAI on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

The OpenAI package combines chat completions, the Responses API, embeddings, image generation, image editing, and supporting task/model endpoints in one place. It is useful when you need OpenAI-compatible request formats with Ace Data Cloud authentication and billing.

## Application Process

Open the OpenAI service page, generate an API token in Ace Data Cloud Console, and use the guides below for each endpoint. The same token can be reused across other Ace Data Cloud services.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [OpenAI on Ace Data Cloud](https://platform.acedata.cloud/service/openai)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/openai/chat/completions" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "model": "gpt-5.2",
    "messages": [{"role": "user", "content": "Write a short hello world program in Python."}]
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for OpenAI.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| OpenAI Chat Completions API | `/openai/chat/completions` | [openai_chat_completion_api_integration_guide.md](docs/openai_chat_completion_api_integration_guide.md) |
| OpenAI Chat Completions 4o Image Guide | `/openai/chat/completions` | [openai_chat_completions_4o_image_api_integration_guide.md](docs/openai_chat_completions_4o_image_api_integration_guide.md) |
| OpenAI Embeddings API | `/openai/embeddings` | [openai_embeddings_api_integration_guide.md](docs/openai_embeddings_api_integration_guide.md) |
| OpenAI Images Generations API | `/openai/images/generations` | [openai_images_generations_api_integration_guide.md](docs/openai_images_generations_api_integration_guide.md) |
| OpenAI Images Edits API | `/openai/images/edits` | [openai_images_edits_api_integration_guide.md](docs/openai_images_edits_api_integration_guide.md) |
| OpenAI Responses API | `/openai/responses` | [openai_responses_api_integration_guide.md](docs/openai_responses_api_integration_guide.md) |
| OpenAI Tasks API | `/openai/tasks` | [openai_tasks_api_integration_guide.md](docs/openai_tasks_api_integration_guide.md) |
| OpenAI Models API | `/openai/models` | OpenAPI reference only |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
