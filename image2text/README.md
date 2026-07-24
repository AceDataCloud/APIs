# Image2Text API

Captcha-recognition API for variable-length English numeric images.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-Automation%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Image2Text](https://platform.acedata.cloud/service/image2text)

Keywords: image2text-api, captcha-recognition, ocr, numeric-captcha, image-to-text, rest-api, automation-api, Ace Data Cloud

## Why Use Image2Text on Ace Data Cloud

- Unified developer platform with one API token, billing system, and usage tracking.
- Production-ready API endpoints served from https://api.acedata.cloud.
- English integration guides, API references, and service documentation.
- Shared trial quota and consistent authentication across Ace Data Cloud services.

## Overview

Image2Text recognizes variable-length English numeric captchas from a Base64-encoded image using `/captcha/recognition/image2text`. It supports synchronous use and async polling through the shared captcha task flow described in the guide.

## Application Process

Open the Image2Text service page, create an Ace Data Cloud API token, and submit Base64 image payloads to the recognition endpoint below. Trial quota is available for first-time users.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Image2Text on Ace Data Cloud](https://platform.acedata.cloud/service/image2text)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/captcha/recognition/image2text" \
  --header "accept: application/json" \
  --header "authorization: ******" \
  --header "content-type: application/json" \
  --data '{
    "image": "iVBORw0KGgoAAAANSUhEUgAA..."
  }'
```

## APIs and Guides

Explore the supported endpoints and local integration guides for Image2Text.

| API | Path | Integration Guidance |
| ---- | ---- | -------------------- |
| Image2Text Recognition API | `/captcha/recognition/image2text` | [image2text_recognition_api_integration_guide.md](docs/image2text_recognition_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you run into issues, check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).
