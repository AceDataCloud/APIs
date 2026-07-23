# Digital English Captcha Recognition API

Digital English captcha recognition service based on deep learning technology, recognizing variable-length English numeric captchas from images.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

API home page: [Ace Data Cloud - Image2Text Captcha Recognition](https://platform.acedata.cloud/documents/captcha-recognition-image2text)

Keywords: image2text-api, captcha-recognition, captcha-solver, ocr-captcha, english-captcha, numeric-captcha, ai-api, REST API, Developer API, Ace Data Cloud

## Why Use Image2Text Captcha API on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building automation, scraping, and verification bypass products

## Overview

The Image2Text Captcha Recognition service provides an endpoint that accepts a Base64-encoded captcha image and returns the recognized text content. It supports variable-length English and numeric captchas using deep learning technology.

## Application Process

To use the Image2Text Captcha API, go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token.

There is a free quota available for first-time applicants, allowing you to use this API for free.

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
  -H 'accept: application/json' \
  -H 'authorization: ******' \
  -H 'content-type: application/json' \
  -d '{
    "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
  }'
```

## APIs and Guides

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Digital English Captcha Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-image2text) | `/captcha/recognition/image2text` | [Digital English Captcha Recognition API Integration Guide](docs/captcha_recognition_image2text_integration_guide.md) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
