# Fish Music Generation API

Fish Audio-compatible text-to-speech and voice model query APIs on Ace Data Cloud.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Music Generation](https://platform.acedata.cloud/services/fish)

Keywords: fish-api, fish-audio, text-to-speech, voice-cloning, voice-models, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Music Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Fish package provides Fish Audio-compatible APIs for text-to-speech generation, querying available voice models, retrieving the details of a single voice model, and polling asynchronous task results.

## Application Process

To use the Fish APIs, open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Music Generation on Ace Data Cloud](https://platform.acedata.cloud/services/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --header "accept: application/json" \
  --header "model: s2-pro" \
  --data '{
    "text": "Hello, this is a Fish-Audio-compatible test."
  }'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish Music Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/documents/fish-tts) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Model Query API](https://platform.acedata.cloud/documents/fish-model-query) | `/fish/model` | [Fish Model Query API Integration Guide](docs/fish_model_query_api_integration_guide.md) |
| [Fish Model Get API](https://platform.acedata.cloud/documents/fish-model-get) | `/fish/model/{id}` | [Fish Model Get API Integration Guide](docs/fish_model_get_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/fish-tasks) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
