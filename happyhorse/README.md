# Happy Horse Video API

Generate and edit AI videos with Happy Horse through one Ace Data Cloud API.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20Video%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Happy Horse Video](https://platform.acedata.cloud/service/happyhorse)

Keywords: happy-horse-api, happyhorse-api, ai-video, video-generation, video-editing,
text-to-video, image-to-video, reference-to-video, rest-api, ai-api, Ace Data Cloud

## Why Use Happy Horse on Ace Data Cloud

- One endpoint for text, first-frame image, reference-image, and video-edit workflows
- Unified API key, billing, usage records, and task tracking
- 720P and 1080P output with 3-15 second generation
- Asynchronous polling and webhook callbacks for long-running jobs
- CDN-backed final video URLs

## Overview

`POST /happyhorse/videos` dispatches four workflows through the `action` field:

| Action | Models | Required input |
|---|---|---|
| `generate` | `happyhorse-1.0-t2v`, `happyhorse-1.1-t2v` | `prompt` |
| `image_to_video` | `happyhorse-1.0-i2v`, `happyhorse-1.1-i2v` | `image_url` |
| `reference_to_video` | `happyhorse-1.0-r2v`, `happyhorse-1.1-r2v` | `prompt`, 1-9 `image_urls` |
| `video_edit` | `happyhorse-1.0-video-edit` | `prompt`, `video_url` |

`POST /happyhorse/tasks` retrieves one or several asynchronous tasks.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Happy Horse Video on Ace Data Cloud](https://platform.acedata.cloud/service/happyhorse)
- Developer docs: [docs.acedata.cloud](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "generate",
    "model": "happyhorse-1.1-t2v",
    "prompt": "A cinematic white horse crossing a snowy ridge at sunrise, slow camera push",
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
    "async": true
  }'
```

Poll the returned task ID:

```bash
curl --request POST "https://api.acedata.cloud/happyhorse/tasks" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"id": "TASK_ID", "action": "retrieve"}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for HappyHorse Video.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [HappyHorse Videos API Integration Instructions](https://platform.acedata.cloud/documents/happyhorse-videos) | `/happyhorse/videos` | [HappyHorse Videos API Integration Instructions](docs/happyhorse_videos_api_integration_guide.md) |
| [HappyHorse Tasks API Integration and Usage](https://platform.acedata.cloud/documents/happyhorse-videos) | `/happyhorse/tasks` | [HappyHorse Tasks API Integration and Usage](docs/happyhorse_tasks_api_integration_guide.md) |

## Agent Integrations

- MCP package: [`mcp-happyhorse`](https://pypi.org/project/mcp-happyhorse/)
- Hosted MCP: `https://happyhorse.mcp.acedata.cloud/mcp`
- Agent Skill: [`happyhorse-video`](https://github.com/AceDataCloud/Skills/tree/main/skills/happyhorse-video)

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

For support, visit [platform.acedata.cloud/support](https://platform.acedata.cloud/support).