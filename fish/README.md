# Fish Music Generation API

Fish Audio AI voice cloning, text-to-speech, and audio generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Music Generation](https://platform.acedata.cloud/service/fish)

Keywords: fish-audio, tts, text-to-speech, voice-cloning, ai-audio, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Music Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Fish Audio is a professional AI voice cloning and text-to-speech platform. With the Fish Music Generation APIs on Ace Data Cloud you can:

- **Clone voices** — upload an audio sample to create a custom voice model.
- **Synthesize speech** — convert text to speech using any voice model (compatible with the Fish Audio official TTS API).
- **Manage voice models** — create, list, and retrieve voice models.
- **Query tasks** — check the status of asynchronous generation tasks.

All endpoints are served at `https://api.acedata.cloud` and use Bearer token authentication.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Music Generation on Ace Data Cloud](https://platform.acedata.cloud/service/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"text": "Hello, world!"}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish Music Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `POST /fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) | `POST /fish/audios` | [Fish Audios Generation API Integration Guide](docs/fish_audios_generation_api_integration_guide.md) |
| [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) | `POST /fish/voices` | [Fish Voices Generation API Integration Guide](docs/fish_voices_generation_api_integration_guide.md) |
| [Fish Model Create API](https://platform.acedata.cloud/documents/62fdf4f1-6a05-4d92-bb15-1bf78b27a14a) | `POST /fish/model` | [Fish Model Create API Integration Guide](docs/fish_model_create_api_integration_guide.md) |
| [Fish Model Query API](https://platform.acedata.cloud/documents/5a9b3e03-2896-5606-a6b9-d9f4469f0e9d) | `GET /fish/model` | [Fish Model Query API Integration Guide](docs/fish_model_query_api_integration_guide.md) |
| [Fish Model Get API](https://platform.acedata.cloud/documents/dabdffe7-254b-5a3f-9eca-425d614d82b9) | `GET /fish/model/{id}` | [Fish Model Get API Integration Guide](docs/fish_model_get_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/44c93949-1419-4a45-8db5-8a8335de7151) | `POST /fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
