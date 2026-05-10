# Fish Audio API

Fish Audio voice cloning and text-to-speech generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Audio](https://platform.acedata.cloud/service/fish)

Keywords: fish-api, fish-audio, voice-clone, text-to-speech, tts, ai-voice, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Audio on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

Fish Audio API provides a comprehensive voice cloning and text-to-speech solution:

1. **Audios** (`/fish/audios`): Clone voices using prompt-based generation — input a prompt, action, voice ID, and model to generate cloned audio output.
2. **Voices** (`/fish/voices`): Create custom voice models from audio URLs — upload a voice sample to build a reusable voice profile.
3. **TTS** (`/fish/tts`): Text-to-speech synthesis fully compatible with the Fish Audio official API — converts text to speech using a specified or cloned voice.
4. **Model** (`/fish/model`): Create and list voice models — manage cloned voice assets with full CRUD support.
5. **Tasks** (`/fish/tasks`): Query task status — retrieve single or batch task results from async audio generation requests.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Audio on Ace Data Cloud](https://platform.acedata.cloud/service/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'authorization: Bearer YOUR_API_KEY' \
  -H 'content-type: application/json' \
  -d '{
    "text": "Hello, welcome to Fish Audio on Ace Data Cloud."
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish Audio.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) | `/fish/audios` | [Fish Audios Generation API Integration Guide](docs/fish_audios_generation_api_integration_guide.md) |
| [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) | `/fish/voices` | [Fish Voices Generation API Integration Guide](docs/fish_voices_generation_api_integration_guide.md) |
| [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `/fish/model` | [Fish Model API Integration Guide](docs/fish_model_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/44c93949-1419-4a45-8db5-8a8335de7151) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
