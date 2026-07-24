# Veo API

Google Veo video generation APIs for creation, task polling, extension, reshoot, object editing, and upsampling.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Veo](https://platform.acedata.cloud/service/veo)

Keywords: veo-api, google-veo, ai-video, video-generation, extend, reshoot, objects, upsample, tasks, rest-api, ai-api, Ace Data Cloud

## Why Use Veo on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

The Veo package covers text-to-video and image-to-video generation with `/veo/videos`, task lookup with `/veo/tasks`, and follow-up editing flows for extend, reshoot, objects, and upsample operations.

## Application Process

Open the Veo service page, create your API token in Ace Data Cloud Console, and choose the guide that matches your video workflow. One platform token is reused across services and includes starter quota for new users.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Veo on Ace Data Cloud](https://platform.acedata.cloud/service/veo)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/veo/videos" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "action": "text2video",
    "model": "veo31-fast",
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden"
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Veo.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Veo Videos Generation API | `/veo/videos` | [veo_videos_generation_api_integration_guide.md](docs/veo_videos_generation_api_integration_guide.md) |
| Veo Extend API | `/veo/extend` | [veo_extend_api_integration_guide.md](docs/veo_extend_api_integration_guide.md) |
| Veo Reshoot API | `/veo/reshoot` | [veo_reshoot_api_integration_guide.md](docs/veo_reshoot_api_integration_guide.md) |
| Veo Objects API | `/veo/objects` | [veo_objects_api_integration_guide.md](docs/veo_objects_api_integration_guide.md) |
| Veo Upsample API | `/veo/upsample` | [veo_upsample_api_integration_guide.md](docs/veo_upsample_api_integration_guide.md) |
| Veo Tasks API | `/veo/tasks` | [veo_tasks_api_integration_guide.md](docs/veo_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
