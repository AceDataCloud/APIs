# Fish Audio API

Fish Audio voice cloning and text-to-speech generation service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Audio](https://platform.acedata.cloud/service/fish)

Keywords: fish-api, fish-audio-api, ai-tts, voice-cloning, text-to-speech, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Audio on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Fish Audio API provides voice cloning and text-to-speech capabilities powered by the Fish Audio platform. It supports:

- **Fish TTS API**: Fully compatible with the Fish Audio official OpenAPI for text-to-speech synthesis. Migrate existing code by swapping credentials only.
- **Fish Audios Generation API**: Clone voices by inputting prompt words and a voice ID.
- **Fish Voices Generation API**: Create your own cloned voice model by uploading an audio link.
- **Fish Tasks API**: Query the execution status of voice generation tasks by task ID.
- **Fish Model API**: Create and manage cloned voice models, fully compatible with the Fish Audio official ModelEntity API.

## Application Process

To use the API, first visit the [Fish Audio API](https://platform.acedata.cloud/service/fish) page and click the "Acquire" button to obtain the credentials needed for the request.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will automatically return to the current page.

Upon the first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

To generate speech from text, send a `POST` request to `/fish/tts` with the `text` field:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "The weather is great today, let us go for a walk."
  }'
```

After the call, the returned result is as follows:

```json
{
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Audio on Ace Data Cloud](https://platform.acedata.cloud/service/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2-pro" \
  --data '{"text": "Hello, this is a test of the Fish TTS API."}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish Audio.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/documents/77adcb84-d59f-5ef9-b8a0-8b35eb42a71d) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) | `/fish/audios` | [Fish Audios Generation API Integration Guide](docs/fish_audios_api_integration_guide.md) |
| [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) | `/fish/voices` | [Fish Voices Generation API Integration Guide](docs/fish_voices_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/44c93949-1419-4a45-8db5-8a8335de7151) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |
| [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `/fish/model` | [Fish Model API Integration Guide](docs/fish_model_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
