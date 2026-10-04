# Flux API

Public API documentation for Flux on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/flux/images` | [English](docs/flux_images.md) · [中文](docs/zh-CN/flux_images.md) |
| POST | `/flux/tasks` | [English](docs/flux_tasks.md) · [中文](docs/zh-CN/flux_tasks.md) |
| POST | `/flux/videos` | [English](docs/flux_generate_video.md) · [中文](docs/zh-CN/flux_generate_video.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
