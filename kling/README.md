# Kling video generation API

Public API documentation for Kling video generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/kling/motion` | [English](docs/kling_motion.md) · [中文](docs/zh-CN/kling_motion.md) |
| POST | `/kling/tasks` | [English](docs/kling_tasks.md) · [中文](docs/zh-CN/kling_tasks.md) |
| POST | `/kling/videos` | [English](docs/kling_videos.md) · [中文](docs/zh-CN/kling_videos.md) |
| POST | `/kling/lip-sync` | [English](docs/kling_lip_sync.md) · [中文](docs/zh-CN/kling_lip_sync.md) |
| POST | `/kling/talking-photo` | [English](docs/kling_talking_photo.md) · [中文](docs/zh-CN/kling_talking_photo.md) |
| POST | `/kling/goods-studio` | [English](docs/kling_goods_studio.md) · [中文](docs/zh-CN/kling_goods_studio.md) |
| POST | `/kling/video-commerce` | [English](docs/kling_video_commerce.md) · [中文](docs/zh-CN/kling_video_commerce.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
