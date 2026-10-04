# OpenAI generation API

Public API documentation for OpenAI generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/openai/chat/completions` | [English](docs/openai_chat_completions.md) · [中文](docs/zh-CN/openai_chat_completions.md) |
| POST | `/openai/embeddings` | [English](docs/openai_embeddings.md) · [中文](docs/zh-CN/openai_embeddings.md) |
| POST | `/openai/images/generations` | [English](docs/openai_images_generations.md) · [中文](docs/zh-CN/openai_images_generations.md) |
| POST | `/openai/responses` | [English](docs/openai_responses.md) · [中文](docs/zh-CN/openai_responses.md) |
| POST | `/openai/images/edits` | [English](docs/openai_images_edits.md) · [中文](docs/zh-CN/openai_images_edits.md) |
| POST | `/v1/audio/speech` | [English](docs/openai_audio_speech.md) · [中文](docs/zh-CN/openai_audio_speech.md) |
| POST | `/v1/audio/transcriptions` | [English](docs/openai_audio_transcriptions.md) · [中文](docs/zh-CN/openai_audio_transcriptions.md) |
| POST | `/openai/tasks` | [English](docs/openai_tasks.md) · [中文](docs/zh-CN/openai_tasks.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
