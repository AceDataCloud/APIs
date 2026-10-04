# Suno Music Generation API

Public API documentation for Suno Music Generation on [Ace Data Cloud](https://platform.acedata.cloud).

Customer guide sources and API schemas are maintained in PlatformBackend. Published English translations are included only when the published Chinese source matches the current source file.

Get an API token from the [console](https://platform.acedata.cloud/console/applications) and send `Authorization: Bearer $ACEDATACLOUD_API_TOKEN` to `https://api.acedata.cloud`.

| Method | Endpoint | Current guide |
| --- | --- | --- |
| POST | `/suno/audios` | [English](docs/suno_audios.md) · [中文](docs/zh-CN/suno_audios.md) |
| POST | `/suno/persona` | [English](docs/suno_persona.md) · [中文](docs/zh-CN/suno_persona.md) |
| POST | `/suno/mp4` | [English](docs/suno_mp4.md) · [中文](docs/zh-CN/suno_mp4.md) |
| POST | `/suno/voices` | [English](docs/suno_voices.md) · [中文](docs/zh-CN/suno_voices.md) |
| POST | `/suno/timing` | [English](docs/suno_timing.md) · [中文](docs/zh-CN/suno_timing.md) |
| POST | `/suno/vox` | [English](docs/suno_vox.md) · [中文](docs/zh-CN/suno_vox.md) |
| POST | `/suno/wav` | [English](docs/suno_wav.md) · [中文](docs/zh-CN/suno_wav.md) |
| POST | `/suno/midi` | [English](docs/suno_midi.md) · [中文](docs/zh-CN/suno_midi.md) |
| POST | `/suno/mp3` | [English](docs/suno_mp3.md) · [中文](docs/zh-CN/suno_mp3.md) |
| POST | `/suno/style` | [English](docs/suno_style.md) · [中文](docs/zh-CN/suno_style.md) |
| POST | `/suno/lyrics` | [English](docs/suno_lyrics.md) · [中文](docs/zh-CN/suno_lyrics.md) |
| POST | `/suno/mashup-lyrics` | [English](docs/suno_mashup_lyrics.md) · [中文](docs/zh-CN/suno_mashup_lyrics.md) |
| POST | `/suno/tasks` | [English](docs/suno_tasks.md) · [中文](docs/zh-CN/suno_tasks.md) |
| POST | `/suno/upload` | [English](docs/suno_upload.md) · [中文](docs/zh-CN/suno_upload.md) |

Full [API reference](docs/platform/README.md) includes request fields, schemas and source commit provenance.

Task submission is not completion. Follow each endpoint’s guide to poll the returned task ID and inspect the terminal result.

<!-- platform-reference:start -->
Read the [current API reference](docs/platform/README.md) for endpoints, request fields and the backend integration guides before using optional or recently added capabilities.
<!-- platform-reference:end -->
