# Recognition of English numerical verification codes API

This article will introduce a Digital English Captcha Recognition API integration guide, which is based on deep learning technology and can be used to recognize variable-length English numeric captchas. It takes the content of the captcha image as input and outputs the captcha result.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Recognition of English numerical verification codes](https://platform.acedata.cloud/documents/captcha-recognition-image2text)

Keywords: image2text-api, image2text, rest-api, ai-api, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Recognition of English numerical verification codes on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

This article will introduce a Digital English Captcha Recognition API integration guide, which is based on deep learning technology and can be used to recognize variable-length English numeric captchas. It takes the content of the captcha image as input and outputs the captcha result.

## Application Process

To use the APIs in this service, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Main docs page: [Service documentation](https://platform.acedata.cloud/documents/captcha-recognition-image2text)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Recognition of English numerical verification codes.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Digital English Captcha Recognition API Integration Instructions](https://platform.acedata.cloud/documents/captcha-recognition-image2text) | `/captcha/recognition/image2text` | [Digital English Captcha Recognition API Integration Instructions](docs/captcha_recognition_image2text_api_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
