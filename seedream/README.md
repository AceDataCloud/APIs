# Seedream Image Generation API

ByteDance Seedream AI image generation & editing service.

API home page: [Ace Data Cloud - Seedream Image Generation](https://platform.acedata.cloud/service/seedream)

Keywords: seedream-api, ai-image, image-generation, image-editing, bytedance, doubao, seededit, text-to-image, rest-api, Ace Data Cloud

## Overview

The Seedream Images API generates, edits, streams, and decomposes images with `doubao-seedream-4-0-250828`, `doubao-seedream-4-5-251128`, `doubao-seedream-5-0-260128`, and `doubao-seedream-5-0-pro-260628`. The Seedream Tasks API queries async task status.

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
| `doubao-seedream-5-0-pro-260628` | Single image, precise editing, transparent background, layer decomposition; 1K/1.5K/2K |
| `doubao-seedream-5-0-260128` / `doubao-seedream-5-0-lite-260128` | Sequential images, streaming, web search; 2K/3K/4K |
| `doubao-seedream-4-5-251128` | 4.5 |
| `doubao-seedream-4-0-250828` | 4.0 |


## Key 5.0 operations

- Generate/edit: `prompt`, optional `image`, model-specific `size`, `output_format`, and prompt optimization.
- Lite image sets: `sequential_image_generation: "auto"` plus `max_images`; input + output ≤ 15.
- Pro transparent edit: one transparent PNG, `background: "transparent"`, `output_format: "png"`.
- Pro layers: one PNG/JPEG, `layer_decomposition: true`; returns a base plus up to 16 positioned PNG layers.
- Lite streaming: `stream: true` with `Accept: application/x-ndjson`; do not combine with async/callback.

## APIs and Guides

| API | Path | Guide |
| ---- | ---- | ---- |
| [Seedream Images API](https://platform.acedata.cloud/documents/86ad30f3-0bc8-4b9b-b019-b9fa5b05672e) | `/seedream/images` | [Integration Guide](docs/seedream_images_generation_api_integration_guide.md) |
| [Seedream Tasks API](https://platform.acedata.cloud/documents/a89ab5c9-f956-42b5-a867-abb3d00d2f75) | `/seedream/tasks` | [Integration Guide](docs/seedream_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Docs](https://docs.acedata.cloud) · [Status](https://status.acedata.cloud) · [GitHub Org](https://github.com/AceDataCloud)
