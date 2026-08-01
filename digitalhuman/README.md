# Digital Human API

Digital human video generation and voice cloning service for creating lip-synced avatar videos from source media and audio/text.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Digital Human](https://platform.acedata.cloud)

Keywords: digital-human-api, avatar-video, lipsync, voice-clone, tts, video-generation, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Digital Human on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Digital Human service provides APIs to generate talking-head videos, clone voices, and query asynchronous task status.

## Authentication

All endpoints require the `Authorization` header with your Ace Data Cloud API token (`******`).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/digital-human/videos" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{
    "video_url": "https://cdn.acedata.cloud/634d760216.mp4",
    "audio_url": "https://cdn1.suno.ai/ec13e502-d043-4eb2-92ee-e900c6da69d1.wav"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| Digital Human Videos API | `/digital-human/videos` | [Digital Human Videos API Integration Guide](docs/digital_human_videos_api_integration_guide.md) |
| Digital Human Voices API | `/digital-human/voices` | [Digital Human Voices API Integration Guide](docs/digital_human_voices_api_integration_guide.md) |
| Digital Human Tasks API | `/digital-human/tasks` | [Digital Human Tasks API Integration Guide](docs/digital_human_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
