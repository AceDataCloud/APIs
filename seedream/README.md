# Seedream Image Generation API

ByteDance Seedream AI image generation & editing service.

API home page: [Ace Data Cloud - Seedream Image Generation](https://platform.acedata.cloud/service/seedream)

Keywords: seedream-api, ai-image, image-generation, image-editing, bytedance, doubao, seededit, text-to-image, rest-api, Ace Data Cloud

## Overview

The Seedream Images API generates and edits ByteDance Seedream (Doubao) images by inputting custom parameters. Models: `doubao-seedream-5.0-lite` (latest), `doubao-seedream-4.5`, `doubao-seedream-4.0`, `doubao-seedream-3.0-t2i`, and `doubao-seededit-3.0-i2i` (image edit). The Seedream Tasks API queries single or batch task results.

## Quick Start

```bash
curl --request POST "https://api.acedata.cloud/seedream/images" \
  --header "Authorization: ******" \
  --header "Content-Type: application/json" \
  --data '{"action": "generate", "model": "doubao-seedream-5.0-lite", "prompt": "a serene mountain lake at sunrise, photorealistic", "size": "2K"}'
```

## Models

| Model | Notes |
| ---- | ---- |
| `doubao-seedream-5.0-lite` | Latest (default) |
| `doubao-seedream-4.5` | 4.5 |
| `doubao-seedream-4.0` | 4.0 |
| `doubao-seedream-3.0-t2i` | 3.0 text-to-image |
| `doubao-seededit-3.0-i2i` | SeedEdit 3.0 image editing |

## APIs and Guides

| API | Path | Guide |
| ---- | ---- | ---- |
| [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) | `/seedream/images` | [Integration Guide](docs/seedream_images_generation_api_integration_guide.md) |
| [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75) | `/seedream/tasks` | [Integration Guide](docs/seedream_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Docs](https://docs.acedata.cloud) · [Status](https://status.acedata.cloud) · [GitHub Org](https://github.com/AceDataCloud)
