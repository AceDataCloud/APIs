# Seedance Video Generation API

ByteDance Seedance AI video generation service with text, image, audio, and video multimodal input.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Seedance Video Generation](https://platform.acedata.cloud/service/seedance)

Keywords: seedance-api, ai-video, video-generation, bytedance, doubao, text-to-video, image-to-video, reference-audio, reference-video, real-person-reference, rest-api, ai-api, aivideo, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Seedance Video Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

The Seedance Videos Generation API generates official ByteDance Seedance (Doubao) videos by inputting custom parameters such as a `content` array (text, image, audio, video), `model`, `resolution`, `ratio`, and `duration`.

The Seedance 2.0 series (`doubao-seedance-2-0-260128`, `doubao-seedance-2-0-fast-260128`, `doubao-seedance-2-0-mini-260615`) adds multimodal reference inputs: real-person / character image references, reference audio, and reference video.

The Seedance Tasks API queries the execution status of tasks by inputting the task ID returned by the Seedance Videos Generation API.

## Application Process

To use the Seedance Videos Generation API, apply for the corresponding service on the [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) page. After entering the page, click the "Acquire" button.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Seedance Video Generation on Ace Data Cloud](https://platform.acedata.cloud/service/seedance)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/seedance/videos" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "doubao-seedance-2-0-260128",
    "content": [
      { "type": "text", "text": "A dancer performing contemporary ballet in a misty forest" }
    ],
    "resolution": "1080p",
    "ratio": "16:9",
    "duration": 5
  }'
```

## Models

| Model | Generation | Notes |
| ---- | ---- | ---- |
| `doubao-seedance-2-0-260128` | 2.0 | Latest generation, highest quality, multimodal reference, up to 4k (recommended) |
| `doubao-seedance-2-0-fast-260128` | 2.0 Fast | Faster 2.0, up to 720p |
| `doubao-seedance-2-0-mini-260615` | 2.0 Mini | Lightweight / most cost-effective 2.0, up to 720p |

## APIs and Guides

Explore the supported endpoints and integration guides for Seedance Video Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Seedance Videos Generation API](https://platform.acedata.cloud/documents/0083b874-4da6-40df-87e3-835b1300c1e8) | `/seedance/videos` | [Seedance Videos Generation API Integration Guide](docs/seedance_videos_generation_api_integration_guide.md) |
| [Seedance Tasks API](https://platform.acedata.cloud/documents/c09d6a1b-3cca-4f7c-add3-8c14be60da3c) | `/seedance/tasks` | [Seedance Tasks API Integration Guide](docs/seedance_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
