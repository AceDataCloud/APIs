# WebExtrator Web Render & Extract API

Public API documentation for WebExtrator Web Render & Extract on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/webextrator/extract` | [English](docs/webextrator_extract.md) · [中文](docs/zh-CN/webextrator_extract.md) |
| POST | `/webextrator/render` | [English](docs/webextrator_render.md) · [中文](docs/zh-CN/webextrator_render.md) |
| POST | `/webextrator/tasks` | [English](docs/webextrator_tasks.md) · [中文](docs/zh-CN/webextrator_tasks.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
