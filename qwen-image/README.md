# Qwen Image API

Qwen Image 3 AI image generation and editing service on Ace Data Cloud.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Qwen Image](https://platform.acedata.cloud/service/qwen-image)

Keywords: qwen-image-api, ai-image, image-generation, image-editing, qwen-image-3, text-to-image, rest-api, ai-api, Ace Data Cloud

## Overview

The Qwen Image Images API generates or edits images with `qwen-image-3.0` and `qwen-image-3.0-pro`. It accepts a text prompt, optional source image URLs, generation count, image size, prompt extension controls, seed, watermark, async mode, and callback URL.

The Qwen Image Tasks API queries the execution status of asynchronous image tasks by task ID.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Qwen Image on Ace Data Cloud](https://platform.acedata.cloud/service/qwen-image)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/qwen-image/images" \
  --header "Authorization: YOUR_API_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen-image-3.0",
    "prompt": "a serene mountain lake at sunrise, photorealistic",
    "size": "1024*1024"
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Qwen Image Images API](https://platform.acedata.cloud/documents/qwen-image-images) | `/qwen-image/images` | [Qwen Image Images API Integration Guide](docs/qwen_image_images_api_integration_guide.md) |
| [Qwen Image Tasks API](https://platform.acedata.cloud/documents/qwen-image-tasks) | `/qwen-image/tasks` | [Qwen Image Tasks API Integration Guide](docs/qwen_image_tasks_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
