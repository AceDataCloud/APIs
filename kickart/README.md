# Kickart API

E-commerce video generation APIs for standard product videos, viral videos, and template-driven video rendering.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Kickart](https://platform.acedata.cloud/service/kickart)

Keywords: kickart-api, ecommerce-video, product-video, viral-video, template-video, ai-video, rest-api, ai-api, Ace Data Cloud

## Why Use Kickart on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

Kickart is designed for e-commerce video production. `/kickart/videos` creates standard product videos, `/kickart/viral-videos` focuses on remixing or viral-style assets, and `/kickart/template-videos` renders videos from a template plus resource list.

## Application Process

Open the Kickart service page, create your Ace Data Cloud API token, and use the endpoint-specific guides below. At the moment the upstream Docs repo only ships OpenAPI specs for Kickart, so the local guides were generated from the spec.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Kickart on Ace Data Cloud](https://platform.acedata.cloud/service/kickart)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/kickart/videos" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "duration": 15,
    "product_url": "https://example.com/products/demo",
    "language": "en",
    "aspect_ratio": "9:16",
    "prompt": "Create a short product intro video"
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Kickart.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Kickart Videos API | `/kickart/videos` | [kickart_videos_api_integration_guide.md](docs/kickart_videos_api_integration_guide.md) |
| Kickart Viral Videos API | `/kickart/viral-videos` | [kickart_viral_videos_api_integration_guide.md](docs/kickart_viral_videos_api_integration_guide.md) |
| Kickart Template Videos API | `/kickart/template-videos` | [kickart_template_videos_api_integration_guide.md](docs/kickart_template_videos_api_integration_guide.md) |

> Note: the Kickart English guides in this repository were generated from the upstream OpenAPI spec because no upstream `en/guides/kickart/` files are currently available.

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
