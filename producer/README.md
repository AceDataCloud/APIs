# Producer Music Generation API

Public API documentation for Producer Music Generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/producer/upload` | [English](docs/producer_upload.md) · [中文](docs/zh-CN/producer_upload.md) |
| POST | `/producer/videos` | [English](docs/producer_videos.md) · [中文](docs/zh-CN/producer_videos.md) |
| POST | `/producer/wav` | [English](docs/producer_wav.md) · [中文](docs/zh-CN/producer_wav.md) |
| POST | `/producer/audios` | [English](docs/producer_audios.md) · [中文](docs/zh-CN/producer_audios.md) |
| POST | `/producer/tasks` | [English](docs/producer_tasks.md) · [中文](docs/zh-CN/producer_tasks.md) |
| POST | `/producer/lyrics` | [English](docs/producer_lyrics.md) · [中文](docs/zh-CN/producer_lyrics.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
