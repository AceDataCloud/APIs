# Seedream Image Generation API

ByteDance Seedream AI image generation & editing service.

API home page: [Ace Data Cloud - Seedream Image Generation](https://platform.acedata.cloud/service/seedream)

Keywords: seedream-api, ai-image, image-generation, image-editing, bytedance, doubao, seededit, text-to-image, rest-api, Ace Data Cloud

## Overview

The Seedream Images API generates and edits ByteDance Seedream (Doubao) images by inputting custom parameters. Models: `doubao-seedream-3-0-t2i-250415`, `doubao-seedream-4-0-250828`, `doubao-seedream-4-5-251128`, `doubao-seedream-5-0-260128`, `doubao-seedream-5.0-lite`, and `doubao-seededit-3-0-i2i-250628` (image edit). The Seedream Tasks API queries async task status.

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/seedream/images" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{"model": "doubao-seedream-5-0-260128", "prompt": "a serene mountain lake at sunrise, photorealistic", "size": "2K"}'
```

## Models

| Model | Notes |
| ---- | ---- |
| `doubao-seedream-5-0-260128` | Latest, highest quality (推荐) |
| `doubao-seedream-5.0-lite` | Lightweight 5.0 |
| `doubao-seedream-4-5-251128` | 4.5 |
| `doubao-seedream-4-0-250828` | 4.0 |
| `doubao-seedream-3-0-t2i-250415` | 3.0 text-to-image |
| `doubao-seededit-3-0-i2i-250628` | SeedEdit 3.0 image editing |

## APIs and Guides

| API | Path | Guide |
| ---- | ---- | ---- |
| [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) | `/seedream/images` | [Integration Guide](docs/seedream_images_generation_api_integration_guide.md) |
| [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75) | `/seedream/tasks` | [Integration Guide](docs/seedream_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Docs](https://docs.acedata.cloud) · [Status](https://status.acedata.cloud) · [GitHub Org](https://github.com/AceDataCloud)
