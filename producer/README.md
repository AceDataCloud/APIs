# Producer API

AI music generation APIs for songs, lyrics, uploads, WAV export, MP4 export, and task polling.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Producer](https://platform.acedata.cloud/service/producer)

Keywords: producer-api, ai-music, audios, lyrics, upload, wav, videos, tasks, song-generation, rest-api, ai-api, Ace Data Cloud

## Why Use Producer on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

Producer supports end-to-end music workflows: generate songs with `/producer/audios`, draft lyrics with `/producer/lyrics`, register reference audio with `/producer/upload`, export results with `/producer/videos` or `/producer/wav`, and poll jobs with `/producer/tasks`.

## Application Process

Open the Producer service page, generate your Ace Data Cloud API token, and call the endpoints below. Trial quota is available for first-time users, and authentication is shared across services.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Producer on Ace Data Cloud](https://platform.acedata.cloud/service/producer)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/producer/audios" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "action": "generate",
    "prompt": "upbeat electronic dance track with synth leads"
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Producer.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Producer Audios Generation API | `/producer/audios` | [producer_audios_generation_api_integration_guide.md](docs/producer_audios_generation_api_integration_guide.md) |
| Producer Lyrics API | `/producer/lyrics` | [producer_lyrics_api_integration_guide.md](docs/producer_lyrics_api_integration_guide.md) |
| Producer Upload API | `/producer/upload` | [producer_upload_api_integration_guide.md](docs/producer_upload_api_integration_guide.md) |
| Producer Videos API | `/producer/videos` | [producer_videos_api_integration_guide.md](docs/producer_videos_api_integration_guide.md) |
| Producer WAV API | `/producer/wav` | [producer_wav_api_integration_guide.md](docs/producer_wav_api_integration_guide.md) |
| Producer Tasks API | `/producer/tasks` | [producer_tasks_api_integration_guide.md](docs/producer_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
