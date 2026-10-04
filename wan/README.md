# Wan API

Public API documentation for Wan on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/wan/tasks` | [English](docs/wan_tasks.md) · [中文](docs/zh-CN/wan_tasks.md) |
| POST | `/wan/videos` | [English](docs/wan_videos.md) · [中文](docs/zh-CN/wan_videos.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
