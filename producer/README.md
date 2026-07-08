# Producer Music Generation API

AI music generation service supporting songs, lyrics, covers, extensions, stem separation, WAV/MP4 export, and reference-audio uploads.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Producer Music Generation](https://platform.acedata.cloud/service/producer)

Keywords: producer-api, ai-music, music-generation, song-generation, lyrics, cover, extend, stems, text-to-music, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Producer Music Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Producer Audios Generation API generates AI songs from a text `prompt` or custom `lyric`, with support for instrumental-only tracks, covers, extensions, and section replacement. The Producer Lyrics Generation API drafts lyrics from a prompt. The Producer Wav / Videos APIs export a finished track to WAV audio or MP4 video, the Upload API registers a reference audio for cover/extend, and the Tasks API polls asynchronous jobs.

## Application Process

To use the Producer Music Generation API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Producer Music Generation on Ace Data Cloud](https://platform.acedata.cloud/service/producer)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/producer/audios" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "action": "generate",
    "prompt": "upbeat electronic dance track with synth leads"
  }'
```

## Models

| Model | Notes |
| ---- | ---- |
| `FUZZ-2.0 Pro` | Default, highest quality |
| `FUZZ-2.0` | Standard quality |
| `FUZZ-2.0 Raw` | Raw output variant |
| `FUZZ-1.1 Pro` | Pro v1.1 |
| `FUZZ-1.0 Pro` | Pro v1.0 |
| `FUZZ-1.1` / `FUZZ-1.0` / `FUZZ-0.8` | Earlier versions |

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| Producer Upload API | `/producer/upload` | Register a reference audio file and reuse its returned `audio_id` for cover or extension workflows. |
| Producer Wav API | `/producer/wav` | Export a generated song to WAV audio. |
| Producer Videos API | `/producer/videos` | Export a generated song to MP4 video. |
| [Producer Audios Generation API](https://platform.acedata.cloud/documents/01d96900-9f8c-41d7-814c-95c7a885ba61) | `/producer/audios` | [Producer Audios Generation API Integration Guide](docs/producer_audios_generation_api_integration_guide.md) |
| [Producer Tasks API](https://platform.acedata.cloud/documents/e706d672-d7c9-4232-8652-0cf53219e7bf) | `/producer/tasks` | [Producer Tasks API Integration Guide](docs/producer_tasks_api_integration_guide.md) |
| Producer Lyrics API | `/producer/lyrics` | Generate song lyrics from a short natural-language prompt. |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
