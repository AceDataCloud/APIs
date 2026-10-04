# Nano Banana Image Generation API

Public API documentation for Nano Banana Image Generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/nano-banana/images` | [English](docs/nanobanana_images.md) · [中文](docs/zh-CN/nanobanana_images.md) |
| POST | `/nano-banana/tasks` | [English](docs/nanobanana_tasks.md) · [中文](docs/zh-CN/nanobanana_tasks.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
