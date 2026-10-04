# Fish voice generation API

Public API documentation for Fish voice generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/fish/tts` | [English](docs/fish_tts.md) · [中文](docs/zh-CN/fish_tts.md) |
| POST | `/fish/model` | [English](docs/fish_model.md) · [中文](docs/zh-CN/fish_model.md) |
| GET | `/fish/model` | [English](docs/fish_model_query.md) · [中文](docs/zh-CN/fish_model_query.md) |
| GET | `/fish/model/{id}` | [English](docs/fish_model_get.md) · [中文](docs/zh-CN/fish_model_get.md) |
| POST | `/fish/tasks` | [English](docs/fish_tasks.md) · [中文](docs/zh-CN/fish_tasks.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
