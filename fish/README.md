# Fish Audio API

Fish Audio voice cloning and text-to-speech service.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Fish Audio](https://platform.acedata.cloud/service/fish)

Keywords: fish-audio-api, fish-tts-api, voice-cloning, text-to-speech, tts-api, ai-voice, rest-api, ai-api, aiaudio, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Fish Audio on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Fish Audio API provides fully compatible access to Fish Audio's official OpenAPI services, including:

- **Fish TTS API** (`/fish/tts`): Text-to-speech synthesis using Fish Audio models. Compatible with the official `https://api.fish.audio/v1/tts` endpoint — migrate by swapping only the base URL and token.
- **Fish Model API** (`/fish/model`): Create and query voice clone models based on audio samples.
- **Fish Audios Generation API** (`/fish/audios`): Clone a voice by providing a prompt and a voice ID.
- **Fish Voices Generation API** (`/fish/voices`): Create a new voice model by uploading an audio sample URL.
- **Fish Tasks API** (`/fish/tasks`): Query the execution status of audio generation tasks by task ID.

## Application Process

To use the Fish TTS API, visit the [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) page and click the "Acquire" button to obtain the credentials needed for the request:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not logged in or registered, you will be automatically redirected to the login page. After logging in, you will automatically return to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

To generate speech from text, send a `POST` request to `/fish/tts` with the `text` field. Optionally specify a voice model via the `model` header and a cloned voice via `reference_id`:

```shell
curl -X POST 'https://api.acedata.cloud/fish/tts' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -H 'model: s2-pro' \
  -d '{
    "text": "Hello, this is a test of the Fish TTS API."
  }'
```

After the call, the returned result is as follows:

```json
{
  "audio_url": "https://platform.r2.fish.audio/task/8a72ff9840234006a9f74cb2fa04f978.mp3"
}
```

Main request parameters:

- `text`: The text to synthesize into speech.
- `reference_id`: The ID of a cloned voice model to use (returned from `/fish/model` or `/fish/voices`).
- `format`: Audio format, e.g. `mp3`.
- `sample_rate`: Sample rate in Hz, e.g. `44100`.
- `callback_url`: Optional asynchronous callback URL.

The `model` HTTP header selects the TTS engine: `s1` or `s2-pro` (default: `s2-pro`).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Fish Audio on Ace Data Cloud](https://platform.acedata.cloud/service/fish)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/fish/tts" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --header "model: s2-pro" \
  --data '{"text": "Hello from Fish Audio!"}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Fish Audio.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Fish TTS API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `/fish/tts` | [Fish TTS API Integration Guide](docs/fish_tts_api_integration_guide.md) |
| [Fish Model API](https://platform.acedata.cloud/services/caf99abc-ddcf-4714-b2a5-862d9b469509) | `/fish/model` | [Fish Model API Integration Guide](docs/fish_model_api_integration_guide.md) |
| [Fish Audios Generation API](https://platform.acedata.cloud/documents/e681b715-54fd-4464-a59a-d7f14500e095) | `/fish/audios` | [Fish Audios Generation API Integration Guide](docs/fish_audios_api_integration_guide.md) |
| [Fish Voices Generation API](https://platform.acedata.cloud/documents/55e61b64-ac7d-4710-a7f1-57a4ba786b17) | `/fish/voices` | [Fish Voices Generation API Integration Guide](docs/fish_voices_api_integration_guide.md) |
| [Fish Tasks API](https://platform.acedata.cloud/documents/44c93949-1419-4a45-8db5-8a8335de7151) | `/fish/tasks` | [Fish Tasks API Integration Guide](docs/fish_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
