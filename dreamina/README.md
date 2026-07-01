# Dreamina API

Dreamina generative video services for talking-photo/digital-human workflows.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Dreamina](https://platform.acedata.cloud/service/dreamina)

Keywords: dreamina-api, talking-photo, digital-human, omnihuman, video-generation, rest-api, ai-api, developer-tools, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Dreamina on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Dreamina provides audio-driven talking-photo video generation and a task retrieval API for asynchronous workflows.

## Application Process

To use the Dreamina API, apply for the corresponding service on the [Dreamina Videos API](https://platform.acedata.cloud/documents/dreamina-videos) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Dreamina on Ace Data Cloud](https://platform.acedata.cloud/service/dreamina)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/dreamina/videos" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "omnihuman-1.5",
    "image_url": "https://cdn.acedata.cloud/4hfydw.jpg",
    "audio_url": "https://cdn.acedata.cloud/6f7d62b18b.wav"
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Dreamina.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Dreamina Videos API](https://platform.acedata.cloud/documents/dreamina-videos) | `/dreamina/videos` | [Dreamina Videos API Integration Guide](docs/dreamina_videos_api_integration_guide.md) |
| [Dreamina Tasks API](https://platform.acedata.cloud/documents/dreamina-tasks-integration) | `/dreamina/tasks` | [Dreamina Tasks API Integration Guide](docs/dreamina_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
