# Fish Voice Generation API

Fish Audio text-to-speech and voice-cloning service: synthesize speech from text and create custom voice models from reference audio.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Voice Generation](https://platform.acedata.cloud/service/fish)

Keywords: fish-api, fish-audio, text-to-speech, tts, voice-clone, voice-model, speech-synthesis, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Voice Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Fish TTS API converts text into natural speech, optionally using a cloned voice model. The Fish Model APIs create, query, and fetch custom voice models from reference audio, and the Fish Tasks API polls asynchronous jobs.

## Application Process

To use the APIs in this service, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Voice Generation on Ace Data Cloud](https://platform.acedata.cloud/service/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "text": "Hello, this is a demonstration of AI voice synthesis."
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish voice generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish Audios Generation API Integration Instructions](https://platform.acedata.cloud/documents/fish-audios) | `/fish/audios` | [Fish Audios Generation API Integration Instructions](docs/fish_audios_api_integration_guide.md) |
| [Fish Model API Integration Guide](https://platform.acedata.cloud/services/fish) | `/fish/model` | [Fish Model API Integration Guide](docs/fish_model_api_integration_guide.md) |
| [Fish Model Get API Integration Guide](https://platform.acedata.cloud/documents/fish-model) | `/fish/model/d7900c21663f485ab63ebdb7e5905036` | [Fish Model Get API Integration Guide](docs/fish_model_get_api_integration_guide.md) |
| [Fish Model Query API Integration Guide](https://platform.acedata.cloud/documents/fish-model) | `/fish/model` | [Fish Model Query API Integration Guide](docs/fish_model_query_api_integration_guide.md) |
| [Fish TTS API Integration Instructions](https://platform.acedata.cloud/services/fish) | `/fish/tts` | [Fish TTS API Integration Instructions](docs/fish_tts_api_integration_guide.md) |
| [Fish Voices Generation API Integration Instructions](https://platform.acedata.cloud/documents/fish-voices) | `/fish/voices` | [Fish Voices Generation API Integration Instructions](docs/fish_voices_api_integration_guide.md) |
| [Fish Tasks API Integration and Usage](https://platform.acedata.cloud/documents/fish-tts) | `/fish/tasks` | [Fish Tasks API Integration and Usage](docs/fish_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
