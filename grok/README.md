# Grok API

xAI Grok APIs for chat completions, video generation, and task lookup.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Grok](https://platform.acedata.cloud/service/grok)

Keywords: grok-api, xai-grok, grok-4.5, grok-4, grok-3, chat-completions, video-generation, tasks, rest-api, ai-api, Ace Data Cloud

## Why Use Grok on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

Ace Data Cloud exposes Grok chat and media workflows behind a single token. You can build text conversations with `/grok/chat/completions`, generate Grok videos with `/grok/videos`, and poll asynchronous results with `/grok/tasks`.

## Application Process

Open the Grok service page, create or reuse your Ace Data Cloud API token, and call the endpoints below. One token works across the platform, and first-time users receive trial quota.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Grok on Ace Data Cloud](https://platform.acedata.cloud/service/grok)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/grok/chat/completions" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "model": "grok-4.5",
    "messages": [{"role": "user", "content": "Hello from Ace Data Cloud"}]
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Grok.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Grok Chat Completions API | `/grok/chat/completions` | [grok_chat_completions_api_integration_guide.md](docs/grok_chat_completions_api_integration_guide.md) |
| Grok Videos API | `/grok/videos` | [grok_videos_api_integration_guide.md](docs/grok_videos_api_integration_guide.md) |
| Grok Tasks API | `/grok/tasks` | [grok_tasks_api_integration_guide.md](docs/grok_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
